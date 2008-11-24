from django.http import Http404
from django.conf import settings

from populous.news.views import collection

class CollectionFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a collection for non-404 responses.
        try:
            return collection(request, request.path_info)
        # Else Return the original response if any errors happened.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response