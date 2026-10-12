from django.shortcuts import render
from tovar.models import Product

def about_view(request):
    latest_products = Product.objects.order_by('-id')[:5]
    return render(request, 'about/about.html', {'latest_products': latest_products})


