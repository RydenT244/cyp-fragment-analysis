import pandas as pd
from load_data import load_data


def extract_features(data):
    # Start with one row per molecule
    df = pd.DataFrame({
        "smiles": data["smiles"]
    })

    # Get CYP-relevant fragments
    fragments = [
        frag for frag in data["fragments"]
        if frag["set"] == "cyp"
    ]

    # Create binary feature columns
    for frag in fragments:
        df[frag["id"]] = 0
        df.loc[frag["idx"], frag["id"]] = 1

    return df


if __name__ == "__main__":
    data = load_data()

    df = extract_features(data)

    print("Feature matrix shape:", df.shape)
    print(df.head())

    # Save features for later analysis
    df.to_csv("data/cyp_features.csv", index=False)

    print("Saved features to data/cyp_features.csv")