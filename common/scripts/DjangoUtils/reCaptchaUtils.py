from django.conf import settings
from urllib import request, parse
import json, ssl # 'import ssl' is DEBUG MODE ONRY

def grecaptcha_request(token) -> bool:

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23) # 'import ssl' is DEBUG MODE ONRY
 
    url     = "https://www.google.com/recaptcha/api/siteverify"
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    data    = {
        'secret':   settings.RECAPTCHA_PRIVATE_KEY,
        'response': token,
    }
    data = parse.urlencode(data).encode()
    req  = request.Request(
        url,
        method  = "POST",
        headers = headers,
        data    = data,
    )
    f        = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    return response['success']