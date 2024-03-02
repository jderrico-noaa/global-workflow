#! /usr/bin/env bash

source "$HOMEgfs/ush/preamble.sh"

###############################################################
## Abstract:
## Archive driver script
## RUN_ENVIR : runtime environment (emc | nco)
## HOMEgfs   : /full/path/to/workflow
## EXPDIR : /full/path/to/config/files
## CDATE  : current analysis date (YYYYMMDDHH)
## CDUMP  : cycle name (gdas / gfs)
## PDY    : current date (YYYYMMDD)
## cyc    : current cycle (HH)
###############################################################

###############################################################
# Source FV3GFS workflow modules
. $HOMEgfs/ush/load_fv3gfs_modules.sh
status=$?
[[ $status -ne 0 ]] && exit $status

###############################################################
# Source relevant configs
configs="base arch"
for config in $configs; do
    . $EXPDIR/config.${config}
    status=$?
    [[ $status -ne 0 ]] && exit $status
done

COMIN=${COMINatmos:-"$ROTDIR/$CDUMP.$PDY/$cyc/atmos"}
cd $COMIN

YYYY=`echo $PDY|cut -c1-4`
###############################################################
# Archive data to HPSS
if [ $HPSSARCH = "YES" ]; then
###############################################################

  if [ $CDUMP = "gfs" ]; then
  
      # archive INPUT directory  (initial conditions)
      htar -P -hcvf $ATARDIR/$YYYY/$CDATE/atmos/${CDATE}_ics.tar INPUT
      status=$?
      if [ $status -ne 0 ]; then
        echo "HTAR $CDATE ics failed"
        exit $status
      fi

      # archive RESTART directory 
      #   only archive tomorrow's data
      nday=$($NDATE +24 ${CDATE})
      nextday=`echo ${nday} | cut -c1-8`
      htar -P -hcvf $ATARDIR/$YYYY/$CDATE/atmos/${CDATE}_restart.tar RERUN_RESTART/${nextday}*
      status=$?
      if [ $status -ne 0 ]; then
        echo "HTAR $CDATE restart failed"
        exit $status
      fi

      # archive GRIB2 files (gfs.t00z.pgrb2.0p25.fHHH, gfs.t00z.pgrb2.0p50.fHHH)
      if [[ -f "gfs.t00z.pgrb2.0p25.f000" ]]; then
        htar -P -cvf $ATARDIR/$YYYY/$CDATE/atmos/${CDATE}_pgrb2.tar gfs.*pgrb2.0p25* gfs.*pgrb2.0p5*
        status=$?
        if [ $status -ne 0 ]; then
          echo "HTAR $CDATE pgrb2.tar failed"
          exit $status
        fi
      fi

      # archive PyGraf files (files.zip)
      if [[ -f "img/full/files.zip" ]]; then
        htar -P -cvf $ATARDIR/$YYYY/$CDATE/atmos/${CDATE}_img.tar img/*/files.zip
        status=$?
        if [ $status -ne 0 ]; then
          echo "HTAR $CDATE img.tar failed"
          exit $status
        fi
      fi

  fi

###############################################################
fi  ##end of HPSS archive
###############################################################
