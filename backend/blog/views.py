import json

from django.http import HttpResponse
from blog.models import Post
from rest_framework import serializers, viewsets, renderers


def blog_index(request):
    posts = list(Post.objects.filter(lang=request.LANGUAGE_CODE).values())
    for post in posts:
       post['created_on'] = post.get('created_on').strftime('%d-%m-%Y')
       post['last_modified'] = post.get('last_modified').strftime('%d-%m-%Y')
    print(posts)
    return HttpResponse(json.dumps(posts), status=200)


def blog_detail(request, pk):
    post = Post.objects.filter(external_id=pk, lang=request.LANGUAGE_CODE).values()[0]
    post['created_on'] = post.get('created_on').strftime('%d-%m-%Y')
    post['last_modified'] = post.get('last_modified').strftime('%d-%m-%Y')
    try:
        return HttpResponse(json.dumps(post), status=200)
    except:
        return HttpResponse(status=404)
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [renderers.JSONRenderer]
