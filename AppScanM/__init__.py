import subprocess
from flask import abort
PROCESS = subprocess.Popen('ipconfig',encoding='utf-8', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='ignore')
PROCESS.stdout.readlines()
def run_cmd(command):
    try:
        output = []
        if not PROCESS.poll(): 
            output.append("PROCESS is Active.")
            PROCESS.stdin.write(command)
            PROCESS.stdin.flush()
        else:
            PROCESS.stdin.
        output = PROCESS.stdout.readlines()
        error = PROCESS.stderr.readlines()
        return {"output":output,"error":error}
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return abort(500,e)
    except Exception as e:
        print("Exception occurred:", e)
        return abort(500,e)
