import streamlit as st
import google.generativeai as genai # Import genai here for configuration

# Import functions/data from our source package modules
# Note: Make sure your terminal is running 'streamlit run app.py'
# from the 'ai_content_generator' directory so imports work.
from src.context import QUESTIONS # Import the questions dict
from src.generators import generate_about_page, generate_blog_post, generate_blog_post_ideas
# utils functions are used internally by generators now

# --- Page Config ---
st.set_page_config(page_title="AI Content Generator", layout="wide")

# --- Initialize Session State ---
# Keeps track of data across reruns
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'site_context' not in st.session_state:
    st.session_state.site_context = None # Will store the dict from the form
if 'about_page_content' not in st.session_state:
    st.session_state.about_page_content = None
if 'blog_ideas' not in st.session_state:
    st.session_state.blog_ideas = None # Will store the list of ideas
if 'generated_blog_posts' not in st.session_state:
    st.session_state.generated_blog_posts = {} # key: topic, value: content

# --- Helper function for API Configuration ---
def configure_api(api_key_from_input):
    """Configures API and sets session state."""
    try:
        genai.configure(api_key=api_key_from_input)
        model_instance = genai.GenerativeModel('gemini-2.0-flash') # Or other model
        # Test call (optional but recommended)
        model_instance.generate_content("Test: Say Hi", generation_config=genai.types.GenerationConfig(temperature=0.1)) # Low temp test
        st.session_state.model = model_instance
        st.session_state.api_key = api_key_from_input
        st.session_state.api_configured = True
        st.sidebar.success("API Configured Successfully!")
        return True
    except Exception as e:
        st.session_state.api_configured = False
        st.session_state.model = None
        st.session_state.api_key = None
        st.sidebar.error(f"API Config Failed: {e}")
        return False

# --- Sidebar for API Key ---
with st.sidebar:
    st.header("API Configuration")
    # Use existing key from session state if available
    api_key_input = st.text_input(
        "Enter Google API Key",
        type="password",
        key="api_key_input_widget",
        value=st.session_state.api_key or "",
        help="Get your key from Google AI Studio."
        )

    if st.button("Configure API", key="configure_api_button"):
        if api_key_input:
            with st.spinner("Configuring API Key and Model..."):
                configure_api(api_key_input)
        else:
            st.warning("Please enter your API Key.")

    if st.session_state.api_configured:
        st.success("API Ready")
    else:
        st.info("API Key needed to proceed.")


# --- Main App Area ---
st.title("✨ AI Content Generator Assistant")

# Only proceed if API is configured
if not st.session_state.api_configured:
    st.warning("⬅️ Please configure your Google API Key in the sidebar to begin.")
else:
    # --- Step 1: Define Website Context ---
    st.header("Step 1: Define Website Context", divider="rainbow")

    # Use columns for better layout
    col1_context, col2_context = st.columns([2, 1]) # Input form on left, status on right

    with col1_context:
        # Form to prevent reruns for every text input change
        with st.form("context_form"):
            st.subheader("Website Details")
            st.caption("Tell the AI about the website. This context will be used for all generated content.")

            # Create text inputs based on the imported QUESTIONS dictionary
            context_inputs = {}
            for key, question in QUESTIONS.items():
                # Use text_area for potentially longer answers like purpose/offerings
                if key in ["website_purpose", "key_offerings", "unique_selling_prop"]:
                     context_inputs[key] = st.text_area(question, key=f"context_{key}", height=100, value=st.session_state.site_context.get(key, "") if st.session_state.site_context else "")
                else:
                     context_inputs[key] = st.text_input(question, key=f"context_{key}", value=st.session_state.site_context.get(key, "") if st.session_state.site_context else "")

            submitted = st.form_submit_button("💾 Save Website Context")

            if submitted:
                # Simple validation
                if not context_inputs.get("website_name") or not context_inputs.get("website_theme"):
                     st.warning("Please provide at least the Website Name and Theme.")
                else:
                    st.session_state.site_context = context_inputs # Store the whole dict
                    st.success("Website Context Saved!")
                    # No rerun needed here, state is saved, Streamlit continues

    with col2_context:
        st.subheader("Context Status")
        if st.session_state.site_context:
            st.success("✅ Context Saved")
            with st.expander("View Current Context"):
                st.json(st.session_state.site_context)
            if st.button("🗑️ Clear Context & Start Over", key="clear_context"):
                # Clear relevant session state variables
                st.session_state.site_context = None
                st.session_state.about_page_content = None
                st.session_state.blog_ideas = None
                st.session_state.generated_blog_posts = {}
                st.rerun() # Rerun to reflect cleared state
        else:
            st.info("Context not yet saved. Please fill the form and save.")


    # --- Step 2: Generate Content (Only if context is saved) ---
    if st.session_state.site_context:
        st.header("Step 2: Generate Content", divider="rainbow")

        # Use columns for About Page and Blog Posts sections
        col1_gen, col2_gen = st.columns(2)

        # --- About Page Section ---
        with col1_gen:
            st.subheader("📄 About Page (~600 words)")

            # Optional inputs for the adapted generate_about_page function
            about_brand_story = st.text_area("Optional Brand Story for About Page:", height=100, key="about_story")
            about_cta = st.text_input("Optional Call to Action for About Page:", key="about_cta")

            if st.button("Generate About Page", key="generate_about"):
                with st.spinner("Generating About Page..."):
                    about_content = generate_about_page(
                        st.session_state.site_context,
                        st.session_state.model,
                        brand_story=about_brand_story if about_brand_story else None,
                        call_to_action=about_cta if about_cta else None
                    )
                    st.session_state.about_page_content = about_content # Store result
                    if not about_content:
                         st.error("Failed to generate About page content.")
                    # No rerun needed, content will display below on next natural run

            # Display About Page if generated
            if st.session_state.about_page_content:
                with st.expander("View Generated About Page", expanded=True):
                    st.markdown(st.session_state.about_page_content)
                    # Add copy-to-clipboard button
                    st.code(st.session_state.about_page_content, language=None) # Show in code block for easy copy
                    # st.button("Copy Text", key="copy_about", on_click=...) # Requires clipboard library


        # --- Blog Ideas & Posts Section ---
        with col2_gen:
            st.subheader("✍️ Blog Posts (~600-800 words)")

            # Generate Ideas Button (only show if no ideas yet)
            if st.session_state.blog_ideas is None:
                if st.button("💡 Generate Blog Post Ideas", key="generate_ideas"):
                    with st.spinner("Generating ideas..."):
                        ideas = generate_blog_post_ideas(st.session_state.site_context, st.session_state.model)
                        if ideas:
                             st.session_state.blog_ideas = ideas
                             st.success(f"Generated {len(ideas)} ideas!")
                        else:
                             st.error("Failed to generate blog ideas.")
                             st.session_state.blog_ideas = [] # Ensure it's list even if failed
                        st.rerun() # Rerun to display the ideas selectbox

            # Display Ideas and Allow Selection/Generation
            topic_to_generate = None
            if st.session_state.blog_ideas is not None:
                if not st.session_state.blog_ideas:
                     st.info("No blog ideas generated yet, or generation failed. Enter a custom topic below.")
                else:
                     st.write("**Suggested Blog Titles:**")
                     # Add placeholder options for selectbox
                     options = ["-- Select an Idea --"] + st.session_state.blog_ideas
                     selected_idea = st.selectbox(
                         "Choose a title to generate:",
                         options,
                         key="idea_selectbox",
                         index=0 # Default to placeholder
                         )
                     if selected_idea != "-- Select an Idea --":
                           topic_to_generate = selected_idea

                # Allow custom topic entry
                custom_topic = st.text_input("Or Enter a Custom Blog Post Topic:", key="custom_topic_input")
                if custom_topic and not topic_to_generate: # Prioritize selected idea if both exist
                     topic_to_generate = custom_topic

                # Button to trigger generation if a topic is selected/entered
                if topic_to_generate:
                     st.write(f"Ready to generate for: **{topic_to_generate}**")
                     # Optional Keywords Input
                     # blog_keywords = st.text_input("Optional Keywords (comma-separated):", key="blog_keywords")

                     if st.button(f"Generate Blog Post: '{topic_to_generate[:40]}...'", key=f"generate_blog_{topic_to_generate}"):
                           with st.spinner(f"Generating post for '{topic_to_generate[:40]}...'"):
                                blog_content = generate_blog_post(
                                     st.session_state.site_context,
                                     st.session_state.model,
                                     topic_to_generate #,
                                     # keywords=blog_keywords if blog_keywords else None
                                )
                                if blog_content:
                                     # Store the generated post, keyed by topic
                                     st.session_state.generated_blog_posts[topic_to_generate] = blog_content
                                     st.success("Blog post generated!")
                                     # Clear inputs for next round? Optional.
                                     # st.session_state.custom_topic_input = ""
                                     # Consider resetting selectbox? Tricky with state.
                                else:
                                     st.error(f"Failed to generate blog post for '{topic_to_generate}'.")
                                st.rerun() # Rerun to show the new post in the list below


            # --- Display Generated Blog Posts ---
            if st.session_state.generated_blog_posts:
                st.markdown("---")
                st.subheader("📚 Generated Blog Posts")
                # Sort by topic? Or order of generation? Dicts are ordered in Python 3.7+
                topics = list(st.session_state.generated_blog_posts.keys())
                for topic in reversed(topics): # Show newest first
                     content = st.session_state.generated_blog_posts[topic]
                     with st.expander(f"📄 {topic}", expanded=False):
                          st.markdown(content)
                          st.code(content, language=None) # Easy copy
