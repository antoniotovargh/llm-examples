import streamlit as st
import anthropic
import ollama as ol
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import datetime
import json

def log_interaction(action, data):
    timestamp = datetime.datetime.now().isoformat()
    log = {"timestamp": timestamp, "action": action, "data": data}
    with open("user_interactions_log.json", "a") as logfile:
        logfile.write(json.dumps(log) + "\n")

def print_txt(text):
    if any("\u0600" <= c <= "\u06FF" for c in text):  # check if text contains Arabic characters
        text = f"<p style='direction: rtl; text-align: right;'>{text}</p>"
    st.markdown(text, unsafe_allow_html=True)

def print_chat_message(message):
    text = message["content"]
    if message["role"] == "user":
        with st.chat_message("user", avatar="🎙️"):
            print_txt(text)
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🦙"):
            print_txt(text)

def get_chat_history(key):
    return st.session_state.chat_history[key]

def init_chat_history(key, system_prompt):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if key not in st.session_state.chat_history:
        st.session_state.chat_history[key] = [{"role": "system", "content": system_prompt}]

def system_prompt_input(default_prompt):
    return st.sidebar.text_area("System Prompt", value=default_prompt, height=100)

def llm_selector():
    ollama_models = [m['name'] for m in ol.list()['models']]
    with st.sidebar:
        return st.selectbox("LLM", ollama_models)



st.title("💬 对话模式")


model = llm_selector()
chat_key = f"对话_chat_history_{model}"  # Unique key for each mode and model
default_prompt = "你是一位有用的助手。"

system_prompt = system_prompt_input(default_prompt)
init_chat_history(chat_key, system_prompt)
chat_history = get_chat_history(chat_key)
for message in chat_history:
    print_chat_message(message)

question = st.chat_input()

debug_mode = st.sidebar.checkbox("Debug Mode", value=True)
log_interaction("User input", {"mode": "对话", "question": question})

if question:
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {question}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    if question:
        user_message = {"role": "user", "content": question}
        # if app_mode == "语音识别":
        print_chat_message(user_message)
        chat_history.append(user_message)
        response = ol.chat(model=model, messages=chat_history)
        answer = response['message']['content']
        ai_message = {"role": "assistant", "content": answer}
        print_chat_message(ai_message)
        chat_history.append(ai_message)
        debug_info = {"messages": chat_history, "response": response}

        if debug_mode:
            st.write("Debug Info: Complete Prompt Interaction")
            st.json(debug_info)

        # truncate chat history to keep 20 messages max
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        # update chat history
        st.session_state.chat_history[chat_key] = chat_history
