import json
import os
from app.models import NLPAnalysis
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class NLPAnalyzer:
    """
    Analyzes salesperson-customer interaction text
    using an LLM.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in .env")

        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"

    def analyze(self, interaction_text: str) -> dict:
        """
        Analyze one salesperson-customer interaction.
        """

        prompt = f"""
You are an NLP analyst for a banking sales interaction
intelligence system.

Analyze ONLY the salesperson-customer interaction below.

Extract the customer's actual intent and requirements.

IMPORTANT:
The interaction may contain:
- spelling mistakes
- grammar mistakes
- abbreviations
- incomplete sentences
- banking terminology
- multiple products
- salesperson actions mixed with customer statements

Do NOT invent information.

==================================================
REQUIRED OUTPUT
==================================================

Return ONLY valid JSON with exactly these fields:

{{
    "sentiment": "positive",
    "follow_up_required": false,
    "interest_shown": null,
    "interested_product": null,
    "not_interested_product": null,
    "customer_intent": "unclear",
    "follow_up_action": null,
    "confidence": 0.0
}}

==================================================
FIELD RULES
==================================================

1. sentiment

Choose exactly one:

- positive
- negative
- neutral

Base sentiment on the customer's interaction/context.

If there is insufficient emotional information, use "neutral".

--------------------------------------------------

2. follow_up_required

Use true ONLY when the customer explicitly asks for, requests,
or clearly indicates a need for a future follow-up.

Examples:

"customer asked to call tomorrow"
→ true

"customer requested callback"
→ true

"customer said call me next week"
→ true

Use false when the future action is only the salesperson's
plan or recommendation.

Examples:

"salesperson will call customer tomorrow"
→ false

"meet customer and guide to download MB"
→ false

"discussed for payment GST"
→ false

If there is insufficient evidence of a customer-requested
follow-up:
→ false

--------------------------------------------------
3. interest_shown

Use:

true
= customer clearly expresses interest in purchasing, applying
for, activating, adopting, or proceeding with a product/service.

false
= customer clearly rejects, refuses, does not require, or is
not interested in a product/service.

null
= customer intent cannot be determined.

IMPORTANT:

Do NOT treat the following as proof of new interest:

- existing activation
- existing usage
- already installed application
- salesperson discussing a product
- salesperson recommending a product
- salesperson visiting/contacting the customer
- product merely being mentioned

Examples:

"customer is activated on ME Enrollment"
→ interest_shown = null

"Already installed Mobile banking application"
→ interest_shown = null

"discussed with customer about business credit card"
→ interest_shown = null

"customer is interested in business credit card"
→ interest_shown = true--------------------------------------------------

4. interested_product

Return the product/service the customer is interested in.

Examples:

"customer is interested in personal loan"
→ "personal loan"

"customer is interested in proceeding with the LAP loan"
→ "LAP loan"

If no clear interest exists:
→ null

--------------------------------------------------

5. not_interested_product

Return the product/service explicitly rejected by the customer.

Examples:

"customer is not interested in credit card"
→ "credit card"

"customer does not require ME and QR"
→ "ME, QR"

If no product is explicitly rejected:
→ null

--------------------------------------------------

6. customer_intent

Choose the PRIMARY intent.

Allowed values:

- product_interest
- product_rejection
- follow_up
- information_request
- service_issue
- general_interaction
- unclear

Priority:

A. product_interest
Use when customer shows clear interest in a product.

B. product_rejection
Use when customer clearly rejects a product.

C. service_issue
Use when customer reports a problem with an existing
banking service/product.

D. information_request
Use when customer asks for information but does not show
clear product interest.

E. follow_up
Use when the primary intent is a future callback/action
and there is no stronger product intent.

F. general_interaction
Use for normal interaction without a specific intent.

G. unclear
Use when intent cannot reasonably be determined.

IMPORTANT:
If the customer shows product interest AND requests a follow-up,
use "product_interest".

--------------------------------------------------

7. follow_up_action

Describe the specific future action.

Examples:

"Call customer tomorrow"
→ "Call the customer tomorrow"

"customer will do next week"
→ "Customer will complete the activity next week"

If there is no follow-up:
→ null

--------------------------------------------------

8. confidence

Return a number between 0 and 1.

Use lower confidence when:

- interaction is extremely short
- intent is ambiguous
- grammar makes interpretation uncertain

Use higher confidence when customer intent is explicit.

==================================================
CRITICAL INTERPRETATION RULES
==================================================

RULE 1:
Do not confuse salesperson activity with customer interest.

Example:

"discussed credit card with customer"

This alone does NOT mean:
interest_shown = true

--------------------------------------------------

RULE 2:
Activation or existing usage is not necessarily new interest.

Example:

"customer already uses mobile banking"

This does NOT mean:
interested_product = mobile banking

--------------------------------------------------

RULE 3:
"No requirement", "not required", "does not require",
"not interested", "will not take", etc. indicate rejection
when a product is identifiable.

Example:

"customer does not require ME"

→ interest_shown = false
→ not_interested_product = "ME"

--------------------------------------------------

RULE 4:
Handle common abbreviations using context.

Examples:

NB = Net Banking
MB = Mobile Banking
ME = Merchant Enrollment
QR = QR / merchant QR
CC = Credit Card

Do not expand an abbreviation if doing so would introduce
uncertainty.

--------------------------------------------------

RULE 5:
If the text only says:

"Discussed."

return:

sentiment = neutral
follow_up_required = false
interest_shown = null
interested_product = null
not_interested_product = null
customer_intent = unclear
follow_up_action = null
confidence should be low

--------------------------------------------------

RULE 6:
If multiple products are mentioned, separate clear interest
from clear rejection.

==================================================

INTERACTION TO ANALYZE:

{interaction_text}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise banking NLP extraction system. "
                        "Return valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM returned invalid JSON: {content}"
            ) from exc

        validated_result = NLPAnalysis.model_validate(result)

        return validated_result.model_dump()