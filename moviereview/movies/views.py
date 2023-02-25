from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import MovieSerializer,UserModelSerializer,MovieModelSer,ReviewSerializer
from .models import Movie,Review
from rest_framework import status,permissions,authentication
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action


# Create your views here.
class MovieView(APIView):
    def post(self,request,*args,**kwargs):
        movie=MovieSerializer(data=request.data)
        if movie.is_valid():
            name=movie.validated_data.get("name")
            price=movie.validated_data.get("ticket_price")
            genre=movie.validated_data.get("genre")
            Movie.objects.create(name=name,ticket_price=price,genre=genre)
            return Response({"msg":"OK"})
        return Response({"msg":"failed"})
    def get(self,request,*args,**kwargs):
        if "genre" in request.query_params:
            genre=request.query_params.get("genre")
            movie=Movie.objects.filter(genre=genre)
            des_movie=MovieSerializer(movie,many=True)
            return Response(data=des_movie.data)
        movies=Movie.objects.all()
        des_movie=MovieSerializer(movies,many=True)
        return Response(data=des_movie.data)

class MovieoneItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            movie=Movie.objects.get(id=id)
            des_movie=MovieSerializer(movie)
            return Response(data=des_movie.data)
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            movie=Movie.objects.get(id=id)
            movie.delete()
            return Response({"msg":"OK"})
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def put(self,req,*args,**kwargs):
        id=kwargs.get("id")
        new_movie=MovieSerializer(data=req.data)
        if new_movie.is_valid():
            old_movie=Movie.objects.get(id=id)
            old_movie.name=new_movie.validated_data.get("name")
            old_movie.ticket_price=new_movie.validated_data.get("ticket_price")
            old_movie.genre=new_movie.validated_data.get("genre")
            old_movie.save()
            return Response({"msg":"OK"})
        return Response({"msg":"Failed"})
class MovieMView(APIView):
    def post(self,request,*args,**kwargs):
        movie=MovieModelSer(data=request.data)
        if movie.is_valid():
            movie.save()
            return Response({"msg":"OK"})
        return Response({"msg":movie.errors},status=status.HTTP_404_NOT_FOUND)
    def get(self,request,*args,**kwargs):
        movie=Movie.objects.all()
        des_movie=MovieModelSer(movie,many=True)
        return Response(data=des_movie.data)

class MovieMItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            movie=Movie.objects.get(id=id)
            des_movie=MovieModelSer(movie)
            return Response(data=des_movie.data)
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def delete(self,req,*args,**kwargs):
        id=kwargs.get("id")
        try:
            movie=Movie.objects.get(id=id)
            movie.delete()
            return Response({"msg":"OK"})
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,*args,**kwargs):
        try:
            id=kwargs.get("id")
            old_movie=Movie.objects.get(id=id)
            new_movie=MovieModelSer(data=request.data,instance=old_movie)
            if new_movie.is_valid():
                new_movie.save()
                return Response({"msg":"OK"})
            else:
                return Response({"msg":new_movie.errors},status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
class UserView(APIView):
    def post(self,req,*args,**kwargs):
        try:
            new_user=UserModelSerializer(data=req.data)
            if new_user.is_valid():
                new_user.save()
                return Response({"msg":"OK"})
            else:
                return Response({"msg":new_user.errors},status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)

class MovieViewViewset(ViewSet):
    def create(self,request,*args,**kwargs):
        movie=MovieModelSer(data=request.data)
        if movie.is_valid():
            movie.save()
            return Response({"msg":"OK"})
        return Response({"msg":movie.errors},status=status.HTTP_404_NOT_FOUND)
    def list(self,request,*args,**kwargs):
        movie=Movie.objects.all()
        des_movie=MovieModelSer(movie,many=True)
        return Response(data=des_movie.data)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            movie=Movie.objects.get(id=id)
            des_movie=MovieModelSer(movie)
            return Response(data=des_movie.data)
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def update(self,request,*args,**kwargs):
        try:
            id=kwargs.get("pk")
            old_movie=Movie.objects.get(id=id)
            new_movie=MovieModelSer(data=request.data,instance=old_movie)
            if new_movie.is_valid():
                new_movie.save()
                return Response({"msg":"OK"})
            else:
                return Response({"msg":new_movie.errors},status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def destroy(self,request,*args,**kwargs):
        try:
            id=kwargs.get("pk")
            movie=Movie.objects.get(id=id)
            movie.delete()
            return Response({"msg":"OK"})
        except:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
    def list(self,request,*args,**kwargs):
        movie=Movie.objects.all()
        if "genre" in request.query_params:
            genre=request.query_params.get("genre")
            movie=movie.filter(genre=genre)
        if "ticket_price_lt" in request.query_params:
            tp=request.query_params.get("ticket_price")
            movie=movie.filter(ticket_price__lt=tp)
        des_movie=MovieModelSer(movie,many=True)
        return Response(data=des_movie.data)

class MovieModelViewSetView(ModelViewSet):
    serializer_class=MovieModelSer
    queryset=Movie.objects.all()
    model=Movie
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    @action(detail=True,methods=["get"])
    def get_review(self,request,*args,**kwargs):
        did=kwargs.get("pk")
        movie=Movie.objects.get(id=did)
        qs=Review.objects.filter(movie=movie)
        ser=ReviewSerializer(qs,many=True)
        return Response(data=ser.data)
    @action(detail=True,methods=["post"])
    def add_review(self,request,*args,**kwargs):
        did=kwargs.get("pk")
        movie=Movie.objects.get(id=did)
        user=request.user
        ser=ReviewSerializer(data=request.data,context={"user":user,"movie":movie})
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        else:
            return Response({"msg":"Failed"},status=status.HTTP_404_NOT_FOUND)
