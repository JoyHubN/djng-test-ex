from django.shortcuts import render
from tovar.models import Product

def catalog_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/catalog.html', {'products': products})


