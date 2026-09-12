import pandas as pd

from services.nlp_analyzer import NLPAnalyzer


DATASET_PATH = "../data/Sample_Shikhar.xlsx"


def main():
    print("Loading dataset...")

    df = pd.read_excel(DATASET_PATH)

    print(f"Rows loaded: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    analyzer = NLPAnalyzer()

    # Take the first interaction for the first real test
    interaction = str(df.iloc[0]["Initiatives/Opportunities"])

    print("\nRAW INTERACTION")
    print("=" * 50)
    print(interaction)

    print("\nNLP ANALYSIS")
    print("=" * 50)

    result = analyzer.analyze(interaction)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
