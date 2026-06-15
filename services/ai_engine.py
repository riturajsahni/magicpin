async def generate(user_prompt: str, max_tokens: int = 300) -> str:
    prompt = user_prompt.lower()

    if "review" in prompt:
        return (
            "Hi Dr. Meera! Clinics with more reviews often attract more bookings. "
            "Consider asking satisfied patients for feedback after every visit."
        )

    if "festival" in prompt:
        return (
            "Festival season is a great opportunity to boost sales. "
            "Consider creating a festive combo offer and promoting it on WhatsApp."
        )

    if "cost" in prompt or "pricing" in prompt:
        return (
            "The cost depends on the campaign strategy you choose. "
            "I can help identify the most effective option."
        )

    return (
        "I can help improve reviews, customer engagement, and business growth."
    )
