from collections import Counter

import pandas as pd

df = pd.read_csv(
    "data/raw/redflags-5k-ctnotices-w-flags.tsv",
    sep="\t",
    encoding="utf-8",
    error_bad_lines=False,
)


cpvs = df["cpvs"]
cpvs = [str(e).split("|") for e in cpvs]


def normalize_cpv_codes(lst):
    return [e[:2] for e in lst]


cpvs = [normalize_cpv_codes(e) for e in cpvs]


def sort_cpvs(lst):
    lst = [int(float(e)) for e in lst]
    sorted(lst)
    lst = [str(e) for e in lst]
    return "|".join(lst)


cpvs_s = [sort_cpvs(e) for e in cpvs]
print("unique cpv codes", len(set(cpvs_s)))  # 1144 unique cpv combinations

cpv_nums = [item for sublist in cpvs for item in sublist]
cpv_nums = Counter(cpv_nums)
cpv_nums = {
    k: v for k, v in sorted(cpv_nums.items(), key=lambda item: item[1], reverse=True)
}

cpv_nums_above_50 = {k: v for k, v in cpv_nums.items() if v > 100}
print("keys", len(list(cpv_nums_above_50.keys())))
print(sum(list(cpv_nums_above_50.values())))
print(list(cpv_nums_above_50.keys()))


def labeling(lst):
    return sorted(set([e for e in lst if e in cpv_nums_above_50]))


cpvs_filtered = [labeling(e) for e in cpvs]
print("no label", len([e for e in cpvs_filtered if len(e) == 0]))
print("multilabel", len([e for e in cpvs_filtered if len(e) > 1]))
print("new labels", len(set(["|".join(e) for e in cpvs_filtered if len(e) > 1])))
# cpvs_filtered = ["|".join(e) for e in cpvs_filtered]
cpvs_filtered = [e[0] if len(e) == 1 else "na" for e in cpvs_filtered]
print(len(set(cpvs_filtered)))

df["cpvs_filtered"] = cpvs_filtered
is_coded = df["cpvs_filtered"] != "na"
df_coded = df[is_coded]

id2txts = zip(df_coded["id"], df_coded["shortDescription"])

for idx, t in id2txts:
    fname = idx + ".txt"
    with open(f"data/interim/txts/{fname}", "w") as outfile:
        outfile.write(t.strip())

with open("data/interim/interim.tsv", "w") as outfile:
    coded_df = df_coded.to_csv(index=False, sep="\t")
    outfile.write(coded_df)
