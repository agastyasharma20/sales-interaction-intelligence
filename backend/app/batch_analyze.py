import os
import time

import pandas as pd
from pydantic import ValidationError

from app.services.nlp_analyzer import NLPAnalyzer

INPUT_FILE = "../data/Sample_Shikhar.xlsx"
OUTPUT_FILE = "../data/analysis_results.xlsx"

INTERACTION_COLUMN = "Initiatives/Opportunities"


def main():
    print("=" * 70)
    print("HDFC SALES INTERACTION NLP - BATCH ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------
    # Load dataset
    # --------------------------------------------------

    print("\nLoading dataset...")

    df = pd.read_excel(INPUT_FILE)

    print(f"Total rows found: {len(df)}")

    if INTERACTION_COLUMN not in df.columns:
        raise ValueError(
            f"Required column '{INTERACTION_COLUMN}' not found."
        )

    # --------------------------------------------------
    # Prepare output columns
    # --------------------------------------------------

    output_columns = [
        "sentiment",
        "follow_up_required",
        "interest_shown",
        "interested_product",
        "not_interested_product",
        "customer_intent",
        "follow_up_action",
        "confidence",
        "analysis_status",
        "analysis_error",
    ]

    for column in output_columns:
        df[column] = None

    # --------------------------------------------------
    # Initialize analyzer
    # --------------------------------------------------

    analyzer = NLPAnalyzer()

    processed = 0
    failed = 0
    skipped = 0

    # --------------------------------------------------
    # Process interactions
    # --------------------------------------------------

    for index, row in df.iterrows():

        interaction = row[INTERACTION_COLUMN]

        # Skip empty interactions
        if pd.isna(interaction) or not str(interaction).strip():
            skipped += 1
            df.at[index, "analysis_status"] = "skipped"
            continue

        interaction = str(interaction).strip()

        print(
            f"\n[{index + 1}/{len(df)}] "
            f"Analyzing interaction..."
        )

        max_retries = 3

        for attempt in range(1, max_retries + 1):

            try:
                result = analyzer.analyze(interaction)

                # Store results
                for key, value in result.items():
                    df.at[index, key] = value

                df.at[index, "analysis_status"] = "success"
                df.at[index, "analysis_error"] = None

                processed += 1

                print("  ✓ Success")
                break

            except ValidationError as exc:
                failed += 1

                df.at[index, "analysis_status"] = "validation_error"
                df.at[index, "analysis_error"] = str(exc)

                print("  ✗ Validation error")
                break

            except Exception as exc:

                print(
                    f"  ⚠ Attempt {attempt}/{max_retries} failed: "
                    f"{exc}"
                )

                if attempt < max_retries:
                    wait_time = attempt * 2

                    print(
                        f"  Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    failed += 1

                    df.at[index, "analysis_status"] = "failed"
                    df.at[index, "analysis_error"] = str(exc)

                    print("  ✗ Failed after retries")

        # Small delay to avoid hammering the API
        time.sleep(0.2)

        # --------------------------------------------------
        # Checkpoint
        # --------------------------------------------------

        if (index + 1) % 25 == 0:

            os.makedirs(
                os.path.dirname(OUTPUT_FILE),
                exist_ok=True,
            )

            df.to_excel(
                OUTPUT_FILE,
                index=False,
            )

            print(
                f"\n  Checkpoint saved at row {index + 1}"
            )

    # --------------------------------------------------
    # Final save
    # --------------------------------------------------

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True,
    )

    df.to_excel(
        OUTPUT_FILE,
        index=False,
    )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print("\n")
    print("=" * 70)
    print("BATCH ANALYSIS COMPLETED")
    print("=" * 70)

    print(f"\nTotal rows:     {len(df)}")
    print(f"Processed:      {processed}")
    print(f"Failed:         {failed}")
    print(f"Skipped:        {skipped}")

    print(f"\nOutput file:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()