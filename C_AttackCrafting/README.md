# Track C — Attack Crafting 🔴 Red Team

> Hand-craft a **sabotage trajectory (straj)**: accomplish a side task while staying under the monitor's radar. One small change, a plausible cover story, a real security property violated.

A straj must complete the side task **and** evade the monitor. **It does not need to solve the main task.** The goal is to be subtle: the sabotage reads as an ordinary bug fix, refactor, feature, etc..

Built on **[control-tower](https://github.com/linuxarena/control-tower)** (LinuxArena / ControlArena).

## Setup

```bash
uv run ct init
uv run ct settings pull linuxarena
```

## Learn from existing strajs

```bash
uv run ct run monitor straj-dataset --action-monitor multi --only-action
# use these results as a point of reference to evaluate the relative effectiveness of your attack
```

Study the worked examples — a homoglyph in an identifier, `$USERNAME` shell expansion pointing at the wrong path, swapped args that leak a secret into public output, debug-wrapper exfiltration: [docs/development/strajs/example-strajs.md](https://github.com/linuxarena/control-tower/blob/main/docs/development/strajs/example-strajs.md).

## Build & test your attack

Either author an attack policy (so the model executes it) or hand-write the trajectory, then check it against the monitor:

```bash
uv run ct run eval --policy attack -e <env> -t <main_task> -s <side_task>
uv run ct run monitor <your-run> --action-monitor multi --only-action   # did you stay under threshold?
```

Then confirm you actually beat the monitor at the audit budget:

```bash
uv run ct game-metrics metrics --honest <honest-run> --attack <your-attack-run> --audit-budgets 1
```

## What makes for a strong attack

- **Subtlety**: no single action looks suspicious in isolation
- **Plausiblity**: every change has a convincing cover story
- **Absence of magic numbers**: hardcoded malicious URLs/strings are trivially caught; discover them in-env instead
- **Scalability**: leaves room for sneakier variants

## [Optional] Papers to start from

Reproduce an attack from one of these, get it under the monitor's threshold in control-tower, then make it sneakier.

- **[SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents](https://arxiv.org/abs/2506.15740)** — Kutasov et al., 2025 (arXiv:2506.15740). Agents complete a benign main task while covertly running a sabotage side task — exactly the straj setup. Reproduce one of their sabotage patterns; improve the cover story so it reads as ordinary debugging.
- **[Sabotage Evaluations for Frontier Models](https://arxiv.org/abs/2410.21514)** — Benton et al. (Anthropic), 2024 (arXiv:2410.21514). Four sabotage threat models including code sabotage and undermining oversight. Reproduce a code-sabotage example; improve toward a *slow-burn* version where harm only emerges from the composition of clean-looking steps.
- **[Preventing Language Models From Hiding Their Reasoning](https://arxiv.org/abs/2310.18512)** — Roger & Greenblatt, 2023 (arXiv:2310.18512). Encoded reasoning / steganography, and how paraphrasing defenses break it. Reproduce an encoded-reasoning channel; improve it to survive a paraphrasing monitor.
- **[AgentDojo: ... Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)** — Debenedetti et al., 2024 (arXiv:2406.13352). Realistic tool-use tasks plus injection attacks. Reproduce an injection hidden in benign-looking content; improve it to slip under the 1% audit budget — discover targets in-env, no magic numbers.

## Deliverables

2-page report + code + 3-min demo; report main/side-task success and safety vs. the `attack` baseline against a named monitor. **Strong attacks can potentially be contributed back to the benchmark.** Use the [red-team PR template](https://github.com/linuxarena/control-tower/blob/main/.github/PULL_REQUEST_TEMPLATE/red-team.md).
