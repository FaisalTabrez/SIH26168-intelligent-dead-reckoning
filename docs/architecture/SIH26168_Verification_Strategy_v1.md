# SIH26168 Verification Strategy v1

## Test-level contract

| Level | Proves | Does not prove | Environment | PR blocking | Cadence |
| --- | --- | --- | --- | --- | --- |
| Unit | Local algorithms, parsers and typed failures | No integration/physical performance | Host/JVM/C++ | Yes | Every PR |
| Contract/schema | Cross-language fields, version/units/frame/clock compatibility | No scientific accuracy | Host codegen | Yes | Every PR |
| Deterministic fixtures | Same evidence/config produces same decisions/state | No real-device generalization | Host/C++/Android replay | Yes for public fixtures | Every PR |
| C++/Python parity | S2 numerical parity/tolerances and evidence decisions | No Android/JNI lifecycle | Linux host | Yes | Every PR + nightly broad seeds |
| Android JVM | Lifecycle-independent Kotlin policy/writer/UI adapters | No hardware/FGS reality | JVM | Yes | Every PR |
| Android instrumentation | APK/service/storage/JNI behaviour on emulator/device | No multi-OEM proof | Emulator/connected device | Yes when runner available; otherwise required release lane | Nightly/manual device |
| Replay | Live-compatible deterministic end-to-end paths and labels | No live sensor quality | Host/Android | Yes | Every PR smoke; nightly full |
| Dataset integrity | Hashes, schemas, dedup, grouping, leakage firewall | No model quality/rights beyond recorded status | Private offline | No public PR dependency; blocks private experiment | Per ingest/run |
| Model evaluation | Matched baseline/ablation and held-out metrics | No deployment parity or final drift truth | Private compute | Blocks model promotion, not classical app | Manual/nightly candidate |
| Map graph | Source lineage, topology, direction, stable IDs | No field legality/current drivability | Host | Yes using public lawful tiny fixture/S6 artifact metadata | Every graph change |
| Map matching | Top-K, abstention, ambiguity and false-CLEAR gates | No universal scientific validity | Host/Android | Yes for logical fixtures | Every PR smoke; nightly/oracle |
| Integration | Queues/JNI/core/integrity/map/output together | No OEM/field performance | Emulator/host/device | Yes for smoke | Nightly/release |
| Physical device | Delivered rates, screen-off, FGS, thermal/storage and live flow on named devices | No universal Android proof | Named phones | No ordinary PR; blocks device claims/release | Manual protocol |
| End-to-end demo | Ten honest events and after-run evidence | No production safety certification | Controlled replay/live rehearsal | Blocks demo release | Every release candidate |

## CI workflow inventory

1. `pr-fast`: formatting, static analysis, schema compatibility, manifest/secret/private-pattern scan, C++ unit/parity smoke, Python unit, Android JVM/lint and public deterministic replay.
2. `android-build`: debug/release compile, lint, JVM, JNI packaging and emulator instrumentation where available.
3. `cpp-core`: pinned CMake build, warnings-as-errors, sanitizers in scheduled lane, S2 fixtures/parity.
4. `python-offline`: unit tests only on synthetic/tiny lawful fixtures; no IO-VNBD download.
5. `contracts`: codegen-diff, backward compatibility, unit/frame/clock checks.
6. `determinism`: repeated fixtures compare hashes/decision traces within declared numeric tolerance.
7. `security`: secret scan, dependency review, SBOM/licence notices and forbidden private artifact patterns.
8. `docs`: internal relative-link, Mermaid syntax where supported and filename/status checks.
9. `nightly-heavy`: sanitizers, broad parity seeds, full replay/map fixtures and optional emulator matrix.
10. `private-experiment` and `device-protocol`: manual protected environments; outputs are manifests/reports, never raw data in public CI.
11. `release-verify`: clean checkout, pinned toolchains, signed build identity, APK/engine/schema/map/model manifests, clean extraction and network-isolated rehearsal.

PR jobs target limited student compute: cache pinned dependencies, shard only independent jobs, keep one small public fixture, cancel superseded runs, and never make GPU/private data/device availability a condition for unrelated changes.

## Claim gates

Repository bootstrap is gated by architecture consistency only. Model promotion requires S4; alignment-dependent live constraints require S3; named-device claims require completed S1; field route claims require permission/safety; drift claims require adequate reference and frozen metric. A smooth demo alone proves none of these.
