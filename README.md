# ✨ AI Content Generator Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-red.svg)](https://streamlit.io/)

A powerful, user-friendly web application that leverages Google's Gemini API to generate high-quality website content, including "About" pages and engaging blog posts. The intuitive interface is built with Streamlit, making content creation a breeze.

![AI Content Generator Assistant Initial Screen](https://github.com/blankv15/blogwriter/blob/master/assets/preview7.png)

## 🚀 Overview

The AI Content Generator Assistant is designed to streamline the content creation process for bloggers, marketers, and website owners. By providing context about your website—such as its purpose, audience, and tone—the application generates tailored content that resonates with your brand. Say goodbye to writer's block and hello to effortless content production.

## 🌟 Features

* **🤖 Advanced AI Engine:** Powered by Google's state-of-the-art Gemini Pro model for coherent, context-aware, and high-quality text generation.
* **🖥️ Interactive Web UI:** A clean, intuitive, and easy-to-navigate web interface built with Streamlit.
* **✍️ Website Context Definition:** Provide the AI with a detailed profile of your website to ensure all generated content is perfectly aligned with your brand voice.
* **📄 "About Page" Generation:** Automatically create a comprehensive and professional "About Page" (approx. 600 words) that tells your brand's story.
* **💡 Blog Idea Generation:** Generates a list of 10 creative and relevant blog post headlines to kickstart your content calendar.
* **📝 Full Blog Post Creation:** Select a suggested headline or enter your own custom topic to generate a full-length blog post (approx. 600-800 words).

## 🛠️ Tech Stack

* **Backend:** Python
* **AI Model:** Google Gemini Pro
* **Web Framework:** Streamlit

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

* [Python 3.9+](https://www.python.org/downloads/)
* `pip` (Python package installer)
* A **Google Gemini API Key**. You can obtain one by following the instructions [here](https://ai.google.dev/gemini-api/docs/api-key).

## ⚙️ Installation & Setup

Follow these steps to get the application running on your local machine.

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/blankv15/ai-content-generator](https://github.com/blankv15/ai-content-generator)
    cd ai-content-generator
    ```

2.  **Create and Activate a Virtual Environment**
    Using a virtual environment is highly recommended to manage project dependencies.
    ```sh
    # Create the virtual environment
    python3 -m venv .venv

    # Activate it (on macOS/Linux)
    source .venv/bin/activate

    # Or activate it (on Windows)
    .\.venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Install all the required Python packages from the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    Launch the Streamlit web server.
    ```sh
    streamlit run app.py
    ```
    Your web browser should automatically open to `http://localhost:8501`.

## 📖 How to Use

### Step 1: API Configuration

Upon launching the app, the first step is to provide your Google Gemini API Key.
* Enter your key in the **API Configuration** section in the sidebar.
* The status indicator will change from `API Not Ready` to `API Ready` upon successful configuration.

![API Configuration Ready](https://github.com/blankv15/blogwriter/blob/master/assets/preview2.png)

### Step 2: Define Website Context

Navigate to the **Step 1: Define Website Context** section. Fill out the form to give the AI a clear understanding of your website. The more detail you provide, the better the generated content will be.

![Define Website Context](https://github.com/blankv15/blogwriter/blob/master/assets/preview3.png)

* Click **Save Website Context** to proceed.

### Step 3: Generate Content

Now you're ready to create!

* **To Generate an "About Page":**
    * Under the **About Page (~600 words)** section, click `Generate About Page`. The content will appear below.

* **To Generate a Blog Post:**
    * Under the **Blog Posts (~600-800 words)** section, you have two options:
        1.  **Choose a suggested title** from the dropdown menu.
        2.  **Enter a Custom Topic** in the text field.
    * Click the `Generate Blog Post` button. Your new article will be displayed below.

![Generated Blog Post Content](https://github.com/blankv15/blogwriter/blob/master/assets/preview5.png)

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or want to add new features, please feel free to:

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.
