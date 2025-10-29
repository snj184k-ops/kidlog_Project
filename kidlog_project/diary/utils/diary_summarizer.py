from utils.gemini import gemini_generate


def diary_summarizer(note_text):
    """
    日記の要約をAIにて生成して取得する
    Args:
        note_text (str): ユーザー入力文章
    Returns:
        str: 要約
    """
    prompt = f"次の赤ちゃん日記を10字以内で簡潔に要約してください：\n{note_text}"
    response = gemini_generate(prompt)
    return response.strip()
