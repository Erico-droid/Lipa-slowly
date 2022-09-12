from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Category, SubCategory, Brand, BrandAdvertisement
from .forms import ProductForm, CommentForm
from django.http import JsonResponse
import random
from feeling_fragrant.settings import site_name
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from feeling_fragrant.settings import site_name, site_tagline, site_country, site_phone, site_address, site_minimum_buy, site_country_code
from itertools import chain
# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()

    Adcount = 0
    query = None
    categories = None
    sort = None
    direction = None
    brands = None
    brandAdv = None
    brand_logo = None
    all_categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    all_brands = Brand.objects.all()
    page_detail = " | All products"

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'subcategory':
                sortkey = 'subcategory__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = Product.objects.all()
            products = products.order_by(sortkey)
            page_detail = " | Sort by products by {} order " .format(sortkey)

        if 'subcategory' in request.GET:
            subcategory = request.GET['subcategory']
            subcategories = request.GET['subcategory'].split(',')
            products = Product.objects.all()
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = SubCategory.objects.filter(name__in=subcategories)
            page_detail = ' | {} Subcategory' .format(subcategory)

        if 'brand' in request.GET:
            brand = request.GET['brand']
            brands = request.GET['brand'].split(',')
            products = Product.objects.all()
            products = list(products.filter(brand__name__in=brands))
            brands = Brand.objects.filter(name__in=brands)
            page_detail = ' | {} brand' .format(brand)

            # displaying ads in between products
            i = 2
            n = i
            for brand in brands:
                adbrand = brand
                brandAdvs = list(BrandAdvertisement.objects.filter(brand=adbrand.id))
                while i < len(products):
                    if len(brandAdvs) < 1:
                        break
                    else:
                        products.insert(i, brandAdvs[0])
                        i += (n+1)
                        brandAdvs.pop(0)

        if 'category' in request.GET:
            category = request.GET['category']
            categories = request.GET['category'].split(',')
            products = Product.objects.all()
            brand = Brand.objects.all()
            products = subcategories.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            page_detail = ' | {} Category' .format(category)
            for category in categories:
                brand_logo = category.brand_category.all()

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
            page_detail = ' | Search results for {}' .format(query)
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'all_categories':all_categories,
        'current_subcategories': subcategories,
        'page_detail':page_detail,
        'current_brands':brands,
        'brands':all_brands,
        'brand_logo':brand_logo
    }
    return render(request, 'products/products.html', context)

def LikeView(request, pk):
    response = {}
    product = get_object_or_404(Product, id = request.POST.get('product_id'))
    liked = False
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        liked = False
        response['message'] = liked
        return render(request, 'products/includes/like-injection.html', locals())
    else:
        product.likes.add(request.user)
        liked = True
        response['message'] = liked
        return render(request, 'products/includes/like-injection.html', locals())

    return HttpResponseRedirect(reverse('product_detail', args=[str(pk)]))

def product_detail(request, product_id, slug):
    """ A view to show individual product details """


    product = get_object_or_404(Product, pk=product_id)
    meta_product_name = "{0} from {1}" .format(product.name, site_name)
    meta_product_description_list = ["Introducing {0}, the company that makes buying now and paying later a breeze! We offer original, one-of-a-kind products that are sure to please. Our fast delivery and user-friendly site make shopping with us a breeze. Plus, our convenient pay-in-installments option makes budgeting for your purchases easy. Whether you're looking for the perfect gift or treating yourself to something special, {0} has what you're looking for. So take a look around and see for yourself why we're the most wished-for retailer around {1}!" .format(site_name, site_country), "Introducing {0}, the company that brings you the best in original, fancy, and most wished for products! Our retail prices are unbeatable, and we offer fast delivery and easy installment plans so you can enjoy your new product as soon as possible. Our user-friendly site makes shopping for your perfect product a breeze, and our wide selection means you're sure to find exactly what you're looking for. Don't wait any longer, shop {0} today!" .format(site_name, site_country), "Looking for a luxurious and original gift that is sure to impress? Look no further than {0}. With our buy now pay later option, you can spread the cost of your purchase over time. With fast delivery and a user-friendly site, we make it easy to find and purchase the perfect gift." .format(site_name, site_country), "Introducing {0}, the company that brings you the best in original, fancy, and most-wished for products! Our retail prices are unbeatable, and we offer the convenience of buy now pay later and pay in installments options. Plus, our fast delivery ensures you'll receive your order quickly and efficiently. And our user-friendly site branding makes shopping with us a breeze!" .format(site_name, site_country)]

    meta_product_description = random.choice(meta_product_description_list)
    response_data = {}
    comments = product.comments.filter(approved=True)
    commented = None
    page_detail = " | {}" .format(product.name)
    try:
        for sub in product.subcategory.all():
            sim = list(Product.objects.filter(subcategory = sub).exclude(id=product_id))
            similar_products = random.sample(sim, 2)
            if not similar_products:
                similar_products = None
    except:
        for sub in product.subcategory.all():
            similar_products = list(Product.objects.filter(subcategory = sub).exclude(id=product_id))[:12]
    object = get_object_or_404(Product, id = product_id)
    total_likes = object.total_likes()

    liked = False
    if object.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == 'POST':
        try:
            comment_form = CommentForm(data=request.POST or None)
            rating = request.POST.get('rate')
            if comment_form.is_valid():
                comment_form.instance.email = request.user.email
                comment_form.instance.name = request.user.username
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.email = comment_form.instance.email
                comment.rating = rating
                commented = True
                comment.save()
                response_data['commented'] = True
        except:
            response_data['message'] = "There was an error"
        return JsonResponse(response_data)
    else:
        comment_form = CommentForm()

    context = {
        'product': product,
        'comments': comments,
        'commented': commented,
        'comment_form': comment_form,
        'total_likes' : total_likes,
        'liked':liked,
        'similar_products':similar_products,
        'page_detail':page_detail,
        'meta_product_name':meta_product_name,
        'meta_product_description':meta_product_description
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    page_detail = " | Add new product"
    template = 'products/add_product.html'
    context = {
        'form': form,
        'page_detail':page_detail
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    page_detail = " | Edit product {}" .format(product.name)
    context = {
        'form': form,
        'product': product,
        'page_detail':page_detail,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
