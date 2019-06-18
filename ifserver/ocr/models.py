import time
import os

from django.db import models


def path_and_rename(instance, filename):
    timestamp = time.time()
    upload_to = 'images'
    ext = filename.split('.')[-1]
    file = '.'.join(filename.split('.')[:-1]).replace(' ', '_')
    filename = '{}.{}'.format(file + "_" + str(timestamp), ext)

    return os.path.join(upload_to, filename)


class ImageResult(models.Model):
    Image = models.ImageField(blank=True, upload_to=path_and_rename)
    OCRData = models.TextField()
