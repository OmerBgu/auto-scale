#!/bin/bash
export PATH=/home/ubuntu/kubernetes/platforms/linux/amd64:$PATH
qoe=$1
if [[ -z "$qoe" ]]; then
   printf '%s\n' "No quality of experince has  entered"
   exit 1
fi
if (($qoe > 3 )); then
 echo "The service level need to be between 1 to 3"
 exit
fi
#snaity check
if (($qoe < 0 )); then
 echo "The service level need to be between 1 to 3"
 exit
fi
sleep 1
rm -rf file2.txt
kubectl get pods >file2.txt
pod=$( awk 'END {print NR}' file2.txt)
pod=$((pod-1)) #temp= number of pods
#echo $temp
if (($pod > 1 )); then
 kubectl scale --replicas=1 rc test  > trash.txt #scale to 1 pod only if there is more pods in the system
fi
pod=1
while [ 1 ]
do
rm -rf file2.txt
rm -rf test.csv
./test.sh #take 5 samples
#sleep 1
kubectl get pods >file2.txt
pod=$( awk 'END {print NR}' file2.txt)
pod=$((pod-1))
pod=1
python rf.py $qoe  $pod
answer=$?
#echo $answer #debug
#echo $answer #for debug
if (( $answer==1 && after_scale!=1 ));then
   echo 'scale up'
  # echo $answer
   pod=$((pod+1))
 # echo "pod="
 # echo $pod  #debug prints
   kubectl scale --replicas=$pod rc test  > trash.txt
  # kubectl scale --replicas=5 rc test
  # exit
 after_scale=1
elif(( $answer ==2 && $pod>1 ));
then
   echo 'scale down'
   pod=$((pod-1))
   kubectl scale --replicas=$pod rc test
else
 echo 'no scale is needed'
 after_scale=0
fi
done
