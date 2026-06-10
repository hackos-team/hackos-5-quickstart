# Track D: Build a policy that breaks an existing control protocol

> 🔴 Red Team | Craft an **untrusted policy** that slips sabotage past it, then propose a fix. As opposed to Track C, projects in this track attempt to break the supervisor, instead of trying to slip past it.

Where Track C hand-crafts one sabotage trajectory, Track D targets the **protocol itself**: exploit blind spots in how it monitors, defers, resamples, or audits.

## Setup

```bash
uv run ct init
uv run ct settings pull linuxarena
```

## Attack a protocol

```bash
uv run ct protocols blue-protocols  # pick a control protocol to target
uv run ct protocols untrusted-policies  # existing attackers to build on

uv run ct run eval \
  --untrusted-policy <your-attack> \
  --protocol trusted-monitoring \
  --protocol-arg sus_threshold=7 \
  --task-file medium
  --no-upload
```

## Write an untrusted policy

Register a policy whose `generate()` mirrors `Model.generate()` (`messages, tools, tool_choice, config → ModelOutput`). The blue protocol wraps it as a normal model and decides whether to monitor / defer / audit / execute.

```python
from control_tower.protocols.policies.registry import policies

@policies.register(attempts_main_task=True, attempts_side_task=True, attempts_sneaky=True)
def my_attack(state, submit, args=None):
    ...  # returns an Inspect Agent that pursues the side task while looking honest
```

Tricks the docs call out: keep **private tools** the blue team never sees by executing their calls inline in your own generate loop and only returning clean outputs; use `request_last_turn()` to grab a final move after the protocol finishes. See [docs/development/protocols.md](https://github.com/linuxarena/control-tower/blob/main/docs/development/protocols.md) and the `private-test-attack` example.

## [Optional] Papers to start from

Reproduce a protocol-level attack from one of these against a control-tower protocol, show its safety collapse, then propose an improvement.

- **[Ctrl-Z: Controlling AI Agents via Resampling](https://arxiv.org/abs/2504.10374)** — Bhatt et al., 2025 (arXiv:2504.10374). Resampling protocols re-run flagged actions, which can leak signal to a clever policy. Reproduce the resampling protocol; break it by exploiting the retry channel; fix it. (Background: Redwood's [retrying vs resampling](https://blog.redwoodresearch.org/p/retrying-vs-resampling-in-ai-control).)
- **[Subversion Strategy Eval](https://arxiv.org/abs/2412.12480)** — Mallen et al., 2024 (arXiv:2412.12480). Can a model, without shared memory, statelessly converge on a protocol-evading strategy? Reproduce the eval against a chosen protocol; improve the untrusted policy's coordination, then patch the leak it exploits.
- **[Adaptive Attacks on Trusted Monitors Subvert AI Control Protocols](https://arxiv.org/abs/2510.09462)** — Terekhov et al., 2025 (arXiv:2510.09462). Inject the monitor to break the protocol that relies on it. Reproduce the attack; fix with monitor input isolation.
- **[Adaptive Deployment of Untrusted LLMs Reduces Distributed Threats](https://arxiv.org/abs/2411.17693)** — Wen et al., 2024 (arXiv:2411.17693). A strong adaptive protocol to target. Reproduce it, then break it with a *distributed* attack whose per-action suspicion stays below the macro-protocol's escalation trigger.
- **[Games for AI Control](https://arxiv.org/abs/2409.07985)** — Griffin et al., 2024 (arXiv:2409.07985). Solve for the red-team's best response to a protocol instead of guessing. Reproduce the game; improve it by deriving the optimal attack at equilibrium, then close the gap.

## Measure & report

```bash
uv run ct game-metrics metrics --honest <run> --attack <your-run> --output-dir results/
```

Show the protocol's safety **collapse** under your attack, then its **recovery** using your proposed fix. Use the [red-team PR template](https://github.com/linuxarena/control-tower/blob/main/.github/PULL_REQUEST_TEMPLATE/red-team.md).
