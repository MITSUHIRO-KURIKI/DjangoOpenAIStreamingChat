# DjangoOpenAIStreamingChat
<img height="450px" src="https://github.com/MITSUHIRO-KURIKI/DjangoOpenAIStreamingChat/blob/main/static/templates/pages/home/img/image.png">

## What is this?
[DjangoTemplate](https://github.com/MITSUHIRO-KURIKI/DjangoTemplate/ "DjangoTemplate")をベースに[OpenAI API](https://openai.com/blog/openai-api "OpenAI API")を利用したチャットアプリを学習として作成しました

#### ストリーミング出力
* [Django Channels](https://channels.readthedocs.io/en/latest/ "Django Channels")(Web Socket)を用いてストリーミング出力に対応しています

#### APIハイパラメータの設定
* ルーム毎にハイパラメータやアイコンを変更できます

#### その他
* 会話履歴数を指定して過去のやり取りを踏まえた会話ができます  
* 上り/下りで使用したToken数を確認できます

## イメージ
<center><img height="450px" src="https://github.com/MITSUHIRO-KURIKI/DjangoOpenAIStreamingChat/blob/main/static/templates/pages/home/img/img_fps10.gif"></center>

## 設置
<sup>[DjangoTemplate](https://mitsuhiro-kuriki.github.io/DjangoTemplate/ "DjangoTemplate")との差分のみ表示</sup>

#### config > settings.pyでの設定
###### RADISの使用<sup>⚠️</sup>
```
IS_USE_RADIS = False
```

#### .envファイル用意
###### OpenAI API KEYの設定
```
OPENAI_API_KEY='*** YOUR OPENAI_API_KEY ***'
```

###### Radisを利用する場合<sup>⚠️</sup>
```
RADIS_HOST='*** RADIS HOST ***'  
RADIS_PORT='*** RADIS PORT ***'
```
<sup>⚠️ GCPでうまく動作せず確認中/詳しい方コメント頂けると有り難いです</sup>
## 実行
```
$ pip install -r requirements-base.txt
$ ProjectSetupBat
$ python manage.py runserver
```

## 主な実行環境
<sup>詳細は requirements-base.txt をご覧ください</sup>
```
python=3.9.18
Django==4.2.1
channels==4.0.0
```

## Other
本アプリケーションで使われる各種ライブラリのライセンスは改変したものを含めて本ライセンスには含まれません。各種ライブラリの原ライセンスに従って利用してください。

## suppl.
```
DjangoTemplate/
├─accounts
│  ├─forms
│  ├─models
│  │  └─receivers
│  └─views
│      └─send_mail
├─apps
│  ├─access_security
│  ├─chat
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
│  └─views
├─config
│  ├─acsess_logic
│  ├─admin_protect
│  ├─extra_settings
│  └─security
├─media
├─static
│  ├─apps
│  └─templates
│      ├─base
│      ├─common
│      │  ├─css
│      │  ├─func
│      │  └─lib
│      ├─meta_image
│      └─pages
│          ├─apps
│          │  └─chat
│          │     └─css
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
│  │  └─SignUp
│  │      └─mail_template
│  ├─apps
│  │  ├─chat
│  │  │  └─room
│  │  │     └─include
│  │  ├─inquiry
│  │  │  └─inquiry_form
│  │  │      └─notice_admin_mail_template
│  │  └─user_properties
│  │      ├─asset
│  │      └─Settings
│  ├─common
│  │  ├─asset
│  │  └─debug
│  └─pages
│      ├─general
│      └─home
└─templatetags
```
