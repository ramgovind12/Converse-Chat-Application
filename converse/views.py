from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse


# Create your views here.

def chat(request: HttpRequest) -> HttpResponse:
    
