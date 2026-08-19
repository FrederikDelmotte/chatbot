import google.generativeai as genai
import streamlit as st

st.title("💬 PZ VA Chatbot")
st.caption(
    "Via deze chatbot kan u ondersteuning vinden voor het nieuwe"
    " strafwetboek. Stel uw vraag zonder het vermelden van persoonsgegevens."
    " Succes!"
)

# 1. Haal de API key op uit Secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

system_instruction = (
    "Je bent een assistent voor politie-inspecteurs van de PZ VA. "
    "Beantwoord vragen professioneel, helder en juridisch correct op basis van"
    " het nieuwe strafwetboek."
)


# 2. Zoek automatisch naar een actief model op jouw account om 404-fouten te voorkomen
@st.cache_resource
def load_model():
  available_models = [
      m.name
      for m in genai.list_models()
      if "generateContent" in m.supported_generation_methods
  ]
  # Zoek bij voorkeur een flash model, anders pak de eerste beschikbare
  chosen_model = next(
      (m for m in available_models if "flash" in m), available_models[0]
  )
  return genai.GenerativeModel(
      model_name=chosen_model, system_instruction=system_instruction
  )


model = load_model()

# 3. Chat-interface
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
