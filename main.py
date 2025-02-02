import spacy
from intents import intents
import time
import random

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

nlp = spacy.load("en_core_web_sm")

# doc = nlp("I want to buy clothes from amazon")

# for token in doc:
#     print(
#         token.text,
#         token.lemma_,
#         token.pos_,
#         token.tag_,
#         token.dep_,
#         token.shape_,
#         token.is_alpha,
#         token.is_stop,
#     )


def get_intent(input_text):
    token_obj = nlp(input_text)

    noun = None
    intent = "unknown_intent"
    location = None

    for token in token_obj:
        if token.pos_ == "VERB":
            lemma = token.lemma_.lower()

            if lemma in intents:
                intent = intents[lemma]

            for key in intents.keys():
                if key in lemma:
                    intent = intents[key]

        if token.pos_ == "NOUN":
            noun = token.text

        if token.pos_ == "PROPN":
            location = token.text

    for ent in token_obj.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            location = ent.text

    return {"noun": noun, "intent": intent, "location": location}


# Example usage
input_text = "book honeymoon tickets for andaman."
result = get_intent(input_text)
# print(result)


def human_typing(page, selector, text):
    for char in text:
        page.type(
            selector, char, delay=random.randint(50, 60)
        )  # 100–300 ms delay per keystroke
        time.sleep(random.uniform(0.05, 0.15))  # Slight pause between characters


def launch_search(query):
    if query == None:
        return False
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    ]
    p = sync_playwright().start()
    user_agent = random.choice(user_agent_list)
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    stealth_sync(page)
    page.goto("https://www.google.com")

    page.wait_for_selector('textarea[name="q"]', timeout=5000)

    # human_typing(page, 'textarea[name="q"]', query)
    page.type('textarea[name="q"]', query)
    page.press('textarea[name="q"]', "Enter")

    page.wait_for_selector("#search", timeout=10000)
    page.wait_for_load_state("networkidle")

    # page.wait_for_selector("#search")
    frame = page.main_frame  # Use the main frame
    first_result = frame.query_selector("a h3")

    print(first_result)

    if first_result:
        time.sleep(3)
        first_result.click()
    else:
        print("No search results found.")

    page.wait_for_load_state("networkidle")
    time.sleep(5)
    # Take a screenshot of the results page
    page.screenshot(path="google_search.png")

    page.wait_for_event("close", timeout=0)
    print("Search completed, screenshot saved.")
    # browser.close()

    # browser.close()


# agent talks with user like a human


def talk_with_user(query):
    resultObj = get_intent(query)
    print(resultObj)
    return f"Are you looking for {resultObj["intent"]}"


launch_search(input_text)

# talking = talk_with_user(input_text)
# print(talking)
