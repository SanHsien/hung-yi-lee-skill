"""維護工具的邊界輸入：套件名稱正規化、Markdown 連結語法。"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_dependency_freshness as fresh
import check_links


@pytest.mark.parametrize("declared", ["typing_extensions", "Typing.Extensions"])
def test_deferral_matches_pypi_normalized_name(
    declared: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(fresh, "fetch_pypi_version", lambda name: "5.0.0")
    packages = fresh.parse_requirements(f"{declared}>=4.0\n", "requirements.txt")
    rows = fresh.collect_status(
        packages, deferrals={"typing-extensions": ("5.0.0", "reviewed")}
    )
    assert rows[0]["deferred_reason"] == "reviewed"
    assert fresh.needs_review(rows[0]) is False


def test_deferral_file_keys_are_normalized(tmp_path: Path) -> None:
    path = tmp_path / "d.json"
    path.write_text(
        '{"deferrals": {"Typing_Extensions": {"deferredLatest": "5", "reason": "x"}}}',
        encoding="utf-8",
    )
    assert "typing-extensions" in fresh.load_deferrals(path)


def test_duplicate_requirement_with_dot_and_dash_is_deduped(tmp_path: Path) -> None:
    (tmp_path / "requirements-dev.txt").write_text("zope.interface>=5\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("zope-interface>=5\n", encoding="utf-8")
    assert len(fresh.load_direct_dependencies(tmp_path)) == 1


def _check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, text: str) -> list[str]:
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    doc = tmp_path / "doc.md"
    (tmp_path / "real.md").write_text("x", encoding="utf-8")
    doc.write_text(text, encoding="utf-8")
    return check_links.check_document(doc)


def test_link_title_is_not_part_of_the_path(tmp_path, monkeypatch) -> None:
    assert _check(tmp_path, monkeypatch, '[a](real.md "a title")\n') == []


def test_missing_image_is_reported_once(tmp_path, monkeypatch) -> None:
    assert len(_check(tmp_path, monkeypatch, "![a](gone.png)\n")) == 1


def test_links_inside_code_fences_are_ignored(tmp_path, monkeypatch) -> None:
    text = "```md\n[example](nowhere.md)\n```\n"
    assert _check(tmp_path, monkeypatch, text) == []
