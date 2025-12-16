"""
Context processors untuk menyediakan data global ke semua templates
"""
import os


def company_info(request):
    """
    Menambahkan informasi perusahaan dari environment variable ke context
    """
    return {
        'COMPANY_NAME': os.getenv('COMP_NAME', 'PT Aksara Delta Teknologi'),
    }
