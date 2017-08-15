import sys
import os
import time
from optparse import OptionParser
import argparse
from astropy.io import fits
import glob
import logging
import subprocess
from subprocess import Popen, list2cmdline
import shutil

import readline

from KMOS_tools import kmos_functions as KF

#Sam's KMOS Calib
#Take a list of KMOS calibrations and reduce them.
#Key difference to kmos_calib.py- can give location of dark files if they've already been reduced.
#Lots of this is taken from the kmos_calib.py file!

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")


#Path to the KMOS static calibaration files (arc lists, reference lines, etc)






if __name__=='__main__':

    parser = argparse.ArgumentParser(description="KMOS Calibration Data Generation Script")
    parser.add_argument('calibration_file_destination', type=str, help='Location for reduced calibration files')
    parser.add_argument('dark_location', type=str, help='Location of dark files')
    parser.add_argument('flat_location', type=str, help='Location of flat files')
    parser.add_argument('wave_location', type=str, help='Location of wave files')
    args=parser.parse_args()
    calibration_file_destination=args.calibration_file_destination
    dark_location=args.dark_location
    flat_location=args.flat_location
    wave_location=args.wave_location

    usage = "usage: %prog [options] data_dir"
    parser = OptionParser(usage=usage, description="KMOS Calibration Data Generation Script")
    parser.add_option("-p", "--parallel", action="store_true", dest="parallel", default=False, help="Parallel execution of esorex")
    parser.add_option("-d", "--description", action="store_true", dest="description", default=False, help="Detailed Description")
    parser.add_option("-b", "--band", default="All", help="Band that needs to be reduced (H, K, HK, YJ, IZ) [default: %default]")
    (options, args) = parser.parse_args()


    logging.info("Parallel Mode: {0}".format(options.parallel))
    logging.info("Description required: {0}".format(options.description))
    logging.info("Wished Band: {0}".format(options.band))



    #TODO write the code to include this as an option
    kmos_static_calib_directory='/Data/KCLASH/Data/Static_Cals/cal'


    # Loop on all files in the input directory
    dark_list = []
    for file in glob.glob(dark_location+"/KMOS*dark*.fits"):
        # Read the Primary header
        fname=os.path.abspath(file)
        hdu = fits.getheader(fname, 0)
        tpl_id = hdu['HIERARCH ESO TPL ID']
        # Only keep the proper TPL.ID
        if tpl_id in ["KMOS_spec_cal_dark"]:
            dark_list.append({   'name': fname, 
                        'tpl_id': tpl_id, 
                        'tpl_start': hdu['HIERARCH ESO TPL START'],
                        'tpl_nexp': hdu['HIERARCH ESO TPL NEXP'],
                        'tpl_expno': hdu['HIERARCH ESO TPL EXPNO'],
                        'dpr_type': hdu['HIERARCH ESO DPR TYPE'],
                        'obs_start': hdu['HIERARCH ESO OBS START'],
                        'band': hdu['HIERARCH ESO INS GRAT1 ID']})

    flat_list=[]
    for file in glob.glob(flat_location+"/KMOS*flat*.fits"):

        fname=os.path.abspath(file)
        # Read the Primary header
        hdu = fits.getheader(fname, 0)
        tpl_id = hdu['HIERARCH ESO TPL ID']
        # Only keep the proper TPL.ID
        if tpl_id in ["KMOS_spec_cal_calunitflat"]:
            flat_list.append({   'name': fname, 
                                    'tpl_id': tpl_id, 
                                    'tpl_start': hdu['HIERARCH ESO TPL START'],
                                    'tpl_nexp': hdu['HIERARCH ESO TPL NEXP'],
                                    'tpl_expno': hdu['HIERARCH ESO TPL EXPNO'],
                                    'dpr_type': hdu['HIERARCH ESO DPR TYPE'],
                                    'obs_start': hdu['HIERARCH ESO OBS START'],
                                    'band': hdu['HIERARCH ESO INS GRAT1 ID']})

    wave_list=[]
    for file in glob.glob(wave_location+"/KMOS*wave*.fits"):

        fname=os.path.abspath(file)
        # Read the Primary header
        hdu = fits.getheader(fname, 0)
        tpl_id = hdu['HIERARCH ESO TPL ID']
        # Only keep the proper TPL.ID
        if tpl_id in ["KMOS_spec_cal_wave"]:
            wave_list.append({   'name': fname, 
                                    'tpl_id': tpl_id, 
                                    'tpl_start': hdu['HIERARCH ESO TPL START'],
                                    'tpl_nexp': hdu['HIERARCH ESO TPL NEXP'],
                                    'tpl_expno': hdu['HIERARCH ESO TPL EXPNO'],
                                    'dpr_type': hdu['HIERARCH ESO DPR TYPE'],
                                    'obs_start': hdu['HIERARCH ESO OBS START'],
                                    'band': hdu['HIERARCH ESO INS GRAT1 ID']})


    calibration_file_destination=os.path.abspath(calibration_file_destination)

    if not os.path.exists('{}'.format(calibration_file_destination)):
        os.makedirs('{}'.format(calibration_file_destination))

    KF.multiple_log('\nOutput folder is {}'.format(calibration_file_destination))

    if not os.path.exists('{}/MASTER_DARK.fits'.format(calibration_file_destination)) or not os.path.exists('{}/BADPIXEL_DARK.fits'.format(calibration_file_destination)):
        
        KF.multiple_log("Dark Data Reduction")
        KF.reduce_darks(calibration_file_destination, dark_list, options)
    else:
        KF.multiple_log('\tDark files already reduced')





    if not os.path.exists('{}/BADPIXEL_FLAT_IZIZIZ.fits'.format(calibration_file_destination)) or not os.path.exists('{}/FLAT_EDGE_IZIZIZ.fits'.format(calibration_file_destination)) or not os.path.exists('{}/MASTER_FLAT_IZIZIZ.fits'.format(calibration_file_destination))    or not os.path.exists('{}/YCAL_IZIZIZ.fits'.format(calibration_file_destination)) or not os.path.exists('{}/XCAL_IZIZIZ.fits'.format(calibration_file_destination)):

        KF.multiple_log("Flat File Reduction")
        KF.reduce_calibs(calibration_file_destination, flat_list, 'kmos_flat', options, reduced_dark_folder=None, reduced_flat_folder=None)
    else:
        KF.multiple_log('\tFlat files already reduced')





    if not os.path.exists('{}/DET_IMG_WAVE_IZIZIZ.fits'.format(calibration_file_destination)) or not os.path.exists('{}/LCAL_IZIZIZ.fits'.format(calibration_file_destination)):
        
        KF.multiple_log("Wave Cal Reduction")
        KF.reduce_calibs(calibration_file_destination, wave_list, 'kmos_wave_cal', options, reduced_dark_folder=None, reduced_flat_folder=None)

    else:
        KF.multiple_log('\tWave Cal files already reduced')


    if not os.path.exists('{}/ILLUM_CORR_IZIZIZ.fits'.format(calibration_file_destination)) or not os.path.exists('{}/SKYFLAT_EDGE_IZIZIZ.fits'.format(calibration_file_destination)):
        
        KF.multiple_log("Illumination Reduction")
        KF.reduce_calibs(calibration_file_destination, flat_list, 'kmos_illumination', options, reduced_dark_folder=None, reduced_flat_folder=None)

    else:
        KF.multiple_log('\tIllumination files already made')

