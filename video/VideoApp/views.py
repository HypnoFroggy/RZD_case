from django.shortcuts import render
from .forms import UploadFileForm
from .filehandle import handle_uploaded_file
from django.http import HttpResponseRedirect
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        print(type(request.FILES))
        if request.FILES:
            handle_uploaded_file(request.FILES.get("file"))
            return HttpResponseRedirect("/success")
    else:
        form = UploadFileForm()
    return render(request, "index.html")

def success(request):
    return render(request, "success.html")