""" This module contains tests for the search_vector_index_service module. """

from unittest.mock import Mock
from typing import List, Tuple
import types
from langchain_core.documents import Document
from langchain_community.vectorstores.azuresearch import AzureSearch
import pytest
from libs.core.services.search_vector_index_service import search

@pytest.fixture(name="setup")
def setup_fixture():
    """ Setup for the tests."""

    obj = types.SimpleNamespace()
    obj.query = "test query"
    obj.number_of_results = 5
    obj.client = Mock(spec=AzureSearch)
    obj.client.semantic_hybrid_search_with_score_and_rerank.return_value = [
        (Mock(spec=Document), 0.5, 0.5) for _ in range(obj.number_of_results)
    ]
    return obj

def test_search(setup):
    """ Test the search function."""

    result = search(setup.client, setup.query, setup.number_of_results)

    assert isinstance(result, List)
    for item in result:
        assert isinstance(item, Tuple)
        assert len(item) == 3
        assert isinstance(item[0], Document)
        assert isinstance(item[1], float)
        assert isinstance(item[2], float)
