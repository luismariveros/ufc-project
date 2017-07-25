# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import *


class IndividuoLista(generics.ListAPIView):
    queryset = Individuo.objects.all()
    serializer_class = IndividuoSerializer


# class IndividuoDetalle(APIView):
#
#     def get_object(self, cedula):
#         try:
#             return Individuo.objects.get(cedula=cedula)
#         except Individuo.DoesNotExist:
#             raise Http404
#
#     def get(self, request, cedula, format=None):
#         persona = self.get_object(cedula)
#         serializer = IndividuoSerializer(persona)
#         return Response(serializer.data)

class IndividuoDetalle(generics.ListAPIView):
    serializer_class = IndividuoSerializer

    def get_queryset(self):
        cedula = self.kwargs['cedula']
        return Individuo.objects.filter(cedula=cedula)


class PadronDepartamento(generics.ListAPIView):
    serializer_class = IndividuoSerializer

    def get_queryset(self):
        codigo = self.kwargs['codigo']
        return Individuo.objects.filter(departamento_id=codigo)


class DepartamentoLista(generics.ListAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
