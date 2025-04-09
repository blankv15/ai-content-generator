# ai_content_generator/src/context.py


# The function below gathers context via the command line (CLI).
# It is NOT used directly by the Streamlit app (app.py), which uses
# st.form and widgets based on the QUESTIONS dictionary above.
# Kept here for potential CLI usage or testing.
# Core questions defining the website's context.
# This dictionary is imported by the Streamlit app (app.py)
# to dynamically create the context input form.
QUESTIONS = {
    "website_name": "What is the name of the website?",
    "website_theme": "What is the central theme or main topic of this website? (Be specific!)",
    "website_purpose": "What is the primary purpose or mission of this website? What problem does it solve or what value does it offer?",
    "target_audience": "Who is the primary target audience for this website?",
    "key_offerings": "What are the main things the website offers (e.g., information, products, services, community)?",
    "unique_selling_prop": "What makes this website unique or different from others in the same niche?",
    "tone_of_voice": "What is the general tone of voice for the website's content? (e.g., professional, friendly, informative, witty, technical)",
    # --- ADDED QUESTIONS ---
    "brand_story": "Brief Brand Story / History (Optional - for About Page):",
    "call_to_action": "Default Call to Action for content (Optional - e.g., 'Visit our blog', 'Check services'):"
    # --- END ADDED QUESTIONS ---
}

# The function below gathers context via the command line (CLI).
# It is NOT used directly by the Streamlit app (app.py).
# Kept here for potential CLI usage or testing.
def gather_website_context():
    """
    Asks core questions about the website via the command line.
    Returns the answers as a dictionary. (CLI Version)
    """
    print("\nGathering core website information (CLI Mode)...")
    print("-" * 30)
    context = {}
    for key, question in QUESTIONS.items():
        # Use input() for CLI interaction
        context[key] = input(f"{question}\n> ")
        print("-" * 10)
    print("\nWebsite context gathered (CLI Mode).")
    return context

# Example of how the QUESTIONS dict might be used elsewhere:
if __name__ == '__main__':
    print("--- Example: Accessing QUESTIONS Dictionary ---")
    for key, question_text in QUESTIONS.items():
        print(f"Key: {key}, Question: {question_text}")