#! /opt/local/bin/python2

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

    parser = argparse.ArgumentParser(description="KMOS Science Reduction Script")
    parser.add_argument('-d', '--reduced_file_destination', type=str, help='Destination for reduced science cubes')
    parser.add_argument('-c', '--calibration_data_location', type=str, help='Location of (dynamic) calibration files: XCAL, YCAL, LCAL, MASTER_FLAT')
    parser.add_argument('-t', '--telluric_location', type=str, help='Location of telluric file: TELLURIC_IZIZIZ.fits')
    parser.add_argument('-i', '--input_files', nargs='*', type=str, help='Location of science files. Can include wildcards')
    parser.add_argument('--static_calib_location', type=str, help='Optional: Location of static calibration files (WAVE_BAND). Otherwise assume /Data/KCLASH/Data/Static_Cals/cal/')
    parser.add_argument('--log_file_name', type=str, help='Optional: name of the log file to save things to')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--no_subtract', action='store_true', help='Optional: add the --no_subtract flag to esorex')
    group.add_argument('--sky_tweak', action='store_true', help='Optional: add the --sky_tweak flag to esorex')
    
    args=parser.parse_args()

    reduced_file_destination=os.path.abspath(args.reduced_file_destination)
    file_locations=[os.path.abspath(f) for f in args.input_files]
    calibration_data_location=os.path.abspath(args.calibration_data_location)
    telluric_location=os.path.abspath(args.telluric_location)
    static_calib_location=args.static_calib_location

    if static_calib_location is not None:
        kmos_static_calib_directory=os.path.abspath(static_calib_location)
    else:
        kmos_static_calib_directory='/Data/KCLASH/Data/Static_Cals/cal'

    
    if args.no_subtract is not None:
        esorex_flags=['--no_subtract']
    elif args.sky_tweak is not None:
        esorex_flags=['--sky_tweak']
    else:
        esorex_flags=None

    #Optional arguments. Code left over from original script and isn't used any more
    #usage = "usage: %prog [options] data_dir"
    # parser = OptionParser(usage=usage, description="KMOS Calibration Data Generation Script")
    # parser.add_option("-p", "--parallel", action="store_true", dest="parallel", default=False, help="Parallel execution of esorex")
    # parser.add_option("-d", "--description", action="store_true", dest="description", default=False, help="Detailed Description")
    # parser.add_option("-b", "--band", default="All", help="Band that needs to be reduced (H, K, HK, YJ, IZ) [default: %default]")
    # (options, args) = parser.parse_args()
    #Hack...
    from argparse import Namespace
    options = Namespace(parallel=False, band='IZ', description=None)


    logging.info("Parallel Mode: {0}".format(options.parallel))
    logging.info("Description required: {0}".format(options.description))
    logging.info("Desired Band: {0}".format(options.band))




    # Loop on all files in the input directory
    sci_list = []
    for loc in file_locations:
        for file in glob.glob("{}/KMOS*sci*.fits".format(loc)):
            # Read the Primary header
            fname=os.path.abspath(file)
            hdu = fits.getheader(fname, 0)
            tpl_id = hdu['HIERARCH ESO TPL ID']
            # Only keep the proper TPL.ID
            if tpl_id in ["KMOS_spec_obs_stare"]:
                sci_list.append({   'name': fname, 
                            'tpl_id': tpl_id, 
                            'tpl_start': hdu['HIERARCH ESO TPL START'],
                            'tpl_nexp': hdu['HIERARCH ESO TPL NEXP'],
                            'tpl_expno': hdu['HIERARCH ESO TPL EXPNO'],
                            'dpr_type': hdu['HIERARCH ESO DPR TYPE'],
                            'obs_start': hdu['HIERARCH ESO OBS START'],
                            'band': hdu['HIERARCH ESO INS GRAT1 ID']})

    #if not os.path.exists("{}/*STAR_SPEC*.fits")
    KF.multiple_log("Science Reduction")
    KF.reduce_science(reduced_file_destination, calibration_data_location, telluric_location, sci_list, 'kmos_sci_red', options, esorex_flags=esorex_flags, log_file_name=args.log_file_name, reduced_dark_folder=None, reduced_flat_folder=None, kmos_static_calib_directory=kmos_static_calib_directory)






