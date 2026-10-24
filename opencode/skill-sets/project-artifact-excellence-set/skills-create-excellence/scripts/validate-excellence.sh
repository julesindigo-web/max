#!/usr/bin/env bash
# Deterministic structural + excellence validation for one skill or a skill set.
# Usage: validate-excellence.sh <skill-or-set-directory>
# Required gates fail closed. Exit codes: 0 = passed; 1 = failed.
# Side effects: read-only; no files are changed. Requires Bash and standard Unix tools.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
METRIC_VALIDATOR="$SCRIPT_DIR/../../validation/validate_metric_specs.py"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
info() { printf 'INFO: %s\n' "$*"; }
pass() { printf 'PASS: %s\n' "$*"; }

validate_metric_bullets() {
  local metrics_content="$1" context="$2" metric_count required_dimension metric_line metric_prefix metric_text normalized_metrics=""
  local -a required_metric_dimensions=("Trigger performance" "Task completion" "Context-token efficiency" "Time-to-working-skill" "Residual defect density")
  metric_count=$(grep -cE '^[*-][[:space:]]+' <<< "$metrics_content" || true)
  (( metric_count >= 5 )) || fail "At least five success metrics are required; found $metric_count: $context"
  while IFS= read -r metric_line; do
    [[ "$metric_line" =~ ^([-*][[:space:]]+)(.*)$ ]] || continue
    metric_prefix="${BASH_REMATCH[1]}"
    metric_text="${BASH_REMATCH[2]}"
    metric_text=${metric_text#\"}; metric_text=${metric_text%\"}
    metric_text=${metric_text#\'}; metric_text=${metric_text%\'}
    normalized_metrics+="${metric_prefix}${metric_text}"$'\n'
    [[ "$metric_text" =~ (≥|≤|>=|<=|[0-9]+|%|percent|within|at[[:space:]]+least|at[[:space:]]+most|zero|per[[:space:]]) ]] || fail "Each success metric must state a measurable target, unit, or explicit bound: $metric_text ($context)"
  done <<< "$metrics_content"
  for required_dimension in "${required_metric_dimensions[@]}"; do
    grep -qiE "^[-*][[:space:]]+(\*\*)?$required_dimension(\*\*)?([[:space:]:—-]|$)" <<< "$normalized_metrics" || fail "Required metric dimension '$required_dimension' is missing from Success Metrics: $context"
  done
}

[[ $# -eq 1 ]] || fail "Usage: $0 <skill-or-set-directory>"
TARGET=${1%/}
[[ -n "$TARGET" ]] || TARGET="/"
[[ -d "$TARGET" ]] || fail "Directory does not exist: $TARGET"

# Validate one SKILL.md without depending on a machine-specific external validator.
validate_skill() {
  local skill_dir="$1" skill_file="$1/SKILL.md" base frontmatter_end line key value
  local name='' description='' metadata_version='' name_count=0 description_count=0 metadata_count=0 metadata_version_count=0 line_count=0 in_metadata=false
  local -a allowed_keys=(name description license compatibility metadata allowed-tools user-invocable)
  local allowed found

  [[ -f "$skill_file" ]] || fail "Missing SKILL.md in: $skill_dir"
  base=$(basename "$skill_dir")
  [[ "$(head -n 1 "$skill_file")" == '---' ]] || fail "Frontmatter must start on line 1 with ---: $skill_file"
  frontmatter_end=$(awk 'NR > 1 && $0 == "---" { print NR; exit }' "$skill_file")
  [[ -n "$frontmatter_end" ]] || fail "Frontmatter closing --- not found: $skill_file"
  (( frontmatter_end > 2 )) || fail "Frontmatter is empty: $skill_file"

  # Parse top-level frontmatter keys; nested metadata keys are allowed under metadata:.
  # Use a temporary file instead of process substitution for portability (environments without /dev/fd).
  frontmatter_tmp=$(mktemp)
  sed -n "2,$((frontmatter_end - 1))p" "$skill_file" > "$frontmatter_tmp" || { rm -f "$frontmatter_tmp"; fail "Failed to extract frontmatter: $skill_file"; }
  while IFS= read -r line; do
    [[ -z "${line//[[:space:]]/}" ]] && continue
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    # Capture metadata.version while ignoring other nested YAML content.
    if [[ "$line" =~ ^[[:space:]] ]]; then
      if [[ "$in_metadata" == true && "$line" =~ ^[[:space:]]{2}version:[[:space:]]*(.*)$ ]]; then
        ((metadata_version_count+=1))
        metadata_version="${BASH_REMATCH[1]}"
      fi
      continue
    fi
    in_metadata=false
    [[ "$line" =~ ^([A-Za-z0-9_-]+):[[:space:]]*(.*)$ ]] || { rm -f "$frontmatter_tmp"; fail "Invalid frontmatter line: $line"; }
    key=${BASH_REMATCH[1]}
    value=${BASH_REMATCH[2]}

    found=false
    for allowed in "${allowed_keys[@]}"; do
      [[ "$key" == "$allowed" ]] && found=true && break
    done
    [[ "$found" == true ]] || { rm -f "$frontmatter_tmp"; fail "Unknown top-level frontmatter key '$key' in $skill_file (put custom keys under metadata)"; }

    case "$key" in
      name)
        ((name_count+=1))
        (( name_count == 1 )) || { rm -f "$frontmatter_tmp"; fail "Duplicate frontmatter key: name"; }
        name="$value"
        ;;
      description)
        ((description_count+=1))
        (( description_count == 1 )) || { rm -f "$frontmatter_tmp"; fail "Duplicate frontmatter key: description"; }
        description="$value"
        ;;
      metadata)
        ((metadata_count+=1))
        (( metadata_count == 1 )) || { rm -f "$frontmatter_tmp"; fail "Duplicate frontmatter key: metadata"; }
        [[ -z "$value" ]] || { rm -f "$frontmatter_tmp"; fail "Frontmatter metadata must be a nested map: $skill_file"; }
        in_metadata=true
        ;;
    esac
  done < "$frontmatter_tmp"
  rm -f "$frontmatter_tmp"

  (( name_count == 1 )) || fail "Required frontmatter key 'name' is missing: $skill_file"
  (( description_count == 1 )) || fail "Required frontmatter key 'description' is missing: $skill_file"
  [[ -n "$name" ]] || fail "Frontmatter name is empty: $skill_file"
  [[ "$name" != \"* && "$name" != *\" && "$name" != \'* && "$name" != *\' ]] || fail "Frontmatter name must be an unquoted scalar: $skill_file"
  [[ ${#name} -ge 2 && ${#name} -le 64 ]] || fail "Skill name must be 2-64 characters: $skill_file"
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail "Skill name must be lowercase kebab-case without consecutive hyphens: $name"
  [[ "$name" == "$base" ]] || fail "Skill name '$name' does not match directory name '$base'"

  [[ -n "$description" ]] || fail "Frontmatter description is empty: $skill_file"
  (( metadata_count == 1 )) || fail "Required frontmatter metadata map is missing: $skill_file"
  (( metadata_version_count == 1 )) || fail "metadata.version must be present exactly once: $skill_file"
  metadata_version=${metadata_version#\"}; metadata_version=${metadata_version%\"}
  metadata_version=${metadata_version#\'}; metadata_version=${metadata_version%\'}
  [[ "$metadata_version" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$ ]] || fail "metadata.version must follow semantic versioning: $skill_file"
  [[ "$description" != \"* && "$description" != *\" && "$description" != \'* && "$description" != *\' ]] || fail "Description must be an unquoted plain scalar: $skill_file"
  (( ${#description} <= 1024 )) || fail "Description exceeds 1024 characters: $skill_file"
  [[ "$description" != *': '* ]] || fail "Description must not contain colon followed by space: $skill_file"
  [[ "$description" != *'<'* && "$description" != *'>'* ]] || fail "Description must not contain angle brackets: $skill_file"
  [[ ! "$description" =~ [Tt][Oo][Dd][Oo] ]] || fail "Description must not contain TODO: $skill_file"
  grep -qiE 'use when|use for|when user|when .*' <<< "$description" || fail "Description must explain when to use the skill: $skill_file"
  grep -qi 'trigger' <<< "$description" || fail "Description must include trigger language/examples: $skill_file"

  # Body must be nonempty and free of unfinished TODO placeholders.
  local body
  body=$(tail -n "+$((frontmatter_end + 1))" "$skill_file")
  [[ -n "${body//[[:space:]]/}" ]] || fail "Skill body is empty: $skill_file"
  if grep -qiE 'TODO[[:space:]]*(—|-|:)' <<< "$body"; then
    fail "Body still contains TODO placeholders: $skill_file"
  fi

  # Success metrics are required, measurable, and use the single five-metric standard.
  local metrics_file metrics_content
  metrics_file=$(mktemp)
  awk '
    /^##[[:space:]]+Success Metrics[[:space:]]*$/ { in_metrics=1; found=1; next }
    in_metrics && /^##[[:space:]]+/ { exit }
    in_metrics && /^[-*][[:space:]]+/ { print }
    END { if (!found) exit 2 }
  ' "$skill_file" > "$metrics_file" || { rm -f "$metrics_file"; fail "Required '## Success Metrics' section is missing: $skill_file"; }
  metrics_content=$(cat "$metrics_file")
  rm -f "$metrics_file"
  validate_metric_bullets "$metrics_content" "$skill_file"
  # Required quality-attribute and human-factors coverage is a gate, not a warning.
  local body_prose
  body_prose=$(grep -viE '^#{1,6}[[:space:]]' <<< "$body" || true)
  grep -qiE 'quality[- ]attributes?' <<< "$body_prose" || fail "Quality-attribute coverage is required: $skill_file"
  grep -qiE '^#{1,4}[[:space:]].*quality[- ]attributes?' <<< "$body" || fail "A dedicated Quality Attributes section is required: $skill_file"
  grep -qiE 'human factors?|cognitive|usability|accessibility|inclusive design' <<< "$body_prose" || fail "Human-factors coverage is required: $skill_file"
  grep -qiE '^#{1,4}[[:space:]].*(human factors?|usability|accessibility)' <<< "$body" || fail "A dedicated Human Factors / Usability / Accessibility section is required: $skill_file"

  # Packaged sets enforce semantically valid metric contracts, not just numeric presence.
  if [[ -f "$METRIC_VALIDATOR" ]]; then
    python3 "$METRIC_VALIDATOR" --skill "$skill_file" || fail "Semantic metric specification validation failed: $skill_file"
  fi


  line_count=$(wc -l < "$skill_file" | tr -d '[:space:]')
  (( line_count <= 500 )) || fail "SKILL.md has $line_count lines; limit is 500: $skill_file"

  # Run the canonical validator too when configured or installed. The built-in
  # checks above remain mandatory if the external validator is unavailable.
  local external_validator="${STRUCTURAL_VALIDATOR:-/root/.grok/skills/skill-creator/scripts/validate-skill.sh}"
  if [[ -n "${STRUCTURAL_VALIDATOR:-}" && ! -f "$external_validator" ]]; then
    fail "STRUCTURAL_VALIDATOR is set but file does not exist: $external_validator"
  fi
  if [[ -f "$external_validator" ]]; then
    bash "$external_validator" "$skill_dir" || fail "External structural validation failed for $skill_dir"
  else
    info "External structural validator not installed; built-in structural checks were applied to $skill_file"
  fi
  pass "Skill validated: $name"
}

if [[ -f "$TARGET/SKILL.md" ]]; then
  validate_skill "$TARGET"
  exit 0
fi

# Skill-set entry: validate the declared members regardless of whether the set uses
# a conventional skills/ directory or keeps member directories at the set root.
if [[ -f "$TARGET/SET.md" || -f "$TARGET/manifest.yaml" ]]; then
  [[ -n "$(find "$TARGET" -maxdepth 1 -type f \( -name SET.md -o -name manifest.yaml \) -print -quit)" ]] || fail "Skill-set marker not found"
  member_count=0
  if [[ -f "$TARGET/manifest.yaml" ]]; then
    manifest_file="$TARGET/manifest.yaml"
    grep -qE '^name:[[:space:]]*[^[:space:]#]+' "$manifest_file" || fail "Set manifest requires a non-empty top-level name: $manifest_file"
    grep -qE '^version:[[:space:]]*[^[:space:]#]+' "$manifest_file" || fail "Set manifest requires a non-empty top-level version: $manifest_file"
    grep -qE '^members:[[:space:]]*$' "$manifest_file" || fail "Set manifest requires a members list: $manifest_file"
    set_metrics_file=$(mktemp)
    awk '
      /^success-metrics:[[:space:]]*$/ { in_metrics=1; found=1; next }
      in_metrics && /^[^[:space:]]/ { exit }
      in_metrics && /^[[:space:]]+-[[:space:]]+/ { sub(/^[[:space:]]*/, ""); print }
      END { if (!found) exit 2 }
    ' "$manifest_file" > "$set_metrics_file" || { rm -f "$set_metrics_file"; fail "Set manifest requires a success-metrics list: $manifest_file"; }
    set_metrics_content=$(cat "$set_metrics_file")
    rm -f "$set_metrics_file"
    validate_metric_bullets "$set_metrics_content" "$manifest_file"

    member_paths_file=$(mktemp)
    awk '
      /^members:[[:space:]]*$/ { in_members=1; next }
      in_members && /^[^[:space:]]/ { exit }
      in_members && /^[[:space:]]+path:[[:space:]]*/ {
        sub(/^[[:space:]]+path:[[:space:]]*/, "")
        gsub(/^"|"$/, "")
        gsub(/^\047|\047$/, "")
        print
      }
    ' "$manifest_file" > "$member_paths_file"
    [[ -s "$member_paths_file" ]] || { rm -f "$member_paths_file"; fail "Set manifest members must declare path values: $manifest_file"; }
    seen_member_paths_file=$(mktemp)
    : > "$seen_member_paths_file"
    while IFS= read -r member_path; do
      [[ -n "$member_path" ]] || continue
      [[ "$member_path" != /* && "/$member_path/" != *"/../"* && "/$member_path/" != *"/./"* ]] || { rm -f "$member_paths_file"; fail "Unsafe or non-relative member path in manifest: $member_path"; }
      if grep -Fxq -- "$member_path" "$seen_member_paths_file"; then rm -f "$member_paths_file" "$seen_member_paths_file"; fail "Duplicate member path in manifest: $member_path"; fi
      printf '%s\n' "$member_path" >> "$seen_member_paths_file"
      member_dir="$TARGET/$member_path"
      [[ -d "$member_dir" && -f "$member_dir/SKILL.md" ]] || { rm -f "$member_paths_file"; fail "Declared set member is missing SKILL.md: $member_path"; }
      ((member_count+=1))
      validate_skill "$member_dir"
    done < "$member_paths_file"
    rm -f "$member_paths_file" "$seen_member_paths_file"
    (( member_count > 0 )) || fail "No valid member skills were declared in $manifest_file"
    if [[ -f "$METRIC_VALIDATOR" ]]; then
      python3 "$METRIC_VALIDATOR" --root "$TARGET" || fail "Semantic metric specification validation failed for set: $TARGET"
    fi
  else
    # SET.md-only compatibility mode retains the conventional skills/ layout.
    set_metrics_file=$(mktemp)
    awk '
      /^##[[:space:]]+Success Metrics[[:space:]]*$/ { in_metrics=1; found=1; next }
      in_metrics && /^##[[:space:]]+/ { exit }
      in_metrics && /^[-*][[:space:]]+/ { print }
      END { if (!found) exit 2 }
    ' "$TARGET/SET.md" > "$set_metrics_file" || { rm -f "$set_metrics_file"; fail "SET.md requires a '## Success Metrics' section: $TARGET/SET.md"; }
    set_metrics_content=$(cat "$set_metrics_file")
    rm -f "$set_metrics_file"
    validate_metric_bullets "$set_metrics_content" "$TARGET/SET.md"
    [[ -d "$TARGET/skills" ]] || fail "SET.md-only skill set must contain a skills/ directory"
    [[ -s "$TARGET/SET.md" ]] || fail "SET.md must not be empty: $TARGET/SET.md"
    # Portable directory listing (avoid process substitution for restricted environments).
    skills_list_tmp=$(mktemp)
    find "$TARGET/skills" -mindepth 1 -maxdepth 1 -type d -print | sort > "$skills_list_tmp"
    while IFS= read -r member_dir; do
      [[ -f "$member_dir/SKILL.md" ]] || continue
      ((member_count+=1))
      validate_skill "$member_dir"
    done < "$skills_list_tmp"
    rm -f "$skills_list_tmp"
    (( member_count > 0 )) || fail "No member skills with SKILL.md found under $TARGET/skills"
  fi
  pass "Skill set validated: $TARGET"
  exit 0
fi

fail "Target is neither a skill (missing SKILL.md) nor a skill set (missing SET.md/manifest.yaml): $TARGET"
