import streamlit as st
import ollama

# 1. Setup the UI page
st.title("My Local LLM Chat 🧠")
st.caption("Powered by Llama 3 and Streamlit")

# 2. Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle new user input
if prompt := st.chat_input("What's on your mind?"):
    # Show user message in UI
    st.chat_message("user").markdown(prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5. Get the LLM response
    with st.chat_message("assistant"):
        # We use a placeholder to stream the text as it generates
        message_placeholder = st.empty()
        full_response = ""
        
        # Call the local Ollama engine
        for chunk in ollama.chat(
            model='llama3',
            messages=st.session_state.messages,
            stream=True
        ):
            # Add the new chunk of text to the full response
            full_response += chunk['message']['content']
            message_placeholder.markdown(full_response + "▌")
            
        # Finalize the response text (remove the blinking cursor)
        message_placeholder.markdown(full_response)
        
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})