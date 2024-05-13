from openai import OpenAI
import streamlit as st
from src import auth
import os

authenticator = auth.StreamlitGoogleAuth(
    secret_credentials_path=os.environ.get('GOOGLE_CREDENTIALS'),
    cookie_name='my_cookie_name',
    cookie_key='this_is_secret',
    redirect_uri='https://glorious-dollop-4pg6r966rxqfj7v-8501.app.github.dev',
)
authenticator.check_authentification()
authenticator.login()
# Display the user information and logout button if the user is authenticated
if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write(f"Hello, {st.session_state['user_info'].get('name')}")
    st.write(f"Your email is {st.session_state['user_info'].get('email')}")
    if st.button('Log out'):
        authenticator.logout()

with st.sidebar:
    openai_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get a Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)"
    "[![Open in GitHub Codespaces](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/burhanuddin6)"
    # Message from the developer
    st.markdown("""🚀 **Google Workspace Taskbot**
                is a chatbot that helps you manage your tasks in Google Workspace.\
                The chatbot uses ReAct prompting technique (Few Shot Classification)\
                to enable the chatbot to understand and perform complex tasks. \
                One example of a task that the chatbot can send emails on your \
                behalf. It includes a combination of data extraction from your Gmail \
                in order to understand the context and user consent by asking for \
                confirmation before performing any irreversible actions.\
                
                Currently, the app has is not verified by Google, due to which users \
                will face issues while trying to authenticate. I am trying to get the app \
                verified so that its use can be demonstrated.\
                """)
    

st.title("🏃 Google Workspace Taskbot")
st.caption("🚀 powered by Gemini")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
