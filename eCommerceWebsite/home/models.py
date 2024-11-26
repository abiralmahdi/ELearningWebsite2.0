from django.db import models

# DB Table for Categories
class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/categories/')

    def __str__(self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField() # Percentage of discount
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products/')

    def __str__(self):
        return self.name
    
class Offers(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.product.name + " - " + str(self.discount)
    
class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.product.name + " - " + self.user
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name + " - " + self.message

class Transanction(models.Model):
    user = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return self.user + " - " + str(self.amount) + " - " + str(self.date)
    
