from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from menus.models import Menu
from orders.forms import OrderItemsForm, OrderForm
from orders.models import Order, OrderItem
from products.models import Product, Variation
from restaurants.models import Restaurant


def order_add_item(request, pk, restaurant_pk, menu_pk, **kwargs):
    product = Product.objects.get(pk=pk)
    menu = Menu.objects.get(pk=menu_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    if request.user.is_authenticated:
        pass
        # TODO: Lógica para usuários autenticados

    try:
        order_slug = request.session["order_slug"]
    except KeyError:
        order = Order(restaurant=restaurant)

        order.save()
        request.session["order_slug"] = order_slug = order.slug

    order = Order.objects.get(slug=order_slug)
    if order.orderitem_set.all().filter(item=product).exists():

        item = OrderItem.objects.get(order=order, item=product)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,
                      f'{product.name} Já está no pedido. '
                      f'<a href="/orders/cart/{order_slug}/" '
                      f'class="alert-link">Ver pedido</a>.')

        return redirect(reverse('menu_display', kwargs={'pk': menu.pk,
                                                        'slug': menu.slug}))

    else:
        item = OrderItem(order=order, item=product, unity_price=product.price)
        item.save()

    messages.success(request, f'{item.item.name} adicionado ao pedido. '
                              f'<a href="/orders/cart/{order_slug}/" '
                              f'class="alert-link">Ver pedido</a>.')

    return redirect(reverse('menu_display', kwargs={'pk': menu.pk,
                                                    'slug': menu.slug}))


def order_add_var_item(request, pk, var_pk, restaurant_pk, menu_pk, **kwargs):
    product = Product.objects.get(pk=pk)
    variation = Variation.objects.get(pk=var_pk)
    menu = Menu.objects.get(pk=menu_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    if request.user.is_authenticated:
        pass
        # TODO: Lógica para usuários autenticados

    try:
        order_slug = request.session["order_slug"]
    except KeyError:
        order = Order(restaurant=restaurant)

        order.save()
        request.session["order_slug"] = order_slug = order.slug

    order = Order.objects.get(slug=order_slug)
    if order.orderitem_set.all().filter(item=product,
                                        variation=variation).exists():

        item = OrderItem.objects.get(order=order, item=product)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,
                      f'{product.name} Já está no pedido. '
                      f'<a href="/orders/cart/{order_slug}/" '
                      f'class="alert-link">Ver pedido</a>.')

        return redirect(reverse('menu_display', kwargs={'pk': menu.pk,
                                                        'slug': menu.slug}))

    else:
        item = OrderItem(order=order, item=product,
                         unity_price=product.productvariation_set.get(
                             variation=variation).price, variation=variation)
        item.save()

    messages.success(request, f'{item.item.name} adicionado ao pedido. '
                              f'<a href="/orders/cart/{order_slug}/" '
                              f'class="alert-link">Ver pedido</a>.')
    return redirect(reverse('menu_display', kwargs={'pk': menu.pk,
                                                    'slug': menu.slug}))


def cart(request, slug):
    order = Order.objects.get(slug=slug)
    order_items = OrderItem.objects.filter(order=order)
    order_total = 0
    for item in order_items:
        subtotal = item.quantity * item.unity_price
        order_total = order_total + subtotal

    order_items_formset = inlineformset_factory(
        Order, OrderItem, form=OrderItemsForm, extra=0, can_delete=True)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order, prefix='main')
        formset = order_items_formset(request.POST, instance=order,
                                      prefix='product')

        try:
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, "Pedido atualizado")
                return redirect(reverse('cart', kwargs={'slug': slug}))
        except Exception as e:
            messages.warning(request,
                             'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = OrderForm(instance=order, prefix='main')
        formset = order_items_formset(instance=order, prefix='product')

    return render(request, 'orders/cart.html', {'order': order,
                                                'order_items': order_items,
                                                'order_total': order_total,
                                                'form': form,
                                                'formset': formset, })


def checkout(request, slug):
    order = Order.objects.get(slug=slug)
    order_items = OrderItem.objects.filter(order=order)
    order_total = 0
    order_items_total = 0
    for item in order_items:
        subtotal = item.quantity * item.unity_price
        order_total = order_total + subtotal
        order_items_total = order_items_total + item.quantity

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
        'order_items_total': order_items_total,
    }
    return render(request, 'orders/simple_checkout.html', context=context)


@login_required
def orders_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.all().filter(restaurant__manager=request.user)

    return render(request, 'orders/list.html', {'orders': orders})


def order_detail(request, slug):
    order = Order.objects.get(slug=slug)
    order_items = OrderItem.objects.filter(order=order)
    order_total = 0
    order_items_total = 0
    for item in order_items:
        subtotal = item.quantity * item.unity_price
        order_total = order_total + subtotal
        order_items_total = order_items_total + item.quantity

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
        'order_items_total': order_items_total,
    }
    return render(request, 'orders/detail.html', context=context)
