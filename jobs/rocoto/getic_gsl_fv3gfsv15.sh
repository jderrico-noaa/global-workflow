#!/bin/bash -x

## this script makes links to FV3GFS (GFSv15.1) nemsio files under /public and copies over GFS analysis file for verification
##   /scratch4/BMC/rtfim/rtfuns/FV3GFS/FV3ICS/YYYYMMDDHH/gfs
##     gfs.tHHz.sfcanl.nemsio -> /public/data/grids/gfs/nemsio/YYDDDHH00.gfs.tHHz.sfcanl.nemsio
##     gfs.tHHz.atmanl.nemsio -> /public/data/grids/gfs/nemsio/YYDDDHH00.gfs.tHHz.atmanl.nemsio
##

echo
echo "CDATE = $CDATE"
echo "CDUMP = $CDUMP"
echo "COMPONENT = $COMPONENT"
echo "ICSDIR = $ICSDIR"
echo "PUBDIR = $PUBDIR"
echo "GFSDIR = $GFSDIR"
echo "RETRODIR = $RETRODIR"
echo "ROTDIR = $ROTDIR"
echo "PSLOT = $PSLOT"
echo

## initialize
yyyymmdd=`echo $CDATE | cut -c1-8`
hh=`echo $CDATE | cut -c9-10`
yyddd=`date +%y%j -u -d $yyyymmdd`
fv3ic_dir=${ROTDIR}/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}

## EMC archive on disk
##    /scratch1/NCEPDEV/rstprod/com/gfs/prod
##         gfs.t00z.atmanl.nemsio
##         gfs.t00z.sfcanl.nemsio
##
EMCDIR=/scratch1/NCEPDEV/rstprod/com/gfs/prod

## create links in FV3ICS directory
mkdir -p $fv3ic_dir
cd $fv3ic_dir
echo "making link to nemsio files under $fv3ic_dir"

pubsfc_file=${yyddd}${hh}00.${CDUMP}.t${hh}z.sfcanl.nemsio 
sfc_file=`echo $pubsfc_file | cut -d. -f2-`
pubatm_file=${yyddd}${hh}00.${CDUMP}.t${hh}z.atmanl.nemsio 
atm_file=`echo $pubatm_file | cut -d. -f2-`

echo "pubsfc_file:  $pubsfc_file"
echo "pubatm_file:  $pubatm_file"

if [[ -f $PUBDIR/${pubsfc_file} ]]; then
  echo "linking $PUBDIR...."
  ln -fs $PUBDIR/${pubsfc_file} $sfc_file 
  ln -fs $PUBDIR/${pubatm_file} $atm_file 
elif  [[ -f $RETRODIR/${pubsfc_file} ]]; then
  echo "linking $RETRODIR...."
  ln -fs $RETRODIR/${pubsfc_file} $sfc_file
  ln -fs $RETRODIR/${pubatm_file} $atm_file 
elif  [[ -f $EMCDIR/${pubsfc_file} ]]; then
  echo "linking $EMCDIR...."
  ln -fs $EMCDIR/${sfc_file} $sfc_file
  ln -fs $EMCDIR/${atm_file} $atm_file 
else
  echo "missing input files!"
  exit 1
fi
