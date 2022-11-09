import subprocess, json, sys
from datetime import datetime
# from hurry.filesize import size, si

now = datetime.now()

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

def perDay(bw):
    bw_per_day = bw / now.day
    return bw_per_day

def estimatedTotal(bw_per_day):
    bw_final = bw_per_day * 30
    return bw_final

def getSolvedLimit(bw_final):
    limit = bw_final * 100 / 75
    return limit
    
def getQuota(user):
    proc = subprocess.Popen([f"whmapi1 showbw searchtype=user search={user} year 2022 month 11 --output=json"], stdout=subprocess.PIPE, shell=True)
    print()
    (out, err) = proc.communicate()
    out = json.loads(str(out)[2:-1])['data']['acct'][0]
    used = int(out['totalbytes'])
    limit = int(out['limit'])
    print(f'user: {user}')
    print(f'used space: {size(used)}')
    print(f"limit: {size(limit)}")
    
    per_day = perDay(used)
    estimated_total = estimatedTotal(per_day)
    new_limit = getSolvedLimit(estimated_total)
    
    print(f'bandwidth per day: {size(per_day)}')
    print(f'estimated bandwidth at months end: {size(estimated_total)}')
    print(f'recomended limit: {size(new_limit)}')
    
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