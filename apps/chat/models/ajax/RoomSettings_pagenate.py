from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from common.scripts.DjangoUtils import get_pagenate_objs_and_range_list
import json
from ...settings import DEFAULT_ROOM_NAME
from ...models import RoomSettings
from ..query_search import room_settings_query_search


@require_http_methods(['POST'])
@login_required
@csrf_protect
def room_settings_pagenate_ajax(request):
    
    # POSTリクエストパラメータの取得▽
    request_page     = int(request.POST.get('request_page', 1))
    per_page_N_items = int(request.POST.get('per_n',        25))
    request_query    = request.POST.get('q',                None)
    request_sort     = 'asc' if request.POST.get('sort',    'asc') == 'asc' else 'desc'
    # POSTリクエストパラメータの取得△

    # sort ロジック▽
    sort = 'room_id__date_create' if request_sort == 'asc' else '-room_id__date_create'
    objs = RoomSettings.objects.filter(room_id__create_user = request.user,
                                       room_id__is_active   = True,
                                       ).order_by(sort).all()
    # sort ロジック△
    # search ロジック▽
    if request_query:
        objs = room_settings_query_search(objs, request_query)
    # search ロジック△
    
    pagenate_objs, pagenate_nav_list, pagenate_nav_page_dict = get_pagenate_objs_and_range_list(objs, request_page, per_page_N_items)

    objs_data_list = []
    for obj in pagenate_objs:
        data_json              = {'url':'/', 'room_name':'load error',}
        data_json['room_id']   = obj.room_id.room_id
        data_json['url']       = reverse('chat:room', kwargs={'room_id': obj.room_id.room_id} )
        data_json['room_name'] = obj.room_name
        objs_data_list.append(data_json)
    
    response_data = {
        'status':        'success',
        'objs_data':     json.dumps(objs_data_list),
        'nav_list':      pagenate_nav_list,
        'nav_page_dict': pagenate_nav_page_dict,
    }
    return JsonResponse(response_data, safe=False)