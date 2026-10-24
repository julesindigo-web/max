"""Focused suite for security-vulnerability-auditor (SVA) coverage.

Covers SVA-semantic paths that generic gates check only structurally:
OWASP Top 10 checklist completeness, remediation mapping with verification,
trigger family span (sec-*), SVA-shaped findings through the real
audit-findings contract validator, and a self secrets-scan of the SVA skill
tree. Deterministic, offline, fail-closed; stdlib only.
"""
from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
SVA = ROOT / "security-vulnerability-auditor"
CHECKLISTS = SVA / "references" / "security-checklists.md"
REMEDIATION = SVA / "references" / "remediation-security.md"
SKILL = SVA / "SKILL.md"
MATRIX = ROOT / "evaluation" / "trigger-evaluation-matrix.json"
ALIASES = ROOT / "i18n" / "id" / "TRIGGER-ALIASES-ID.md"

spec = importlib.util.spec_from_file_location(
    "paf_sva", str(ROOT / "skills-create-excellence" / "scripts" / "process-audit-feedback.py"))
PAF = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PAF)

# Same high-precision set as validate-plugins.sh session-log scan.
SECRET_PATTERNS = [
    r"-----BEGIN ([A-Z ]*PRIVATE KEY|OPENSSH PRIVATE KEY)-----",
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"sk-ant-[A-Za-z0-9-]{10,}",
    r"xox[bpas]-[A-Za-z0-9-]+",
]


def sva_finding(fid, title, severity, evidence, status="open",
                evidence_status="verified", severity_basis="observed_impact",
                confidence="high", recurrence_count=0):
    return {
        "id": fid,
        "title": title,
        "category": "project.security",
        "severity": severity,
        "status": status,
        "evidence": evidence,
        "source_artifact": "security-vulnerability-auditor/SKILL.md",
        "recurrence_count": recurrence_count,
        "evidence_status": evidence_status,
        "confidence": confidence,
        "verification_method": "Direct read of cited file plus offline retest per remediation-security.md",
        "as_of_context": "SVA skill v1.0.0, set v2.0.0, 2026-10-15",
        "impact_rationale": ("Reachable exposure confirmed by cited evidence; "
                             "exploitability ranked per SVA triage order."),
        "severity_basis": severity_basis,
    }


def sva_event(findings):
    return {
        "schema_version": "1.1",
        "audit_id": "AUD-2026-10-15-SVA-001",
        "audited_at": "2026-10-15T12:00:00+00:00",
        "project": "sva-suite-fixture",
        "findings": findings,
    }


class SvaChecklistTests(unittest.TestCase):
    def test_checklist_covers_owasp_top10(self):
        text = CHECKLISTS.read_text(encoding="utf-8")
        required = [
            "Injection", "Broken access control", "Cryptographic failures",
            "Insecure design", "Security misconfiguration", "Vulnerable components",
            "Auth failures", "Integrity failures", "Logging failures", "SSRF",
        ]
        for category in required:
            self.assertIn(category, text, f"OWASP category missing: {category}")

    def test_checklist_covers_secrets_rbac_data(self):
        text = CHECKLISTS.read_text(encoding="utf-8")
        for marker in ("## B. Secrets Leakage", "## C. RBAC and ABAC Review", "## D. Data Protection"):
            self.assertIn(marker, text, f"checklist section missing: {marker}")
        self.assertIn("90 days", text, "rotation runbook freshness requirement missing")
        self.assertIn("least privilege", text.lower(), "least-privilege requirement missing")
        self.assertIn("TLS 1.2", text, "TLS floor requirement missing")


class SvaRemediationTests(unittest.TestCase):
    def test_remediation_maps_to_checklist_with_verification(self):
        text = REMEDIATION.read_text(encoding="utf-8")
        sections = [
            "Rotate Leaked Secrets", "Fix Injection", "Repair Access Control",
            "Harden Crypto and Transport", "Update Vulnerable Dependencies",
            "Normalize and Close",
        ]
        for section in sections:
            self.assertIn(section, text, f"remediation section missing: {section}")
        # Every fix path must state its verification (SVA "Fix with verification").
        blocks = re.split(r"^## \d+\. ", text, flags=re.M)[1:]
        self.assertEqual(len(blocks), 6, "expected 6 numbered remediation sections")
        for block in blocks:
            self.assertRegex(block, r"[Vv]erif", "remediation section lacks verification step")

    def test_remediation_states_scan_bars(self):
        text = REMEDIATION.read_text(encoding="utf-8")
        self.assertIn("at least 2 scanners", text, "secrets closure bar (2-scanner zero hits) missing")
        self.assertIn("at least 5 attack strings", text, "injection retest bar missing")
        self.assertIn("two distinct low-privilege accounts", text, "IDOR retest bar missing")
        self.assertIn("zero known high-severity reachable issues", text, "dependency closure bar missing")


class SvaWiringTests(unittest.TestCase):
    def test_skill_wires_references(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/security-checklists.md", skill)
        self.assertIn("references/remediation-security.md", skill)
        self.assertIn("project-artifact-auditor@>=2.0.0", skill, "depends-on auditor missing")
        self.assertTrue(CHECKLISTS.is_file() and REMEDIATION.is_file())
        self.assertLessEqual(int(skill.count("\n")) + 1, 500, "SKILL.md exceeds 500-line budget")


class SvaTriggerTests(unittest.TestCase):
    def test_triggers_span_security_families(self):
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        sva = matrix["skills"]["security-vulnerability-auditor"]
        pos, neg = sva["positive"], sva["negative"]
        self.assertEqual(len(pos), 5, "SVA needs 5 positive cases")
        self.assertEqual(len(neg), 5, "SVA needs 5 negative cases")
        ids = [c["id"] for c in pos + neg]
        self.assertEqual(len(set(ids)), 10, "SVA case IDs must be unique")
        self.assertTrue(all(i.startswith("sec-") for i in ids))
        joined = " ".join(c.get("prompt", "") for c in pos).lower()
        families = {
            "owasp/injection/access": ["owasp", "injection", "access control"],
            "dependency": ["dependenc", "vulnerab", "pinned"],
            "secrets": ["secret", "token", "private key"],
            "privilege": ["privilege", "escalation", "authorization"],
            "auth": ["authentication", "rate limiting"],
        }
        for family, keywords in families.items():
            self.assertTrue(any(k in joined for k in keywords),
                            f"SVA positives miss family: {family}")
        neg_joined = " ".join(c.get("prompt", "") for c in neg).lower()
        for keyword in ("owasp", "vulnerab", "secret", "injection", "auth"):
            self.assertNotIn(keyword, neg_joined, f"negative leaks security signal: {keyword}")

    def test_indonesian_aliases_cover_sva(self):
        text = ALIASES.read_text(encoding="utf-8").lower()
        self.assertIn("owasp", text, "ID alias for OWASP sweep missing")
        self.assertIn("secret", text, "ID alias for secrets review missing")


class SvaContractTests(unittest.TestCase):
    def test_sva_findings_validate_through_contract(self):
        event = sva_event([
            sva_finding("SVA-INJ-001", "String-built SQL query on login",
                        "Critical", "auth/login.py:42 builds query via f-string; payload retest bypassed auth.",
                        severity_basis="observed_impact"),
            sva_finding("SVA-SEC-001", "Committed AWS key in sample config",
                        "Critical", "config/sample.env:3 holds live-format key; rotation runbook started.",
                        severity_basis="mandatory_control_gap"),
            sva_finding("SVA-DEP-001", "Reachable vulnerable transitive dependency",
                        "Major", "Call graph shows import of libfoo 1.2.3 (CVE fixture); upgrade to 1.2.4 pinned.",
                        evidence_status="inference", confidence="medium",
                        severity_basis="conditional_risk"),
        ])
        validated = PAF.validate_event(event)
        self.assertEqual(len(validated["findings"]), 3)
        self.assertTrue(all(f["category"] == "project.security" for f in validated["findings"]))

    def test_sva_unknown_critical_requires_conditional_risk(self):
        bad = sva_event([sva_finding(
            "SVA-UNK-001", "Possible SSRF in webhook fetcher", "Critical",
            "Outbound URL unsanitized; reachability not yet proven.",
            evidence_status="unknown_untested", severity_basis="observed_impact")])
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad)
        ok = sva_event([dict(
            sva_finding("SVA-UNK-001", "Possible SSRF in webhook fetcher", "Critical",
                        "Outbound URL unsanitized; reachability not yet proven.",
                        evidence_status="unknown_untested", severity_basis="conditional_risk"),
            impact_rationale=("If the fetcher follows redirects, internal addresses could be reached; "
                              "conditional on redirect behavior."))])
        self.assertEqual(len(PAF.validate_event(ok)["findings"]), 1)

    def test_sva_finding_missing_calibration_fails_closed(self):
        event = sva_event([sva_finding("SVA-CAL-001", "Weak password hashing",
                                       "Major", "auth/hash.py:9 uses single-round hash.")])
        del event["findings"][0]["verification_method"]
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(event)


class SvaSelfScanTests(unittest.TestCase):
    def test_secret_patterns_are_non_vacuous(self):
        # Guards the self-scan below against vacuous pass: each pattern must
        # match a runtime-constructed exemplar (never committed to disk).
        exemplars = {
            0: "-----BEGIN RSA PRIVATE KEY-----",
            1: "AKIA" + "I" * 16,
            2: "ghp_" + "a" * 20,
            3: "sk-ant-" + "x" * 10,
            4: "xoxb-" + "1" * 9,
        }
        for index, pattern in enumerate(SECRET_PATTERNS):
            self.assertRegex(exemplars[index], pattern, f"pattern {index} matches nothing")

    def test_sva_skill_tree_holds_no_committed_secrets(self):
        compiled = [re.compile(p) for p in SECRET_PATTERNS]
        hits = []
        for path in sorted(SVA.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for rx in compiled:
                if rx.search(text):
                    hits.append(f"{path.relative_to(ROOT)}:{rx.pattern[:24]}")
        self.assertEqual(hits, [], f"committed secret patterns in SVA tree: {hits}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
