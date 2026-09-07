# Generated Contract Bindings

This directory contains deterministic target language bindings produced by [`ci/generate_contract_bindings.py`](../../ci/generate_contract_bindings.py) from JSON Schema Draft 2020-12 and canonical enum contracts, adhering strictly to [`docs/GENERATED_FILE_POLICY.md`](../../docs/GENERATED_FILE_POLICY.md).

## Generated Artifacts

- **`contract_version.json`**: Canonical JSON manifest tracking the contract version and all source schema inputs.
- **`cpp/`**:
  - `enums.hpp`: Strongly typed C++20 `enum class` definitions with `constexpr std::string_view to_string(...)` and `parse_...` helpers in `namespace sih26168::contracts`.
  - `models.hpp`: C++20 data structures for base envelopes, timestamps, and provenance headers.
- **`python/`**:
  - `enums.py`: Python `StrEnum` / `Enum` classes matching all canonical state enumerations.
  - `models.py`: Frozen dataclass models for base envelopes, timestamps, provenance, and validity gates with `.to_dict()` and `.from_dict()` serialization.
  - `__init__.py`: Clean package re-export.
- **`kotlin/`**:
  - `Enums.kt`: Kotlin `enum class` definitions in package `org.sih26168.contracts.enums`.
  - `Models.kt`: Kotlin `data class` definitions in package `org.sih26168.contracts.models`.

## Drift Verification and Regeneration

To verify on-disk artifacts against source schemas (as executed in CI `generated-file-drift-check`):
```bash
python ci/generate_contract_bindings.py --check
```

To deterministically regenerate all bindings:
```bash
python ci/generate_contract_bindings.py
```
