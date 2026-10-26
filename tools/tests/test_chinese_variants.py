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


@pytest.mark.parametrize(
    ("simplified", "traditional"),
    [
        ("恢复", "恢復"),
        ("回复", "回覆"),
        ("反复", "反覆"),
        ("头发", "頭髮"),
        ("复制", "複製"),
        ("修复", "修復"),
        ("公里", "公里"),
        ("请回复邮件", "請回覆郵件"),
    ],
)
def test_word_level_simplified_converts_to_the_word_taiwan_uses(
    simplified: str, traditional: str
) -> None:
    assert zh.s2t(simplified) == traditional


def test_character_level_conversion_still_applies_outside_listed_words() -> None:
    assert zh.s2t("复杂") == "複雜"
    assert zh.s2t("发现") == "發現"
    assert zh.s2t("制度") == "制度"


def test_reply_query_also_expands_to_the_other_taiwan_form() -> None:
    expanded = zh.expand_query_tokens(["回复"])
    assert "回覆" in expanded and "回復" in expanded
    assert zh.s2t("回复") == "回覆"  # primary conversion never picks 回複


@pytest.mark.parametrize("simplified", ["恢复", "回复", "反复", "头发", "复制", "修复"])
def test_word_level_queries_reach_the_corpus(simplified: str, corpus: str) -> None:
    assert any(t in corpus for t in zh.expand_query_tokens([simplified]))


@pytest.mark.parametrize(
    ("simplified", "traditional"),
    [
        ("开发型", "開發型"),
        ("研发型", "研發型"),
        ("机制作用", "機制作用"),
        ("控制作业", "控制作業"),
        ("机制造成", "機制造成"),
    ],
)
def test_word_table_does_not_misfire_across_word_boundaries(
    simplified: str, traditional: str
) -> None:
    assert zh.s2t(simplified) == traditional


def test_search_expansion_keeps_the_character_table_form() -> None:
    assert "開發型" in zh.expand_query_tokens(["开发型"])
    assert "機制作用" in zh.expand_query_tokens(["机制作用"])
    assert "製作" in zh.expand_query_tokens(["制作"])
    assert "髮型" in zh.expand_query_tokens(["发型"])


def test_hair_converts_back_to_simplified() -> None:
    assert zh.t2s("頭髮") == "头发"


@pytest.mark.parametrize(
    "simplified",
    ["重复原来", "重复发生", "重复活动", "重复位置", "处理发现", "回答复杂", "汇报复杂度", "健康复杂"],
)
def test_word_boundary_straddling_text_gets_plain_character_conversion(
    simplified: str,
) -> None:
    plain = "".join(zh.S2T_MAP.get(c, c) for c in simplified)
    assert zh.s2t(simplified) == plain


def test_alternate_only_words_still_widen_search() -> None:
    assert "復原" in zh.expand_query_tokens(["复原"])
    assert "理髮" in zh.expand_query_tokens(["理发"])
    assert "康復" in zh.expand_query_tokens(["康复"])
