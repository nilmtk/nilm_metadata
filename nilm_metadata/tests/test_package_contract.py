from __future__ import annotations

from importlib.resources import files

import pandas as pd
import yaml

from nilm_metadata import convert_yaml_to_hdf5, get_appliance_types


def write_yaml(path, document) -> None:
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def test_packaged_vocabulary_is_available() -> None:
    package = files("nilm_metadata")
    appliance_file = package.joinpath(
        "central_metadata", "appliance_types", "appliance.yaml"
    )
    country_file = package.joinpath("central_metadata", "country.yaml")

    assert appliance_file.is_file()
    assert country_file.is_file()
    assert get_appliance_types()["fridge"]["type"] == "fridge"


def test_yaml_to_hdf5_conversion_round_trip(tmp_path) -> None:
    metadata_dir = tmp_path / "metadata"
    metadata_dir.mkdir()
    output = tmp_path / "dataset.h5"

    write_yaml(metadata_dir / "dataset.yaml", {"name": "TEST"})
    write_yaml(
        metadata_dir / "meter_devices.yaml",
        {
            "test-meter": {
                "sample_period": 6,
                "measurements": [
                    {"physical_quantity": "power", "type": "active"}
                ],
            }
        },
    )
    write_yaml(
        metadata_dir / "building1.yaml",
        {
            "instance": 1,
            "elec_meters": {
                1: {"site_meter": True, "device_model": "test-meter"},
                2: {"submeter_of": 1, "device_model": "test-meter"},
            },
            "appliances": [{"type": "fridge", "instance": 1, "meters": [2]}],
        },
    )

    convert_yaml_to_hdf5(str(metadata_dir), str(output))

    with pd.HDFStore(output, mode="r") as store:
        assert store.root._v_attrs.metadata["name"] == "TEST"
        building = store.get_node("/building1")._v_attrs.metadata
        assert building["appliances"][0]["type"] == "fridge"
        assert building["elec_meters"][2]["data_location"] == (
            "/building1/elec/meter2"
        )
