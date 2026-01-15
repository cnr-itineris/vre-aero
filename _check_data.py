
#!/usr/bin/env python3
"""
*** EARLINET data availability check (CCP compatible) ***
- Queries ACTRIS-ARES opticalproducts for a whole-day window
- Succeeds if at least 1 file is available
"""
import sys
import requests
from datetime import datetime

LEVELS = '1.0'

def validate_date(s):
    try:
        datetime.strptime(s, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_optical_product(fromDate, toDate, station):
    if not (validate_date(fromDate) and validate_date(toDate)):
        return None
    url = 'https://api.actris-ares.eu/api/services/restapi/opticalproducts'
    params = {
        'fromDate': fromDate,
        'toDate': toDate,
        'fromDayTime': '00:00',
        'toDayTime': '23:59',
        'stations': station,
        'levels': LEVELS,
        'opticaltype': 'particledepolarization',
        'particledepolarization': 'true',
    }
    try:
        r = requests.get(url, params=params, headers={'Accept': 'application/json'}, timeout=60)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.RequestException:
        return None

def main(fromDate, toDate, station):
    payload = get_optical_product(fromDate, toDate, station)
    if not payload:
        print('EXIT_FAILURE')
        return 1
    files = [x.get('ID') for x in payload if 'ID' in x]
    if len(files) > 0:
        print('EXIT_SUCCESS')
        return 0
    print('EXIT_FAILURE')
    return 1

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('ERROR: Provide 3 arguments: fromDate toDate station')
        sys.exit(1)
    fromDate = sys.argv[1]
    toDate = sys.argv[2]
    station = sys.argv[3]
    sys.exit(main(fromDate, toDate, station))
