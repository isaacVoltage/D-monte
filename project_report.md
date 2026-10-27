# Academic Mini-Project Report

---

# DESIGN AND IMPLEMENTATION OF A SIMPLE INVERTED INDEX GENERATOR FOR INFORMATION RETRIEVAL

**A Mini-Project Report submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology / Bachelor of Engineering in Computer Science and Engineering / Information Technology**

---

### Student Details
- **Student Name:** `[Insert Student Name]`
- **Roll Number / PRN:** `[Insert Roll Number]`
- **Class / Division / Semester:** `[Insert Class / Semester]`
- **Academic Year:** `2025 – 2026`
- **Department:** Department of Computer Science and Engineering
- **Institution / College:** `[Insert College Name & Location]`
- **Under the Guidance of:** `[Insert Faculty Guide Name]`

---

## 2. Abstract

Information Retrieval (IR) systems enable users to discover relevant text documents from large collections in response to keyword queries. The cornerstone of modern search technology is the **Inverted Index**, a specialized data structure that inverts the traditional document-to-word representation into a word-to-documents dictionary. 

This project presents the design, mathematical formulation, implementation, and empirical verification of a lightweight Inverted Index Generator developed in Python and Streamlit. The application automates document ingestion, text normalization (case folding and punctuation stripping), unique posting list generation with duplicate suppression, and Boolean query evaluation (Keyword, Boolean AND, Boolean OR). 

A modular architecture cleanly decouples the core algorithmic logic from the user presentation layer. The system was verified through an automated test suite comprising 17 distinct unit and integration tests using `pytest`, alongside browser-based interactive evaluation. The resulting system serves as a transparent educational tool for students and educators to study the internal mechanics of search engines without the complexity of opaque commercial frameworks.

---

## 3. Introduction to Information Retrieval

Information Retrieval is an interdisciplinary branch of computer science focused on the representation, storage, organization of, and access to information items. Unlike database systems that execute exact relational queries (e.g., SQL queries seeking structured records with strict boolean constraints), an Information Retrieval system handles unstructured natural language text.

In an IR system, the user expresses their information need through an unstructured search query composed of one or more terms. The core challenge of an IR engine is twofold:
1. **Efficiency:** Quickly identifying which documents out of a vast collection contain the query words without scanning every document from beginning to end.
2. **Effectiveness:** Returning documents that satisfy the user's specific informational requirements.

Search engines address the efficiency challenge by computing an **Inverted Index** during an offline or background indexing phase. When a search query is submitted, the engine queries the index rather than the raw text, reducing search time by orders of magnitude.

---

## 4. Problem Statement

Given a collection of $N$ text documents $\mathcal{D} = \{d_1, d_2, \dots, d_N\}$:
- Performing a sequential scan (**linear search / grep**) across all documents to identify matches for a query word requires $\mathcal{O}(N \times M)$ comparisons, where $M$ is the average length of a document.
- As the number of documents grows, linear scanning becomes computationally prohibitive.
- Furthermore, evaluating Boolean queries (such as finding documents containing term $A$ **AND** term $B$) through brute-force text matching requires repeated multi-pass scans.

Therefore, the objective is to design, implement, and validate an in-memory Inverted Index Generator that:
1. Converts arbitrary document collections into an indexed vocabulary $\mathcal{V}$ where each term $t \in \mathcal{V}$ points to an ordered list of unique document IDs (the *posting list*).
2. Prevents redundant document identifiers from appearing in posting lists when words are repeated within a document.
3. Provides sub-second query retrieval supporting single keywords, Boolean AND (intersection), and Boolean OR (union).
4. Delivers an interactive interface for educational exploration and laboratory demonstration.

---

## 5. Objectives

1. **Algorithm Implementation:** Implement pure Python algorithms for tokenization, normalization, inverted index construction, and posting list maintenance.
2. **Duplicate Prevention:** Guarantee that a word occurring multiple times in a single document is added to that document's posting list exactly once, while properly tracking within-document term frequencies.
3. **Boolean Operations:** Provide exact set-theoretic retrieval:
   - Conjunction (AND): $\text{Postings}(t_1) \cap \text{Postings}(t_2)$
   - Disjunction (OR): $\text{Postings}(t_1) \cup \text{Postings}(t_2)$
4. **Interactive Dashboard:** Build a modern web interface using Streamlit featuring real-time index updates, document management, vocabulary inspection, and metrics.
5. **Academic Rigor & Testing:** Ensure 100% test coverage for edge cases, including empty documents, nonexistent query terms, case-insensitivity, and index resetting.

---

## 6. Scope of the Project

### In-Scope:
- Ingestion of user-defined documents and standard preset classroom text datasets.
- Text normalization: Lowercase conversion, whitespace stripping, and punctuation elimination.
- Construction and maintenance of inverted indices with document frequencies and posting lists.
- Exact-match keyword retrieval, Boolean AND retrieval, and Boolean OR retrieval.
- Automated testing through `pytest`.
- In-browser interactive demonstration via Streamlit.

### Out-of-Scope (Design Constraints):
- External databases, SQL servers, or persistent disk storage engines.
- Neural networks, deep learning models, embeddings, or transformer architectures.
- External web APIs or paid third-party services.
- User authentication and multi-tenant access control.
- High-level ranking algorithms (BM25 / PageRank) that obscure fundamental IR concepts for beginner students.

---

## 7. Existing Approach and Proposed System

| Parameter | Existing Approach (Linear Scan / Grep) | Proposed System (Inverted Index) |
| :--- | :--- | :--- |
| **Search Paradigm** | Sequential text search across every document file | Direct dictionary lookup into precomputed posting lists |
| **Search Time Complexity** | $\mathcal{O}(N \times M)$ | $\mathcal{O}(1)$ lookup + $\mathcal{O}(L_1 + L_2)$ list merge |
| **Scalability** | Degrades linearly with document collection size | Sub-second retrieval even with extensive vocabularies |
| **Boolean Query Support** | Multi-pass string matching with nested conditionals | Fast set operations (intersection $\cap$ and union $\cup$) |
| **Preprocessing Overhead** | Zero preprocessing; high query latency | Small one-time indexing cost; near-instantaneous queries |
| **Memory Footprint** | Low memory at rest | Stores vocabulary dictionary and posting lists in RAM |

---

## 8. System Requirements

### Hardware Requirements:
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher (or equivalent virtual CPU).
- **RAM:** Minimum 2 GB (4 GB recommended).
- **Disk Space:** 100 MB free storage for Python runtime and application code.
- **Display:** Standard monitor with resolution $1280 \times 720$ or higher.

### Software Requirements:
- **Operating System:** Microsoft Windows 10/11, macOS, or Linux.
- **Runtime Environment:** Python 3.8 to Python 3.12 (Verified on Python 3.12.6).
- **Web Framework:** Streamlit 1.30.0+ (Verified on 1.57.0).
- **Data Representation:** Pandas 2.0.0+ (Verified on 3.0.1).
- **Test Framework:** Pytest 8.0.0+ (Verified on 9.1.1).
- **Browser:** Any modern Chromium-based browser (Google Chrome, Microsoft Edge) or Mozilla Firefox.

---

## 9. System Architecture and Workflow

```
+-------------------------------------------------------------------------+
|                              USER INTERACTION                           |
|       (Add Document, Load Presets, Input Query, Select Boolean Mode)    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                           STREAMLIT WEB LAYER                           |
|      (app.py - State Management, Session Cache, Interactive UI Tabs)    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                        INVERTED INDEX CORE ENGINE                       |
|                             (inverted_index.py)                         |
|                                                                         |
|  +--------------------+   +---------------------+   +----------------+  |
|  |   1. Tokenizer     |-->| 2. Index Builder    |-->| 3. Query Engine|  |
|  | - Lowercase folding|   | - Unique Doc ID set |   | - Keyword      |  |
|  | - Regex word match |   | - Postings list map |   | - Boolean AND  |  |
|  | - Strip punctuation|   | - Term frequency TF |   | - Boolean OR   |  |
|  +--------------------+   +---------------------+   +----------------+  |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                           DATA STRUCTURES                               |
|   - Documents Dictionary: {doc_id: Document(id, title, content)}        |
|   - Inverted Index:       {term: [sorted doc_ids]}                      |
|   - Term Frequencies:     {term: {doc_id: count}}                       |
+-------------------------------------------------------------------------+
```

### Detailed Workflow:
1. **Document Ingestion:** The user supplies a document title and text body. An incrementing integer ID ($1, 2, 3, \dots$) is assigned.
2. **Text Normalization & Tokenization:** The text is converted to lowercase. A regular expression `\b[a-zA-Z0-9_]+\b` extracts word tokens while discarding punctuation.
3. **Index Construction:** For each unique token in the document, the document ID is appended to that token's posting list if not already present.
4. **Query Evaluation:** When a query is entered, the engine tokenizes the query string.
   - For **Boolean AND**: The posting lists of all query tokens are intersected: $R = P(t_1) \cap P(t_2) \cap \dots$
   - For **Boolean OR**: The posting lists of all query tokens are united: $R = P(t_1) \cup P(t_2) \cup \dots$
5. **Presentation:** Matching documents are formatted with their ID, title, full text, and highlighted keyword badges.

---

## 10. Explanation of the Inverted Index Algorithm

### Data Representation:
Let the vocabulary be $\mathcal{V} = \{t_1, t_2, \dots, t_V\}$.
For each term $t \in \mathcal{V}$, its entry in the inverted index is:
$$\text{Index}[t] = \langle \text{doc\_id}_1, \text{doc\_id}_2, \dots, \text{doc\_id}_k \rangle$$
where $\text{doc\_id}_1 < \text{doc\_id}_2 < \dots < \text{doc\_id}_k$ and each $\text{doc\_id}_i \in \{1, \dots, N\}$.

### Algorithm 1: Document Indexing with Duplicate Suppression
```python
def add_document(doc_id, text):
    tokens = tokenize(text)
    doc_term_counts = {}
    for token in tokens:
        doc_term_counts[token] = doc_term_counts.get(token, 0) + 1
    
    for term, count in doc_term_counts.items():
        if term not in index:
            index[term] = []
        if doc_id not in index[term]:
            index[term].append(doc_id)
            index[term].sort()
        term_frequencies[term][doc_id] = count
```

### Algorithm 2: Boolean Conjunction (AND) Retrieval
```python
def boolean_and_search(query_tokens):
    if not query_tokens:
        return []
    if query_tokens[0] not in index:
        return []
    
    result_set = set(index[query_tokens[0]])
    for token in query_tokens[1:]:
        if token in index:
            result_set = result_set.intersection(index[token])
        else:
            return []  # Any missing term results in an empty intersection
    return sorted(list(result_set))
```

### Algorithm 3: Boolean Disjunction (OR) Retrieval
```python
def boolean_or_search(query_tokens):
    result_set = set()
    for token in query_tokens:
        if token in index:
            result_set = result_set.union(index[token])
    return sorted(list(result_set))
```

---

## 11. Implementation Methodology

The implementation follows a modular, three-tier separation of concerns:

1. **`inverted_index.py` (Core Model):**
   - Implements the `Document` dataclass and `InvertedIndex` engine.
   - Contains zero GUI or Streamlit code, ensuring pure computational independence and testability.
   - All text manipulation utilizes Python standard library modules (`re`, `dataclasses`, `typing`).

2. **`app.py` (Streamlit Presentation Layer):**
   - Provides a multi-tab interface (`Search Engine`, `Document Collection`, `Inverted Index Table`, `How to Work`).
   - Uses `st.session_state` to retain the active `InvertedIndex` instance across user interactions.
   - Embeds custom CSS styles for card styling, status badges, and term highlight spans.

3. **`test_inverted_index.py` (Verification Suite):**
   - Implements pytest test cases evaluating every functional requirement, edge case, and boundary condition.

---

## 12. Sample Input and Output

### Input Document Collection:
- **Document 1 (ID: 1):** Title: `"Python Basics"`, Content: `"I love Python"`
- **Document 2 (ID: 2):** Title: `"Python Ease"`, Content: `"Python is easy"`
- **Document 3 (ID: 3):** Title: `"Java Basics"`, Content: `"I love Java"`

### Generated Inverted Index Dictionary:
```json
{
  "basics": [1, 3],
  "ease": [2],
  "easy": [2],
  "i": [1, 3],
  "is": [2],
  "java": [3],
  "love": [1, 3],
  "python": [1, 2]
}
```

### Query Execution Scenarios:

#### Scenario A: Single Keyword Search (`"python"`)
- **Query Tokens:** `['python']`
- **Posting List:** `[1, 2]`
- **Retrieved Documents:**
  - Doc 1: "I love Python" (Title: Python Basics)
  - Doc 2: "Python is easy" (Title: Python Ease)

#### Scenario B: Boolean AND Search (`"love python"`)
- **Query Tokens:** `['love', 'python']`
- **Posting Lists:** $\text{Postings}(\text{love}) = [1, 3]$, $\text{Postings}(\text{python}) = [1, 2]$
- **Set Intersection:** $[1, 3] \cap [1, 2] = [1]$
- **Retrieved Document:**
  - Doc 1: "I love Python"

#### Scenario C: Boolean OR Search (`"python java"`)
- **Query Tokens:** `['python', 'java']`
- **Posting Lists:** $\text{Postings}(\text{python}) = [1, 2]$, $\text{Postings}(\text{java}) = [3]$
- **Set Union:** $[1, 2] \cup [3] = [1, 2, 3]$
- **Retrieved Documents:**
  - Doc 1, Doc 2, Doc 3

#### Scenario D: Out-of-Vocabulary Search (`"cplusplus"`)
- **Query Tokens:** `['cplusplus']`
- **Posting List:** Not in vocabulary
- **Retrieved Documents:** None (Helpful notification rendered in UI)

---

## 13. Testing and Results

Testing was conducted using `pytest` version 9.1.1 on Python 3.12.6. All 17 automated tests executed and passed cleanly.

### Automated Test Execution Log:
```
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Simple Inverted Index Generator
collected 17 items

test_inverted_index.py::test_tokenization_basic PASSED                   [  5%]
test_inverted_index.py::test_tokenization_empty PASSED                   [ 11%]
test_inverted_index.py::test_prompt_classroom_example PASSED             [ 17%]
test_inverted_index.py::test_repeated_words_within_document PASSED       [ 23%]
test_inverted_index.py::test_words_in_multiple_documents PASSED          [ 29%]
test_inverted_index.py::test_case_insensitive_indexing_and_search PASSED [ 35%]
test_inverted_index.py::test_search_results_structure PASSED             [ 41%]
test_inverted_index.py::test_empty_document_handling PASSED              [ 47%]
test_inverted_index.py::test_empty_query_handling PASSED                 [ 52%]
test_inverted_index.py::test_nonexistent_word_search PASSED              [ 58%]
test_inverted_index.py::test_boolean_and_search PASSED                   [ 64%]
test_inverted_index.py::test_boolean_or_search PASSED                    [ 70%]
test_inverted_index.py::test_clear_collection PASSED                     [ 76%]
test_inverted_index.py::test_statistics_accuracy PASSED                  [ 82%]
test_inverted_index.py::test_punctuation_and_hyphens PASSED              [ 88%]
test_inverted_index.py::test_get_document_by_id PASSED                   [ 94%]
test_inverted_index.py::test_index_table_data_format PASSED              [100%]

============================= 17 passed in 0.05s ==============================
```

### Browser Verification Summary:
The running application on `http://localhost:8501` was verified using an autonomous browser subagent:
- Verified page title and aesthetic header rendering.
- Conducted live search for keyword `"python"`, yielding Doc 1 and Doc 2 with matching badges.
- Conducted live search for `"love python"` under Boolean AND mode, yielding strictly Doc 1.
- Inspected the Inverted Index Table tab, confirming accurate tabular mapping of terms, posting lists, and document frequencies.
- Inspected the How to Work tab, confirming pipeline display and FAQ expanders.

---

## 14. Advantages and Limitations

### Advantages:
1. **Sub-second Retrieval:** Posting list lookups avoid sequential scanning entirely.
2. **Deterministic & Transparent:** Zero opaque ML weights; every retrieved document can be traced directly to posting list set operations.
3. **No Heavy Dependencies:** Implemented using pure Python data structures and minimal standard libraries.
4. **Duplicate Immunity:** Automatically deduplicates document occurrences while tracking frequency counts.
5. **Educational UI:** Real-time metrics, live index tables, and built-in how-to-work guides.

### Limitations:
1. **In-Memory Storage:** The index is stored in volatile RAM; restarting the server clears unsaved session data.
2. **Exact-Token Matching:** Words with common stems (e.g. *"program"*, *"programming"*, *"programmer"*) are treated as independent vocabulary terms.
3. **No Dynamic Ranking:** Matching documents are ordered by term frequency rather than advanced probabilistic relevance models (BM25).

---

## 15. Future Enhancements

1. **Linguistic Preprocessing:**
   - Integrate the Porter Stemming algorithm or lemmatization to conflate grammatical variations of terms.
   - Implement customizable stop-word removal filters (e.g., omitting *"the"*, *"is"*, *"at"*).
2. **Positional Inverted Indexing:**
   - Store term positions within each document to support exact phrase matching (e.g. `"love Python"` as a sequential bi-gram).
3. **Vector Space Ranking (TF-IDF):**
   - Calculate Term Frequency-Inverse Document Frequency (TF-IDF) weights and Cosine Similarity to score document relevance on a continuous scale $[0, 1]$.
4. **Persistent Serialization:**
   - Add SQLite or JSON disk persistence to retain collections across server restarts.

---

## 16. Conclusion

The "Design and Implementation of a Simple Inverted Index Generator for Information Retrieval" project demonstrates the fundamental concepts that power modern search engines. By mapping vocabulary terms to document posting lists, the system eliminates the computational bottleneck of sequential string searching. 

The application successfully fulfills all specified requirements: document management, automated inverted index generation, duplicate ID suppression, case-insensitive keyword searching, and Boolean AND/OR retrieval. Backed by 17 passing automated unit tests and a modern, responsive Streamlit dashboard, this project delivers an academically rigorous, reliable, and beginner-friendly solution for computer science students.

---

## 17. References

1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
2. Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern Information Retrieval: The Concepts and Technology Behind Search* (2nd ed.). Addison-Wesley.
3. Croft, W. B., Metzler, D., & Strohman, T. (2010). *Search Engines: Information Retrieval in Practice*. Pearson Education.
4. Streamlit Documentation. (2024). *Streamlit API Reference & Session State Management*. https://docs.streamlit.io/
5. Python Software Foundation. (2024). *Python 3.12 Standard Library: re and dataclasses documentation*. https://docs.python.org/3/
6. Pytest Development Team. (2024). *pytest: simple powerful testing with Python*. https://docs.pytest.org/
