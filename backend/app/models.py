from typing import Literal, Optional

from pydantic import BaseModel, Field


class NLPAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]

    follow_up_required: bool

    interest_shown: Optional[bool] = None

    interested_product: Optional[str] = None

    not_interested_product: Optional[str] = None

    customer_intent: Literal[
        "product_interest",
        "product_rejection",
        "follow_up",
        "information_request",
        "service_issue",
        "general_interaction",
        "unclear",
    ]

    follow_up_action: Optional[str] = None

    confidence: float = Field(ge=0.0, le=1.0)