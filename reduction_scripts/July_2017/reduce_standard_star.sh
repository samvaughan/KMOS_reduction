#Reduce all standard stars

BASE_DIR='/Data/KCLASH/python_scripts'
TELLS='Data/Cals/Tellurics'
RAW='Data/Cals/Sorted_Calib_Files'
CALS='Data/Cals/Reduced_Calibrations'


python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T04-37-29" "$RAW/OB_tellurics_2017-07-15T04-37-29/" "$CALS/CALIBS_2017_07_15/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T10-14-00" "$RAW/OB_tellurics_2017-07-15T10-14-00" "$CALS/CALIBS_2017_07_15/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T23-11-29" "$RAW/OB_tellurics_2017-07-15T23-11-29" "$CALS/CALIBS_2017_07_15/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T08-32-42" "$RAW/OB_tellurics_2017-07-15T08-32-42" "$CALS/CALIBS_2017_07_15/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T22-33-04" "$RAW/OB_tellurics_2017-07-15T22-33-04" "$CALS/CALIBS_2017_07_15/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T10-00-17" "$RAW/OB_tellurics_2017-07-15T10-00-17" "$CALS/CALIBS_2017_07_15/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-15T22-56-20" "$RAW/OB_tellurics_2017-07-15T22-56-20" "$CALS/CALIBS_2017_07_15/"

python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-16T10-19-39" "$RAW/OB_tellurics_2017-07-16T10-19-39" "$CALS/CALIBS_2017_07_16/"
python2 "$BASE_DIR/standard_star.py" "$TELLS/telluric_2017-07-16T04-21-51" "$RAW/OB_tellurics_2017-07-16T04-21-51" "$CALS/CALIBS_2017_07_16/"