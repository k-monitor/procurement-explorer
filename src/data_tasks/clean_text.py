from os import listdir
from os.path import isfile, join

in_path = "data/interim/ml"
out_path = "data/interim/clean_txt"
sentence_ending = [".", "?", "...", "!"]
ml_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]

for ml_file in ml_files:
    with open(join(in_path, ml_file), "r") as infile:
        with open(join(out_path, ml_file), "w") as outfile:
            text = []
            sent = []
            for l in infile:
                l = l.strip().split("\t")

                if len(l) > 2:
                    stem, pos = l[1], l[2]
                    if pos != "PUNCT" and stem not in sentence_ending:
                        if pos != "PUNCT" and pos != "NUM":
                            sent.append(stem.lower())
                    else:
                        text.append(" ".join(sent))
                        sent = []
            text = [t for t in text if len(t) > 0]
            outfile.write("\n".join(text))
