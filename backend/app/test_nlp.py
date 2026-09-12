from services.nlp_analyzer import NLPAnalyzer


analyzer = NLPAnalyzer()


test_interactions = [
    (
        "Product interest",
        "customer is interested in personal loan"
    ),
    (
        "Product rejection",
        "customer is not interested in credit card"
    ),
    (
        "Simple rejection",
        "not interested"
    ),
    (
        "Existing activation",
        "customer is activated on ME Enrollment MB Activation NB Activation"
    ),
    (
        "Existing application",
        "Already installed Mobile banking application and SmartHub Vyapar."
    ),
    (
        "Product discussion only",
        "discussed with customer about activated net banking and business credit card"
    ),
    (
        "Service issue",
        "customer sale was down as he has some issues as confirmed."
    ),
    (
        "Customer follow-up",
        "customer asked to call tomorrow"
    ),
]


for number, (test_name, interaction) in enumerate(
    test_interactions,
    start=1
):

    print("\n")
    print("=" * 70)
    print(f"TEST CASE {number}: {test_name}")
    print("=" * 70)

    print("\nInteraction:")
    print(interaction)

    result = analyzer.analyze(interaction)

    print("\nAnalysis:")

    for key, value in result.items():
        print(f"{key}: {value}")