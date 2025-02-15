from venv import logger
from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from app.models import LastProduct, MainProduct, Product, SubProduct, MainSubProduct, SubLastProduct,Order
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login
from app.models import UserCreateForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
    
    context = {
        'form':form,
    }

    return render(request,'registration/signup.html',context)

def Master(request):
    return render(request, 'master.html')

def About(request):
    return render(request, 'about.html')

def Index(request):

    related_mainsubproduct = MainSubProduct.objects.all()
    mainsubproduct = MainSubProduct.objects.all()

    related_subproducts = SubProduct.objects.all()
    subproducts = SubProduct.objects.all()
    
    related_sublastproduct = LastProduct.objects.all()
    sublastproduct = SubLastProduct.objects.all()

    

    productID = request.GET.get('product')

    if productID:
        # Fetch the main product
        selected_product = get_object_or_404(Product, id=productID)
        # Fetch sub-products related to the selected product
        related_subproducts = SubProduct.objects.filter(product=selected_product)
    else:
        selected_product = None
        related_subproducts = SubProduct.objects.none()
    
    mainproductID = request.GET.get('mainproduct')

    if mainproductID:
        # Fetch the main product
        selected_mainproduct = get_object_or_404(MainProduct, id=mainproductID)
        # Fetch sub-products related to the selected product
        related_mainsubproduct = MainSubProduct.objects.filter(MainProduct=selected_mainproduct)
    else:
        selected_mainproduct = None
        related_mainsubproduct = MainSubProduct.objects.none()

    lastproductID = request.GET.get('lastproduct')

    if lastproductID:
        selected_lastproduct = get_object_or_404(LastProduct, id=lastproductID)
        # Fetch sub-products related to the selected product
        related_sublastproduct = SubLastProduct.objects.filter(lastProduct=selected_lastproduct)
    else:
        selected_lastproduct = None
        related_sublastproduct = SubLastProduct.objects.none()

    context = {
        'product': Product.objects.all(),
        'mainproduct' :MainProduct.objects.all(),
        'lastproduct' :LastProduct.objects.all(),
        'subproduct': related_subproducts,  # Pass related sub-products
        'selected_lastproduct': selected_lastproduct,
        'sublastproduct': related_sublastproduct,
        'selected_product': selected_product,  # Optional: Pass the selected product
        'all_subproducts': subproducts,
        'mainsubproduct': related_mainsubproduct,
        'all_subproducts2': mainsubproduct,
        'all_subproduct3': sublastproduct,


    }
    return render(request, 'index.html', context)

def subproduct_view(request, id):
    # Fetch the product using the given ID
    selected_product = get_object_or_404(Product, id=id)
    
    # Fetch all subproducts related to this product
    related_subproducts = SubProduct.objects.filter(product=selected_product)

    context = {
        'selected_product': selected_product,
        'subproducts': related_subproducts,
    }
    return render(request, 'subproduct.html', context)


def mainsubproduct_view(request, id):
    # Fetch all MainProduct objects for the index section
    mainproducts = MainProduct.objects.all()
    
    # Fetch the selected MainProduct and related MainSubProduct
    selected_mainproduct = get_object_or_404(MainProduct, id=id)
    related_mainsubproduct = MainSubProduct.objects.filter(mainproduct=selected_mainproduct)

    context = {
        'mainproduct': mainproducts,
        'selected_mainproduct': selected_mainproduct,
        'mainsubproduct': related_mainsubproduct,
    }
    return render(request, 'subproduct2.html', context)

def lastsubproduct_view(request, id):
    # Fetch the LastProduct using the given ID
    selected_lastproduct = get_object_or_404(LastProduct, id=id)
    # Fetch all SubLastProduct objects related to this LastProduct
    related_sublastproduct = SubLastProduct.objects.filter(lastProduct=selected_lastproduct)

    context = {
        'selected_lastproduct': selected_lastproduct,
        'sublastproduct': related_sublastproduct,
    }
    return render(request, 'subproduct3.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id, type):
    """
    Add an item to the cart based on the product type.
    """
    cart = Cart(request)

    # Fetch the product based on the type
    product_types = {
        'Product': Product,
        'MainProduct': MainProduct,
        'SubProduct': SubProduct,
        'MainSubProduct': MainSubProduct,
        'SubLastProduct': SubLastProduct,
    }
    product_model = product_types.get(type)

    if not product_model:
        # Redirect or handle invalid type
        return redirect('index')

    # Fetch the product or return 404 if not found
    product = get_object_or_404(product_model, id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    """
    Remove an item completely from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)  # Assuming only `Product` for clearing
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        logger.error(f"Product with id {id} does not exist.")
        return redirect("cart_detail")  # Or handle the error appropriately
    
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    """
    Decrement the quantity of an item in the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)  # Assuming `Product` for decrement
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    """
    Clear all items from the cart.
    """
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    """
    Display the details of the cart.
    """
    return render(request, 'cart/cart_detail.html')

def CheckOut(request):
    if request.method =='POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pncode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)

       



        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total =  a*b
            order = Order(
                User = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                total = total,
                image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                
            )
            order.save()

        request.session['cart'] = {}
        return redirect("index")
    return HttpResponse('This is checkout page')

def Your_Order(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Replace with the actual login page URL

    # Get the current authenticated user
    user = request.user
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    # Fetch orders for the authenticated user
    order = Order.objects.filter(User=user)

    context = {
        'order' : order,
    }

    print(order,user)  # For debugging purposes

    # Pass orders to the template
    return render(request, 'order.html', {'order': order})