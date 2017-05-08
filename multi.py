import subprocess, argparse, os
from subprocess import Popen

# Parse arguments from command line
parser = argparse.ArgumentParser(description='Sendloop unsubscribe app multi runner')
parser.add_argument('-w', '--worker', dest="worker", action='store', required=True)
parser.add_argument('-f', '--file', dest="file", action='store', required=True)
parser.add_argument('-l', '--log', dest="log", action='store', required=True)
arguments = parser.parse_args()

# Worker count
worker = int(arguments.worker)

# File location
file = arguments.file

# Log filename
log = arguments.log

cmd = 'wc -l ' + file
output = subprocess.check_output(cmd,shell=True).strip()
rows = int(output[:str(output).find(" ")-2].decode("utf-8"))

perWorker = (rows + worker) // worker

print("Workers: " + str(worker))
print("Rows: " + str(rows))
print("Rows per worker: " + str(perWorker))

processes = []
# Start 'worker' different worker
for i in range(worker):
    processes.append(subprocess.Popen(['python3','remover.py', '-f' + file, '-c' + str(perWorker), '-s' + str(i * perWorker), '-l' + "temp_" + log + "_" + str(i+1) + '.txt']))

exit_codes = [p.wait() for p in processes]
print("\n\n====== RESULT ==========")
os.system("cat temp_" + log + "_*.txt | sort -n | uniq >> " + log + ".txt")
os.system("rm temp_" + log + "_*.txt")
print(file + " file unsubscribed with " + str(worker) + " workers")
print("Log file: " + log + ".txt")
