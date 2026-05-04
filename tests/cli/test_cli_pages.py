"""End-to-end tests for `mdfic pages-to-pdf` with the AppleScript runner mocked."""
from mdfic.cli import cli


def test_pages_to_pdf_constructs_correct_script(cli_runner, monkeypatch, tmp_path):
    captured = []
    monkeypatch.setattr("mdfic.utils.oascript", lambda script: captured.append(script))

    inp = tmp_path / "input.docx"
    out = tmp_path / "output.pdf"

    result = cli_runner.invoke(cli, ["pages-to-pdf", "-o", str(out), str(inp)])
    assert result.exit_code == 0, result.output
    assert len(captured) == 1

    script = captured[0]
    assert 'tell application "Pages"' in script
    assert f'POSIX file "{inp}"' in script
    assert f'POSIX file "{out}"' in script
    assert "export to output as PDF" in script


def test_pages_to_pdf_default_output_relative_to_cwd(cli_runner, monkeypatch, tmp_path):
    captured = []
    monkeypatch.setattr("mdfic.utils.oascript", lambda script: captured.append(script))
    monkeypatch.chdir(tmp_path)

    inp = tmp_path / "input.docx"

    result = cli_runner.invoke(cli, ["pages-to-pdf", str(inp)])
    assert result.exit_code == 0, result.output
    assert len(captured) == 1

    expected_out = tmp_path / "story.pdf"
    assert f'POSIX file "{expected_out}"' in captured[0]
