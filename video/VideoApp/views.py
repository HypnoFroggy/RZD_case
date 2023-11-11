from django.shortcuts import render
from .filehandle import handle_uploaded_file
from django.http import HttpResponseRedirect
max = 0
def index(request):
    if request.method == "POST":
        if request.FILES:
            global max
            max = handle_uploaded_file(request.FILES.get("f"))
            return HttpResponseRedirect("/success")
    return render(request, "index.html")
def success(request):
    return render(request, "success.html",context={"result":max})