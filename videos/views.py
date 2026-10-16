from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

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