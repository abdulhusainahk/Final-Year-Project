from django.db import models


class SampleModel(models.Model):
    name = models.CharField(max_length=500)
    filepath = models.FileField(null=True)

    # def __str__(self):
    #   return self.name + ": " + str(self.filepath)
