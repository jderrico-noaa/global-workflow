USER=role.rtfim


BASEDIR=/scratch1/BMC/gsd-fv3/rtruns/UFS-Chem
STMP=/scratch1/NCEPDEV/stmp2/$USER/RUNDIRS
IDATE=2024040200
EDATE=2024040200
APP=ATM
PSLOT=rt_hr3-c384
RES=384
GFS_CYC=1
START=cold
COMROT=$BASEDIR/FV3GFSrun
EXPDIR=$BASEDIR/FV3GFSwfm
ICSDIR=$COMROT/$PSLOT


./setup_expt.py gfs forecast-only --idate $IDATE --edate $EDATE --app $APP --gfs_cyc $GFS_CYC --resdetatmos $RES --pslot $PSLOT --comroot $COMROT --expdir $EXPDIR 


./setup_xml.py $EXPDIR/$PSLOT

