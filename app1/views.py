from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import DocumentForm
from .models import Document
import cv2
import os
import base64
from imageapp.settings import BASE_DIR

# 好きなキーに変えてね！
KEY = '7f5dae0f5b772adbe9b212fd07a6bd3a'


def index(request):
    """
    アップローダ。アップロードした画像のIDを暗号化して処理関数に渡す。
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            photo_id = Document.objects.latest('id').id
            # URLの暗号化
            idPlusKey = (str(photo_id) + KEY).encode('utf8')
            code = base64.urlsafe_b64encode(idPlusKey).decode("ascii")
            # 処理関数へのリダイレクト
            redirect_url = reverse('process', kwargs={'code': code})
            return redirect(redirect_url)
    else:
        form = DocumentForm()

    return render(request, 'app1/index.html', {'form': form, })


def process(request, code):
    """
    アップロードされた画像に対して処理をする関数。
    grayボタンでgray呼び出し、mosaicボタンでモザイク呼び出し(モザイクはまだ実装していない)
    """
    # URL文字列のbyteオブジェクト変換→デコード(base64)→デコード(utf8)
    code = code.encode("ascii")
    tmp = base64.urlsafe_b64decode(code).decode('utf8')
    # デコードした文字列からidを取り出す
    id = int(tmp.replace(KEY, "").strip())
    obj = Document.objects.get(id=id)

    if request.method == 'POST':
        # pathの取得
        input_path = BASE_DIR + obj.photo.url
        before_filename = os.path.splitext(os.path.basename(input_path))[0]
        after_filename = before_filename + "_processed.jpg"
        output_path = BASE_DIR + "/media/processed/" + after_filename

        # 画像処理。Elifでモザイク追加予定
        if 'button_process' in request.POST:
            gray(input_path, output_path)

        # DBに処理済み画像のパスを記録。
        obj.processed = "/processed/" + after_filename
        obj.save()

        return render(request, 'app1/result.html', {'obj': obj})

    return render(request, 'app1/process.html', {'obj': obj})


def gray(input_path, output_path):
    """
    画像を白黒にする処理
    """
    # ファイル名が2バイト文字だとエラーが起きるので、エラーハンドリング
    img = cv2.imread(input_path)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, im_gray, [cv2.IMWRITE_JPEG_QUALITY, 100])
