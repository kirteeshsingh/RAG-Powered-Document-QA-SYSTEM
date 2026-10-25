"""Unit tests for the Chatbot class.

The Cohere client is mocked, so the tests run offline without API keys.
"""

import os
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from chatbot import Chatbot


def make_chatbot(mock_client):
    with patch("chatbot.cohere.Client", return_value=mock_client):
        vectorstore = MagicMock()
        bot = Chatbot(vectorstore, "fake-key")
    return bot, vectorstore


class TestRespond:
    def test_uses_retrieval_when_search_queries_are_returned(self):
        mock_client = MagicMock()
        mock_client.chat.return_value = SimpleNamespace(
            search_queries=[SimpleNamespace(text="refund policy")]
        )
        mock_client.chat_stream.return_value = iter([])

        bot, vectorstore = make_chatbot(mock_client)
        vectorstore.retrieve.return_value = [{"text": "retrieved chunk"}]

        _, retrieved_docs = bot.respond("What is the refund policy?")

        vectorstore.retrieve.assert_called_once_with("refund policy")
        assert retrieved_docs == [{"text": "retrieved chunk"}]
        stream_kwargs = mock_client.chat_stream.call_args.kwargs
        assert stream_kwargs["documents"] == [{"text": "retrieved chunk"}]

    def test_skips_retrieval_when_no_search_queries(self):
        mock_client = MagicMock()
        mock_client.chat.return_value = SimpleNamespace(search_queries=[])
        mock_client.chat_stream.return_value = iter([])

        bot, vectorstore = make_chatbot(mock_client)

        _, retrieved_docs = bot.respond("Hello!")

        vectorstore.retrieve.assert_not_called()
        assert retrieved_docs == []
        stream_kwargs = mock_client.chat_stream.call_args.kwargs
        assert "documents" not in stream_kwargs

    def test_conversation_id_is_stable_across_turns(self):
        mock_client = MagicMock()
        mock_client.chat.return_value = SimpleNamespace(search_queries=[])
        mock_client.chat_stream.return_value = iter([])

        bot, _ = make_chatbot(mock_client)
        bot.respond("first")
        first_id = mock_client.chat_stream.call_args.kwargs["conversation_id"]
        bot.respond("second")
        second_id = mock_client.chat_stream.call_args.kwargs["conversation_id"]

        assert first_id == second_id == bot.conversation_id
