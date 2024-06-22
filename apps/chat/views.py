from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView
from common.scripts.DjangoUtils import get_pagenate_objs_and_range_list
from common.scripts.DjangoUtils import generate_uuid_hex
from uuid import uuid4
from .models import Room, RoomSettings, Message
from .models.query_search import room_settings_query_search
from .forms import RoomSettingsChangeForm
from .settings import (
    MAX_HISSTORY_N, MIN_TOKENS, MAX_TOKENS,
    ALLOWD_DOMAINS_LIST, DEFAULT_ROOM_NAME,
)

class RoomListView(LoginRequiredMixin, ListView):

    model                 = RoomSettings
    template_name         = 'apps/chat/room/list.html'
    pagenate_range_Nsplit = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        # GETリクエストパラメータの取得▽
        request_page     = self.request.GET.get('page',  1)
        per_page_N_items = self.request.GET.get('per_n', 25)
        request_sort     = self.request.GET.get('sort',  'desc') # or 'asc'
        request_query    = self.request.GET.get('q',     None)
        # url_param
        url_param = {
            'page':  request_page,
            'per_n': per_page_N_items,
            'sort':  request_sort,
            'q':     request_query,
        }
        # GETリクエストパラメータの取得△

        # sort ロジック▽
        sort = 'room_id__date_create' if request_sort == 'asc' else '-room_id__date_create'
        objs = self.model.objects.filter(room_id__create_user = self.request.user,
                                         room_id__is_active   = True,
                                         ).order_by(sort).all()
        # sort ロジック△
        # search ロジック▽
        if request_query:
            objs = room_settings_query_search(objs, request_query)
        # search ロジック△

        # pagenate 情報▽
        pagenate_objs, pagenate_nav_list, pagenate_nav_page_dict = get_pagenate_objs_and_range_list(objs, request_page, per_page_N_items)
        pagenate = {
            'objs':             pagenate_objs,
            'page':             request_page,
            'per_page_N_items': per_page_N_items,
            'nav_list':         pagenate_nav_list,
            'nav_page_dict':    pagenate_nav_page_dict,
            'nav_range':        [ x for x in range(1,
                                                   pagenate_nav_page_dict['page_count']+1 if pagenate_nav_page_dict['page_count']+1 != 0 else 1,
                                                   int(pagenate_nav_page_dict['page_count']/self.pagenate_range_Nsplit) if int(pagenate_nav_page_dict['page_count']/self.pagenate_range_Nsplit) != 0 else 1 ) ],
        }
        # pagenate 情報△
        
        context.update({
            'AjaxEndPoint':    reverse('chat:room_settings_pagenate_ajax'),
            'form_action_url': reverse('chat:room_list'),
            'pagenate':        pagenate,
            'url_param':       url_param,
        })
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):

        # POSTリクエストパラメータの取得▽
        delete_room_id    = request.POST.get('DeleteRoom',    None)
        # POSTリクエストパラメータの取得△

        # ルームの作成▽
        if 'RoomCreate' in request.POST:
            # 未使用のルームの削除▽
            ## 今回新しいルームを作成するユーザがもつ DEFAULT_ROOM_NAME のRoom
            unUsedroom = Room.objects.filter(create_user = request.user,
                                             related_room_settings_model_room_id__room_name = DEFAULT_ROOM_NAME)
            unUsedroom.delete()
            # 未使用のルームの削除△
            room = Room.objects.create(room_id     = generate_uuid_hex(),
                                       create_user = request.user)
            success_url = reverse_lazy('chat:room',
                                       kwargs={'room_id': room.room_id})
            return HttpResponseRedirect(success_url)
        # ルームの作成△

        # ルームの削除▽
        ## データは保持してユーザには非表示にする
        elif delete_room_id:
            room = get_object_or_404(Room,
                                     room_id     = delete_room_id,
                                     create_user = request.user,)
            room.is_active = False
            room.save()
            success_url = reverse_lazy('chat:room_list')
            return HttpResponseRedirect(success_url)
        # ルームの削除△

        reverse_url = reverse_lazy('chat:room_list')
        return HttpResponseRedirect(reverse_url)

class RoomView(LoginRequiredMixin, UpdateView):

    model               = RoomSettings
    template_name       = 'apps/chat/room/room.html'
    fields              = ('room_name',)
    context_object_name = 'room_settings'

    def get_object(self):
        return get_object_or_404(self.model,
                                 room_id__create_user = self.request.user,
                                 room_id__room_id     = self.kwargs['room_id'],
                                 room_id__is_active   = True,)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ユーザに紐づくルーム一覧の取得
        room_objects = Room.objects.filter(create_user = self.request.user,
                                           is_active   = True,
                                           ).order_by('-date_create')

        # ルームに紐づくメッセージの取得
        message_objects = Message.objects.filter(room_id__create_user = self.request.user,
                                                 room_id__room_id     = self.kwargs['room_id'],
                                                 is_active            = True,
                                                 ).order_by('date_create')

        context.update({
            'room_settings_form':  RoomSettingsChangeForm(**self.get_form_kwargs()),
            'room_objects':        room_objects,
            'message_objects':     message_objects,
            'MAX_HISSTORY_N':      MAX_HISSTORY_N,
            'MIN_TOKENS':          MIN_TOKENS,
            'MAX_TOKENS':          MAX_TOKENS,
            'MFDU_AjaxEndPoint':   reverse('chat:message_feedback_dissatisfaction_update_ajax'),
            'MFDC_AjaxEndPoint':   reverse('chat:message_feedback_dissatisfaction_comment_ajax'),
            'ALLOWD_DOMAINS_LIST': ALLOWD_DOMAINS_LIST,
        })
        return context
    
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        
        # POSTリクエストパラメータの取得▽
        delete_room_id    = request.POST.get('DeleteRoom',    None)
        delete_message_id = request.POST.get('DeleteMessage', None)
        # POSTリクエストパラメータの取得△

        # ルームの設定変更▽
        if 'RoomSettingsUpdate' in request.POST:
            instance           = get_object_or_404(self.model,
                                                   room_id__create_user = self.request.user,
                                                   room_id__room_id     = self.kwargs['room_id'])
            room_settings_form = RoomSettingsChangeForm(**self.get_form_kwargs(), instance=instance)
            if room_settings_form.is_valid():
                return self.form_valid(room_settings_form)
            else:
                self.object = self.get_object()
                return self.form_invalid(room_settings_form)
        # ルームの設定変更△

        # ルームの作成▽
        elif 'RoomCreate' in request.POST:
            # 未使用のルームの削除▽
            # 今回新しいルームを作成するユーザがもつ DEFAULT_ROOM_NAME のRoom
            unUsedroom = Room.objects.filter(create_user = request.user,
                                             related_room_settings_model_room_id__room_name = DEFAULT_ROOM_NAME)
            unUsedroom.delete()
            # 未使用のルームの削除△
            room = Room.objects.create(room_id     = generate_uuid_hex(),
                                       create_user = request.user)
            reverse_url = reverse_lazy('chat:room',
                                       kwargs={'room_id': room.room_id})
            return HttpResponseRedirect(reverse_url)
        # ルームの作成△

        # ルームの削除▽
        ## データは保持してユーザには非表示にする
        elif delete_room_id:
            room = get_object_or_404(Room,
                                     room_id     = delete_room_id,
                                     create_user = request.user,)
            room.is_active = False
            room.save()
            if delete_room_id != self.kwargs['room_id']:
                # 現在アクセスしているルームでなければ戻る
                success_url = reverse_lazy('chat:room',
                                           kwargs={'room_id': self.kwargs['room_id']},)
            else:
                # 現在アクセスしているルームであれば一覧に遷移させる
                success_url = reverse_lazy('chat:room_list')
            return HttpResponseRedirect(success_url)
        # ルームの削除△
        
        # メッセージの削除▽
        ## データは保持してユーザには非表示にする
        elif delete_message_id:
            meaage = get_object_or_404(Message,
                                       message_id           = delete_message_id,
                                       room_id__create_user = request.user,)
            meaage.is_active = False
            meaage.save()

            success_url = reverse_lazy('chat:room',
                                       kwargs={'room_id': self.kwargs['room_id']},)
            return HttpResponseRedirect(success_url)
        # メッセージの削除△

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        success_url = reverse_lazy('chat:room',
                                   kwargs={'room_id': self.object.room_id.room_id})
        return success_url