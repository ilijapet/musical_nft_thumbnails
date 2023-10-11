from django.contrib.postgres.fields import ArrayField
from django.db import models



class Customer(models.Model):
    
    CRYPTO = "CRYPTO"
    CREDIT = "CREDIT"

    OPTIONS = [
        (CRYPTO, "cypto buyer"),
        (CREDIT, "credit card buyer")
    ]
    
    created_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name  = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, blank=True) 
    email = models.EmailField(max_length=250, blank=True)
    type = models.CharField( 
        max_length = 20, 
        choices = OPTIONS, 
        default = 'CRYPTO'
        ) 
    total_no_of_nfts = models.IntegerField(default=0)
    nft_ids = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True) 
    nft_metadata_ids = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True) 

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")

    

# class NFTMetadata(models.Model):
    # attributes = 
    # descrition = text
    # external_link = url
    # img = link to ipfs
    # name = name