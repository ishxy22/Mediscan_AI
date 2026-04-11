"""Train Random Forest on symptom strings → binary features; save model and symptom list."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

_ROOT = Path(__file__).resolve().parent.parent
_DATA_PATH = _ROOT / "data" / "dataset.csv"
_MODEL_DIR = Path(__file__).resolve().parent

_SYMPTOM_SLOTS = [f"Symptom_{i}" for i in range(1, 18)]


def _row_symptoms(row: pd.Series) -> set[str]:
    present: set[str] = set()
    for col in _SYMPTOM_SLOTS:
        raw = row[col]
        if pd.isna(raw):
            continue
        s = str(raw).strip()
        if s:
            present.add(s)
    return present


def load_xy(csv_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(csv_path)
    for col in _SYMPTOM_SLOTS:
        if col not in df.columns:
            raise ValueError(f"Missing column {col!r} in {csv_path}")
    if "Disease" not in df.columns:
        raise ValueError(f"Missing 'Disease' column in {csv_path}")

    all_symptoms: set[str] = set()
    for _, row in df.iterrows():
        all_symptoms.update(_row_symptoms(row))

    symptom_columns = sorted(all_symptoms)
    rows: list[list[int]] = []
    for _, row in df.iterrows():
        present = _row_symptoms(row)
        rows.append([1 if s in present else 0 for s in symptom_columns])

    X = pd.DataFrame(rows, columns=symptom_columns, index=df.index)
    y = df["Disease"].astype(str).str.strip()
    return X, y


def main() -> None:
    X, y = load_xy(_DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    joblib.dump(clf, _MODEL_DIR / "rf_model.pkl")
    joblib.dump(list(X.columns), _MODEL_DIR / "symptoms_list.pkl")


if __name__ == "__main__":
    main()
