from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from django import dispatch
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import  Customer, Product, Cart, BookingsPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



#def home(request):
     #if 'q' in request.GET:
        #  q=request.GET['q']
         # product=Product.objects.filter(title__icontains=q)
   #  else:
    #      product=Product.objects.all()
   #  return render(request, 'app/home.html',product)

def search(request):
     query=request.GET['query']
     allProduct=Product.objects.filter(title__icontains=query)
     products={'allProduct':allProduct}
     return render(request,'app/search.html',products)


class ProductView(View):
     def get(self, request):
          totalitem=0
          bikerentals = Product.objects.filter(category='B')
          carrentals = Product.objects.filter(category='C')
          luxury = Product.objects.filter(category='L')
          cheapdeals = Product.objects.filter(category='CD')
          popularattractions = Product.objects.filter(category='P')
          if request.user.is_authenticated:
               totalitem=len(Cart.objects.filter(user=request.user))
          return render(request, 'app/home.html', {'bikerentals':bikerentals,'carrentals':carrentals, 'luxury':luxury, 'cheapdeals':cheapdeals,'popularattractions':popularattractions,'totalitem':totalitem} )
          
#def product_detail(request):
     #return render(request, 'app/productdetail.html')

class ProductDetailView(View):
      def get(self, request, pk):
           totalitem=0
           product=Product.objects.get(pk=pk)
           item_already_in_cart=False
           if request.user.is_authenticated:
                if request.user.is_authenticated:
                   totalitem=len(Cart.objects.filter(user=request.user))
                item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
           return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})


@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
          user=request.user
          cart=Cart.objects.filter(user=user)
          #print(cart)
          amount=0.0
          service_amount=50.0
          total_amount=0.0
          cart_product=[ p for p in Cart.objects.all() if p.user == user]
          #print(cart_product)
          if cart_product:
               for p in cart_product:
                    tempamount=(p.quantity * p.product.discounted_price)
                    amount += float(tempamount)
                    totalamount = amount + service_amount
               return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
          else:
               return render(request, 'app/emptycart.html', {'totalitem':totalitem})

def plus_cart(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        service_amount=50.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += float(tempamount)
            
            
     data={
       'quantity':c.quantity,
       'amount':amount,
       'totalamount':amount + service_amount
       }
     return JsonResponse(data)

def minus_cart(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        service_amount=50.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += float(tempamount)
            
            
     data={
       'quantity':c.quantity,
       'amount':amount,
       'totalamount':amount + service_amount
       }
     return JsonResponse(data)

def remove_cart(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        service_amount=50.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += float(tempamount)
            
            
     data={
       'amount':amount,
       'totalamount':amount + service_amount
       }
     return JsonResponse(data)

def book_now(request):
      return render(request, 'app/booknow.html')

@login_required
def address(request):
 totalitem=0
 if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def bookings(request):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
     bp = BookingsPlaced.objects.filter(user=request.user)
     return render(request, 'app/bookings.html', {'bookings_placed':bp, 'totalitem':totalitem})


def luxury(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
     if data == None:
      luxury = Product.objects.filter(category='L')
     elif data == 'below':
         luxury=Product.objects.filter(category='L').filter(discounted_price__lt=7500) 
     elif data == 'above':
         luxury=Product.objects.filter(category='L').filter(discounted_price__gt=7900)
     return render(request, 'app/luxury.html' , {'luxury':luxury, 'totalitem':totalitem})
def cheap_deals(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
     if data == None:
      cheap_deals = Product.objects.filter(category='CD')
     elif data == 'below':
      cheap_deals=Product.objects.filter(category='CD').filter(discounted_price__lt=3000) 
     elif data == 'above':
      cheap_deals=Product.objects.filter(category='CD').filter(discounted_price__gt=3500)
     return render(request, 'app/cheapdeals.html' , {'cheap_deals':cheap_deals, 'totalitem':totalitem})
 
def car_rentals(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
     if data == None:
      car_rentals = Product.objects.filter(category='C')
     elif data == 'below':
         car_rentals=Product.objects.filter(category='C').filter(discounted_price__lt=750) 
     elif data == 'above':
         car_rentals=Product.objects.filter(category='C').filter(discounted_price__gt=850)
     return render(request, 'app/carrentals.html' , {'car_rentals':car_rentals, 'totalitem':totalitem})
     

def bike_rentals(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
     if data == None:
        bike_rentals= Product.objects.filter(category='B')
     elif data == 'below':
         bike_rentals=Product.objects.filter(category='B').filter(discounted_price__lt=450) 
     elif data == 'above':
         bike_rentals=Product.objects.filter(category='B').filter(discounted_price__gt=500)
     return render(request, 'app/bikerentals.html' , {'bike_rentals':bike_rentals, 'totalitem':totalitem})

def popular_attractions(request, data=None):
     if data == None:
        popular_attractions= Product.objects.filter(category='P')
     return render(request, 'app/popular.html' , {'popular_attractions':popular_attractions})
    


class CustomerRegistrationView(View):
     def get(self, request):
      form = CustomerRegistrationForm()
      return render(request, 'app/customerregistration.html', {'form':form})
     
     def post(self, request):
          form =  CustomerRegistrationForm(request.POST)
          if form.is_valid():
               messages.success(request, 'Congratulations!! Register Done Succesfully')
               form.save()
          return render(request, 'app/customerregistration.html', {'form': form})
@login_required         
def checkout(request):
     totalitem=0
     if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
     user=request.user
     add=Customer.objects.filter(user=user)
     cart_items=Cart.objects.filter(user=user)
     amount=0.0
     service_amount=50.0
     totalamount=0.0
     cart_product=[p for p in Cart.objects.all() if p.user == request.user]
     if cart_product:
      for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += float(tempamount)
     totalamount=amount+service_amount
     
     
     return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem':totalitem})
@login_required
def payment_done(request):
     user=request.user
     custid=request.GET.get('custid')
     customer=Customer.objects.get(id=custid)
     cart=Cart.objects.filter(user=user)
     for c in cart:
        BookingsPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
        return redirect("bookings")
     return render(request, 'app/bookings.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
     def get(self, request):
          form = CustomerProfileForm()
          return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

     def post(self, request):
          totalitem=0
          if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
          form = CustomerProfileForm(request.POST)
          if form.is_valid():
               usr = request.user
               name = form.cleaned_data['name']
               locality = form.cleaned_data['locality']
               city = form.cleaned_data['city']
               state = form.cleaned_data['state']
               zipcode = form.cleaned_data['zipcode']
               reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
               reg.save()
               messages.success(request, 'Congratulations!! Profile Updated Successfully.')
          
          return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})