#! /usr/bin/env bash

source "$HOMEgfs/ush/preamble.sh"

###############################################################
## Abstract:
## Regrid the high resolution Gaussian Met. analysis data (nemsio) into Gaussian model resolution (nemsio)
## RUN_ENVIR : runtime environment (emc | nco)
## HOMEgfs   : /full/path/to/workflow
## EXPDIR : /full/path/to/config/files
## ROTDIR : /full/path/to/output/files
## CDATE  : current date (YYYYMMDDHH)
## CDUMP  : cycle name (gdas / gfs)
## PDY    : current date (YYYYMMDD)
## cyc    : current cycle (HH)
###############################################################
# initialize variables
SYEAR=$(echo $CDATE | cut -c1-4)
SMONTH=$(echo $CDATE | cut -c5-6)
SDAY=$(echo $CDATE | cut -c7-8)
TMPDAY=$($NDATE -24 $PDY$cyc)
HISDAY=$(echo $TMPDAY | cut -c1-8)

# Temporary rundirectory
if [ ! -s $DATA ]; then mkdir -p $DATA; fi
cd $DATA || exit 8

res=$(echo $CASE |cut -c2-5)
LONB=$((4*res))
LATB=$((2*res))

mkdir -p regrid
cd regrid

# link atmf000.nc file from previous day
$NLN ${ROTDIR}/${CDUMP}.${HISDAY}/${cyc}/atmos/gfs.t${cyc}z.atmf000.nc
status=$?
if [ $status -ne 0 ]; then
     echo "error linking of gfs.t00z.atmf000.nc failed  $status "
     return $status
fi

$NCP $EXECgfs/enkf_chgres_recenter_nc.x . 
status=$?
if [ $status -ne 0 ]; then
     echo "error enkf_chgres_recenter_nc failed  $status "
     return $status
fi

cat > ./fort.43 << !
 &chgres_setup
  i_output=$LONB
  j_output=$LATB
  input_file="$ICSDIR/$SYEAR$SMONTH$SDAY${cyc}/$CDUMP/gdas.t${cyc}z.atmanl.nc"
  output_file="atmanl.$SYEAR$SMONTH$SDAY${cyc}.nc"
  terrain_file="./$CDUMP.t00z.atmf000.nc"
  cld_amt=.F.
  ref_file="./$CDUMP.t00z.atmf000.nc"
 /
!

mpirun -n 1 ./enkf_chgres_recenter_nc.x "./fort.43"
status=$?
if [ $status -ne 0 ]; then
     echo "error enkf_chgres_recenter_nc failed  $status "
     return $status
fi

###############################################################
