# Use relative import to get helper function from the same package
from .utils import call_gemini_api

def generate_about_page(website_context, model):
    """
    Generates an 'About Us' page aiming for approx 600 words,
    using the provided website context and AI model.
    """
    if not model or not website_context:
        print("Error: Model or website context is missing for About Page generation.")
        return None

    print("\nGenerating 'About Us' page (aiming for ~600 words)...")
    print("-" * 30)

    # These could also be moved to context.py if always needed,
    # but keeping here makes them specific to this generator's run.
    brand_story = input("Any brief brand story/history for the About page? (Optional, leave blank if none)\n> ")
    call_to_action = input("Specific call to action for the About page? (e.g., explore posts, contact us)\n> ")

    prompt = f"""
    Act as an expert copywriter creating a compelling 'About Us' page.
    Use the following website context and specific details:

    **Website Context:**
    * Name: {website_context.get('website_name', 'N/A')}
    * Central Theme: {website_context.get('website_theme', 'N/A')}
    * Purpose/Mission: {website_context.get('website_purpose', 'N/A')}
    * Target Audience: {website_context.get('target_audience', 'N/A')}
    * Key Offerings: {website_context.get('key_offerings', 'N/A')}
    * Uniqueness: {website_context.get('unique_selling_prop', 'N/A')}
    * General Tone: {website_context.get('tone_of_voice', 'neutral')}

    **About Page Specifics:**
    * Brand Story: {brand_story if brand_story else 'Not provided.'}
    * Call to Action: {call_to_action if call_to_action else 'Encourage exploration of the site.'}

    **Instructions:**
    1. Write a coherent and engaging 'About Us' page clearly reflecting the central theme.
    2. Strictly adhere to the general tone specified in the context.
    3. Target the specified audience.
    4. Naturally integrate the purpose, offerings, and uniqueness.
    5. Incorporate the brand story concisely if provided.
    6. Conclude with or integrate the call to action.
    7. Structure logically. Do not add information not derived from the details provided.
    8. Important: Write the content to be approximately 600 words long.
    """
    return call_gemini_api(model, prompt)


def generate_blog_post(website_context, model, topic, keywords=None):
    """
    Generates a blog post aiming for 600-800 words on a specific topic,
    using the website context and AI model.
    """
    if not model or not website_context:
        print("Error: Model or website context is missing for Blog Post generation.")
        return None
    if not topic:
        print("Error: Blog post topic is required.")
        return None

    print(f"\nGenerating Blog Post about: '{topic}' (aiming for 600-800 words)...")
    print("-" * 30)

    prompt = f"""
    Act as a knowledgeable blog writer creating an engaging post for the website '{website_context.get('website_name', 'this website')}'.

    **Website Context (Use this for relevance and tone):**
    * Central Theme: {website_context.get('website_theme', 'N/A')}
    * Target Audience: {website_context.get('target_audience', 'N/A')}
    * General Tone: {website_context.get('tone_of_voice', 'neutral')}

    **Blog Post Specifics:**
    * Topic: {topic}
    * Target Keywords (Optional): {keywords if keywords else 'Focus on the main topic naturally.'}
    * Required Word Count Range: Approximately 600 to 800 words.

    **Instructions:**
    1. Write an informative and engaging blog post specifically about '{topic}'.
    2. Ensure the content is highly relevant to the website's central theme: '{website_context.get('website_theme', 'N/A')}'.
    3. Write in a style and language appropriate for the target audience: '{website_context.get('target_audience', 'N/A')}'.
    4. Maintain the general tone: '{website_context.get('tone_of_voice', 'neutral')}'.
    5. If keywords were provided, try to incorporate them naturally.
    6. Important: Write the post to be approximately 600 to 800 words long, ensuring quality and coherence within this range.
    7. Structure the post logically with an introduction, main body (perhaps with subheadings), and a conclusion.
    8. The content must be original and focused solely on the provided topic within the website's context.
    """
    return call_gemini_api(model, prompt)

# Keep existing imports and functions (generate_about_page, generate_blog_post)
from .utils import call_gemini_api
import re # Import regular expressions for parsing

# ... (keep generate_about_page and generate_blog_post functions here) ...

def generate_blog_post_ideas(website_context, model):
    """
    Generates a list of 10 blog post title ideas based on the website context.
    Returns a list of strings (titles) or None if failed.
    """
    if not model or not website_context:
        print("Error: Model or website context is missing for Idea generation.")
        return None

    print("\nGenerating 10 Blog Post Title Ideas...")
    print("-" * 30)

    prompt = f"""
    Act as an expert content strategist and blogger for the website '{website_context.get('website_name', 'this website')}'.

    **Website Context:**
    * Central Theme: {website_context.get('website_theme', 'N/A')}
    * Target Audience: {website_context.get('target_audience', 'N/A')}
    * Purpose/Mission: {website_context.get('website_purpose', 'N/A')}
    * Key Offerings: {website_context.get('key_offerings', 'N/A')}
    * General Tone: {website_context.get('tone_of_voice', 'neutral')}

    **Task:**
    Based *only* on the website context provided above, generate a list of exactly 10 engaging and relevant blog post titles.
    The titles should:
    - Be suitable for the target audience.
    - Directly relate to the website's central theme and purpose.
    - Be varied and interesting.

    **Output Format:**
    Provide the output as a numbered list (1. Title 1, 2. Title 2, ... 10. Title 10).
    Do not include any introductory or concluding text, just the numbered list of titles.
    """

    raw_ideas_text = call_gemini_api(model, prompt)

    if not raw_ideas_text:
        print("Could not generate blog post ideas.")
        return None

    # Attempt to parse the numbered list into a Python list
    ideas = []
    # Split lines, strip whitespace, remove potential numbering (e.g., "1. ", "1) ", "1 - ")
    for line in raw_ideas_text.strip().split('\n'):
        # Regex to remove leading numbers, periods, spaces, hyphens etc.
        cleaned_line = re.sub(r"^\s*\d+[\.\)\-]?\s*", "", line.strip())
        if cleaned_line: # Only add if something remains after cleaning
            ideas.append(cleaned_line)

    if len(ideas) == 0:
         print("Could not parse generated ideas into a list. Raw Output:")
         print(raw_ideas_text)
         return None # Or return raw_ideas_text if you want to handle it differently

    # Ensure we have roughly 10, even if parsing wasn't perfect
    # print(f"Successfully parsed {len(ideas)} ideas.") # Optional debug print
    return ideas[:10] # Return up to 10 parsed ideas