from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import cv2
from imageapp.settings import BASE_DIR


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        # 最新の画像を出す処理
        form = DocumentForm()
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id=max_id)
        # 画像のURLを取得したい_けどopenCVで画像が読み取れない。
        # パーミッションエラーかしら
        input_path = BASE_DIR + obj.photo.url
        output_path = BASE_DIR + "/media/processed/processed.jpg"
        print(input_path)
        # PATHは正しい
        process(input_path, output_path)
        obj.process = "/media/processed/processed.jpg"
        obj.save()

    return render(request, 'app1/index.html', {
        'form': form,
        'obj': obj
    })


def process(input_path, output_path):
    img = cv2.imread(input_path)
    # エラー発生
    img_processed = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2GRAY)
    cv2.imwrite(output_path, img_processed)
