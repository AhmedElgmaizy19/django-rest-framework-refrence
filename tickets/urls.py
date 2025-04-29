from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests',viewsets_guest)
router.register('movies',viewsets_movie)
router.register('reversition',viewsets_reversition)


urlpatterns = [
    #1
    path('jsonresponse/', no_rest_no_model , name='no_rest_model' ),
    #2
    path('jsonresponse_model/',  no_rest_from_model , name='no_rest_model' ),
    # 3.1
    path('rest/fbv_list/',  FBV_list),
    #3.2
    path('rest/FBV_pk/<int:pk>',  FBV_pk),
    #4.1
    path('rest/CBV_list/', CBV_list.as_view()),
    #4.2
    path('rest/CBV_pk/<int:pk>/', CBV_pk.as_view()),
    #5.1
    path('rest/mixin_list/', Mixin_List.as_view()),
    #5.2
    path('rest/mixin_pk/<int:pk>/',Mixin_pk.as_view()),
    #6.1
    path('rest/genric_list/',Genric_list.as_view()),
    #6.2
    path('rest/genric_pk/<int:pk>/',Genric_pk.as_view()),
    #7
    path('rest/viewset/',include(router.urls)),
    
    path('rest/new_reversition/',new_reversition),
    
    # auth url
    path('api-auth',include('rest_framework.urls')),
    
    # auth_token
    path('token-Auth',obtain_auth_token),
    
    #post 
    
     path('rest/post_pk/<int:pk>/',post_pk.as_view()),
]