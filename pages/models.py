from django.db import models

# Create your models here.
class Reward(models.Model):
    name = models.CharField(max_length=200, null=True)
    photo=models.ImageField(upload_to='photo/',blank=False)
    points_needed=models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
