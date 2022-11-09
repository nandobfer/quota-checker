import subprocess, json, sys
from datetime import datetime
# from hurry.filesize import size, si

now = datetime.now()

def size(value):
    return round(value / float(1<<20), 2)

def formated_size(value):
    return f'{value} mb'

def perDay(bw):
    bw_per_day = bw / now.day
    return bw_per_day

def estimatedTotal(bw_per_day):
    bw_final = bw_per_day * 30
    return bw_final

def getSolvedLimit(bw_final):
    limit = bw_final * 100 / 75
    return limit

def setLimit(user, value):
    try:
        proc = subprocess.Popen([f"whmapi1 limitbw user={user} bwlimit={value} --output=json"], stdout=subprocess.PIPE, shell=True)
        print()
        (out, err) = proc.communicate()
        print(f'limit updated to: {formated_size(value)}')
    except:
        print(f'failed to update {user} limit')

def getQuota(user):
    proc = subprocess.Popen([f"whmapi1 showbw searchtype=user search={user} year 2022 month 11 --output=json"], stdout=subprocess.PIPE, shell=True)
    print()
    (out, err) = proc.communicate()
    out = json.loads(str(out)[2:-1])['data']['acct'][0]
    used = int(out['totalbytes'])
    limit = int(out['limit'])
    print(f'user: {user}')
    print(f'used bandwidth: {formated_size(size(used))}')
    print(f"limit: {formated_size(size(limit))}")
    
    per_day = perDay(used)
    estimated_total = estimatedTotal(per_day)
    new_limit = getSolvedLimit(estimated_total)
    
    print(f'bandwidth per day: {formated_size(size(per_day))}')
    print(f'estimated bandwidth at months end: {formated_size(size(estimated_total))}')
    print(f'recomended limit: {formated_size(size(new_limit))}')
    setLimit(user, int(size(new_limit)))
    
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