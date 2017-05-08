import subprocess
from subprocess import Popen

# Start 40 different worker
for i in range(40):
    subprocess.Popen(['python3','remover.py', '-f[FILENAME].csv', '-c[COUNT]', '-r[REGEX]', '-s' + str(i * 1000), '-llog'  + str(i+1) + '.txt'])
