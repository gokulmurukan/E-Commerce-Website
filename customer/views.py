from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from customer.forms import RegisterationForm,SigninForm,ReviewForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from ecommweb.models import Products,Carts,Orders,Offers
from django.utils.decorators import method_decorator

# Create your views here.

def signin_requird(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid session, Not LogedIn")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=RegisterationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegisterationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("signin")
        else:
            return render(request,"signup.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=SigninForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=SigninForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                print(usr)
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})

@method_decorator(signin_requird,name="dispatch")
class HomeView(View):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        return render(request,"home.html",{"products":qs})

@method_decorator(signin_requird,name="dispatch")
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        return render(request,"product_detail.html",{"product":qs})

@method_decorator(signin_requird,name="dispatch")
class AddToCartView(View):
    def post(self,request,*args,**kwargs):
        qty=request.POST.get("qty")
        user=request.user
        id=kwargs.get("id")
        product=Products.objects.get(id=id)

        Carts.objects.create(product=product,user=user,qty=qty)
        return redirect("home")

@method_decorator(signin_requird,name="dispatch")
class CartListView(View):
    def get(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user,status="in-cart")
        return render(request,"cart-list.html",{"carts":qs})

@method_decorator(signin_requird,name="dispatch")
class CartRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Carts.objects.filter(id=id).update(status="cancelled")
        return redirect("home")

@method_decorator(signin_requird,name="dispatch")
class MakeOrderView(View):
    def get(self,request,*arg,**kwargs):
        id=kwargs.get("id")
        qs=Carts.objects.get(id=id)
        return render(request,"checkout.html",{"cart":qs})

    def post(self,request,*arg,**kwargs):
        user=request.user
        adress=request.POST.get("adress")
        id=kwargs.get("id")
        qs=Carts.objects.get(id=id)
        product=qs.product
        Orders.objects.create(product=product,user=user,adress=adress)
        qs.status="order-placed"
        qs.save()
        return redirect("home")

@method_decorator(signin_requird,name="dispatch")
class MyOrderView(View):
    def get(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user).exclude(status="cancelled")
        return render(request,"order-list.html",{"order":qs})

@method_decorator(signin_requird,name="dispatch")
class OrderRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Orders.objects.filter(id=id).update(status="cancelled")
        return redirect("home")

@method_decorator(signin_requird,name="dispatch")
class DiscountProductView(View):
    def get(self,request,*args,**kwargs):
        qs=Offers.objects.all()
        return render(request,"offer_product.html",{"offers":qs})

@method_decorator(signin_requird,name="dispatch")
class ReviewCreateView(View):
    def get(self,request,*args,**kwargs):
        form=ReviewForm()
        return render(request,"review_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=ReviewForm(request.POST)
        id=kwargs.get("id")
        pro=Products.objects.get(id=id)

        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect("home")
        else:
            return render(request,"review_add.html",{"form":form})


