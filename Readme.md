# Prepare data for lab examination

Creates per term folders, copies student uploads into them and generates a CSV for grades excel.

Expected input file structure:
```
run.py  # The script.
students.csv  # List of student information, downloaded from course website as CSV grades list.
LV1/
- uploads/  # Unzipped downloaded student uploads from Ferko.
-- JMBAG1
-- ...
- terms_from_analizer.txt  # Standardized file of terms and list of JMBAGs.
```

Expected output file structure:
```
table.csv  # CSV list of terms and student info to copy into Sheets/Excel.
result.log  # Log of script evaluation for later reference (when students did not upload or uploaded as not .zip).
LV1/
- 11-01_09-00/  # Each term has its folder.
-- JMBAG1/
--- JMBAG1.zip
--- JMBAG1/
---- implementation.cpp
---- ...
-- JMBAG2/
--- ...
- 11-01_09-30/
-- ...
```
