from django.contrib import admin
from .models import LandingMarketingImage, SubscriptionEmail, JobApplication, JobOpportunity, JobCategory
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'time',
        'pay'
    )
    prepopulated_fields = {'slug':('name',)}

admin.site.register(LandingMarketingImage)
admin.site.register(SubscriptionEmail)
admin.site.register(JobApplication)
admin.site.register(JobOpportunity, JobOpportunityAdmin)
admin.site.register(JobCategory)
