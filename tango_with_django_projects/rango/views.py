from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
	#-likes: sort by descending order
	#:5 slice and dice array
	context_dict = {}
	category_list = Category.objects.order_by("-likes")[:5]
	context_dict ['categories'] = category_list

	top_viewed_page = Page.objects.order_by("views")[:5]
	context_dict ['pages'] = top_viewed_page
	#render function: take user input request
	#template of file name
	
	return render(request,'rango/index.html',context_dict)

def about(request):
	return render(request,'rango/about.html')


def category(request,category_name_slug):
	returned_value = {}
	
	try:
          	category = Category.objects.get(slug=category_name_slug)
          	returned_value["category_name"] = category.name

          	pages = Page.objects.filter(category=category)
          	returned_value["pages"] = pages
          	returned_value["category"] = category
          	returned_value["category_name_slug"] = category_name_slug
	except Category.DoesNotExist:
		pass

	return render(request,"rango/category.html",returned_value)
@login_required
def add_category(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			cat = form.save(commit = True)
			print cat
			print cat.slug
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request,"rango/add_category.html",{"form":form})

@login_required
def add_page(request,category_name_slug):
	try:
		cat = Category.objects.get(slug = category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method =="POST":
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				new_page = form.save(commit =False)
				new_page.category = cat
				new_page.views = 0
				new_page.save()
				print new_page
				print new_page.title
				return category(request,category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
	context_dict = {"form":form,"category":cat}
	return render(request,"rango/add_page.html",context_dict)

def register(request):
	registered = False
	if request.method == "POST":
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user  = user_form.save()
			user.set_password(user.password)
			user.save()

			#set False to set user attribute
			profile = profile_form.save(commit = False)
			profile.user = user

			if "picture" in request.FILES:
				profile.picture = request.FILES["picture"]
			profile.save()

			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,"rango/register.html",{"user_form":user_form,"profile_form": profile_form,"registered":registered})

def user_login(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(username=username,password= password)
		if user:
			if user.is_active:
				#inform to Django this user logined.
				login(request,user)
				return HttpResponseRedirect("/rango/")
			else:
				return HttpResponse("Your account is disabled")
		else:
			print ("Invalid login details {0},{1}", username,password)
			return HttpResponse("Invalid username or password")
	else:
		return render(request,"rango/login.html")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/rango/")


