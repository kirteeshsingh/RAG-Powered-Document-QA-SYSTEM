"""Unit tests for the VectorStore class.

All Cohere and Pinecone calls are mocked, so the tests run offline
without API keys.
"""

import os
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import fitz
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vectorstore import VectorStore


def make_store() -> VectorStore:
    """Create a VectorStore instance without running __init__."""
    store = VectorStore.__new__(VectorStore)
    store.chunks = []
    store.embeddings = []
    store.retrieve_top_k = 10
    store.rerank_top_k = 3
    return store


class TestExtractTextFromPdf:
    def test_extracts_text_from_generated_pdf(self, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Retrieval Augmented Generation groundwork.")
        doc.save(pdf_path)
        doc.close()

        store = make_store()
        text = store.extract_text_from_pdf(str(pdf_path))

        assert "Retrieval Augmented Generation" in text


class TestSplitText:
    def test_short_text_becomes_single_chunk(self):
        store = make_store()
        store.pdf_text = "One sentence. Another sentence."
        store.split_text(chunk_size=1000)

        assert len(store.chunks) == 1
        assert "One sentence" in store.chunks[0]

    def test_long_text_is_split_into_multiple_chunks(self):
        store = make_store()
        store.pdf_text = ". ".join(f"Sentence number {i}" for i in range(200))
        store.split_text(chunk_size=200)

        assert len(store.chunks) > 1
        for chunk in store.chunks:
            # Each chunk stays near the configured size plus one sentence.
            assert len(chunk) < 200 + 60

    def test_no_content_is_lost_when_splitting(self):
        store = make_store()
        sentences = [f"Fact {i} about the document" for i in range(50)]
        store.pdf_text = ". ".join(sentences)
        store.split_text(chunk_size=150)

        joined = " ".join(store.chunks)
        for sentence in sentences:
            assert sentence in joined


class TestEmbedChunks:
    def test_embeddings_are_collected_in_batches(self):
        store = make_store()
        store.chunks = [f"chunk {i}" for i in range(200)]
        store.co = MagicMock()
        store.co.embed.side_effect = lambda texts, **kwargs: SimpleNamespace(
            embeddings=[[0.1, 0.2]] * len(texts)
        )

        store.embed_chunks(batch_size=90)

        assert len(store.embeddings) == 200
        # 200 chunks with batch size 90 -> 3 API calls (90 + 90 + 20).
        assert store.co.embed.call_count == 3

    def test_embed_uses_search_document_input_type(self):
        store = make_store()
        store.chunks = ["only chunk"]
        store.co = MagicMock()
        store.co.embed.return_value = SimpleNamespace(embeddings=[[0.5]])

        store.embed_chunks()

        kwargs = store.co.embed.call_args.kwargs
        assert kwargs["input_type"] == "search_document"


class TestRetrieve:
    def test_retrieve_returns_reranked_metadata(self):
        store = make_store()
        store.co = MagicMock()
        store.co.embed.return_value = SimpleNamespace(embeddings=[[0.1, 0.2]])

        matches = [
            {"metadata": {"text": "doc A"}},
            {"metadata": {"text": "doc B"}},
            {"metadata": {"text": "doc C"}},
        ]
        store.index = MagicMock()
        store.index.query.return_value = {"matches": matches}

        # Rerank returns documents in a new order: C first, then A.
        store.co.rerank.return_value = SimpleNamespace(
            results=[SimpleNamespace(index=2), SimpleNamespace(index=0)]
        )

        result = store.retrieve("what is in the document?")

        assert result == [{"text": "doc C"}, {"text": "doc A"}]
        store.index.query.assert_called_once()
        query_kwargs = store.index.query.call_args.kwargs
        assert query_kwargs["top_k"] == store.retrieve_top_k
        assert query_kwargs["include_metadata"] is True

    def test_retrieve_embeds_query_with_search_query_input_type(self):
        store = make_store()
        store.co = MagicMock()
        store.co.embed.return_value = SimpleNamespace(embeddings=[[0.3]])
        store.index = MagicMock()
        store.index.query.return_value = {"matches": []}
        store.co.rerank.return_value = SimpleNamespace(results=[])

        store.retrieve("query text")

        kwargs = store.co.embed.call_args.kwargs
        assert kwargs["input_type"] == "search_query"
