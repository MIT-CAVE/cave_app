from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class CustomSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Force Secure Connections
        # Not used in production since secure connections are terminated at the load balancer
        # if not request.is_secure():
        #     return HttpResponsePermanentRedirect(f"https://{request.get_host()}{request.get_full_path()}")
        response = self.get_response(request)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response['Content-Security-Policy'] = f"default-src 'self' {" ".join(settings.CONTENT_SOURCE_URLS)} 'unsafe-inline'; img-src 'self' data:; frame-src 'self' {settings.STATIC_APP_URL}; form-action 'self'; frame-ancestors 'none';" 
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Embedder-Policy'] = 'credentialless'
        response['Cross-Origin-Resource-Policy'] = 'same-site'
        response['Access-Control-Allow-Origin'] = f"{settings.STATIC_APP_URL}"
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['referrer-policy'] = 'same-origin'
        return response