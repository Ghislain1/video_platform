from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegistrationForm

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CategoryForm, VideoForm
from .models import Video

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

@user_passes_test(is_main_admin, login_url="/admin/login/")
def manage_videos(request):
    videos = Video.objects.select_related("category").all()

    search_query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")
    access_type = request.GET.get("access_type", "")

    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    if category_id.isdigit():
        videos = videos.filter(category_id=int(category_id))

    if status in ["published", "draft"]:
        videos = videos.filter(
            is_published=(status == "published")
        )

    if access_type in ["free", "paid"]:
        videos = videos.filter(access_type=access_type)

    context = {
        "videos": videos,
        "categories": Category.objects.all(),
        "search_query": search_query,
        "selected_category": category_id,
        "selected_status": status,
        "selected_access_type": access_type,
    }

    return render(
        request,
        "admin_dashboard/manage_videos.html",
        context,
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
def edit_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    if request.method == "POST":
        form = VideoForm(
            request.POST,
            request.FILES,
            instance=video,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Video updated successfully.",
            )
            return redirect("videos:manage_videos")
    else:
        form = VideoForm(instance=video)

    return render(
        request,
        "admin_dashboard/edit_video.html",
        {"form": form, "video": video},
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
@require_POST
def toggle_video_publication(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    video.is_published = not video.is_published
    video.save(update_fields=["is_published", "updated_at"])

    messages.success(
        request,
        "Video publication status updated.",
    )

    return redirect("videos:manage_videos")


@user_passes_test(is_main_admin, login_url="/admin/login/")
@require_POST
def delete_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.delete()

    messages.success(
        request,
        "Video deleted successfully.",
    )

    return redirect("videos:manage_videos")

@user_passes_test(is_main_admin, login_url="/admin/login/")
def manage_categories(request):
    categories = Category.objects.all()

    return render(
        request,
        "admin_dashboard/manage_categories.html",
        {"categories": categories}
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect("videos:manage_categories")
    else:
        form = CategoryForm()

    return render(
        request,
        "admin_dashboard/category_form.html",
        {"form": form, "page_title": "Add Category"}
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("videos:manage_categories")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "admin_dashboard/category_form.html",
        {"form": form, "page_title": "Edit Category"}
    )


@user_passes_test(is_main_admin, login_url="/admin/login/")
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if category.videos.exists():
        messages.error(
            request,
            "This category cannot be deleted because it contains videos."
        )
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")

    return redirect("videos:manage_categories")

def public_video_library(request):
    videos = Video.objects.filter(
        is_published=True
    ).select_related("category")

    categories = Category.objects.all()

    search_query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    access_type = request.GET.get("access", "").strip()

    # Search by title or description
    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    # Filter by category
    if category_id.isdigit():
        videos = videos.filter(category_id=int(category_id))

    # Filter free or paid videos
    if access_type in ["free", "paid"]:
        videos = videos.filter(access_type=access_type)

    context = {
        "videos": videos,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
        "selected_access": access_type,
    }

    return render(
        request,
        "videos/public_library.html",
        context
    )


def public_video_detail(request, video_id):
    video = get_object_or_404(
        Video.objects.select_related("category"),
        pk=video_id,
        is_published=True
    )

    return render(
        request,
        "videos/video_detail.html",
        {"video": video}
    )

def register_view(request):
    if request.user.is_authenticated:
        return redirect("videos:account")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully."
            )

            return redirect("videos:account")
    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("videos:account")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)

            return redirect("videos:account")
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": request.GET.get("next", "")
        }
    )


@login_required(login_url="videos:login")
def account_view(request):
    return render(
        request,
        "accounts/account.html",
        {"account_user": request.user}
    )


@login_required(login_url="videos:login")
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")

    return redirect("videos:public_library")