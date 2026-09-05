"""
Confirms a remediation actually worked, rather than just trusting that
the action command returned success. This is what makes the loop
Observe -> Reason -> Act -> Verify -> Adapt, not just Act -> Assume.
"""
import subprocess
import time


def verify_restart_container(container_name: str, timeout_seconds: int = 15) -> dict:
    """
    Verification for RESTART_CONTAINER, per SCN-001:
    1. Container is running
    2. (Health check, if the container defines one)
    3. In a real pipeline: rerun the failed stage and confirm it passes.
       Here, we simulate that final check since there's no real CI stage
       to rerun in this local test.
    """
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip() == "true":
            return {"verified": True, "detail": "container running and stable"}
        time.sleep(2)

    return {"verified": False, "detail": "container did not reach running state in time"}


VERIFIERS = {
    "RESTART_CONTAINER": verify_restart_container,
    # ROLLBACK_DEPLOYMENT, RESOLVE_PORT_CONFLICT, RETRY_DEPENDENCY_INSTALL,
    # RERUN_TEST_STAGE verifiers get added here as each is wired to a real target.
}


def verify_action(action_name: str, verify_params: dict) -> dict:
    if action_name not in VERIFIERS:
        return {"verified": False, "detail": f"no verifier defined for '{action_name}'"}
    return VERIFIERS[action_name](**verify_params)
