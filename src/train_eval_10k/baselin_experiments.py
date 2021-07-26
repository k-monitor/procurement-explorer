import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

df = pd.read_csv("data/processed/redflags10k.tsv", sep="\t", encoding="utf-8")

X = np.load("data/processed/document_embeddings.npy")
y = list(df["Category"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42, stratify=y, test_size=0.5
)

clf = GradientBoostingClassifier(
    n_estimators=100, learning_rate=1.0, max_depth=4, random_state=42
)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
