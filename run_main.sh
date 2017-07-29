#!/bin/bash
QOE=1
price_per_seconds_of_pod=5  
price_of_deploy_new_pod=40 
time_slot_money_threshold=10 # the threshold per time slot currently 5 sec wehere if the money spent grater then this dont scale up
time_of_deploy_new_pod=2

python main.py $QOE $price_per_seconds_of_pod $price_of_deploy_new_pod $time_slot_money_threshold $time_of_deploy_new_pod

