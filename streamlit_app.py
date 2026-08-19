import google.generativeai as genai
import streamlit as st

st.title("💬 PZ VA Chatbot")
st.caption(
    "Via deze chatbot kan u ondersteuning vinden voor het nieuwe"
    " strafwetboek. Stel uw vraag zonder het vermelden van persoonsgegevens."
)

# 1. API Key ophalen
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
  st.error(
      "❌ Geen API key gevonden in Streamlit Secrets! Voeg 'GEMINI_API_KEY' toe."
  )
  st.stop()

genai.configure(api_key=api_key)

# 2. Model initialiseren met expliciet pad
system_instruction = (
    "Je bent een assistent voor politie-inspecteurs van de PZ VA. "
    "Beantwoord vragen professioneel, helder en juridisch correct op basis van"
    " het nieuwe strafwetboek."
)

try:
  model = genai.GenerativeModel(
      model_name="models/gemini-2.5-flash",
      system_instruction=system_instruction,
  )
except Exception as e:
  st.error(f"Fout bij laden van het model: {e}")
  st.stop()

# 3. Chatgeschiedenis
if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# 4. Invoer en antwoord
if prompt := st.chat_input("Stel uw vraag over het strafwetboek..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  try:
    response = model.generate_content(prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )
    with st.chat_message("assistant"):
      st.markdown(response.text)
  except Exception as e:
    st.error(
        "Er is een probleem met de verbinding naar de Gemini API. Controleer"
        " of je API Key actief is in Google AI Studio."
    )
    st.caption(f"Details: {e}")
