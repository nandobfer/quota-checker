import subprocess, json, sys

def getQuota(user):
    proc = subprocess.Popen([f"whmapi1 showbw searchtype=user search={user} year 2022 month 11 --output=jsonpretty"], stdout=subprocess.PIPE, shell=True)
    print()
    (out, err) = proc.communicate()
    out = json.loads(str(out))
    out = out.split('/dev/sda1')[1]
    out = out.strip()
    used = int(out.split(' ')[0])
    limit = int(out.split(' ')[2])
    print(f'user: {user}')
    print(f'used space: {used}')
    print(f"limit: {limit}")
    
if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
else:
    proc = subprocess.Popen(['ls /home'], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = str(out)
    out = out.split('\\n')
    out.pop(0)
    out.pop(-1)

    for user in out:
        try:
            getQuota(user)
        except:
            pass