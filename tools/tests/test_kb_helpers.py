from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import hungyi_kb as kb


def test_slugify_converts_symbols_and_preserves_cjk() -> None:
    assert kb.slugify("Hello World") == "hello-world"
    assert kb.slugify("機器學習 & 深度學習") == "機器學習-and-深度學習"
    assert kb.slugify("---test--case---") == "test-case"
    assert kb.slugify("") == "untitled"


def test_timestamp_formatting() -> None:
    assert kb.timestamp(0) == "00:00:00"
    assert kb.timestamp(65) == "00:01:05"
    assert kb.timestamp(3665) == "01:01:05"


def test_parse_series_detects_brackets_and_separators() -> None:
    assert kb.parse_series("【生成式AI導論 2024】第10講：Transformer") == "生成式AI導論 2024"
    assert kb.parse_series("ML 2021: Regression") == "ML 2021"
    assert kb.parse_series("深度學習：類神經網路") == "深度學習"
    assert kb.parse_series("Special Lecture - Model Editing") == "Special Lecture"
    assert kb.parse_series("General Talk on Future AI") == "Standalone Talks"


def test_infer_topics_maps_keywords() -> None:
    topics = kb.infer_topics("Transformer and LLM introduction")
    assert "llm-and-transformers" in topics

    topics_speech = kb.infer_topics("語音辨識與合成技術")
    assert "speech-and-audio" in topics_speech

    fallback = kb.infer_topics("A completely unrelated title with zero ML buzzwords")
    assert fallback == ["ml-fundamentals"]


def test_simplified_to_traditional_conversion() -> None:
    from hungyi_chinese import s2t, t2s

    assert s2t("语言模型深度学习强化学习") == "語言模型深度學習強化學習"
    assert t2s("語言模型深度學習強化學習") == "语言模型深度学习强化学习"
    assert s2t("知识图谱与神经网络") == "知識圖譜與神經網絡"


def test_tokenize_query_chinese_expansion() -> None:
    tokens_llm = kb.tokenize_query("语言模型")
    assert "语言模型" in tokens_llm
    assert "語言模型" in tokens_llm

    tokens_rl = kb.tokenize_query("强化学习")
    assert "强化学习" in tokens_rl
    assert "強化學習" in tokens_rl
    assert "增強式學習" in tokens_rl or "增強學習" in tokens_rl


def test_search_with_simplified_query() -> None:
    # Existing cached videos should be matchable via simplified Chinese query
    payload = kb.search("语言模型", limit=3)
    assert payload["query"] == "语言模型"
    assert "語言模型" in payload["tokens"]
    assert len(payload["results"]) > 0
    assert payload["results"][0]["score"] > 0


def test_file_io_utf8_resilience(tmp_path: Path) -> None:
    # Verify save_json, load_json, and write_markdown handle CJK properly without environment dependency
    sample_data = {"title": "語言模型深度學習", "topics": ["繁體中文", "簡體中文-语言模型"]}
    json_file = tmp_path / "test.json"
    kb.save_json(json_file, sample_data)

    loaded = kb.load_json(json_file, {})
    assert loaded == sample_data

    md_file = tmp_path / "test.md"
    kb.write_markdown(md_file, "# 測試文件\n內容包含繁體與簡體字。")
    read_back = md_file.read_text(encoding="utf-8")
    assert "測試文件" in read_back
    assert "簡體字" in read_back


def test_now_iso_format_and_py310_utc_compat() -> None:
    iso = kb.now_iso()
    assert "+00:00" in iso or "Z" in iso
    assert kb.UTC is not None


def test_graph_query_and_token_matching() -> None:
    pytest.importorskip("networkx")
    import networkx as nx
    from hungyi_graph import query_graph

    G = nx.Graph()
    G.add_node("concept:transformer", label="Transformer", type="concept")
    G.add_node("concept:attention", label="Self-Attention", type="concept")
    G.add_node("video:v1", label="生成式AI 2024 第3講 Transformer", type="video")
    G.add_edge("concept:transformer", "concept:attention", relation="mechanism", confidence="EXTRACTED", weight=1.0)
    G.add_edge("video:v1", "concept:transformer", relation="explains", confidence="EXTRACTED", weight=1.0)

    partition = {
        "concept:transformer": 0,
        "concept:attention": 0,
        "video:v1": 1,
    }

    # Traditional query
    res_trad = query_graph(G, partition, "Transformer 架構")
    assert len(res_trad["results"]) > 0
    labels = [n["label"] for n in res_trad["results"]]
    assert "Transformer" in labels

    # Simplified query
    res_simp = query_graph(G, partition, "什么是 attention")
    assert len(res_simp["results"]) > 0
    labels_simp = [n["label"] for n in res_simp["results"]]
    assert "Self-Attention" in labels_simp


def test_stop_token_filtering_cross_strait() -> None:
    trad = kb.tokenize_query("什麼是 transformer")
    simp = kb.tokenize_query("什么是 transformer")
    assert trad == ["transformer"]
    assert simp == ["transformer"]
    assert kb.is_stop_token("什麼是")
    assert kb.is_stop_token("什么是")
    assert kb.is_stop_token("為什麼")
    assert kb.is_stop_token("为什么")


def test_expand_query_tokens_avoids_overexpansion() -> None:
    from hungyi_chinese import expand_query_tokens

    # Searching for generic word "學習" should not explode into 28 specific ML terms
    expanded_learn = expand_query_tokens(["學習"])
    assert "reinforcement learning" not in expanded_learn
    assert "contrastive learning" not in expanded_learn
    assert "深度學習" not in expanded_learn
    assert "學習" in expanded_learn

    # Searching for generic word "模型" should not expand to diffusion model or LLM
    expanded_model = expand_query_tokens(["模型"])
    assert "diffusion model" not in expanded_model
    assert "大型語言模型" not in expanded_model
    assert "模型" in expanded_model

    # Specific AI term should expand correctly
    expanded_rl = expand_query_tokens(["强化学习"])
    assert "強化學習" in expanded_rl
    assert "增強式學習" in expanded_rl
    assert "reinforcement learning" in expanded_rl


def test_graph_query_filters_stop_words() -> None:
    pytest.importorskip("networkx")
    import networkx as nx
    from hungyi_graph import query_graph

    G = nx.Graph()
    G.add_node("concept:transformer", label="Transformer", type="concept")
    partition = {"concept:transformer": 0}

    res_trad = query_graph(G, partition, "什麼是 transformer")
    assert "什麼是" not in res_trad["tokens"]
    assert "transformer" in res_trad["tokens"]

    res_simp = query_graph(G, partition, "什么是 transformer")
    assert "什么是" not in res_simp["tokens"]
    assert "transformer" in res_simp["tokens"]

