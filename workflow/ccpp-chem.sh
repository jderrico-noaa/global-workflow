USER=Judy.K.Henderson
GITDIR=/scratch2/BMC/gsd-fv3-dev/jhender/test/test_p8-chem/            ## where your git checkout is located
COMROT=$GITDIR/FV3GFSrun                                         ## default COMROT directory
EXPDIR=$GITDIR/FV3GFSwfm                                         ## default EXPDIR directory
ICSDIR=$COMROT/FV3ICS

PSLOT=p8-chem
IDATE=2024010100
EDATE=2024010100
RESDET=384

### gfs_cyc 1  00Z only;  gfs_cyc 2  00Z and 12Z

./setup_expt.py forecast-only --pslot $PSLOT  --gfs_cyc 1 \
       --idate $IDATE --edate $EDATE --resdet $RESDET \
       --icsdir $ICSDIR --comrot $COMROT --expdir $EXPDIR
