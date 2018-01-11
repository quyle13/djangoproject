from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

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
	except Category.DoesNotExist:
		pass

	return render(request,"rango/category.html",returned_value)
