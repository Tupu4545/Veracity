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

# Sanitize environment to prevent httpx/proxies initialization errors
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(key, None)

app = Flask(__name__)

# Fallback keys from .env
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
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 20
            }
            res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=5)
            return res.json()['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"-> Keyword extraction failed: {str(e)}. Falling back to raw claim.")
    return claim

@app.route('/analyze', methods=['POST'])
def analyze_claim():
    data = request.json
    user_claim = data.get('claim', '')
    provider = data.get('provider', 'groq')
    
    # 1. Handle Demo Mode
    if provider == "demo":
        import time
        time.sleep(2)
        return jsonify({
            "is_true": "False",
            "confidence_score": 92,
            "political_bias": "Neutral",
            "explanation": "This is a demonstration analysis. In a live environment, Veracity cross-references your claim against live data from NewsAPI using the selected LPU or Gemini model. Based on historical data, the current claim maps to known bot-generated structures.",
            "chart_data": {"supporting_count": 1, "refuting_count": 8, "neutral_count": 3},
            "real_sources": [
                {"source_name": "Demo News Network", "title": "Understanding the spread of misinformation in 2026", "url": "#"},
                {"source_name": "FactCheck Sandbox", "title": "Why this specific claim is definitively false", "url": "#"}
            ]
        })

    # 2. Get Keys and Base URL
    api_key = data.get('api_key')
    news_key = data.get('news_api_key') or ENV_NEWS_KEY
    base_url = data.get('base_url')

    if not api_key:
        return jsonify({'error': 'AI Provider Key is missing. Check settings.'}), 400
    if not news_key:
        return jsonify({'error': 'NewsAPI Key is missing. Check settings.'}), 400

    # 3. Optimize search query
    search_query = extract_search_keywords(user_claim, provider, api_key, base_url)

    # 4. Fetch news context with Adaptive Retry (Feeling Lucky)
    def fetch_news(query):
        url = f"https://newsapi.org/v2/everything?q={requests.utils.quote(query)}&pageSize=12&sortBy=publishedAt&apiKey={news_key}"
        res = requests.get(url, timeout=10).json()
        return res.get('articles', []), res

    articles = []
    try:
        articles, full_res = fetch_news(search_query)
        
        # If no articles found, try a broader search (Feeling Lucky mode)
        if not articles:
            print(f"-> No results for '{search_query}'. Broadening search...")
            broad_query = user_claim.split()[0] if len(user_claim.split()) > 0 else search_query
            # Try to get a better broad query from AI
            try:
                broad_query = extract_search_keywords(f"broaden this search: {user_claim}", provider, api_key, base_url)
            except: pass
            
            articles, full_res = fetch_news(broad_query)
            if articles:
                scraped_context = f"NOTE: Initial specific search yielded zero results. Switched to broader 'Feeling Lucky' context.\n"
            else:
                scraped_context = "CRITICAL: No news articles found even after broadening the search."
        else:
            scraped_context = ""

        if articles:
            for i, article in enumerate(articles):
                scraped_context += f"\n--- ARTICLE {i+1} ---\nSource: {article.get('source', {}).get('name')}\nTitle: {article.get('title')}\nSummary: {article.get('description')}\n"
                real_sources_metadata.append({
                    "source_name": article.get('source', {}).get('name'), 
                    "title": article.get('title'), 
                    "url": article.get('url')
                })
    except Exception as e:
        return jsonify({'error': f'Live news retrieval failed: {str(e)}'}), 500

    # 5. Framing Analysis
    analysis_prompt = f"""
    You are an expert fact-checker and media sentiment analyst. Current year is 2026.
    
    Target Claim to evaluate: "{user_claim}"
    
    Live Context provided by NewsAPI:
    {scraped_context}

    INSTRUCTIONS:
    1. Read and cross-examine EVERY single article provided above against the target claim.
    2. If the context says 'No news articles found', the claim is likely 'Misleading' or 'Unverifiable' rather than strictly False, unless you have definitive prior knowledge.
    3. Categorize every single article into Supporting, Refuting, or Neutral.
    
    You must return ONLY a valid JSON object matching this structure:
    {{
      "is_true": "True" or "False" or "Misleading",
      "confidence_score": 0-100,
      "political_bias": "Bias Label",
      "explanation": "Summarize the supporting vs refuting arguments found in the context.",
      "chart_data": {{"supporting_count": X, "refuting_count": Y, "neutral_count": Z}}
    }}
    """

    try:
        if provider == "groq":
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": analysis_prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            ai_analysis = json.loads(response.choices[0].message.content)
        
        elif provider == "gemini":
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=analysis_prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
                config_overrides={'temperature': 0.1}
            )
            ai_analysis = json.loads(response.text)

        elif provider == "custom":
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4-turbo",
                "messages": [{"role": "user", "content": analysis_prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0.1
            }
            res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=30)
            res_data = res.json()
            ai_analysis = res_data['choices'][0]['message']['content']
            if isinstance(ai_analysis, str): ai_analysis = json.loads(ai_analysis)

        ai_analysis['real_sources'] = real_sources_metadata
        return jsonify(ai_analysis)

    except Exception as e:
        return jsonify({'error': f'AI Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
