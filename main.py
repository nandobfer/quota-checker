import subprocess, json, sys

def getQuota(user):
    proc = subprocess.Popen([f"whmapi1 showbw searchtype=user search={user} year 2022 month 11 --output=json"], stdout=subprocess.PIPE, shell=True)
    print()
    (out, err) = proc.communicate()
    # out = json.loads(str(out)[1:])
    print(str(out)[2:-1])
    print(type(out))
    # out = out.split('/dev/sda1')[1]
    # out = out.strip()
    # used = int(out.split(' ')[0])
    # limit = int(out.split(' ')[2])
    # print(f'user: {user}')
    # print(f'used space: {used}')
    # print(f"limit: {limit}")
    
if __name__ == "__main__":
    user = sys.argv[1]
    getQuota(user)
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