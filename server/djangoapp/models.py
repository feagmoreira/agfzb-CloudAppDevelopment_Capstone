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
               "Year: " + str((self.Year)) + ", " + \
               "Dealer Id: " + str((self.Dealer_Id))

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer st
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id, sentiment="neutral"):
        # Dearlership
        self.dealership = dealership
        # Name
        self.name = name
        # Purchase
        self.purchase = purchase
        # Review
        self.review = review
        # Pruchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Sentiment
        self.sentiment = sentiment
        # Id
        self.id = id

    def __str__(self):
        return "Review id: " + str((self.id)) + ", " + \
               "Dearlership: " + str((self.dealership)) + ", " + \
               "Name: " + self.review + ", " + \
               "Review: " + self.review