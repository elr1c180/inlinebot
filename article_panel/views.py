from django.shortcuts import render, redirect
from .models import Article, Photo


def all_art(request):
    articles = Article.objects.all()

    return render(request, 'all.html', {'articles':articles})

def create(request):
    
    if request.method == 'POST':
        media = request.FILES.getlist('image')
        tags = request.POST.get('tags')
        title = request.POST.get('title')
        text = request.POST.get('content')

        article = Article.objects.create(title=title, tags=tags, text=text)
        if media:
            for media_file in media:
                photo = Photo(image=media_file)
                photo.save()
                article.media.add(photo)

        return redirect('/success/')

    return render(request, 'create.html')

def success(request):
    return render(request, 'success.html')