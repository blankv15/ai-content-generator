# Import functions from our source package modules
from src.api_config import configure_api_and_model
from src.context import gather_website_context
from src.generators import generate_about_page, generate_blog_post, generate_blog_post_ideas
from src.utils import display_output

def run_generator():
    """Main function to orchestrate the content generation process."""

    print("Initializing AI Content Generator...")
    ai_model = configure_api_and_model()

    if not ai_model:
        print("Could not initialize AI Model. Exiting.")
        return

    site_context = gather_website_context()

    if not site_context:
        print("Website context gathering failed or was interrupted. Exiting.")
        return

    # --- Generate About Page ---
    print("\n" + "="*40)
    print("Proceeding to generate the About Page...")
    about_page_content = generate_about_page(site_context, ai_model)
    if about_page_content:
        display_output("About Page (~600 words)", about_page_content)
    else:
        print("Failed to generate About Page content.")

    # --- Generate Blog Post Ideas --- MODIFIED SECTION START
    print("\n" + "="*40)
    print("Now, let's generate some blog post ideas based on the context...")
    blog_ideas = generate_blog_post_ideas(site_context, ai_model)

    if not blog_ideas:
        print("Could not generate blog post ideas. Proceeding to manual topic entry.")
        blog_ideas = [] # Ensure blog_ideas is an empty list if generation failed
    else:
        print("\nHere are some suggested blog post titles:")
        for i, title in enumerate(blog_ideas):
            print(f"{i + 1}. {title}")
        print("-" * 30)
    # --- Generate About Page ---
    print("\n" + "="*40)
    print("Proceeding to generate the About Page...")
    about_page_content = generate_about_page(site_context, ai_model)
    if about_page_content:
        display_output("About Page (~600 words)", about_page_content)
    else:
        print("Failed to generate About Page content.")


    # --- Generate Blog Posts (Example Loop) ---
    print("\n" + "="*40)
    print("Now let's generate some blog posts using the same website context.")

    while True: # Loop to generate multiple posts
        topic = input("Enter the topic for the next blog post (or type 'quit' to exit):\n> ")
        if topic.lower() == 'quit':
            break
        if not topic:
            print("Topic cannot be empty.")
            continue

        # Optional: Ask for keywords if needed for this specific post
        # keywords = input("Enter any target keywords (comma-separated, optional):\n> ")

        blog_post_content = generate_blog_post(
            site_context,
            ai_model,
            topic #,
            # keywords=keywords if keywords else None
        )

        if blog_post_content:
            display_output(f"Blog Post (~600-800 words): '{topic[:30]}...'", blog_post_content)
        else:
            print(f"Failed to generate blog post content for topic: {topic}")

        print("\n" + "="*40) # Separator for next post or exit

    print("\nContent generation finished.")


# --- Main Execution Guard ---
if __name__ == "__main__":
    run_generator()