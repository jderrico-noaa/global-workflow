 rocotorun -w rt_c384ics.xml -d ~/rt_dbfiles/rt_c384ics.db
 rocotostat -w rt_c384ics.xml -d ~/rt_dbfiles/rt_c384ics.db -c `date --date='4 days ago' +%Y%m%d0000`: | m
 rocotoboot -w rt_c384ics.xml -d ~/rt_dbfiles/rt_c384ics.db -c 202404260000 -t gfsfcst
 rocotocheck -w rt_c384ics.xml -d ~/rt_dbfiles/rt_c384ics.db -c 202404260000 -t gfsfcst
