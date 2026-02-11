from rest_framework import serializers
from .models import Person, PersonDocument


class PersonDocumentSerializer(serializers.ModelSerializer):
    signed_file_url = serializers.ReadOnlyField()

    class Meta:
        model = PersonDocument
        fields = [
            'id',
            'person',
            'document_type',
            'title',
            'file',
            'issued_date',
            'expired_date',
            'signed_file_url',
        ]


class PersonSerializer(serializers.ModelSerializer):
    documents = PersonDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = [
            'id',
            'vendor',
            'full_name',
            'role',
            'email',
            'skills',
            'phone',
            'documents',
        ]
