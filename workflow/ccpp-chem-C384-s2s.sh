USER=Kate.Zhang


BASEDIR=/scratch1/BMC/gsd-fv3-dev/lzhang/p8-ccpp-chem/global-workflow
STMP=/scratch1/NCEPDEV/stmp2/$USER
CONFIGDIR=$BASEDIR/parm/config
IDATE=2016080100
EDATE=2016080100
APP=S2SW
PSLOT=UFS_C384_CCPP
RES=384
GFS_CYC=1
COMROT=/scratch1/BMC/gsd-fv3-dev/NCEPDEV/global/$USER/fv3gfs/comrot
EXPDIR=/scratch2/BMC/gsd-fv3-dev/NCEPDEV/global/$USER/fv3gfs/expdir
ICSDIR=$COMROT/$PSLOT


./setup_expt.py forecast-only --app $APP --pslot $PSLOT --configdir $CONFIGDIR --idate $IDATE --edate $EDATE --res $RES --gfs_cyc $GFS_CYC --comrot $COMROT --expdir $EXPDIR --icsdir $ICSDIR


./setup_xml.py $EXPDIR/$PSLOT

