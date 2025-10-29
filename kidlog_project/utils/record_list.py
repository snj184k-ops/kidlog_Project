from django.db.models import Avg, Count, Sum, F, ExpressionWrapper, DurationField
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from kidlog.models import (
    HtmtRecord,
    MilkRecord,
    SleepRecord,
    PoopRecord,
    PeeRecord,
    TemperatureRecord,
    FoodRecord,
)
from datetime import date

from django.db.models.functions import TruncDate


def childcare_record_list(child, today, mode, growth_flg):
    """
    乳児記録一覧について、リクエストに応じた期間の平均を取得してレスポンスする

    Args:
        child (Childクラス): 子ども情報
        today (datetime): 当日時間
        mode (str): 期間
        growth_flg (bool): 身長・体重データの取得範囲
    Returns:
        dict: 乳児記録一覧
    """
    if mode == "week":
        start_date = today - timedelta(days=7)
    elif mode == "month":
        start_date = today - timedelta(days=30)
    else:
        start_date = today

    record_dict = {
        "avg_milk": _avg_milk(child, start_date),
        "avg_poop": _avg_poop(child, start_date),
        "avg_pee": _avg_pee(child, start_date),
        "avg_sleep": _avg_sleep(child, start_date),
        "avg_temp": _avg_temp(child, start_date),
        "avg_food": _avg_food(child, start_date),
        "menu_list": _menu_list(child, start_date),
    }
    if growth_flg:
        record_dict["growth_chart"] = _get_growth_chart_view(child, growth_flg)
    else:
        htmt_data = _get_growth_chart_view(child, growth_flg)
        record_dict["height_data"] = htmt_data["height_data"][0]
        record_dict["weight_data"] = htmt_data["weight_data"][0]
    return record_dict


def _get_growth_chart_view(child, growth_flg):
    """
    身長体重の記録一覧をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        growth_flg (bool): 身長・体重データの取得範囲
    Returns:
        dict: 身長体重記録
    """
    labels = ["0ヶ月前"]
    height_data = []
    weight_data = []

    if HtmtRecord.objects.exists():
        today_record = HtmtRecord.objects.filter(child=child).latest("date")
        height_data.append(today_record.height if today_record else None)
        weight_data.append(today_record.weight if today_record else None)

        # dashboard作画用の場合はtrue,ai用の場合はfalse
        if growth_flg:
            records = _htmt_records(child)

            months_list = [1, 3, 6, 9, 12]

            for m in months_list:
                record = records[m]
                if record:
                    labels.append(f"{m}ヶ月前")
                    height_data.append(record.height)
                    weight_data.append(record.weight)

    return {
        "labels": labels,
        "height_data": height_data,
        "weight_data": weight_data,
    }


def _htmt_records(child):
    """
    対象期間の身長体重のデータをレスポンスする

    Args:
        child (Childクラス): 子ども情報
    Returns:
        list: 身長体重記録
    """
    today = date.today()
    results = {}

    # チェックしたい月数
    months_list = [1, 3, 6, 9, 12]

    for m in months_list:
        target_date = today + relativedelta(months=-m)

        qs = HtmtRecord.objects.filter(
            child=child,
            date__year=target_date.year,
            date__month=target_date.month,
        )

        if qs.exists():
            record = qs.latest("date")
            results[m] = record
        else:
            results[m] = None
    return results


def _avg_milk(child, start_date):
    """
    対象期間の平均ミルク量をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 1日あたりの平均ミルク量
    """
    milk_per_day = (
        MilkRecord.objects.filter(child=child, time__date__gte=start_date)
        .annotate(day=TruncDate("time"))
        .values("day")
        .annotate(total=Sum("amount"))
    )
    avg_milk = round(milk_per_day.aggregate(avg=Avg("total"))["avg"] or 0, 1)
    return avg_milk


def _avg_poop(child, start_date):
    """
    対象期間のうんち回数をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 1日あたりの平均うんち回数
    """
    poop_per_day = (
        PoopRecord.objects.filter(child=child, time__date__gte=start_date)
        .annotate(day=TruncDate("time"))
        .values("day")
        .annotate(count=Count("id"))
    )
    avg_poop = round(poop_per_day.aggregate(avg=Avg("count"))["avg"] or 0, 1)
    return avg_poop


def _avg_pee(child, start_date):
    """
    対象期間のおしっこ回数をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 1日あたりの平均おしっこ回数
    """
    pee_per_day = (
        PeeRecord.objects.filter(child=child, time__date__gte=start_date)
        .annotate(day=TruncDate("time"))
        .values("day")
        .annotate(count=Count("id"))
    )
    avg_pee = round(pee_per_day.aggregate(avg=Avg("count"))["avg"] or 0, 1)
    return avg_pee


def _avg_sleep(child, start_date):
    """
    対象期間の睡眠時間をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 1日あたりの平均睡眠時間
    """
    sleep_per_day = (
        SleepRecord.objects.filter(child=child, start_time__date__gte=start_date)
        .annotate(
            duration=ExpressionWrapper(
                F("end_time") - F("start_time"),
                output_field=DurationField(),
            )
        )
        .annotate(day=TruncDate("start_time"))
        .values("day")
        .annotate(total=Sum("duration"))
    )
    avg_sleep_td = sleep_per_day.aggregate(avg=Avg("total"))["avg"]
    avg_sleep_hours = round(
        (avg_sleep_td.total_seconds() / 3600) if avg_sleep_td else 0, 1
    )
    return avg_sleep_hours


def _avg_temp(child, start_date):
    """
    対象期間の温度をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 1日あたりの平均温度
    """
    temp_per_day = (
        TemperatureRecord.objects.filter(child=child, time__date__gte=start_date)
        .annotate(day=TruncDate("time"))
        .values("day")
        .annotate(avg_temp=Avg("temperature"))
    )
    avg_temp = round(temp_per_day.aggregate(avg=Avg("avg_temp"))["avg"] or 0, 1)
    return avg_temp


def _avg_food(child, start_date):
    """
    対象期間の食事回数をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 1日あたりの平均食事回数
    """
    food_per_day = (
        FoodRecord.objects.filter(child=child, time__date__gte=start_date)
        .annotate(day=TruncDate("time"))
        .values("day")
        .annotate(count=Count("id"))
    )
    avg_food = round(food_per_day.aggregate(avg=Avg("count"))["avg"] or 0, 1)
    return avg_food


def _menu_list(child, start_date):
    """
    対象期間の食事内容をレスポンスする

    Args:
        child (Childクラス): 子ども情報
        start_date (datetime): 取得開始期間
    Returns:
        list: 食事内容
    """
    top_menus = (
        FoodRecord.objects.filter(child=child, time__date__gte=start_date)
        .values("menu")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")[:3]
    )
    menu_list = ", ".join([m["menu"] for m in top_menus]) or "なし"
    return menu_list
