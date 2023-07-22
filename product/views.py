from django.shortcuts import render, redirect
from .forms import ProductForm, TransactionForm, CategoryForm, SubcategoryForm
from .models import Details, Stock, Transaction, Category, Subcategory
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime

# Create your views here.


@login_required
def category_list(request):
    context = {"category_list": Category.objects.all()}
    return render(request, "product/categorylist.html", context)


@login_required
def category_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = CategoryForm()
        else:
            category = Category.objects.get(pk=id)
            form = CategoryForm(instance=category)
        return render(request, "product/addcategory.html", {"form": form})
    else:
        # Retrieve the user field from the POST data
        user_id = request.POST.get("user")
        if id == 0:
            form = CategoryForm(request.POST)
        else:
            category = Category.objects.get(pk=id)
            form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(
                commit=False
            )  # Save the form, but don't commit to the database yet
            category.created_by = (
                request.user
            )  # Set the created_by field to the logged-in user
            category.created_on = datetime.datetime.now()
            form.save()
        return redirect("category_list")


@login_required
def category_delete(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    return redirect("category_list")


@login_required
def subcategory_list(request):
    subcategories = Subcategory.objects.order_by("pk")

    # Create a Paginator instance and specify the number of items per page
    paginator = Paginator(subcategories, request.GET.get("per_page", 6))

    # Get the current page number from the request
    page_number = request.GET.get("page")

    # Retrieve the page using the page number
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }
    return render(request, "product/subcategorylist.html", context)


@login_required
def subcategory_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = SubcategoryForm()
        else:
            subcategory = Subcategory.objects.get(pk=id)
            form = SubcategoryForm(instance=subcategory)
        return render(request, "product/addsubcategory.html", {"form": form})
    else:
        if id == 0:
            form = SubcategoryForm(request.POST)
        else:
            subcategory = Subcategory.objects.get(pk=id)
            form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.created_by = request.user
            subcategory.updated_on = datetime.datetime.now()
            form.save()

        return redirect("subcategory_list")


@login_required
def subcategory_delete(request, id):
    subcategory = Subcategory.objects.get(pk=id)
    subcategory.delete()
    return redirect("subcategory_list")


def getsubcategories(request):
    category_id = request.GET.get("category_id")
    subcategories = Subcategory.objects.filter(category_name_id=category_id).values(
        "id", "name"
    )
    return JsonResponse(list(subcategories), safe=False)


@login_required
def product_list(request):
    product_list = Details.objects.order_by("pk")

    # Create a Paginator instance and specify the number of items per page
    paginator = Paginator(product_list, request.GET.get("per_page", 6))

    # Get the current page number from the request
    page_number = request.GET.get("page")

    # Retrieve the page using the page number
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }
    return render(request, "product/productlist.html", context)


@login_required
def product_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ProductForm()
        else:
            product = Details.objects.get(pk=id)
            form = ProductForm(instance=product)
        return render(request, "product/addproduct.html", {"form": form})
    else:
        if id == 0:
            form = ProductForm(request.POST, request.FILES)
        else:
            product = Details.objects.get(pk=id)
            form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.updated_on = datetime.datetime.now()
            form.save()
        return redirect("product_list")


@login_required
def product_delete(request, id):
    product = Details.objects.get(pk=id)
    product.delete()
    return redirect("product_list")


@login_required
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            product = transaction.product
            stock = product.stock

            # Upddate stock quantitiy based on transction type
            if transaction.transaction_type == "sale":
                stock.quantity -= transaction.quantity
            elif transaction.transaction_type == "purchase":
                stock.quantity += transaction.quantity
            elif transaction.transaction_type == "return_inward":
                stock.quantity += 0
            elif transaction.transaction_type == "return_outward":
                stock.quantity -= transaction.quantity
            elif transaction.transaction_type == "disposal":
                stock.quantity -= transaction.quantity

            stock.save()
            transaction.save()

            return redirect("transaction_list")
    else:
        form = TransactionForm()
    return render(request, "/product/transaction_create.html", {"form": form})


@login_required
def transaction_list(request):
    context = {"transctions": Transaction.objects.all()}
    return render(request, "/product/transaction_list.html"), context
