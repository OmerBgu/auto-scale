rm -rf test.csv
for run in {1..5}
do
 echo $(./sample.sh) >> test.csv

done

