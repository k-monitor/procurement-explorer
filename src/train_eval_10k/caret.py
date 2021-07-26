import numpy as np
import pandas as pd
from pycaret.classification import *
from sklearn.metrics import classification_report

df = pd.read_csv("data/processed/redflags10k.tsv", sep="\t", encoding="utf-8")

X = np.load("data/processed/document_embeddings.npy")
y = list(df["Category"])
np.savetxt("data/foo.csv", X, delimiter=",")

targets = [str(i) for i in list(range(len(X[0])))]
cdf = pd.DataFrame(X, columns=targets)
cdf["Category"] = y

data = cdf.sample(frac=0.95, random_state=786)
data_unseen = cdf.drop(data.index)
data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)


clf101 = setup(data=data, target="Category", session_id=123)
best_model = compare_models()
print(best_model)
etc = create_model("et")

tuned_etc = tune_model(etc)

plot_model(tuned_etc, plot="auc")
plot_model(tuned_etc, plot="pr")
plot_model(tuned_etc, plot="confusion_matrix")

predictions = predict_model(tuned_etc)

print(classification_report(predictions["Category"], predictions["Label"]))

final_et = finalize_model(tuned_etc)
unseen_predictions = predict_model(final_et, data=data_unseen)

print(
    classification_report(unseen_predictions["Category"], unseen_predictions["Label"])
)

save_model(final_et, "models/et_2020_03_02")
