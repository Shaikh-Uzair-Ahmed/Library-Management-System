from django.http import HttpResponsePermanentRedirect

class CaseInsensitiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Convert the path to title case
        path = request.path_info
        request.path_info = path.title()  # Converts the path to title case
        
        # Proceed with the view handling
        response = self.get_response(request)
        
        #redirect to the title-cased URL permanently
        #(So that whatever you do it will show titled urls)
        if response.status_code == 404 and request.path != request.path_info:
            return HttpResponsePermanentRedirect(request.path_info)
        
        return response