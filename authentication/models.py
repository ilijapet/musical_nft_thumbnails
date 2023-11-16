from django.contrib.postgres.fields import ArrayField
from django.db import models


class NFTMetadata(models.Model):
    name = models.CharField(verbose_name="ime pevaca", max_length=100)
    description = models.CharField(max_length=2000)
    cover_file_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    CRYPTO = "CRYPTO"
    CREDIT = "CREDIT"

    OPTIONS = [(CRYPTO, "cypto buyer"), (CREDIT, "credit card buyer")]

    created_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, blank=True)
    eth_address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=250, blank=True)
    type = models.CharField(
        max_length=20,
        choices=OPTIONS,
        # default="CRYPTO"
    )
    total_no_of_nfts = models.IntegerField(default=0)
    nft_ids = ArrayField(
        models.IntegerField(null=True, blank=True), null=True, blank=True
    )
    nft_metadata = models.ManyToManyField(NFTMetadata)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
