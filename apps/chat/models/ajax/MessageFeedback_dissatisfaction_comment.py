from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from apps.inquiry.models import Inquiry
from ...models import MessageFeedback

@require_http_methods(['POST'])
@login_required
@csrf_protect
def message_feedback_dissatisfaction_comment_ajax(request):
    # POSTリクエストパラメータの取得▽
    feedbackType = request.POST.get('feedbackType', None)
    feedbackId   = request.POST.get('feedbackId',   None)
    feedbackText = request.POST.get('feedbackText', None)
    # POSTリクエストパラメータの取得△
    
    if feedbackType == 'message':
        if feedbackId:
            # ルームの所有者のみ変更可能な点に注意
            message_feedback = MessageFeedback.objects.filter(message_id__message_id           = feedbackId,
                                                              message_id__room_id__create_user = request.user,
                                                              ).first()
            
            message_feedback.dissatisfaction_comment = feedbackText
            message_feedback.date_create             = timezone.now()
            message_feedback.save()
            
            status = 'success'
        else:
            status = 'error'

    elif feedbackType == 'room':
        if feedbackId and feedbackText.replace(' ','').replace('　','').replace('\r\n','').replace('\n','') != '':
            feedbackText = f'room経由ご意見:{feedbackId}\n' + feedbackText
            
            forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
            if forwarded_addresses:
                client_addr = forwarded_addresses.split(',')[0]
            else:
                client_addr = request.META.get('REMOTE_ADDR')

            _ = Inquiry.objects.create(unique_account_id = request.user,
                                       email             = request.user.email,
                                       inquiry_text      = feedbackText,
                                       date_create       = timezone.now(),
                                       ip_address        = client_addr,
                                       is_notice_admin   = False,)
            status = 'success'
        else:
            status = 'error'
    else:
        status = 'error'
        
    response_data = {
        'status': status,
    }
    return JsonResponse(response_data, safe=False)