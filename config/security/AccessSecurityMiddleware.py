# Referrer
# https://qiita.com/kin292929/items/92aa0f6f5e1fbca553ee
# https://qiita.com/kenkono/items/d95aee6e79f671c67aba
import os
import environ
from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
import subprocess
import time
from apps.access_security.models import BlockIpList, AccessSecurity
from common.scripts import RequestUtil, print_color

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# 一定期間の大量アクセスを遮断
ACCESS_COUNT_SECONDS_TIME = env.get_value('ACCESS_COUNT_SECONDS_TIME',int) # アクセス計測する対象時間(秒)
N_TIMES_TO_BLOCK_ACCESS   = env.get_value('N_TIMES_TO_BLOCK_ACCESS',int)   # 対象時間中にアクセス遮断する回数
N_TIMES_TO_ADD_BLOCKLIST  = env.get_value('N_TIMES_TO_ADD_BLOCKLIST',int)  # 対象期間中にブロックリストへ追加する回数
BLOCKLIST_EFFECTIVE_DAYS  = env.get_value('BLOCKLIST_EFFECTIVE_DAYS',int)  # ブロックリストの有効期間(日)
# 登録済みブロックリストからのアクセスを遮断
REGISTERED_BLOCK_IP_LIST_READ_FREC = env.get_value('REGISTERED_BLOCK_IP_LIST_READ_FREC',int) # DBを再読み込みするまでの時間(分)

PASS_IP_LIST    = 'pass_ip_list'
BLOCK_IP_LIST   = 'block_ip_list'
CONTROL_IP_LIST = 'control_ip_list'
CONTROL_IP_LIST_DEFAULT = {
    PASS_IP_LIST: [],
    BLOCK_IP_LIST: [],
}

class AccessSecurityMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):

        request_util    = RequestUtil(request)
        ip              = request_util.get_ip()
        
        # 登録済みブロックリストに基づくアクセス遮断▽
        if is_registered_block_ip(ip):
            AccessSecurity.objects.insert_access_log(request, 'REGISTERED_IP_BLOCK')
            if settings.DEBUG:
                print_color('info: config.security.AccessSecurityMiddleware(line 46), REGISTERED_IP_BLOCK', 4)
            raise Http404('Page not found')
        # 登録済みブロックリストに基づくアクセス遮断△
        
        # 一定期間の大量アクセスに基づくアクセス遮断▽
        control_ip_list = cache.get(CONTROL_IP_LIST, CONTROL_IP_LIST_DEFAULT)
        
        # パスリスト通過
        if ip in control_ip_list[PASS_IP_LIST]: return
        # ブロックリスト拒否
        if ip in control_ip_list[BLOCK_IP_LIST]:
            # ブロックリスト対象のIPで期限を確認
            if cache.get('block_ip_' + ip) is None:
                # 期限切れならブロックリストから除外
                control_ip_list[BLOCK_IP_LIST].remove(ip)
                cache.set(CONTROL_IP_LIST, control_ip_list)
            else:
                # ログ記録
                AccessSecurity.objects.insert_access_log(request, 'IP_BLOCK')
                if settings.DEBUG:
                    print_color('info: config.security.AccessSecurityMiddleware(line 66), IP_BLOCK', 4)
                raise Http404('Page not found')

        ip_time_list = cache.get(ip, [])
        time_temp    = time.time()
        
        # 設定時間前の更新記録(キャッシュ)を削除
        while ip_time_list and (time_temp - ip_time_list[-1]) > ACCESS_COUNT_SECONDS_TIME:
            ip_time_list.pop()
        ip_time_list.insert(0, time_temp)
        cache.set(ip, ip_time_list, timeout=ACCESS_COUNT_SECONDS_TIME)
        
        # ブロックリスト登録
        if len(ip_time_list) > N_TIMES_TO_ADD_BLOCKLIST:
            control_ip_list[BLOCK_IP_LIST].append(ip)
            # 該当IPは設定期間アクセス遮断
            cache.set(CONTROL_IP_LIST, control_ip_list, timeout=60*60*24*BLOCKLIST_EFFECTIVE_DAYS)
            cache.set('block_ip_' + ip, '', timeout=60*60*24*BLOCKLIST_EFFECTIVE_DAYS)
            # ログ記録
            AccessSecurity.objects.insert_access_log(request, 'SET_BLOCK_IP')
            if settings.DEBUG:
                print_color('info: config.security.AccessSecurityMiddleware(line 87), SET_BLOCK_IP', 4)

        # アクセス拒否        
        if len(ip_time_list) > N_TIMES_TO_BLOCK_ACCESS:
            if is_google_bot(ip):
                # googlebotのIPをパスリストに登録する
                control_ip_list[PASS_IP_LIST].append(ip)
                cache.set(CONTROL_IP_LIST, control_ip_list, timeout=60*60*24*365)
                # ログ記録(googlebotのIPをパスリスト: 特に不要であればコメントアウト)
                # AccessSecurity.objects.insert_access_log(request, 'SET_PASS_IP')
            else:
                # ログ記録
                AccessSecurity.objects.insert_access_log(request, 'COUNT_BLOCK')
                if settings.DEBUG:
                    print_color('info: config.security.AccessSecurityMiddleware(line 101), COUNT_BLOCK', 4)
                raise Http404('Page not found')
        # 一定期間の大量アクセスに基づくアクセス遮断△


# 登録済みブロックリストをキャッシュに保存
def is_registered_block_ip(ip) -> bool:
    # cacheからIPを抜き出す。
    registered_block_ips = cache.get('registered_block_ip_objs')

    # cacheにない場合、DBから情報を抜き取り格納する。
    if registered_block_ips is None:
        registered_block_ips = list(BlockIpList.objects.all())
        cache.set('registered_block_ip_objs', registered_block_ips, REGISTERED_BLOCK_IP_LIST_READ_FREC*60)

    registered_black_ip_list = [registered_block_ip.ip for registered_block_ip in registered_block_ips]
    return ip in registered_black_ip_list

# googlebotか判定する
def is_google_bot(ip):
    try:
        host = subprocess.run(['host', ip], stdout=subprocess.PIPE).stdout.decode().replace('\n', '')
        return host.endswith(('googlebot.com', 'google.com'))
    except:
        return False