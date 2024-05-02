 rocotorun -w rt_hr3-chem.xml -d ~/rt_dbfiles/rt_hr3-chem.db
 rocotostat -w rt_hr3-chem.xml -d ~/rt_dbfiles/rt_hr3-chem.db -c `date --date='4 days ago' +%Y%m%d0000`: | more
 rocotoboot -w rt_hr3-chem.xml -d ~/rt_dbfiles/rt_hr3-chem.db -c 202404010000 -t gfsfcst
 rocotocheck -w rt_hr3-chem.xml -d ~/rt_dbfiles/rt_hr3-chem.db -c 202404010000 -t gfsfcst

 rocotorun -w rt_pygraf_ufs-chem.xml -d ~/rt_dbfiles/rt_pygraf_ufs-chem.db
 rocotostat -w rt_pygraf_ufs-chem.xml -d ~/rt_dbfiles/rt_pygraf_ufs-chem.db -c `date --date='4 days ago' +%Y%m%d0000`: | more
 rocotoboot -w rt_pygraf_ufs-chem.xml -d ~/rt_dbfiles/rt_pygraf_ufs-chem.db -c 202404010000 -t remapgrib_000
 rocotocheck -w rt_pygraf_ufs-chem.xml -d ~/rt_dbfiles/rt_pygraf_ufs-chem.db -c 202404010000 -t remapgrib_000
