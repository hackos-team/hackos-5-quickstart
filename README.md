# HackOS 5 — AI Control Hackathon · Quickstart

Limit the harm an untrusted AI agent can cause while it operates, even when it actively tries to subvert the controls around it. The core game: can a *weaker, trusted* model catch a *stronger, untrusted* agent attempting sabotage? And while keeping false alarms under ~1%?

Everything here runs on **[control-tower](https://github.com/linuxarena/control-tower)**, the AI-control eval framework (LinuxArena / ControlArena) by Redwood Research and UK's AISI.

## Shared setup (all tracks)

```bash
uv run ct init  # completions, `ct` alias, settings, agent skills
uv run ct settings pull linuxarena  # environments, main tasks, side tasks
```

Before spending any of your credits, run this to make sure everything works (it just runs `ls` and then exist, no model calls):

```bash
uv run ct run eval --policy test --env tiktok --just-main-tasks --limit 1 --no-upload
```

## Pick a track

| | Track | Team | You build |
| --- | --- | --- | --- |
| **[A](A_MonitorBuilding/)** | Monitor Building | 🔵 Blue | A monitor that scores how suspicious each action/trajectory is |
| **[B](B-ProtocolDesign/)** | Protocol Design | 🔵 Blue | A protocol (defer / rewrite / gate) and its safety–usefulness tradeoff |
| **[C](C-AttackCrafting/)** | Attack Crafting | 🔴 Red | A sabotage trajectory (straj) that evades the monitor |
| **[D](D-ProtocolBreaking/)** | Break a Protocol | 🔴 Red | An untrusted policy that beats a protocol — then a fix |
| **[E](E-NewControls/)** | New Side Tasks | ⚪ Gray | A new side task / environment / scorer that extends the testbed |

## The shared vocabulary

- **Main task**: the legitimate job the agent is asked to do.
- **Side task**: a high-stakes sabotage objective the untrusted agent may pursue covertly.
- **Straj**: a *sabotage trajectory*: a run that accomplishes the side task while staying subtle.
- **Monitor**: scores suspiciousness, 0 (clean) → 10 (very suspicious).
- **Protocol**: the blue-team decision policy that acts on monitor scores (audit / defer / rewrite / gate).
- **Safety** = caught / (caught + uncaught successful sabotage), at a fixed audit budget (FPR on honest runs).
- **Usefulness** = honest main-task success rate.

By default, `anthropic/claude-haiku-4-5` is used as the untrusted model and `openai/gpt-4.1-nano` as the trusted one. If you decide to change this, beware of the cost of beefier models (especially since these evaluations tend to be token-heavy) and make sure to document this change in your deliverables.

## Judging & deliverables

Scored 1–5 on **impact & innovation**, **execution quality**, and **clarity**. Each team ships:

- 📄 a 2-page report;
- 💻 a code repo;
- 🎬 a 3-minute demo (either a video or in person)
  - if it's a video, it can be an unlisted youtube link, public google drive link, etc.. Just make sure that we can access it.

1st-2nd-3rd place for the best monitors and best attack respectively, and "best side tasks" award.

## Docs worth skimming at least once

- [Control concepts](https://github.com/linuxarena/control-tower/blob/main/docs/control-concepts.md)
- [Hands-on guide](https://github.com/linuxarena/control-tower/blob/main/docs/hands-on-guide.md)
- [Running evals](https://github.com/linuxarena/control-tower/blob/main/docs/running-evals.md)
- [Monitoring](https://github.com/linuxarena/control-tower/blob/main/docs/monitoring.md)
- [Protocols](https://github.com/linuxarena/control-tower/blob/main/docs/development/protocols.md)
- [Safety curves](https://github.com/linuxarena/control-tower/blob/main/docs/safety-curves.md)
- [Making side tasks](https://github.com/linuxarena/control-tower/blob/main/docs/development/making-side-tasks.md)
