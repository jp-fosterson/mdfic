"""End-to-end tests for `mdfic progress` against a real tmp git repo."""
import subprocess

from mdfic.cli import cli


def _commit_all(repo, msg):
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg], check=True)


def test_progress_counts_added_words(cli_runner, tmp_git_repo):
    story = tmp_git_repo / "story.md"
    story.write_text("initial content here\n")
    _commit_all(tmp_git_repo, "init")

    story.write_text("initial content here\nfive new added words here\n")

    result = cli_runner.invoke(cli, ["progress"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "5"


def test_progress_zero_when_clean(cli_runner, tmp_git_repo):
    story = tmp_git_repo / "story.md"
    story.write_text("nothing\n")
    _commit_all(tmp_git_repo, "init")

    result = cli_runner.invoke(cli, ["progress"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "0"


def test_progress_since_counts_historical_diff(cli_runner, tmp_git_repo):
    story = tmp_git_repo / "story.md"
    story.write_text("first commit content\n")
    _commit_all(tmp_git_repo, "first")

    story.write_text("first commit content\nfour additional new words\n")
    _commit_all(tmp_git_repo, "second")

    # --since 1 -> HEAD@{1} (state after first commit). Diff to HEAD is the
    # second commit's additions.
    result = cli_runner.invoke(cli, ["progress", "--since", "1"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "4"
