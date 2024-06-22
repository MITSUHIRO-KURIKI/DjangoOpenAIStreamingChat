from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from ...models import MessageFeedback

@require_http_methods(['POST'])
@login_required
@csrf_protect
def message_feedback_dissatisfaction_update_ajax(request):
    # POSTリクエストパラメータの取得▽
    message_id = request.POST.get('message_id', None)
    # POSTリクエストパラメータの取得△
    
    if message_id:
        # ルームの所有者のみ変更可能な点に注意
        message_feedback = MessageFeedback.objects.filter(message_id__message_id           = message_id,
                                                          message_id__room_id__create_user = request.user,
                                                          ).first()
        message_feedback.dissatisfaction = True
        message_feedback.date_create     = timezone.now()
        message_feedback.save()
        
        status = 'success'
    else:
        status = 'error'
    
    response_data = {
        'status': status,
    }
    return JsonResponse(response_data, safe=False)