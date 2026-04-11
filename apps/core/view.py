from django.http import HttpResponse
from .models import Table


def home(request):
    tables_count = Table.objects.count()
    return HttpResponse(f"Welcome! Tables in database: {tables_count}")