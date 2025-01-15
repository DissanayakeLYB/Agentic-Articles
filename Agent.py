import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv()
API_KEY = os.environ.get("groq_API")

client = Groq(api_key=API_KEY)


# Web scraping using Selenium
def scrape_web_detailed(topic, num_links=3):
    """
    Search Google for the topic, follow links, and scrape detailed content.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service()  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(topic)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  

        links = driver.find_elements(By.CSS_SELECTOR, "a")
        urls = []
        for link in links:
            href = link.get_attribute("href")
            if href and "http" in href and "google" not in href:
                urls.append(href)
                if len(urls) >= num_links:
                    break

        detailed_content = []
        for url in urls:
            try:
                driver.get(url)
                time.sleep(5)  

                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                page_content = " ".join([para.text for para in paragraphs if para.text])
                if page_content:
                    detailed_content.append(page_content[:1000]) 
            except Exception as e:
                st.error(f"Error scraping {url}: {e}")
                continue

        return detailed_content

    finally:
        driver.quit()


# article generation using Groq API
def generate_article_with_groq(topic, research_data):
    """
    Use Groq API to generate an article based on a topic and research data.
    """
    prompt = f"Write a well-structured, informative, and engaging article on the topic: '{topic}'. Use the following research data: {research_data}"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    article = chat_completion.choices[0].message.content
    return article


# Quillbot AI Content Detector
def check_ai_generated_content(article):
    """
    Check how much of the content is detected as AI-generated using Quillbot AI Content Detector.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service()  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://quillbot.com/ai-content-detector")
        time.sleep(3)  

        text_area = driver.find_element(By.XPATH, '//div[@placeholder="To analyze text, add at least 80 words."]')
        text_area.send_keys(article)

        # Wait for the button to be visible and clickable
        wait = WebDriverWait(driver, 10)
        detect_ai_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="aidr-primary-cta"]'))
        )
        ActionChains(driver).move_to_element(detect_ai_button).click(detect_ai_button).perform()

        time.sleep(5) 

        wait = WebDriverWait(driver, 10)
        result_div = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="MuiBox-root css-1xb5foi"]'))
        )

        result_text = result_div.text

        return result_text

    except Exception as e:
        st.error(f"Error during AI content detection: {e}")
        return "Error"

    finally:
        driver.quit()


# Streamlit app
def main():
    st.title("AgentArticle")
    st.write("Enter a topic to scrape web data, generate an informative article, and check AI-generated content percentage.")

    # Input: Topic
    topic = st.text_input("Enter the topic for the article:")

    if st.button("Generate Article"):
        if not topic.strip():
            st.error("Please enter a valid topic.")
        else:
            # Step 1: Fetch web-scraped data
            st.write("Fetching research data from the web...")
            research_data = scrape_web_detailed(topic)

            if not research_data:
                st.error("Could not fetch sufficient data for the topic. Please try again.")
                return

            # Groq generates the article
            st.write("Generating the article using Groq...")
            article = generate_article_with_groq(topic, " ".join(research_data))

            if article:
                st.subheader("Generated Article:")
                st.write(article)

                st.write("Checking AI-generated content percentage...")
                ai_percentage = check_ai_generated_content(article)
                st.write(f"**AI Content Detection Result:** {ai_percentage}%")
            else:
                st.error("Could not generate an article. Please try again.")


if __name__ == "__main__":
    main()
