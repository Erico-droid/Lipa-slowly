from products.models import Product, Category, SubCategory, SuperCategory
import random
from feeling_fragrant.settings import site_name, site_email, site_tagline, site_country, site_phone, site_address, site_minimum_buy, site_country_code
from django.urls import resolve
from .forms import EmailSubscriptionForm

def base_menu(request):
    email_sub_form = EmailSubscriptionForm()
    current_url = resolve(request.path_info).url_name
    base_categories = Category.objects.all()
    base_subcategories = SubCategory.objects.all()
    base_supercategories = SuperCategory.objects.all()
    base_products = Product.objects.all()
    meta_name_list = ["{} | The best way to buy on credit" .format(site_name), "{} | Pay As You Go. Exact Date." .format(site_name), "{} | Totally Secure" .format(site_name)]
    meta_description_list = ["Friendly pay in installments for a year at your comfort in {}" .format(site_country), "With {}, you can shop online and pay for your purchases in installments. Your credit information is safely stored and never disclosed, so that only you have access to your data." .format(site_name), "We are the easiest way to pay in installments with the exact date of each payment. So, you can make payments and shop now in {}." .format(site_country)]
    meta_name = random.choice(meta_name_list)
    meta_description = random.choice(meta_description_list)
    try:
        favourites = request.user.likes.all()
    except:
        favourites = "Login to access your favourites"
    context = {'base_categories':base_categories,
                'base_subcategories':base_subcategories,
                'base_products':base_products,
                'favourites':favourites,
                'meta_name':meta_name,
                'meta_description':meta_description,
                'current_url':current_url,
                'site_email':site_email,
                'email_sub_form':email_sub_form,
                'base_supercategories':base_supercategories
                }
    return context
