
#!/usr/bin/env python3
"""
*** Lidar data plotting routine (CCP compatible) ***
- Orchestrates: _check_data.py -> _get_data.py -> _plot_elda.py
- Ensures folders exist under --basepath (e.g., /ccp_data)
"""
import os
import sys
import argparse
import subprocess

# relative folders under basepath
TMP = 'tmp'
OUT = 'output'
PLOTS = 'plots'

def dir_set(basepath: str):
    os.makedirs(os.path.join(basepath, TMP), exist_ok=True)
    os.makedirs(os.path.join(basepath, OUT), exist_ok=True)
    os.makedirs(os.path.join(basepath, PLOTS), exist_ok=True)
    return os.path.isdir(os.path.join(basepath, TMP)) and \
           os.path.isdir(os.path.join(basepath, OUT)) and \
           os.path.isdir(os.path.join(basepath, PLOTS))

def check_var(panel: str):
    return panel in ("5p", "3p")

def run_script(args):
    proc = subprocess.run(args, capture_output=True, text=True)
    # pass-through for debugging if needed
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip(), file=sys.stderr)
    return proc.returncode

def main(fromDate, toDate, fromHour, toHour, station, panel, basepath):
    if not dir_set(basepath):
        print('ERROR: unable to set working directories!')
        return 1
    if not check_var(panel):
        print('ERROR: panel mode accepts "5p" or "3p" only!')
        return 1

    # 1) availability check
    rc = run_script([sys.executable, '_check_data.py', fromDate, toDate, station])
    if rc != 0:
        print('ERROR: No data available!')
        return 1

    # 2) download
    rc = run_script([sys.executable, '_get_data.py', fromDate, toDate, fromHour, toHour, station, basepath])
    if rc != 0:
        print('ERROR: No data downloaded!')
        return 1

    # 3) plotting
    rc = run_script([sys.executable, '_plot_elda.py', fromDate, toDate, fromHour, toHour, station, panel, basepath])
    if rc != 0:
        print('ERROR: Plotting failure!')
        return 1

    print('EXIT_SUCCESS')
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description='Download, process and plot EARLINET optical products (CCP compatible).')
    parser.add_argument('--obs_site', type=str, required=True)
    parser.add_argument('--obs_date_min', type=str, required=True)
    parser.add_argument('--obs_date_max', type=str, required=True)
    parser.add_argument('--obs_hour_min', type=str, required=True)
    parser.add_argument('--obs_hour_max', type=str, required=True)
    parser.add_argument('--panel', type=str, required=True, help="'5p' or '3p'")
    parser.add_argument('--basepath', type=str, default='.')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    station = args.obs_site
    fromDate = args.obs_date_min
    toDate = args.obs_date_max
    fromHour = args.obs_hour_min
    toHour = args.obs_hour_max
    panel = args.panel
    basepath = args.basepath

    print('#' * 30)
    print('# Lidar profiles routine')
    print('#' * 30)
    print('Observational site:', station)
    print('Start date:', fromDate)
    print('End date:', toDate)
    print('Start hour:', fromHour)
    print('End hour:', toHour)
    print('Panel:', panel)

    rc = main(fromDate, toDate, fromHour, toHour, station, panel, basepath)
    sys.exit(rc)
