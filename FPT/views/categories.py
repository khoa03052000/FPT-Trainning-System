from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import CategoryCreate
from FPT.models import Course, Category


@require_http_methods(["GET"])
@login_required
def manage_categories(request):
    if request.user.is_staff:
        categories = Category.objects.all()
        context = {
            "categories": categories
        }
        return render(request, "category.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def create_category(request):
    if request.user.is_staff:
        upload = CategoryCreate()
        if request.method == 'POST':
            check_category = Category.objects.get(name=request.POST["name"])
            if check_category:
                messages.warning(request, f"The category with name {check_category.name} is exist")
                return redirect("FPT:create-category")
            upload = CategoryCreate(request.POST)
            if upload.is_valid():
                upload.save()
                messages.success(request, "Create category success")
                return redirect('FPT:categories')
            else:
                messages.error(request, "Your form is not valid for create category")
                return redirect('FPT:categories')
        else:
            return render(request, 'category_create.html', {'upload_form': upload})
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def category_detail(request, category_id):
    if request.user.is_staff:
        category_id = int(category_id)
        try:
            category_self = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Not found category")
            return redirect("FPT:categories")
        context ={
            "category": category_self
        }
        return render(request, 'category_detail.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def update_category(request, category_id):
    if request.user.is_staff:
        category_id = int(category_id)
        try:
            category_self = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Not found category")
            return redirect("FPT:category-detail")
        if request.method == 'GET':
            category_form = CategoryCreate()
            context = {
                'upload_form': category_form,
                'category': category_self
            }
            return render(request, 'category_update.html', context)
        if request.method == 'POST':
            check_category = Category.objects.get(name=request.POST["name"])
            if check_category:
                messages.warning(request, f"The category with name {check_category.name} is exist")
                return redirect("FPT:category-detail", category_id=category_self.id)
            category_form = CategoryCreate(request.POST, instance=category_self)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Update category success")
                return redirect("FPT:category-detail", category_id=category_self.id)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def delete_category(request, category_id):
    if request.user.is_staff:
        category_id = int(category_id)
        try:
            category_self = Category.objects.get(id=category_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found category")
            return redirect('FPT:categories')
        category_self.delete()
        if request.method == "POST":
            return HttpResponse(status=204)
        messages.success(request, "Delete category success")
        return redirect("FPT:categories")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def search_category(request):
    if request.user.is_staff:
        if request.method == "POST":
            categories = Category.objects.filter(
                Q(name__icontains=request.POST["q"]) |
                Q(description__icontains=request.POST["q"])
            )
            if categories.exists():
                messages.success(
                    request, f"Search category success with {categories.count()} results"
                )
                context = {"categories": categories}
                return render(request, "category.html", context)

            messages.warning(request, f"Not found category {request.POST['q']}")
            context = {
                "categories": categories
            }
            return render(request, "category.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
