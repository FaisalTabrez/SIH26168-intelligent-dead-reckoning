# SIH26168 Repository Blueprint v1

## Monorepo tree

```text
/
├── android/app/                  # Compose app, FGS, UI, live/replay wiring
├── android/acquisition/          # Sensor/location adapters and writer
├── android/navigation-jni/       # JNI wrapper and Android packaging
├── core/navigation/              # Portable C++20 S2 core
├── core/include/                 # Public edge-engine API only
├── contracts/                    # Proto/JSON Schema/enums and generated policy
├── tools/analyzer/               # Python session/evaluation tooling
├── tools/dataset/                # IO-VNBD adapters; no data
├── tools/training/               # Baselines/training/export; no weights by default
├── tools/maps/                   # PBF→graph/display builds and lineage
├── fixtures/public/              # Synthetic/de-identified deterministic fixtures
├── experiments/manifests/        # Non-sensitive run manifests and templates
├── demo/scenarios/               # Frozen masks/scripts; no private recordings
├── docs/architecture/            # Revision 3 and ADRs
├── docs/protocols/               # Device, field, privacy, release protocols
├── ci/                           # Reproducible scripts invoked by workflows
└── third_party/notices/          # Licences/attribution/SBOM inputs
```

## Dependency rules

Allowed: `android/app → acquisition/navigation-jni/contracts`; `navigation-jni → core/contracts`; offline tools → contracts and read-only artifacts; demo → public scenarios/contracts. Core may depend on Eigen and generated contract primitives, never Android, UI, map renderer, Python, network or model runtime. Matcher consumes core output but cannot mutate core internals. Training cannot be an Android build dependency.

Forbidden: UI/display → core feedback; map-matched/display position as GNSS/core measurement; vehicle/VBOX/CAN/wheel fields in runtime features; Play-services-only location requirement; network/cloud inference; public CI → private dataset/recording; Android app → Python; direct cross-module imports bypassing public contracts.

## Ownership

| Area | Primary | Mandatory reviewer | Bounded collaboration |
| --- | --- | --- | --- |
| Core/JNI/canonical contracts | R1 | designated second technical integrator (default R5) + R4 for evidence | Beginners receive fixtures/docs, not convention changes. |
| Acquisition/app/UI | R5 | R1 for scientific boundary; R4 tests | R6 UI copy/demo states. |
| Dataset ingestion | R2 | R4 + R3 | Bounded schema/dedup tasks. |
| ML | R3 | R1 safety boundary + R4 evaluation | No model influence without validator. |
| CI/analyzer/map build/release | R4 | R1 | R2/R3 add domain tests. |
| Demo/field/docs/pitch | R6 | R1 scientific claims + R4 evidence | Own scripts/checklists, never manufacture results. |

Changes to S2 conventions, I-01..I-22 major schemas, state ownership, feature firewall, GNSS/map/model influence, metric definitions, privacy/licensing and release manifests require both technical-lead and evidence-owner review. CODEOWNERS must enforce this.

## Artifact policy

Never commit raw IO-VNBD archives/CSVs/JPGs/extracts, team raw recordings, sensitive exact routes, credentials, API tokens, signing keys, local SDKs, build outputs, unapproved weights, provider-generated third-party map imagery or files with absolute paths. Use templates and hash-only private manifest references. `.gitignore`, pre-commit and CI forbidden-pattern/size checks overlap intentionally.

Generated files are committed only when consumers cannot generate them cheaply and their source/tool/hash header is deterministic; otherwise CI generates and diffs them. Large binaries use release storage or documented private artifact storage, not Git LFS by default. Public fixtures must be synthetic/de-identified, small, licensed and accompanied by expected outputs. Secrets come only from protected runtime/CI stores and are never needed for the offline app.

## Bootstrap milestone acceptance

Create directories/build roots, ownership/CODEOWNERS, contribution/PR templates, labels/milestones later from WP IDs, branch rules, lockfiles, schema skeleton, one C++/Kotlin/Python smoke test, public synthetic fixture, fast CI lanes, privacy/licence policies and ADR index. Do not add IO-VNBD, production algorithms or GitHub issues until the subsequent repository task.
