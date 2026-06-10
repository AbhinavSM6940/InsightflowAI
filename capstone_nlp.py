"""
Capstone Project: NLP Engineer Solution

Part 1: Sentiment Analysis
- Pre-process review text
- Generate VADER sentiment scores
- Create sentiment classes from overall ratings
- Train/evaluate Decision Tree and Multinomial Naive Bayes using TF-IDF

Part 2: Relationship Extraction & Topic Modeling
- Process multiple text files
- Annotate entities with spaCy
- Validate entity labels with a manual lookup dictionary
- Extract company attributes
- Run LDA topic modeling with Gensim
- Group articles by dominant topic
"""

from __future__ import annotations

import argparse
import builtins
import importlib
import os
import re
import string
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

import nltk


# ----------------------------- Utility / Setup -----------------------------
def ensure_nltk_resources() -> None:
    """Download required NLTK resources if they are missing."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("sentiment/vader_lexicon.zip", "vader_lexicon"),
    ]
    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


def load_spacy_model(model_name: str = "en_core_web_sm"):
    """
    Load spaCy model and provide a clear error if unavailable.
    The user can install model via:
      python -m spacy download en_core_web_sm
    """
    try:
        spacy_mod = import_spacy_with_torch_fallback()
        return spacy_mod.load(model_name)
    except OSError as exc:
        raise RuntimeError(
            f"spaCy model '{model_name}' is not installed. "
            f"Install with: python -m spacy download {model_name}"
        ) from exc


def import_spacy_with_torch_fallback() -> Any:
    """
    Import spaCy with a fallback for environments where a broken torch DLL
    causes OSError during thinc's optional torch detection.
    """
    try:
        return importlib.import_module("spacy")
    except OSError as exc:
        err = str(exc).lower()
        if "c10.dll" not in err and "torch" not in err:
            raise

        original_import = builtins.__import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "torch" or name.startswith("torch."):
                raise ImportError("Skipping torch due local DLL issue.")
            return original_import(name, globals, locals, fromlist, level)

        builtins.__import__ = guarded_import
        try:
            # Clear partial modules to retry a clean import path.
            for mod_name in list(sys.modules.keys()):
                if mod_name == "spacy" or mod_name.startswith("spacy.") or mod_name.startswith("thinc"):
                    sys.modules.pop(mod_name, None)
            return importlib.import_module("spacy")
        finally:
            builtins.__import__ = original_import


# ----------------------------- Part 1: Sentiment -----------------------------
def clean_text(text: str, stop_words: set) -> str:
    """Lowercase text, remove punctuation, tokenize, and remove stopwords."""
    if pd.isna(text):
        return ""

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    tokens = [tok for tok in tokens if tok.isalpha() and tok not in stop_words]
    return " ".join(tokens)


def categorize_overall_rating(rating: float) -> str:
    """Map numeric overall rating to Negative/Neutral/Positive class."""
    if rating <= 2:
        return "Negative"
    if rating == 3:
        return "Neutral"
    return "Positive"


def run_sentiment_analysis_pipeline(
    reviews_csv_path: str,
    text_column: str = "reviewText",
    rating_column: str = "overall",
) -> pd.DataFrame:
    """
    Execute Part 1:
    - Load CSV
    - Preprocess reviews
    - Compute VADER polarity scores
    - Create target category from overall rating
    - Train and evaluate Decision Tree + MultinomialNB
    """
    ensure_nltk_resources()
    stop_words = set(stopwords.words("english"))
    sia = SentimentIntensityAnalyzer()

    df = pd.read_csv(reviews_csv_path)
    required_cols = {text_column, rating_column}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    # Keep only rows with required fields
    df = df[[text_column, rating_column]].dropna().copy()

    # Text cleaning
    df["clean_text"] = df[text_column].astype(str).apply(lambda x: clean_text(x, stop_words))

    # VADER polarity scores
    vader_scores = df["clean_text"].apply(sia.polarity_scores).apply(pd.Series)
    vader_scores.columns = ["vader_neg", "vader_neu", "vader_pos", "vader_compound"]
    df = pd.concat([df, vader_scores], axis=1)

    # Target class from overall rating
    df["rating_category"] = df[rating_column].apply(categorize_overall_rating)

    # TF-IDF features
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df["clean_text"])
    y = df["rating_category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Model 1: Decision Tree
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    print("\n=== DecisionTreeClassifier Classification Report ===")
    print(classification_report(y_test, dt_pred, zero_division=0))

    # Model 2: Multinomial Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train, y_train)
    nb_pred = nb_model.predict(X_test)
    print("\n=== MultinomialNB Classification Report ===")
    print(classification_report(y_test, nb_pred, zero_division=0))

    return df


# ----------------------------- Part 2: Extraction + LDA -----------------------------
@dataclass
class DocumentExtraction:
    file_name: str
    company_name: str
    headquarters: str
    domain: str
    date_of_incorporation: str
    company_type: str


def read_text_files(text_dir: str) -> Dict[str, str]:
    """Load all .txt files from a directory."""
    if not os.path.isdir(text_dir):
        raise ValueError(f"Directory does not exist: {text_dir}")

    files = {}
    for file_name in os.listdir(text_dir):
        if file_name.lower().endswith(".txt"):
            full_path = os.path.join(text_dir, file_name)
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                files[file_name] = f.read()
    if not files:
        raise ValueError(f"No .txt files found in directory: {text_dir}")
    return files


def build_manual_lookup() -> Dict[str, set]:
    """
    Manual lookup dictionary for validation.
    Extend this dictionary with project-specific values as needed.
    """
    return {
        "Company": {
            "google",
            "microsoft",
            "amazon",
            "apple",
            "meta",
            "tesla",
            "infosys",
            "tcs",
            "wipro",
        },
        "Place": {
            "california",
            "new york",
            "seattle",
            "london",
            "bangalore",
            "mumbai",
            "hyderabad",
            "delhi",
            "paris",
        },
        "Domain": {
            "technology",
            "finance",
            "healthcare",
            "retail",
            "automotive",
            "telecommunications",
            "software",
            "cloud computing",
        },
    }


def validate_entity(entity_text: str, entity_group: str, lookup: Dict[str, set]) -> bool:
    """Validate extracted entity against manual lookup dictionary."""
    return entity_text.lower().strip() in lookup.get(entity_group, set())


def extract_company_attributes(
    text: str, nlp, lookup: Dict[str, set]
) -> Dict[str, str]:
    """
    Extract specific attributes:
    - Company Name
    - Headquarters
    - Domain
    - Date of Incorporation
    - Company Type
    """
    doc = nlp(text)

    company_name = "Not Found"
    headquarters = "Not Found"
    domain = "Not Found"
    date_of_incorporation = "Not Found"
    company_type = "Not Found"

    # Entity extraction based on spaCy labels + manual validation
    for ent in doc.ents:
        ent_text = ent.text.strip()
        lower_text = ent_text.lower()

        if company_name == "Not Found" and ent.label_ == "ORG":
            if validate_entity(lower_text, "Company", lookup):
                company_name = ent_text

        if headquarters == "Not Found" and ent.label_ in {"GPE", "LOC"}:
            if validate_entity(lower_text, "Place", lookup):
                headquarters = ent_text

        if domain == "Not Found":
            if validate_entity(lower_text, "Domain", lookup):
                domain = ent_text

        if date_of_incorporation == "Not Found" and ent.label_ == "DATE":
            date_of_incorporation = ent_text

    # Pattern-based fallback for company type
    type_patterns = [
        r"\b(private limited|public limited|llc|ltd|inc\.?|corporation|corp\.?)\b",
    ]
    for pattern in type_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            company_type = match.group(1)
            break

    return {
        "Company Name": company_name,
        "Headquarters": headquarters,
        "Domain": domain,
        "Date of Incorporation": date_of_incorporation,
        "Company Type": company_type,
    }


def preprocess_for_topic_modeling(text: str, stop_words: set) -> List[str]:
    """Tokenize and clean text for LDA topic modeling."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [tok for tok in tokens if tok.isalpha() and tok not in stop_words and len(tok) > 2]


def run_topic_modeling(
    docs_by_file: Dict[str, str],
    num_topics: int = 4,
    passes: int = 15,
) -> Tuple[LdaModel, Dict[str, List[Tuple[int, float]]], Dict[int, List[str]]]:
    """
    Run Gensim LDA and group articles by dominant topic.
    Returns:
    - trained LDA model
    - topic distribution per file
    - grouped files by dominant topic
    """
    ensure_nltk_resources()
    stop_words = set(stopwords.words("english"))

    file_names = list(docs_by_file.keys())
    tokenized_docs = [
        preprocess_for_topic_modeling(docs_by_file[file_name], stop_words) for file_name in file_names
    ]

    dictionary = corpora.Dictionary(tokenized_docs)
    dictionary.filter_extremes(no_below=1, no_above=0.7)
    corpus = [dictionary.doc2bow(doc_tokens) for doc_tokens in tokenized_docs]

    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=passes,
    )

    topic_distributions = {}
    grouped_articles: Dict[int, List[str]] = {}
    for i, bow in enumerate(corpus):
        topic_probabilities = lda_model.get_document_topics(bow)
        topic_distributions[file_names[i]] = topic_probabilities

        dominant_topic = max(topic_probabilities, key=lambda x: x[1])[0]
        grouped_articles.setdefault(dominant_topic, []).append(file_names[i])

    return lda_model, topic_distributions, grouped_articles


def run_relationship_and_topic_pipeline(text_dir: str) -> Tuple[pd.DataFrame, LdaModel]:
    """Execute Part 2 end-to-end."""
    nlp = load_spacy_model("en_core_web_sm")
    lookup = build_manual_lookup()
    docs_by_file = read_text_files(text_dir)

    # Relationship extraction
    records = []
    for file_name, text in docs_by_file.items():
        attrs = extract_company_attributes(text, nlp, lookup)
        records.append(
            DocumentExtraction(
                file_name=file_name,
                company_name=attrs["Company Name"],
                headquarters=attrs["Headquarters"],
                domain=attrs["Domain"],
                date_of_incorporation=attrs["Date of Incorporation"],
                company_type=attrs["Company Type"],
            ).__dict__
        )
    extraction_df = pd.DataFrame(records)

    print("\n=== Extracted Company Attributes ===")
    print(extraction_df.to_string(index=False))

    # Topic modeling
    lda_model, topic_distributions, grouped_articles = run_topic_modeling(docs_by_file)

    print("\n=== LDA Topics ===")
    for topic_id, topic_words in lda_model.print_topics(num_words=10):
        print(f"Topic {topic_id}: {topic_words}")

    print("\n=== Articles Grouped by Dominant Topic ===")
    for topic_id, files in sorted(grouped_articles.items()):
        print(f"Topic {topic_id}: {files}")

    # Also print per-file distribution
    print("\n=== Topic Distribution Per Article ===")
    for file_name, distribution in topic_distributions.items():
        dist_str = ", ".join([f"(Topic {t}, {p:.3f})" for t, p in distribution])
        print(f"{file_name}: {dist_str}")

    return extraction_df, lda_model


# ----------------------------- Main Entry Point -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Two-part NLP Capstone Solution")
    parser.add_argument(
        "--reviews_csv",
        type=str,
        required=True,
        help="Path to reviews CSV file (must contain reviewText and overall columns by default).",
    )
    parser.add_argument(
        "--text_dir",
        type=str,
        required=True,
        help="Path to directory containing .txt files for extraction/topic modeling.",
    )
    parser.add_argument(
        "--text_column",
        type=str,
        default="reviewText",
        help="Review text column name in CSV.",
    )
    parser.add_argument(
        "--rating_column",
        type=str,
        default="overall",
        help="Overall rating column name in CSV.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("Running Part 1: Sentiment Analysis...")
    _ = run_sentiment_analysis_pipeline(
        reviews_csv_path=args.reviews_csv,
        text_column=args.text_column,
        rating_column=args.rating_column,
    )

    print("\nRunning Part 2: Relationship Extraction & Topic Modeling...")
    _ = run_relationship_and_topic_pipeline(args.text_dir)


if __name__ == "__main__":
    main()
