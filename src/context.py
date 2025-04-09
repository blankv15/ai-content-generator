def gather_website_context():
    """
    Asks core questions about the website and returns the answers
    as a dictionary (the website context).
    """
    print("\nLet's gather core information about this website.")
    print("This context will be used for generating various content pieces.")
    print("-" * 30)

    # Core questions defining the website's context
    questions = {
        "website_name": "What is the name of the website?",
        "website_theme": "What is the central theme or main topic of this website? (Be specific!)",
        "website_purpose": "What is the primary purpose or mission of this website? What problem does it solve or what value does it offer?",
        "target_audience": "Who is the primary target audience for this website?",
        "key_offerings": "What are the main things the website offers (e.g., information, products, services, community)?",
        "unique_selling_prop": "What makes this website unique or different from others in the same niche?",
        "tone_of_voice": "What is the general tone of voice for the website's content? (e.g., professional, friendly, informative, witty, technical)",
    }

    context = {}
    for key, question in questions.items():
        context[key] = input(f"{question}\n> ")
        print("-" * 10) # Separator

    print("\nWebsite context gathered.")
    return context