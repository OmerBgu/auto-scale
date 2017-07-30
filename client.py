"""
client simulation  
===================

this is the inital hand-shake of a new client 
----------
this program is a simple client simulation that enterd based on posin entrance to the server
and capture the network delay on the client side 
"""


import subprocess
import time
import numpy as np
import webbrowser
import requests
import csv
import datetime
import sys



if __name__ == "__main__":
    #this script take as a parameter the pods number
    url='http://a8826b8f8422b11e791bf061beb5b7cb-726656503.us-west-2.elb.amazonaws.com/'
    #yakurl='http://a8826b8f8422b11e791bf061beb5b7cb-726656503.us-west-2.elb.amazonaws.com/'


    for x in range(0, 100):
        #print ("x= %d"%(x))
        response=requests.get(url)
        #response2 = requests.get(urlscl)
        #response3 = requests.get(yakurl)
        with open('DataDelay.csv', 'a', newline='') as csvfile:
            fieldnames = ['delay time', 'date','pods']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            delay=response.elapsed.total_seconds()
            #date=response.headers['Date']
            date = datetime.datetime.now()
            writer.writerow({'delay time': delay, 'date': date,'pods':sys.argv[1]})


        #incognito mode to enter and watch the entire movie
        if x < 10:
            subprocess.Popen(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "-incognito", url])
        t = np.random.exponential(2)





