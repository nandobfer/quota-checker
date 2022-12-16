import subprocess, json, sys
from datetime import datetime
from burgos.mysql_handler import Mysql
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
        proc = subprocess.Popen([f"/usr/sbin/whmapi1 limitbw user={user} bwlimit={value} --output=json"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print(f'limit updated to: {formated_size(value)}')
    except:
        print(f'failed to update {user} limit')
        
def logHistory(data):
    mysql = Mysql({
        'host': 'app.agenciaboz.com.br',
        'user': 'python',
        'password': 'SucessoZOP2022!',
        'database': 'agenciaboz_sistema'
    }, '')
    mysql.connect()
    # print(data)

    columns = "(user, used, prediction, date)"
    values = f"""("{data["user"]}", {data["used"]}, {data["prediction"]}, current_date())"""
    sql = f"""INSERT INTO historico_bandwitdh {columns} VALUES {values} ;"""
    
    mysql.run(sql)
    mysql.disconnect()
    
def getAccountUser(user, out, index):
    data = json.loads(str(out)[2:-1])['data']['acct'][index]
    if data['user'] == user:
        return data
    else:
        index += 1
        data = getAccountUser(user, out, index)
        
    return data

def getQuota(user):
    proc = subprocess.Popen([f"/usr/sbin/whmapi1 showbw searchtype=user search={user} year {now.year} month {now.month} --output=json"], stdout=subprocess.PIPE, shell=True)
    print()
    (out, err) = proc.communicate()
    try:
        data = getAccountUser(user, out, 0)
    except:
        print(f"""user {user} doesn't have an acct:""")
        return False
    used = int(data['totalbytes'])
    try:
        limit = int(data['limit'])
    except:
        print(f"{user}'s limit is configured as unlimited.")
        return False
        
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
    logHistory({'user': user, 'used': size(used), 'prediction': size(estimated_total)})
    
user = sys.argv[1]
getQuota(user)