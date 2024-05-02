 rocotorun -w rt_hr3-c384.xml -d ~/rt_dbfiles/rt_hr3-c384.db
 rocotostat -w rt_hr3-c384.xml -d ~/rt_dbfiles/rt_hr3-c384.db -c `date --date='4 days ago' +%Y%m%d0000`: | more
 rocotoboot -w rt_hr3-c384.xml -d ~/rt_dbfiles/rt_hr3-c384.db -c 202404010000 -t gfsfcst
 rocotocheck -w rt_hr3-c384.xml -d ~/rt_dbfiles/rt_hr3-c384.db -c 202404010000 -t gfsfcst

 rocotorun -w rt_pygraf_ufs-c384.xml -d ~/rt_dbfiles/rt_pygraf_ufs-c384.db
 rocotostat -w rt_pygraf_ufs-c384.xml -d ~/rt_dbfiles/rt_pygraf_ufs-c384.db -c `date --date='4 days ago' +%Y%m%d0000`: | more
 rocotoboot -w rt_pygraf_ufs-c384.xml -d ~/rt_dbfiles/rt_pygraf_ufs-c384.db -c 202404010000 -t gfspygraf_full 
 rocotocheck -w rt_pygraf_ufs-c384.xml -d ~/rt_dbfiles/rt_pygraf_ufs-c384.db -c 202404010000 -t gfspygraf_full 
