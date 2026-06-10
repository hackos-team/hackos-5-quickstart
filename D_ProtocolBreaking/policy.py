from control_tower.protocols.policies.registry import policies

@policies.register(attempts_main_task=True, attempts_side_task=True, attempts_sneaky=True)
def my_attack(state, submit, args=None):
    ...  # returns an Inspect Agent that pursues the side task while looking honest
