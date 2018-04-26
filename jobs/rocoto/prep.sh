#!/bin/ksh -x

###############################################################
# Source FV3GFS workflow modules
. $HOMEgfs/ush/load_fv3gfs_modules.sh
status=$?
[[ $status -ne 0 ]] && exit $status

###############################################################
# Source relevant configs
configs="base prep prepbufr"
for config in $configs; do
    . $EXPDIR/config.${config}
    status=$?
    [[ $status -ne 0 ]] && exit $status
done

export CHGRP_CMD=${CHGRP_CMD:-"chgrp ${group_name:-rstprod}"}
###############################################################
# Source machine runtime environment
. $BASE_ENV/${machine}.env prep
status=$?
[[ $status -ne 0 ]] && exit $status

###############################################################
# Set script and dependency variables
export OPREFIX="${CDUMP}.t${cyc}z."
export COMOUT="$ROTDIR/$CDUMP.$PDY/$cyc"
[[ ! -d $COMOUT ]] && mkdir -p $COMOUT


###############################################################
# For running real-time parallels on WCOSS_C, execute tropcy_qc and 
# copy files from operational syndata directory to a local directory.
# Otherwise, copy existing tcvital data from globaldump.

if [ $PROCESS_TROPCY = "YES" ]; then

    export ARCHSYNDNCO=$COMROOTp1/arch/prod/syndat
    if [ $RUN_ENVIR != "nco" ]; then
        export ARCHSYND=${ROTDIR}/syndat
        if [ ! -d ${ARCHSYND} ]; then mkdir -p $ARCHSYND; fi
        if [ ! -s $ARCHSYND/syndat_akavit ]; then 
            for file in syndat_akavit syndat_dateck syndat_stmcat.scr syndat_stmcat syndat_sthisto syndat_sthista ; do
                cp $ARCHSYNDNCO/$file $ARCHSYND/. 
            done
        fi
    fi

    $HOMEgfs/jobs/JGLOBAL_TROPCY_QC_RELOC
    status=$?
    [[ $status -ne 0 ]] && exit $status

else
    cp $DMPDIR/$CDATE/$CDUMP/${CDUMP}.t${cyc}z.syndata.tcvitals.tm00 $COMOUT/.
fi


###############################################################
# Generate prepbufr files from dumps or copy from OPS
if [ $DO_MAKEPREPBUFR = "YES" ]; then
    export USHSYND=""   # set blank so that prepobs_makeprepbufr defaults USHSYND to HOMEobsproc_prep}/ush
    $HOMEgfs/jobs/JGLOBAL_PREP
    [[ $status -ne 0 ]] && exit $status
else
    $NCP $DMPDIR/$CDATE/$CDUMP/${OPREFIX}prepbufr               $COMOUT/${OPREFIX}prepbufr
    $NCP $DMPDIR/$CDATE/$CDUMP/${OPREFIX}prepbufr.acft_profiles $COMOUT/${OPREFIX}prepbufr.acft_profiles
    [[ $DONST = "YES" ]] && $NCP $DMPDIR/$CDATE/$CDUMP/${OPREFIX}nsstbufr $COMOUT/${OPREFIX}nsstbufr
fi

################################################################################
# Exit out cleanly
exit 0
