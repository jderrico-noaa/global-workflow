#!/bin/ksh -x

###############################################################
## Abstract:
## Regrid the high resolution Gaussian Met. analysis data (nemsio) into Gaussian model resolution (nemsio)
## RUN_ENVIR : runtime environment (emc | nco)
## HOMEgfs   : /full/path/to/workflow
## EXPDIR : /full/path/to/config/files
## CDATE  : current date (YYYYMMDDHH)
## CDUMP  : cycle name (gdas / gfs)
## PDY    : current date (YYYYMMDD)
## cyc    : current cycle (HH)
###############################################################
# Source FV3GFS workflow modules
#JKH. $HOMEgfs/ush/load_fv3gfs_modules.sh
#JKHstatus=$?
#JKH[[ $status -ne 0 ]] && exit $status

###############################################################
# Source relevant configs
#JKHconfigs="base regrid"
#JKHfor config in $configs; do
#JKH    . $EXPDIR/config.${config}
#JKH    status=$?
#JKH    [[ $status -ne 0 ]] && exit $status
#JKHdone
###############################################################
TMPDAY=`$NDATE -24 $PDY$cyc`
HISDAY=`echo $TMPDAY | cut -c1-8`

# Temporary rundirectory
if [ ! -s $DATA ]; then mkdir -p $DATA; fi
cd $DATA || exit 8

res=$(echo $CASE |cut -c2-5)
LONB=$((4*res))
LATB=$((2*res))

mkdir -p regrid
cd regrid
#$NCP /scratch3/BMC/fim/lzhang/EMC_FV3/fv3gfs_merge_v1/global_shared.v15.0.0/exec/chgres_recenter.exe . 
$NCP $EXECgfs/chgres_recenter.exe . 
status=$?
if [ $status -ne 0 ]; then
     echo "error chgres_recenter failed  $status "
     return $status
fi

cat > ./fort.43 << !
 &nam_setup
  i_output=$LONB
  j_output=$LATB
  input_file="$ICSDIR/$SYEAR$SMONTH$SDAY$SHOUR/$CDUMP/gdas.t${cyc}z.atmanl.nemsio"
  output_file="atmanl.$SYEAR$SMONTH$SDAY$SHOUR"
  terrain_file="$OUTDIR/$CDUMP.$HISDAY/00/$CDUMP.t00z.atmf000.nemsio"
  vcoord_file="$FIXgfs/fix_am/global_hyblev.l65.txt"
 /
!

./chgres_recenter.exe 
status=$?
if [ $status -ne 0 ]; then
     echo "error chgres_recenter failed  $status "
     return $status
fi

###############################################################
