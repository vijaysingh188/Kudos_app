"""
URL configuration for kudos_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
print("URLs configuration loaded")
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from kudos.views import UserViewSet, KudoViewSet
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
import json

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'kudos', KudoViewSet)

def debug_view(request):
    return JsonResponse({"message": "Debug endpoint reached"})

@csrf_exempt
def custom_obtain_auth_token(request, *args, **kwargs):
    print("Request Method:", request.method)
    print("Request Headers:", request.headers)
    print("Request Body:", request.body.decode('utf-8'))

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Parsed JSON Data:", data)
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))

    response = obtain_auth_token(request, *args, **kwargs)
    response.render()  # Ensure the response is rendered before accessing its content
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content.decode('utf-8'))
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/api-token-auth/', custom_obtain_auth_token),  # Updated to include /api/ prefix
]

urlpatterns += [
    path('debug/', debug_view),  # Add a debug endpoint to test the server
]