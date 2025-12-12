from workflow.state import EvaluateState


class CountManager:
    def run(self, state: EvaluateState) -> EvaluateState:
        return self.increment_count(state)

    def increment_count(self, state: EvaluateState) -> EvaluateState:
        new_state = state.copy()
        new_state["current_count"] = state["current_count"] + 1
        return new_state
