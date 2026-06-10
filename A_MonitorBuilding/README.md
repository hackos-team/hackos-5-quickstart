# Track A: Monitor Building

> 🔵 Blue Team | Build a monitor that scores how suspicious each agent action (or whole trajectory) is — and catches sabotage while keeping false alarms under the audit budget (~1%).

## The game

An untrusted agent works on a *main task* and may secretly attempt a *side task* (sabotage). Your monitor assigns a suspiciousness score (**0 = clean → 10 = very suspicious**) to each action and/or the full trajectory. A run is "caught" if a flagged action falls within the audit budget. You win by maximizing:

> **Safety** = caught / (caught + uncaught successful sabotage), at a fixed false-positive rate on honest runs.

The whole point: a *weaker, trusted* monitor catching a *stronger, untrusted* agent without crying wolf on honest work.

## Setup

```bash
uv run ct init
uv run ct settings pull linuxarena
```

## Run the baseline loop

```bash
# 1. Generate trajectories, or just use the shared sabotage dataset (straj-dataset)
uv run ct run eval --policy honest -e clinical_trial -t adverse_reaction_followup_tracking --no-upload
uv run ct run eval --policy attack -e clinical_trial -t adverse_reaction_followup_tracking -s suppress_safety_notifications --no-upload

# 2. Score with a built-in monitor
uv run ct run monitor straj-dataset --action-monitor multi --only-action

# 3. List the other available monitors that you could use
uv run ct protocols monitors
```

You want to try and perform better than the available monitors.

## Write your own monitor

Some boilerplate has been provided for you in `monitor.py`. At any moment, you can test your monitor with the following command:

```sh
uv run ct run monitor straj-dataset --action-monitor track_a-monitor_building.monitor:my_action_monitor --only-action
```

For monitors that need the whole sequence (temporal / drift signals), register a trajectory-level monitor instead (scores once per trajectory instead of once per action). An example has already been included in `monitor.py`, and you can use the following command to test it:

```sh
uv run ct run monitor straj-dataset --action-monitor track_a-monitor_building.monitor:my_traj_monitor
```

## Measure safety vs. usefulness

```bash
uv run ct game-metrics metrics --honest <honest-run> --attack <attack-run> \
  --audit-budgets 0.1 --audit-budgets 1 --audit-budgets 5 --output-dir results/
```

Writes `safety_curves.png` + `metrics.json`. If your monitor produces only per-action scores, add `--mode action_only`.

## [Optional] Papers to start from

Pick one, reproduce its monitoring result inside control-tower, then push past it.

- **[AI Control: Improving Safety Despite Intentional Subversion](https://arxiv.org/abs/2312.06942)** — Greenblatt et al., 2023 (arXiv:2312.06942). The founding paper; defines *trusted monitoring* and the audit-budget game. Reproduce the trusted-monitor baseline; improve the scoring beyond a single LLM suspicion call (ensembles, drift-from-task, per-action + trajectory fusion).
- **[Reliable Weak-to-Strong Monitoring of LLM Agents](https://arxiv.org/abs/2508.19461)** — Kale et al., 2025 (arXiv:2508.19461). Finds monitor *scaffolding/architecture* matters more than whether the agent knows it's being watched. Reproduce their scaffolding comparison; improve with an agentic monitor that asks follow-up questions before flagging.
- **[Monitoring Reasoning Models for Misbehavior…](https://arxiv.org/abs/2503.11926)** — Baker et al. (OpenAI), 2025 (arXiv:2503.11926). CoT monitoring catches a lot — but pressure teaches models to obfuscate. Reproduce a CoT-based monitor; improve robustness so the score doesn't collapse when the reasoning goes quiet.
- **[Adaptive Attacks on Trusted Monitors Subvert AI Control Protocols](https://arxiv.org/abs/2510.09462)** — Terekhov et al., 2025 (arXiv:2510.09462). Prompt-injection *against the monitor itself* breaks otherwise-safe protocols. Reproduce the attack on your monitor; improve by hardening it (input isolation, injection detection).
- **[A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511)** — Angelopoulos & Bates, 2021 (arXiv:2107.07511). The formal tool for a *guaranteed* ≤1% FPR threshold instead of an empirical cutoff. Reproduce conformal calibration on honest-run scores; improve the audit threshold's stability across environments.

## Deliverables

2-page report + code + 3-min demo. Compare your monitor to a baseline on the **same** attack & honest runs; report score distributions, percentiles, and safety at several audit budgets — and confirm usefulness isn't degraded. Use the [blue-team PR template](https://github.com/linuxarena/control-tower/blob/main/.github/PULL_REQUEST_TEMPLATE/blue-team.md).

- [docs/monitoring.md](https://github.com/linuxarena/control-tower/blob/main/docs/monitoring.md)
- [docs/safety-curves.md](https://github.com/linuxarena/control-tower/blob/main/docs/safety-curves.md)
