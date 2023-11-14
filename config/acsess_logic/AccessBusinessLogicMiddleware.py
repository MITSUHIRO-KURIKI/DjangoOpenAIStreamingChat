from common.scripts import print_color

# どのページにでもアクセスするたびに何か実行する必要がある場合に使用
class AccessBusinessLogicMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ユーザーがログインしているかどうかを確認する
        if request.user.is_authenticated:
            print_color('info RUN: config.acsess_logic.AccessBusinessLogicMiddleware user.is_authenticated', ColorCode=4)
        else:
            print_color('info RUN: config.acsess_logic.AccessBusinessLogicMiddleware user.is_anonymous',     ColorCode=4)
            
        return self.get_response(request)