import streamlit as st
import openai
import base64


openai.api_key = st.secrets['OPENAI_API_KEY']
st.session_state["model"] = st.secrets['OPENAI_FINETUNED_MODEL']
st.session_state["assistant_id"] = st.secrets['OPENAI_ASSISTANT_KEY']
st.title("HuggingMind Bot")


    
            
client = openai.OpenAI(
        api_key=openai.api_key,
    )

# Function to convert image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


with st.sidebar:
    img_path = "./assets/HuggingMind.svg"  
    img_base64 = img_to_base64(img_path)
    st.markdown(
        f'<img src="data:image/svg+xml;base64,{img_base64}" style="width:100%; height:auto;">',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("""\nHuggingMind is an AI-driven mental health chatbot provides university 
students with 24/7 personalized support and immediate access to professional guidance, utilizing 
advanced language models and university-specific mental health resources.
""")
 

# INITIAL_MESSAGE = {
#         "role": "assistant",
#         "content": "Hey there, I'm Mental Health Chatbot! How can I help you today?",
#     }
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    # st.session_state.messages.append(INITIAL_MESSAGE)

for message in st.session_state.messages:
    print(message)
    with st.chat_message(message['role']):
        st.markdown(message["content"])

thread = client.beta.threads.create()
def submit_chat(user_input):
    
    message_format = {"role": "user", "content": user_input}
    st.session_state.messages.append(message_format)
    with st.chat_message("user",avatar='./assets/user_icon.png'):
        st.markdown(user_input)

    message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
            )

    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=st.session_state["assistant_id"]
    ) as stream:
        assistant_response = st.chat_message("assistant", avatar='./assets/huggingmind_chat_icon.png').empty()
        full_response = ""
        for event in stream:
        # Print the text from text delta events
            if event.event == "thread.message.delta" and event.data.delta.content:
                full_response += event.data.delta.content[0].text.value
                assistant_response.write(full_response)
                # st.chat_message("assistant").write(response_container)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def main():
    if prompt := st.chat_input("Have a conversation with me :)"):
        submit_chat(prompt)
        # display_chat_history()

main()
