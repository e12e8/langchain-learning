def should_terminate(reflection, state, current_step_idx, total_steps):
    if reflection.get("is_success") and current_step_idx == total_steps - 1:
        return True

    if any(count > 5 for count in state.step_retry_counts.values()):
        return True

    return False
