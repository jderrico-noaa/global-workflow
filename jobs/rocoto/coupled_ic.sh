#! /usr/bin/env bash

source "$HOMEgfs/ush/preamble.sh"

###############################################################
## Abstract:
## Copy initial conditions from BASE_CPLIC to ROTDIR for coupled forecast-only runs
## HOMEgfs   : /full/path/to/workflow
## EXPDIR : /full/path/to/config/files
## ICSDIR : /full/path/to/ics/files
## CDUMP  : cycle name (gdas / gfs)
## PDY    : current date (YYYYMMDD)
## cyc    : current cycle (HH)
###############################################################

###############################################################
# Source FV3GFS workflow modules
. ${HOMEgfs}/ush/load_fv3gfs_modules.sh
status=$?
[[ ${status} -ne 0 ]] && exit ${status}
err=0

###############################################################
# Source relevant configs
configs="base coupled_ic "
for config in ${configs}; do
    . ${EXPDIR}/config.${config}
    status=$?
    [[ ${status} -ne 0 ]] && exit ${status}
done

###############################################################
# Source machine runtime environment
. ${BASE_ENV}/${machine}.env config.coupled_ic
status=$?
[[ ${status} -ne 0 ]] && exit ${status}

###############################################################

error_message(){
    echo "FATAL ERROR: Unable to copy ${1} to ${2} (Error code ${3})"
}

###############################################################
# Start staging

# Stage the FV3 initial conditions to ROTDIR (cold start)
ATMdir="${ROTDIR}/${CDUMP}.${PDY}/${cyc}/atmos/INPUT"
#JKHATMdir="${COMOUTatmos}/INPUT"
[[ ! -d "${ATMdir}" ]] && mkdir -p "${ATMdir}"
for file in gfs_ctrl.nc chgres_done; do
  source="${ICSDIR}/${PDY}${cyc}/${CDUMP}/${CASE}/INPUT/${file}"
  target="${ATMdir}/${file}"
  ${NCP} "${source}" "${target}"
  rc=$?
  [[ ${rc} -ne 0 ]] && error_message "${source}" "${target}" "${rc}"
  err=$((err + rc))
done
for ftype in gfs_data sfc_data; do
  for ((tt = 1; tt <= 6; tt++)); do
    source="${ICSDIR}/${PDY}${cyc}/${CDUMP}/${CASE}/INPUT/${ftype}.tile${tt}.nc"
    target="${ATMdir}/${ftype}.tile${tt}.nc"
    ${NCP} "${source}" "${target}"
    rc=$?
    [[ ${rc} -ne 0 ]] && error_message "${source}" "${target}" "${rc}"
    err=$((err + rc))
  done
done

###############################################################
# Check for errors and exit if any of the above failed
if  [[ "${err}" -ne 0 ]] ; then
  echo "FATAL ERROR: Unable to copy ICs from ${BASE_CPLIC} to ${ROTDIR}; ABORT!"
  exit "${err}"
fi

##############################################################
# Exit cleanly
#exit 0
