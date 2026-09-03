import logging
from actions.tools import (
    restart_container,
    resolve_port_conflict,
    retry_dependency_install,
    rollback_deployment,
    rerun_test_stage,
)
from actions.policy import is_action_allowed

logger = logging.getLogger("action_registry")

ACTION_REGISTRY = {
    "RESTART_CONTAINER": restart_container,
    "RESOLVE_PORT_CONFLICT": resolve_port_conflict,
    "RETRY_DEPENDENCY_INSTALL": retry_dependency_install,
    "ROLLBACK_DEPLOYMENT": rollback_deployment,
    "RERUN_TEST_STAGE": rerun_test_stage,
}


class ActionNotAllowedError(Exception):
    pass


def execute_action(action_name: str, params: dict, confidence: float, retry_count: int, **context) -> dict:
    """
    The only entry point the agent's decision step is allowed to call.
    The LLM never runs a command directly — it can only request an
    action_name, which is checked here against the allowlist AND policy
    before anything actually executes.
    """
    allowed, reason = is_action_allowed(action_name, confidence, retry_count, **context)
    if not allowed:
        logger.warning(f"BLOCKED action='{action_name}' reason='{reason}'")
        raise ActionNotAllowedError(reason)

    if action_name not in ACTION_REGISTRY:
        raise ActionNotAllowedError(f"'{action_name}' has no registered implementation")

    logger.info(f"EXECUTING action='{action_name}' params={params}")
    func = ACTION_REGISTRY[action_name]
    return func(**params)
