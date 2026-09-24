from pathlib import Path

import pytest

from solaris.analyze.settings import DataSourceDirSettings


@pytest.fixture(autouse=True)
def clear_solaris_data_env(monkeypatch):
    """隔离开发机上可能存在的 SOLARIS_DATA_* 环境变量"""
    for name in (
        'SOLARIS_DATA_BASE_DIR',
        'SOLARIS_DATA_PATCH_DIR',
        'SOLARIS_DATA_HTML5_DIR',
        'SOLARIS_DATA_UNITY_DIR',
        'SOLARIS_DATA_FLASH_DIR',
    ):
        monkeypatch.delenv(name, raising=False)


def test_sub_dirs_derive_from_base_dir():
    settings = DataSourceDirSettings(BASE_DIR='custom')

    assert settings.PATCH_DIR == Path('custom') / 'patch'
    assert settings.HTML5_DIR == Path('custom') / 'html5'
    assert settings.UNITY_DIR == Path('custom') / 'unity'
    assert settings.FLASH_DIR == Path('custom') / 'flash'


def test_default_base_dir_keeps_source_layout():
    settings = DataSourceDirSettings()

    assert settings.BASE_DIR == Path('./source')
    assert settings.UNITY_DIR == Path('./source') / 'unity'
    assert settings.PATCH_DIR == Path('./source') / 'patch'


def test_explicit_sub_dir_wins_over_base_dir():
    settings = DataSourceDirSettings(
        BASE_DIR='custom',
        UNITY_DIR='/elsewhere/unity',
    )

    assert settings.UNITY_DIR == Path('/elsewhere/unity')
    assert settings.PATCH_DIR == Path('custom') / 'patch'
