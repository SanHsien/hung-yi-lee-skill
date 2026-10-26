"""簡體查詢轉繁體後，必須落在逐字稿實際使用的臺灣常用字形上。

字表的一對一轉換會挑到異體字（為→爲、裡→裏）或香港／大陸字形（複→復），
於是「因为」「复杂」「这里」這類簡體查詢轉出的詞在語料裡一次都出現不了。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import hungyi_chinese as zh

TRANSCRIPTS = sorted((ROOT / "raw" / "youtube" / "transcripts").glob("*.md"))


@pytest.fixture(scope="module")
def corpus() -> str:
    return "".join(path.read_text(encoding="utf-8") for path in TRANSCRIPTS)


@pytest.mark.parametrize(
    "simplified",
    ["因为", "为了", "作为", "复杂", "重复", "这里", "台湾"],
)
def test_simplified_query_reaches_a_form_the_transcripts_use(
    simplified: str, corpus: str
) -> None:
    expanded = zh.expand_query_tokens([simplified])
    hits = [token for token in expanded if token in corpus]
    assert hits, f"{simplified!r} expanded to {expanded!r}, none occur in the corpus"


def test_variant_forms_are_not_chosen_as_the_traditional_form() -> None:
    assert zh.s2t("为") == "為"
    assert zh.s2t("里面") == "裡面"
    assert zh.s2t("接着") == "接著"
    assert zh.s2t("复杂") == "複雜"
    assert zh.s2t("台湾") == "台灣"


def test_traditional_taiwan_forms_convert_back_to_simplified() -> None:
    assert zh.t2s("因為") == "因为"
    assert zh.t2s("這裡") == "这里"
    assert zh.t2s("複雜") == "复杂"
