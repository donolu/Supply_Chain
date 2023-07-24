from django.test import TestCase
from .forms import ProductForm  # Import your ProductForm class
from .models import Category, Subcategory  # Import your Category and Subcategory models


class ProductFormTestCase(TestCase):
    def test_subcategory_choices(self):
        # Create a category and subcategories to test with
        category = Category.objects.create(category_name="Test Category")
        subcategory1 = Subcategory.objects.create(
            name="Subcategory 1", category_name=category
        )
        subcategory2 = Subcategory.objects.create(
            name="Subcategory 2", category_name=category
        )

        # Simulate a form submission with the selected category
        form_data = {
            "productname": "Test Product",
            "category_name": category.pk,  # Set the selected category
        }
        form = ProductForm(data=form_data)

        # Call the subcategory_choices method with the form instance
        queryset = form.subcategory_choices(form)

        # Assert that the queryset contains the subcategories related to the selected category
        self.assertQuerysetEqual(
            queryset, [repr(subcategory1), repr(subcategory2)], ordered=False
        )


# Create your tests here.
