from django.shortcuts import render,redirect
from django.views import View
from ecommapp.forms import UserRegister,UserLogin,cartForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Products,Carts,orders
from django.core.mail import send_mail,settings

# Create your views here.

class HomeView(View):
    def get(self,request,*args,**kwargs):
        data=Products.objects.all()
        return render(request,'index.html',{'products':data})
    
class UserRegView(View):
    def get(self,request,*args,**kwargs):
        form=UserRegister()
        return render(request,'user_register.html',{'form':form})
    

    def post(self,request,*args,**kwargs):
        form=UserRegister(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,'Registration successfull')
            return redirect('log_view')
        else:
            messages.error(request,'invalid')
            return redirect('home_view')
        
class UserLoginView(View):
    def get(self,request,*args,**kwargs):
        form=UserLogin()
        return render(request,'userlogin.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)      
            messages.success(request,'Login successful')
            return redirect('home_view')
        else:
            messages.error(request,'invalid credentials')
            return redirect('log_view')
        
class UserLogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'Logout successful')
        return redirect('home_view')
    
class ProductDetailsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        return render(request,'productdetail.html',{'product':product})

# class Productdetails(View):
#     def get(self,request,*args,**kwargs):
#      id=kwargs.get('id')
#      data1=Products.objects.get(id=id)
#      return render(request,'productdetails.html',{'product':data1})

class Addtocart(View):
    def get(self,request,*args,**kwargs):
        form=cartForm()
        id=kwargs.get('id')
        prd=Products.objects.get(id=id)
        return render(request,'addtocart.html',{'addcart':form,'product':prd})
    def post(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get('id')
        prd=Products.objects.get(id=id)
        qty=request.POST.get('quantity')
        Carts.objects.create(user=user,product=prd,quantity=qty)
        return redirect('home_view')
    
class Cartproduct(View):
    def get(self,request,*args,**kwargs):
         cart=Carts.objects.filter(user=request.user).exclude(status='order-placed')
         return render(request,'showcart.html',{'cart':cart})

class PlaceOrderView(View):
    def get(self,request,*args,**kwargs):
        form=OrderForm()
        return render(request,'place-order.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get('cart_id')
        cart=Carts.objects.get(id=cart_id)
        user=request.user
        address=request.POST.get('address')
        email=request.POST.get('email')
        orders.objects.create(user=user,product=cart,address=address,email=email)
        send_mail('confirmation','order placed successfully!',settings.EMAIL_HOST_USER,[email])
        cart.status='order_placed'
        cart.save()
        return redirect('home_view')

class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        data=Carts.objects.get(id=id)
        data.delete()
        return redirect('crtpr')
    



