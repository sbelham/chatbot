import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import SystemMessage
from utils import *

#google_api_key = st.secrets["google"]["api_key"]

# Configuración inicial
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖")

with st.sidebar:
    modelo = st.selectbox(
        "Selecciona el modelo de Gemini (para respuestas más rápidas, usa gemini-2.5-flash-lite)",
        ("gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"),
    )
    st.write("Modelo seleccionado:", modelo)

    modo = st.selectbox(
        "Modo de respuesta",
        ("Normal","Formal","Modo profesor","Chistoso","Poético")
    )

    temperatura = st.slider(
        "Temperatura (controla la creatividad de las respuestas. Valor más alto = respuestas más creativas, más bajo = respuestas más centradas)",
        min_value=0.0,
        max_value=2.0,
        value=0.9,  # default value
        step=0.1
    )
    top_k = st.slider(
        "Top K (selecciona las palabras con las probabilidades más altas para ser la siguiente palabra. 0 = valor por defecto del modelo)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,  # default value
        step=1.0
    )
    top_p = st.slider(
        "Top P (un valor bajo selecciona solo las palabras más probables, mientras que un valor alto permite mayor variabilidad. 0 = valor por defecto del modelo)",
        min_value=0.0,
        max_value=1.0,
        value=0.0,  # default value
        step=0.01
    )
    max_tokens = st.slider(
        "Tokens máximos (número máximo de tokens para cada respuesta. 0 = valor por defecto del modelo)",
        min_value=0.0,
        max_value=1000.0,
        value=0.0,  # default value
        step=1.0
    )

    top_k_param = None if top_k == 0 else top_k
    top_p_param = None if top_p == 0.0 else top_p
    max_tokens_param = None if max_tokens == 0.0 else max_tokens

prompt_modo = modo_a_prompt(modo)

# Store/update system message
if "system_message" not in st.session_state:
    st.session_state.system_message = SystemMessage(content=prompt_modo)
else:
    st.session_state.system_message.content = prompt_modo

google_api_key = st.text_input("Clave API", type="password")
if not google_api_key:
    st.info("Añade tu clave API de Gemini para continuar ", icon="🗝️")
else:

    chat_model = ChatGoogleGenerativeAI(model=modelo,temperature=temperatura,api_key=google_api_key,
                                        top_k=top_k_param,top_p=top_p_param,max_output_tokens=max_tokens_param,
                                        streaming=True)

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

        mensajes_para_gemini = [
            st.session_state.system_message, 
            *st.session_state.mensajes        
        ]

        with st.chat_message("assistant"):
            streamed_text = st.write_stream(
                chat_model.stream(mensajes_para_gemini)
            )

        st.session_state.mensajes.append(AIMessage(content=streamed_text))

    if st.button("Limpiar chat"): #Limpia el chat y los mensajes guardados en sesion
        st.session_state.mensajes = [] # st.session_state.conversation = None
        st.rerun()