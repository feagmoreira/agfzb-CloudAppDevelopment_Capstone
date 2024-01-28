from django.db import models
from django.utils.timezone import now

# Car Make model
class CarMake(models.Model):
    Name = models.CharField(null=False, max_length=30)
    Description = models.CharField(null=False, max_length=200)
    
    # Object string representation
    def __str__(self):
        return "Name: " + self.Name + ", Description: " + self.Description

class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon")
    ]

    Make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Dealer_Id = models.IntegerField(null=False)
    Name = models.CharField(null=False, max_length=30)
    Type = models.CharField(null=False, max_length=50, choices=TYPE_CHOICES)
    Year = models.DateField(null=False)
    
    # Object string representation
    def __str__(self):
        return "Model: " + self.Name + ", " + \
               "Type: " + self.Type + ", " + \
               "Year: " + str(self.Year) + ", " + \
               "Dealer Id: " + str(self.Dealer_Id)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
