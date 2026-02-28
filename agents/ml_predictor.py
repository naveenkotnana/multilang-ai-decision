"""Agent 4: ML Predictor Agent.

Loads a trained scikit-learn model and predicts urgency level
with confidence scores.
"""

from __future__ import annotations

import os
import joblib
import pandas as pd
from typing import Tuple

from .feature_agent import FeatureVector

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
_MODEL_PATH = os.path.join(_MODEL_DIR, "multilingual_classifier.pkl")

URGENCY_MAP = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}


class MLPredictorAgent:
    """Predicts urgency level from feature vectors using a trained model."""

    name = "ML_PREDICTOR"

    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is None:
            if not os.path.exists(_MODEL_PATH):
                raise FileNotFoundError(
                    f"Trained model not found at {_MODEL_PATH}. "
                    "Run `python train_model.py` first."
                )
            self._model = joblib.load(_MODEL_PATH)

    def predict(self, features: FeatureVector) -> Tuple[str, float]:
        """Return (urgency_label, confidence) for the given features."""
        self._load_model()

        df = pd.DataFrame([features.to_dict()])
        prediction = int(self._model.predict(df)[0])
        probabilities = self._model.predict_proba(df)[0]
        confidence = float(probabilities.max())

        return URGENCY_MAP.get(prediction, "MEDIUM"), confidence
