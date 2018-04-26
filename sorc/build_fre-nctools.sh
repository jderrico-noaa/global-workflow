#!/bin/sh
set -eux

source ./machine-setup.sh > /dev/null 2>&1
system_site=$target
if [ $system_site = "wcoss_cray" ]; then
  system_site=cray
fi

cwd=`pwd`

# Check final exec folder exists
if [ ! -d "../exec" ]; then
  mkdir ../exec
fi

cd fre-nctools.fd/

home_dir=`pwd`/../..
srcDir=`pwd`

#Build in a temporary directory.
tmpDir=`pwd`/build
mkdir -p $tmpDir
cd $tmpDir

echo "////////////////////////////////////////////////////////////////////////////////"
echo "//////////////////////////////////////////////////////// Environment Settings //"
echo "////////////////////////////////////////////////////////////////////////////////"

#Original setup is for cray so for now require input only on a different platform.

set +x
module list
module use ../../../modulefiles/fv3gfs                  > /dev/null 2>&1
module load fre-nctools.${target} > /dev/null 2>&1
module list
set -x

MPICH_UNEX_BUFFER_SIZE=256m
MPICH_MAX_SHORT_MSG_SIZE=64000
MPICH_PTL_UNEX_EVENTS=160k
KMP_STACKSIZE=2g
F_UFMTENDIAN=big
if [ $system_site = theia ]; then
  HDF5_DIR=$HDF5
  NETCDF_DIR=$NETCDF
fi

alias make="make HDF5_HOME=${HDF5_DIR}  NETCDF_HOME=${NETCDF_DIR} NC_BLKSZ=64K SITE=${system_site} -f fre-nctools.mk"

echo "////////////////////////////////////////////////////////////////////////////////"
echo "//////////////////////////////////////////////////////////// Directory Layout //"
echo "////////////////////////////////////////////////////////////////////////////////"

mkdir -p share/src
cp -r $srcDir/shared share/src/.
cp -r $srcDir/tools share/src/.

echo "Done..."

for freNCToolsDir in tools/make_hgrid tools/make_solo_mosaic tools/fregrid
do
  echo "////////////////////////////////////////////////////////////////////////////////"
  echo "////////////////////////////////////////////////////////////////// $freNCToolsDir:t"
  echo "////////////////////////////////////////////////////////////////////////////////"

  cd share/src/$freNCToolsDir
  cp fre-nctools.mk_${system_site} fre-nctools.mk
  targets=` grep "TARGETS  :=" fre-nctools.mk | cut -f2 -d'=' `
  echo "Making $targets"

  make clean
  make

  for Target in $targets
  do
    if [ -f $Target ]; then
      mv $Target $home_dir/exec
    else
      echo "Error during '$Target' build"
      exit 1
    fi
  done
  make clean
  cd $tmpDir
done

echo "////////////////////////////////////////////////////////////////////////////////"
echo "///////////////////////////////////////////////////////////////// filter_topo //"
echo "////////////////////////////////////////////////////////////////////////////////"

cd ../tools/filter_topo
./make.csh_${target}
mv filter_topo $home_dir/exec/.

echo "\n////////// CLEANING UP TEMPORARY BUILD AREA //////////\n"
rm -fr $tmpDir

exit
