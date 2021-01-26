from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from prostateHelper.forms import LoadImageForm
from prostateHelper.models import Image

from PIL import Image as PilImage
import base64
import numpy as np
from io import BytesIO

from .ai_helper import AIManager

ai_manager = AIManager()


def index(request):
    if request.method == 'POST':
        form = LoadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_id = form.save().id
            return HttpResponseRedirect(reverse('prostateHelper:analysed_image', args=(image_id,)))
    else:
        form = LoadImageForm()
    return render(request, 'prostateHelper/index.html', {'form': form})


def process(original):
    return ai_manager.predict_image(original)


def analysed_image(request, image_id):
    if request.method == 'GET':
        try:
            im = Image.objects.get(pk=image_id)
            output_array = process(im.original)
            result_uri = convert_array_to_uri(output_array)
        except Image.DoesNotExist:
            raise Http404("Image does not exist")
        return render(request, 'prostateHelper/analysed_image.html',
                      {'image': im, 'result_uri': result_uri})


def convert_array_to_uri(arr):
    arr = arr * 255
    arr = arr.astype(np.uint8)
    img = PilImage.fromarray(arr)
    data = BytesIO()
    img.save(data, "JPEG")  # pick your format
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')