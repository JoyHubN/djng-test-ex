from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from tovar.models import Product, KorzinaItem
from tovar.forms import TovarAdd

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tovar/home.html')

def tovar_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    form = TovarAdd()
    return render(request, 'tovar/tovar_detail.html', {'product': product, 'form': form})

@login_required(login_url='login')
def korzina_view(request: HttpRequest) -> HttpResponse:
    items = KorzinaItem.objects.filter(us=request.user)
    return render(request, 'tovar/korzina.html', {'items': items})

@login_required(login_url='login')
def add_to_cart_view(request: HttpRequest, product_id: int) -> HttpResponse:
    with transaction.atomic():
        product = Product.objects.select_for_update().get(pk=product_id)

        print(request.POST)
        form = TovarAdd(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
        else:
            quantity = 1

        item, created_item = KorzinaItem.objects.get_or_create(us=request.user, product=product)
        current_in_cart = item.quantity if not created_item else 0
        total_requested = current_in_cart + quantity
        diff = total_requested - current_in_cart  # сколько дополнительных единиц требуется

        if diff > product.count:
            messages.error(request, f"Ошибка: на складе недостаточно товара '{product.name}'. Доступно на складе: {product.count} шт.")
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
