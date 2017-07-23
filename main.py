#!/bin/sh
import sys
import subprocess
import rf
#TO DO:
#change all auto scale script to python script 
#ADD manipulate on output of kubectl get pod to get the pod number
#implement calc of money on is it woth to deploy new pod  on function should_i_deploy()
#check commands in VM
def commnad(cmd,arg,out):
	#p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p=subprocess.Popen([cmd,arg])
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	if out!=0:		
		print p.returncode
		print output
		print err
	else:
		return output
def pods_scale(pod):
	concatenate_cmd='kubectl scale --replicas='+str(pod)+ 'rc test'
	commnad(concatenate_cmd,'',0)  #kubectl scale --replicas=$pod rc test  > trash.txt

def should_i_deploy(total_money,price_of_deploy_new_pod):
	#implement here a math calculatoin with money and return 1 if 
	# is worth to deploy new pod 0 else	
	return 1

def main():
	#input check	
	if len(sys.argv)<2:
		print "No quality of experince has  entered"
		sys.exit(0)
	else:
		qoe=int(sys.argv[1])
		print qoe
	if qoe> 3 or qoe<1:
		print "The service level need to be between 1 to 3"
		sys.exit(0)
	if len(sys.argv)>3:
		price_per_seconds_of_pod=int(sys.argv[2])
		price_of_deploy_new_pod=int(sys.argv[3])
	commnad('sh','test.sh',0)
	commnad('rm','',0) #rm -rf file2.txt
	pods_output=commnad('kubectl get pods','',1) #kubectl get pods >file2.txt

	#ADD manipulate on output of kubectl get pod to get the pod number
	#pod=int(commnad('awk END {print NR}',file2.txt,1)) #pod=$( awk 'END {print NR}' file2.txt) 	
	pod=2 #debugging 
	if pod >1:  #so that we will start simulation from 1 pod
		pod=1
		pods_scale(pod)
	var = 1
	while var == 1 :  # This constructs an infinite loop
		desicion=rf.predict(qoe,pod)
		total_money=total_money+price_per_seconds_of_pod*pod
		if desicion==1 and should_i_deploy(total_money,price_of_deploy_new_pod)==1:	#need to scale up
			pod=pod+1
			pods_scale(pod)
		if desicion ==-1: #scale down 
			pod=pod-1
			pods_scale(pod)
if __name__ == "__main__":
	main()
