from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
import random, string

class SuperCategory(models.Model):
    class Meta:
        verbose_name = "Super Category"
        verbose_name_plural = "Super Categories"
    name = models.CharField(max_length=254)
    image = models.ImageField(upload_to = "super_category_image/", null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    super_category = models.ForeignKey(SuperCategory, on_delete = models.CASCADE, null = True, related_name="category")
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(upload_to = "category_image/", null=True, blank=True)
    icon = models.ImageField(upload_to = "category_icon/", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Brand(models.Model):
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    name = models.CharField(max_length=254, null=False, blank=False)
    category = models.ManyToManyField(Category, related_name = 'brand_category')
    logo = models.ImageField(upload_to = "brand_logos/", null=True, blank=True)
    slogan = models.CharField(max_length=24, null=True, blank=True)
    main_image = models.ImageField(upload_to = "brand_main_image/", null=True, blank=True)

    def __str__(self):
        return self.name

class BrandAdvertisement(models.Model):
    class Meta:
        verbose_name = "Brand avertisement"
        verbose_name_plural = "Brand advertisements"

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="advertise_product", null = True)
    image_one = models.ImageField(upload_to = "brand_adv_images/", null=True, blank=True)
    ad = models.BooleanField(default = True, null = False)

    def __str__(self):
        return self.product.name

class SubCategory(models.Model):
    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=5, null = True, blank = True)
    image = models.ImageField(upload_to = "subcategory_image/", null=True, blank=True)
    category = models.ManyToManyField('Category', related_name="subcategory")

    def __str__(self):
        return self.name


class Product(models.Model):
    subcategory = models.ManyToManyField('Subcategory', related_name = "products_subcategory")
    sku = models.CharField(max_length=254, null=False, blank=False, unique = True)
    slug = models.SlugField(null=True, blank = True, unique=True)
    name = models.CharField(max_length=254)
    available = models.BooleanField(default = True)
    description = RichTextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_brand", blank = True, null = True)
    additional_description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slow_price = models.DecimalField(max_digits=10, decimal_places=2, default = None, null = True, blank = True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name = 'likes')
    average_rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rating_sorting = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    youtube_video_url = models.CharField(max_length = 254, null = True, blank = True, default = "https://www.youtube.com/embed/Jfrjeg26Cwk")

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

    def average_rating(self):
        for x in list(self.comments.all().values('approved')):
            if x['approved'] == True:
                # might need to add .values('approved') below after testing
                rating = round(self.comments.all().values('approved').aggregate(Sum('rating'))['rating__sum']/self.comments.count())
                self.rating_sorting = rating
                return rating

    def save(self, *args, **kwargs):
        self.slow_price = float(self.price) * 0.45
        self.sku = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
      return reverse('product_detail', kwargs={'product_id':self.id, 'slug': self.slug})

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    rating = models.IntegerField(default = 1, null=True, blank=True)
    reply = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.user}"
