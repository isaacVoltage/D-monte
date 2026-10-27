# Simple Inverted Index Generator for Information Retrieval

A lightweight, beginner-friendly Information Retrieval (IR) application built with Python and Streamlit. This project constructs an inverted index data structure from text documents, tracks posting lists and term frequencies, and retrieves relevant documents using case-insensitive keyword and Boolean (AND, OR) search queries.

---

## 📌 1. Project Introduction

Information Retrieval (IR) is the science of searching for documents, information within documents, and metadata about documents. At the core of commercial web search engines (such as Google and Bing) is the **Inverted Index**—a data structure that maps every unique word in a document collection to the list of document identifiers in which it occurs.

This project implements a fully functional inverted index generator and query processor designed specifically for undergraduate computer science and engineering mini-projects, classroom demonstrations, and lab projects.

---

## 🎯 2. Problem Statement

Scanning through thousands or millions of documents sequentially using linear search (such as Unix `grep`) requires $\mathcal{O}(N \times M)$ time complexity, where $N$ is the number of documents and $M$ is the average document length. For large-scale text databases, this brute-force approach is unacceptably slow.

There is a need for an indexing system that precomputes a word-to-document mapping, enabling sub-second search latency, Boolean filtering, and collection statistics without relying on opaque machine learning libraries or external search engines.

---

## 🚀 3. Objectives

- **Educational Clarity**: Provide an intuitive, transparent implementation of Information Retrieval concepts without external black-box search frameworks.
- **Index Generation**: Parse, tokenize, and normalize text to build an inverted index mapping each vocabulary term to unique document identifiers.
- **Duplicate Prevention**: Ensure words repeated multiple times within the same document do not produce duplicate document IDs in the posting list.
- **Boolean Search**: Support Keyword search as well as Boolean `AND` (set intersection) and Boolean `OR` (set union) query evaluations.
- **Interactive Demonstration**: Deliver a clean, responsive Streamlit web interface with real-time index inspection, sample presets, and how-to-work guides.
- **Automated Verification**: Include comprehensive unit and integration tests using `pytest` to validate algorithmic correctness.

---

## ✨ 4. Key Features

- **Document Management**:
  - Add custom documents with a title and content.
  - Automatically assigns unique, sequential Document IDs (`Doc 1`, `Doc 2`, etc.).
  - One-click presets: *Classroom Preset* (3 standard documents) and *Extended Preset* (6 IR concept documents).
  - Clear/reset functionality to purge the collection and restart indexing.

- **Inverted Index Generation**:
  - Tokenization and case normalization (strips punctuation and whitespace).
  - Avoids duplicate document IDs in posting lists for repeated words within the same document.
  - Tracks document frequency (DF) and term occurrences.
  - Displays the generated inverted index in an interactive, searchable table with CSV export.

- **Query Processing & Retrieval**:
  - **Single Keyword / Phrase Retrieval**: Finds all documents containing the query terms.
  - **Boolean AND Retrieval**: Intersects posting lists ($P(t_1) \cap P(t_2)$) to return documents containing all query terms.
  - **Boolean OR Retrieval**: Unites posting lists ($P(t_1) \cup P(t_2)$) to return documents containing at least one query term.
  - Visual query execution trace and matching term highlight tags.

- **Educational & How to Work Tools**:
  - Built-in How to Work tab explaining the inverted index data structure, posting lists, time complexity, and frequently asked questions with clear answers.
  - **Light / Dark Mode Toggle**: Instant top-left theme switcher with custom high-contrast color palettes for comfortable presentation in any ambient lighting.

---

## 🛠️ 5. Technology Requirements

- **Programming Language**: Python 3.8+ (Tested on Python 3.12.6)
- **Web Interface**: Streamlit (`>=1.30.0`)
- **Data Handling**: Pandas (`>=2.0.0`)
- **Automated Testing**: Pytest (`>=8.0.0`)
- **Standard Libraries**: `re`, `dataclasses`, `typing`, `html`

> **Note**: No databases, machine learning models, deep learning frameworks, paid APIs, or user authentication mechanisms are used. The implementation relies strictly on fundamental data structures (hash maps, sets, lists).

---

## 💻 6. Installation Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd "d:/Simple Inverted Index Generator"
   ```

2. **Verify Python is installed**:
   ```bash
   python --version
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ 7. Running the Application

Launch the Streamlit web dashboard:
```bash
python -m streamlit run app.py
```

Once started, Streamlit will display local and network URLs:
```
Local URL: http://localhost:8501
```
Open your web browser and navigate to `http://localhost:8501`.

---

## 🧪 8. Automated Testing

The project includes an automated test suite covering 17 test scenarios in `test_inverted_index.py`.

Run the automated tests using:
```bash
python -m pytest -v
```

### Verified Test Cases:
1. `test_tokenization_basic`: Tokenization and lowercasing.
2. `test_tokenization_empty`: Safe handling of empty text.
3. `test_prompt_classroom_example`: Exact prompt specification (Doc 1, Doc 2, Doc 3).
4. `test_repeated_words_within_document`: Verification that repeated words don't duplicate doc IDs.
5. `test_words_in_multiple_documents`: Correct mapping across multiple documents.
6. `test_case_insensitive_indexing_and_search`: Uppercase, lowercase, mixed case equivalence.
7. `test_search_results_structure`: Return format (doc_id, title, content, matched_terms).
8. `test_empty_document_handling`: Graceful processing of empty input.
9. `test_empty_query_handling`: Graceful handling of empty queries.
10. `test_nonexistent_word_search`: Searching for out-of-vocabulary terms returns empty list without error.
11. `test_boolean_and_search`: Exact posting list intersection.
12. `test_boolean_or_search`: Exact posting list union.
13. `test_clear_collection`: Complete state purge and re-indexing verification.
14. `test_statistics_accuracy`: Document count, vocabulary size, and posting counts.
15. `test_punctuation_and_hyphens`: Normalization of special characters.
16. `test_get_document_by_id`: Document retrieval by unique ID.
17. `test_index_table_data_format`: Table data generation for UI rendering.

---

## 📝 9. Sample Input and Output

### Input Documents:
- **Doc 1**: "I love Python"
- **Doc 2**: "Python is easy"
- **Doc 3**: "I love Java"

### Generated Inverted Index:
| Term | Posting List (Doc IDs) | Documents | Document Frequency (DF) |
| :--- | :--- | :--- | :--- |
| **easy** | `[2]` | Doc 2 | 1 |
| **i** | `[1, 3]` | Doc 1, Doc 3 | 2 |
| **is** | `[2]` | Doc 2 | 1 |
| **java** | `[3]` | Doc 3 | 1 |
| **love** | `[1, 3]` | Doc 1, Doc 3 | 2 |
| **python** | `[1, 2]` | Doc 1, Doc 2 | 2 |

### Sample Queries & Results:
- **Query**: `python` (Keyword)
  - **Matches**: Doc 1 ("I love Python"), Doc 2 ("Python is easy")
- **Query**: `love python` (Boolean AND)
  - **Intersection**: $P(\text{love}) \cap P(\text{python}) = \{1, 3\} \cap \{1, 2\} = \{1\}$
  - **Matches**: Doc 1 ("I love Python")
- **Query**: `python java` (Boolean OR)
  - **Union**: $P(\text{python}) \cup P(\text{java}) = \{1, 2\} \cup \{3\} = \{1, 2, 3\}$
  - **Matches**: Doc 1, Doc 2, Doc 3

---

## ⚠️ 10. Project Limitations & Future Scope

### Current Limitations:
- Operates in-memory (data persists in the active session, not on disk).
- Tokenization uses standard alphanumeric regex without morphological stemming (e.g. *run*, *running*, *runs* are indexed separately).
- Stop-words (e.g., *is*, *the*, *a*) are retained in the index to preserve simplicity and demonstrate raw frequency behavior.

### Future Scope:
- Integration of Porter Stemmer or Snowball Stemmer for linguistic normalization.
- Stop-word removal toggle in the UI.
- TF-IDF scoring and Cosine Similarity vector space ranking.
- Persistent disk storage using SQLite or serialized binary indices.

---

## 💡 11. How to Work & Frequently Asked Questions (FAQ)

1. **What is an Inverted Index?**
   An inverted index is a dictionary data structure that maps each unique term in a document collection to a list of document IDs (called a posting list) where the term occurs.

2. **Why is it called "inverted"?**
   Traditional storage maps documents to the words they contain (Forward Index). An inverted index flips this relationship, mapping words to the documents that contain them.

3. **How does Boolean search work with posting lists?**
   - **AND**: Intersection of sorted posting lists ($\mathcal{O}(L_1 + L_2)$).
   - **OR**: Union of sorted posting lists ($\mathcal{O}(L_1 + L_2)$).

4. **How do you avoid duplicate document IDs when a word appears multiple times in a document?**
   By checking whether the document ID is already present in the term's posting list, or by gathering unique terms per document before updating the index.
