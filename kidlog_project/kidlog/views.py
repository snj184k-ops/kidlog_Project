from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import (
    Child,
    MilkRecord,
    SleepRecord,
    PoopRecord,
    PeeRecord,
    TemperatureRecord,
    FoodRecord,
)
from .forms import (
    MilkRecordForm,
    SleepRecordForm,
    PeeRecordForm,
    PoopRecordForm,
    TemperatureRecordForm,
    FoodRecordForm,
    HtmtRecordForm,
)
from diary.forms import DiaryRecordForm
from diary.utils.diary_summarizer import diary_summarizer
from utils.record_list import childcare_record_list


@login_required
def dashboard(request, child_id):
    """
    dashboard画面遷移及び各種レコード登録

    Args:
        child_id (int): 子ども識別番号
    Returns:
        dashboard画面
    """
    child = get_object_or_404(Child, id=child_id)

    if request.method == "POST":
        if "htwt_record" in request.POST:
            form = HtmtRecordForm(request.POST, prefix="htmt")
            if form.is_valid():
                rec = form.save(commit=False)
                rec.child = child
                rec.save()
            return redirect("dashboard", child_id=child.id)

        elif "diary_record" in request.POST:
            form = DiaryRecordForm(request.POST, prefix="diary")
            if form.is_valid():
                rec = form.save(commit=False)
                rec.summary = diary_summarizer(rec.note)
                rec.child = child
                rec.save()
            return redirect("dashboard", child_id=child.id)

        elif "infant_record" in request.POST:
            forms = [
                MilkRecordForm(request.POST, prefix="milk"),
                SleepRecordForm(request.POST, prefix="sleep"),
                PoopRecordForm(request.POST, prefix="poop"),
                PeeRecordForm(request.POST, prefix="pee"),
                TemperatureRecordForm(request.POST, prefix="temp"),
                FoodRecordForm(request.POST, prefix="food"),
            ]
            for form in forms:
                if form.is_valid():
                    rec = form.save(commit=False)
                    rec.child = child
                    rec.save()
            return redirect("dashboard", child_id=child.id)

    else:
        forms = {
            "diary_form": DiaryRecordForm(prefix="diary"),
            "htmt_form": HtmtRecordForm(prefix="htmt"),
            "milk_form": MilkRecordForm(prefix="milk"),
            "sleep_form": SleepRecordForm(prefix="sleep"),
            "poop_form": PoopRecordForm(prefix="poop"),
            "pee_form": PeeRecordForm(prefix="pee"),
            "temp_form": TemperatureRecordForm(prefix="temp"),
            "food_form": FoodRecordForm(prefix="food"),
            "htmt_form": HtmtRecordForm(prefix="htmt"),
        }
    today_time = timezone.now().date()
    mode = request.GET.get("mode", "today")

    context = {
        "child": child,
        "mode": mode,
        "record_dict": childcare_record_list(child, today_time, mode, True),
        **forms,
    }

    return render(request, "kidlog/dashboard.html", context)


def baby_record_add(request, child_id):
    """
    乳児記録登録

    Args:
        child_id (int): 子ども識別番号
    Returns:
        乳児記録一覧画面 or 乳児記録登録画面
    """
    child = get_object_or_404(Child, id=child_id)

    if request.method == "POST":
        forms = [
            MilkRecordForm(request.POST, prefix="milk"),
            SleepRecordForm(request.POST, prefix="sleep"),
            PoopRecordForm(request.POST, prefix="poop"),
            PeeRecordForm(request.POST, prefix="pee"),
            TemperatureRecordForm(request.POST, prefix="temp"),
            FoodRecordForm(request.POST, prefix="food"),
        ]
        for form in forms:
            if form.is_valid():
                rec = form.save(commit=False)
                rec.child = child
                rec.save()
        return redirect("baby_record_overview", child_id=child.id)
    else:
        forms = {
            "milk_form": MilkRecordForm(prefix="milk"),
            "sleep_form": SleepRecordForm(prefix="sleep"),
            "poop_form": PoopRecordForm(prefix="poop"),
            "pee_form": PeeRecordForm(prefix="pee"),
            "temp_form": TemperatureRecordForm(prefix="temp"),
            "food_form": FoodRecordForm(prefix="food"),
        }

    return render(request, "kidlog/baby_record_add.html", {"child": child, **forms})


def baby_record_overview(request, child_id):
    """
    乳児記録一覧表示

    Args:
        child_id (int): 子ども識別番号
    Returns:
        乳児記録一覧画面
    """
    child = get_object_or_404(Child, id=child_id)
    today = timezone.now().date()

    # 今日の全レコードを取得
    milk = MilkRecord.objects.filter(child=child, time__date=today)
    sleep = SleepRecord.objects.filter(child=child, start_time__date=today)
    poop = PoopRecord.objects.filter(child=child, time__date=today)
    pee = PeeRecord.objects.filter(child=child, time__date=today)
    temp = TemperatureRecord.objects.filter(child=child, time__date=today)
    food = FoodRecord.objects.filter(child=child, time__date=today)

    # 共通フォーマットに変換
    timeline = []

    for r in milk:
        timeline.append(
            {
                "time": r.time,
                "type": "授乳",
                "icon": "🍼",
                "content": f"{r.amount}ml {r.note or ''}",
            }
        )
    for r in sleep:
        timeline.append(
            {"time": r.start_time, "type": "睡眠開始", "icon": "😴", "content": ""}
        )
        timeline.append(
            {"time": r.end_time, "type": "睡眠終了", "icon": "😴", "content": ""}
        )
    for r in poop:
        timeline.append(
            {"time": r.time, "type": "うんち", "icon": "💩", "content": r.note or ""}
        )
    for r in pee:
        timeline.append(
            {"time": r.time, "type": "おしっこ", "icon": "🚽", "content": r.note or ""}
        )
    for r in temp:
        timeline.append(
            {
                "time": r.time,
                "type": "体温",
                "icon": "🌡️",
                "content": f"{r.temperature}℃ {r.note or ''}",
            }
        )
    for r in food:
        timeline.append(
            {
                "time": r.time,
                "type": "離乳食",
                "icon": "🍚",
                "content": f"{r.menu} {r.amount or ''} {r.note or ''}",
            }
        )

    # 時間でソート
    timeline = sorted(timeline, key=lambda x: x["time"])

    context = {
        "child": child,
        "today": today,
        "timeline": timeline,
    }
    return render(request, "kidlog/baby_record_overview.html", context)
