from click.testing import CliRunner

from solaris.cli.analyze import analyze


def _listed_analyzer_names(output: str) -> list[str]:
    names = []
    for line in output.splitlines():
        if line.startswith('分析器: '):
            names.append(line.removeprefix('分析器: ').split(' |')[0])
    return names


def test_overlapping_packages_do_not_duplicate_analyzers():
    """pet 包会递归导入 skill 包也导出的分析器，重复类曾让拓扑排序误报循环依赖"""
    runner = CliRunner()
    result = runner.invoke(
        analyze,
        [
            '--package-name',
            'solaris.analyze.analyzers.pet',
            '--package-name',
            'solaris.analyze.analyzers.skill',
            '--list-analyzers',
            'data',
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    analyzer_names = _listed_analyzer_names(result.output)
    assert len(analyzer_names) == len(set(analyzer_names))
    # 两个包共有的分析器只保留一份
    assert analyzer_names.count('PetAdvanceAnalyzer') == 1
    assert 'SkillAnalyzer' in analyzer_names
