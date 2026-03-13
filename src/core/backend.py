def risk_assessment(symptoms: str, pregnancy_week: int = 30) -> tuple[str, str]:
    """
    Triage logic for maternal symptom risk assessment.
    Returns (risk_level, recommended_action).
    """
    symptoms_lower = symptoms.lower()
    risk_level = "Low"
    action = "Self-care guidance"

    HIGH_RISK_COMBOS = [
        ({"headache", "swelling"}, "Possible pre-eclampsia — Urgent medical referral"),
        ({"blurred vision", "headache"}, "Possible pre-eclampsia — Urgent medical referral"),
        ({"bleeding", "abdominal pain"}, "Possible placental issue — Urgent medical referral"),
        ({"fever", "bleeding"}, "Possible infection — Urgent medical referral"),
    ]

    MODERATE_KEYWORDS = [
        "headache", "swelling", "bleeding", "blurred vision",
        "abdominal pain", "cramping", "fever", "vomiting",
        "dizziness", "chest pain", "shortness of breath",
    ]

    HIGH_KEYWORDS = [
        "severe bleeding", "heavy bleeding", "unconscious",
        "can't breathe", "cannot breathe", "fits", "seizure",
        "baby not moving", "no movement",
    ]

    # Check high-risk single keywords
    if any(kw in symptoms_lower for kw in HIGH_KEYWORDS):
        return "High", "Urgent medical referral — call emergency services"

    # Check high-risk combinations
    for keyword_set, action_text in HIGH_RISK_COMBOS:
        if all(kw in symptoms_lower for kw in keyword_set):
            return "High", action_text

    # Check moderate keywords
    if any(kw in symptoms_lower for kw in MODERATE_KEYWORDS):
        risk_level = "Moderate"
        action = "Volunteer follow-up recommended"

        # Escalate based on trimester
        if pregnancy_week >= 37 and any(kw in symptoms_lower for kw in ["bleeding", "cramping", "abdominal pain"]):
            risk_level = "High"
            action = "Urgent medical referral — near term with concerning symptoms"

    return risk_level, action
