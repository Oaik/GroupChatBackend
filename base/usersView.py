from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

import requests

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def getUsers(request):
    url = 'http://localhost:5000/users'
    r = requests.get(url)
    data = r.json()
    # print(data[0]["username"])
    return Response(data, status=status.HTTP_200_OK)
