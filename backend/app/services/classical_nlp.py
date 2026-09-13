import re
from typing import Optional


class ClassicalNLPAnalyzer:
    """
    Traditional NLP analyzer for banking sales interactions.

    This implementation uses:
    - Text normalization
    - Pattern matching
    - Negation detection
    - Domain product/entity extraction
    - Rule-based intent classification

    No LLM or external API is used.
    """

    # ============================================================
    # PRODUCT VOCABULARY
    # ============================================================

    PRODUCT_ALIASES = {
        "Personal Loan": [
            "personal loan",
            "personal loans",
        ],
        "Business Loan": [
            "business loan",
            "business loans",
        ],
        "LAP Loan": [
            "lap loan",
            "lap",
        ],
        "Business Credit Card": [
            "business credit card",
            "business credit cards",
        ],
        "Credit Card": [
            "credit card",
            "credit cards",
        ],
        "CASA": [
            "casa",
        ],
        "FD": [
            "fixed deposit",
            "fd",
        ],
        "QR": [
            "qr code",
            "qr",
        ],
        "POS": [
            "pos",
        ],
        "Net Banking": [
            "net banking",
            "netbanking",
        ],
        "Mobile Banking": [
            "mobile banking",
            "mobile banking application",
        ],
        "ME": [
            "me enrollment",
            "merchant enrollment",
        ],
        "GST Payments": [
            "gst payment",
            "gst payments",
        ],
        "CBDT Payments": [
            "cbdt payment",
            "cbdt payments",
        ],
        "Debit Card": [
            "debit card",
            "debit cards",
        ],
        "Debit Transactions": [
            "debit transaction",
            "debit transactions",
        ],
        "Soundbox": [
            "soundbox",
        ],
        "SmartHub Vyapar": [
            "smarthub vyapar",
            "smart hub vyapar",
        ],
    }

    # ============================================================
    # POSITIVE CUSTOMER INTENT
    # ============================================================

    POSITIVE_PATTERNS = [
        "customer is interested",
        "customer interested",
        "interested in",
        "customer wants",
        "customer wanted",
        "customer would like",
        "customer asked for",
        "customer requested",
        "customer needs",
        "customer requires",
        "customer will take",
        "customer will opt",
        "customer will do",
        "customer will proceed",
        "customer agreed",
        "customer agreed to",
        "customer opted",
        "customer proceeding",
        "customer is proceeding",
        "he will do",
        "he'll do",
        "he wants",
        "he wanted",
        "he agreed",
        "he'll take",
        "he will take",
        "will take",
        "will opt",
        "will do",
        "will proceed",
        "proceeding",
        "proceed with",
        "interested",
    ]

    # ============================================================
    # NEGATIVE / REJECTION PATTERNS
    # ============================================================

    NEGATIVE_PATTERNS = [
        "not interested",
        "no interest",
        "not required",
        "no requirement",
        "no requirements",
        "does not require",
        "doesn't require",
        "do not require",
        "don't require",
        "did not require",
        "no need",
        "no needs",
        "not need",
        "does not need",
        "doesn't need",
        "do not need",
        "don't need",
        "did not need",
        "will not take",
        "will not opt",
        "will not proceed",
        "not want",
        "don't want",
        "doesn't want",
        "did not want",
        "refused",
        "rejected",
        "declined",
        "no requirement for",
    ]

    # ============================================================
    # CUSTOMER-REQUESTED FOLLOW-UP
    # ============================================================

    # IMPORTANT:
    # A generic "follow up" written by the salesperson is NOT
    # considered a customer-requested follow-up.
    FOLLOW_UP_PATTERNS = [
        r"customer .*asked .*call",
        r"customer .*ask .*call",
        r"customer .*requested .*call",
        r"customer .*request .*callback",
        r"customer .*asked .*callback",
        r"customer .*said .*call",
        r"customer .*told .*call",
        r"customer .*contact .*later",
        r"customer .*call .*tomorrow",
        r"customer .*call .*next week",
        r"customer .*call .*later",
        r"customer .*asked .*contact",
        r"customer .*requested .*contact",
        r"call me",
        r"contact me",
    ]

    # ============================================================
    # SERVICE ISSUE PATTERNS
    # ============================================================

    SERVICE_ISSUE_PATTERNS = [
        "issue",
        "problem",
        "error",
        "not working",
        "unable to",
        "unable",
        "failed",
        "failure",
        "complaint",
        "transaction failed",
        "payment failed",
        "login failed",
        "unable to login",
        "unable to transact",
        "transaction issue",
        "payment issue",
        "account issue",
        "service issue",
    ]

    # ============================================================
    # TEXT NORMALIZATION
    # ============================================================

    def normalize(self, text: str) -> str:
        """
        Normalize noisy interaction text.

        Examples:
        - Converts text to lowercase
        - Removes punctuation
        - Removes repeated whitespace
        """

        text = str(text).lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        return text

    # ============================================================
    # PRODUCT EXTRACTION
    # ============================================================

    def extract_products(self, text: str) -> list[str]:
        """
        Extract banking products explicitly mentioned
        in the interaction.

        Longer product names are checked first.
        """

        text = self.normalize(text)

        found = []

        aliases = []

        for product, variations in self.PRODUCT_ALIASES.items():

            for variation in variations:

                aliases.append(
                    (
                        variation,
                        product,
                    )
                )

        # Check longer phrases first.
        aliases.sort(
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for variation, product in aliases:

            pattern = (
                rf"\b{re.escape(variation)}\b"
            )

            if re.search(
                pattern,
                text,
            ):

                # Prevent generic Credit Card from being
                # extracted when Business Credit Card exists.
                if (
                    product == "Credit Card"
                    and "Business Credit Card" in found
                ):
                    continue

                if product not in found:
                    found.append(product)

        return found

    # ============================================================
    # FOLLOW-UP DETECTION
    # ============================================================

    def detect_follow_up(
        self,
        text: str,
    ) -> tuple[bool, Optional[str]]:
        """
        Detect only explicit customer-requested follow-up.
        """

        normalized = self.normalize(text)

        for pattern in self.FOLLOW_UP_PATTERNS:

            if re.search(
                pattern,
                normalized,
            ):

                return (
                    True,
                    self._build_follow_up_action(
                        normalized
                    ),
                )

        return False, None

    # ============================================================
    # FOLLOW-UP ACTION
    # ============================================================

    def _build_follow_up_action(
        self,
        text: str,
    ) -> str:
        """
        Build a simple human-readable follow-up action.
        """

        if "tomorrow" in text:
            return "Call the customer tomorrow"

        if "next week" in text:
            return "Call the customer next week"

        if "later" in text:
            return "Contact the customer later"

        if "callback" in text:
            return "Call the customer back"

        if "call" in text:
            return "Call the customer"

        if "contact" in text:
            return "Contact the customer"

        return "Follow up with the customer"

    # ============================================================
    # REJECTION DETECTION
    # ============================================================

    def detect_rejection(
        self,
        text: str,
    ) -> bool:
        """
        Detect explicit rejection / lack of requirement.
        """

        normalized = self.normalize(text)

        return any(
            pattern in normalized
            for pattern in self.NEGATIVE_PATTERNS
        )

    # ============================================================
    # INTEREST DETECTION
    # ============================================================

    def detect_interest(
        self,
        text: str,
    ) -> bool:
        """
        Detect explicit customer interest.

        Rejection takes priority over positive patterns.
        """

        normalized = self.normalize(text)

        # Rejection always wins.
        if self.detect_rejection(
            normalized
        ):
            return False

        return any(
            pattern in normalized
            for pattern in self.POSITIVE_PATTERNS
        )

    # ============================================================
    # REJECTED PRODUCT EXTRACTION
    # ============================================================

    def extract_rejected_products(
        self,
        text: str,
    ) -> list[str]:
        """
        Identify products explicitly rejected
        by the customer.
        """

        normalized = self.normalize(text)

        rejected = []

        products = self.extract_products(
            normalized
        )

        rejection_phrases = [
            "not interested in",
            "not required",
            "no requirement",
            "no requirements",
            "does not require",
            "doesn't require",
            "do not require",
            "don't require",
            "did not require",
            "no need",
            "does not need",
            "doesn't need",
            "do not need",
            "don't need",
            "did not need",
            "not want",
            "don't want",
            "doesn't want",
            "did not want",
            "will not take",
            "will not opt",
        ]

        for product in products:

            aliases = self.PRODUCT_ALIASES[
                product
            ]

            for alias in aliases:

                for rejection in rejection_phrases:

                    pattern = (
                        rf"\b{re.escape(rejection)}\b"
                        rf".{{0,50}}"
                        rf"\b{re.escape(alias)}\b"
                    )

                    if re.search(
                        pattern,
                        normalized,
                    ):

                        rejected.append(
                            product
                        )

                        break

                if product in rejected:
                    break

        return list(
            dict.fromkeys(
                rejected
            )
        )

    # ============================================================
    # SENTIMENT
    # ============================================================

    def sentiment(
        self,
        text: str,
    ) -> str:
        """
        Basic domain sentiment classification.

        This is intentionally conservative.
        """

        normalized = self.normalize(text)

        if self.detect_rejection(
            normalized
        ):
            return "negative"

        positive_patterns = [
            "interested",
            "happy",
            "satisfied",
            "good",
            "agree",
            "agreed",
            "proceed",
            "proceeding",
            "will do",
            "would like",
        ]

        if any(
            pattern in normalized
            for pattern in positive_patterns
        ):
            return "positive"

        return "neutral"

    # ============================================================
    # MAIN ANALYSIS
    # ============================================================

    def analyze(
        self,
        text: str,
    ) -> dict:
        """
        Analyze one salesperson-customer interaction.
        """

        normalized = self.normalize(text)

        products = self.extract_products(
            normalized
        )

        (
            follow_up_required,
            follow_up_action,
        ) = self.detect_follow_up(
            normalized
        )

        rejected_products = (
            self.extract_rejected_products(
                normalized
            )
        )

        # ========================================================
        # 1. PRODUCT REJECTION
        # ========================================================

        if rejected_products:

            interest_shown = False

            interested_product = None

            not_interested_product = (
                ", ".join(
                    rejected_products
                )
            )

            customer_intent = (
                "product_rejection"
            )

        # ========================================================
        # 2. PRODUCT INTEREST
        # ========================================================

        elif (
            self.detect_interest(
                normalized
            )
            and products
        ):

            interest_shown = True

            interested_product = (
                ", ".join(
                    products
                )
            )

            not_interested_product = None

            customer_intent = (
                "product_interest"
            )

        # ========================================================
        # 3. CUSTOMER REQUESTED FOLLOW-UP
        # ========================================================

        elif follow_up_required:

            interest_shown = None

            interested_product = None

            not_interested_product = None

            customer_intent = (
                "follow_up"
            )

        # ========================================================
        # 4. SERVICE ISSUE
        # ========================================================

        elif any(
            pattern in normalized
            for pattern in self.SERVICE_ISSUE_PATTERNS
        ):

            interest_shown = None

            interested_product = None

            not_interested_product = None

            customer_intent = (
                "service_issue"
            )

        # ========================================================
        # 5. UNCLEAR
        # ========================================================

        else:

            interest_shown = None

            interested_product = None

            not_interested_product = None

            customer_intent = (
                "unclear"
            )

        return {
            "sentiment": self.sentiment(
                normalized
            ),
            "follow_up_required": (
                follow_up_required
            ),
            "interest_shown": (
                interest_shown
            ),
            "interested_product": (
                interested_product
            ),
            "not_interested_product": (
                not_interested_product
            ),
            "customer_intent": (
                customer_intent
            ),
            "follow_up_action": (
                follow_up_action
            ),
        }