
from django.http import HttpResponseRedirect,  Http404
from django.shortcuts import render
from django.urls import reverse
from prostateHelper.forms import LoadImageForm
from prostateHelper.models import Image

from PIL import Image as PilImage
import PIL.ImageOps
import base64
from io import StringIO


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
    # transform and save
    pil_image = PilImage.open(original)
    inverted_image = PIL.ImageOps.invert(pil_image)
    result_path = "D:\Anca\manaBionica\master\sem3\ITSG- Bunastare sociala\DjangoMedical\DjangoMedical\medicalHelper\media\processed_images\output.jpeg"
    inverted_image.save(result_path)
    return result_path


def analysed_image(request, image_id):
    if request.method == 'GET':
        try:
            im = Image.objects.get(pk=image_id)
            result = process(im.original)
        except Image.DoesNotExist:
            raise Http404("Image does not exist")
        return render(request, 'prostateHelper/analysed_image.html',
                      {'image': im, 'result': result})
