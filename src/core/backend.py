def risk_assessment(symptoms, pregnancy_week):
    """
    Simple triage logic for demo.
    """
    risk_level = "Low"
    action = "Self-care guidance"

    concerning = ["headache", "swelling", "bleeding", "blurred vision", "abdominal pain"]

    if any(s in symptoms.lower() for s in concerning):
        if "headache" in symptoms.lower() and "swelling" in symptoms.lower():
            risk_level = "High"
            action = "Urgent medical referral"
        else:
            risk_level = "Moderate"
            action = "Volunteer follow-up"

    return risk_level, action
