from django.contrib import admin
from .models import Product, Category, Comment, SubCategory, SuperCategory, Brand, BrandAdvertisement


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'image',
        'average_rating'
    )
    prepopulated_fields = {'slug':('name',)}

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'product', 'created_on', 'approved', "rating")
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, queryset):
        queryset.update(approved=True)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(SuperCategory)
admin.site.register(Brand)
admin.site.register(BrandAdvertisement)
