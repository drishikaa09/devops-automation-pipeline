"""
Full agent loop: error -> decide -> policy check -> execute -> verify
-> (on failure) retry once -> verify again -> success or escalate.
"""
import json
import subprocess
from agent_decide import decide
from actions.registry import execute_action, ActionNotAllowedError
from verification import verify_action


def handle_incident(error_text: str, action_params: dict, verify_params: dict, **policy_context) -> dict:
    decision = decide(error_text)
    print(f"Agent decision:\n{json.dumps(decision, indent=2)}\n")

    if decision["decision"] != "AUTO_REMEDIATE":
        print(f"Escalating: {decision['reason']}")
        return {"status": "ESCALATED", "decision": decision}

    retry_count = 0
    while retry_count <= 1:  # one retry, per locked scenario policy
        try:
            result = execute_action(
                decision["action"], action_params,
                confidence=decision["confidence"], retry_count=retry_count,
                **policy_context
            )
            print(f"Execution attempt {retry_count}: {result}")
        except ActionNotAllowedError as e:
            print(f"Action blocked by policy: {e}")
            return {"status": "ESCALATED", "decision": decision, "block_reason": str(e)}

        verification = verify_action(decision["action"], verify_params)
        print(f"Verification attempt {retry_count}: {verification}\n")

        if verification["verified"]:
            return {"status": "SUCCESS", "decision": decision, "verification": verification}

        retry_count += 1

    print("Verification failed after retry — escalating.")
    return {"status": "ESCALATED", "decision": decision, "verification": verification}


if __name__ == "__main__":
    subprocess.run(["docker", "rm", "-f", "test-agent-container"], capture_output=True)
    subprocess.run(["docker", "run", "-d", "--name", "test-agent-container", "nginx"], capture_output=True)

    test_error = "Container exited with code 137, docker logs show OOMKilled true"
    outcome = handle_incident(
        test_error,
        action_params={"container_name": "test-agent-container"},
        verify_params={"container_name": "test-agent-container"},
    )
    print(f"Final outcome: {outcome['status']}")
