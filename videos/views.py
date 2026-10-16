from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse

from videos.forms import VideoForm

from .models import Category, Video


def is_main_admin(user):
    return (
        user.is_authenticated
        and user.is_active
        and user.is_superuser
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
def admin_dashboard(request):
    context = {
        "total_videos": Video.objects.count(),
        "published_videos": Video.objects.filter(
            is_published=True
        ).count(),
        "draft_videos": Video.objects.filter(
            is_published=False
        ).count(),
        "total_categories": Category.objects.count(),
        "recent_videos": Video.objects.select_related(
            "category"
        ).order_by("-created_at")[:5],
    }

    return render(
        request,
        "admin_dashboard/dashboard.html",
        context,
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
def add_video(request):
    if request.method == "POST":
        form = VideoForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            video = form.save()
            messages.success(
                request,
                f'La vidéo "{video.title}" a été ajoutée avec succès.',
            )
            return redirect(reverse("videos:add_video"))

        messages.error(
            request,
            "Le formulaire contient des erreurs. Vérifie les champs.",
        )
    else:
        form = VideoForm()

    return render(
        request,
        "admin_dashboard/add_video.html",
        {"form": form},
    )