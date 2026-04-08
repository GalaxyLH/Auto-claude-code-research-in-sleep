import importlib.util
import json
from pathlib import Path
from subprocess import CompletedProcess


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "deepxiv_fetch.py"


def load_module():
    spec = importlib.util.spec_from_file_location("deepxiv_fetch", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_ensure_deepxiv_installed_returns_error_when_binary_missing(monkeypatch):
    deepxiv_fetch = load_module()
    monkeypatch.setattr(deepxiv_fetch.shutil, "which", lambda _: None)

    info = deepxiv_fetch.ensure_deepxiv_installed()

    assert info["ok"] is False
    assert "pip install deepxiv-sdk" in info["message"]


def test_run_cli_json_returns_decoded_payload(monkeypatch):
    deepxiv_fetch = load_module()
    monkeypatch.setattr(deepxiv_fetch.shutil, "which", lambda _: "deepxiv")

    def fake_run(*args, **kwargs):
        return CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=json.dumps({"results": []}),
            stderr="",
        )

    monkeypatch.setattr(deepxiv_fetch.subprocess, "run", fake_run)

    payload = deepxiv_fetch.run_cli_json(["search", "agent memory", "--output", "json"])

    assert payload == {"results": []}


def test_run_cli_text_returns_stdout(monkeypatch):
    deepxiv_fetch = load_module()
    monkeypatch.setattr(deepxiv_fetch.shutil, "which", lambda _: "deepxiv")

    def fake_run(*args, **kwargs):
        return CompletedProcess(args=args[0], returncode=0, stdout="ok\n", stderr="")

    monkeypatch.setattr(deepxiv_fetch.subprocess, "run", fake_run)

    payload = deepxiv_fetch.run_cli_text(["health"])

    assert payload == "ok"


def test_cli_parser_builds_help_without_traceback():
    deepxiv_fetch = load_module()

    parser = deepxiv_fetch.build_parser()

    help_text = parser.format_help()

    assert "search" in help_text
    assert "paper-brief" in help_text
