from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLO_FILE = ROOT / "config" / "slo.yaml"
ALERT_FILE = ROOT / "config" / "alert_rules.yaml"
RUNBOOK_FILE = ROOT / "docs" / "alerts.md"

EXPECTED_SLOS = {
    "latency_p95_ms": {"objective": 3000, "target": 99.5},
    "error_rate_pct": {"objective": 2, "target": 99.0},
    "daily_cost_usd": {"objective": 2.5, "target": 100.0},
    "quality_score_avg": {"objective": 0.75, "target": 95.0},
}

EXPECTED_ALERTS = [
    ("high_latency_p95", "docs/alerts.md#1-high-latency-p95"),
    ("high_error_rate", "docs/alerts.md#2-high-error-rate"),
    ("cost_budget_spike", "docs/alerts.md#3-cost-budget-spike"),
]

EXPECTED_RUNBOOK_HEADINGS = [
    "## 1. High latency P95",
    "## 2. High error rate",
    "## 3. Cost budget spike",
]


def parse_scalar(value: str) -> float | int | str:
    value = value.strip()
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+(?:\.\d+)?", value):
        return float(value)
    return value


def parse_slo_file(text: str) -> dict[str, dict[str, float | int | str]]:
    slis: dict[str, dict[str, float | int | str]] = {}
    current: str | None = None

    for raw_line in text.splitlines():
        if match := re.match(r"^\s{2}([a-z0-9_]+):\s*$", raw_line):
            current = match.group(1)
            slis[current] = {}
            continue
        if current and (match := re.match(r"^\s{4}(objective|target):\s*(.+?)\s*$", raw_line)):
            slis[current][match.group(1)] = parse_scalar(match.group(2))

    return slis


def parse_alert_file(text: str) -> list[dict[str, str]]:
    alerts: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in text.splitlines():
        if match := re.match(r"^\s*-\s+name:\s+(\S+)\s*$", raw_line):
            if current:
                alerts.append(current)
            current = {"name": match.group(1)}
            continue
        if current and (match := re.match(r"^\s+(severity|condition|type|owner|runbook):\s+(.+?)\s*$", raw_line)):
            current[match.group(1)] = match.group(2)

    if current:
        alerts.append(current)

    return alerts


def check_slos() -> list[str]:
    text = SLO_FILE.read_text(encoding="utf-8")
    parsed = parse_slo_file(text)
    errors: list[str] = []

    for sli_name, expected in EXPECTED_SLOS.items():
        actual = parsed.get(sli_name)
        if not actual:
            errors.append(f"missing SLI block: {sli_name}")
            continue
        for field, expected_value in expected.items():
            actual_value = actual.get(field)
            if actual_value != expected_value:
                errors.append(
                    f"{sli_name}.{field} expected {expected_value!r}, got {actual_value!r}"
                )

    return errors


def check_alerts() -> list[str]:
    text = ALERT_FILE.read_text(encoding="utf-8")
    alerts = parse_alert_file(text)
    runbook_text = RUNBOOK_FILE.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(alerts) != len(EXPECTED_ALERTS):
        errors.append(f"expected {len(EXPECTED_ALERTS)} alert rules, found {len(alerts)}")

    for (expected_name, expected_runbook), alert in zip(EXPECTED_ALERTS, alerts):
        actual_name = alert.get("name")
        actual_runbook = alert.get("runbook")
        if actual_name != expected_name:
            errors.append(f"alert name expected {expected_name!r}, got {actual_name!r}")
        if actual_runbook != expected_runbook:
            errors.append(
                f"{expected_name} runbook expected {expected_runbook!r}, got {actual_runbook!r}"
            )

    for heading in EXPECTED_RUNBOOK_HEADINGS:
        if heading not in runbook_text:
            errors.append(f"missing runbook heading: {heading}")

    return errors


def main() -> int:
    checks = [
        ("SLO config", check_slos),
        ("Alert rules", check_alerts),
    ]

    total_errors: list[str] = []
    for label, fn in checks:
        errors = fn()
        if errors:
            print(f"[FAIL] {label}")
            for error in errors:
                print(f"  - {error}")
            total_errors.extend(errors)
        else:
            print(f"[PASS] {label}")

    if total_errors:
        print(f"\nSummary: {len(total_errors)} issue(s) found")
        return 1

    print("\nSummary: all Person B checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
