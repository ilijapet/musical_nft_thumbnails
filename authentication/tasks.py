# tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from web3_interface import contract_interface
from models import Customer


@shared_task
def event_listener():
    suc, result = contract_interface.event()
    if suc:
        # c1 = Customer.objects.get(eth_adderss=result.args.owner)
            # update database of users to have eth address field
        # take user based on eth address
        # check if user already have that song
        # if not, add it to the database
        print(type(result.args.numberOfNFT), result.args.numberOfNFT, type(result.args.owner), result.args.owner)



