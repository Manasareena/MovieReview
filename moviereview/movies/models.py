from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Movie(models.Model):
    name=models.CharField(max_length=150)
    ticket_price=models.IntegerField()
    genre=models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    review=models.CharField(max_length=300)
    rating=models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(10.0)])
    date=models.DateField(auto_now_add=True)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    class Meta:
        unique_together=('user','movie')
    
