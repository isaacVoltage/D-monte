"""
Test Suite for Simple Inverted Index Generator
----------------------------------------------
Tests cover:
1. Basic inverted index generation matching user prompt specifications.
2. Words appearing in multiple documents.
3. Repeated words within a document (verifying duplicate doc IDs are avoided).
4. Case-insensitive indexing and searching.
5. Accurate search results retrieval.
6. Empty documents and empty queries handling.
7. Searches for terms not present in the vocabulary.
8. Collection clearing and index reset.
9. Boolean AND and Boolean OR operations.
10. Punctuation and whitespace normalization.
"""

import pytest
from inverted_index import InvertedIndex, Document


@pytest.fixture
def empty_index():
    """Provides a fresh InvertedIndex instance."""
    return InvertedIndex()


@pytest.fixture
def sample_classroom_index():
    """
    Provides an InvertedIndex with the exact example from the project prompt:
    Doc 1: I love Python
    Doc 2: Python is easy
    Doc 3: I love Java
    """
    idx = InvertedIndex()
    # Note: To match content-only test exactly, we can set title as Doc label or empty
    idx.add_document("Doc 1", "I love Python")
    idx.add_document("Doc 2", "Python is easy")
    idx.add_document("Doc 3", "I love Java")
    return idx


def test_tokenization_basic():
    """Test text lowercasing and punctuation stripping."""
    tokens = InvertedIndex.tokenize("Hello, World! This is a test... 123?")
    assert tokens == ["hello", "world", "this", "is", "a", "test", "123"]


def test_tokenization_empty():
    """Test tokenization of empty or whitespace-only strings."""
    assert InvertedIndex.tokenize("") == []
    assert InvertedIndex.tokenize("   \n\t  ") == []
    assert InvertedIndex.tokenize(None) == []


def test_prompt_classroom_example(empty_index):
    """
    Verifies the exact specification in the user prompt:
    Doc 1: I love Python
    Doc 2: Python is easy
    Doc 3: I love Java

    Expected inverted index:
    - python -> Doc 1, Doc 2
    - love -> Doc 1, Doc 3
    - java -> Doc 3
    - easy -> Doc 2
    """
    # Using content only for indexing to match prompt specification exactly
    doc1_id = empty_index.add_document("", "I love Python")
    doc2_id = empty_index.add_document("", "Python is easy")
    doc3_id = empty_index.add_document("", "I love Java")

    assert doc1_id == 1
    assert doc2_id == 2
    assert doc3_id == 3

    index = empty_index.get_index()

    # Check the exact mappings
    assert index["python"] == [1, 2]
    assert index["love"] == [1, 3]
    assert index["java"] == [3]
    assert index["easy"] == [2]
    assert index["i"] == [1, 3]
    assert index["is"] == [2]


def test_repeated_words_within_document(empty_index):
    """
    Verify that repeated words within the same document do NOT create
    duplicate document IDs in the posting list.
    """
    doc_id = empty_index.add_document(
        "Repeated Words", 
        "python python python data python data"
    )
    index = empty_index.get_index()

    assert index["python"] == [doc_id]
    assert index["data"] == [doc_id]
    # Check that term frequency is tracked properly without duplicating postings
    assert empty_index.term_frequencies["python"][doc_id] == 4
    assert empty_index.term_frequencies["data"][doc_id] == 2


def test_words_in_multiple_documents(sample_classroom_index):
    """
    Verify words that appear across multiple documents are correctly mapped.
    """
    index = sample_classroom_index.get_index()
    # 'python' appears in Doc 1 and Doc 2
    assert index["python"] == [1, 2]
    # 'love' appears in Doc 1 and Doc 3
    assert index["love"] == [1, 3]


def test_case_insensitive_indexing_and_search(empty_index):
    """
    Verify that indexing and searching are completely case-insensitive.
    """
    empty_index.add_document("Tech 1", "PYTHON and PYTEST are GREAT")
    empty_index.add_document("Tech 2", "Python is great for scripting")

    # Search in lowercase, uppercase, and mixed case
    results_lower = empty_index.search("python")
    results_upper = empty_index.search("PYTHON")
    results_mixed = empty_index.search("PyThOn")

    assert len(results_lower) == 2
    assert len(results_upper) == 2
    assert len(results_mixed) == 2

    matching_ids = [r["doc_id"] for r in results_lower]
    assert matching_ids == [1, 2]


def test_search_results_structure(sample_classroom_index):
    """
    Verify that search results contain doc_id, title, content, and matched terms.
    """
    results = sample_classroom_index.search("Java")
    assert len(results) == 1
    res = results[0]

    assert res["doc_id"] == 3
    assert res["title"] == "Doc 3"
    assert res["content"] == "I love Java"
    assert "java" in res["matched_terms"]


def test_empty_document_handling(empty_index):
    """
    Verify that empty or whitespace-only documents are handled safely.
    """
    doc_id1 = empty_index.add_document("", "")
    doc_id2 = empty_index.add_document("Empty Title", "   ")

    stats = empty_index.get_statistics()
    assert stats["total_documents"] == 2
    # Only "empty" and "title" from the title should be in vocab
    assert "empty" in empty_index.get_index()
    assert "title" in empty_index.get_index()
    assert len(empty_index.get_index()) == 2


def test_empty_query_handling(sample_classroom_index):
    """
    Verify that empty or whitespace search queries return an empty list gracefully.
    """
    assert sample_classroom_index.search("") == []
    assert sample_classroom_index.search("   ") == []
    assert sample_classroom_index.search_boolean_and("") == []
    assert sample_classroom_index.search_boolean_or("") == []


def test_nonexistent_word_search(sample_classroom_index):
    """
    Verify that searching for terms not in the document collection returns an empty list without error.
    """
    results = sample_classroom_index.search("cplusplus")
    assert results == []

    results_and = sample_classroom_index.search_boolean_and("python AND ruby")
    assert results_and == []


def test_boolean_and_search(sample_classroom_index):
    """
    Verify Boolean AND retrieves only documents containing ALL query terms.
    """
    # Doc 1: I love Python
    # Doc 2: Python is easy
    # Doc 3: I love Java

    # 'love' AND 'python' -> only Doc 1
    results = sample_classroom_index.search_boolean_and("love python")
    assert len(results) == 1
    assert results[0]["doc_id"] == 1

    # 'love' AND 'java' -> only Doc 3
    results = sample_classroom_index.search_boolean_and("love java")
    assert len(results) == 1
    assert results[0]["doc_id"] == 3

    # 'python' AND 'easy' -> only Doc 2
    results = sample_classroom_index.search_boolean_and("python easy")
    assert len(results) == 1
    assert results[0]["doc_id"] == 2

    # 'python' AND 'java' -> no document has both
    results = sample_classroom_index.search_boolean_and("python java")
    assert len(results) == 0


def test_boolean_or_search(sample_classroom_index):
    """
    Verify Boolean OR retrieves documents containing ANY of the query terms.
    """
    # 'python' OR 'java' -> Doc 1, Doc 2, Doc 3
    results = sample_classroom_index.search_boolean_or("python java")
    doc_ids = sorted([r["doc_id"] for r in results])
    assert doc_ids == [1, 2, 3]

    # 'easy' OR 'java' -> Doc 2, Doc 3
    results = sample_classroom_index.search_boolean_or("easy java")
    doc_ids = sorted([r["doc_id"] for r in results])
    assert doc_ids == [2, 3]


def test_clear_collection(sample_classroom_index):
    """
    Verify clearing the collection resets documents, index, and statistics.
    """
    stats_before = sample_classroom_index.get_statistics()
    assert stats_before["total_documents"] == 3
    assert stats_before["total_vocabulary"] > 0

    sample_classroom_index.clear()

    stats_after = sample_classroom_index.get_statistics()
    assert stats_after["total_documents"] == 0
    assert stats_after["total_vocabulary"] == 0
    assert stats_after["total_postings"] == 0
    assert sample_classroom_index.get_index() == {}
    assert sample_classroom_index.get_all_documents() == []

    # Can add new documents after reset and IDs start from 1
    new_id = sample_classroom_index.add_document("Fresh Doc", "Fresh start")
    assert new_id == 1
    assert sample_classroom_index.get_statistics()["total_documents"] == 1


def test_statistics_accuracy(empty_index):
    """
    Verify that document and vocabulary statistics calculate accurately.
    """
    empty_index.add_document("Doc 1", "apple banana")
    empty_index.add_document("Doc 2", "banana cherry cherry")

    stats = empty_index.get_statistics()
    assert stats["total_documents"] == 2
    # Vocabulary: 'doc', '1', '2', 'apple', 'banana', 'cherry'
    assert stats["total_vocabulary"] == 6
    # Postings:
    # doc -> [1, 2] (len 2)
    # 1 -> [1] (len 1)
    # 2 -> [2] (len 1)
    # apple -> [1] (len 1)
    # banana -> [1, 2] (len 2)
    # cherry -> [2] (len 1)
    # Total postings = 2 + 1 + 1 + 1 + 2 + 1 = 8
    assert stats["total_postings"] == 8


def test_punctuation_and_hyphens(empty_index):
    """
    Verify that punctuation, quotes, and hyphens are stripped correctly.
    """
    empty_index.add_document("Symbols Test", "Data-Mining: 'Information' (Retrieval) & Search!")
    index = empty_index.get_index()

    assert "data" in index
    assert "mining" in index
    assert "information" in index
    assert "retrieval" in index
    assert "search" in index


def test_get_document_by_id(sample_classroom_index):
    """
    Verify retrieving a specific document by its ID.
    """
    doc2 = sample_classroom_index.get_document(2)
    assert doc2 is not None
    assert doc2.content == "Python is easy"

    doc_missing = sample_classroom_index.get_document(999)
    assert doc_missing is None


def test_index_table_data_format(sample_classroom_index):
    """
    Verify the table formatting helper function generates valid rows.
    """
    table_rows = sample_classroom_index.get_index_table_data()
    assert len(table_rows) > 0
    # Every row should have the expected keys
    for row in table_rows:
        assert "Term" in row
        assert "Posting List (Doc IDs)" in row
        assert "Document Labels" in row
        assert "Document Frequency (DF)" in row
