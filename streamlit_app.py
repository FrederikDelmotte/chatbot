import google.generativeai as genai
import streamlit as st

st.title("💬 PZ VA Chatbot")
st.caption(
    "Via deze chatbot kan u ondersteuning vinden voor het nieuwe"
    " strafwetboek. Stel uw vraag zonder het vermelden van persoonsgegevens."
    " Succes!"
)

# Haal de API key op uit Secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

system_instruction = (
    "Je bent een assistent voor politie-inspecteurs van de PZ VA. "
    "Beantwoord vragen professioneel, helder en juridisch correct op basis van"
    " het nieuwe strafwetboek."
)

# Gebruik gemini-1.5-flash-latest (of gemini-2.0-flash) om 404 te voorkomen
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", system_instruction=system_instruction
)

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("Stel uw vraag over het strafwetboek..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  response = model.generate_content(prompt)
  st.session_state.messages.append(
      {"role": "assistant", "content": response.text}
  )
  with st.chat_message("assistant"):
    st.markdown(response.text)
