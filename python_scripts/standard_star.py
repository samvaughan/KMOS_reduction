"""
Take a folder containing observations of a telluric star. 
Make a .sof file of those observations, as well as the required calibrations. 
Make the requried output directories. 
Run the esorex recipe kmos_std_star with that .sof file
"""



import sys
import os
import argparse
from astropy.io import fits
import glob
import logging
from optparse import OptionParser


from KMOS_tools import kmos_functions as KF


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="KMOS Standard Star Reduction Script")
    parser.add_argument('reduced_file_destination', type=str, help='Location for reduced standard star cubes')
    parser.add_argument('input_files', type=str, help='Location of standard star files')
    parser.add_argument('calibration_data_location', type=str, help='Location of (dynamic) calibration files: XCAL, YCAL, LCAL, MASTER_FLAT')
    parser.add_argument('--static_calib_location', type=str, help='Optional: Location of static calibration files (WAVE_BAND). Otherwise assume /Data/KCLASH/Data/Static_Cals/cal/')
    args=parser.parse_args()

    reduced_file_destination=os.path.abspath(args.reduced_file_destination)
    file_location=os.path.abspath(args.input_files)
    calibration_data_location=os.path.abspath(args.calibration_data_location)
    static_calib_location=args.static_calib_location

    if static_calib_location is not None:
        kmos_static_calib_directory=os.path.abspath(static_calib_location)
    else:
        kmos_static_calib_directory='/Data/KCLASH/Data/Static_Cals/cal'



    #Optional arguments. Code left over from original script and isn't used any more
    usage = "usage: %prog [options] data_dir"
    parser = OptionParser(usage=usage, description="KMOS Calibration Data Generation Script")
    parser.add_option("-p", "--parallel", action="store_true", dest="parallel", default=False, help="Parallel execution of esorex")
    parser.add_option("-d", "--description", action="store_true", dest="description", default=False, help="Detailed Description")
    parser.add_option("-b", "--band", default="All", help="Band that needs to be reduced (H, K, HK, YJ, IZ) [default: %default]")
    (options, args) = parser.parse_args()

    logging.info("Parallel Mode: {0}".format(options.parallel))
    logging.info("Description required: {0}".format(options.description))
    logging.info("Desired Band: {0}".format(options.band))




    # Loop on all files in the input directory
    star_list = []
    for file in glob.glob(file_location+"/KMOS*star*.fits"):
        # Read the Primary header
        fname=os.path.abspath(file)
        hdu = fits.getheader(fname, 0)
        tpl_id = hdu['HIERARCH ESO TPL ID']
        # Only keep the proper TPL.ID
        if tpl_id in ["KMOS_spec_cal_stdstar"]:
            star_list.append({   'name': fname, 
                        'tpl_id': tpl_id, 
                        'tpl_start': hdu['HIERARCH ESO TPL START'],
                        'tpl_nexp': hdu['HIERARCH ESO TPL NEXP'],
                        'tpl_expno': hdu['HIERARCH ESO TPL EXPNO'],
                        'dpr_type': hdu['HIERARCH ESO DPR TYPE'],
                        'obs_start': hdu['HIERARCH ESO OBS START'],
                        'band': hdu['HIERARCH ESO INS GRAT1 ID']})

    #if not os.path.exists("{}/*STAR_SPEC*.fits")
    KF.multiple_log("Standard Star Reduction")
    KF.reduce_std_star(reduced_file_destination, calibration_data_location, star_list, 'kmos_std_star', options, reduced_dark_folder=None, reduced_flat_folder=None, kmos_static_calib_directory=kmos_static_calib_directory)






