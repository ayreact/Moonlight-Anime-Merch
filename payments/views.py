from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from products.models import Order
from django.conf import settings
from .paystack import Paystack
import requests

def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        amount = order.total  # Get the total amount from the order
        email = order.email

        payment = Payment.objects.create(
            amount=amount,
            email=email,
            user=request.user,
            order=order  # Link payment to the order
        )
        
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
            'amount_value': payment.amount,
        }
        
        return render(request, 'payments/make_payment.html', context)
    context = {
        'order':order
    }

    return render(request, 'payments/payment.html', context)

def initialize_payment(request):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": request.user.email,  # or wherever you have the email
        "amount": request.POST.get("amount"),  # in kobo (for NGN)
        "callback_url": request.build_absolute_uri(reverse('verify_payment')),
        "currency": "NGN",  # you can adjust this as needed
        "reference": "unique_ref_here"  # generate a unique reference
    }

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    if response_data["status"]:
        return redirect(response_data["data"]["authorization_url"])
    else:
        # Handle error (e.g., show an error page)
        return redirect("error_page")


def verify_payment(request, reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data["status"]:
        if response_data["data"]["status"] == "success":
            # Process successful payment
            return redirect("payment_success")
        else:
            # Payment failed
            return redirect("payment_failed")
    # else:
    #     # Handle verification failure
    #     return redirect("error_page")

def payment_success(request):
    return render(request, 'payemnts/success.html')

def payment_failed(request):
    return render(request, 'payments/payment_failed.html')