# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import *


class PersonaLista(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaDetalle(APIView):

    def get_object(self, cedula):
        try:
            return Persona.objects.get(cedula=cedula)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, cedula, format=None):
        persona = self.get_object(cedula)
        serializer = PersonaSerializer(persona)
        return Response(serializer.data)
