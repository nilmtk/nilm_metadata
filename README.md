# NILM Metadata

NILM Metadata gives energy datasets a shared vocabulary and structure. It is
the place to define appliance names, meter relationships, buildings, and
dataset metadata so that tools do not need a different naming rule for every
dataset.

This repository contains:

- the controlled appliance vocabulary in YAML;
- the dataset, building, meter, and appliance schema;
- Python helpers that resolve inherited appliance types; and
- an optional YAML-to-HDF5 converter.

It does not contain energy readings, dataset downloads, disaggregation models,
or benchmark results.

## Ecosystem repositories

| Research task | Repository |
| --- | --- |
| Dataset conversion, meter access, preprocessing, and metrics | [NILMTK core](https://github.com/nilmtk/nilmtk) |
| Appliance taxonomy, synonyms, meter relationships, and dataset schema | **NILM Metadata — this repository** |
| Disaggregation model implementation and testing | [nilmtk-contrib](https://github.com/nilmtk/nilmtk-contrib) |
| Fixed T1/T2/T3 evaluation and published result bundles | [NILMbench](https://github.com/nilmtk/nilmbench) |

The [NILMTK start page](https://nilmtk.github.io/) connects the four projects.

## Install and verify

Use Python 3.11 for the shared NILMTK environment. Install
[uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install \
  "nilm-metadata @ git+https://github.com/nilmtk/nilm_metadata.git"
python -c "from nilm_metadata import get_appliance_types; print(get_appliance_types()['fridge']['type'])"
```

The last command should print `fridge`. On Windows PowerShell, activate the
environment with `.venv\Scripts\Activate.ps1`.

If you need the standalone YAML-to-HDF5 converter, install the HDF5 extra:

```bash
uv pip install \
  "nilm-metadata[hdf5] @ git+https://github.com/nilmtk/nilm_metadata.git"
```

NILMTK core already supplies its own HDF5 dependency.

## Use the appliance vocabulary

`get_appliance_types()` returns the resolved vocabulary. Parent fields and
components have already been inherited.

```python
from nilm_metadata import get_appliance_types

appliance_types = get_appliance_types()
fridge = appliance_types["fridge"]

print(fridge["categories"])
print(fridge.get("synonyms", []))
```

The source vocabulary is split by domain under
[`nilm_metadata/central_metadata/appliance_types`](nilm_metadata/central_metadata/appliance_types).

## Describe a dataset

A dataset metadata directory normally contains:

```text
metadata/
├── dataset.yaml
├── meter_devices.yaml
├── building1.yaml
└── building2.yaml
```

- `dataset.yaml` describes the dataset and its provenance.
- `meter_devices.yaml` describes each meter model.
- `buildingN.yaml` maps meters, wiring, and appliances for one building.

Start with the [worked tutorial](https://nilm-metadata.readthedocs.io/en/latest/tutorial.html),
then use the [dataset schema](https://nilm-metadata.readthedocs.io/en/latest/dataset_metadata.html)
for the complete field reference.

With the `hdf5` extra installed, write the YAML metadata into a NILMTK HDF5
file with:

```python
from nilm_metadata import convert_yaml_to_hdf5

convert_yaml_to_hdf5("metadata", "dataset.h5")
```

The converter appends metadata to the target HDF5 file. Keep the original YAML
with the dataset as the readable archival representation.

## Add or change an appliance type

1. Search the existing YAML files for the canonical type and its synonyms.
2. Edit the closest domain file. Reuse a parent instead of copying inherited
   fields.
3. Add a focused test when inheritance, components, or a public name changes.
4. Run the complete local gate:

```bash
git clone https://github.com/nilmtk/nilm_metadata.git
cd nilm_metadata
uv sync --frozen --extra dev --extra hdf5
uv run python scripts/check_docs.py
uv run pytest
uv run sphinx-build -E -W --keep-going -b html docs/source docs/build/html
uv build
uv run python scripts/check_distribution.py dist
```

A vocabulary PR should explain why the new canonical name is needed, list the
source dataset labels it normalizes, and cite an external standard or dataset
documentation when one exists.

## Docker

There is no metadata-only Docker image. The package is small and installs in
the same Python environment as NILMTK. The general nilmtk-contrib development
image includes it; NILMbench owns the pinned CPU and CUDA benchmark images.

## Citation

If you use NILM Metadata in research, cite the metadata paper:

```bibtex
@inproceedings{kelly2014metadata,
  title     = {Metadata for Energy Disaggregation},
  author    = {Kelly, Jack and Knottenbelt, William},
  booktitle = {2014 IEEE 38th International Computer Software and
               Applications Conference Workshops},
  year      = {2014},
  pages     = {578--583},
  doi       = {10.1109/COMPSACW.2014.97}
}
```

Paper: [DOI 10.1109/COMPSACW.2014.97](https://doi.org/10.1109/COMPSACW.2014.97) ·
[arXiv:1403.5946](https://arxiv.org/abs/1403.5946)

Also cite each dataset whose measurements you use. Cite model papers through
nilmtk-contrib, and cite NILMbench only when using its protocols, runner, or
leaderboard results.

## Documentation and support

- [Tutorial](https://nilm-metadata.readthedocs.io/en/latest/tutorial.html)
- [Dataset metadata reference](https://nilm-metadata.readthedocs.io/en/latest/dataset_metadata.html)
- [Central appliance metadata reference](https://nilm-metadata.readthedocs.io/en/latest/central_metadata.html)
- [Issues](https://github.com/nilmtk/nilm_metadata/issues)

NILM Metadata is licensed under the Apache License 2.0.
