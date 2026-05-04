"""End-to-end tests for `mdfic copyedit` with the LangChain chain mocked.

The autouse fixture sets `OPENAI_USER` and stubs `keyring.get_password` so the
module-level keyring lookup in `mdfic/copyedit.py` does not trigger a keychain
prompt on dev machines where `OPENAI_USER` is set in the shell.
"""
import pytest

from mdfic.cli import cli


@pytest.fixture(autouse=True)
def safe_copyedit_env(monkeypatch):
    monkeypatch.setenv("OPENAI_USER", "test_user")
    monkeypatch.setattr("keyring.get_password", lambda *a, **kw: "sk-stub")
    # Trigger import under the safe environment so module-level init (env
    # read + keyring lookup + ChatOpenAI instantiation) happens with our
    # patches in place. Subsequent calls are cached no-ops.
    import mdfic.copyedit  # noqa: F401


class _FakeChain:
    def __init__(self, response="[edited stub output]"):
        self.calls = []
        self.response = response

    def invoke(self, msg):
        self.calls.append(msg)
        return self.response


def test_copyedit_emits_yaml_frontmatter(cli_runner, monkeypatch, single_story, tmp_path):
    fake = _FakeChain()
    monkeypatch.setattr("mdfic.copyedit.copy_editor_chain", fake)

    out = tmp_path / "edited.md"
    result = cli_runner.invoke(cli, ["copyedit", "-o", str(out), str(single_story)])
    assert result.exit_code == 0, result.output

    edited = out.read_text()
    assert edited.startswith("---\n")
    assert "\n...\n" in edited
    assert "[edited stub output]" in edited


def test_copyedit_invokes_chain_per_chunk(cli_runner, monkeypatch, single_story, tmp_path):
    fake = _FakeChain()
    monkeypatch.setattr("mdfic.copyedit.copy_editor_chain", fake)

    out = tmp_path / "edited.md"
    result = cli_runner.invoke(cli, ["copyedit", "-o", str(out), str(single_story)])
    assert result.exit_code == 0, result.output

    # The single asset is well under MAX_WORDS*6 chars, so it produces one chunk.
    assert len(fake.calls) == 1


def test_copyedit_passes_strength_to_chain(cli_runner, monkeypatch, single_story, tmp_path):
    fake = _FakeChain()
    monkeypatch.setattr("mdfic.copyedit.copy_editor_chain", fake)

    out = tmp_path / "edited.md"
    result = cli_runner.invoke(
        cli,
        ["copyedit", "--strength", "heavy", "-o", str(out), str(single_story)],
    )
    assert result.exit_code == 0, result.output

    assert all(call["strength"] == "heavy" for call in fake.calls)
    assert all("text" in call for call in fake.calls)
