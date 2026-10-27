import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cyp_fragment_data.json"

def load_data():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    data = load_data()

    print("Available fields:", list(data.keys()))
    print("Number of molecules:", len(data["smiles"]))
    print("Number of datasets:", len(data["datasets"]))
    print("Number of fragments:", len(data["fragments"]))

    cyp_fragments = [
        frag for frag in data["fragments"]
        if frag["set"] == "cyp"
    ]

    print("\nCYP-relevant groups:")
    for frag in cyp_fragments:
        print(frag["label"] + ":", len(frag["idx"]))