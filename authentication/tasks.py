# tasks.py
# from __future__ import absolute_import, unicode_literals
from celery import shared_task
from web3_interface import contract_interface
from .models import Customer


@shared_task
def event_listener():
    suc, result = contract_interface.event()
    if suc:
        try:        
            c1 = Customer.objects.get(eth_address=result.args.owner)
            if result.args.numberOfNFT not in c1.nft_ids:
                # update user db
                c1.nft_ids.append(result.args.numberOfNFT)
                c1.total_no_of_nfts += 1
                c1.save()
        except Exception as e:
            print (e)



