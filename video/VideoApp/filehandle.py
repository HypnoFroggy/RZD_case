import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .ai import getlist
def handle_uploaded_file(files):
    path = default_storage.save('tmp/video.mp4', ContentFile(files.read()))
    list = getlist().items()
    max = 0
    for name, value in list:
        if value > max:
            max = value
    return max