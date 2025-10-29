from django.shortcuts import render, redirect, get_object_or_404
from kidlog.models import Child
from utils.gemini import gemini_generate
from .utils.summarizer import build_analysis_prompt
from utils.record_list import childcare_record_list
from django.utils import timezone


def chat_page(request, child_id):
    """
    質問内容よりAIにて回答を生成して取得する

    Args:
        child_id (int): 子ども識別番号
    Returns:
        AIChat画面
    """
    if "first_ai_question" in request.POST:
        request.session["chat_history"] = []
        prompt = request.POST.get("first_ai_question", "")
    else:
        prompt = request.POST.get("prompt", "")

    chat_history = request.session["chat_history"]

    if request.method == "POST":
        user_prompt = prompt.strip()
        if not chat_history:
            if user_prompt:
                child = get_object_or_404(Child, id=child_id)
                age_display = child.age_years_months
                age = f"{age_display[0]}歳{age_display[1]}ヶ月"
                today_time = timezone.now().date()
                childcare_summary_data = childcare_record_list(
                    child, today_time, "week", False
                )
                childcare_summary_data["age"] = age

                prompt = build_analysis_prompt(childcare_summary_data, user_prompt)

        else:
            # 直近の履歴をまとめてAIにコンテキストとして渡す
            history_text = ""
            for msg in chat_history[-10:]:
                if msg["role"] == "user":
                    role_name = "ユーザー"
                else:
                    role_name = "AI"
                history_text += f"{role_name}: {msg['text']}\n"

            prompt = f"{history_text}\nユーザー: {user_prompt}\nAI:"

        ai_response = gemini_generate(prompt)

        chat_history.append({"role": "user", "text": user_prompt})
        chat_history.append({"role": "ai", "text": ai_response})
        request.session["chat_history"] = chat_history
        request.session.modified = True

    context = {
        "child_id": child_id,
        "chat_history": chat_history,
    }

    return render(request, "ai_chat/ai_chat.html", context)
