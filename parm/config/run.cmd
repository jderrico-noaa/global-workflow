rocotorun -d /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.db -w /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.xml

rocotoboot -d /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.db -w /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.xml -c 201607150000 -t gfsfcst

rocotostat -d /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.db -w /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.xml

rocotocheck -d /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.db -w /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.xml -c 201607150000 -t gfsfcst 

rocotorewind -d /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.db -w /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.xml -c 201607150000 -t gfsfcst

rocotocomplete -d /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.db -w /scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/Kate.Zhang/fv3gfs/expdir/UFS_C96_CCPP/UFS_C96_CCPP.xml -c 201310010000 -t gfs.forecast.highres 
