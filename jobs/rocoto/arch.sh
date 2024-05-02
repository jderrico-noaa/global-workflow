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

COMIN=${COMINatmos:-"$ROTDIR/$CDUMP.$PDY/$cyc/model_data/atmos"}
COMINP=${COMINP:-"$ROTDIR/$CDUMP.$PDY/$cyc/products/atmos/grib2"}
COMINF=${COMINF:-"$ROTDIR/$CDUMP.$PDY/$cyc/products/atmos"}
COMINC=${COMINC:-"$ROTDIR/$CDUMP.$PDY/$cyc/"}

YYYY=`echo $PDY|cut -c1-4`
###############################################################
# Archive data to HPSS
if [ $HPSSARCH = "YES" ]; then
###############################################################

  if [ $CDUMP = "gfs" ]; then
      cd $COMIN  
      # archive INPUT directory  (initial conditions)
      htar -P -hcvf $ATARDIR/$YYYY/$CDATE/${CDATE}_ics.tar input
      status=$?
      if [ $status -ne 0 ]; then
        echo "HTAR $CDATE ics failed"
        exit $status
      fi

      # archive RESTART directory 
      #   only archive tomorrow's data
      nday=$($NDATE +24 ${CDATE})
      nextday=`echo ${nday} | cut -c1-8`
      htar -P -hcvf $ATARDIR/$YYYY/$CDATE/${CDATE}_restart.tar restart/${nextday}*
      status=$?
      if [ $status -ne 0 ]; then
        echo "HTAR $CDATE restart failed"
        exit $status
      fi

            # archive history directory
      #   only archive tomorrow's data
      nday=$($NDATE +24 ${CDATE})
      nextday=`echo ${nday} | cut -c1-8`
      htar -P -hcvf $ATARDIR/$YYYY/$CDATE/historync.tar history
      status=$?
      if [ $status -ne 0 ]; then
        echo "HTAR $CDATE restart failed"
        exit $status
      fi

      cd $COMINP
      # archive GRIB2 files (gfs.t00z.pgrb2.0p25.fHHH, gfs.t00z.pgrb2.0p50.fHHH)
      if [[ -f "0p25/gfs.t00z.pgrb2.0p25.f000" ]]; then
        htar -P -cvf $ATARDIR/$YYYY/$CDATE/${CDATE}_pgrb2.tar 0p25 0p50 1p00
        status=$?
        if [ $status -ne 0 ]; then
          echo "HTAR $CDATE pgrb2.tar failed"
          exit $status
        fi
      fi

     cd $COMINF
      # archive PyGraf files (files.zip)
      if [[ -f "img/full/files.zip" ]]; then
        htar -P -cvf $ATARDIR/$YYYY/$CDATE/${CDATE}_img.tar img/*/files.zip
        status=$?
        if [ $status -ne 0 ]; then
          echo "HTAR $CDATE img.tar failed"
          exit $status
        fi
      fi

      cd $COMINC
        htar -P -cvf $ATARDIR/$YYYY/$CDATE/${CDATE}_conf.tar conf
        status=$?
        if [ $status -ne 0 ]; then
          echo "HTAR $CDATE img.tar failed"
          exit $status
        fi

  fi

###############################################################
fi  ##end of HPSS archive
###############################################################
