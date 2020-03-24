from imageapp.settings import BASE_DIR
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from .forms import DocumentForm
from .models import Document
import cv2
import os
import base64
from google.cloud import storage
import tempfile
import urllib.parse

# 好きなキーに変えてね！
KEY = '7f5dae0f5b772adbe9b212fd07a6bd3a'

# Google Storage関連の処理
base_url = 'https://storage.googleapis.com/imageapp_ryopenguin/'


def index(request):
    """アップローダ。アップロードした画像のIDを暗号化して処理関数に渡す。"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            code = encodeId(Document.objects.latest('id').id)
            # 処理関数へのリダイレクト
            redirect_url = reverse('process', kwargs={'code': code})
            return redirect(redirect_url)
    else:
        form = DocumentForm()

    return render(request, 'app1/index.html', {'form': form, })


def process(request, code):
    """
    アップロードされた画像に対して処理をする関数。
    grayボタンでgray呼び出し、mosaicボタンでモザイク呼び出し
    """
    try:
        obj = Document.objects.get(id=decodeCryptedId(code))
        if request.method == 'POST':
            # URLを渡す→パス取得&アップロードが完了した後にアップロード後URLが帰ってくるのでそれをprocessedに保存
            # obj.photo.urlのみgray(),mosaic()に渡す
            input_url = obj.photo.url

            # 画像処理。Elifでモザイク追加予定
            if 'button_gray' in request.POST:
                output_pass = gray(input_url)
            elif 'button_mosaic' in request.POST:
                output_pass = mosaic(input_url)

            # DBに処理済み画像のパスを記録。
            obj.processed = output_pass
            obj.save()

            return render(request, 'app1/result.html', {'obj': obj})

        return render(request, 'app1/process.html', {'obj': obj})

    except Exception:
        raise Http404


def encodeId(id):
    """
    IDの暗号化（URLで生のID入力して画像にアクセスできないようにする）
    IDのキャスト＋KEY結合→エンコード（utf8）→エンコード(base64)→byteの文字列化
    """
    idPlusKey = (str(id) + KEY).encode('utf8')
    code = base64.urlsafe_b64encode(idPlusKey).decode("ascii")
    return code


def decodeCryptedId(code):
    """
    暗号化されたIDの複合
    URL文字列のbyteオブジェクト変換→デコード(base64)→デコード(utf8)
    """
    code = code.encode("ascii")
    tmp = base64.urlsafe_b64decode(code).decode('utf8')
    id = int(tmp.replace(KEY, "").strip())
    return id


def gray(input_url):
    """
    1.GCS画像をtempdirに保存
    2.OpenCVでtempdirの画像を加工、tempdirに保存
    3.2の保存した加工済み画像をアップロード
    """
    try:
        input_url_with_noQ = urllib.parse.urlunparse(
            urllib.parse.urlparse(input_url)._replace(query=None))
        input_filename = os.path.basename(input_url_with_noQ)
        output_filename = os.path.splitext(input_filename)[
            0] + '_processed.jpg'
        output_pass = 'processed/' + output_filename

        with tempfile.TemporaryDirectory() as tmpdir:
            # GCSの処理対象画像を一時ディレクトリにダウンロード
            client = storage.Client()
            bucket = client.get_bucket('imageapp_ryopenguin')
            blob = bucket.blob('documents/' + input_filename)
            downloadDir = os.path.join(tmpdir, input_filename)
            blob.download_to_filename(downloadDir)

            # 画像を置いた一時ディレクトリから読み取り、処理へ
            img = cv2.imread(downloadDir)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(tmpdir, output_filename),
                        img_gray, [cv2.IMWRITE_JPEG_QUALITY, 100])

            # 画像のGCSへのアップロード
            client = storage.Client()
            bucket = client.get_bucket('imageapp_ryopenguin')
            blob = bucket.blob('processed/' + output_filename)
            blob.upload_from_filename(
                filename=os.path.join(tmpdir, output_filename))

        return output_pass

    except Exception as e:
        print(e)


def mosaic(input_url):
    """
    1.GCS画像をtempdirに保存
    2.OpenCVでtempdirの画像を加工、tempdirに保存
    3.2の保存した加工済み画像をアップロード
    """
    try:
        input_url_with_noQ = urllib.parse.urlunparse(
            urllib.parse.urlparse(input_url)._replace(query=None))
        input_filename = os.path.basename(input_url_with_noQ)
        output_filename = os.path.splitext(input_filename)[
            0] + '_processed.jpg'
        output_pass = 'processed/' + output_filename

        with tempfile.TemporaryDirectory() as tmpdir:
            # GCSの処理対象画像を一時ディレクトリにダウンロード
            client = storage.Client()
            bucket = client.get_bucket('imageapp_ryopenguin')
            blob = bucket.blob('documents/' + input_filename)
            downloadDir = os.path.join(tmpdir, input_filename)
            blob.download_to_filename(downloadDir)

            # 画像を置いた一時ディレクトリから読み取り、処理へ
            img = cv2.imread(downloadDir)

            # 分類器はStaticに入れる
            face_cascade_path = BASE_DIR + \
                '/app1/static/app1/xml/haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(face_cascade_path)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.05)
            ratio = 0.05
            for x, y, w, h in faces:
                small = cv2.resize(img[y: y + h, x: x + w], None,
                                   fx=ratio, fy=ratio,
                                   interpolation=cv2.INTER_NEAREST)
                img[y: y + h, x: x +
                    w] = cv2.resize(small, (w, h),
                                    interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(os.path.join(tmpdir, output_filename), img)

            # 画像のGCSへのアップロード
            client = storage.Client()
            bucket = client.get_bucket('imageapp_ryopenguin')
            blob = bucket.blob('processed/' + output_filename)
            blob.upload_from_filename(
                filename=os.path.join(tmpdir, output_filename))

        return output_pass

    except Exception as e:
        print(e)


def about(request):
    return render(request, 'app1/about.html')


def example(request):
    return render(request, 'app1/example.html')
