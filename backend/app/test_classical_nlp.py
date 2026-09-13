from app.services.classical_nlp import ClassicalNLPAnalyzer

analyzer = ClassicalNLPAnalyzer()


test_cases = [
    "customer is interested in personal loan",
    "customer is not interested in credit card",
    "not interested",
    "customer is activated on ME Enrollment MB Activation NB Activation",
    "Already installed Mobile banking application and SmartHub Vyapar.",
    "discussed with customer about activated net banking and business credit card",
    "customer sale was down as he has some issues as confirmed.",
    "customer asked to call tomorrow",
]


for number, interaction in enumerate(test_cases, start=1):

    print("\n" + "=" * 70)
    print(f"TEST CASE {number}")
    print("=" * 70)

    print("\nInteraction:")
    print(interaction)

    result = analyzer.analyze(interaction)

    print("\nAnalysis:")

    for key, value in result.items():
        print(f"{key}: {value}")