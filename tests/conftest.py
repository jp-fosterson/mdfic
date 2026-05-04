from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def asset_dir():
    return Path(__file__).parent / "assets"


@pytest.fixture
def single_story(asset_dir):
    return asset_dir / "single" / "single.md"


@pytest.fixture
def multi_metadata(asset_dir):
    return asset_dir / "multi" / "metadata.yaml"


@pytest.fixture
def multi_parts(asset_dir):
    return [
        asset_dir / "multi" / "multi-01.md",
        asset_dir / "multi" / "multi-02.md",
    ]
