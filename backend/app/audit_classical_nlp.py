import pandas as pd

from app.services.classical_nlp import ClassicalNLPAnalyzer


INPUT_FILE = "../data/Sample_Shikhar.xlsx"


def main():

    print("=" * 70)
    print("CLASSICAL NLP DATASET AUDIT")
    print("=" * 70)

    df = pd.read_excel(INPUT_FILE)

    analyzer = ClassicalNLPAnalyzer()

    results = []

    for index, row in df.iterrows():

        interaction = row["Initiatives/Opportunities"]

        if pd.isna(interaction):
            continue

        interaction = str(interaction).strip()

        if not interaction:
            continue

        result = analyzer.analyze(interaction)

        results.append({
            "row": index + 2,
            "interaction": interaction,
            **result,
        })

    result_df = pd.DataFrame(results)

    print("\nTotal interactions analyzed:", len(result_df))

    print("\n" + "=" * 70)
    print("SENTIMENT DISTRIBUTION")
    print("=" * 70)

    print(
        result_df["sentiment"]
        .value_counts()
        .to_string()
    )

    print("\n" + "=" * 70)
    print("CUSTOMER INTENT DISTRIBUTION")
    print("=" * 70)

    print(
        result_df["customer_intent"]
        .value_counts()
        .to_string()
    )

    print("\n" + "=" * 70)
    print("INTEREST DISTRIBUTION")
    print("=" * 70)

    print(
        result_df["interest_shown"]
        .value_counts(dropna=False)
        .to_string()
    )

    print("\n" + "=" * 70)
    print("FOLLOW-UP DISTRIBUTION")
    print("=" * 70)

    print(
        result_df["follow_up_required"]
        .value_counts()
        .to_string()
    )

    print("\n" + "=" * 70)
    print("PRODUCTS DETECTED")
    print("=" * 70)

    products = (
        result_df["interested_product"]
        .dropna()
        .value_counts()
    )

    if len(products):
        print(products.to_string())
    else:
        print("No interested products detected.")

    print("\n" + "=" * 70)
    print("SAMPLE CLASSIFICATIONS")
    print("=" * 70)

    sample = result_df[
        [
            "row",
            "interaction",
            "sentiment",
            "interest_shown",
            "interested_product",
            "not_interested_product",
            "customer_intent",
            "follow_up_required",
        ]
    ].head(20)

    for _, row in sample.iterrows():

        print(f"\nRow {row['row']}:")
        print(f"Interaction: {row['interaction']}")
        print(f"Sentiment: {row['sentiment']}")
        print(f"Interest: {row['interest_shown']}")
        print(f"Interested Product: {row['interested_product']}")
        print(
            f"Rejected Product: "
            f"{row['not_interested_product']}"
        )
        print(f"Intent: {row['customer_intent']}")
        print(
            f"Follow-up: "
            f"{row['follow_up_required']}"
        )


if __name__ == "__main__":
    main()