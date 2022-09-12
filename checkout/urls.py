from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
    # path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    # path('online/lipa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    #
    # # register, confirmation, validation and callback urls
    # path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    # path('c2b/simulate', views.simulate_c2btransaction, name="simulate"),
    # path('c2b/status', views.check_payment_status, name="payment_status"),
    # path('c2b/transaction', views.get_transaction, name="get_transaction"),
    # path('c2b/confirmation', views.confirmation, name="confirmation"),
    # path('c2b/validation', views.validation, name="validation"),
    # path('c2b/callback', views.call_back, name="call_back"),
]

# return round(self.comments.all().aggregate(Sum('rating'))['rating__sum']/self.comments.count())
