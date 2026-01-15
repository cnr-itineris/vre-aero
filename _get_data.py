
#!/usr/bin/env python3
"""
*** EARLINET file download procedure (CCP compatible, DEBUG + fallback) ***
- Validates inputs
- Queries ACTRIS-ARES API (opticalproducts) with proper params
- If time window returns no files, falls back to full-day query
- Downloads ZIP and extracts NetCDF files under basepath/output
- DEBUG=1 env var prints verbose diagnostics
"""
import os, sys, glob, requests, zipfile
from datetime import datetime
from urllib.parse import unquote

levels = '1.0'
TMP = 'tmp'
OUT = 'output'

def _debug():
    return os.environ.get('DEBUG') == '1'

def validate_inputs(fromDate, toDate, fromHour, toHour):
    try:
        datetime.strptime(fromDate, '%Y-%m-%d')
        datetime.strptime(toDate, '%Y-%m-%d')
        datetime.strptime(fromHour, '%H:%M')
        datetime.strptime(toHour, '%H:%M')
        return True
    except ValueError:
        return False

def _optical_query(fromDate, toDate, fromHour, toHour, station):
    url = 'https://api.actris-ares.eu/api/services/restapi/opticalproducts'
    params = {
        'fromDate': fromDate,
        'toDate': toDate,
        'fromDayTime': fromHour,
        'toDayTime': toHour,
        'stations': station,
        'levels': levels,
        'opticaltype': 'particledepolarization',
        'particledepolarization': 'true',
    }
    if _debug():
        print(f"[DBG] GET {url} params={params}")
    try:
        r = requests.get(url, params=params, headers={'Accept':'application/json'}, timeout=60)
        if _debug():
            print(f"[DBG] status={r.status_code}")
        if r.status_code != 200:
            return None
        return r.json()
    except requests.RequestException as e:
        if _debug():
            print(f"[DBG] request error: {e}")
        return None

def _collect_filenames(metadata):
    names = []
    for it in metadata:
        if 'Filename' in it:
            names.append(it['Filename'])
        elif 'filename' in it:
            names.append(it['filename'])
    return sorted(set(names))

def _download_zip(filenames_csv, file_name, basepath):
    dst_dir = os.path.join(basepath, TMP)
    os.makedirs(dst_dir, exist_ok=True)

    target_zip = os.path.join(dst_dir, file_name)
    if os.path.exists(target_zip):
        if _debug():
            print("[DBG] ZIP already present, skip download")
        return target_zip

    url = 'https://api.actris-ares.eu/api/services/restapi/opticalproducts/downloads'
    params = {'filenames': filenames_csv}
    if _debug():
        print(f"[DBG] GET {url} params={params}")
    try:
        r = requests.get(url, params=params, headers={'Accept':'application/zip'}, timeout=120)
    except requests.RequestException as e:
        if _debug():
            print(f"[DBG] download error: {e}")
        return None

    if _debug():
        print(f"[DBG] status={r.status_code} content-type={r.headers.get('content-type')}")

    if r.status_code != 200:
        return None

    ctype = (r.headers.get('content-type') or '').lower()
    if 'zip' not in ctype:
        if _debug():
            snippet = r.text[:500] if hasattr(r, 'text') else ''
            print(f"[DBG] Unexpected content-type: {ctype} body[:500]={snippet}")
        return None

    cd = r.headers.get('content-disposition','')
    if 'filename=' in cd:
        temp_file = unquote(cd.split('filename=', 1)[1].strip().strip('"'))
    else:
        temp_file = 'download.zip'

    tmp_zip = os.path.join(dst_dir, temp_file)
    with open(tmp_zip, 'wb') as f:
        f.write(r.content)

    if os.path.exists(target_zip):
        os.remove(target_zip)
    os.replace(tmp_zip, target_zip)
    return target_zip

def main(fromDate, toDate, fromHour, toHour, station, basepath):
    if not validate_inputs(fromDate, toDate, fromHour, toHour):
        print('EXIT_FAILURE'); return 1

    os.makedirs(os.path.join(basepath, TMP), exist_ok=True)
    os.makedirs(os.path.join(basepath, OUT), exist_ok=True)

    md = _optical_query(fromDate, toDate, fromHour, toHour, station)
    filenames = _collect_filenames(md or [])

    if not filenames:
        if _debug():
            print("[DBG] No filenames in time window, fallback to full day")
        md_day = _optical_query(fromDate, toDate, '00:00', '23:59', station)
        filenames = _collect_filenames(md_day or [])

    if _debug():
        print(f"[DBG] filenames count={len(filenames)}")
        if filenames[:3]:
            print(f"[DBG] sample filenames={filenames[:3]}")

    if not filenames:
        print('EXIT_FAILURE'); return 1

    zip_logical_name = (
        f"EARLINET_AerRemSen_{station}_"
        f"{fromDate.replace('-','')}_{toDate.replace('-','')}_"
        f"{fromHour.replace(':','')}_{toHour.replace(':','')}.zip"
    )
    zip_path = _download_zip(','.join(filenames), zip_logical_name, basepath)
    if not zip_path:
        print('EXIT_FAILURE'); return 1

    for path in glob.glob(os.path.join(basepath, OUT, '*.nc')):
        try: os.remove(path)
        except OSError: pass

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(os.path.join(basepath, OUT))
    except zipfile.BadZipFile:
        print('EXIT_FAILURE'); return 1

    found_nc = []
    for root, _, files in os.walk(os.path.join(basepath, OUT)):
        for f in files:
            if f.lower().endswith('.nc'):
                found_nc.append(os.path.join(root, f))

    if _debug():
        print(f"[DBG] extracted .nc count={len(found_nc)}")

    if found_nc:
        print('EXIT_SUCCESS'); return 0
    else:
        print('EXIT_FAILURE'); return 1

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('ERROR: Provide 6 arguments: fromDate toDate fromHour toHour station basepath')
        sys.exit(1)
    rc = main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    sys.exit(rc)
