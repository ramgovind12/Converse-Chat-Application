from datetime import datetime
import random
from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
import json
from typing import AsyncGenerator


# Create your views here.

def lobby(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            request.session['username'] == username
        else:
            names = [
                "Penguin", "Sunflower", "Butterfly", "Rainbow", "Dragon", "Star", "Moon", "Cupcake", "Sparrow", "Whale"
            ]
            request.session['username'] = f"{random.choice(names)}-{hash(datetime.now().timestamp())}"
        return redirect('chat')
    return render(request,'lobby.html')

def chat(request: HttpRequest) -> HttpResponse:
    if not request.session.get('username'):
        return redirect('lobby')
    return render(request,'chat.html')
