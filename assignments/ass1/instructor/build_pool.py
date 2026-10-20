"""Build the pool of comments the students sample from (instructor only; students get the result).

Source: Civil Comments (google/civil_comments, test split, CC0). Each comment has a `toxicity`
score = the share of crowd annotators who called it toxic. We cut the score into five bands that
we expect to land on the 1-5 scale, and keep N_PER_BAND short comments from each band.

Run:  python instructor/build_pool.py            (downloads about 20 MB the first time)
Writes:
  student/data/pool.csv       id | text   (shuffled; no score, no band, no label)
  student/prepare_items.py    its _MIX line is rewritten: the band of every comment, encoded (so the
                              script can draw a balanced sample while the data file stays clean)
  instructor/pool_key.csv     id | toxicity | severe_toxicity | threat | insult | identity_attack | band
"""
import base64
import random
import re
import zlib
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
URL = ("https://huggingface.co/datasets/google/civil_comments/resolve/"
       "refs%2Fconvert%2Fparquet/default/test/0000.parquet")
CACHE = HERE / "civil_comments_test.parquet"  # not committed: see .gitignore

SEED = 2024
N_PER_BAND = 50
MIN_CHARS, MAX_CHARS = 60, 400

# expected rating -> which comments qualify. The crowd score alone is noisy at the top (a mild comment
# can get 1.00), so bands 4 and 5 also need the subtype scores (insult, obscene, threat, ...) to agree.
# Band 5 was read by hand: these rows (index in the source file) look mild, are off-topic or spam, or are
# needlessly gratuitous, so they are left out.
EXCLUDE_5 = {48730, 89710, 86310, 55628, 59031, 53673, 35688, 80360, 13060, 94647, 25383, 38322, 35749,
             62809, 96628, 25628, 32069, 66948}
SEVERITY = ["severe_toxicity", "threat", "identity_attack", "insult", "obscene"]

BANDS = {
    1: lambda d: d.toxicity == 0,
    2: lambda d: d.toxicity.between(0.1, 0.3),
    3: lambda d: d.toxicity.between(0.4, 0.6),
    4: lambda d: d.toxicity.between(0.7, 0.89) & (d.insult >= 0.6),
    5: lambda d: ((d.toxicity >= 0.9) & ~d.index.isin(EXCLUDE_5) & (d[SEVERITY].sum(axis=1) >= 1.3)
                  & ((d.severe_toxicity >= 0.15) | (d.threat >= 0.5) | (d.identity_attack >= 0.5)
                     | ((d.insult >= 0.9) & (d.obscene >= 0.3)))),
}


def main():
    if not CACHE.exists():
        print("downloading", URL)
        urllib.request.urlretrieve(URL, CACHE)
    d = pd.read_parquet(CACHE)
    d["text"] = d.text.str.replace(r"\s+", " ", regex=True).str.strip()
    d = d[d.text.str.len().between(MIN_CHARS, MAX_CHARS)]
    d = d[~d.text.str.contains(r"https?://|www\.|@\w", regex=True)]  # no links or handles
    d = d.drop_duplicates("text")

    rng = random.Random(SEED)
    parts = []
    for band, rule in BANDS.items():
        pool = d[rule(d)]
        pick = pool.sample(n=N_PER_BAND, random_state=SEED).assign(band=band)
        parts.append(pick)
        print(f"band {band}: {len(pool)} candidates, kept {N_PER_BAND}")
    pool = pd.concat(parts).sample(frac=1, random_state=SEED).reset_index(drop=True)
    pool.insert(0, "id", [f"c{i:03d}" for i in range(1, len(pool) + 1)])

    (ROOT / "student" / "data").mkdir(exist_ok=True)
    pool[["id", "text"]].to_csv(ROOT / "student" / "data" / "pool.csv", index=False, encoding="utf-8")
    pool[["id", "toxicity", "severe_toxicity", "threat", "insult", "identity_attack", "band"]].to_csv(
        HERE / "pool_key.csv", index=False)
    # the band of every comment, in the order of the sorted ids, packed so that it is not readable at a glance
    bands = "".join(str(b) for _, b in sorted(zip(pool.id, pool.band)))
    mix = base64.b64encode(zlib.compress(bands.encode())).decode()
    script = ROOT / "student" / "prepare_items.py"
    text = script.read_text(encoding="utf-8")
    text = re.sub(r'^_MIX = ".*"$', f'_MIX = "{mix}"', text, flags=re.M)
    script.write_text(text, encoding="utf-8")
    print("wrote", len(pool), "comments")


if __name__ == "__main__":
    main()
