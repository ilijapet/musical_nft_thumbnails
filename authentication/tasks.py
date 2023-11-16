# tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from web3_interface import contract_interface


@shared_task
def event_listener():
    # task code here
    result = contract_interface.event()
    return result


