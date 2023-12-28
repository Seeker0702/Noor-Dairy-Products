from django.shortcuts import render, redirect
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
import razorpay
from .models import OrderPlaced, Payment, Product,Customer,Cart, wishlist
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.contrib.auth import get_user_model
# Create your views here.


def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())
@login_required
def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

@login_required
def contact(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        wishlist1 = wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(wishlist.objects.filter(user=request.user))
        return render(request, "app/productdetail.html",locals())
    
@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0]).values('title')
        return render(request, "app/category.html", locals())
    
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        # return render(request, "app/login.html", locals())
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid.")
    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account"
    mail_subject = "Activate your user account"
    message = render_to_string("app/account_activate.html",{
        'user' : user.username,
        'domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
        'protocol' : 'https' if request.is_secure() else 'http'
    })
    email =  EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on the link')

    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed correctly.')


# class CustomerRegistrtionView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         totalitem=0
#         wishitem=0
#         if request.user.is_authenticated:
#             totalitem=len(Cart.objects.filter(user=request.user))
#             wishitem=len(wishlist.objects.filter(user=request.user))
#         return render(request, 'app/customerregistration.html',locals())
#     def post(self, request):
#         form = CustomerRegistrationForm(request.POST)
        
#         if form.is_valid():
#             user=form.save(commit=False)
#             user.is_active=False
#             user.save()
#             activateEmail(request, user, form.cleaned_data.get('email'))
#             # return redirect("/")
#             # messages.success(request, "Congratulations! User Register Successfully")
#         else:
#             messages.warning(request, "Invalid Input Data")
#         return render(request, 'app/customerregistration.html',locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.warning(request, f"User with email {email} already exists. Please log in.")
                return render(request, 'app/customerregistration.html', locals())

            # Use a different variable name to avoid conflicts with the class name 'User'
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            activateEmail(request, new_user, email)
            # return redirect("/")
            # messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'app/customerregistration.html', locals())
    

    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())
        
    def post(self, request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())
    
@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        amount =0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            amount = amount+value
        
        totalamount=amount+40
        razoramount = int(totalamount*100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data ={"amount":razoramount, "currency":"INR", "receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_MvyJYPZSZZdfzd', 'entity': 'order', 'amount': 37000, 'amount_paid': 0, 'amount_due': 37000, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1699008097}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment =Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())

# def payment_done(request):
#     order_id = request.GET.get('order_id')
#     payment_id = request.GET.get('payment_id')
#     cust_id = request.GET.get('cust_id')
#     user=request.user
#     customer = Customer.objects.get(id=cust_id)
#     payment = Payment.objects.get(razorpay_order_id = order_id)
#     payment.paid = True
#     payment.razorpay_payment_id =payment_id
#     payment.save()
#     cart =Cart.objects.filter(user=user)
#     for c in cart:
#         OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
#         c.delete()
#     return redirect("orders")



@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    
    return HttpResponseRedirect(reverse('orders'))

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())

    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

# def add_to_cart(request):
#     user = request.user
#     product_id = int(request.GET.get('prod_id'))
#     product = Product.objects.get(id=int(product_id))
#     Cart(user=user, product=product).save()
#     return redirect("/cart")
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    # Remove trailing slash if it exists
    if product_id.endswith('/'):
        product_id = product_id.rstrip('/')

    try:
        product = Product.objects.get(id=int(product_id))
        Cart(user=user, product=product).save()
        return redirect("/cart")
    except (ValueError, Product.DoesNotExist):
        # Handle the case where product_id is not a valid integer or product doesn't exist
        # You can display an error message, log the issue, or redirect to an error page.
        return redirect("/error-page")  # Replace with your error handling logic







from django.shortcuts import get_object_or_404, redirect

# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
    
#     try:
#         product_id = int(product_id)
#     except (TypeError, ValueError):
#         return redirect("/checkout")  
#     product = get_object_or_404(Product, id=product_id)
#     Cart(user=user, product=product).save()
#     return redirect("/cart")

@login_required
def show_cart(request):
    user= request.user
    cart = Cart.objects.filter(user=user)
    amount =0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = amount+value
    totalamount=amount+40
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount = amount+value
        totalamount=amount+40
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount = amount+value
        totalamount=amount+40
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount = amount+value
        totalamount=amount+40
        # print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required
def orders(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


def plus_wishlist(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist(user=user,product=product).save()
        data ={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    

def minus_wishlist(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist.objects.filter(user=user,product=product).delete()
        data ={
            'message':'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    
@login_required
def search(request):
    query=request.GET['search']
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html", locals())