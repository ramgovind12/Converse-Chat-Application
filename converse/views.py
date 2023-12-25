from datetime import datetime
import random
from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse, JsonResponse, StreamingHttpResponse
import json
from typing import AsyncGenerator
from . import models
import logging


# Create your views here.

def lobby(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            request.session['username'] = username
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

# def create_message(request: HttpRequest) -> HttpResponse:
#     content = request.POST.get("content")
#     username = request.session.get("username")

#     if not username:
#         return HttpResponse(status=403)
#     author, _ = models.Author.objects.get_or_create(name=username)

#     if content:
#         models.Message.objects.create(author=author, content=content)
#         return HttpResponse(status=201)
#     else:
#         return HttpResponse(status=200)

import logging

def create_message(request: HttpRequest) -> HttpResponse:
    try:
        content = request.POST.get('content')
        username = request.session.get('username')

        if not username:
            return HttpResponse(status=403)

        author, _ = models.Author.objects.get_or_create(name=username)

        if content:
            models.Message.objects.create(author=author, content=content)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'}, status=400)
    except Exception as e:
        logging.error("Error in create_message view: %s", str(e), exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)


async def stream_chat_messages(request: HttpRequest) ->  StreamingHttpResponse:
    async def event_stream():
        async for message in get_existing_messages():
            yield message
        last_id = await get_last_message_id()
        while True:
            new_messages = models.Message.objects.filter(id__gt = last_id).order_by('created_at').values('id','author__name','content')
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            
    async def get_existing_messages() -> AsyncGenerator:
        messages = models.Message.objects.all().order_by('created_at').values('id','author__name','content')
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"


    async def get_last_message_id() -> int:
        last_message = await models.Message.objects.all().alast()
        return last_message.id if last_message else 0
    
    return StreamingHttpResponse(event_stream(), content_type = 'text/event-stream')
