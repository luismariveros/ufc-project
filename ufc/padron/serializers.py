from rest_framework import serializers
from .models import Individuo, Departamento


class IndividuoSerializer(serializers.ModelSerializer):
    departamento = serializers.StringRelatedField()
    #departamento = serializers.SlugRelatedField(read_only=True, slug_field='nombre')

    class Meta:
        model = Individuo
        fields = ('cedula', 'nombre', 'departamento')


class DepartamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departamento
        exclude = ('id', )