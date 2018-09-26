import csv
from apscheduler.schedulers.background import BackgroundScheduler
import time
from shutil import copyfile
import os

#TODO :install apscheduler with pip install apscheduler


def parse(pod_name):

    top_output = "top_output.txt"
    #TODO : chagne the copy copyfile to this line of kubectl top
    #os.system("kubectl top node >> top_output.txt")
    copyfile("top_output_example", "top_output.txt")

    # open and read the txt file.
    text_file = open(top_output, "r")

    # Read each line of text file and save it in lines.
    lines = text_file.readlines()
    text_file.close()
    # open the csv file in append mode.
    mycsv = csv.writer(open('train.csv', 'a',newline=''))

    #  kube-system-test  fluentd-gcp-v2.0-z6xh9              100m (10%)  0 (0%)      200Mi (11%) 300Mi (17%)
    for line in lines:
        if pod_name in line:
                cpu_requests_milicore = line.split()[2].split("m")[0]
                cpu_requests_precent = line.split()[3]
                cpu_requests_precent = cpu_requests_precent.split('(', 1)[1].split(')')[0].split("%")[0]
                cpu_limit_milicore = line.split()[4].split("m")[0]
                memory_requests_Mi = line.split()[6].split("M")[0]
                memory_requests_precent = line.split()[7].split('(', 1)[1].split(')')[0].split("%")[0]
                memory_limits_Mi = line.split()[8].split("M")[0]
                memory_limits_precent = line.split()[9].split('(', 1)[1].split(')')[0].split("%")[0]
                print("cpu_requests_milicore : {0} cpu_requests_precent : {1} cpu_limit_milicore : {2} memory_requests_Mi  : {3} "
                      "memory_requests_precent : {4} memory_limits_Mi : {5} memory_limits_precent : {6}".format(cpu_requests_milicore,cpu_requests_precent,cpu_limit_milicore,memory_requests_Mi,memory_requests_precent,memory_limits_Mi,memory_limits_precent))
                mycsv.writerow([cpu_requests_milicore, cpu_requests_precent, cpu_limit_milicore, memory_requests_Mi,
                                memory_requests_precent, memory_limits_Mi,memory_limits_precent])
    if os.path.exists(top_output):
        os.remove(top_output)
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        pod_name= sys.argv[1]
    else:
        pod_name ="kube-system-test"

    with open('train.csv', 'w',newline='') as outcsv:
        writer = csv.writer(outcsv)
        # Write header for csv file.
        writer.writerow(["cpu_requests_milicore", "cpu_requests_precent", "cpu_limit_milicore", "memory_requests_Mi","memory_requests_precent", "memory_limits_Mi", "memory_limits_precent"])

    sched = BackgroundScheduler()
    sched.add_job(parse, 'interval', seconds=1,args=[pod_name])
    sched.start()
    time.sleep(5)

    sched.shutdown()
