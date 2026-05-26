import os
import requests
import streamlit as st


@st.cache_data(ttl=600)
def get_ai_advice(rates: dict) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return "No API key configured."

    habit_summary = "\n".join(
        f"- {name}: {round(rate / 100 * 7)}/7 days ({rate}%)"
        for name, rate in rates.items()
    )

    prompt = f"""You are a habit coach. Based on the user's last 7 days:
            {habit_summary}

        Give short, personal advice (2 sentences) about what the user should focus on next week. Be encouraging but honest.
        \n\n\n end with a short motivational quote \n end with a relevant emoji and authors name, NEVER unknown author """

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    if "choices" not in data:
        raise RuntimeError(data.get("message", "Unknown error"))
    return data["choices"][0]["message"]["content"]
