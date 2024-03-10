# data_processing_app/models.py
from django.db import models

class ProcessedData(models.Model):
    data = models.TextField()

    def to_dict(self):
        return {'data': self.data}
