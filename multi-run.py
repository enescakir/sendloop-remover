import subprocess
from subprocess import Popen

for i in range(40):
    subprocess.Popen(['python3','migrate.py', '-fsendloop_opens.csv', '-c1000', '-rgmail', '-s' + str(i * 1000), '-lsonuc'  + str(i+1) + '.txt'])
