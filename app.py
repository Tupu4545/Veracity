import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq
from google import genai
from google.genai import types

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Fallback keys from .env
ENV_GROQ_KEY = os.getenv("GROQ_API_KEY")
ENV_GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
ENV_NEWS_KEY = os.getenv("NEWS_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/api-docs')
def api_docs():
    return render_template('api_docs.html')

def extract_search_keywords(claim, provider, api_key, base_url=None):
    """Uses the selected provider to convert natural language claims into keywords."""
    prompt = f"""
    Convert the following user statement into 2-4 highly optimized search keywords for a news database.
    Ignore questioning words (e.g., 'was', 'is', 'did') and focus on the core subject and event.
    
    Statement: "{claim}"
    
    Return ONLY the keywords separated by spaces. Do not include any other text or punctuation.
    """
    
    try:
        if provider == "groq":
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=20
            )
            return response.choices[0].message.content.strip()
        
        elif provider == "gemini":
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text.strip()
            
        elif provider == "custom":
            # Using standard requests for OpenAI-compatible custom endpoints
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-3.5-turbo", # Default fallback for custom endpoints
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 20
            }
            res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)
            return res.json()['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"-> Keyword extraction failed: {str(e)}. Falling back to raw claim.")
        return claim

@app.route('/analyze', methods=['POST'])
def analyze_claim():
    data = request.json
    user_claim = data.get('claim', '')
    provider = data.get('provider', 'groq')

    if provider == "demo":
        import time
        time.sleep(2) # Simulate network delay
        return jsonify({
            "is_true": "False",
            "confidence_score": 92,
            "political_bias": "Neutral",
            "explanation": "This is a demonstration analysis. In a live environment, Veracity cross-references your claim against live data from NewsAPI using the selected LPU or Gemini model. Based on historical data, the current claim maps to known bot-generated structures.",
            "chart_data": {"supporting_count": 1, "refuting_count": 8, "neutral_count": 3},
            "real_sources": [
                {"source_name": "Demo News Network", "title": "Understanding the spread of misinformation in 2026", "url": "#"},
                {"source_name": "FactCheck Sandbox", "title": "Why this specific claim is definitively false", "url": "#"}
            ],
            "timestamp": requests.utils.quote(user_claim)
        })

    api_key = data.get('api_key')
    news_key = data.get('news_api_key') or ENV_NEWS_KEY
    base_url = data.get('base_url')

    if not api_key:
        return jsonify({'error': 'API Key is missing. Check settings.'}), 400
    if not news_key:
        return jsonify({'error': 'NewsAPI Key is missing. Check settings.'}), 400

    # 1. Optimize search query
    search_query = extract_search_keywords(user_claim, provider, api_key, base_url)

    # 2. Fetch news context
    news_url = f"https://newsapi.org/v2/everything?q={requests.utils.quote(search_query)}&pageSize=12&sortBy=publishedAt&apiKey={news_key}"
    scraped_context = ""
    real_sources_metadata = []

    try:
        news_response = requests.get(news_url).json()
        articles = news_response.get('articles', [])
        if articles:
            for i, article in enumerate(articles):
                scraped_context += f"\n--- ARTICLE {i+1} ---\nSource: {article.get('source', {}).get('name')}\nTitle: {article.get('title')}\nSummary: {article.get('description')}\n"
                real_sources_metadata.append({"source_name": article.get('source', {}).get('name'), "title": article.get('title'), "url": article.get('url')})
        else:
            scraped_context = "No active news articles found."
    except:
        return jsonify({'error': 'News retrieval failed.'}), 500

    # 3. Framing Analysis
    analysis_prompt = f"""
    You are an expert fact-checker. Current year is 2026.
    Target Claim: "{user_claim}"
    Live Context: {scraped_context}
    
    Return ONLY a JSON object:
    {{
      "is_true": "True"|"False"|"Misleading",
      "confidence_score": 0-100,
      "political_bias": "Bias",
      "explanation": "Reasoning...",
      "chart_data": {{"supporting_count":X, "refuting_count":Y, "neutral_count":Z}}
    }}
    """

    try:
        if provider == "groq":
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": analysis_prompt}],
                response_format={"type": "json_object"}
            )
            ai_analysis = json.loads(response.choices[0].message.content)
        
        elif provider == "gemini":
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=analysis_prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            ai_analysis = json.loads(response.text)

        elif provider == "custom":
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4-turbo", # Or user choice
                "messages": [{"role": "user", "content": analysis_prompt}],
                "response_format": {"type": "json_object"}
            }
            res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)
            ai_analysis = res.json()['choices'][0]['message']['content']
            if isinstance(ai_analysis, str): ai_analysis = json.loads(ai_analysis)

        ai_analysis['real_sources'] = real_sources_metadata
        return jsonify(ai_analysis)

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
