#!/bin/sh 

## this script makes a link to $ICSDIR/YYYYMMDDHH/gfs/<CASE>/INPUT
##   /scratch4/BMC/rtfim/rtruns/FV3ICS/YYYYMMDDHH/gfs/C384|C768/INPUT
##

echo
echo "CDATE = $CDATE"
echo "CASE = $CASE"
echo "CDUMP = $CDUMP"
echo "ICSDIR = $ICSDIR"
echo "ROTDIR = $ROTDIR"
echo

## initialize
yyyymmdd=`echo $CDATE | cut -c1-8`
hh=`echo $CDATE | cut -c9-10`
fv3ic_dir=$ICSDIR/${CDATE}/${CDUMP}/${CASE}
outdir=${ROTDIR}/${CDUMP}.${yyyymmdd}/${hh}

## create link to FV3ICS directory
if [[ ! -d $outdir ]]; then
  mkdir -p $outdir
  status=$?
  if [ $status -ne 0 ]; then
    echo "can't make link to $outdir...."
    return $status
  fi
fi
cd $outdir
echo "making link to FV3ICS directory:  $fv3ic_dir/INPUT"
ln -fs $fv3ic_dir/INPUT
status=$?
exit $status
