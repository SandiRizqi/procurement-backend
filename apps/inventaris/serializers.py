from rest_framework import serializers
from .models import TenagaAhli, TenagaAhliDocument


class TenagaAhliDocumentSerializer(serializers.ModelSerializer):
    signed_file_url = serializers.ReadOnlyField()

    class Meta:
        model = TenagaAhliDocument
        fields = [
            'id',
            'person',
            'type',
            'judul',
            'file',
            'issued_date',
            'expired_date',
            'signed_file_url',
        ]


class TenagaAhliSerializer(serializers.ModelSerializer):
    documents = TenagaAhliDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = TenagaAhli
        fields = [
            'id',
            'nama_lengkap',
            'jabatan',
            'email',
            'skills',
            'telepon',
            'documents',
        ]
