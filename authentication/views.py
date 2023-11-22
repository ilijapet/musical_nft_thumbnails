from django.conf import settings  
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, OrderForm
from .models import Customer
from web3_interface import contract_interface

import stripe 

class HomeView(TemplateView):
    def post(self, request):
        if "username" in request.POST:
            # check to see if loggin in
            user_name = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect("home")
            else:
                messages.success(
                    request, "There was An Error login in, please try again"
                )
                return redirect("home")
        else:
            user = Customer.objects.get(username=request.user)
            orderForm = OrderForm(instance=user, data=request.POST)
            if orderForm.is_valid():
                orderForm.save()
                messages.success(request, "You successfully update payment method")
                return redirect("home")
            messages.success(
                request, "There was an error in updating of your payment method"
            )
            return redirect("home")

    def get(self, request):
        if str(request.user) == "AnonymousUser":
            return render(request, "home.html", {})
        name = str(request.user)
        customer = Customer.objects.get(username=name)
        nft_metadata = customer.nft_metadata.all()
        orderForm = OrderForm()
        return render(
            request,
            "home.html",
            {"customer": customer, "orderForm": orderForm, "metadata": nft_metadata},
        )
    
class LogoutUser(TemplateView):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out!")
        return redirect("home")

class RegisterUser(TemplateView):
    def post(self, request):
        # Everything what user send pass to our SignUpForm
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate use and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            Customer.objects.create(
                username=user,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            messages.success(request, "You have been sucesfuly logged in ")
            return redirect("home")
        return render(request, "register.html", {"form": form})

    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

# Stripe integration
class StripeConfigView(TemplateView): # new
    
        @csrf_exempt
        def get(self, request):
            stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
            return JsonResponse(stripe_config, safe=False)

class CreateCheckoutSession(TemplateView): # new   

    @csrf_exempt
    def get(self, request):
        number_of_nfts = request.GET.get("number")
        domain_url = 'https://musicnft-405811.ew.r.appspot.com/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 2000,
                            'product_data': {
                                'name': 'MusicalNFT',
                            },
                            },
                            'quantity': number_of_nfts,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelledView(TemplateView):
    template_name = 'cancelled.html'

# payments/views.py
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Mint new NFT
        result = contract_interface.mint_nft("ipfs://uri.test")
        suc, result = contract_interface.event()
        if suc:
            try:        
                c1 = Customer.objects.get(eth_address=result.args.owner)
                if result.args.numberOfNFT not in c1.nft_ids:
                    # update custodial wallet information db
                    c1.nft_ids.append(result.args.numberOfNFT)
                    c1.total_no_of_nfts += 1
                    c1.save()
                    # update customer db
                    user = event["data"]["object"]["customer_details"]["name"]
                    name, last = user.split()
                    c2 = Customer.objects.get(first_name=name, last_name=last)
                    c2.nft_ids.append(result.args.numberOfNFT)
                    c2.total_no_of_nfts += 1         
                    c2.save()            
            except Exception as e:
                print (e)
    return HttpResponse(status=200)
    

