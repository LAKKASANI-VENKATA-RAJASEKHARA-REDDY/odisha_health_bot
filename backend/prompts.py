def build_gemini_prompt(user_query, context_data):
    """
    Build a contextual prompt for Gemini API using database info
    """
    prompt = f"""
You are an AI healthcare assistant for Odisha, India. Use the following data to answer queries accurately:
{context_data}

User question: {user_query}

Answer the question clearly and accurately. Keep responses concise.
"""
    return prompt
