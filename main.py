import subprocess


def getQuota(user):
        proc = subprocess.Popen([f"quota {user}"], stdout=subprocess.PIPE, shell=True)
        print()
        (out, err) = proc.communicate()
        out = str(out)
        out = out.split('/dev/sda1')[1]
        out = out.strip()
        used = int(out.split(' ')[0])
        limit = int(out.split(' ')[2])
        print(f'user: {user}')
        print(f'used space: {used}')
        print(f"limit: {limit}")

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