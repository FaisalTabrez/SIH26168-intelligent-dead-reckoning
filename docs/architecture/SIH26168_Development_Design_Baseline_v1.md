# SIH26168 Development Design Baseline v1

**Architecture status:** `ARCH3-READY-FOR-REPOSITORY-BOOTSTRAP`

## 1. Design invariants

1. Raw evidence is immutable; source and arrival clocks, axes, sequences, provider and delivery defects survive ingestion.
2. C-07 is the only writer of the S2 state, biases and covariance. Calibration cannot rewrite samples; alignment cannot enter the S2 state.
3. Core time is boot-scoped monotonic. Wall time is auxiliary. Cross-device/boot clocks are never directly compared.
4. One physical GNSS-family observation is offered once. Rejected/malformed evidence IDs are consumed.
5. Learned/map output is a proposal with uncertainty, provenance, bound, deadline and terminal decision. Disabled is a complete baseline.
6. Ground truth/withheld GNSS never enters inference during an outage. Display smoothing never enters scientific state.
7. Every failure becomes an explicit health/state/reason; visually plausible output is not substituted for missing evidence.

## 2. State and failure model

| Axis | States | Owner | Degraded rule |
| --- | --- | --- | --- |
| Sensor availability | AVAILABLE / PARTIAL / GAP / MISSING_MANDATORY / FAILED | C-03 | No accel/gyro: no valid propagation; magnetometer loss is quality-gated, not fatal. |
| GNSS availability | HEALTHY / DEGRADED / UNAVAILABLE / CANDIDATE_RETURN | C-09 | Absent/rejected fixes enter DR; source evidence still logged. |
| Navigation mode | INITIALIZING / GNSS_AIDED / DEGRADED / BLACKOUT_DR / REACQUIRING / FAULT | C-09+C-07 | FAULT invalidates scientific output; no silent hold-as-valid. |
| Alignment | UNINITIALIZED / VALID / UNCERTAIN / SLIP_SUSPECTED | C-05 | Disable vehicle-frame ML/NHC when not VALID. |
| Model | DISABLED / LOADING / SHADOW / ELIGIBLE / REJECTED / FAILED | C-08 | Classical core continues. |
| Map | MISSING / NO_CANDIDATE / AMBIGUOUS / CLEAR / FAILED | C-10 | Publish unmatched state; only CLEAR after gates. |
| Reacquisition | IDLE / SCREENING / DWELL / ACCEPTED / REJECTED | C-09 | Rejected candidates do not alter state. |
| Recording | STARTING / HEALTHY / EVIDENCE_DEGRADED / LOW_STORAGE / INCOMPLETE / COMPLETE | C-02 | Navigation may continue visibly unrecorded only with EVIDENCE_DEGRADED; no later claim. |
| Demo source | LIVE_DEVICE / DETERMINISTIC_REPLAY | C-12 | SIMULATED_OUTAGE and DEMO are independent persistent labels. |

### Failure responses

| Failure | Required response |
| --- | --- |
| Missing accelerometer or gyroscope | Refuse/terminate valid scientific navigation; keep diagnostics. |
| Missing/rejected magnetometer | Continue without it; alignment/yaw uncertainty reflects loss. |
| Stale GNSS | Reject update; enter degraded/outage by hysteresis. |
| Non-monotonic/equal/oversized IMU dt | Retain raw record, reject core input, increment gap/fault evidence; never reorder/interpolate. |
| Sensor gap/batched delivery | Preserve source ordering/arrival bursts; accept only S2-valid dt; flag missing samples. |
| Thermal throttling | Shed optional model/map cadence first; record thermal/rates; never relabel reduced output. |
| Low storage | Finalize recoverable chunks; mark LOW_STORAGE/EVIDENCE_DEGRADED; block claims from unrecorded interval. |
| Missing/invalid model or inference timeout/OOD | Reject proposal; continue classical core. |
| Missing/corrupt map or no candidates | Continue unmatched; show status; never download implicitly. |
| Multiple roads or GNSS/map disagreement | Top-K/AMBIGUOUS/abstain; do not force nearest road. |
| Process recreation | Recover bytes as incomplete; start a new scientific run/state, not a continuous restoration. |
| Corrupt/incomplete replay | Reject normal demo; allow only labelled diagnostic inspection. |

## 3. Threading, buffers and backpressure

- **Acquisition HandlerThread:** copies callbacks quickly into two independently owned bounded queues: evidence and runtime. It performs no inference.
- **Writer I/O thread:** owns chunk buffers/files. At the hard queue limit, it records loss counters if possible, marks the session invalid for claims and requests a controlled recording stop. It never silently evicts raw evidence.
- **Navigation executor:** single serial owner of C-03/C-06/C-07/C-09 calls. JNI core handles never receive concurrent calls.
- **Model worker:** owns a bounded causal window and deadline. Late output is rejected by epoch; it cannot block propagation.
- **Map worker:** latest scientific state with bounded previous hypotheses. Intermediate states may be skipped for matching only, with sequences recorded; core states are not dropped by the matcher.
- **UI main thread:** latest-wins I-16 presentation only. UI backpressure never reaches the scientific path.

Direct JNI buffers have one producer/consumer lifetime and an explicit release. No component retains an Android callback array after return. Queue sizes and deadlines are I-22 configuration values and are frozen per run.

## 4. Runtime data flows

| Flow | Producer | Consumer | Clock | Ordering | Buffer | Validation | Failure | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Startup | C-01 | C-20,C-13 | wall auxiliary; monotonic created | Config before source | No source queue | Manifest/config/capability checks | Block scientific start | build/config/capability event |
| 2 Permissions | C-01 | Android OS/UI | callback arrival only | User decisions ordered | None | Fine location/notification/FGS capability | Explain and remain idle | permission events |
| 3 Recording start | C-01 | C-02,C-03 | new boot-scoped monotonic session | Session header precedes samples | Bounded writer/runtime queues | Storage/config/sensors | Fail closed or explicit evidence degraded | session start/context |
| 4 GNSS-aided | C-03,C-09 | C-07 | source/core monotonic | IMU strict; GNSS evidence-once | IMU batches; latest status | S2 dt; fix age/covariance | Reject typed evidence | raw, decisions, states |
| 5 Quality degradation | C-09 | C-07,C-11 | core epoch | hysteretic transitions | No special buffer | integrity/innovation | DEGRADED; inflate/reject by policy | health/mode/reasons |
| 6 Declared outage | C-09/C-12 | C-07 | core/session monotonic | mask starts at exact epoch | Raw GNSS still writer-bound | mask ID/type | BLACKOUT_DR | I-14 and hidden-field list |
| 7 Dead reckoning | C-07 | C-11,C-10 | IMU source monotonic | S2 strict accepted order | Bounded IMU batches | dt/numeric/covariance | FAULT on core failure; gaps visible | state/covariance/gaps |
| 8 Learned enabled | C-08 | C-07 | window endpoint core epoch | Proposal after full causal window | Bounded rolling window | manifest/OOD/deadline/bounds | Reject/no effect | proposal and decision |
| 9 Learned unavailable/rejected | C-08 | C-11 | core epoch | Terminal decision per proposal | Drop stale proposal | reason code | Classical continuation | timeout/OOD/rejection |
| 10 Candidate generation | C-10 | C-11 | state epoch | Same map/state version | Latest state; bounded K | graph hash/origin/covariance | 0..K/abstain | scores/versions |
| 11 Map ambiguity | C-10 | C-11 | state epoch | AMBIGUOUS until gate clears | Top-K retained bounded | entropy/margin/direction | No constraint; unmatched state | candidate distribution |
| 12 GNSS return | C-01,C-09 | C-07 | source arrival + core epoch | Candidate state first | Small dwell window | age/provenance/covariance | REACQUIRING | all candidate fixes |
| 13 Inconsistent return | C-09,C-07 | C-11 | exact state epoch | Evidence consumed once | Dwell reset by policy | NIS/consistency | Reject; stay DR | NIS/reason |
| 14 Credible fix | C-09,C-07 | C-11 | exact state epoch | Repeated consistent dwell | Bounded dwell | S2 gate + policy | Accept update | accepted fix/update |
| 15 Smooth recovery | C-11 | C-13 | scientific epoch + UI arrival | Scientific unchanged; display derived | Latest UI | jump/staleness labels | No fake scientific interpolation | both traces/policy |
| 16 Stop/export | C-01,C-02 | User/C-14 | session monotonic; wall auxiliary | Stop event then chunk finalize | Drain writer bounded | hash/size/completeness | INCOMPLETE if drain fails | manifest/export hash |
| 17 Process recovery | C-02 | C-01,C-12 | new process; old clock identity retained | Finalize abandoned partial | No state restoration | chunk hashes | New scientific run; old diagnostic session | recovery event |
| 18 Recorded replay | C-12 | C-01 consumers | recorded session clock | Original ordering/sequence | Read-ahead bounded | manifest/chunk/config | Reject corrupt/incomplete except diagnostic | control/run IDs |
| 19 Replay simulated outage | C-12 | C-09 | recorded session clock | Frozen mask at epochs | Raw/reference retained separately | scenario hash | Reject invalid mask | mask and withheld evidence |

## 5. Learned-model boundary

Candidate inputs are causal windows of validated accelerometer/gyro, `dt`, gap/validity masks, optional alignment only when VALID, stationary/motion context and declared device profile. Raw phone GNSS is excluded during blackout; every vehicle/VBOX/CAN/wheel field is label/evaluation-only. Candidate output starts with bounded forward-speed or velocity pseudo-measurement plus covariance/confidence. Additional heads require an ADR and evidence.

C-08 owns windowing and runtime normalization using I-19; C-16 owns training transforms but exports their exact parameters. Physical bounds, OOD rules, maximum runtime and stale-epoch rejection live in I-19/I-22. Every proposal receives ACCEPTED/REJECTED/SHADOW_ONLY. On any failure the classical path continues. Shadow mode is mandatory before influence. Ablations cover classical-only, model shadow, model eligible, map off/on, and each constraint. Split grouping occurs before windows, exact duplicates/parent sessions stay in one role, and future/withheld GNSS canaries must fail if accessed.

## 6. Error handling and observability

Use typed result codes at every boundary; exceptions do not cross JNI. Scientific fatal errors invalidate output and end the core run. Optional subsystem faults degrade only that subsystem. Logs contain monotonic epoch, sequence, component, code, config/build and evidence IDs; no raw location is copied into ordinary diagnostic logs. Counters include delivered/accepted/rejected samples, gaps, queue high-water/loss, propagation/update latency, model deadline/OOD, matcher latency/entropy/abstention, output rate, storage, thermal and mode dwell.

## 7. Feature flags and demo isolation

Flags are compile-time capability plus signed/hashed run configuration: `model_mode=DISABLED|SHADOW|ELIGIBLE`, `map_match=OFF|TOP_K`, `map_feedback=OFF|EXPERIMENTAL`, `source=LIVE|REPLAY`, and `simulated_outage=OFF|SCENARIO_ID`. Release/live builds contain no mock-location provider. Replay and simulated outage require permanent UI badges and session evidence. Unknown flags reject start.

## 8. Storage, privacy, security and recovery

App-private storage is primary; export is user-initiated. Sessions have limits/reserve, atomic chunks, SHA-256 and COMPLETE/INCOMPLETE status. Public fixtures are synthetic/de-identified. IO-VNBD and team route recordings remain private. Secrets are absent from configs/artifacts and checked before merge. Dependency locks/SBOM/notices are release inputs. No network permission is necessary for the navigation path; any future network feature is outside scientific health and requires an ADR/threat review.

## 9. Reproducible builds

Pin Gradle wrapper, AGP, Kotlin, JDK, Android SDK/NDK/CMake, C++ dependencies, Python lock with hashes, model runtime, schema generator and map tools/container digest. Generated files name their source/schema/tool version and are reproducible or excluded. Release artifacts carry I-18/I-19/I-21/I-22 identities and an outer artifact manifest.

## 10. Requirement coverage rule

All IDs found in the supplied baseline are recorded in `machine_readable/architecture_status.json`. Mandatory functional/deliverable/deployment/constraint requirements map to components/work packages; performance and internal targets map to verification evidence; unknowns remain open; out-of-scope items are enforced exclusions. Coverage means architectural disposition, not verified compliance.
