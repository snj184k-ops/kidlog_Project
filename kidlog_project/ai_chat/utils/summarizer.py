from django.conf import settings
import os

KEY_LABELS = {
    "age": "年齢",
    "height_data": "平均身長 (cm)",
    "weight_data": "平均体重 (kg)",
    "avg_milk": "平均ミルク摂取量 (ml)",
    "avg_poop": "平均うんち回数 (回)",
    "avg_pee": "平均おしっこ回数 (回)",
    "avg_sleep": "平均睡眠時間 (時間)",
    "avg_temp": "平均体温 (度)",
    "avg_food": "平均食事回数 (回)",
    "menu_list": "平均食事メニュー",
}


def load_prompt_template(filename):
    """
    テンプレートプロンプトを読み込み、プロンプト文字列をレスポンス

    Args:
        template_name (str): テンプレートプロンプトのファイル名

    Returns:
        str: 文字列化したテンプレートプロンプト
    """
    prompt_path = os.path.join(settings.BASE_DIR, "ai_chat", "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def build_analysis_prompt(childcare_summary_data, user_prompt, max_chars=300):
    """
    ユーザー質問とコンテキストを取得してプロンプトを作成

    Args:
        childcare_summary_data (dict): 乳児記録の平均データ
        user_prompt (str): AI質問
        max_chars (int): AI解答の最大文字数

    Returns:
        str: GeminiAIへリクエストするプロンプト
    """

    template = load_prompt_template("analysis_prompt.txt")

    childcare_summary_lines = "\n".join(
        [
            f"- {KEY_LABELS.get(key, key)}: {value}"
            for key, value in childcare_summary_data.items()
        ]
    )

    return (
        template.replace("{{period}}", "1週間")
        .replace("{{childcare_summary_lines}}", childcare_summary_lines)
        .replace("{{user_prompt}}", user_prompt)
        .replace("{{max_chars}}", str(max_chars))
    )
