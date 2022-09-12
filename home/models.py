from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.


class LandingMarketingImage(models.Model):
    name = models.CharField(max_length=250, null = False, blank  = False)
    marketing_image = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.name

class SubscriptionEmail(models.Model):
    email = models.EmailField(max_length = 200)

    def __str__(self):
        return self.email

class JobCategory(models.Model):
    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"
    name = models.CharField(max_length = 100, null = False, blank = False)

    def __str__(self):
        return self.name

class JobOpportunity(models.Model):
    TIME_CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
    )
    class Meta:
        verbose_name = "Job Opportunity"
        verbose_name_plural = "Job Opportunities"
    name = models.CharField(max_length = 100, null = False, blank = False)
    category = models.ForeignKey(JobCategory, on_delete = models.CASCADE, null = True, related_name = "job_opportunity")
    location = models.CharField(max_length = 100, null = False, blank = False)
    pay = models.IntegerField( null = False, blank = False)
    slug = models.SlugField(null=True, blank = True, unique=True)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    decription = RichTextField()
    requirements = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('job_detail', kwargs={'jobopportunity_id':self.id, 'slug': self.slug})

class JobApplication(models.Model):
    job_opportunity = models.ForeignKey(JobOpportunity, on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 100, null = False, blank = False)
    email = models.EmailField(max_length = 100, null = False, blank = False)
    phone = models.IntegerField(null = False, blank = False)
    previous_position = models.CharField(max_length = 200, null = False, blank = False)
    education = models.CharField(max_length = 200, null = False, blank = False)
    experience_summary = models.TextField()
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='job_applications/', null = True)

    def __str__(self):
        return self.full_name
