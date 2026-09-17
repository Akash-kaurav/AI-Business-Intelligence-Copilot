from src.intent_router import detect_business_intent


questions = [
    "Why did revenue decline?",
    "What will tomorrow's revenue be?",
    "Which customers are at risk?",
    "Which products are business winners?",
    "What are the top categories?",
    "Which sellers are risky?",
    "Are there any data quality issues?",
    "Hello, how are you?"
]


for question in questions:

    intent = detect_business_intent(question)

    print(
        f"Question: {question}"
    )

    print(
        f"Intent: {intent}"
    )

    print("-" * 50)