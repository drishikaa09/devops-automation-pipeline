"""
Ties the agent's decision step to the Action Registry. This is the
full loop: error -> decide -> policy check -> execute (or escalate).
"""
import json
import subprocess
from agent_decide import decide
from actions.registry import execute_action, ActionNotAllowedError


def handle_incident(error_text: str, action_params: dict, retry_count: int = 0, **policy_context) -> dict:
    decision = decide(error_text)
    print(f"Agent decision:\n{json.dumps(decision, indent=2)}\n")

    if decision["decision"] != "AUTO_REMEDIATE":
        print(f"Escalating: {decision['reason']}")
        return {"status": "ESCALATED", "decision": decision}

    try:
        result = execute_action(
            decision["action"],
            action_params,
            confidence=decision["confidence"],
            retry_count=retry_count,
            **policy_context
        )
        print(f"Execution result: {result}")
        return {"status": "EXECUTED", "decision": decision, "result": result}
    except ActionNotAllowedError as e:
        print(f"Action blocked by policy: {e}")
        return {"status": "ESCALATED", "decision": decision, "block_reason": str(e)}


if __name__ == "__main__":
    # Set up a real test container so restart_container has something to act on
    subprocess.run(["docker", "rm", "-f", "test-agent-container"], capture_output=True)
    subprocess.run(["docker", "run", "-d", "--name", "test-agent-container", "nginx"], capture_output=True)

    test_error = "Container exited with code 137, docker logs show OOMKilled true"
    outcome = handle_incident(
        test_error,
        action_params={"container_name": "test-agent-container"},
        retry_count=0
    )
    print(f"\nFinal outcome: {outcome['status']}")
