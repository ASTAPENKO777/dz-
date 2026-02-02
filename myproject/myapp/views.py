from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Post, Comment

def posts_view(request):
    posts = Post.objects.all().prefetch_related('comment_set')
    return render(request, 'myapp/posts.html', {'posts': posts})

@csrf_exempt
@require_POST
def add_comment(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        text = data.get('text')
        
        if not text:
            return JsonResponse({'error': 'Comment text is required'}, status=400)
        
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(post=post, text=text)
        
        return JsonResponse({
            'id': comment.id,
            'text': comment.text,
            'comments_count': post.comment_set.count()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def delete_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        post_id = comment.post.id
        comment.delete()
        
        post = get_object_or_404(Post, id=post_id)
        return JsonResponse({
            'success': True,
            'comments_count': post.comment_set.count()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def like_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        
        return JsonResponse({
            'likes': post.likes,
            'dislikes': post.dislikes
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def dislike_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        post.dislikes += 1
        post.save()
        
        return JsonResponse({
            'likes': post.likes,
            'dislikes': post.dislikes
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
