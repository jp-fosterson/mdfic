import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner


def pytest_collection_modifyitems(config, items):
    if shutil.which("pandoc") is not None:
        return
    skip_pandoc = pytest.mark.skip(reason="pandoc not on PATH")
    for item in items:
        if "pandoc" in item.keywords:
            item.add_marker(skip_pandoc)


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
