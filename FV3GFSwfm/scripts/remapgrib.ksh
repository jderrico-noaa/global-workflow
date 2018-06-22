#!/bin/ksh --login

# this file remaps 1/4 degree lat/lon grids to other grids
#    236 201 244 130 224 242

# initialize
module load wgrib2
ECHO=echo
MKDIR=mkdir
WGRIB2=wgrib2
#GRID_NAMES=201D130D244D236D224D242
echo entering remapgrib.ksh....
echo "****************************"
echo "FV3GFS_RUN  = ${FV3GFS_RUN}"
echo "PSLOT       = ${PSLOT}"
echo "CDUMP       = ${CDUMP}"
echo "yyjjjhh     = ${yyjjjhh}"
echo "yyyymmdd    = ${yyyymmdd}"
echo "hh          = ${hh}"
echo "fcst        = ${fcst}"
echo "GRID_NAMES  = ${GRID_NAMES}"
echo

#########################
# Grid Definitions
#########################
# Full domain
#---------
# 32 km
export grid_specs_221="lambert:253:50.000000 214.500000:349:32463.000000 1.000000:277:32463.000000"

#---------
# CONUS
#---------
# 13 km
export grid_specs_130="lambert:265:25.000000 233.862000:451:13545.000000 16.281000:337:13545.000000"
# 20 km
export grid_specs_252="lambert:265:25.000000 233.862000:301:20318.000000 16.281000:225:20318.000000"
# 40 km
export grid_specs_236="lambert:265:25.000000 233.862000:151:40635.000000 16.281000:113:40635.000000"

#---------
# Alaska
#---------
export grid_specs_242="nps:225:60.000000 187.000000:553:11250.000000 30.000000:425:11250.000000"

#---------
# Hawaii
#---------
export grid_specs_243="latlon 190.0:126:0.400 10.000:101:0.400"

#---------
# Puerto Rico
#---------
export grid_specs_200="lambert:253:50.000000 285.720000:108:16232.000000 16.201000:94:16232.000000"

#---------
#HRRRE
#---------
export grid_specs_999="lambert:253:50.000000 227.500000:675:13545.000000 7.500000:500:13545.000000"

#---------
# North Polar Stereographic
#---------
export grid_specs_201="nps:225:60.000000 210.000000:65:381000.000000 -20.826000:65:381000.000000"

#---------
# South Polar Stereographic
#---------
export grid_specs_224="sps:255:60.000000 120.000000:65:381000.000000 20.826000:65:381000.000000"

#---------
# North Atlantic
#---------
export grid_specs_244="latlon 261.750:275:0.25 0.250:203:0.25"
#########################

# make post directory if doesn't exist
postDir=${FV3GFS_RUN}/${PSLOT}/${CDUMP}.${yyyymmdd}/${hh}/post
echo "postDir:  $postDir"
if [ ! -d ${postDir} ]
then
  echo "creating ${postDir} "
  mkdir -p ${postDir}
fi

grids=$(echo $GRID_NAMES|sed 's/D/ /g')
src_gribfile=gfs.t${hh}z.pgrb2.0p25.f${fcst}

# loop through each grid
grids=$(echo $GRID_NAMES|sed 's/D/ /g')
for grid in $grids
do
    tgt_gribfile_dir=${postDir}/${grid}
    ${MKDIR} -p ${tgt_gribfile_dir}
    tgt_gribfile=${tgt_gribfile_dir}/${yyjjjhh}000${fcst}.g2
    ${ECHO} "Processing grids for grid ${grid}"
    eval grid_specs=\${grid_specs_${grid}}
    ${WGRIB2} ${postDir}/../${src_gribfile} -set_grib_type c3 -new_grid_winds grid \
      -new_grid_interpolation bilinear \
      -new_grid ${grid_specs} ${tgt_gribfile}
done
