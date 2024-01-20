import google.generativeai as genai
import os
import pprint
from google.generativeai import GenerationConfig

def get_model_details(model_name):
    """
    Fetches and prints details of the specified model.
    """
    model = genai.get_model(model_name)
    pprint.pprint(model)

def choose_model():
    """
    Displays a menu for model selection and returns the chosen model name.
    """
    models = {
        "1": "models/gemini-pro",
        "2": "models/gemini-pro-vision",
        "3": "models/embedding-001",
        "4": "models/aqa"
    }

    for key, value in models.items():
        print(f"{key}: {value}")

    choice = input("Choose a model number: ")
    return models.get(choice, "models/gemini-pro")  # Default to Gemini Pro

def main():
    # Configure the API key
    api_key = 'AIzaSyCzZuQ8AciAhPYiHKj3q7OqzD5S_kwFl0g'  # Replace with your actual API key
    genai.configure(api_key=api_key)

    # Model selection
    model_name = choose_model()
    get_model_details(model_name)

    # Initialize the GenerativeModel
    model = genai.GenerativeModel(model_name)

    # Generation configuration for fluid responses
    generation_config = GenerationConfig(
        temperature=0.7,       
        top_p=0.9,             
        top_k=40,              
        max_output_tokens=200, 
        stop_sequences=["\n"]  
    )

    # Start a chat session
    chat = model.start_chat()

    # Initialize chat history
    chat_history = []

    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            break

        # Send message and get response with custom configuration
        response = chat.send_message(user_message, generation_config=generation_config)
        
        print("AI:", response.text)

        # Save exchange to history
        chat_history.append({"You": user_message, "AI": response.text})

    # Save chat history to a file
    with open('chat_history.txt', 'w') as file:
        for exchange in chat_history:
            file.write(f"You: {exchange['You']}\nAI: {exchange['AI']}\n\n")

    print("Chat history saved and chat session ended.")

if __name__ == "__main__":
    main()