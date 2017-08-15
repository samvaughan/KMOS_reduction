#!/usr/bin/env bash


calib_file_folder='/Data/KCLASH/Data/Cals/Sorted_Calib_Files'
reduced_calib_folder='/Data/KCLASH/Data/Cals/Reduced_Calibrations'

python2 /Data/KCLASH/python_scripts/reduce_calibs.py "$reduced_calib_folder"/CALIBS_2017_07_15 "$calib_file_folder"/OB_darks_2017-07-15T10-46-44 "$calib_file_folder"/OB_flats_2017-07-15T11-02-53 "$calib_file_folder"/OB_wave_cals_2017-07-15T11-02-53
python2 /Data/KCLASH/python_scripts/reduce_calibs.py "$reduced_calib_folder"/CALIBS_2017_07_16 "$calib_file_folder"/OB_darks_2017-07-16T10-48-27 "$calib_file_folder"/OB_flats_2017-07-16T11-04-36 "$calib_file_folder"/OB_wave_cals_2017-07-16T11-04-36
python2 /Data/KCLASH/python_scripts/reduce_calibs.py "$reduced_calib_folder"/CALIBS_2017_06_29 "$calib_file_folder"/OB_darks_2017-06-29T10-28-22 "$calib_file_folder"/OB_flats_2017-06-29T10-44-35 "$calib_file_folder"/OB_wave_cals_2017-06-29T10-44-35