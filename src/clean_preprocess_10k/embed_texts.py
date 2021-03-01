import nltk
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/processed/redflags10k.tsv", sep="\t", encoding="utf-8")

text_fields = [
    "shortDescription",
    "financialAbility",
    "otherParticularConditions",
    "particularProfession",
    "personalSituation",
    "technicalCapacity",
]


def filter_sentence(sent):
    tokens = nltk.tokenize.word_tokenize(sent)
    wds = [e.lower() for e in tokens if e.isalpha()]
    return " ".join(wds)


model = SentenceTransformer("SZTAKI-HLT/hubert-base-cc")

document_vectors = []
for idx, row in df.iterrows():
    procurement_text = []
    for field in text_fields:
        procurement_text.append(str(row[field]))
    procurement_text = " ".join(procurement_text)
    sentences = nltk.sent_tokenize(procurement_text)
    sentences2vectorize = [filter_sentence(s) for s in sentences]
    sentence_embeddings = model.encode(sentences2vectorize)
    mean_vector = np.mean(sentence_embeddings, axis=0)
    document_vectors.append(mean_vector)


s2 = np.asarray(document_vectors)
with open("data/processed/document_embeddings.npy", "wb") as outfile:
    np.save(outfile, s2)
