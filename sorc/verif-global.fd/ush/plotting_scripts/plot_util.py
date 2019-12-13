import numpy as np
import datetime as datetime

"""!@namespace plot_util
 @brief Provides  Utility functions for METplus plotting use case.
"""

def get_date_arrays(plot_time, start_date_YYYYmmdd, end_date_YYYYmmdd,
                    valid_time_info, init_time_info, lead):
    """! Create arrays of dates for requested plotting
 
            Args:
                plot_time - string of describing the treatment
                            of dates, either valid or init
                start_date_YYYYmmdd - string of start date formatted
                                      in %Y%m%d
                end_date_YYYYmmdd - string of the end date formatted 
                                    in %Y%m%d
                valid_time_info - list of valid hour information
                init_time_info - list of initialization hour information
                lead - string of the forecast lead hour

            Returns:
                plot_time_dates - array of ordinal dates based on user
                                  provided information
                expected_stat_file_dates - array of dates that are expected to
                                           be found in the MET .stat files
                                           based on user provided information,
                                           formatted as "%Y%m%d"+"_"+"%H%M%S"
    """
    if len(lead) == 2 or len(lead) == 4:
        lead = lead.ljust(6, '0')
    elif len(lead) == 3 or len(lead) == 5:
        lead = lead.ljust(7, '0')
    plot_time_dates = []
    expected_stat_file_dates = []
    if plot_time == "valid":
        if len(init_time_info) > 1:
             valid_start_hour = valid_time_info[0]
             valid_end_hour = valid_time_info[-1]
        else:
             lead_hour_seconds = int(int(lead[:-4])%24) * 3600
             if lead[-4:]:
                 lead_min_seconds = int(lead[-4:-2]) * 60
             else:
                  lead_min_seconds = 0
             init_hour_seconds = int(int(init_time_info[0][:-4])%24) * 3600
             if init_time_info[0][-4:]:
                 init_min_seconds = int(init_time_info[0][-4:-2]) * 60
             else:
                 init_min_seconds = 0
             lead_init_offset = datetime.timedelta(seconds=lead_hour_seconds
                                                   + lead_min_seconds 
                                                   + init_hour_seconds
                                                   + init_min_seconds)
             totsec = lead_init_offset.total_seconds()
             valid_hour = int(totsec//3600)
             valid_min = int((totsec%3600) // 60)
             valid_sec = int((totsec%3600)%60)
             valid_start_hour = str(valid_hour).zfill(2)+ \
                                str(valid_min).zfill(2)+str(valid_sec).zfill(2)
             valid_end_hour = valid_start_hour
        if len(valid_time_info) > 1 and len(init_time_info) > 1:
            delta_t = datetime.timedelta(seconds=(datetime.datetime.strptime(
                          valid_time_info[1], "%H%M%S")
                      - datetime.datetime.strptime(
                          valid_time_info[0], "%H%M%S")).total_seconds())
        else:
            delta_t = datetime.timedelta(seconds=86400)
        plot_start_date_YYYYmmddHHMMSS = \
            datetime.datetime.strptime(start_date_YYYYmmdd+ \
                                       valid_start_hour, "%Y%m%d%H%M%S")
        plot_end_date_YYYYmmddHHMMSS = \
            datetime.datetime.strptime(end_date_YYYYmmdd+ \
                                       valid_end_hour, "%Y%m%d%H%M%S") \
            + delta_t
        dates = np.arange(plot_start_date_YYYYmmddHHMMSS, 
                          plot_end_date_YYYYmmddHHMMSS, 
                          delta_t).astype(datetime.datetime)
        for date in dates:
            dt = date.time()
            seconds = (dt.hour * 60 + dt.minute) * 60 + dt.second
            plot_time_dates.append(date.toordinal() + seconds/86400.)
            expected_stat_file_dates.append(date.strftime("%Y%m%d"+"_"+"%H%M%S"))
    elif plot_time == "init":
        if len(valid_time_info) > 1:
           init_start_hour = init_time_info[0]
           init_end_hour = init_time_info[-1]
        else:
           lead_hour_seconds = int(int(lead[:-4])%24) * 3600
           if lead[-4:-2]:
               lead_min_seconds = int(lead[-4:-2]) * 60
           else:
               lead_min_seconds = 0
           valid_hour_seconds = int(int(valid_time_info[0][:-4])%24) * 3600
           if valid_time_info[0][-4:-2]:
               valid_min_seconds = int(valid_time_info[0][-4:-2]) * 60
           else:
               valid_min_seconds = 0
           lead_init_offset = datetime.timedelta(seconds=lead_hour_seconds
                                                 + lead_min_seconds
                                                 - valid_hour_seconds
                                                 - valid_min_seconds)
           totsec = lead_init_offset.total_seconds()
           init_hour = int(totsec//3600)
           init_min = int((totsec%3600) // 60)
           init_sec = int((totsec%3600)%60)
           init_start_hour = str(init_hour).zfill(2)+ \
                              str(init_min).zfill(2)+str(init_sec).zfill(2)
           init_end_hour = init_start_hour
        if len(valid_time_info) > 1 and len(init_time_info) > 1:
            delta_t = datetime.timedelta(seconds=(datetime.datetime.strptime(
                          init_time_info[1], "%H%M%S") \
                      - datetime.datetime.strptime(
                          init_time_info[0], "%H%M%S")).total_seconds())
        else:
            delta_t = datetime.timedelta(seconds=86400)
        plot_start_date_YYYYmmddHHMMSS = \
            datetime.datetime.strptime(start_date_YYYYmmdd+ \
                                       init_start_hour, "%Y%m%d%H%M%S")
        plot_end_date_YYYYmmddHHMMSS = \
            datetime.datetime.strptime(end_date_YYYYmmdd+ \
                                       init_end_hour, "%Y%m%d%H%M%S") \
            + delta_t
        dates = np.arange(plot_start_date_YYYYmmddHHMMSS,
                          plot_end_date_YYYYmmddHHMMSS,
                          delta_t).astype(datetime.datetime)
        for date in dates:
            dt = date.time()
            seconds = (dt.hour * 60 + dt.minute) * 60 + dt.second
            plot_time_dates.append(date.toordinal() + seconds/86400.)
            lead_time_HHMMSS = lead
            delta_lead = datetime.timedelta(hours=int(lead_time_HHMMSS[:-4]),
                                            minutes=int(lead_time_HHMMSS[-4:-2]),
                                            seconds=int(lead_time_HHMMSS[-2:]))
            expected_stat_file_dates.append( \
                (datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S") \
                + delta_lead).strftime("%Y%m%d"+"_"+"%H%M%S"))
    return plot_time_dates, expected_stat_file_dates

def get_stat_file_base_columns(met_version):
    """! Standard MET .stat file columns based on
         version number
 
             Args:
                 met_version - string of MET version number
                               being used to run stat_analysis

             Returns:
                 stat_file_base_columns - list of the standard
                                          columns shared among the
                                          different line types
    """
    met_version = float(met_version)
    if met_version < 8.1:
        stat_file_base_columns = [ 
            "VERSION", "MODEL", "DESC", "FCST_LEAD", "FCST_VALID_BEG",
            "FCST_VALID_END", "OBS_LEAD", "OBS_VALID_BEG", "OBS_VALID_END",
            "FCST_VAR", "FCST_LEV", "OBS_VAR", "OBS_LEV", "OBTYPE", "VX_MASK",
            "INTERP_MTHD", "INTERP_PNTS", "FCST_THRESH", "OBS_THRESH", 
            "COV_THRESH", "ALPHA", "LINE_TYPE"
            ]
    else:
        stat_file_base_columns = [
            "VERSION", "MODEL", "DESC", "FCST_LEAD", "FCST_VALID_BEG",
            "FCST_VALID_END", "OBS_LEAD", "OBS_VALID_BEG", "OBS_VALID_END",
            "FCST_VAR", "FCST_UNITS", "FCST_LEV", "OBS_VAR", "OBS_UNITS",
            "OBS_LEV", "OBTYPE", "VX_MASK", "INTERP_MTHD", "INTERP_PNTS",
            "FCST_THRESH", "OBS_THRESH", "COV_THRESH", "ALPHA", "LINE_TYPE"
]
    return stat_file_base_columns

def get_stat_file_line_type_columns(logger, met_version, line_type):
    """! Line type MET .stat file columns based on
         version number
 
             Args:
                 met_version - string of MET version number
                               being used to run stat_analysis
                 line_type - string of the line type of the MET
                             .stat file being read

             Returns:
                 stat_file_line_type_columns - list of the line type columns
    """
    met_version = float(met_version)
    if line_type == "SL1L2":
        if met_version >= 6.0:
            stat_file_line_type_columns = [ 
                "TOTAL", "FBAR", "OBAR", "FOBAR", "FFBAR", "OOBAR", "MAE"
                 ]
    elif line_type == "SAL1L2":
        if met_version >= 6.0:
            stat_file_line_type_columns = [
                "TOTAL", "FABAR", "OABAR", "FOABAR", "FFABAR", "OOABAR", "MAE"
                 ]
    elif line_type == "VL1L2":
        if met_version == 6.0 or met_version == 6.1:
            stat_file_line_type_columns = [
                "TOTAL", "UFBAR", "VFBAR", "UOBAR", "VOBAR", "UVFOBAR", 
                "UVFFBAR", "UVOOBAR"
                 ]
        elif met_version >= 7.0:
            stat_file_line_type_columns = [
                "TOTAL", "UFBAR", "VFBAR", "UOBAR", "VOBAR", "UVFOBAR", 
                "UVFFBAR", "UVOOBAR", "F_SPEED_BAR", "O_SPEED_BAR"
                ]
    elif line_type == "VAL1L2":
        if met_version >= 6.0:
            stat_file_line_type_columns = [
                "TOTAL", "UFABAR", "VFABAR", "UOABAR", "VOABAR", "UVFOABAR",
                "UVFFABAR", "UVOOABAR"
                ]
    elif line_type == "VCNT":
        if met_version >= 7.0:
            stat_file_line_type_columns = [ 
                "TOTAL", "FBAR", "FBAR_NCL", "FBAR_NCU", "OBAR", "OBAR_NCL",
                "OBAR_NCU", "FS_RMS", "FS_RMS_NCL", "FS_RMS_NCU", "OS_RMS",
                "OS_RMS_NCL", "OS_RMS_NCU", "MSVE", "MSVE_NCL", "MSVE_NCU",
                "RMSVE", "RMSVE_NCL", "RMSVE_NCU", "FSTDEV", "FSTDEV_NCL",
                "FSTDEV_NCU", "OSTDEV", "OSTDEV_NCL", "OSTDEV_NCU", "FDIR",
                "FDIR_NCL", "FDIR_NCU", "ODIR", "ODIR_NCL", "ODIR_NCU",
                "FBAR_SPEED", "FBAR_SPEED_NCL", "FBAR_SPEED_NCU", "OBAR_SPEED",
                "OBAR_SPEED_NCL", "OBAR_SPEED_NCU", "VDIFF_SPEED",
                "VDIFF_SPEED_NCL", "VDIFF_SPEED_NCU", "VDIFF_DIR", 
                "VDIFF_DIR_NCL", "VDIFF_DIR_NCU", "SPEED_ERR", "SPEED_ERR_NCL",
                "SPEED_ERR_NCU", "SPEED_ABSERR", "SPEED_ABSERR_NCL", 
                "SPEED_ABSERR_NCU", "DIR_ERR", "DIR_ERR_NCL", "DIR_ERR_NCU", 
                "DIR_ABSERR", "DIR_ABSERR_NCL", "DIR_ABSERR_NCU"
                ]
        else:
            logger.error("VCNT is not a valid LINE_TYPE in METV"+met_version)
            exit(1)
    return stat_file_line_type_columns

def get_clevels(data):
    """! Get contour levels for plotting
  
              Args:
                  data - array of data to be contoured
 
              Returns:
                  clevles - array of contoure levels
    """
    if np.abs(np.nanmin(data)) > np.nanmax(data):
       cmax = np.abs(np.nanmin(data))
       cmin = np.nanmin(data)
    else:
       cmax = np.nanmax(data)
       cmin = -1 * np.nanmax(data)
    if cmax > 1:
       cmin = round(cmin-1,0)
       cmax = round(cmax+1,0)
    else:
       cmin = round(cmin-0.1,1)
       cmax = round(cmax+0.1,1)
    clevels = np.linspace(cmin, cmax, 11, endpoint=True)
    return clevels

def calculate_ci(logger, ci_method, modelB_values, modelA_values, total_days):
    """! Calculate confidence intervals between two sets of data
 
             Args:
                 ci_method - string of the method to use to 
                             calculate the confidence intervals
                 modelB_values - array of values
                 modelA_values - array of values
                 total_days - float of total number of days being considered,
                              sample size

             Returns:
                 intvl - float of the confidence interval
    """
    modelB_modelA_diff = modelB_values - modelA_values
    ndays = total_days - np.ma.count_masked(modelB_modelA_diff)
    modelB_modelA_diff_mean = modelB_modelA_diff.mean()
    modelB_modelA_std = np.sqrt(((modelB_modelA_diff \
                                  - modelB_modelA_diff_mean)**2).mean())
    if ci_method == "EMC":
        if ndays >= 80:
            intvl = 1.960*modelB_modelA_std/np.sqrt(ndays-1)
        elif ndays >= 40 and ndays < 80:
            intvl = 2.000*modelB_modelA_std/np.sqrt(ndays-1)
        elif ndays >= 20 and ndays < 40:
            intvl = 2.042*modelB_modelA_std/np.sqrt(ndays-1)
        elif ndays < 20:
            intvl = 2.228*modelB_modelA_std/np.sqrt(ndays-1)
    else:
        logger.error("Invalid entry for CI_METHOD, use EMC")
        exit(1)
    return intvl

def get_stat_plot_name(logger, stat):
    """! Get the formalized name of the statistic being plotted
 
             Args:
                 stat - string of the simple statistic name
                        being plotted

             Returns:
                 stat_plot_name - string of the formal statistic
                                  name being plotted
    """
    if stat == "bias":
        stat_plot_name = "Bias"
    elif stat == "rmse":
        stat_plot_name = "Root Mean Square Error"
    elif stat == "msess":
        stat_plot_name = "Murphy's Mean Square Error Skill Score"
    elif stat == "rsd":
        stat_plot_name = "Ratio of Standard Deviation"
    elif stat == "rmse_md":
        stat_plot_name = "Root Mean Square Error from Mean Error"
    elif stat == "rmse_pv":
        stat_plot_name = "Root Mean Square Error from Pattern Variation"
    elif stat == "pcor":
        stat_plot_name = "Pattern Correlation"
    elif stat == "acc":
        stat_plot_name = "Anomaly Correlation Coefficient"
    elif stat == "fbar":
        stat_plot_name = "Forecast Averages"
    elif stat == "fbar_obar":
        stat_plot_name = "Average"
    elif stat_ == "speed_err":
        stat_plot_name = "Difference in Average FCST and "+ \
                         "OBS Wind Vector Speeds"
    elif stat_ == "dir_err":
        stat_plot_name = "Difference in Average FCST and "+ \
                         "OBS Wind Vector Direction"
    elif stat_ == "rmsve":
        stat_plot_name = "Root Mean Square Difference Vector Error"
    elif stat_ == "vdiff_speed":
        stat_plot_name = "Difference Vector Speed"
    elif stat_ == "vdiff_dir":
        stat_plot_name = "Difference Vector Direction"
    elif stat_ == "fbar_obar_speed":
        stat_plot_name = "Average Wind Vector Speed"
    elif stat_ == "fbar_obar_dir":
        stat_plot_name = "Average Wind Vector Direction"
    elif stat_ == "fbar_speed":
        stat_plot_name = "Average Forecast Wind Vector Speed"
    elif stat_ == "fbar_dir":
        stat_plot_name = "Average Forecast Wind Vector Direction"
    else:
        logger.error(stat+" is not a valid option")
        exit(1)
    return stat_plot_name

def calculate_stat(logger, model_data, stat):
    """! Calculate the statistic from the data from the
         read in MET .stat file(s)
 
             Args:
                 model_data - Dataframe containing the model(s)
                              information from the MET .stat files
                 stat - string of the simple statistic name
                        being plotted

             Returns:
                 stat_values - Dataframe of the statistic values
                 stat_values_array - array of the statistic values
                 stat_plot_name - string of the formal statistic
                                  name being plotted
    """
    model_data_columns = model_data.columns.values.tolist()
    if model_data_columns == [ "TOTAL" ]:
        logger.warning("Empty model_data dataframe")
        stat_values = model_data.loc[:]["TOTAL"]
    else:
        if all(elem in model_data_columns for elem in ["FBAR", "OBAR", "MAE"]):
            line_type = "SL1L2"
            fbar = model_data.loc[:]["FBAR"]
            obar = model_data.loc[:]["OBAR"]
            fobar = model_data.loc[:]["FOBAR"]
            ffbar = model_data.loc[:]["FFBAR"]
            oobar = model_data.loc[:]["OOBAR"]
        elif all(elem in model_data_columns for elem in ["FABAR", "OABAR", "MAE"]):
            line_type = "SAL1L2"
            fabar = model_data.loc[:]["FABAR"]
            oabar = model_data.loc[:]["OABAR"]
            foabar = model_data.loc[:]["FOABAR"]
            ffabar = model_data.loc[:]["FFABAR"]
            ooabar = model_data.loc[:]["OOABAR"]
        elif all(elem in model_data_columns for elem in ["UFBAR", "VFBAR"]):
            line_type = "VL1L2"
            ufbar = model_data.loc[:]["UFBAR"]
            vfbar = model_data.loc[:]["VFBAR"]
            uobar = model_data.loc[:]["UOBAR"]
            vobar = model_data.loc[:]["VOBAR"]
            uvfobar = model_data.loc[:]["UVFOBAR"]
            uvffbar = model_data.loc[:]["UVFFBAR"]
            uvoobar = model_data.loc[:]["UVOOBAR"]
        elif all(elem in model_data_columns for elem in ["UFABAR", "VFABAR"]):
            line_type = "VAL1L2"
            ufabar = model_data.loc[:]["UFABAR"]
            vfabar = model_data.loc[:]["VFABAR"]
            uoabar = model_data.loc[:]["UOABAR"]
            voabar = model_data.loc[:]["VOABAR"]
            uvfoabar = model_data.loc[:]["UVFOABAR"]
            uvffabar = model_data.loc[:]["UVFFABAR"]
            uvooabar = model_data.loc[:]["UVOOABAR"]
        elif all(elem in model_data_columns for elem in ["VDIFF_SPEED", "VDIFF_DIR"]):
            line_type = "VCNT"
            fbar = model_data.loc[:]["FBAR"]
            obar = model_data.loc[:]["OBAR"]
            fs_rms = model_data.loc[:]["FS_RMS"]
            os_rms = model_data.loc[:]["OS_RMS"]
            msve = model_data.loc[:]["MSVE"]
            rmsve = model_data.loc[:]["RMSVE"]
            fstdev = model_data.loc[:]["FSTDEV"]
            ostdev = model_data.loc[:]["OSTDEV"]
            fdir = model_data.loc[:]["FDIR"]
            odir = model_data.loc[:]["ODIR"]
            fbar_speed = model_data.loc[:]["FBAR_SPEED"]
            obar_speed = model_data.loc[:]["OBAR_SPEED"]
            vdiff_speed = model_data.loc[:]["VDIFF_SPEED"]
            vdiff_dir =  model_data.loc[:]["VDIFF_DIR"]
            speed_err = model_data.loc[:]["SPEED_ERR"]
            dir_err = model_data.loc[:]["DIR_ERR"]
        else:
            logger.error("Could not recognize line type from columns")
            exit(1)
    if stat == "bias":
        stat_plot_name = "Bias"
        if line_type == "SL1L2":
            stat_values = fbar - obar
        elif line_type == "VL1L2":
            stat_values = np.sqrt(uvffbar) - np.sqrt(uvoobar)
        elif line_type == "VCNT":
            stat_values = fbar - obar
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "rmse":
        stat_plot_name = "Root Mean Square Error"
        if line_type == "SL1L2":
            stat_values = np.sqrt(ffbar + oobar - 2*fobar)
        elif line_type == "VL1L2":
            stat_values = np.sqrt(uvffbar + uvoobar - 2*uvfobar)
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "msess":
        stat_plot_name = "Murphy's Mean Square Error Skill Score"
        if line_type == "SL1L2":
            mse = ffbar + oobar - 2*fobar
            var_o = oobar - obar*obar
            stat_values = 1 - mse/var_o
        elif line_type == "VL1L2":
            mse = uvffbar + uvoobar - 2*uvfobar
            var_o = uvoobar - uobar*uobar - vobar*vobar 
            stat_values = 1 - mse/var_o
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "rsd":
        stat_plot_name = "Ratio of Standard Deviation"
        if line_type == "SL1L2":
            var_f = ffbar - fbar*fbar
            var_o = oobar - obar*obar
            stat_values = np.sqrt(var_f)/np.sqrt(var_o)
        elif line_type == "VL1L2":
            var_f = uvffbar - ufbar*ufbar - vfbar*vfbar
            var_o = uvoobar - uobar*uobar - vobar*vobar
            stat_values = np.sqrt(var_f)/np.sqrt(var_o)
        elif line_type == "VCNT":
            stat_values = fstdev/ostdev
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "rmse_md":
        stat_plot_name = "Root Mean Square Error from Mean Error"
        if line_type == "SL1L2":
            stat_values = np.sqrt((fbar-obar)**2)
        elif line_type == "VL1L2":
            stat_values = np.sqrt((ufbar - uobar)**2 + (vfbar - vobar)**2)
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "rmse_pv":
        stat_plot_name = "Root Mean Square Error from Pattern Variation"
        if line_type == "SL1L2":
            var_f = ffbar - fbar**2
            var_o = oobar - obar**2
            R = (fobar - (fbar*obar))/(np.sqrt(var_f*var_o))
            stat_values = np.sqrt(var_f + var_o - 2*np.sqrt(var_f*var_o)*R)
        elif line_type == "VL1L2":
            var_f = uvffbar - ufbar*ufbar - vfbar*vfbar
            var_o = uvoobar - uobar*uobar - vobar*vobar
            R = (uvfobar - ufbar*uobar - vfbar*vobar)/(np.sqrt(var_f*var_o))
            stat_values = np.sqrt(var_f + var_o - 2*np.sqrt(var_f*var_o)*R)
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "pcor":
        stat_plot_name = "Pattern Correlation"
        if line_type == "SL1L2":
            var_f = ffbar - fbar*fbar
            var_o = oobar - obar*obar
            stat_values = (fobar - fbar*obar)/(np.sqrt(var_f*var_o))
        elif line_type == "VL1L2":
            var_f = uvffbar - ufbar*ufbar - vfbar*vfbar
            var_o = uvoobar - uobar*uobar - vobar*vobar
            stat_values = (uvfobar - ufbar*uobar - vfbar*vobar)/(np.sqrt(
                              var_f*var_o))
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "acc":
        stat_plot_name = "Anomaly Correlation Coefficient"
        if line_type == "SAL1L2":
            stat_values = \
                (foabar - fabar*oabar)/(np.sqrt(
                (ffabar - fabar*fabar)*(ooabar - oabar*oabar)))
        elif line_type == "VAL1L2":
            stat_values = (uvfoabar)/(np.sqrt(uvffabar*uvooabar))
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "fbar":
        stat_plot_name = "Forecast Averages"
        if line_type == "SL1L2":
            stat_values = fbar
        elif line_type == "VL1L2":
            stat_values = np.sqrt(uvffbar)
        elif line_type == "VCNT":
            stat_values = fbar
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat == "fbar_obar":
        stat_plot_name = "Average"
        if line_type == "SL1L2":
            stat_values = model_data.loc[:][["FBAR", "OBAR"]]
            stat_values_fbar = model_data.loc[:]["FBAR"]
            stat_values_obar = model_data.loc[:]["OBAR"]
        elif line_type == "VL1L2":
            stat_values = model_data.loc[:][["UVFFBAR", "UVOOBAR"]]
            stat_values_fbar = np.sqrt(model_data.loc[:]["UVFFBAR"])
            stat_values_obar = np.sqrt(model_data.loc[:]["UVOOBAR"])
        elif line_type == "VCNT":
            stat_values = model_data.loc[:][["FBAR", "OBAR"]]
            stat_values_fbar = model_data.loc[:]["FBAR"]
            stat_values_obar = model_data.loc[:]["OBAR"]
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "speed_err":
        stat_plot_name = "Difference in Average FCST and "+ \
                         "OBS Wind Vector Speeds"
        if line_type == "VCNT":
            stat_values = speed_err
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "dir_err":
        stat_plot_name = "Difference in Average FCST and "+ \
                         "OBS Wind Vector Direction"
        if line_type == "VCNT":
           stat_values = dir_err
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "rmsve":
        stat_plot_name = "Root Mean Square Difference Vector Error"
        if line_type == "VCNT":
           stat_values = rmsve
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "vdiff_speed":
        stat_plot_name = "Difference Vector Speed"
        if line_type == "VCNT":
            stat_values = vdiff_speed
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "vdiff_dir":
        stat_plot_name = "Difference Vector Direction"
        if line_type == "VCNT":
           stat_values = vdiff_dir
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "fbar_obar_speed":
        stat_plot_name = "Average Wind Vector Speed"
        if line_type == "VCNT":
            stat_values = model_data.loc[:][("FBAR_SPEED", "OBAR_SPEED")]
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "fbar_obar_dir":
        stat_plot_name = "Average Wind Vector Direction"
        if line_type == "VCNT":
           stat_values = model_data.loc[:][("FDIR", "ODIR")]
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "fbar_speed":
        stat_plot_name = "Average Forecast Wind Vector Speed"
        if line_type == "VCNT":
            stat_values = fbar_speed
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    elif stat_ == "fbar_dir":
        stat_plot_name = "Average Forecast Wind Vector Direction"
        if line_type == "VCNT":
            stat_values = fdir
        else:
            logger.error(stat+" cannot be computed from line type "+line_type)
            exit(1)
    else:
        logger.error(stat+" is not a valid option")
        exit(1)
    nindex = stat_values.index.nlevels 
    if stat == "fbar_obar":
        if nindex == 2:
            index0 = len(stat_values_fbar.index.get_level_values(0).unique())
            index1 = len(stat_values_fbar.index.get_level_values(1).unique())
            stat_values_array_fbar = \
                np.ma.masked_invalid(stat_values_fbar.values.reshape(
                index0,index1))
            index0 = len(stat_values_obar.index.get_level_values(0).unique())
            index1 = len(stat_values_obar.index.get_level_values(1).unique())
            stat_values_array_obar = \
                np.ma.masked_invalid(stat_values_obar.values.reshape(
                index0,index1))
        elif nindex == 3:
            index0 = len(stat_values_fbar.index.get_level_values(0).unique())
            index1 = len(stat_values_fbar.index.get_level_values(1).unique())
            index2 = len(stat_values_fbar.index.get_level_values(2).unique())
            stat_values_array_fbar = \
                np.ma.masked_invalid(stat_values_fbar.values.reshape(
                index0,index1,index2))
            index0 = len(stat_values_obar.index.get_level_values(0).unique())
            index1 = len(stat_values_obar.index.get_level_values(1).unique())
            index2 = len(stat_values_obar.index.get_level_values(2).unique())
            stat_values_array_obar = \
                np.ma.masked_invalid(stat_values_obar.values.reshape(
                index0,index1,index2))
        stat_values_array = np.ma.array([stat_values_array_fbar, 
                                         stat_values_array_obar
                                        ])
    else:
        if nindex == 2:
            index0 = len(stat_values.index.get_level_values(0).unique())
            index1 = len(stat_values.index.get_level_values(1).unique())
            stat_values_array = \
                np.ma.masked_invalid(stat_values.values.reshape(
                index0,index1))
        elif nindex == 3:
            index0 = len(stat_values.index.get_level_values(0).unique())
            index1 = len(stat_values.index.get_level_values(1).unique())
            index2 = len(stat_values.index.get_level_values(2).unique())
            stat_values_array = \
                np.ma.masked_invalid(stat_values.values.reshape(
                index0,index1,index2))
    return stat_values, stat_values_array, stat_plot_name
