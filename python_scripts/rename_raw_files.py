#! /opt/local/bin/python2

from astropy.io import fits
import glob
import os
import argparse

parser=argparse.ArgumentParser('Rename KMOS observation files according to whether they are science, darks, flats, etc. Will create and sort into folders called "Sci", "Cals" and "Acqs"')
parser.add_argument('data_dir', help='Main Data directory. Sci, Cals and Acqs folders will be made here')
parser.add_argument('path', help='Raw data dir, containing files called KMOS*.fits')
parser.add_argument('-n', '--dry_run', help="Don't actually move the files- just print where they're going", action='store_true')
parser.add_argument('-q', '--quiet', help="Don't print to the terminal", action='store_true')
args=parser.parse_args()

data_dir=args.data_dir
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

# 'tpl_start': hdu['HIERARCH ESO TPL START'],
# 'tpl_nexp': hdu['HIERARCH ESO TPL NEXP'],
# 'tpl_expno': hdu['HIERARCH ESO TPL EXPNO'],
# 'dpr_type': hdu['HIERARCH ESO DPR TYPE'],
# 'obs_start': hdu['HIERARCH ESO OBS START'],
# 'band': hdu['HIERARCH ESO INS GRAT1 ID']}

if not dry_run_flag:
    if not os.path.exists('./{}/Sci/'.format(data_dir)):
        os.makedirs('./{}/Sci/'.format(data_dir))
    if not os.path.exists('./{}/Cals/'.format(data_dir)):
        os.makedirs('./{}/Cals/'.format(data_dir))  
    if not os.path.exists('./{}/Acqs/'.format(data_dir)):
        os.makedirs('./{}/Acqs/'.format(data_dir))   


OB_start_times = set()
unmoved_files={}


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
        


    if rename_file:
        basename=os.path.basename(file).rsplit('.', 1)[0]

        if obs_type == 'dark':
            new_name='./{}/Cals/{}_{}_{}__{}.fits'.format(data_dir, basename, obs_type, obs_start, t_start)

        elif obs_type == 'flat':
            if dpr_type =='FLAT,LAMP':
                obs_type='flat_on'
                
            elif dpr_type =='FLAT,OFF':
                obs_type='flat_off'
            else:
                raise NameError('Type of flat not understood!')


            new_name='./{}/Cals/{}_{}_{}__{}.fits'.format(data_dir, basename, obs_type, band, obs_start, t_start)


        elif obs_type == 'wave' or obs_type == 'star':

            new_name='./{}/Cals/{}_{}_{}__{}__{}.fits'.format(data_dir,basename, obs_type, band, obs_start, t_start)

        elif obs_type == 'acq' or obs_type =='acq_star':
            new_name='./{}/Acqs/{}_{}_{}__{}__{}.fits'.format(data_dir,basename, obs_type, band, obs_start, t_start)

        elif obs_type == 'sci':
            new_name='./{}/Sci/{}_{}_{}__{}__{}.fits'.format(data_dir,basename, obs_type, band, obs_start, t_start)

        else:
            raise NameError('Obs type {} not understood!'.format(obs_types))
        

        OB_start_times.add(obs_start)

        if not args.quiet:
            print '{} --> {}'.format(file, new_name)

        #If we're not doing a dry run
        if not dry_run_flag:
            try:
                os.rename(file, new_name)
            except:
                raise NameError("Couldn't move {} to {}!".format(file, new_name))
    else:
        unmoved_files[file]=file_type




if unmoved_files:
    print "\n-------------------------"
    print "Some files weren't dealt with:"
    print "\tType:\tFilename"
    for i in unmoved_files:
        print "\t{}: {}".format(unmoved_files[i], i)
    print "-------------------------\n"




