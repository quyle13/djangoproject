from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello world. Click here to go to <a href='/rango/about'>About</a>")

def about(request):
	return HttpResponse ("Rango says here is the about page. Click here <a href='/rango/'> to go to home page </a>")
