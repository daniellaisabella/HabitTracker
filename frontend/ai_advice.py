import os
import requests
import streamlit as st


#denne cacher i 24 timer, undgå unøde kald hver gang streamlit rerunner ved itneraktion
#den rerunner hvis der sker ændringer i rates dict (chacher baseret på input) 
@st.cache_data(ttl=86400)
def get_ai_advice(rates: dict) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return "No API key configured."

    habit_summary = "\n".join(
        #producer en string med name: days/7days (rate%) for hver habit i rates dict
        f"- {name}: {round(rate / 100 * 7)}/7 days ({rate}%)"
        # som iterere over items i rates dict med name og rate
        for name, rate in rates.items()
    )

    #prompt som sendes til post requests til api 
    prompt = f"""You are a habit coach. Based on the user's stats from last week / last 7 days:
            {habit_summary}

        Give short, personal advice (2 sentences) about what the user should focus on next week. Be encouraging but honest.
        \n\n\n end with a short motivational quote \n end with a relevant emoji and authors name, NEVER unknown author """

    # post request til mistral med api ket fra .env og format json fordi det er standard http format til llm 
    # post requestet returnerer data som jeg gemer i variablen response
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    # http response formaterer jeg fra json til python dict 
    data = response.json()
    if "choices" not in data:
        raise RuntimeError(data.get("message", "Unknown error"))
    # retunerer første svar (choices) og message content (content er en type under message)
    return data["choices"][0]["message"]["content"]
