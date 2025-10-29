from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Child,
    DiaryRecord,
)
from .forms import DiaryRecordForm
from .utils.diary_summarizer import diary_summarizer
from collections import defaultdict


@login_required
def diary_list(request, child_id):
    """
    ユーザーに子ども情報の削除

    Args:
        child_id (int): 子ども識別番号
    Returns:
        日記一覧画面
    """
    child = get_object_or_404(Child, pk=child_id)
    records = DiaryRecord.objects.filter(child=child).order_by("-time")

    # DiaryRecordテーブルのレコードを月毎にdict型にして取得
    diary_by_month = defaultdict(list)
    for r in records:
        month_label = r.time.strftime("%Y年%m月")
        diary_by_month[month_label].append(r)

    context = {
        "child": child,
        "diary_by_month": dict(diary_by_month),
    }
    return render(request, "diary/diary_list.html", context)


def diary_add(request, child_id):
    """
    日記の追加

    Args:
        child_id (int): 子ども識別番号
    Returns:
        日記記入画面
    """
    child = get_object_or_404(Child, pk=child_id)
    if request.method == "POST":
        form = DiaryRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.child = child
            record.summary = diary_summarizer(record.note)
            record.save()
            return redirect("diary_list", child_id=child.id)
    else:
        form = DiaryRecordForm()

    return render(request, "diary/diary_edit.html", {"form": form, "child": child})


def diary_edit(request, child_id, pk):
    """
    日記の編集
    Args:
        child_id (int): 子ども識別番号
        pk (int): 日記識別番号
    Returns:
        日記記入画面
    """
    child = get_object_or_404(Child, pk=child_id)
    record = get_object_or_404(DiaryRecord, pk=pk, child=child)
    if request.method == "POST":
        form = DiaryRecordForm(request.POST, instance=record)
        if form.is_valid():
            record.summary = diary_summarizer(record.note)
            form.save()
            return redirect("diary_list", child_id=child.id)
    else:
        form = DiaryRecordForm(instance=record)

    return render(request, "diary/diary_edit.html", {"form": form, "child": child})


def diary_delete(request, child_id, pk):
    """
    日記の削除
    Args:
        child_id (int): 子ども識別番号
        pk (int): 日記識別番号
    Returns:
        日記一覧画面
    """
    child = get_object_or_404(Child, pk=child_id)
    record = get_object_or_404(DiaryRecord, pk=pk, child=child)
    if request.method == "POST":
        record.delete()
    return redirect("diary_list", child_id=child.id)
