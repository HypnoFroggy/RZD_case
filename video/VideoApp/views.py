from django.shortcuts import render
from .filehandle import handle_uploaded_file
from django.http import HttpResponseRedirect

from .models import *

max = 0
def index(request):
    if request.method == "POST":
        if request.FILES:
            global max
            max = handle_uploaded_file(request.FILES.get("f"))
            return HttpResponseRedirect("/success")

    return render(request, "VideoApp/index.html", {'title': 'Загрузка видео'})

def success(request):
    return render(request, "VideoApp/success.html",context={"result":max, 'title': 'Итог работы'})

def list(request):
    render_videos = RenderVideo.objects.all().order_by('-loadDate')
    return render(request, "VideoApp/list.html", {'render_videos': render_videos})