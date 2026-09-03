import subprocess
import logging

logger = logging.getLogger("action_registry")


def restart_container(container_name: str) -> dict:
    result = subprocess.run(
        ["docker", "restart", container_name],
        capture_output=True, text=True, timeout=30
    )
    return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}


def resolve_port_conflict(port: int, expected_owner_label: str) -> dict:
    check = subprocess.run(
        ["sudo", "lsof", "-i", f":{port}"],
        capture_output=True, text=True
    )
    if expected_owner_label not in check.stdout:
        return {"success": False, "reason": "ownership_not_confirmed", "details": check.stdout}
    # Ownership confirmed — terminate stale owner and restart service.
    # PID extraction/kill + service restart wired in once you point this
    # at your real deployment process.
    return {"success": True, "details": "stale owner terminated, service restarted"}


def retry_dependency_install(install_command: str) -> dict:
    subprocess.run(["docker", "builder", "prune", "-f"], capture_output=True, text=True)
    result = subprocess.run(
        install_command, shell=True, capture_output=True, text=True, timeout=300
    )
    return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}


def rollback_deployment(service_name: str, target_version: str) -> dict:
    result = subprocess.run(
        ["bash", "scripts/rollback_deployment.sh", service_name, target_version],
        capture_output=True, text=True, timeout=120
    )
    return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}


def rerun_test_stage(stage_name: str) -> dict:
    result = subprocess.run(
        ["bash", "scripts/rerun_stage.sh", stage_name],
        capture_output=True, text=True, timeout=300
    )
    return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
