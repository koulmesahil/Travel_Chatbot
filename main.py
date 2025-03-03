import streamlit as st
import time
import logging
import datetime
import os
from openai import OpenAI

from travelbot import travelbot_ui
from customersupportbot import customersupportbot_ui  # Add this import


# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

def initialize_session():
    """Initialize session state variables if they don't exist"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display the chat history with timestamps"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            timestamp = message.get("timestamp", "")
            if timestamp:
                st.write(f"[{timestamp}] {message['content']}")
            else:
                st.write(message['content'])

def add_message(role, content):
    """Add a message to the chat history with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": role, "content": content, "timestamp": timestamp})

def prepare_conversation_history(max_messages=10):
    """Create a properly formatted conversation history for the API"""
    conversation_history = []
    # Reverse to get oldest first, then take only the last max_messages
    messages_subset = st.session_state.messages[-max_messages:]
    
    for msg in messages_subset:
        conversation_history.append({"role": msg["role"], "content": msg["content"]})
    
    return conversation_history

def get_openai_response(api_key, messages, model="gpt-3.5-turbo", max_tokens=500, temperature=0.7):
    """Get a response from the OpenAI API with simplified error handling"""
    try:
        # Initialize the client with the API key
        client = OpenAI(api_key=api_key)
        
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content, None
    except Exception as e:
        logging.error(f"Error with OpenAI API: {str(e)}")
        error_message = str(e)
        
        # Provide user-friendly error messages based on error text
        if "rate limit" in error_message.lower():
            return None, "Rate limit exceeded. Please try again in a moment."
        elif "authentication" in error_message.lower() or "api key" in error_message.lower():
            return None, "API key is invalid. Please check your API key."
        elif "connect" in error_message.lower():
            return None, "Cannot connect to OpenAI API. Please check your internet connection."
        else:
            return None, f"Error: {error_message}"

def simulate_typing(text, placeholder, speed=0.01):
    """Simulate typing effect for the AI response"""
    buffer_text = ""
    for word in text.split():
        buffer_text += word + " "
        placeholder.text(buffer_text)
        time.sleep(speed)

def export_chat_history():
    """Export chat history to a text file"""
    chat_history = "\n".join([f"{msg['role'].capitalize()} [{msg.get('timestamp', '')}]: {msg['content']}" 
                             for msg in st.session_state.messages])
    
    # Add timestamp to the download filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_history_{timestamp}.txt"
    
    return chat_history, filename

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.messages = []

def save_api_key():
    """Save API key to session state"""
    if "saved_api_key" not in st.session_state:
        st.session_state.saved_api_key = ""

def main():
    # Set up Streamlit page config
    st.set_page_config(page_title="Multi-Model Chatbot", layout="wide")
    
    # Initialize session
    initialize_session()
    save_api_key()
    
    # Sidebar for user options
    st.sidebar.title("Chatbot Settings")
    
    # Model selection (for future use with other models)
    model_options = ["OpenAI GPT-3.5", "OpenAI GPT-4", "OpenAI GPT-3.5-turbo-16k"] 
    selected_model = st.sidebar.selectbox("Select Language Model", model_options)
    
    # Dropdown for selecting chatbot functionality
    chatbot_options = [ "Travelbot", "Customer Support"]  # Added Meditation Bot
    selected_chatbot = st.sidebar.selectbox("Select Chatbot Functionality", chatbot_options)
    
    # Custom API Key Input with persistence
    api_key = st.sidebar.text_input("Enter API Key", value=st.session_state.saved_api_key, type="password")
    if api_key != st.session_state.saved_api_key:
        st.session_state.saved_api_key = api_key
    
    # Define temperature and max tokens with sliders for better UX
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1, 
                                   help="Higher values make output more random, lower values more deterministic")
    max_tokens = st.sidebar.slider("Max Response Length", 50, 4000, 500, 50,
                                  help="Maximum length of the AI response")
    
    # Typing speed control
    typing_speed = st.sidebar.slider("Typing Speed", 0.001, 0.05, 0.01, 0.001,
                                    help="Speed of the typing animation (lower is faster)")

    # UI Controls in sidebar
    st.sidebar.subheader("Chat Controls")
    sidebar_col1, sidebar_col2 = st.sidebar.columns(2)
    
    with sidebar_col1:
        if st.button("Clear Chat"):
            clear_chat_history()
            st.rerun()  # Using st.rerun() instead of experimental_rerun
    
    with sidebar_col2:
        # Export chat button
        chat_data, filename = export_chat_history()
        st.download_button("Export Chat", chat_data, filename)
    
    # Main chat interface
    #st.title(f"Chat with {selected_chatbot}")
     
    # Display chat history
    display_chat_history()
    
    # Modify UI vibe based on selected chatbot
    if selected_chatbot == "Travelbot":
        travelbot_ui()
    

    elif selected_chatbot == "Customer Support":
       customersupportbot_ui()
    
    # User input
    user_input = st.chat_input("Type your message...") 
    
    # Process user input
    if user_input:
        # Add and display user message
        add_message("user", user_input)
        with st.chat_message("user"):
            st.write(user_input)
        
        # Check for API key
        if not api_key:
            st.warning("Please provide an API key to use the selected model.")
            return
        
        # Show loading indicator
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("AI is thinking..."):
                # Get the model name based on selection
                if selected_model == "OpenAI GPT-3.5":
                    model_name = "gpt-3.5-turbo"
                elif selected_model == "OpenAI GPT-4":
                    model_name = "gpt-4"
                elif selected_model == "OpenAI GPT-3.5-turbo-16k":
                    model_name = "gpt-3.5-turbo-16k"
                
                # Prepare conversation history
                conversation_history = prepare_conversation_history()
                
                # Get AI response with functionality-based adjustments
                response_text, error = get_openai_response(
                    api_key, 
                    conversation_history, 
                    model_name, 
                    max_tokens, 
                    temperature
                )
                
  
                if error:
                    response_placeholder.error(error)
                else:
                    # Simulate typing effect
                    simulate_typing(response_text, response_placeholder, speed=typing_speed)
                    
                    # Add the message to history
                    add_message("assistant", response_text)


if __name__ == "__main__":
    main()
