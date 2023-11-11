import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
def handle_uploaded_file(files):
    path = default_storage.save('tmp/video.mp3', ContentFile(files.read()))