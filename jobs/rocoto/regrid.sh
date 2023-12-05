#! /usr/bin/env bash

source "$HOMEgfs/ush/preamble.sh"

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
. $HOMEgfs/ush/load_fv3gfs_modules.sh
status=$?
[[ $status -ne 0 ]] && exit $status

###############################################################
# Source relevant configs
configs="base regrid"
for config in $configs; do
    . $EXPDIR/config.${config}
    status=$?
    [[ $status -ne 0 ]] && exit $status
done
###############################################################
if [ $CDATE -ge "2021032212" ]; then
    $HOMEgfs/jobs/rocoto/regrid_gfsv16.sh
else
    $HOMEgfs/jobs/rocoto/regrid_gfsv15.sh
fi
rc=$?
if [ $rc -ne 0 ]; then
    echo "error regrid $rc "
    exit $rc
fi 

###############################################################

###############################################################
# Exit cleanly

