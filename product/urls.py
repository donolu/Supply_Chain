from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.product_form, name="product_insert"
    ),  # get and post req. for insert operation
    path(
        "<int:id>/", views.product_form, name="product_update"
    ),  # get and post req. for update operation
    path("delete/<int:id>/", views.product_delete, name="product_delete"),
    path(
        "list/", views.product_list, name="product_list"
    ),  # get req. to retrieve and display all records
    path("create_category/", views.category_form, name="category_form"),
    path("create_category/<int:id>/", views.category_form, name="category_update"),
    path("category_list/", views.category_list, name="category_list"),
    path("category_delete/<int:id>/", views.category_delete, name="category_delete"),
    path("create_subcategory/", views.subcategory_form, name="subcategory_form"),
    path(
        "create_subcategory/<int:id>/",
        views.subcategory_form,
        name="subcategory_update",
    ),
    path("subcategory_list/", views.subcategory_list, name="subcategory_list"),
    path(
        "subcategory_delete/<int:id>/",
        views.subcategory_delete,
        name="subcategory_delete",
    ),
    path("getsubcategories/", views.getsubcategories, name="getsubcategories"),
    path("create_product/", views.product_form, name="product_form"),
    path("create_product/<int:id>/", views.product_form, name="product_update"),
    path("product_list/", views.product_list, name="product_list"),
    path("product_delete/<int:id>/", views.product_delete, name="product_delete"),
    path("product_detail/<int:pk>/", views.product_detail, name="product-detail"),
]
