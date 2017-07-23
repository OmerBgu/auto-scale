#!/bin/bash
QOE=1
price_per_seconds_of_pod=5  
price_of_deploy_new_pod=40 

python main.py $QOE $price_per_seconds_of_pod $price_of_deploy_new_pod

