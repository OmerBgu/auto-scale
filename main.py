"""

this is the main loop endles loop that each 5 seconds does:
===================

take 5 samples of the server cluster cpu and memory  
----------
intrafacing with kubernetes cli

predict the network delay  
----------
using random forest method (may cahnge easily the clasify algorythem) and according to intial training data
delay formula = =TRUNC(IF(H138<1.2,1,IF(H138<1.5,2,3)))


make decision based on qoe level 
----------
if you are in the right qoe- do nothing if you are lees then it- scale down ,grater then it- check if it is economic woethy anf if so scale uo else go back to the begining 


how to use this project? 
----------
**run this script ./run_main.sh**
**all the parmters are in this script**:

* QOE-number between 1 to 3 ,1 is the the best qualuty of experince and 3 is the worst
* price_per_seconds_of_pod- price of o seconds that 1 pod is wotking in $  
* price_of_deploy_new_pod: price of o seconds that 1 pod is wotking in $ 
* time_slot_money_threshold- the threshold per time slot currently 5 sec wehere if the money spent grater then this dont scale up
* time_of_deploy_new_pod- time in seconds

"""



#!/bin/sh
import sys
import subprocess
import rf
pod =1
#TO DO:
#change awk from file2.txt to manipulate output of kubectl get pod to know the pod number (see the output of it again)
#implement calc of money on is it woth to deploy new pod  on function should_i_deploy() **strated ad naive implementation talk to omer gurevitz on it
#check commands in VM
#talk to reuven on implemnt base on wireshark and not client
def commnad(cmd,arg,out):
	"""short description of the function command

    execute bash command 

    parameteres: the comand and it's arguments

    :returns: output and error if there is
    """
	#p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p=subprocess.Popen([cmd,arg])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	if out!=0:    
		print p.returncode
		print output
   		print err
	else:
		return output
def pods_scale(pod):
	"""short description of the function
    scale up to the pod number  
    """
	#concatenate_cmd='kubectl scale --replicas='+str(pod)+ 'rc test'
	p=subprocess.Popen(['kubectl','scale','--replicas='+str(pod),'rc','test'])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	print p.returncode
	print output
   	print err
	#commnad(concatenate_cmd,'',0)  #kubectl scale --replicas=$pod rc test  > trash.txt
def cmd_arg(arg1,arg2,arg3):
	p=subprocess.Popen([arg1,arg2,arg3])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	return output 
def cmd_4_arg(arg1,arg2,arg3,arg4):
	p=subprocess.Popen([arg1,arg2,arg3,arg4])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	return output
def should_i_deploy(sum_money_spent_in_the_system,price_of_deploy_new_pod,price_per_seconds_of_pod,time_of_deploy_new_pod,time_slot_money_threshold):
	"""short description of the function
    make decision to scale up if price_of_deploy_new_pod*time_of_deploy_new_pod+price_per_seconds_of_pod*pod <time_slot_money_threshold 
    """	
	#implement here a math calculatoin with money and return 1 if 
	#is worth to deploy new pod 0 else
	global pod	
	calc=price_of_deploy_new_pod*time_of_deploy_new_pod+price_per_seconds_of_pod*pod
	if calc<time_slot_money_threshold:
   	     return 1
	else:
        	print "the deploy of a new pod is too expensive at the moment, if you want yo may change the money per time slot threshold"
		return 0
def get_pod_from_output(pods_output):
	"""short description of the function
  	get the pods number from kubectl top pods output 
    """	
	#get the pod numer as int from this string and return it
	return 1
def main():
	"""short description of the function
	main loop 
    """	
	#input check
	if len(sys.argv)<2:
		print "No quality of experince has  entered"
		sys.exit(0)
	else:
		qoe=int(sys.argv[1])
   		#print qoe
  	if qoe> 3 or qoe<1:
		print "The service level need to be between 1 to 3"
   		sys.exit(0)
  	if len(sys.argv)>3:
   		price_per_seconds_of_pod=int(sys.argv[2])#cost of pod per time slot currently per 1 sec
   		price_of_deploy_new_pod=int(sys.argv[3]) 
   		time_slot_money_threshold=int(sys.argv[4])
   		time_of_deploy_new_pod=int(sys.argv[5]) 
  		#commnad('sh','test.sh',0)  #---just for debug 
  		commnad('rm','file2.txt',0) #rm -rf file2.txt
	global pod
	pods_output=cmd_arg('kubectl','get','pods')	
	print pods_output
	pod=get_pod_from_output(pods_output)	#implement this function
  	#ADD manipulate on output of kubectl get pod to get the pod number
	p=cmd_4_arg('awk','END','{print NR}','file2.txt')	
	#pod=int(commnad('awk','END {print NR} '+path,1)) #pod=$( awk 'END {print NR}' file2.txt)     	
	pod=1 #debugging 
  	if pod >1:  #so that we will start simulation from 1 pod
   		pod=1
   		pods_scale(pod)
  	var = 1
	sum_money_spent_in_the_system=0
  	while var == 1 :  # This constructs an infinite loop
         	desicion=1       
		desicion=rf.predict(qoe,pod) 
                sum_money_spent_in_the_system=sum_money_spent_in_the_system+price_per_seconds_of_pod*pod
                if desicion==1:  
                        if should_i_deploy(sum_money_spent_in_the_system,price_of_deploy_new_pod,price_per_seconds_of_pod,time_of_deploy_new_pod,time_slot_money_threshold)==1:  #need to  scale up
                         	pod=pod+1
                                pods_scale(pod)
                if desicion ==-1: #scale down 
                        pod=pod-1
                        pods_scale(pod)
if __name__ == "__main__":
	main()
