import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

in_path = "data/interim/txts"
out_path = "data/interim/ml"

text_files = [
    f for f in os.listdir(in_path) if os.path.isfile(os.path.join(in_path, f))
]


def process_text(text_file):
    fname = os.path.join(in_path, text_file)
    outfname = os.path.join(out_path, text_file)
    try:
        subprocess.call(
            [
                "java",
                "-Xmx1G",
                "-jar",
                "etc/magyarlanc-3.0.jar",
                "-mode",
                "morphparse",
                "-input",
                fname,
                "-output",
                outfname,
            ]
        )
    except Exception as e:
        print(e)
        pass


with ProcessPoolExecutor(max_workers=3) as executor:
    executor.map(process_text, text_files)
