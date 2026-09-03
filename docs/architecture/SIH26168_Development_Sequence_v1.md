# SIH26168 Development Sequence v1

**Planning horizon:** approximately one to two months, expressed as dependency phases rather than false precision.

## Critical path

`WP-00 → WP-01 → WP-02/WP-03 → WP-06/WP-07/WP-14 → WP-13 → WP-15 → WP-17`.

S2 enables WP-03 immediately. S6B1 enables WP-08 in parallel. Conditional private IO-VNBD use enables WP-10/11, but ML is not on the classical demo critical path. S1 physical evidence blocks named-device claims, not bootstrap/replay. S3 blocks alignment-dependent live constraints and the intended car demonstration claim. Field validation blocks final route selection, not replay.

## Phase intent

- **P0 Bootstrap:** repository/governance/contracts.
- **P1 Foundations:** import S1 acquisition, integrate S2 core/JNI, deterministic replay.
- **P2 Gates/core/map/data:** close physical/alignment questions, build integrity/reacquisition and matcher, private ingestion.
- **P3 Classical demo:** model-disabled baseline, analyzer, offline UI, evidence-honest scenario.
- **P4 Optional ML + integrated demo:** shadow then eligible model only if gates pass; ten-event rehearsal.
- **P5 Edge:** reusable external adapter and rate profiling.
- **P6 Release:** named evidence, privacy/licence, clean build and safe field/replay rehearsal.

## Issue-ready work packages

| ID | Phase | Work package | Components | Dependencies | Class | Acceptance boundary |
| --- | --- | --- | --- | --- | --- | --- |
| WP-00 | P0 Bootstrap | Repository and governance scaffold | C-19,C-20 |  | bootstrap | Monorepo skeleton, owners, branch rules, generated-file policy and fast empty CI lanes exist; no production claim. |
| WP-01 | P0 Bootstrap | Contract/schema v1 implementation | C-20 | WP-00 | production | All I-01..I-22 have machine schemas/enums, compatibility tests and generated bindings; S2 fields match exactly. |
| WP-02 | P1 Foundations | Import and harden Android acquisition | C-01,C-02,C-03 | WP-01 | production | Existing S1 path builds in monorepo; raw clocks/axes/provenance round-trip into verified sessions. |
| WP-03 | P1 Foundations | Canonical C++ core and JNI integration | C-06,C-07 | WP-01 | critical production | S2 tests and C++/NumPy parity pass; JNI batch fixture produces identical accepted/rejected evidence and state. |
| WP-04 | P1 Foundations | Deterministic replay backbone | C-12,C-14 | WP-01,WP-02 | demo+verification | A public synthetic session replays deterministically through live-compatible input contracts with clear REPLAY label. |
| WP-05 | P2 Physical gates | Complete S1 physical-device protocol | C-01,C-02,C-03 | WP-02 | production evidence | Named device sessions and analyzer outputs adjudicate rate, gap, screen-off, battery and thermal gates without generalizing beyond devices. |
| WP-06 | P2 Physical gates | S3 alignment and mount-slip spike | C-04,C-05 | WP-02,WP-03 | critical experiment | Predeclared controlled car tests select or reject a method; alignment covariance/status contract is exercised; failure disables dependent aids. |
| WP-07 | P2 Core behaviour | GNSS integrity/outage/reacquisition | C-09,C-07 | WP-03,WP-04 | critical production | Good, biased, stale and intermittent return fixtures prove no first-fix privilege, evidence-once semantics and continuous typed modes. |
| WP-08 | P2 Map | Runtime graph store and top-K matcher | C-10,C-18 | WP-01 | production | Frozen S6B1 graph verifies, clear/ambiguous/off-road fixtures meet frozen logical gates, and matcher can abstain. |
| WP-09 | P3 Demo shell | Offline navigation UI and honest telemetry | C-11,C-13 | WP-04,WP-08 | demo-critical | Airplane-mode replay shows local map, traces, uncertainty, candidates and mandatory mode labels; attribution visible. |
| WP-10 | P2 Data | Private IO-VNBD ingestion and leakage firewall | C-15 | WP-00 | offline private | Pinned private subset manifest, six-schema handling, dedup/group split and runtime-vs-label canary checks pass; no raw bytes enter repo. |
| WP-11 | P3 ML experiment | Classical baselines and bounded learned aid | C-16 | WP-10,WP-14 | offline experimental | Matched baseline/ablation on frozen split and masks; results labelled exploratory; no claim or release beyond rights/evidence. |
| WP-12 | P4 ML runtime | Model export and Android shadow mode | C-08,C-17 | WP-03,WP-11 | optional production experiment | Golden parity, deadline/OOD/bounds and disabled fallback pass; shadow-mode decisions logged before influence is enabled. |
| WP-13 | P3 Evaluation | Integrated analyzer and claim firewall | C-14,C-19 | WP-03,WP-07,WP-08 | verification | Reports separate raw INS, fused, matched, display and reference; compute endpoint/max/RMSE/rates/transitions and reject invalid provenance. |
| WP-14 | P3 Classical baseline | Calibration/constraints classical baseline | C-04,C-05,C-07 | WP-03,WP-06 | critical production | Model-disabled car replay/live path produces bounded typed outputs; alignment-dependent constraints are gated and ablatable. |
| WP-15 | P4 Demo integration | Ten-event deterministic demonstration | C-07,C-09,C-10,C-11,C-12,C-13 | WP-07,WP-08,WP-09,WP-13,WP-14 | demo-critical | Script shows valid GNSS, simulated outage, turn, uncertainty growth, candidates, biased-return rejection, credible acceptance, smooth display recovery and after-run comparison. |
| WP-16 | P5 Edge deliverable | External IMU adapter and rate profiling | C-06,C-07,C-20 | WP-03 | production | Documented adapter replays external-format data; input/propagation/output rates reported separately; no universal 200 Hz claim. |
| WP-17 | P6 Release | Release verification and field rehearsal | C-19,C-02,C-13 | WP-05,WP-15,WP-16 | release | Clean build/install, network-isolated replay/live rehearsal, privacy/licence/secret scan and artifact hashes pass; field route separately approved or replay-only. |

## Parallelization and deferral

After WP-01, Android acquisition, core/JNI, replay, map runtime and private dataset ingestion proceed in parallel. UI begins on replay contracts before live science is ready. R1 concentrates on WP-03/06/07/14; R5 on WP-02/09; R4 on WP-04/08/13 and CI; R2/R3 on WP-10/11; R6 on honest scenarios, validation and field permission.

Defer dynamic map download/routing, nationwide maps, two-wheeler claims/data unless required, full raw-GNSS solver, cloud/backend, consumer-app integration, mock-location build, production certification, lane-level guarantee and ML influence that does not beat a matched baseline.
