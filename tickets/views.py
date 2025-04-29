from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse 
from .models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status , filters , mixins , generics , viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import isAuthorReadOnley

# Create your views here.

# without rest no model query FBV
def no_rest_no_model(request):
    response = [
        {
            'id':1,
            'name':'ahmed',
            'mobile':'010837744'
            
            },
        {
            'id':2,
            'name':'wael',
            'mobile':'01083774434'
            
            }
    ]
    return JsonResponse(response,safe=False)


# no rest  query from model
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guest':list(data.values('name','mobile')) 
    }
    
    return JsonResponse(response)

# with restframe work and query from models

# list GET , POST
# update == PUT , delete = DELETE 

@api_view(['GET','POST'])
def FBV_list(request):
    # request is GET
    if request.method == 'GET' :
        data = Guest.objects.all()
        serializer = GuestSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['PUT','DELETE','GET'])
def FBV_pk(request,pk):
    guest = get_object_or_404(Guest , pk=pk)
    
    if request.method == 'GET' :
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CBV_list(APIView):
    def get(self,request):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CBV_pk(APIView):
    def get_object(self,pk):
        return  get_object_or_404(Guest, pk=pk)
    
    # GET
    def get(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# getall post    
class Mixin_List(mixins.ListModelMixin , mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
class Mixin_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self,request,pk):
        return self.retrieve(request,pk)
    
    def put(self,request,pk):
        return self.update(request,pk)
    
    def delete(self,request,pk):
        return self.destroy(request,pk)
    
    
class Genric_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
class Genric_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
 
    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoveSerializer
    filter_backends = [filters.SearchFilter]
    serach_fields = ['movie']
    
    
class viewsets_reversition(viewsets.ModelViewSet):
    queryset = Reversition.objects.all()
    serializer_class = Reversition
    

@api_view(['GET'])
def find_movie(request):
    movie = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie '],
    )
    serializer = MoveSerializer(movie,many=True)
    return Response(serializer.data)


# @api_view(['POST'])
# def new_reversition(request):
#     movie = Movie.objects.get(
#         hall = request.data['hall'],
#         movie = request.data['movie '],
#     )
    
#     guest = Guest()
#     guest.name = request.data['name']
#     guest.mobile = request.data['mobile']
#     guest.save()
    
#     reversition = Reversition()
#     reversition.movie = movie
#     reversition.guest = guest
#     reversition.save()
#     return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def new_reversition(request):
    try:
        # Validate required fields
        required_fields = ['hall', 'movie', 'name', 'mobile']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Missing required field: {field}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Get or return 404 if movie doesn't exist
        movie = get_object_or_404(
            Movie,
            hall=request.data['hall'],
            movie=request.data['movie']  # Removed extra space
        )
        
        # Create guest with serializer for validation
        guest_serializer = GuestSerializer(data={
            'name': request.data['name'],
            'mobile': request.data['mobile']
        })
        if guest_serializer.is_valid():
            guest = guest_serializer.save()
        else:
            return Response(
                guest_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create reservation
        reversition = Reversition.objects.create(
            movie=movie,
            guest=guest
        )
        
        # Return the created reservation data
        serializer = RversitionSerializer(reversition)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

class post_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [isAuthorReadOnley]