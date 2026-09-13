# Sales Interaction Intelligence

A traditional NLP-based system for analyzing salesperson-customer interactions in the banking domain.

The system extracts customer sentiment, follow-up requirements, product interest/rejection, and customer intent from unstructured sales interaction notes.

---

## Problem Statement

Sales teams generate a large number of customer interaction notes containing information about:

- Customer interest
- Product requirements
- Product rejection
- Follow-up requests
- Service issues
- Banking product discussions

These interactions are often written as short, noisy, and inconsistent text containing spelling mistakes, abbreviations, incomplete sentences, and banking terminology.

The objective of this project is to automatically convert these unstructured interaction notes into structured information using traditional NLP techniques.

---

## Objectives

The system focuses on five primary requirements:

1. Identify customer sentiment
2. Identify whether the customer requested a follow-up
3. Identify whether the customer showed interest
4. Identify the product the customer is interested in
5. Identify the product the customer is not interested in

Additional customer intent classification is also performed.

---

## NLP Pipeline

```text
Sales Interaction
       │
       ▼
Text Normalization
       │
       ▼
Domain Product Extraction
       │
       ▼
Negation / Rejection Detection
       │
       ▼
Intent Pattern Detection
       │
       ├───────────────┐
       ▼               ▼
 Sentiment        Follow-up
       │               │
       └───────┬───────┘
               ▼
       Structured Output