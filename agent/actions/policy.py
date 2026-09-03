"""
Per-action policy constraints, derived directly from the locked
SCN-001 through SCN-005 scenario definitions. This is intentionally
kept separate from the LLM decision logic — the LLM proposes,
this file (checked in code, not by a prompt) disposes.
"""

ACTION_POLICIES = {
    "RESTART_CONTAINER": {
        "risk": "LOW",
        "min_confidence": 0.85,
        "max_retries": 1,
    },
    "RESOLVE_PORT_CONFLICT": {
        "risk": "LOW",
        "min_confidence": 0.85,
        "max_retries": 1,
        "requires_ownership_check": True,
    },
    "RETRY_DEPENDENCY_INSTALL": {
        "risk": "LOW",
        "min_confidence": 0.80,
        "max_retries": 1,
        "allowed_only_for_subtype": "transient",
    },
    "ROLLBACK_DEPLOYMENT": {
        "risk": "HIGH",
        "min_confidence": 0.85,
        "max_retries": 0,  # one-shot only, never a repeat rollback per incident
        "requires_deterministic_target": True,
    },
    "RERUN_TEST_STAGE": {
        "risk": "LOW",
        "min_confidence": 0.80,
        "max_retries": 1,
        "allowed_only_for_subtype": "flaky_signature",
    },
}


def is_action_allowed(action_name: str, confidence: float, retry_count: int, **context) -> tuple[bool, str]:
    """Returns (allowed: bool, reason: str). This is the Policy Check step."""
    if action_name not in ACTION_POLICIES:
        return False, f"'{action_name}' is not an approved action"

    policy = ACTION_POLICIES[action_name]

    if confidence < policy["min_confidence"]:
        return False, f"confidence {confidence} below required {policy['min_confidence']}"

    if retry_count > policy["max_retries"]:
        return False, f"retry count {retry_count} exceeds max {policy['max_retries']}"

    if policy.get("requires_ownership_check") and not context.get("ownership_confirmed"):
        return False, "ownership not positively confirmed"

    if policy.get("allowed_only_for_subtype") and context.get("failure_subtype") != policy["allowed_only_for_subtype"]:
        return False, f"failure subtype '{context.get('failure_subtype')}' not eligible for this action"

    if policy.get("requires_deterministic_target") and not context.get("deterministic_target_resolved"):
        return False, "rollback target was not deterministically resolved"

    return True, "allowed"
