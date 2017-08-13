"""

this is the main loop endles loop that each 5 seconds does:
===================

take 5 samples of the server cluster cpu and memory  
----------
using the with kubernetes cli

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
#implement calc of money on is it woth to deploy new pod  on function should_i_deploy() **strated ad naive implementation talk to omer gurevitz on it
#check commands in VM
#implement sample that replace sample.sh
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
    scale up to the pod number and then sleep for 3 second so that system will updatede  
    """
	#concatenate_cmd='kubectl scale --replicas='+str(pod)+ 'rc test'
	p=subprocess.Popen(['kubectl','scale','--replicas='+str(pod),'rc','test'])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	print p.returncode
	print output
   	print err
	sleep (3)
def cmd_arg(arg1,arg2,arg3):
	p=subprocess.Popen([arg1,arg2,arg3])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	return output 
def cmd_4_arg(arg1,arg2,arg3,arg4):
	p=subprocess.Popen([arg1,arg2,arg3,arg4])
	output, err = p.communicate(b"input data that is passed to subprocess stdin")
	return output
	"""this function is checking threshold policy if it is larger then 70%
	 in cpu or in memory return -1 means not worty to cale up else worth to scale up 
      
    """
def threshold_policy(pod):
	with open('/home/omer/Downloads/pods_status.txt') as f:
			wordlist = [r.split()[2] for r in f]
			cpu1= int (wordlist[1][0])*10+int (wordlist[1][1])
			cpu2= int (wordlist[2][0])*10+int (wordlist[2][1])
			if cpu1>0.7  or cpu2>0.7 :
				return -1
			wordlist = [r.split()[4] for r in f]
			print wordlist
			mem=int (wordlist[1][0])*10+int (wordlist[1][1])
			if mem >0.7 :
				return -1
			return 1
			

def should_i_deploy(Money_Spent,price_of_deploy_new_pod,price_per_seconds_of_pod,Money_Profit,time_slot_money_threshold):
	"""short description of the function
    make decision to scale up if price_of_deploy_new_pod+price_per_seconds_of_pod*pod <time_slot_money_threshold 
    """	
	#implement here a math calculatoin with money and return 1 if 
	#is worth to deploy new pod 0 else
	global pod	
	calc=price_of_deploy_new_pod+price_per_seconds_of_pod*pod
	if calc<time_slot_money_threshold:
   	     return 1
	else:
        	print "the deploy of a new pod is too expensive at the moment, larger then user threshold"
		return 0
def get_pod_from_output(pods_output):
	"""short description of the function
  	get the pods number from kubectl top pods output 
    """	
	with open('/home/omer/Downloads/get_pod.txt') as f:
    		 pods=sum(1 for _ in f)
	pods=pods-1	
	print ('pods number is %d'%(pods) )	
	#get the pod numer as int from this string and return it
	return pods
def sample():
	'''
	this function take 5 seconds of sample via kubectl top pods
	replace the sample.sh script
	'''
def main():
	"""short description of the function
	main loop 
    """	
	#input check
	price_qoe = [0] * 4 #array of 3 prices in index 0 qoe price 1 ,index 1 aoe price 2...
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
   		price_qoe[0]=int(sys.argv[5]) 
		price_qoe[1]=int(sys.argv[6])
		price_qoe[2]=int(sys.argv[7])
		price_qoe[3]=int(price_qoe[2]/2) # the last qoe price we can charge for giving qoe level worest then 3 is half of 3
		penalty=int(sys.argv[8]) 
  		#commnad('sh','test.sh',0)  #---just for debug 
  		commnad('rm','file2.txt',0) #rm -rf file2.txt 
	threshold_policy(2)
	global pod
	pods_output=cmd_arg('kubectl','get','pod')
	#maybe change to -> kubectl top pod --capacity	
	pod=get_pod_from_output(pods_output)	#implement this function
  	#ADD manipulate on output of kubectl get pod to get the pod number
	#p=cmd_4_arg('awk','END','{print NR}','file2.txt')	
	pod=1 #debugging 
  	if pod >1:  #so that we will start simulation from 1 pod
   		pod=1
   		pods_scale(pod)
  	var = 1
	Money_Spent=0
	Money_Profit=0
  	while var == 1 :  # This constructs an infinite loop
         	desicion=1       
		desicion=rf.predict(qoe,pod) 
                Money_Spent=Money_Spent+price_per_seconds_of_pod*pod
                if desicion==1:  
			Money_Profit=Money_Profit-penalty+price_qoe[qoe]*pod #price_qoe[qoe] is in qoe 1 worst then you shold be 
                        if should_i_deploy(Money_Spent,price_of_deploy_new_pod,price_per_seconds_of_pod,Money_Profit,time_slot_money_threshold)==1:  #need to  scale up
                         	pod=pod+1
                                pods_scale(pod)
                if desicion ==-1: #scale down 
			Money_Profit=Money_Profit+price_qoe[qoe-1]*pod #add standart money to profit                        
			pod=pod-1
                        pods_scale(pod)
		if desicion ==0: #nothing just add money to profit
			Money_Profit+Money_Profit+price_qoe[qoe-1]*pod 
if __name__ == "__main__":
	main()
