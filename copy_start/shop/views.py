from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from shop.models import Product, KorzinaItem, Category, Order, OrderItem
from shop.forms import DocumentForm, TovarAdd, OrderCheckoutForm

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'shop/home.html')

def test_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Файл успешно загружен!')
            return redirect('test')
    else:
        form = DocumentForm()
    return render(request, 'shop/test.html', {'form': form})

def about_view(request: HttpRequest) -> HttpResponse:
    latest_products = Product.objects.order_by('-id')[:5]
    return render(request, 'shop/about.html', {'latest_products': latest_products})

def where_find_us_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'shop/where_find_us.html')

def catalog_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.filter(count__gt=0)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    sort_by = request.GET.get('sort', '-id')
    if sort_by in ['id', '-id', 'year', '-year', 'name', '-name', 'price', '-price']:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-id')
    categories = Category.objects.all()
    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'current_sort': sort_by,
    })

def tovar_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    form = TovarAdd()
    return render(request, 'shop/tovar_detail.html', {'product': product, 'form': form})

@login_required(login_url='login')
def korzina_view(request: HttpRequest) -> HttpResponse:
    items = KorzinaItem.objects.filter(us=request.user)
    orders = Order.objects.filter(user=request.user)
    form = OrderCheckoutForm()
    return render(request, 'shop/korzina.html', {
        'items': items,
        'orders': orders,
        'form': form
    })

@login_required(login_url='login')
def add_to_cart_view(request: HttpRequest, product_id: int) -> HttpResponse:
    with transaction.atomic():
        product = Product.objects.select_for_update().get(pk=product_id)
        form = TovarAdd(request.POST)
        quantity = form.cleaned_data['quantity'] if form.is_valid() else 1
        item, created_item = KorzinaItem.objects.get_or_create(us=request.user, product=product)
        current_in_cart = item.quantity if not created_item else 0
        total_requested = current_in_cart + quantity
        diff = quantity
        if diff > product.count:
            messages.error(request, f"Ошибка: на складе недостаточно товара '{product.name}'. Доступно: {product.count} шт.")
        else:
            product.count -= diff
            product.save()
            item.quantity = total_requested
            item.save()
            messages.success(request, f"Товар '{product.name}' добавлен в корзину.")
    return redirect('tovar_detail', pk=product.id)

@login_required(login_url='login')
def increase_cart_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
    with transaction.atomic():
        item = get_object_or_404(KorzinaItem.objects.select_related('product'), pk=item_id, us=request.user)
        product = Product.objects.select_for_update().get(pk=item.product.id)
        if product.count < 1:
            messages.error(request, f"Нельзя увеличить количество: на складе больше нет товара '{product.name}'.")
        else:
            product.count -= 1
            product.save()
            item.quantity += 1
            item.save()
            messages.success(request, f"Количество товара '{product.name}' увеличено.")
    return redirect('korzina')

@login_required(login_url='login')
def decrease_cart_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
    with transaction.atomic():
        item = get_object_or_404(KorzinaItem.objects.select_related('product'), pk=item_id, us=request.user)
        product = Product.objects.select_for_update().get(pk=item.product.id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            product.count += 1
            product.save()
            messages.success(request, f"Количество товара '{product.name}' уменьшено.")
        else:
            product.count += item.quantity
            product.save()
            item.delete()
            messages.success(request, f"Товар '{product.name}' удален из корзины.")
    return redirect('korzina')

@login_required(login_url='login')
def remove_from_cart_view(request: HttpRequest, item_id: int) -> HttpResponse:
    with transaction.atomic():
        item = get_object_or_404(KorzinaItem.objects.select_related('product'), pk=item_id, us=request.user)
        product = Product.objects.select_for_update().get(pk=item.product.id)
        product.count += item.quantity
        product.save()
        item.delete()
        messages.success(request, "Товар удален из корзины.")
    return redirect('korzina')

@login_required(login_url='login')
def checkout_order_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if not request.user.check_password(password):
                messages.error(request, 'Неверный пароль. Заказ не сформирован.')
                return redirect('korzina')
            with transaction.atomic():
                items = KorzinaItem.objects.filter(us=request.user).select_related('product')
                if not items.exists():
                    messages.error(request, 'Корзина пуста.')
                    return redirect('korzina')
                order = Order.objects.create(user=request.user, status='new')
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                items.delete()
                messages.success(request, 'Заказ успешно сформирован!')
        else:
            messages.error(request, 'Ошибка валидации формы пароля.')
    return redirect('korzina')

@login_required(login_url='login')
def delete_order_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status == 'new':
        with transaction.atomic():
            for order_item in order.items.all():
                if order_item.product:
                    order_item.product.count += order_item.quantity
                    order_item.product.save()
            order.delete()
            messages.success(request, 'Новый заказ успешно удален.')
    else:
        messages.error(request, 'Можно удалять только новые заказы.')
    return redirect('korzina')
