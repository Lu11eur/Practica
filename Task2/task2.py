import sys
from datetime import datetime

def log(mess):
    time = datetime.now()
    print(f'|{time}| {mess}', file=sys.stderr)

log("something")
