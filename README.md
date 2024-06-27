# DjangoOpenAIStreamingChat
<img src="https://github.com/MITSUHIRO-KURIKI/DjangoOpenAIStreamingChat/blob/main/static/templates/pages/home/img/image.png">

## What is this?
[DjangoTemplate](https://github.com/MITSUHIRO-KURIKI/DjangoTemplate/ "DjangoTemplate")をベースに[OpenAI API](https://openai.com/blog/openai-api "OpenAI API")を利用したチャットアプリを学習として作成しました

### 🍭UPDATE
* [celery](https://github.com/celery/celery/tree/main/examples/django "celery")を[Django Channels](https://channels.readthedocs.io/en/latest/ "Django Channels")と統合し、一部の処理を Worker で処理を行います(Localで動作確認済。GCPは未確認ですが、おそらくデプロイできると思います)   
* [marked.js](https://github.com/markedjs/marked "marked.js"), [DOMPurify](https://github.com/cure53/DOMPurify "DOMPurify")を利用してLLMに含まれる Markdown を html化の実装  
* [prism.js](https://prismjs.com/ "prism.js")を利用してLLMに含まれるコードをシンタックスハイライトの実装  
* [mermaid.js](https://github.com/mermaidjs/mermaidjs.github.io "mermaid.js")を利用してLLMに含まれるフロー図表示の実装
* 会話のやり取りから次の質問候補提示の実装  
* ルームの設定画面からモデル選択の実装  
* 望ましくない回答に対する👎評価とフィードバックモーダルの実装  

#### ストリーミング出力
* [Django Channels](https://channels.readthedocs.io/en/latest/ "Django Channels")(Web Socket)を用いてストリーミング出力に対応しています

#### APIハイパラメータの設定
* ルーム毎にハイパラメータやアイコンを変更できます

#### その他
* 会話履歴数を指定して過去のやり取りを踏まえた会話ができます  
* 上り/下りで使用したToken数を確認できます

## イメージ
<center><img width="540px" src="https://github.com/MITSUHIRO-KURIKI/DjangoOpenAIStreamingChat/blob/main/static/templates/pages/home/img/img_fps10.gif"></center>

## 設置
<sup>[DjangoTemplate](https://github.com/MITSUHIRO-KURIKI/DjangoTemplate/ "DjangoTemplate")との差分のみ表示</sup>

#### config > settings.pyでの設定
###### RADISの使用
```
# RADIS(WebSoocket/Celery)
IS_USE_RADIS = True
```

#### .envファイル用意
###### OpenAI API KEYの設定
```
OPENAI_API_KEY='*** YOUR OPENAI_API_KEY ***'
```

###### Radisの利用
```
RADIS_HOST='*** RADIS HOST ***'  
RADIS_PORT='*** RADIS PORT ***'
```

## 実行
* terminal(0)  
```
$ pip install -r requirements-base.txt
$ ProjectSetupBat
$ python manage.py runserver
```
* terminal(1)  
```
$ RunRedisServer
```
* terminal(2)  
```
$ RunCeleryWorker
```

## 主な実行環境
<sup>詳細は requirements-base.txt をご覧ください</sup>
```
python=3.9.18
Django==4.2.1
channels==4.0.0
celery==5.4.0
```

## Other
本アプリケーションで使われる各種ライブラリのライセンスは改変したものを含めて本ライセンスには含まれません。各種ライブラリの原ライセンスに従って利用してください。

## suppl.
```
DjangoOpenAIStreamingChat/
├─accounts
│  ├─forms
│  ├─models
│  │  └─receivers
│  └─views
│      └─send_mail
├─apps
│  ├─access_security
│  │  └─models
│  │      └─receivers
│  ├─chat
│  │  ├─models
│  │  │  ├─ajax
│  │  │  ├─ModelNameChoice
│  │  │  └─query_search
│  │  └─Utils
│  ├─inquiry
│  │  ├─models
│  │  │  └─receivers
│  │  └─views
│  └─user_properties
│      ├─models
│      └─views
├─common
│  ├─lib
│  │  ├─axes
│  │  ├─social_core
│  │  └─social_django
│  ├─scripts
│  │  ├─DjangoUtils
│  │  ├─LlmUtils
│  │  ├─NLPUtils
│  │  ├─PlotlyUtils
│  │  └─PythonCodeUtils
│  └─views
├─config
│  ├─acsess_logic
│  ├─admin_protect
│  ├─extra_settings
│  └─security
├─media
│  └─apps
│      ├─chat
│      │  └─ai_icon
│      └─user_profile
│          └─user_icon
├─static
│  ├─apps
│  │  ├─chat
│  │  │  └─ai_icon
│  │  │      └─default
│  │  └─user_profile
│  │      └─user_icon
│  │          └─default
│  └─templates
│      ├─apps
│      │  └─chat
│      │      └─css
│      ├─base
│      ├─common
│      │  ├─css
│      │  ├─func
│      │  └─lib
│      ├─meta_image
│      └─pages
│          └─home
├─templates
│  ├─accounts
│  │  ├─AccountDelete
│  │  ├─AccountLock
│  │  ├─EmailChange
│  │  │  └─mail_template
│  │  ├─LogIn
│  │  ├─PasswordChange
│  │  ├─PasswordReset
│  │  │  └─mail_template
│  │  ├─SignUp
│  │  │  └─mail_template
│  │  ├─TokenDelete
│  │  └─UserIdSet
│  ├─apps
│  │  ├─chat
│  │  │  ├─include
│  │  │  └─room
│  │  │      └─include
│  │  │          └─feedback
│  │  ├─inquiry
│  │  │  └─inquiry_form
│  │  │      └─notice_admin_mail_template
│  │  └─user_properties
│  │      ├─asset
│  │      │  └─sidenav
│  │      └─Settings
│  ├─common
│  │  ├─asset
│  │  └─debug
│  └─pages
│      ├─general
│      └─home
└─templatetags
```
