#!/bin/sh
import sys
import subprocess
import rf
#TODO: change all auto scale script to python script 
def commnad(cmd,arg,output):
	#p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	if arg!='to_file':	
		p=subprocess.Popen([cmd,arg])
		output, err = p.communicate(b"input data that is passed to subprocess' stdin")
		print p.returncode
		print output
		print err
	else:
		p=subprocess.Popen([cmd>file2.txt])
	if output==1:
		return output


def main():
	if len(sys.argv)<2:
		print "No quality of experince has  entered"
	else:
		qoe=sys.argv[1]
	if qoe> 3 or qoe<1:
		print "The service level need to be between 1 to 3"
	
	
	commnad('sh','test.sh',0)
	commnad('rm','file2.txt',0) #rm -rf file2.txt
	#commnad('kubectl get pods','to_file') #kubectl get pods >file2.txt
	#pod=int(commnad('awk END {print NR}',file2.txt,1)) #pod=$( awk 'END {print NR}' file2.txt) 	
	pod=1
	pod=1 #debugging 
	if pod >1:  #so that we will start simulation from 1 pod
		concatenate_cmd='kubectl scale --replicas='+str(pod)+ 'rc test'
		commnad(concatenate_cmd,'to_file',0)  #kubectl scale --replicas=$pod rc test  > trash.txt
	
	desicion=rf.predict(qoe,pod)
if __name__ == "__main__":
	main()
