from django.shortcuts import render,redirect
from .models import Product, Category,Customer
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login 
from django.views import View


class index(View):
    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product_id:
            quantity = cart.get(product_id, 0)
            if remove:
                if quantity > 1:
                    cart[product_id] = quantity - 1
                else:
                    cart.pop(product_id)
            else:
                cart[product_id] = quantity + 1

        request.session['cart'] = cart
        print("Cart after update:", request.session['cart'])  # Debugging line
        return redirect('homepage')

    def get(self, request):
        products = None
        categories = Category.get_all_categories()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.get_all_products_by_category_id(category_id)
        else:
            products = Product.get_all_products()

        data = {
            'products': products,
            'categories': categories
        }
        return render(request, 'index.html', data)

    

def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone_number = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        con_password = request.POST.get('confirm_password')

        value={
            'first_name':first_name,
            'last_name':last_name,
            'phone_number':phone_number,
            'email':email,
        }

        # Form validation
        error_message = None
        if not first_name:
            error_message = "First Name is required."
        elif len(first_name) < 4:
            error_message = "First Name must be at least 4 characters long."
        elif not last_name:
            error_message = "Last Name is required."
        elif len(last_name) < 4:
            error_message = "Last Name must be at least 4 characters long."
        elif not phone_number:
            error_message = "Phone Number is required."
        elif len(phone_number) != 10:
            error_message = "Phone Number must be 10 digits long."
        elif len(email) < 5:
            error_message = "Email must be at least 5 characters long."
        elif password != con_password:
            error_message = "Passwords do not match."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."
        elif Customer.objects.filter(email=email).exists():
            error_message = "Email is already registered."

        data={
            'error': error_message,
            'values':value
        }    

        if error_message:
            return render(request, 'signup.html', data)

        
        # Hash the password
        hashed_password = make_password(password)

        # Create a new user object
        user = Customer(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=hashed_password
        )
        user.save()
        # Optionally, you can log in the user after signup
        # login(request, user)

        # Redirect the user to the login page after successful signup
        return redirect('login')

    # Render the signup form
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                # Authentication successful, set session variable and redirect
                request.session['customer'] = customer.id
                request.session['email'] = email
                return redirect('homepage')
            else:
                # Authentication failed, show error message
                error_message = "Invalid email or password."
                return render(request, 'login.html', {'error': error_message})
        except Customer.DoesNotExist:
            # User does not exist, show error message
            error_message = "Invalid email or password."
            return render(request, 'login.html', {'error': error_message})

    # For GET request, render login page
    return render(request, 'login.html')




# def login(request):
#     if request.method =='GET':
#         return render(request,'login.html')
#     else:
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         customer=Customer.get_customer_by_email(email)
#         error_message=None
#         if customer:
#             flag=check_password(password,customer.password)
#             if flag:
#                 return redirect("homepage")
#             else:
#                 error_message="Email or password invalid"    
#         else:
#             error_message="'Invalid email or password."
#         return render(request,'login.html',{'error':error_message})



# #class login(View):
#     def get(self, request):
#         return render(request,'login.html')  
#     def post(self, request):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         customer=Customer.get_customer_by_email(email)
#         error_message=None
#         if customer:
#             flag=check_password(password,customer.password)
#             if flag:
#                 return redirect("homepage")
#             else:
#                 error_message="Email or password invalid"    
#         else:
#             error_message="'Invalid email or password."
#         return render(request,'login.html',{'error':error_message})


def logout(request):
    # Ensure the 'customer_id' key exists in the session before attempting to delete it
    request.session.clear()   
    # Redirect to the login page after logout
    return redirect('login')



from django.shortcuts import render
from django.views import View
from .models import Product

class cart(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        if cart:
            product_ids = list(cart.keys())
            products = Product.get_products_by_id(product_ids)
        else:
            products = []

        return render(request, "cart.html", {'products': products, 'cart': cart})




        # cart = request.session.get('cart', {})
        # if not cart:
        #     cart_items = []
        # else:
        #     cart_items = list(cart.keys())

        # print(cart_items)
        #return render(request, "cart.html", {'cart_items': cart_items})