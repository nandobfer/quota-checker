import subprocess, json, sys
from datetime import datetime
from hurry.filesize import size, si

now = datetime.now()

def perDay(bw):
    bw_per_day = bw / now.day
    return bw_per_day
    
def getQuota(user):
    proc = subprocess.Popen([f"whmapi1 showbw searchtype=user search={user} year 2022 month 11 --output=json"], stdout=subprocess.PIPE, shell=True)
    print()
    (out, err) = proc.communicate()
    out = json.loads(str(out)[2:-1])['data']['acct'][0]
    used = int(out['totalbytes'])
    limit = int(out['limit'])
    print(f'user: {user}')
    print(f'used space: {size(used, system=si)}')
    print(f"limit: {size(limit, system=si)}")
    
    print(f'bandwidth per day: {perDay(used)}')
    
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