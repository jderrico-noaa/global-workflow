#! /usr/bin/env bash

source "$HOMEgfs/ush/preamble.sh"

## this script makes links to FV3GFS netcdf files under /public and copies over GFS analysis file for verification
##   /home/rtfim/UFS_CAMSUITE/FV3GFSrun/FV3ICS/YYYYMMDDHH/gfs
##     gfs.tHHz.sfcanl.nc -> /public/data/grids/gfs/netcdf/YYDDDHH00.gfs.tHHz.sfcanl.nc
##     gfs.tHHz.atmanl.nc -> /public/data/grids/gfs/netcdf/YYDDDHH00.gfs.tHHz.atmanl.nc

echo
echo "CDATE = $CDATE"
echo "CDUMP = $CDUMP"
echo "ICSDIR = $ICSDIR"
echo "PUBDIR = $PUBDIR"
echo "GFSDIR = $GFSDIR"
echo "RETRODIR = $RETRODIR"
echo "ROTDIR = $ROTDIR"
echo

## initialize
export COMPONENT="atmos"
yyyymmdd=`echo $CDATE | cut -c1-8`
hh=`echo $CDATE | cut -c9-10`
yyddd=`date +%y%j -u -d $yyyymmdd`
fv3ic_dir=$ICSDIR/${CDATE}/${CDUMP}

## create links in FV3ICS directory
mkdir -p $fv3ic_dir
cd $fv3ic_dir
echo "making link to netcdf files under $fv3ic_dir"

pubsfc_file=${yyddd}${hh}00.${CDUMP}.t${hh}z.sfcanl.nc
sfc_file=`echo $pubsfc_file | cut -d. -f2-`
pubatm_file=${yyddd}${hh}00.${CDUMP}.t${hh}z.atmanl.nc
atm_file=`echo $pubatm_file | cut -d. -f2-`

# create link for GDAS atmanl
#    use GFS atmanl instead of GDAS atmanl file
gdas_atm_file=gdas.t${hh}z.atmanl.nc

###
### look on local /public directory
###
if [[ -f $PUBDIR/${pubsfc_file} ]]; then
  echo "linking $PUBDIR...."
  echo "pubsfc_file:  $pubsfc_file"
  echo "pubatm_file:  $pubatm_file"
  echo "link $pubatm_file to $gdas_atm_file"
  ln -fs $PUBDIR/${pubsfc_file} $sfc_file 
  ln -fs $PUBDIR/${pubatm_file} $atm_file 
  ln -fs $PUBDIR/${pubatm_file} $gdas_atm_file 
elif  [[ -f $RETRODIR/${pubsfc_file} ]]; then
  echo "linking $RETRODIR...."
  echo "pubsfc_file:  $pubsfc_file"
  echo "pubatm_file:  $pubatm_file"
  echo "link $pubatm_file to $gdas_atm_file"
  ln -fs $RETRODIR/${pubsfc_file} $sfc_file
  ln -fs $RETRODIR/${pubatm_file} $atm_file 
  ln -fs $RETRODIR/${pubatm_file} $gdas_atm_file 
elif  [[ -f $GFSDIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${sfc_file} ]]; then
  echo "linking $GFSDIR...."
  echo "sfc_file:  $sfc_file"
  echo "atm_file:  $atm_file"
  echo "link $atm_file to $gdas_atm_file"
  ln -s $GFSDIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${sfc_file}
  ln -s $GFSDIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${atm_file}
  ln -s $GFSDIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${atm_file} $gdas_atm_file
elif  [[ -f $RETRODIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${sfc_file} ]]; then
  echo "linking $RETRODIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}..."
  echo "sfc_file:  $sfc_file"
  echo "atm_file:  $atm_file"
  echo "link $atm_file to $gdas_atm_file"
  ln -s $RETRODIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${sfc_file}
  ln -s $RETRODIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${atm_file}
  ln -s $RETRODIR/${CDUMP}.${yyyymmdd}/${hh}/${COMPONENT}/${atm_file} $gdas_atm_file
else
  echo "missing input files!"
  exit 5
fi
