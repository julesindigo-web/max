#!/usr/bin/env python3
"""Deterministic AST doc-sync inventory and drift checker (stdlib only).

Usage:
  python3 ast-doc-sync.py inventory <target-dir>
  python3 ast-doc-sync.py check <target-dir> <baseline.json>

Commands:
  inventory - walk target dir for *.py and *.{js,ts,jsx,tsx}, print JSON inventory.
  check     - compare current inventory to baseline file, print drift report.

Inventory output (stdout, exit 0):
  {"files": N, "symbols": [{"file": str, "name": str, "args": [str], "line": int}]}

Check output (stdout):
  {"added": [...], "removed": [...], "changed": [...], "in_sync": bool}
  exit 0 when in sync, exit 1 on drift, exit 2 on usage or I/O errors.
"""
import ast
import json
import os
import re
import sys


JS_TS_EXTS = (".js", ".ts", ".jsx", ".tsx")
PY_EXT = ".py"

# Match common exported symbols in JS/TS without external parsers.
JS_EXPORT_RE = re.compile(
    r"""^\s*export\s+(?:default\s+)?"""
    r"""(?:async\s+)?"""
    r"""(?:function\s+(?P<func>[A-Za-z_$][\w$]*)\s*(?P<fargs>\([^)]*\))"""
    r"""|class\s+(?P<class>[A-Za-z_$][\w$]*)"""
    r"""|(?:const|let|var)\s+(?P<const>[A-Za-z_$][\w$]*)\s*=)""",
    re.MULTILINE,
)


def eprint(msg):
    print(msg, file=sys.stderr)


def parse_py_file(path, rel):
    symbols = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            src = fh.read()
        tree = ast.parse(src, filename=path)
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        eprint("warning: skipping unparsable python file %s: %s" % (rel, exc))
        return symbols

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.stack = []

        def visit_ClassDef(self, node):
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def _record(self, node):
            qname = ".".join(self.stack + [node.name]) if self.stack else node.name
            args = [a.arg for a in node.args.args]
            # posonly/kwonly/vararg/kwarg names are disjoint from regular args in valid
            # Python (duplicates are SyntaxError, unparsable earlier); append unconditionally.
            for a in node.args.posonlyargs:
                args.append(a.arg)
            for a in node.args.kwonlyargs:
                args.append(a.arg)
            if node.args.vararg:
                args.append(node.args.vararg.arg)
            if node.args.kwarg:
                args.append(node.args.kwarg.arg)
            symbols.append(
                {"file": rel, "name": qname, "args": args, "line": node.lineno}
            )

        def visit_FunctionDef(self, node):
            self._record(node)
            self.stack.append(node.name)
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node):
            self._record(node)
            self.stack.append(node.name)
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            self.stack.pop()

    Visitor().visit(tree)
    return symbols


def parse_js_ts_file(path, rel):
    symbols = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        text = "".join(lines)
    except (OSError, UnicodeDecodeError) as exc:
        eprint("warning: skipping unreadable file %s: %s" % (rel, exc))
        return symbols
    for m in JS_EXPORT_RE.finditer(text):
        name = m.group("func") or m.group("class") or m.group("const")
        # Regex guarantees one group matched; no empty-name case.
        # Compute 1-indexed line number from match offset.
        line = text.count("\n", 0, m.start()) + 1
        args = []
        fargs = m.group("fargs")
        if fargs:
            inner = fargs.strip()[1:-1].strip() if len(fargs.strip()) >= 2 else ""
            if inner:
                for part in inner.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    # Strip TS types, defaults, and rest markers.
                    part = part.lstrip("...")
                    part = part.split("=")[0].strip()
                    part = part.split(":")[0].strip()
                    if part:
                        args.append(part)
        symbols.append({"file": rel, "name": name, "args": args, "line": line})
    return symbols


def build_inventory(target_dir):
    symbols = []
    file_count = 0
    for root, dirs, files in os.walk(target_dir):
        dirs.sort()
        for fn in sorted(files):
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, target_dir)
            lower = fn.lower()
            if lower.endswith(PY_EXT):
                file_count += 1
                symbols.extend(parse_py_file(full, rel))
            elif lower.endswith(JS_TS_EXTS):
                file_count += 1
                symbols.extend(parse_js_ts_file(full, rel))
    symbols.sort(key=lambda s: (s["file"], s["name"], s["line"]))
    return {"files": file_count, "symbols": symbols}


def cmd_inventory(target_dir):
    if not os.path.isdir(target_dir):
        eprint("error: target directory does not exist or is not a directory: %s" % target_dir)
        return 2
    inv = build_inventory(target_dir)
    print(json.dumps(inv, indent=2, sort_keys=False))
    return 0


def symbol_key(sym):
    return sym.get("file", "") + "::" + sym.get("name", "")


def cmd_check(target_dir, baseline_path):
    if not os.path.isdir(target_dir):
        eprint("error: target directory does not exist or is not a directory: %s" % target_dir)
        return 2
    try:
        with open(baseline_path, "r", encoding="utf-8") as fh:
            baseline = json.load(fh)
    except FileNotFoundError:
        eprint("error: baseline file not found: %s" % baseline_path)
        return 2
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        eprint("error: invalid baseline JSON %s: %s" % (baseline_path, exc))
        return 2
    if not isinstance(baseline, dict) or "symbols" not in baseline:
        eprint("error: invalid baseline JSON %s: expected object with symbols list" % baseline_path)
        return 2
    current = build_inventory(target_dir)
    base_map = {}
    for s in baseline.get("symbols", []):
        base_map[symbol_key(s)] = s
    cur_map = {}
    for s in current["symbols"]:
        cur_map[symbol_key(s)] = s
    added = sorted(
        [cur_map[k] for k in cur_map if k not in base_map],
        key=lambda s: (s["file"], s["name"]),
    )
    removed = sorted(
        [base_map[k] for k in base_map if k not in cur_map],
        key=lambda s: (s["file"], s["name"]),
    )
    changed = []
    for k in sorted(set(cur_map) & set(base_map)):
        b = base_map[k]
        c = cur_map[k]
        if b.get("args") != c.get("args") or b.get("line") != c.get("line"):
            changed.append(
                {
                    "key": k,
                    "baseline": b,
                    "current": c,
                }
            )
    changed.sort(key=lambda e: e["key"])
    report = {
        "added": added,
        "removed": removed,
        "changed": changed,
        "in_sync": not added and not removed and not changed,
    }
    print(json.dumps(report, indent=2, sort_keys=False))
    return 0 if report["in_sync"] else 1


def main(argv):
    if len(argv) < 3:
        eprint("usage: ast-doc-sync.py inventory <target-dir>")
        eprint("       ast-doc-sync.py check <target-dir> <baseline.json>")
        return 2
    cmd = argv[1]
    if cmd == "inventory" and len(argv) == 3:
        return cmd_inventory(argv[2])
    if cmd == "check" and len(argv) == 4:
        return cmd_check(argv[2], argv[3])
    eprint("usage: ast-doc-sync.py inventory <target-dir>")
    eprint("       ast-doc-sync.py check <target-dir> <baseline.json>")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
