from django.shortcuts import redirect
import re

class Redirect404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path.startswith('/admin'):
            return self.get_response(request)

        if request.path.startswith('/plans'):
            return self.get_response(request)

        
        if request.path.startswith('/video/') and ('/hls/' in request.path):
            
            return self.get_response(request)

        if request.path.startswith('/signup') and ('/login' in request.path):
            
            return self.get_response(request)

        if '/dashboard' in request.path:
            
            return self.get_response(request)

        
        response = self.get_response(request)
        
        
        if response.status_code == 404:
            return redirect('/')  
        
        return response