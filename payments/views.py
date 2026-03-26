import stripe
from django.shortcuts import render
from video_platform.settings import STRIPE_SECRET_KEY
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from videos.models import Video
from .models import Purchase

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, video_id):
    video = get_object_or_404(Video, id= video_id)

    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'cad',
            'product_data': {
                'name': video.title,
            },
            'unit_amount': int(video.price * 100), # cents 
        },
        'quantity': 1, # number of videos
    }],
    mode = 'payment',
    success_url = 'http://127.0.0.1:8000/payment-success/?session_id={CHECKOUT_SESSION_ID}',
    cancel_url = 'http://127.0.0.1:8000/payment-cancel',
    )

    # Save purchase (pending)
    Purchase.objects.create(
        user= request.user,
        video = video,
        stripe_session_id = session.id
    )
    return redirect(session.url)

def payment_success(request):
    session_id = request.GET.get('session_id')

    purchase = Purchase.objects.filter( stripe_session_id = session_id).first()

    if purchase:
        purchase.is_paid = True
        purchase.save()
    return redirect('/')

def payment_cancel(request):
    return redirect('/')