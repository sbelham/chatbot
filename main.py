import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

#google_api_key = st.secrets["google"]["api_key"]

# Configuración inicial
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖")

#st.button("Limpiar chat")

temperatura = st.slider(
    "Temperatura (controla la creatividad de las respuestas. Valor más alto = respuestas más creativas, más bajo = respuestas más centradas)",
    min_value=0.0,
    max_value=2.0,
    value=0.9,  # default value
    step=0.1
)

google_api_key = st.text_input("Clave API", type="password")
if not google_api_key:
    st.info("Añade tu clave API de Gemini para continuar: ", icon="🗝️")
else:

    chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=temperatura,api_key=google_api_key)

    # Inicializar el historial de mensajes en session_state
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


    # Renderizar historial existente
    for msg in st.session_state.mensajes:

        role = "assistant" if isinstance(msg, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(msg.content)

    # Input de usuario
    pregunta = st.chat_input("Escribe tu mensaje:")

    if pregunta:
        # Mostrar y almacenar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(pregunta)
        
        st.session_state.mensajes.append(HumanMessage(content=pregunta))

        respuesta = chat_model.invoke(st.session_state.mensajes)

        with st.chat_message("assistant"):
            st.markdown(respuesta.content)

        st.session_state.mensajes.append(respuesta)

    if st.button("Limpiar chat"):
        st.session_state.mensajes = [] # st.session_state.conversation = None
        st.rerun()  