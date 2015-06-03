from django.conf import settings

def baseurl(request):
    """
    Return a base_url template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'
        
    return {'base_url': scheme + request.get_host() + '/' + settings.URL_INFIX,}
