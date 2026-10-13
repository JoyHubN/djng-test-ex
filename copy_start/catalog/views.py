from django.shortcuts import render
from tovar.models import Product, Category

def catalog_view(request):
    # Пользователю всегда показываются только те товары, которые есть в наличии (count > 0)
    products = Product.objects.filter(count__gt=0)

    # Фильтрация по категориям
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Упорядочение: по новизне (по умолчанию), по году, по наименованию, по цене
    sort_by = request.GET.get('sort', '-id')
    if sort_by in ['id', '-id', 'year', '-year', 'name', '-name', 'price', '-price']:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-id')

    categories = Category.objects.all()
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'current_sort': sort_by,
    })
