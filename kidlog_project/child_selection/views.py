from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Child
from .forms import ChildForm


@login_required
def child_selection_view(request):
    """
    ユーザーに紐づいた子ども選択画面

    Args:
    Returns:
        子ども選択画面
    """
    children = Child.objects.filter(user=request.user)
    return render(
        request, "child_selection/child_selection.html", {"children": children}
    )


# 子ども追加
def add_child_view(request):
    """
    ユーザーに紐づいた子どもの追加

    Args:
    Returns:
        子ども選択画面
    """
    if request.method == "POST":
        form = ChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            child.user = request.user
            child.save()
            children = Child.objects.filter(user=request.user)
            return render(
                request, "child_selection/child_selection.html", {"children": children}
            )
    else:
        form = ChildForm()
    return render(request, "child_selection/add_child.html", {"form": form})


def delete_child(request, child_id):
    """
    ユーザーに子ども情報の削除

    Args:
    Returns:
        子ども選択画面
    """
    child = get_object_or_404(Child, id=child_id)

    if request.method == "POST":
        child.delete()
        return redirect("child_selection")

    return redirect("child_selection")
