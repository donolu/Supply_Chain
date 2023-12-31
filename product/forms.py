from django import forms
from .models import Details, Transaction, Category, Subcategory, Batch
from widget_tweaks.templatetags.widget_tweaks import add_class


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("category_name", "category_code")
        labels = {
            "category_name": "Category Name",
            "category_code": "Category Code",
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields[
            "category_code"
        ].empty_label = "Enter Category code in '00001' format"


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ("name", "category_name", "subcategory_code", "description")
        labels = {
            "name": "Sub Category name",
            "category_name": "Parent Category",
            "subcategory_code": "Sub Category Code",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super(SubcategoryForm, self).__init__(*args, **kwargs)
        self.fields["category_name"].empty_label = "Select Parent Category"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Details
        fields = (
            "productname",
            "category_name",
            "sub_category",
            "sku",
            "unit",
            "description",
            "product_image",
            "status",
        )
        labels = {
            "productname": "Product Name",
            "category_name": "Category",
            "sub_category": "Sub Category",
            "unit": "Unit",
            "sku": "SKU",
            "product_image": "Product Image",
            "status": "Status",
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["sub_category"].queryset = Subcategory.objects.none()
        self.fields["category_name"].empty_label = "Choose Category"
        self.fields["sub_category"].empty_label = "Choose Sub Category"
        self.fields["unit"].empty_label = "Choose Unit"

        # Set the SKU field as readonly
        self.fields["sku"].widget.attrs["readonly"] = True

        # Set Category and SubCategory as queryset
        self.fields["category_name"].queryset = Category.objects.all()

        # Dynamically set the sub_category choices based on selected category
        if self.is_bound and "category_name" in self.data:
            try:
                category_id = int(self.data.get("category_name"))
                self.fields["sub_category"].queryset = Subcategory.objects.filter(
                    category_name_id=category_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields[
                "sub_category"
            ].queryset = self.instance.category_name.subcategory_set.order_by("name")

    def clean_sku(self):
        # Override the clean_sku method to preserve the sku value during form submission
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            return instance.sku
        else:
            return self.cleaned_data.get("sku")


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["product", "batch", "transaction_type", "quantity", "sale_id"]
        # Add other fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["batch"].queryset = Batch.objects.none()

        if "product" in self.data:
            try:
                product_id = int(self.data.get("product"))
                self.fields["batch"].queryset = Batch.objects.filter(
                    product_id=product_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["batch"].queryset = self.instance.product.productbatch_set

    def clean_sale_id(self):
        transaction_type = self.cleaned_data.get("transaction_type")
        sale_id = self.cleaned_data.get("sale_id")

        if transaction_type == "return_inward":
            # Check if the provided sale_id exists in the database
            if not Transaction.objects.filter(id=sale_id).exists():
                raise forms.ValidationError(
                    "Invalid Sale ID for Return Inward transaction."
                )

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get("transaction_type")
        sale_id = cleaned_data.get("sale_id")

        if transaction_type == "return_inward" and not sale_id:
            raise forms.ValidationError(
                "Please provide the Sale ID for Return Inward transactions."
            )
        elif transaction_type != "retun_inward" and sale_id:
            raise forms.ValidationError(
                "Sale ID should only be provided for Return Inward transactions."
            )

    def save(self, commit=True):
        transaction = super().save(commit=False)

        # Set the logged-in user as the timestamp
        if not transaction.id:  # Only set the timestamp if it's a new transaction
            # transaction.timestamp = timezone.now()
            transaction.updated_by = (
                self.request.user
            )  # Assuming 'self.request' is available

        if commit:
            transaction.save()

        return transaction
