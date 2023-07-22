from django.db import models
from django.utils import timezone
# from django.core.files import File
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from io import BytesIO
from users.models import User





# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_code = models.CharField(max_length=50, unique=False, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)  # Set to current datetime on creation
    updated_on = models.DateTimeField(auto_now=True, blank=True)  # Set to current datetime on every save (insert or update)


    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_code = models.CharField(max_length=50, unique=False)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)  # Set to current datetime on creation
    updated_on = models.DateTimeField(auto_now=True, blank=True)  # Set to current datetime on every save (insert or update)

    def __str__(self):
        return self.name


class Details(models.Model):
    UNIT_TYPES = (
        ("piece", "Piece"),
        ("weight", "Weight"),
    )

    STATUS_TYPES = (
        ("active","Active"),
        ("disabled","Disabled"),
    )

    productname = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=10, unique=True, default="PT00001")
    barcode_image = models.ImageField(upload_to="barcodes/", blank=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=20, default='piece', choices=UNIT_TYPES)
    status = models.CharField(max_length=10, default='active', choices=STATUS_TYPES)
    description = models.TextField(blank=True, null=True)
    product_image = models.ImageField(upload_to="product_imgs/", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Set to current datetime on creation
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)  # Set to current datetime on every save (insert or update)


    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_sku()

        if not self.barcode_image:
            self.generate_barcode()

        super().save(*args, **kwargs)

    def generate_sku(self):
        # Generate the SKU based on the last generated SKU in the database
        last_sku = Details.objects.order_by("-id").values_list("sku", flat=True).first()

        if last_sku:
            # Get the number part of the last product's SKU
            last_sku_number = int(last_sku[2:])  # Extract the number part from the SKU
            # Generate the next number part by incrementing the last number
            new_sku_number = last_sku_number + 1

            # Create the new SKU by combining the prefix 'PT' and the new number
            new_sku = f"PT{str(new_sku_number).zfill(5)}"  # Generate the new SKU

        else:
            # If there are no existing products, start with the initial number
            new_sku = "PT00001"

        return new_sku
    

    def generate_barcode(self):
        # Generate the barcode
        code128 = get_barcode_class("code128")        
        barcode_img = code128(self.sku, writer=ImageWriter())

        # Create a BytesIO object to store the barcode image content
        barcode_buffer = BytesIO()

        # Save the barcode image to the BytesIO object
        barcode_img.write(barcode_buffer)

        # Set the filename for the barcode image
        filename = f"{self.sku}.png"

        # Save the barcode image content to the barcode_image field
        self.barcode_image.save(filename, barcode_buffer)

        """        # Open a file in write-binary mode and save the barcode image
        with open(f"media/barcodes/{filename}", "wb") as f:
            barcode_img.write(f)

        # Save the barcode image field in the model instance
        self.barcode_image.save(filename, File(f)) """



class Stock(models.Model):
    product = models.OneToOneField(Details, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    last_updated = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("sale", "Sale"),
        ("purchase", "Purchase"),
        ("return_inward","Return Inward"),
        ("return_outward","Return Outward"),
        ("disposal","Disposal"),
    )
    tran_date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Details, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    sale_id = models.IntegerField(null=True, blank=True)  # Related sale ID for Return Inward
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.product} ({self.quantity})"
