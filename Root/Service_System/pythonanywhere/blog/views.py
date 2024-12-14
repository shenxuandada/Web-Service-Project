from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from rest_framework import viewsets
from .serializers import PostSerializer
from django.http import HttpResponse
from django.db.models import Sum  #12.14new add

from rest_framework.views import APIView    #12.14new add
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import DetectionRecord
from datetime import datetime

class ImageListView(APIView):         #12.14new add
    def get(self, request):
        images = Post.objects.filter(image__isnull=False)
        serializer = PostSerializer(images, many=True)
        return Response(serializer.data)


from django.contrib.auth import authenticate, login                #12.14xintianjia
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    else:
        return render(request, 'login.html')


def post_list(request):    #12.14new add
    from datetime import datetime
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    hourly_count = DetectionRecord.objects.filter(
        detected_hour=now
    ).aggregate(total_count=Sum('count'))['total_count'] or 0

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts, 'hourly_count': hourly_count})



@api_view(['POST'])            #12.14new add
def upload_detection_data(request):

    try:
        detected_hour = request.data.get('detected_hour')  # e.g., '2024-12-14T10:00:00'
        count = int(request.data.get('count', 0))

        if not detected_hour or count < 0:
            return Response({"error": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

        DetectionRecord.objects.create(
            detected_hour=datetime.fromisoformat(detected_hour),
            count=count
        )
        return Response({"message": "Detection data uploaded successfully"}, status=HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)




















def js_test(request):
    return HttpResponse("This is a test view for js_test.")



# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class BlogImages(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer








# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
# from django.http import HttpResponse
# from .models import Post
# from .forms import PostForm
# from rest_framework import viewsets
# from .serializers import PostSerializer


# def js_test(request):
#     """
#     测试视图，返回简单响应。
#     """
#     return HttpResponse("This is a test view for js_test.")


# def post_list(request):
#     """
#     显示发布的文章列表。
#     """
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})


# def post_detail(request, pk):
#     """
#     显示单篇文章的详细内容。
#     """
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})


# def post_new(request):
#     """
#     创建新的文章，包括处理 category_counts 字段。
#     """
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)  # 确保处理上传的文件
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()

#             # 如果表单中有 category_counts，解析后保存
#             category_counts = request.POST.get("category_counts")
#             if category_counts:
#                 post.category_counts = category_counts

#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})


# def post_edit(request, pk):
#     """
#     编辑现有的文章，包括更新 category_counts 字段。
#     """
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)  # 确保处理上传的文件
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()

#             # 如果表单中有 category_counts，解析后更新
#             category_counts = request.POST.get("category_counts")
#             if category_counts:
#                 post.category_counts = category_counts

#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})


# class BlogImages(viewsets.ModelViewSet):
#     """
#     使用 Django REST framework 处理文章的 API 视图。
#     """
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def perform_create(self, serializer):
#         """
#         在创建文章时自动处理逻辑。
#         """
#         serializer.save(
#             author=self.request.user,
#             published_date=timezone.now()
#         )

#     def perform_update(self, serializer):
#         """
#         在更新文章时自动处理逻辑。
#         """
#         serializer.save(
#             published_date=timezone.now()
#         )
