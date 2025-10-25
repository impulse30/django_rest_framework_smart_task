from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def ping(request):
    """
    Simple health check endpoint.
    """
    return Response({"message": "pong 🏓 test"})
