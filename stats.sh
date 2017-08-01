#!/bin/bash

for run in {1..10}
do
  kubectl top pods --namespace=ruvenname>>log.csv
  date>>log.csv
  sleep 1
done



sed -i 's/CPU(cores)//g' log.csv
sed -i 's/MEMORY(bytes)//g' log.csv
sed -i 's/NAME//g' log.csv
sed -i '/^\s*$/d' log.csv

 t=$(date)
sed -n "s/$/${t}/" log.csv