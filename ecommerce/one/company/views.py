from django.http import JsonResponse
from django.shortcuts import redirect,render
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from company.form import CustomUserForm
import json
from django.http import HttpResponseRedirect

def home(request):
    return render(request,'shop/index.html')

def add_to_buy(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            print(request.user.id)
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Buy.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'product added'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Buy.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'already added'},status=200)
                    else:
                        return JsonResponse({'status':'not avaliable'},status=200)
        else:
            return JsonResponse({'status':'login to add'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)


def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request,"invalid user name or password")
                return redirect('/login')
        return render(request,"shop/login.html")

 
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration success you can login now..!")
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})


def collection(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'shop/collection.html',{"catagory":catagory})
def collectionview(request,name):
    if (Catagory.objects.filter(name=name,status=0)):
        products=Products.objects.filter(category__name=name)
        return render(request,'shop/products/index.html',{"products":products,"category_name":name})
    else:
        messages.warning(request,"no such catagory found")
        return redirect('collection')

def product_details(request,cname,pname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if(Products.objects.filter(name=pname,status=0)):
             products=Products.objects.filter(name=pname,status=0).first()
             return render(request,'shop/products/product_detail.html',{"products":products})
        else:
            messages.error(request,"no such catagory found")
            return redirect('collection')
    else:
        messages.error(request,"no such catagory found")
        return redirect('collection')



