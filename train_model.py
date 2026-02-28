"""Synthetic training data generator + model trainer.

Generates multilingual training samples using language-specific
urgency/sentiment keywords, then trains a LogisticRegression
classifier for urgency prediction (LOW / MEDIUM / HIGH).

Usage:
    python train_model.py
"""

from __future__ import annotations

import os
import sys
import random
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
import joblib

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from languages import LANGUAGE_REGISTRY

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
_MODEL_PATH = os.path.join(_MODEL_DIR, "multilingual_classifier.pkl")
_LANG_CODES = ["en", "hi", "te", "ta", "ml", "kn", "or", "mr"]
_URGENCY_LABELS = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}

random.seed(42)
np.random.seed(42)


def generate_samples(n_per_lang: int = 500) -> pd.DataFrame:
    """Generate synthetic feature vectors for all 8 languages."""
    rows = []
    for lang_code in _LANG_CODES:
        lang = LANGUAGE_REGISTRY[lang_code]
        for _ in range(n_per_lang):
            # Randomly sample scenario parameters
            severity = random.randint(1, 10)
            interactions = random.randint(0, 10)
            is_premium = random.choice([0, 1])

            # Simulate urgency signal based on scenario
            if severity >= 8:
                urgency_signal = random.uniform(0.4, 1.0)
                label = 2  # HIGH
            elif severity >= 5:
                urgency_signal = random.uniform(0.15, 0.6)
                label = 1  # MEDIUM
            else:
                urgency_signal = random.uniform(0.0, 0.3)
                label = 0  # LOW

            # Add noise: premium customers with many interactions trend higher
            if is_premium and interactions >= 4:
                label = min(label + 1, 2)
            # Very low severity should stay low
            if severity <= 2 and urgency_signal < 0.1:
                label = 0

            sentiment = random.uniform(-1, 0) if label >= 1 else random.uniform(-0.3, 1)
            urgency_kw = random.randint(0, 4) if label >= 1 else random.randint(0, 1)
            neg_kw = random.randint(0, 3) if label >= 1 else random.randint(0, 1)
            pos_kw = random.randint(0, 2) if label == 0 else random.randint(0, 1)
            tokens = random.randint(3, 30)

            row = {
                "urgency_signal": urgency_signal,
                "sentiment_score": sentiment,
                "urgency_keyword_count": urgency_kw,
                "negative_keyword_count": neg_kw,
                "positive_keyword_count": pos_kw,
                "token_count": tokens,
                "customer_type_premium": is_premium,
                "interaction_count": interactions,
                "severity_score": severity,
            }
            # One-hot language encoding
            for lc in _LANG_CODES:
                row[f"lang_{lc}"] = int(lc == lang_code)

            row["label"] = label
            rows.append(row)

    return pd.DataFrame(rows)


def train():
    """Train the multilingual urgency classifier and save it."""
    print("=" * 60)
    print("  Multi-Language Urgency Classifier Trainer")
    print("=" * 60)

    print("\n📊 Generating synthetic training data...")
    df = generate_samples(n_per_lang=600)
    print(f"   Total samples: {len(df)}")
    print(f"   Label distribution:\n{df['label'].value_counts().sort_index().to_string()}")

    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )

    print(f"\n🏋️ Training LogisticRegression (train={len(X_train)}, test={len(X_test)})...")
    model = LogisticRegression(
        max_iter=1000,
        multi_class="multinomial",
        solver="lbfgs",
        C=1.0,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["LOW", "MEDIUM", "HIGH"]))

    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"🔁 5-Fold CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Per-language accuracy
    print("\n🌐 Per-Language Accuracy:")
    for lang_code in _LANG_CODES:
        mask = X_test[f"lang_{lang_code}"] == 1
        if mask.sum() > 0:
            lang_acc = (y_pred[mask] == y_test.values[mask]).mean()
            lang_name = LANGUAGE_REGISTRY[lang_code].native_name
            print(f"   {lang_name} ({lang_code}): {lang_acc:.1%}")

    # Save model
    os.makedirs(_MODEL_DIR, exist_ok=True)
    joblib.dump(model, _MODEL_PATH)
    print(f"\n✅ Model saved to {_MODEL_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    train()
