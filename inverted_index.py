"""
Inverted Index Generator for Information Retrieval
--------------------------------------------------
This module provides the core data structures and algorithms for:
1. Text tokenization and normalization (lowercasing, punctuation stripping).
2. Building an inverted index mapping vocabulary terms to document IDs.
3. Preventing duplicate document IDs in posting lists.
4. Boolean retrieval (AND, OR) and single-keyword searching.
5. Index management (adding documents, clearing, stats generation).

Designed for simplicity, modularity, and academic clarity.
"""

import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Document:
    """Represents an indexed text document."""
    doc_id: int
    title: str
    content: str

    def to_dict(self) -> Dict[str, any]:
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "content": self.content
        }


class InvertedIndex:
    """
    Inverted Index Engine for Information Retrieval.
    
    Data Structure:
        - documents: Dict[int, Document]
            Maps doc_id to Document instance.
        - index: Dict[str, List[int]]
            Maps a normalized term (word) to a sorted list of unique doc_ids.
        - term_frequencies: Dict[str, Dict[int, int]]
            Optional frequency tracker: term -> {doc_id: count}
    """

    def __init__(self):
        self.documents: Dict[int, Document] = {}
        self.index: Dict[str, List[int]] = {}
        self.term_frequencies: Dict[str, Dict[int, int]] = {}
        self._next_doc_id: int = 1

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Converts text into normalized lowercase word tokens.
        Strips punctuation and whitespace.
        
        Example:
            "I love Python! Python is easy." -> ['i', 'love', 'python', 'python', 'is', 'easy']
        """
        if not text:
            return []
        # Convert to lowercase
        lowered = text.lower()
        # Find all alphanumeric sequences (words/numbers), ignoring punctuation
        tokens = re.findall(r"\b[a-zA-Z0-9_]+\b", lowered)
        return tokens

    def add_document(self, title: str, content: str) -> int:
        """
        Adds a new document to the collection and updates the inverted index.
        
        Args:
            title: The title or headline of the document.
            content: The text content of the document.
            
        Returns:
            The assigned unique integer document ID.
        """
        doc_id = self._next_doc_id
        self._next_doc_id += 1

        cleaned_title = title.strip() if title and title.strip() else f"Document {doc_id}"
        cleaned_content = content.strip() if content else ""

        doc = Document(doc_id=doc_id, title=cleaned_title, content=cleaned_content)
        self.documents[doc_id] = doc

        # Index user-provided title and content
        texts_to_index = []
        if title and title.strip():
            texts_to_index.append(title.strip())
        if cleaned_content:
            texts_to_index.append(cleaned_content)
        full_text = " ".join(texts_to_index)
        tokens = self.tokenize(full_text)

        # Count frequencies in this document
        doc_term_counts: Dict[str, int] = {}
        for token in tokens:
            doc_term_counts[token] = doc_term_counts.get(token, 0) + 1

        # Update index with unique doc_id per term
        for term, count in doc_term_counts.items():
            if term not in self.index:
                self.index[term] = []
                self.term_frequencies[term] = {}

            # Prevent duplicate document IDs
            if doc_id not in self.index[term]:
                self.index[term].append(doc_id)
                self.index[term].sort()

            self.term_frequencies[term][doc_id] = count

        return doc_id

    def load_sample_documents(self, preset: str = "classroom") -> List[int]:
        """
        Loads standard sample documents into the collection.
        
        Preset "classroom":
            Doc 1: I love Python
            Doc 2: Python is easy
            Doc 3: I love Java
            
        Preset "extended":
            Adds additional documents covering Information Retrieval, search engines, and computer science.
        """
        added_ids = []
        if preset == "classroom":
            samples = [
                ("Python Basics", "I love Python"),
                ("Python Ease", "Python is easy"),
                ("Java Basics", "I love Java")
            ]
        else:
            samples = [
                ("Python Basics", "I love Python programming language"),
                ("Python Ease", "Python is easy to learn and write"),
                ("Java Basics", "I love Java and object oriented programming"),
                ("Information Retrieval", "Information retrieval systems find relevant documents from text databases"),
                ("Search Engines", "Search engines build inverted indexes to retrieve fast search results"),
                ("Inverted Index Structure", "An inverted index maps words to document identifiers efficiently")
            ]

        for title, content in samples:
            doc_id = self.add_document(title, content)
            added_ids.append(doc_id)

        return added_ids

    def search_keyword(self, query: str) -> List[Dict[str, any]]:
        """
        Searches for a single keyword or phrase (case-insensitive).
        If multiple words are entered without boolean operators, performs a standard union (OR).
        """
        tokens = self.tokenize(query)
        if not tokens:
            return []

        # Find matching document IDs across all query tokens
        matched_doc_ids: Set[int] = set()
        for token in tokens:
            if token in self.index:
                matched_doc_ids.update(self.index[token])

        return self._build_search_results(sorted(list(matched_doc_ids)), tokens)

    def search_boolean_and(self, query: str) -> List[Dict[str, any]]:
        """
        Boolean AND Search:
        Retrieves documents that contain ALL specified query terms.
        Intersection of posting lists: doc_ids(term1) ∩ doc_ids(term2) ∩ ...
        """
        tokens = self.tokenize(query)
        if not tokens:
            return []

        # Check if first token exists
        if tokens[0] not in self.index:
            return []

        # Initialize with postings of the first token
        matching_set = set(self.index[tokens[0]])

        # Intersect with postings of subsequent tokens
        for token in tokens[1:]:
            if token in self.index:
                matching_set.intersection_update(self.index[token])
            else:
                # If any term is not in vocabulary, intersection is empty
                return []

        return self._build_search_results(sorted(list(matching_set)), tokens)

    def search_boolean_or(self, query: str) -> List[Dict[str, any]]:
        """
        Boolean OR Search:
        Retrieves documents that contain AT LEAST ONE specified query term.
        Union of posting lists: doc_ids(term1) ∪ doc_ids(term2) ∪ ...
        """
        tokens = self.tokenize(query)
        if not tokens:
            return []

        matching_set: Set[int] = set()
        for token in tokens:
            if token in self.index:
                matching_set.update(self.index[token])

        return self._build_search_results(sorted(list(matching_set)), tokens)

    def search(self, query: str, mode: str = "KEYWORD") -> List[Dict[str, any]]:
        """
        Unified search interface supporting KEYWORD, AND, and OR modes.
        """
        mode = mode.upper()
        if mode == "AND":
            return self.search_boolean_and(query)
        elif mode == "OR":
            return self.search_boolean_or(query)
        else:
            return self.search_keyword(query)

    def _build_search_results(self, doc_ids: List[int], query_tokens: List[str]) -> List[Dict[str, any]]:
        """
        Constructs detailed search result objects with document details,
        matched query terms, and term frequencies.
        """
        results = []
        for doc_id in doc_ids:
            doc = self.documents.get(doc_id)
            if not doc:
                continue

            # Identify which query tokens actually appeared in this document
            matched_terms = []
            score = 0
            for token in query_tokens:
                if token in self.term_frequencies and doc_id in self.term_frequencies[token]:
                    matched_terms.append(token)
                    score += self.term_frequencies[token][doc_id]

            results.append({
                "doc_id": doc.doc_id,
                "doc_label": f"Doc {doc.doc_id}",
                "title": doc.title,
                "content": doc.content,
                "matched_terms": sorted(list(set(matched_terms))),
                "frequency_count": score
            })

        # Rank slightly by match frequency for helpful ordering
        results.sort(key=lambda r: (len(r["matched_terms"]), r["frequency_count"]), reverse=True)
        return results

    def get_index(self) -> Dict[str, List[int]]:
        """
        Returns the inverted index dictionary sorted alphabetically by term.
        Format: { "word": [1, 2], ... }
        """
        return {term: sorted(self.index[term]) for term in sorted(self.index.keys())}

    def get_index_table_data(self) -> List[Dict[str, any]]:
        """
        Returns structured rows for displaying the inverted index in a table.
        Columns: Term, Document IDs, Document Labels, Document Count (Postings Length).
        """
        table = []
        for term in sorted(self.index.keys()):
            doc_ids = sorted(self.index[term])
            labels = [f"Doc {d}" for d in doc_ids]
            table.append({
                "Term": term,
                "Posting List (Doc IDs)": ", ".join(map(str, doc_ids)),
                "Document Labels": ", ".join(labels),
                "Document Frequency (DF)": len(doc_ids)
            })
        return table

    def get_all_documents(self) -> List[Document]:
        """Returns all documents in order of doc_id."""
        return [self.documents[doc_id] for doc_id in sorted(self.documents.keys())]

    def get_document(self, doc_id: int) -> Optional[Document]:
        """Retrieves a single document by its ID."""
        return self.documents.get(doc_id)

    def get_statistics(self) -> Dict[str, int]:
        """
        Returns collection statistics:
        - total_documents: Number of indexed documents.
        - total_vocabulary: Number of unique indexed words.
        - total_postings: Total number of (term, doc) pairs.
        - total_word_occurrences: Total words counted across all documents.
        """
        total_docs = len(self.documents)
        total_vocab = len(self.index)
        total_postings = sum(len(postings) for postings in self.index.values())
        total_occurrences = sum(
            sum(counts.values()) for counts in self.term_frequencies.values()
        )

        return {
            "total_documents": total_docs,
            "total_vocabulary": total_vocab,
            "total_postings": total_postings,
            "total_word_occurrences": total_occurrences
        }

    def clear(self):
        """Clears all documents and resets the inverted index."""
        self.documents.clear()
        self.index.clear()
        self.term_frequencies.clear()
        self._next_doc_id = 1
