from os import listdir
from os.path import isfile, join

import pandas as pd

in_path = "data/interim/clean_txt"

df = pd.read_csv("data/interim/interim.tsv", encoding="utf-8", sep="\t")

text_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]
idxs = list(df["id"])

texts = []
for text_file in text_files:
    with open(join(in_path, text_file), "r") as infile:
        text = []
        for l in infile:
            s = l.strip().split()
            text.extend(s)
    texts.append(text)

df["cleaned text"] = texts
is_text = [True if len(e) > 0 else False for e in texts]

df_final = df[is_text]

with open("data/processed/redflags.tsv", "w") as outfile:
    outfile.write(df_final.to_csv(index=False, sep="\t"))
