USER=role.rtfim
GITDIR=/scratch1/BMC/gsd-fv3/rtruns/P8-Chem/               ## where your git checkout is located
COMROT=$GITDIR/FV3GFSrun                                         ## default COMROT directory
EXPDIR=$GITDIR/FV3GFSwfm                                         ## default EXPDIR directory
ICSDIR=/scratch1/BMC/gsd-fv3/rtruns/FV3ICS_L127

PSLOT=rt_p8-c384
IDATE=2024020100
EDATE=2034010100
RESDET=384

### gfs_cyc 1  00Z only;  gfs_cyc 2  00Z and 12Z

./setup_expt.py forecast-only --pslot $PSLOT  --gfs_cyc 1 \
       --idate $IDATE --edate $EDATE --resdet $RESDET \
       --icsdir $ICSDIR --comrot $COMROT --expdir $EXPDIR
