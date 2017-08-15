set -e

BASE_DIR="/Data/KCLASH/python_scripts"
DEST="/Data/KCLASH/Data/Sci/1931_BL/NoSubtract"
RAW="/Data/KCLASH/Data/Sci/Raw_files"
CALS="/Data/KCLASH/Data/Cals/Reduced_Calibrations/CALIBS_2017_07_16"
TELL="/Data/KCLASH/Data/Cals/Tellurics"


#echo Running "$BASE_DIR/reduce_science.py" --reduced_file_destination "$DEST/Vanilla" --input_files "$RAW/OB_1931_MASTER_BL_2017-07-16T0*" --calibration_data_location "$CALS/CALIBS_2017_07_16/" --telluric_location "$TELL/telluric_2017-07-16T04-21-51/"
#python2 "$BASE_DIR/reduce_science.py" -d "$DEST" -i "$RAW/OB_1931_MASTER_BL_2017-07-16T02-05-43" -c "$CALS" -t "$TELL/telluric_2017-07-16T10-19-39" --no_subtract
#python2 "$BASE_DIR/reduce_science.py" -d "$DEST" -i "$RAW/OB_1931_MASTER_BL_2017-07-16T03-39-03" -c "$CALS" -t "$TELL/telluric_2017-07-16T04-21-51/" --no_subtract
python2 "$BASE_DIR/reduce_science.py" -d "$DEST" -i "$RAW/OB_1931_MASTER_BL_2017-07-16T04-46-05" -c "$CALS" -t "$TELL/telluric_2017-07-16T04-21-51/" --no_subtract