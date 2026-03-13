def process_question(question, qa_chain):
    predefined_answers = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! What can I do for you?",
        "hey": "Hey! How can I help you?",
        "good morning": "Good morning! How can I assist you?",
        "good afternoon": "Good afternoon! What can I help you with?",
        "good evening": "Good evening! How can I assist you?"
    }

    question_lower = question.lower()
    if question_lower in predefined_answers:
        return predefined_answers[question_lower]

    res = qa_chain.invoke(question)
    answer_text = res["result"]
    sources = res.get("source_documents", [])

    if sources:
        pages = [str(doc.metadata.get("page", "Unknown")) for doc in sources]
        page_info = f"(Found on page(s): {', '.join(pages)})"
        return f"{answer_text}\n\n{page_info}"
    else:
        return f"""Dear HR Team,

I was reviewing the HR Policy document but could not locate information regarding: "{question}".

Could you please provide clarification or direct me to the relevant section?

Thank you,
[Your Name]"""
