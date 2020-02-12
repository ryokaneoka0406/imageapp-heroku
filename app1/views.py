from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document


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

    return render(request, 'app1/index.html', {
        'form': form,
        'obj': obj
    })
