from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import cv2
import os
from imageapp.settings import BASE_DIR


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('process')
    else:
        # form描画
        form = DocumentForm()

    return render(request, 'app1/index.html', {'form': form, })


def process(request):
    max_id = Document.objects.latest('id').id
    obj = Document.objects.get(id=max_id)

    if request.method == 'POST':
        if 'button_process' in request.POST:
            # pathの取得
            input_path = BASE_DIR + obj.photo.url
            before_filename = os.path.splitext(os.path.basename(input_path))[0]
            after_filename = before_filename + "_processed.jpg"
            output_path = BASE_DIR + "/media/processed/" + after_filename

            # 処理＆Record
            gray(input_path, output_path)
            obj.processed = "/processed/" + after_filename
            obj.save()

            return render(request, 'app1/result.html', {'obj': obj})

    return render(request, 'app1/process.html', {'obj': obj})


def gray(input_path, output_path):
    img = cv2.imread(input_path)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, im_gray, [cv2.IMWRITE_JPEG_QUALITY, 100])
