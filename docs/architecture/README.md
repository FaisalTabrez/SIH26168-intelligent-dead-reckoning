# SIH26168 Architecture Revision 3 Working Development Baseline

**Architecture status:** `ARCH3-READY-FOR-REPOSITORY-BOOTSTRAP`  
**Decision date:** 2026-09-02  
**Scope:** Architecture, contracts, repository implications and issue-ready work packages. No production code, repository, GitHub issue, repeated spike or field-route approval is included.

## Decision

The project is sufficiently reconciled to create a monorepo, schemas, CI scaffold and issue backlog. This status does **not** mean S1, S3, S4, Android map rendering, runtime map matching, field access, device generalization or drift performance has passed.

The development baseline is a standalone, offline-first Android app plus a portable C++ navigation core. The accepted S2 core is the sole owner of `p^n`, `v^n`, `q^n_b`, accelerometer/gyro bias posteriors, covariance and the evidence-ID ledger. Android acquisition preserves raw axes and source clocks. S3 alignment remains an external, uncertainty-bearing `b→v` estimate used only by eligible vehicle constraints and learned features. Learned and map proposals are optional, bounded and rejectable; neither may replace propagation or conceal divergence.

## Package map

- [High-level architecture](SIH26168_High_Level_Architecture_Revision3.md)
- [Development design baseline](SIH26168_Development_Design_Baseline_v1.md)
- [Interface inventory](SIH26168_Interface_Inventory_v1.md)
- [Component register](SIH26168_Component_Register_v1.csv)
- [ADR register](SIH26168_ADR_Register_v1.md)
- [Risk register](SIH26168_Risk_Register_v1.csv)
- [Verification strategy](SIH26168_Verification_Strategy_v1.md)
- [Demo architecture](SIH26168_Demo_Architecture_v1.md)
- [Repository blueprint](SIH26168_Repository_Blueprint_v1.md)
- [Development sequence](SIH26168_Development_Sequence_v1.md)
- [Open decisions](SIH26168_Open_Decisions_v1.md)
- [Architecture manifest](SIH26168_ARCHITECTURE_MANIFEST_v1.json)

`machine_readable/` contains components, interfaces, work packages, risks and the status/requirement-coverage record.

## Evidence status carried forward

| Gate | Revision 3 treatment |
| --- | --- |
| S0 | `S0-CONDITIONAL — ORGANIZER-DIRECTED COMPETITION USE`: private competition experimentation may proceed; raw data/extracts stay out of the public repo; redistribution and model-weight release remain conditional; scientific limitations remain. |
| S1 | `S1-PENDING-DEVICE-EVIDENCE`: supplied report has no executed physical protocol measurements. A task-level assertion of a OnePlus run is not used quantitatively because its session/analyzer evidence is absent here. |
| S2 | Accepted for bounded mathematical conventions and numerical parity; not evidence of phone drift performance. |
| S3 | Unresolved and mandatory before an alignment-dependent live car claim. |
| S4 | Experimental; the baseline runs with the learned component disabled. |
| S6A/S6B1 | Conditional foundations. Frozen PBF/graph lineage and two candidate routes exist; both routes remain `FIELD_VALIDATION_PENDING`; Android renderer and runtime matcher are not established. |

## Public/private boundary

Public: source code, schemas, synthetic fixtures, integrity tooling, download instructions, manifests without private paths, map/code notices where lawful. Private: IO-VNBD raw files/extracts, private recordings, exact sensitive routes, credentials, unapproved derived labels, and redistribution-conditional weights.
