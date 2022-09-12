from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    page_detail = " | Bag"
    context = {
    'page_detail':page_detail,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    type_of_pay = request.POST.get('type_pay')
    redirect_url = request.POST.get('redirect_url')
    size = type_of_pay

    if type_of_pay == "payment_in_installments":
        quantity = 1;
    else:
        quantity = quantity

    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                if type_of_pay == "payment_in_installments":
                    bag[item_id]['items_by_size'][size] = quantity
                    messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
                else:
                    bag[item_id]['items_by_size'][size] += quantity
                    messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            if type_of_pay == "payment_in_installments":
                messages.success(request, f'Added {product.name} to your bag under lipia pole pole.')
            else:
                messages.success(request, f'Added {product.name} to your bag.')
    else:
        if item_id in list(bag.keys()):
            if type_of_pay == "payment_in_installments":
                bag[item_id] = quantity
                messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
                print(request, f'Updated {product.name} quantity to {bag[item_id]}')
            else:
                bag[item_id] += quantity
                messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
                print(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
            print(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    type_of_pay = request.POST.get('type_pay')
    if type_of_pay:
        size = type_of_pay
    else:
        size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)