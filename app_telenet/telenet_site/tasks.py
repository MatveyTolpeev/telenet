from celery import Celery, shared_task
import pandas as pd
from .models import Service


@shared_task
def fill_service_from_excel(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        service = Service(
            name=row['name'],
            description=row['description'],
            price=row['price']
        )
        service.save()