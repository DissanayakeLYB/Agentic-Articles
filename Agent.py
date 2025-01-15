from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def scrape_web_detailed(topic, num_links=3):
    """
    Search Google for the topic, follow links, and scrape detailed content.
    """
    # Set up Selenium with headers
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Mimic a real user
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set capabilities to avoid SSL errors
    capabilities = {
        "acceptInsecureCerts": True
    }
    # Merge options and capabilities
    chrome_options.set_capability("goog:chromeOptions", capabilities)

    service = Service()  # Ensure correct path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Perform Google search
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(topic)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for results to load

        # Extract top links from search results
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        urls = []
        for link in links:
            href = link.get_attribute("href")
            if href and "http" in href and "google" not in href:
                urls.append(href)
                if len(urls) >= num_links:
                    break

        # Visit each link and extract content
        detailed_content = []
        for url in urls:
            try:
                driver.get(url)
                time.sleep(5)  # Wait for the page to load

                # Try extracting paragraphs
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                page_content = " ".join([para.text for para in paragraphs if para.text])
                if page_content:
                    detailed_content.append(page_content[:1000])  # Limit to 1000 chars per page
            except Exception as e:
                print(f"Error accessing {url}: {e}")
                continue

        return detailed_content

    finally:
        driver.quit()


# Test the function
if __name__ == "__main__":
    topic = input("Enter the topic you want to research: ")
    print("Researching the topic...")
    detailed_snippets = scrape_web_detailed(topic)

    if detailed_snippets:
        print("\nGenerated Article:")
        print("\n".join(detailed_snippets))
    else:
        print("No sufficient research data found.")
