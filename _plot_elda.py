
# -*- coding: utf-8 -*-
"""
Reads NetCDF from basepath/output and produces figures via _plot_module.
Exits with code 0 on success (required by CCP main supervisor).
"""
import os
import sys
import glob
import numpy as np
import xarray as xr
from _plot_module import plot_night, plot_day

OUT = 'output'

np.seterr(invalid='ignore')


def main(fromDate, toDate, fromHour, toHour, station, panel, basepath):
    elda_DIR = os.path.join(basepath, OUT)

    # patterns (adjust according to actual filenames inside the ZIP)
    b0355_DIR = glob.glob(os.path.join(elda_DIR, '*_b0355*.nc'))
    b0532_DIR = glob.glob(os.path.join(elda_DIR, '*_b0532*.nc'))
    b1064_DIR = glob.glob(os.path.join(elda_DIR, '*_b1064*.nc'))
    e0355_DIR = glob.glob(os.path.join(elda_DIR, '*_e0355*.nc'))
    e0532_DIR = glob.glob(os.path.join(elda_DIR, '*_e0532*.nc'))

    if not (b0355_DIR and b0532_DIR and b1064_DIR):
        print('EXIT_FAILURE')
        return 1
    if panel == '5p' and not (e0355_DIR and e0532_DIR):
        print('EXIT_FAILURE')
        return 1

    DS_b0355 = xr.open_dataset(b0355_DIR[0], decode_times=False)
    DS_b0532 = xr.open_dataset(b0532_DIR[0], decode_times=False)
    DS_b1064 = xr.open_dataset(b1064_DIR[0], decode_times=False)

    # 355
    b0355 = DS_b0355.backscatter.values
    b0355_e = DS_b0355.error_backscatter.values
    d0355 = DS_b0355.particledepolarization.values
    d0355_e = DS_b0355.error_particledepolarization.values
    v0355 = DS_b0355.volumedepolarization.values
    v0355_e = DS_b0355.error_volumedepolarization.values
    height_b0355 = DS_b0355.altitude.values

    # 532
    b0532 = DS_b0532.backscatter.values
    b0532_e = DS_b0532.error_backscatter.values
    d0532 = DS_b0532.particledepolarization.values
    d0532_e = DS_b0532.error_particledepolarization.values
    v0532 = DS_b0532.volumedepolarization.values
    v0532_e = DS_b0532.error_volumedepolarization.values
    height_b0532 = DS_b0532.altitude.values

    # 1064
    b1064 = DS_b1064.backscatter.values
    b1064_e = DS_b1064.error_backscatter.values
    d1064 = DS_b1064.particledepolarization.values
    d1064_e = DS_b1064.error_particledepolarization.values
    v1064 = DS_b1064.volumedepolarization.values
    v1064_e = DS_b1064.error_volumedepolarization.values
    height_b1064 = DS_b1064.altitude.values

    if panel == '5p':
        DS_e0355 = xr.open_dataset(e0355_DIR[0], decode_times=False)
        DS_e0532 = xr.open_dataset(e0532_DIR[0], decode_times=False)
        e0355 = DS_e0355.extinction.values
        e0355_e = DS_e0355.error_extinction.values
        e0355_bRaman = DS_e0355.backscatter.values
        e0355_bRaman_e = DS_e0355.error_backscatter.values
        height_e0355 = DS_e0355.altitude.values

        e0532 = DS_e0532.extinction.values
        e0532_e = DS_e0532.error_extinction.values
        e0532_bRaman = DS_e0532.backscatter.values
        e0532_bRaman_e = DS_e0532.error_backscatter.values
        height_e0532 = DS_e0532.altitude.values

        # lidar ratios
        S0355 = (e0355 / e0355_bRaman)[0,0,:]
        S0355_e = S0355 * np.sqrt((e0355_e/e0355)**2 + (e0355_bRaman_e/e0355_bRaman)**2)
        S0532 = (e0532 / e0532_bRaman)[0,0,:]
        S0532_e = S0532 * np.sqrt((e0532_e/e0532)**2 + (e0532_bRaman_e/e0532_bRaman)**2)

        # angstrom exponents
        def make_range_consistent(range1, range2, data1, data1_e, data2, data2_e):
            import numpy as _np
            min_h = _np.maximum(range1[0], range2[0])
            max_h = _np.minimum(range1[-1], range2[-1])
            r1s1 = range1[range1 >= min_h]
            r1s2 = r1s1[r1s1 <= max_h]
            r2s1 = range2[range2 >= min_h]
            d1 = data1[0,0,:]
            d1_e = data1_e[0,0,:]
            d2 = data2[0,0,:]
            d2_e = data2_e[0,0,:]
            d1_RD = d1[range1 >= min_h][r1s1 <= max_h]
            d1e_RD = d1_e[range1 >= min_h][r1s1 <= max_h]
            d2_RD = d2[range2 >= min_h][r2s1 <= max_h]
            d2e_RD = d2_e[range2 >= min_h][r2s1 <= max_h]
            return r1s2, d1_RD, d1e_RD, d2_RD, d2e_RD

        r_355_1064, b0355_RD, b0355_e_RD, b1064_RD, b1064_e_RD = \
            make_range_consistent(height_b0355, height_b1064, b0355, b0355_e, b1064, b1064_e)
        AEb_355_1064 = -np.log(b0355_RD/b1064_RD)/np.log(355.0/1064)
        AEb_355_1064_e = np.log(1064/355.)*np.sqrt((b0355_e_RD/b0355_RD)**2 + (b1064_e_RD/b1064_RD)**2)

        r_355_532, b0355_RD, b0355_e_RD, b0532_RD, b0532_e_RD = \
            make_range_consistent(height_b0355, height_b0532, b0355, b0355_e, b0532, b0532_e)
        AEb_355_532 = -np.log(b0355_RD/b0532_RD)/np.log(355.0/532)
        AEb_355_532_e = np.log(532/355.)*np.sqrt((b0355_e_RD/b0355_RD)**2 + (b0532_e_RD/b0532_RD)**2)

        r_532_1064, b0532_RD, b0532_e_RD, b1064_RD, b1064_e_RD = \
            make_range_consistent(height_b0532, height_b1064, b0532, b0532_e, b1064, b1064_e)
        AEb_532_1064 = -np.log(b0532_RD/b1064_RD)/np.log(532.0/1064)
        AEb_532_1064_e = np.log(1064/532.)*np.sqrt((b0532_e_RD/b0532_RD)**2 + (b1064_e_RD/b1064_RD)**2)

        r_a_355_532, e0355_RD, e0355_e_RD, e0532_RD, e0532_e_RD = \
            make_range_consistent(height_e0355, height_e0532, e0355, e0355_e, e0532, e0532_e)
        AEe_355_532 = -np.log(e0355_RD/e0532_RD)/np.log(355.0/532)
        AEe_355_532_e = np.log(532./355.)*np.sqrt((e0355_e_RD/e0355_RD)**2 + (e0532_e_RD/e0532_RD)**2)

        basename = os.path.basename(f"{station}_{fromDate}_{fromHour.replace(':','')}_{toDate}_{toHour.replace(':','')}_{panel}")
        res = plot_night(b0355,b0355_e,height_b0355,b0532,b0532_e,height_b0532,b1064,b1064_e,height_b1064,
                         e0355,e0355_e,height_e0355,e0532,e0532_e,height_e0532,
                         AEb_355_1064,AEb_355_1064_e,r_355_1064,
                         AEb_355_532,AEb_355_532_e,r_355_532,
                         AEb_532_1064,AEb_532_1064_e,r_532_1064,
                         AEe_355_532,AEe_355_532_e,r_a_355_532,
                         S0355,S0355_e,S0532,S0532_e,
                         d0532,d0532_e,v0532,v0532_e,
                         d0355,d0355_e,v0355,v0355_e,
                         d1064,d1064_e,v1064,v1064_e,
                         basename, basepath)
        return 0 if res == 'EXIT_SUCCESS' else 1

    # panel == '3p'
    # angstrom exponents (backscatter only)
    def make_range_consistent(range1, range2, data1, data1_e, data2, data2_e):
        import numpy as _np
        min_h = _np.maximum(range1[0], range2[0])
        max_h = _np.minimum(range1[-1], range2[-1])
        r1s1 = range1[range1 >= min_h]
        r1s2 = r1s1[r1s1 <= max_h]
        r2s1 = range2[range2 >= min_h]
        d1 = data1[0,0,:]
        d1_e = data1_e[0,0,:]
        d2 = data2[0,0,:]
        d2_e = data2_e[0,0,:]
        d1_RD = d1[range1 >= min_h][r1s1 <= max_h]
        d1e_RD = d1_e[range1 >= min_h][r1s1 <= max_h]
        d2_RD = d2[range2 >= min_h][r2s1 <= max_h]
        d2e_RD = d2_e[range2 >= min_h][r2s1 <= max_h]
        return r1s2, d1_RD, d1e_RD, d2_RD, d2e_RD

    r_532_1064, b0532_RD, b0532_e_RD, b1064_RD, b1064_e_RD = \
        make_range_consistent(height_b0532, height_b1064, b0532, b0532_e, b1064, b1064_e)
    AEb_532_1064 = -np.log(b0532_RD/b1064_RD)/np.log(532.0/1064)
    AEb_532_1064_e = abs(np.log(532.0/1064)*((b0532_e_RD/b0532_RD)+(b1064_e_RD/b1064_RD)))

    r_355_532, b0355_RD, b0355_e_RD, b0532_RD, b0532_e_RD = \
        make_range_consistent(height_b0355, height_b0532, b0355, b0355_e, b0532, b0532_e)
    AEb_355_532 = -np.log(b0355_RD/b0532_RD)/np.log(355.0/532)
    AEb_355_532_e = abs(np.log(355.0/532)*((b0355_e_RD/b0355_RD)+(b0532_e_RD/b0532_RD)))

    r_355_1064, b0355_RD, b0355_e_RD, b1064_RD, b1064_e_RD = \
        make_range_consistent(height_b0355, height_b1064, b0355, b0355_e, b1064, b1064_e)
    AEb_355_1064 = -np.log(b0355_RD/b1064_RD)/np.log(355.0/1064)
    AEb_355_1064_e = abs(np.log(355.0/1064)*((b0355_e_RD/b0355_RD)+(b1064_e_RD/b1064_RD)))

    basename = os.path.basename(f"{station}_{fromDate}_{fromHour.replace(':','')}_{toDate}_{toHour.replace(':','')}_{panel}")
    res = plot_day(b0355,b0355_e,height_b0355,b0532,b0532_e,height_b0532,b1064,b1064_e,height_b1064,
                   AEb_355_1064,AEb_355_1064_e,r_355_1064,
                   AEb_355_532,AEb_355_532_e,r_355_532,
                   AEb_532_1064,AEb_532_1064_e,r_532_1064,
                   d0532,d0532_e,v0532,v0532_e,
                   d0355,d0355_e,v0355,v0355_e,
                   d1064,d1064_e,v1064,v1064_e,
                   basename, basepath)
    return 0 if res == 'EXIT_SUCCESS' else 1


if __name__ == '__main__':
    if len(sys.argv) < 8:
        print('ERROR: Provide 7 arguments: fromDate toDate fromHour toHour station panel basepath')
        sys.exit(1)
    fromDate = sys.argv[1]
    toDate = sys.argv[2]
    fromHour = sys.argv[3]
    toHour = sys.argv[4]
    station = sys.argv[5]
    panel = sys.argv[6]
    basepath = sys.argv[7]
    rc = main(fromDate, toDate, fromHour, toHour, station, panel, basepath)
    if rc == 0:
        print('EXIT_SUCCESS')
    else:
        print('EXIT_FAILURE')
    sys.exit(rc)
