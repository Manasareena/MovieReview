from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import movie_items

# Create your views here.

class MovieItems(APIView):
    def get(self,request,*args,**kwargs):
        if "genre" in request.query_params:
            gen=request.query_params.get("genre")
            movies=[i for i in movie_items if i["genre"]==gen]
            return Response(data=movies)
        if "limit" in request.query_params:
            lmt=request.query_params.get("limit")
            movies=movie_items[0:int(lmt)]
            return Response(data=movies)
        return Response(data=movie_items)
    def post(self,request,*args,**kwargs):
        data=request.data
        movie_items.append(data)
        return Response(data=movie_items)

class SpecificItem(APIView):
    def get(self,request,*args,**kwargs):
        movie_code=kwargs.get('mid')
        movie=[i for i in movie_items if i["code"]==movie_code].pop()
        return Response(data=movie)
    def delete(self,request,*args,**kwargs):
        movie_code=kwargs.get('mid')
        movie=[i for i in movie_items if i["code"]==movie_code].pop()
        movie_items.remove(movie)
        return Response(data=movie_items)
    def put(self,request,*args,**kwargs):
        movie_code=kwargs.get('mid')
        data=request.data
        movie=[i for i in movie_items if i["code"]==movie_code].pop()
        index=movie_items.index(movie)
        movie_items[index]=data
        return Response(data=movie_items)

