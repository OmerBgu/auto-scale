rm -rf file2.txt log1.csv log3.csv log4.csv
#for run in {1..1}
#do
  kubectl top pods >>log1.csv
  date>>log.csv
  dat=$(date +%T)
 sleep 1
#done
rm -rf file2.txt 
 kubectl get pods >>file2.txt

sed -i '/NAME         READY     STATUS    RESTARTS   AGE/d' ./file2.txt	
  temp=$( awk 'END {print NR}' file2.txt)
sed -i 's/CPU(cores)//g' log1.csv
sed -i 's/MEMORY(bytes)//g' log1.csv
sed -i 's/NAME//g' log1.csv
sed -i '/^\s*$/d' log1.csv
sed -i '/^\stest*$/d' log1.csv
sed -i 's/Mi//g' log1.csv
sed -i 's/m//g' log1.csv 
awk -F' ' '{ print $2" , "$3 " ," }' log1.csv >> log3.csv
echo $(cat log3.csv) > log4.csv
sed -i "s|$| "$temp"|" log4.csv
sed -i "s|$| "" , "$dat"|" log4.csv
cat log4.csv

