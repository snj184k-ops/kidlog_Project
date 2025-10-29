import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1/models"


def gemini_generate(prompt, model="gemini-2.5-flash"):
    """
    GeminiAPIへのリクエスト及びレスポンス(回答)を取得、レスポンス

    Args:
        prompt (str): プロンプト
        model (str): geminiAIモデル
    Returns:
        str: 回答 or error内容
    """
    url = f"{BASE_URL}/{model}:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.text}"
