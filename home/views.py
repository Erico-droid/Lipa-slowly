from django.shortcuts import render, get_object_or_404
from products.models import Category, SubCategory, Product, Brand
from .models import LandingMarketingImage, JobOpportunity, JobCategory
import random
from feeling_fragrant.settings import site_tagline
from django.contrib import messages
from .forms import EmailSubscriptionForm, JobApplicationForm

# from background_task import background
# Create your views here.

# @background(schedule=60)
# def get_random_subcategories():
#     timing = [18, 19, 0]
#     now = datetime.datetime.now()
#     data = [now.hour, now.minute, now.second]
#     if data == timing:
#         print("hello world")

def index(request):
    """ A view to return the index page """
    if request.method == "POST":
        form = EmailSubscriptionForm(request.POST)
        email_value = request.POST.get('email')
        if form.is_valid():
            email_file = open('email_file.txt', 'a')
            email_file.write("{}\n" .format(str(email_value)))
            email_file.close()
            form.save()
            messages.success(request, "Email has been received Successfully")
        else:
            messages.error(request, 'Failed to add the email, make sure you entered the correct one.')

    form = EmailSubscriptionForm()
    category = Category.objects.all()
    all_brands = list(Brand.objects.all())
    every_brand = Brand.objects.all()
    subCategory = SubCategory.objects.all()
    sub_category = list(SubCategory.objects.all())
    products = list(Product.objects.all())
    trending_products = random.sample(products, 12)
    display_category = random.sample(sub_category, 4)
    random_subcategory = random.sample(sub_category, 1)
    brand = random.sample(all_brands, 1)
    for rand_sub in random_subcategory:
        sub = rand_sub
    display_products_all = Product.objects.filter(subcategory = sub)
    print(display_products_all)
    trending_products_count = len(trending_products)
    dummy = Product.objects.filter(id=5)
    marketing_image = LandingMarketingImage.objects.all()[:1]
    page_detail = " | {}" .format(site_tagline)
    # print(request.user.likes.count())
    context = {
        "category": category,
        "subCategory":subCategory,
        "products":products,
        "trending_products":trending_products,
        "trending_products_count":trending_products_count,
        "display_category":display_category,
        'dummy':dummy,
        'marketing_image':marketing_image,
        'display_products_all':display_products_all,
        'sub':sub,
        'page_detail':page_detail,
        'form':form,
        'brand':brand,
        'every_brand':every_brand
    }
    return render(request, 'home/index.html', context)

def termsandconditions(request):
    page_detail = " | Terms and conditions"
    context = {'page_detail':page_detail}
    return render(request, 'home/terms-and-conditions.html', context)

def privacypolicy(request):
    page_detail = " | Privacy policy"
    context = {'page_detail':page_detail}
    return render(request, 'home/privacy-policy.html', context)

def frequentlyaskedquestions(request):
    page_detail = " | Frequently asked questions"
    context = {'page_detail':page_detail}
    return render(request, 'home/frequently-asked-questions.html', context)

def careers(request):
    jobs = JobOpportunity.objects.all()
    all_categories = JobCategory.objects.all()
    page_detail = " | Careers"
    categories = None
    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category']
            categories = request.GET['category'].split(',')
            job_category = get_object_or_404(JobCategory, name=category)
            jobs = jobs.filter(category=job_category)
            categories = JobCategory.objects.filter(name__in=categories)
            all_categories = all_categories.exclude(id=categories[0].id)
            page_detail = ' | {} jobs' .format(category)
    context = {'page_detail':page_detail,
                'jobs':jobs,
                'current_categories':categories,
                'all_categories':all_categories
    }
    return render(request, 'home/careers.html', context)

def job(request, jobopportunity_id, slug):
    job_opportunity = get_object_or_404(JobOpportunity, pk=jobopportunity_id)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.job_opportunity = job_opportunity
            form.save()
            name = request.POST.get('full_name').split()[0]
            email = request.POST.get('email')
            messages.success(request, "{0}, your job application has been received Successfully. Our team will contact you regarding this role to your email '{1}' shortly." .format(name, email))
        else:
            print(form.errors.as_data())
            messages.error(request, 'Your job submission failed, recheck your application.')

    form = JobApplicationForm(request.POST or None, request.FILES or None)
    job_categories = JobCategory.objects.all()
    similar_jobs = JobOpportunity.objects.filter(category=job_opportunity.category).exclude(id=jobopportunity_id)
    print(job_opportunity.get_absolute_url)
    page_detail = " | Careers"
    context = { 'page_detail':page_detail,
                'job_opportunity':job_opportunity,
                'job_categories':job_categories,
                'similar_jobs':similar_jobs,
                'form':form
    }
    return render(request, 'home/det_careers.html', context)
