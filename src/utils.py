import textwrap

# Note: No 'google.generativeai' import needed here if model object is passed in
# import google.generativeai as genai # Keep commented unless needed directly

def call_gemini_api(model, prompt):
    """
    Helper function to call the Gemini API using the provided model object
    and handles basic response/errors.
    """
    if not model:
        print("Error: AI model object not provided to call_gemini_api.")
        return None
    try:
        response = model.generate_content(prompt)
        # Basic check if text exists
        if hasattr(response, 'text') and response.text:
            return response.text
        else:
             # Check for safety ratings or blockages if applicable
            try:
                 # Check if prompt_feedback exists and has safety_ratings
                 if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
                    print(f"Generation possibly blocked or failed. Safety Ratings: {response.prompt_feedback.safety_ratings}")
                 else:
                    print("Generation failed. No text was returned, and detailed feedback unavailable.")

            except Exception as feedback_error:
                 print(f"Generation failed. No text returned. Error accessing feedback: {feedback_error}")
            return None
    except Exception as e:
        print(f"\nAn error occurred while calling the Gemini API: {e}")
        return None

def display_output(content_type, text):
    """
    Formats and prints the generated text.
    """
    print(f"\n--- Generated {content_type} ---")
    if text:
        # Format the output nicely
        formatted_text = '\n'.join(textwrap.wrap(text, width=80))
        print(formatted_text)
    else:
        print("No content was generated.")
    print(f"--- End of Generated {content_type} ---")
    print("\nReminder: AI word counts are approximate. Review the length and quality.")