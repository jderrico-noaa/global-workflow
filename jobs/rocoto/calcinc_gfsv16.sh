#! /usr/bin/env bash

source "$HOMEgfs/ush/preamble.sh"

###############################################################
## Abstract:
## Calculate increment of Met. fields for CCPP-CHEM
## RUN_ENVIR : runtime environment (emc | nco)
## HOMEgfs   : /full/path/to/workflow
## EXPDIR : /full/path/to/config/files
## CDATE  : current date (YYYYMMDDHH)
## CDUMP  : cycle name (gdas / gfs)
## PDY    : current date (YYYYMMDD)
## cyc    : current cycle (HH)
###############################################################
# Source machine runtime environment
. $BASE_ENV/${machine}.env calcinc
status=$?
[[ $status -ne 0 ]] && exit $status
###############################################################
CALCINCEXEC=${CALCINCEXEC:-$HOMEgfs/exec/calc_increment_ens_ncio.x}
NTHREADS_CALCINC=${NTHREADS_CALCINC:-1}
ncmd=${ncmd:-1}
imp_physics=${imp_physics:-99}
INCREMENTS_TO_ZERO=${INCREMENTS_TO_ZERO:-"'NONE'"}
DO_CALC_INCREMENT=${DO_CALC_INCREMENT:-"YES"}
export ERRSCRIPT=${ERRSCRIPT:-'eval [[ $err = 0 ]]'}

TMPDAY=`$NDATE -24 $PDY$cyc`
HISDAY=`echo $TMPDAY | cut -c1-8`

if [ $DO_CALC_INCREMENT = "YES" ]; then

  export DATA="$RUNDIR/$CDATE/$CDUMP"

  [[ ! -d $DATA ]] && mkdir -p $DATA
  cd $DATA
#JKH  ln -sf $RUNDIR1/$CDATE/$CDUMP/regrid regrid #lzhang
  mkdir -p calcinc
  cd calcinc

  # link atmf024.nc file
  $NLN $OUTDIR/$CDUMP.$HISDAY/00/atmos/$CDUMP.t00z.atmf024.nc

  export OMP_NUM_THREADS=$NTHREADS_CALCINC
  $NCP $CALCINCEXEC .
  $NLN $CDUMP.t00z.atmf024.nc atmges_mem001  
  $NLN ../regrid/atmanl.$PDY$cyc.nc atmanl_mem001  
  $NLN atminc.nc atminc_mem001
  rm -f calc_increment.nml
  cat > calc_increment.nml << EOF
&setup
  datapath = './'
  analysis_filename = 'atmanl'
  firstguess_filename = 'atmges'
  increment_filename = 'atminc'
  debug = .false.
  nens = $ncmd
  imp_physics = $imp_physics
/
&zeroinc
  incvars_to_zero = $INCREMENTS_TO_ZERO
/
EOF
  cat calc_increment.nml

#JKH  APRUN=$(eval echo $APRUN_CALCINC)
#JKH  $APRUN $(basename $CALCINCEXEC)
  $(basename $CALCINCEXEC)
  rc=$?

  export ERR=$rc
  export err=$ERR
  $ERRSCRIPT || exit 3
fi
   
###############################################################

###############################################################
# Exit cleanly
