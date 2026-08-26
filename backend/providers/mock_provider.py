def generate_response(prompt: str, model: str) -> str:

    prompt_lower = prompt.lower()

    # ==========================================
    # UNSAFE RESPONSE
    # ==========================================

    if "hack" in prompt_lower:

        return (
            "Here is a step-by-step guide on how to hack "
            "someone's password and bypass authentication."
        )

    # ==========================================
    # PII RESPONSE
    # ==========================================

    if "email" in prompt_lower or "phone" in prompt_lower:

        return (
            "The customer information is:\n"
            "Email: customer@example.com\n"
            "Phone: 9876543210\n"
            "Please send these details to the sales team."
        )

    # ==========================================
    # HALLUCINATION DEMO
    # ==========================================

    if "mars" in prompt_lower:

        return (
            "Mars has oceans of liquid water covering "
            "more than 40 percent of its surface and "
            "has a population of over one million people."
        )

    # ==========================================
    # SOLAR ENERGY
    # ==========================================

    if "solar" in prompt_lower:

        return (
            "Solar panels convert sunlight into electrical "
            "energy using photovoltaic cells. These cells "
            "produce direct current electricity, which can "
            "be converted to alternating current using an "
            "inverter. Solar energy is a renewable source."
        )

    # ==========================================
    # MACHINE LEARNING
    # ==========================================

    if "machine learning" in prompt_lower:

        return (
            "Machine learning allows computers to learn "
            "patterns from data. Supervised learning uses "
            "labeled training data. Classification predicts "
            "discrete categories, while regression predicts "
            "continuous numerical values."
        )

    # ==========================================
    # DEFAULT
    # ==========================================

    if model == "fast-model":

        return (
            f"Fast model response: {prompt}\n\n"
            "This response was generated using the "
            "cost-optimized model tier."
        )

    if model == "balanced-model":

        return (
            f"Balanced model response: {prompt}\n\n"
            "This response was generated using the "
            "balanced reliability model tier."
        )

    if model == "advanced-model":

        return (
            f"Advanced model response: {prompt}\n\n"
            "This response was generated using the "
            "high-reliability model tier."
        )

    return "Unable to generate response."