from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "Sample_Shikhar.xlsx"


def main():
    df = pd.read_excel(DATASET_PATH)

    interactions = (
        df["Initiatives/Opportunities"]
        .dropna()
        .astype(str)
    )

    # Remove very short/empty interactions
    meaningful = interactions[
        interactions.str.strip().str.len() > 10
    ]

    print(f"Total rows: {len(df)}")
    print(f"Meaningful interactions: {len(meaningful)}")

    print("\nSAMPLE REAL INTERACTIONS")
    print("=" * 70)

    for index, interaction in meaningful.head(20).items():
        print(f"\nRow {index + 2}:")
        print(interaction)


if __name__ == "__main__":
    main()