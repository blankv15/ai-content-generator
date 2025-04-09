# ai_content_generator/app.py (MODIFIED)

import streamlit as st
import google.generativeai as genai # Import genai here for configuration

# Import functions/data from our source package modules
# Note: Make sure your terminal is running 'streamlit run app.py'
# from the 'ai_content_generator' directory so imports work.
# ASSUMPTION: src/context.py now includes 'brand_story' and 'call_to_action' in QUESTIONS
from src.context import QUESTIONS # Import the questions dict
from src.generators import generate_about_page, generate_blog_post, generate_blog_post_ideas
# utils functions are used internally by generators now

# --- Page Config ---
st.set_page_config(page_title="AI Content Generator", layout="wide")

# --- Initialize Session State ---
# (Initializations remain the same)
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
        # MODIFIED: Changed to a likely valid model name
        model_instance = genai.GenerativeModel('gemini-1.5-flash-latest')
        # Test call (optional but recommended)
        # Consider potential errors during test call as well
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
# (Sidebar code remains the same)
with st.sidebar:
    st.header("API Configuration")
    api_key_input = st.text_input(
        "Enter Google API Key",
        type="password",
        key="api_key_input_widget",
        value=st.session_state.api_key or "",
        help="Get your key from Google AI Studio."
        )
    if st.button("Configure API", key="configure_api_button"):
        # ... (configuration logic remains the same) ...
        if api_key_input:
            with st.spinner("Configuring API Key and Model..."):
                configure_api(api_key_input)
        else:
            st.warning("Please enter your API Key.")

    if st.session_state.api_configured: st.success("API Ready")
    else: st.info("API Key needed to proceed.")


# --- Main App Area ---
st.title("✨ AI Content Generator Assistant")

if not st.session_state.api_configured:
    st.warning("⬅️ Please configure your Google API Key in the sidebar to begin.")
else:
    # --- Step 1: Define Website Context ---
    st.header("Step 1: Define Website Context", divider="rainbow")
    col1_context, col2_context = st.columns([2, 1])

    with col1_context:
        with st.form("context_form"):
            st.subheader("Website Details")
            st.caption("Tell the AI about the website. This context will be used for all generated content.")

            context_inputs = {}
            for key, question in QUESTIONS.items():
                previous_value = st.session_state.site_context.get(key, "") if st.session_state.site_context else ""
                # MODIFIED: Specifically check for brand_story key for text_area
                if key in ["website_purpose", "key_offerings", "unique_selling_prop", "brand_story"]:
                     context_inputs[key] = st.text_area(question, key=f"context_{key}", height=100, value=previous_value)
                else: # Handles name, theme, audience, tone, call_to_action
                     context_inputs[key] = st.text_input(question, key=f"context_{key}", value=previous_value)

            submitted = st.form_submit_button("💾 Save Website Context")
            if submitted:
                if not context_inputs.get("website_name") or not context_inputs.get("website_theme"):
                     st.warning("Please provide at least the Website Name and Theme.")
                else:
                    st.session_state.site_context = context_inputs
                    st.success("Website Context Saved!")
                    # Optional: st.rerun()

    with col2_context:
        st.subheader("Context Status")
        # (Context status display remains the same)
        if st.session_state.site_context:
            st.success("✅ Context Saved")
            with st.expander("View Current Context"):
                st.json(st.session_state.site_context) # Will show story/cta if saved
            if st.button("🗑️ Clear Context & Start Over", key="clear_context"):
                # ... (clear state logic remains same) ...
                st.rerun()
        else:
            st.info("Context not yet saved.")


    # --- Step 2: Generate Content (Only if context is saved) ---
    if st.session_state.site_context:
        st.header("Step 2: Generate Content", divider="rainbow")
        col1_gen, col2_gen = st.columns(2)

        # --- About Page Section ---
        with col1_gen:
            st.subheader("📄 About Page (~600 words)")

            # --- REMOVED WIDGETS for Brand Story and CTA ---
            # These are now collected in the form above and stored in site_context

            if st.button("Generate About Page", key="generate_about"):
                if not st.session_state.model:
                     st.error("API Model not configured.")
                else:
                    with st.spinner("Generating About Page..."):
                        try:
                            # --- MODIFIED: Get story/cta from context ---
                            brand_story_from_context = st.session_state.site_context.get("brand_story") # Use key from QUESTIONS
                            cta_from_context = st.session_state.site_context.get("call_to_action")       # Use key from QUESTIONS

                            about_content = generate_about_page(
                                st.session_state.site_context,
                                st.session_state.model,
                                brand_story=brand_story_from_context, # Pass value from context (can be None or empty)
                                call_to_action=cta_from_context      # Pass value from context (can be None or empty)
                            )
                            # --- END MODIFICATION ---

                            st.session_state.about_page_content = about_content
                            if not about_content:
                                 st.error("Failed to generate About page content (No text returned). Check console logs.")

                        except Exception as e:
                            st.session_state.about_page_content = None
                            st.error("An error occurred during About Page generation.")
                            st.exception(e)
                            print(f"ERROR in app.py during generate_about_page call: {e}")

            # Display About Page if generated
            if st.session_state.about_page_content:
                with st.expander("View Generated About Page", expanded=True):
                    st.markdown(st.session_state.about_page_content)
                    st.code(st.session_state.about_page_content, language=None)


        # --- Blog Ideas & Posts Section ---
        with col2_gen:
            # (Blog post generation code remains the same as your provided version)
            st.subheader("✍️ Blog Posts (~600-800 words)")
            # ... (Generate Ideas button) ...
            # ... (Selectbox / Custom topic input) ...
            # ... (Generate Blog Post button logic) ...
            # ... (Display generated blog posts) ...
            if st.session_state.blog_ideas is None:
                if st.button("💡 Generate Blog Post Ideas", key="generate_ideas"):
                    # ... (generate ideas logic) ...
                    with st.spinner("Generating ideas..."):
                        ideas = generate_blog_post_ideas(st.session_state.site_context, st.session_state.model)
                        if ideas: st.session_state.blog_ideas = ideas
                        else: st.session_state.blog_ideas = []
                        st.rerun()

            topic_to_generate = None
            if st.session_state.blog_ideas is not None:
                if not st.session_state.blog_ideas: st.info("No blog ideas generated yet...")
                else:
                    # ... (selectbox logic) ...
                    options = ["-- Select an Idea --"] + st.session_state.blog_ideas
                    selected_idea = st.selectbox("Choose a title:", options, key="idea_selectbox", index=0)
                    if selected_idea != "-- Select an Idea --": topic_to_generate = selected_idea

                custom_topic = st.text_input("Or Enter a Custom Topic:", key="custom_topic_input")
                if custom_topic and not topic_to_generate: topic_to_generate = custom_topic

                if topic_to_generate:
                    st.write(f"Ready for: **{topic_to_generate}**")
                    if st.button(f"Generate Blog Post: '{topic_to_generate[:40]}...'", key=f"generate_blog_{topic_to_generate}"):
                         # ... (generate blog post logic) ...
                         with st.spinner(f"Generating post..."):
                            blog_content = generate_blog_post(st.session_state.site_context, st.session_state.model, topic_to_generate)
                            if blog_content:
                                st.session_state.generated_blog_posts[topic_to_generate] = blog_content
                                st.success("Blog post generated!")
                            else:
                                st.error(f"Failed to generate blog post for '{topic_to_generate}'.")
                            st.rerun()

            if st.session_state.generated_blog_posts:
                st.markdown("---")
                st.subheader("📚 Generated Blog Posts")
                # ... (display generated posts) ...
                topics = list(st.session_state.generated_blog_posts.keys())
                for topic in reversed(topics):
                    content = st.session_state.generated_blog_posts[topic]
                    with st.expander(f"📄 {topic}", expanded=False):
                        st.markdown(content)
                        st.code(content, language=None)