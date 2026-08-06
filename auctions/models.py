from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64 , unique= True)
    def __str__(self):
        return self.name

class Listing(models.Model):
    product_name =  models.CharField(max_length=64)
    product_image =  models.URLField(blank= True , null= True)
    owner = models.ForeignKey(User , on_delete= models.CASCADE)
    starting_bid = models.DecimalField(max_digits= 8 , decimal_places= 2)
    product_description = models.TextField()
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    is_active = models.BooleanField(default= True)
    watchlist = models.ManyToManyField(User, blank=True , related_name="watchlist")
    def __str__(self):
        return self.product_name

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits= 8 , decimal_places= 2)
    bid_product = models.ForeignKey(Listing , on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.bidder} - {self.bid_amount} for {self.bid_product}"

class Comment(models.Model):
    message = models.TextField()    
    listing = models.ForeignKey(Listing , on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE )
    def __str__(self):
        return f"{self.user} - {self.listing} : {self.message}  "