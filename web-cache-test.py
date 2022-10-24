#!/usr/bin/env python3

import subprocess
import sys
import time

url = 'https://192.168.100.50:4444/account-data?id=20002'
# url = 'https://10.89.60.52:4444/account-data?id=20002'

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, timeout=10, capture_output=True)

    except subprocess.TimeoutExpired as timeout_err:
        print('Request {} timed out'.format(command))

    except subprocess.CalledProcessError as err:
        retcode = err.returncode
        print('Error executing: ' + command)
        print('Exit Code: ' + str(retcode))
        sys.exit(retcode)

    except KeyboardInterrupt:
        sys.exit("Exiting...")

    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit("Exiting...")


counter = 0

try:
    while True:
        t1 = time.time()
        run_command('curl -k -v --url ' + url)
        t2 = time.time()
        print('Request no: {} handled in {} ms'.format(counter, (t2 - t1) * 1000))
        time.sleep(0.1)
        counter = counter + 1

except KeyboardInterrupt:
    sys.exit("Exiting...")
