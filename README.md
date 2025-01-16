# **AgentArticle 🕵️‍♂️**

AgentArticle is an AI-powered application that combines web scraping, natural language processing, and AI tools to generate high-quality, human-like articles that you can share on your LinkedIn or other social Media Platforms. The application integrates various APIs, AI tools, and Selenium automation to streamline content creation, making it ideal for professionals, content creators, and marketers.

---

## **Features**

- **Web Scraping**: Automatically scrape detailed content from the web using Selenium.
- **AI Article Generation**: Use the Groq API to generate informative articles based on the scraped data.
- **AI Content Detection**: Detect AI-generated content using the Quillbot AI Content Detector.
- **Humanization**: Improve the human-like quality of AI-generated content using Humanize AI.
- **Streamlit UI**: User-friendly interface for easy interaction and content generation.

---

## **Technologies Used**

- **Programming Language**: Python
- **Libraries**:
  - [Streamlit](https://streamlit.io/) for building the web app interface.
  - [Selenium](https://www.selenium.dev/) with `undetected-chromedriver` for web automation and scraping.
  - [Requests](https://docs.python-requests.org/) for API calls.
  - [dotenv](https://pypi.org/project/python-dotenv/) for managing environment variables.
- **APIs**:
  - [Groq API](https://groq.com/) for article generation.

---

## **How It Works**

1. The user enters a topic of interest via the Streamlit interface.

2. Selenium automates Google search and scrapes content from the top 3 relevant links.

3. The Groq API processes the scraped data and generates a concise, well-structured article.

4. The generated article is analyzed to detect AI-generated content using Quillbot.

5. If the AI-detection percentage exceeds 10%, the article is humanized using Humanize AI. Step 4 and Step 5 are repeated until the Ai-detection percentage reduces than 10%.

6. The final article is displayed and can be copied or downloaded for further use.

---

## **Installation**

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/DissanayakeLYB/Agentic-Articles
cd Agentic-Article
```

### **Step 2: Install Dependencies**

Make sure you have Python 3.8 or higher installed.

```bash
pip install -r requirements.txt
```

### **Step 3: Set Up Environment Variables**

Create a `.env` file in the project directory and add the following:

```
groq_API=<YOUR_GROQ_API_KEY>
```

### **Step 4: Run the Application**

```bash
streamlit run Agent.py
```

---

## **Screenshots**

### **Main Interface**

![Main Interface](https://github.com/DissanayakeLYB/Agentic-Articles/main-interface.png)

### **Generated Article**

![Generated Article](https://github.com/DissanayakeLYB/Agentic-Articles/generated_article.pn)

---

## **Future Improvements**

- To add support for additional AI models.
- Expanding the scraping capabilities to include more resources.
- Enhance error handling and logging mechanisms.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

---

## **License**

This project is licensed under the [MIT License](https://github.com/DissanayakeLYB/Agentic-Articles/blob/main/LICENSE).

---
