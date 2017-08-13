#!/bin/bash
QOE=1
price_per_seconds_of_pod=5  
price_of_deploy_new_pod=40 
time_slot_money_threshold=10 # the threshold per time slot currently 5 sec wehere if the money spent grater then this dont scale up
price_qoe_1=50
price_qoe_2=25
price_qoe_3=15
penalty=10

python main.py $QOE $price_per_seconds_of_pod $price_of_deploy_new_pod $time_slot_money_threshold $price_qoe_1 $price_qoe_2 $price_qoe_3 $penalty

