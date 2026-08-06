import subprocess
print("Run system command from Python:")

res = subprocess.run(["ls", ], capture_output=True, text=True)
print(res.stdout)
with open("sample.sql", "r") as filehandle:
    res = subprocess.run(["mariadb","-utango", "-ptango"], capture_output=True, stdin=filehandle, text=True)
print(res.stdout)

print (res.returncode)

print("The end.")