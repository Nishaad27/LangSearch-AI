# LangSearch-AI

LangSearch-AI is an AI-powered search assistant built with **Streamlit** and **LangChain**. It leverages **Llama3** for natural language processing and integrates real-time search tools like **Wikipedia, Arxiv, and DuckDuckGo** to provide structured, in-depth responses to user queries.

## Features

- AI-Powered Search: Uses **Llama3-8b-8192** for intelligent responses.
- Multi-Source Search: Retrieves data from Wikipedia, Arxiv, and DuckDuckGo.
- Streamlit UI: Simple and interactive chatbot interface.
- Error Handling: Graceful handling of rate limits and parsing errors.
- Dark Mode Support: Adaptive styles for light and dark themes.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Nishaad27/LangSearch-AI.git
   cd LangSearch-AI
   ```

2. Create a virtual environment (Optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file and add your `GROQ_API_KEY`:
     ```
     GROQ_API_KEY=your_api_key_here
     ```

5. Run the application:
   ```sh
   streamlit run app.py
   ```

## UI Preview

![LangSearch UI](https://github.com/Nishaad27/LangSearch-AI/raw/main/assets/screenshot.png)

## Tech Stack

- Frontend: Streamlit
- Backend: Python, LangChain
- LLM Model: Llama3-8b-8192
- Search APIs: Wikipedia, Arxiv, DuckDuckGo

## Contributions

Feel free to contribute by submitting issues, feature requests, or pull requests.

---

Built by **Nishaad**

