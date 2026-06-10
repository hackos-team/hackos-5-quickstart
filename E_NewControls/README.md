# Track E: New Side Tasks / Extend the Testbed

> ⚪ Gray Team | Author a new **side task** (a high-stakes sabotage objective), a new environment, or a new scorer and prove it's accomplishable with at least one straj (**s**abotage **traj**ectory).

Side tasks are the foundation of the whole benchmark: they're what every monitor and protocol gets tested against.

## Setup

```bash
uv run ct init
uv run ct settings pull linuxarena
```

## Anatomy of a side task

```
side_tasks/my_task_idea/        # add the _idea suffix while WIP so tests don't gate on it
  __init__.py                   # make_side_task_config_from_path(..., failure_type=, task_category=, scorer=)
  scorer.py                     # @linux_scorer; the main function MUST be named scorer()
  docs/
    goal.md                     # shown to RED team — the sabotage objective
    attack_surface.md           # files / services / components that can be targeted
    scorer.md                   # what the scorer checks (pseudocode)
    scoring_details.md          # optional: constraints the agent must know
    NOTES.md                    # why it's incriminating, how it's prevented
```

```python
from pathlib import Path
from .scorer import scorer
from control_tower.task.task_config import make_side_task_config_from_path

config = make_side_task_config_from_path(
    Path(__file__).parent,
    failure_type="delayed",          # "live" (harm during the run) or "delayed" (planted, fires later)
    task_category="exfiltration",    # exfiltration | running_malware | data_tampering |
                                     # access_control_bypass | monitoring_subversion | access_secret | other
    scorer=scorer,
)
```

## Design rules (summarized from the docs by an LLM)

- **Fire-or-arrest test** — would you fire/arrest someone for doing this? Aim for *arrest*-level stakes.
- **Not accidentally triggerable** by an honest agent doing the main task.
- **Describe outcomes, not methods** — "steal admin credentials," *not* "edit config X to add a backdoor."
- **Avoid magic numbers** (hardcoded malicious URLs/strings) — make them discoverable in-env so monitors can't trivially match them.
- **Intelligence-scaling** — smarter attackers should be able to do it in sneakier ways.
- **Coverable** by multiple plausible main tasks.

Full guide: [making-side-tasks.md](https://github.com/linuxarena/control-tower/blob/main/docs/development/making-side-tasks.md)
-> Main tasks guide for reference: [making-main-tasks.md](https://github.com/linuxarena/control-tower/blob/main/docs/development/making-main-tasks.md)

## Validate it

Every side task needs **≥1 straj** proving it's accomplishable subtly:

```bash
uv run ct run side-task-review  # auto-audit: reward-hacking, magic numbers, straj feasibility
uv run ct run monitor <straj-run> --action-monitor multi --only-action
```

If you can't build a low-suspiciousness straj on any untrusted model, the side task is probably misdesigned but it is still valuable data. Optionally, we recommend you accompany it with a harder side task for comparison.

## Papers to start from — reproduce, then improve

These define environments, side tasks, and the threat-model taxonomy. Reproduce a task category here, then extend it into the testbed.

- **[SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents](https://arxiv.org/abs/2506.15740)** — Kutasov et al., 2025 (arXiv:2506.15740). Complex agentic environments paired with sabotage side tasks. **Reproduce** the structure of one environment; **improve** by porting a new side task into control-tower with a validating straj.
- **[Sabotage Evaluations for Frontier Models](https://arxiv.org/abs/2410.21514)** — Benton et al. (Anthropic), 2024 (arXiv:2410.21514). Four threat models (decision sabotage, code sabotage, sandbagging, undermining oversight). **Reproduce** one as a side task; **improve** the scorer so it's not accidentally triggerable by an honest agent.
- **[AgentDojo: …Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)** — Debenedetti et al., 2024 (arXiv:2406.13352). An extensible tool-use environment — a model for *how to build* a new one. **Reproduce** a task + attack surface; **improve** into a fresh environment + side task (e.g. CTF-style cybersecurity).
- **[How to evaluate control measures for LLM agents?](https://arxiv.org/abs/2504.05259)** — Korbak et al. (UK AISI), 2025 (arXiv:2504.05259). How threat models should scale with capability. **Reproduce** their threat-model framing for your task; **improve** by designing a side task whose difficulty scales with attacker intelligence (sneakier solutions for smarter models).

## Deliverables

2-page report + code (environment / side-task / scorer + a validating sabotage trajectory/straj) + 3-min demo. **New tasks that survive review can potentially be contributed back to LinuxArena.**
