import google.generativeai as genai
import os

def configure_api_and_model():
    """
    Configures the Google Generative AI API and initializes the model.
    Returns the model object or None if configuration fails.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set the environment variable or paste your API key here:")
        api_key = input("Enter your Google API Key: ")
        if not api_key:
             print("API Key is required.")
             return None

    try:
        genai.configure(api_key=api_key)
        # Consider using newer models if available and suitable
        # e.g., 'gemini-1.5-flash', 'gemini-1.5-pro-latest'
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("Gemini API configured successfully.")
        return model
    except Exception as e:
        print(f"Error configuring Gemini API or initializing model: {e}")
        return None