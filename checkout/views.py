from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core import serializers
from .forms import OrderForm
from .models import Order, OrderLineItem, MpesaPayment
from django.http import JsonResponse, HttpResponseRedirect
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents
from django.views.decorators.csrf import csrf_exempt
import time
from requests.auth import HTTPBasicAuth
import requests
import stripe
import json
# from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
import datetime
import base64
from decimal import *

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # pid = request.POST.get('client_secret').split('_secret')[0]
            # order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill the form with any info the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

# def getAccessToken(request):
#     consumer_key = '4A9Qvlj99deGpDyDDHRnA9JCdAWxmyjs' #copy hfs consumer key
#     consumer_secret = '9m2vjCRX0I3TeyFj' #copy hfs consumer secret
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#     r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']
#     return HttpResponse(validated_mpesa_access_token)
#
# def lipa_na_mpesa_online(request):
#     response_data = {}
#     # order_number = request.session.get('order_number')
#     # order = get_object_or_404(Order, order_number=order_number)
#     # print('*******************', order.grand_total, '*******************')
#     # transaction_id = None
#     if request.method == "POST":
#         bag = request.session.get('bag', {})
#         # order = get_object_or_404(Order, order_number=order_number)
#         MpesaNo = request.POST.get('mpesaNumber')
#         response_data['message'] = "Check your phone for ussd prompt to complete the payment."
#         access_token = MpesaAccessToken.validated_mpesa_access_token
#         api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#         headers = {"Authorization": "Bearer %s" % access_token}
#         request = {
#             "ShortCode": LipanaMpesaPpassword.Business_short_code,
#             "Password": LipanaMpesaPpassword.decode_password,
#             "Timestamp": LipanaMpesaPpassword.lipa_time,
#             "CommandID": "CustomerBuyGoodsOnline",
#             "Amount": 1,
#             "PartyA": MpesaNo,  # replace with your phone number to get stk push
#             "PartyB": LipanaMpesaPpassword.Business_short_code,
#             "Msisdn": MpesaNo,  # replace with your phone number to get stk push
#             "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
#             "AccountReference": "Kijana",
#             "TransactionDesc": "Get the money first."
#         }
#         response = requests.post(api_url, json=request, headers=headers)
#         json_response = json.loads(response.text)
#         print(json_response)
#         return JsonResponse(response_data)
#
# def get_transaction(request):
#     response_json = {}
#     if request.method == 'POST':
#         transaction_id = request.POST.get('transactionId')
#         try:
#             transaction = MpesaPayment.objects.get(trans_id=transaction_id)
#             order_number = request.session.get('order_number')
#             order = get_object_or_404(Order, order_number=order_number)
#             if float(order.grand_total) > float(transaction.amount):
#                 balance = float(order.grand_total) - float(transaction.amount)
#                 transaction.order_id = order_number
#                 transaction.save()
#                 response_json['balance_error'] = 'you have a balance of {0}.complete your payment'.format(balance)
#                 print('incomplete')
#                 return JsonResponse(response_json)
#             else:
#                 print('complete')
#                 transaction.order_id = order_number
#                 transaction.is_successful = True
#                 transaction.is_finished = True
#                 transaction.save()
#                 return JsonResponse()
#         except ObjectDoesNotExist:
#             response_json['message'] = "Your transaction has not been found"
#         transaction.save()
#         return JsonResponse((response_json))
#
# def check_payment_status(checkout_request_id, shortcode=None):
#     code = LipanaMpesaPpassword.Business_short_code
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
#     checkout_request_id = "ws_CO_260320222036399021"
#     s = code + LipanaMpesaPpassword.passkey + time_now
#     encoded = base64.b64encode(s.encode('utf-8')).decode('utf-8')
#
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
#     headers = {
#         "Authorization": "Bearer %s" % access_token,
#         "Content-Type": "application/json",
#     }
#     request = {
#         "BusinessShortCode": code,
#         "Password": encoded,
#         "Timestamp": time_now,
#         "CheckoutRequestID": checkout_request_id
#     }
#     response = requests.post(api_url, json=request, headers=headers)
#     json_response = json.loads(response.text)
#     print(json_response)
#     if 'ResponseCode' in json_response and json_response["ResponseCode"] == "0":
#         requestId = json_response.get('CheckoutRequestID')
#         transaction = MpesaPayment.objects.get(
#             checkout_request_id=requestId)
#         if transaction:
#             transaction.is_finished = True
#             transaction.is_successful = True
#             transaction.save()
#
#         result_code = json_response['ResultCode']
#         response_message = json_response['ResultDesc']
#         return {
#             "result_code": result_code,
#             "status": result_code == "0",
#             "finished": transaction.is_finished,
#             "successful": transaction.is_successful,
#             "message": response_message
#         }
#     else:
#         raise Exception("Error checking transaction status", json_response)
#
# @csrf_exempt
# def register_urls(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     headers = {"Authorization":"Bearer %s" % access_token}
#     options = {"ShortCode":LipanaMpesaPpassword.Test_c2b_shortcode,
#                "ResponseType":"Completed",
#                "ConfirmationURL":"https://391f-102-68-76-241.ngrok.io/checkout/c2b/confirmation",
#                "ValidationURL":"https://391f-102-68-76-241.ngrok.io/checkout/c2b/validation"}
#     response = requests.post(api_url, json=options, headers=headers)
#     # print(headers, options)
#     return HttpResponse(response.text)
#
# @csrf_exempt
# def simulate_c2btransaction(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
#     headers = {"Authorization":"Bearer %s" % access_token}
#     options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
#                # "CustomerPayBillOnline",  # CustomerBuyGoodsOnline
#                "CommandID": "CustomerBuyGoodsOnline",
#                "Amount": "1",
#                # phone_number sendng the trxn, starting with Xtrycode minus plus (+) sign
#                "Msisdn": "254705912645",
#                "BillRefNumber": "",
#                }
#
#     try:
#         response = requests.post(api_url, headers=headers, json=options)
#
#     except:
#         response = requests.post(api_url, json=request, headers=headers, verify=False)
#
#     return HttpResponse(response.text)
#
#
# @csrf_exempt
# def call_back(request):
#     print(request)
#     return HttpResponse(request)
#
#
# @csrf_exempt
# def validation(request):
#     mpesa_body =request.body.decode('utf-8')
#     print(mpesa_body, "This is request data in validation")
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))
#
#
# @csrf_exempt
# def confirmation(request):
#     response_json = {}
#     if request.method == "POST":
#         response = request.POST.get('confirmationCode')
#         print(response)
#         try:
#             transaction = MpesaPayment.objects.get(reference=response)
#             mpesatransaction = get_object_or_404(MpesaPayment, id = transaction.id)
#             if transaction.is_confirmed == True:
#                 response_json['message'] = "This transaction was found and was already confirmed"
#             elif transaction.is_confirmed == False:
#                 response_json['message'] = "Transaction found. You are being redirected..."
#                 mpesatransaction.is_confirmed = True
#                 mpesatransaction.save()
#         except:
#             response_json['message'] = "Transaction not found. Please recheck your confirmation code and submit"
#     print(response_json)
#     return JsonResponse(response_json)
#
#     mpesa_body =request.body.decode('utf-8')
#     mpesa_payment = json.loads(mpesa_body.text)
#     print(mpesa_payment)
#     payment = MpesaPayment(
#         first_name=mpesa_payment['FirstName'],
#         last_name=mpesa_payment['LastName'],
#         middle_name=mpesa_payment['MiddleName'],
#         trans_id=mpesa_payment['TransID'],
#         phone_number=mpesa_payment['MSISDN'],
#         amount=mpesa_payment['TransAmount'],
#         reference=mpesa_payment['BillRefNumber'],
#         organization_balance=mpesa_payment['OrgAccountBalance'],
#         type=mpesa_payment['TransactionType'],
#     )
#     payment.save()
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        # del request.session['bag']
        print("there is shhit")

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
