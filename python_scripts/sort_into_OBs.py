#! /opt/local/bin/python2

from astropy.io import fits
import glob
import os



import argparse

parser=argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('-n', '--dry_run', help="Don't actually move the files- just print where they're going", action='store_true')
parser.add_argument('-q', '--quiet', help="Don't print to the terminal", action='store_true')
args=parser.parse_args()

path=args.path
dry_run_flag=args.dry_run

if dry_run_flag:
    print '\n-----------'
    print 'Dry Run'
    print '-----------\n'

files=glob.glob('{}/KMOS*.fits'.format(path))

#Header keywords and filename endings we want to add
header_file_endings={
'KMOS_spec_obs_stare':'sci',
'KMOS_spec_cal_dark':'dark',
'KMOS_spec_cal_calunitflat':'flat',
'KMOS_spec_cal_wave':'wave',
'KMOS_spec_cal_stdstar':'star',
'KMOS_spec_acq':'acq',
'KMOS_spec_acq_stdstar':'acq_star',
}



OB_start_times = set()

for file in files:

    hdr=fits.getheader(file)
    file_type=hdr['HIERARCH ESO TPL ID']
    obs_start=hdr['HIERARCH ESO OBS START'].replace(':', '-')
    t_start=hdr['HIERARCH ESO TPL START'].replace(':', '-')
    band=hdr['HIERARCH ESO INS GRAT1 ID']
    dpr_type=hdr['HIERARCH ESO DPR TYPE']

    rename_file=True
    try:
        obs_type=header_file_endings[file_type]
    except KeyError:
        rename_file=False
    
    basename=os.path.basename(file)
    filedirname=os.path.dirname(file)


    if rename_file:

        if obs_type == 'dark':
            directory_string='darks'
        elif obs_type == 'flat':
            directory_string='flats'
        elif obs_type == 'wave':
            directory_string='wave_cals'
        elif obs_type == 'star':
            directory_string='tellurics'
        elif obs_type == 'sci':
            #Make the directory string the target name
            directory_string=hdr['OBJECT'].split('.')[0]
            



        new_directory='{}/OB_{}_{}'.format(filedirname, directory_string, obs_start)
        if not dry_run_flag:        
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)


        if not args.quiet:
            print '{} --> {}/{}'.format(file, new_directory, basename)

        if not dry_run_flag:
            os.rename(file, '{}/{}'.format(new_directory, basename))