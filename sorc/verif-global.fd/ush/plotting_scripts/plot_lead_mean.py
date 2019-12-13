## Edited from METplus V2.1
## for EMC purposes

from __future__ import (print_function, division)
import os
import numpy as np
import plot_util as plot_util
import pandas as pd
import warnings
import logging
import datetime
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md

warnings.filterwarnings('ignore')
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.formatter.useoffset'] = False
colors = [
    '#000000', '#2F1E80', '#D55E00', '#882255', 
    '#018C66', '#D6B616', '#036398', '#CC79A7'
]
verif_case = os.environ['VERIF_CASE']
verif_type = os.environ['VERIF_TYPE']
plot_time = os.environ['PLOT_TIME']
start_date_YYYYmmdd = os.environ['START_DATE_YYYYmmdd']
end_date_YYYYmmdd = os.environ['END_DATE_YYYYmmdd']
start_date_YYYYmmdd_dt = datetime.datetime.strptime(os.environ['START_DATE_YYYYmmdd'], "%Y%m%d")
end_date_YYYYmmdd_dt = datetime.datetime.strptime(os.environ['END_DATE_YYYYmmdd'], "%Y%m%d")
valid_time_info = os.environ['VALID_TIME_INFO'].replace('"','').split(", ")
init_time_info = os.environ['INIT_TIME_INFO'].replace('"','').split(", ")
fcst_var_name = os.environ['FCST_VAR_NAME']
fcst_var_name = os.environ['FCST_VAR_NAME']
fcst_var_extra = (
    os.environ['FCST_VAR_EXTRA'].replace(" ", "")
    .replace("=","").replace(";","").replace('"','')
    .replace("'","").replace(",","-").replace("_","")
)
if fcst_var_extra == "None":
    fcst_var_extra = ""
if os.environ['FCST_VAR_EXTRA'] == "None":
    fcst_var_extra_title = ""
else:
    fcst_var_extra_title = " "+os.environ['FCST_VAR_EXTRA']+" "
fcst_var_level = os.environ['FCST_VAR_LEVEL']
fcst_var_thresh = (
    os.environ['FCST_VAR_THRESH'].replace(" ","")
    .replace(">=","ge").replace("<=","le")
    .replace(">","gt").replace("<","lt")
    .replace("==","eq").replace("!=","ne")
)
if fcst_var_thresh == "None":
    fcst_var_thresh = ""
    fcst_var_thresh_title = ""
else:
    fcst_var_thresh_title = " "+fcst_var_thresh
obs_var_name = os.environ['OBS_VAR_NAME']
obs_var_extra = (
    os.environ['OBS_VAR_EXTRA'].replace(" ", "")
    .replace("=","").replace(";","")
    .replace('"','').replace("'","")
    .replace(",","-").replace("_","")
)
if obs_var_extra == "None":
    obs_var_extra = ""
if os.environ['OBS_VAR_EXTRA'] == "None":
    obs_var_extra_title = ""
else:
    obs_var_extra_title = " "+os.environ['OBS_VAR_EXTRA']+" "
obs_var_level = os.environ['OBS_VAR_LEVEL']
obs_var_thresh = (
    os.environ['OBS_VAR_THRESH'].replace(" ","")
    .replace(">=","ge").replace("<=","le")
    .replace(">","gt").replace("<","lt")
    .replace("==","eq").replace("!=","ne")
)
if obs_var_thresh == "None":
    obs_var_thresh = ""
    obs_var_thresh_title = ""
else:
    obs_var_thresh_title = " "+obs_var_thresh
interp = os.environ['INTERP']
region = os.environ['REGION']
lead_list = os.environ['LEAD_LIST'].split(", ")
leads = np.asarray(lead_list).astype(float)
stat_file_input_dir_base = os.environ['STAT_FILES_INPUT_DIR']
plotting_out_dir = os.environ['PLOTTING_OUT_DIR_FULL']
plotting_out_dir_data = os.path.join(plotting_out_dir,
                                     "data",
                                     plot_time+start_date_YYYYmmdd+"to"+end_date_YYYYmmdd
                                     +"_valid"+valid_time_info[0]+"to"+valid_time_info[-1]+"Z"
                                     +"_init"+init_time_info[0]+"to"+init_time_info[-1]+"Z")
plotting_out_dir_imgs = os.path.join(plotting_out_dir,
                                     "imgs")
if not os.path.exists(plotting_out_dir_data):
    os.makedirs(plotting_out_dir_data)
if not os.path.exists(plotting_out_dir_imgs):
    os.makedirs(plotting_out_dir_imgs)
plot_stats_list = os.environ['PLOT_STATS_LIST'].split(", ")
model_name_list = os.environ['MODEL_NAME_LIST'].split(" ")
model_plot_name_list = os.environ['MODEL_PLOT_NAME_LIST'].split(" ")
model_info = zip(model_name_list, model_plot_name_list)
mean_file_cols = [ "LEADS", "VALS", "OVALS" ]
ci_file_cols = [ "LEADS", "VALS" ]
ci_method = os.environ['CI_METHOD']
grid = os.environ['VERIF_GRID']
logger = logging.getLogger(os.environ['LOGGING_FILENAME'])
logger.setLevel(os.environ['LOGGING_LEVEL'])
formatter = logging.Formatter("%(asctime)s.%(msecs)03d (%(filename)s:%(lineno)d)"
                              +"%(levelname)s: %(message)s","%m/%d %H:%M:%S")
file_handler = logging.FileHandler(os.environ['LOGGING_FILENAME'], mode='a')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
noaa_logo_img_array = matplotlib.image.imread(os.path.join(os.environ['USHverif_global'],
                                                           'plotting_scripts',
                                                           'noaa.png'))
leads_sec = leads * 3600.
nmodels = len(model_name_list)
CI_bar_max_widths = np.append(np.diff(leads_sec),
                              leads[-1]-leads[-2])/1.5
CI_bar_min_widths = np.append(np.diff(leads_sec),
                              leads[-1]-leads[-2])/nmodels
CI_bar_intvl_widths = (
    (CI_bar_max_widths-CI_bar_min_widths)/nmodels
)
CI_bar_intvl_widths = CI_bar_intvl_widths/3600.
CI_bar_max_widths = CI_bar_max_widths/3600.
CI_bar_min_widths = CI_bar_min_widths/3600.
for stat in plot_stats_list:
    logger.debug("Working on "+stat)
    stat_plot_name = plot_util.get_stat_plot_name(logger, 
                                                  stat)
    logger.info("Reading in model data")
    for model in model_info:
        model_num = model_info.index(model) + 1
        model_index = model_info.index(model)
        model_name = model[0]
        model_plot_name = model[1]
        if stat == "fbar_obar":
            model_mean_data = np.empty([2,len(lead_list)])
        else:
            model_mean_data = np.empty(len(lead_list))
        model_mean_data.fill(np.nan)
        model_mean_file = os.path.join(plotting_out_dir_data, 
                                       model_plot_name
                                       +"_"+stat
                                       #+"_"+plot_time+start_date_YYYYmmdd+"to"+end_date_YYYYmmdd
                                       #+"_valid"+valid_time_info[0]+"to"+valid_time_info[-1]+"Z"
                                       #+"_init"+init_time_info[0]+"to"+init_time_info[-1]+"Z"
                                       +"_fcst"+fcst_var_name+fcst_var_level+fcst_var_extra+fcst_var_thresh
                                       +"_obs"+obs_var_name+obs_var_level+obs_var_extra+obs_var_thresh
                                       +"_interp"+interp
                                       +"_region"+region
                                       +"_LEAD_MEAN.txt")
        if os.path.exists(model_mean_file):
            nrow = sum(1 for line in open(model_mean_file))
            if nrow == 0: 
                logger.warning("Model "+str(model_num)+" "
                               +model_name+" with plot name "
                               +model_plot_name+" file: "
                               +model_mean_file+" empty")
            else:
                logger.debug("Model "+str(model_num)+" "
                             +model_name+" with plot name "
                             +model_plot_name+" file: "
                             +model_mean_file+" exists")
                model_mean_file_data = pd.read_csv(model_mean_file, 
                                                   sep=" ", 
                                                   header=None, 
                                                   names=mean_file_cols, 
                                                   dtype=str)
                if stat == "fbar_obar":
                    model_mean_file_data_leads = model_mean_file_data.loc[:]['LEADS'].tolist()
                    model_mean_file_data_vals = model_mean_file_data.loc[:]['VALS'].tolist()
                    model_mean_file_data_ovals = model_mean_file_data.loc[:]['OVALS'].tolist()
                    for lead in lead_list:
                        lead_index = lead_list.index(lead)
                        if lead in model_mean_file_data_leads:
                            model_mean_file_data_lead_index = model_mean_file_data_leads.index(lead)
                            if model_mean_file_data_vals[model_mean_file_data_lead_index] == "--":
                                 model_mean_data[0,lead_index] = np.nan
                            else:
                                model_mean_data[0,lead_index] = float(model_mean_file_data_vals[model_mean_file_data_lead_index])
                            if model_mean_file_data_ovals[model_mean_file_data_lead_index] == "--":
                                model_mean_data[1,lead_index] = np.nan
                            else:
                                model_mean_data[1,lead_index] = float(model_mean_file_data_ovals[model_mean_file_data_lead_index])
                else:
                    model_mean_file_data_leads = model_mean_file_data.loc[:]['LEADS'].tolist()
                    model_mean_file_data_vals = model_mean_file_data.loc[:]['VALS'].tolist()
                    for lead in lead_list:
                        lead_index = lead_list.index(lead)
                        if lead in model_mean_file_data_leads:
                            model_mean_file_data_lead_index = model_mean_file_data_leads.index(lead)
                            if model_mean_file_data_vals[model_mean_file_data_lead_index] == "--":
                                model_mean_data[lead_index] = np.nan
                            else:
                                model_mean_data[lead_index] = float(model_mean_file_data_vals[model_mean_file_data_lead_index])
        else:
            logger.warning("Model "+str(model_num)+" "
                           +model_name+" with plot name "
                           +model_plot_name+" file: "
                           +model_mean_file+" does not exist")
        if model_num == 1:
            fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10,12), sharex=True)
            ax1.grid(True)
            ax1.tick_params(axis='x', pad=15)
            ax1.set_xticks(leads)
            ax1.set_xlim([leads[0], leads[-1]])
            ax1.tick_params(axis='y', pad=15)
            ax1.set_ylabel("Mean", labelpad=30)
            ax2.grid(True)
            ax2.tick_params(axis='x', pad=15)
            ax2.set_xlabel("Forecast Hour", labelpad=30)
            ax2.tick_params(axis='y', pad=15)
            ax2.set_ylabel("Difference", labelpad=30)
            boxstyle = matplotlib.patches.BoxStyle("Square", pad=0.25)
            props = {'boxstyle': boxstyle,
            'facecolor': 'white',
            'linestyle': 'solid',
            'linewidth': 1,
            'edgecolor': 'black',}
            ax2.text(0.7055, 1.05, 
                     "Note: differences outside the outline bars are significant\n"
                     +" at the 95% confidence interval", 
                     ha="center", 
                     va="center", 
                     fontsize=10, 
                     bbox=props, 
                     transform=ax2.transAxes)
            if stat == "fbar_obar":
                ax2.set_title("Difference from obs", loc="left")
                ax1.plot(leads, model_mean_data[0,:], 
                         color=colors[model_index], 
                         ls='-', 
                         linewidth=3.0, 
                         marker='None', 
                         markersize=7, 
                         label=model_plot_name,
                         zorder=(nmodels-model_index)+4)
                ax1.plot(leads, model_mean_data[1,:], 
                         color='dimgrey', 
                         ls='-', 
                         linewidth=2.5, 
                         marker='None', 
                         markersize=7, 
                         label="Obs.",
                         zorder=4)
                ax2.plot(leads, np.zeros_like(leads), 
                         color='black', 
                         ls='-', 
                         linewidth=2.0,
                         zorder=4)
                ax2.plot(leads, model_mean_data[0,:]-model_mean_data[1,:], 
                         color=colors[model_index], 
                         ls='-', 
                         linewidth=2.0, 
                         marker='o', 
                         markersize=7,
                         zorder=(nmodels-model_index)+4)
                if ci_method != "NONE":
                    model_ci_data = np.empty(len(lead_list))
                    model_ci_data.fill(np.nan)
                    model_ci_file = os.path.join(plotting_out_dir_data, 
                                                 model_plot_name
                                                 +"_"+stat
                                                 #+"_"+plot_time+start_date_YYYYmmdd+"to"+end_date_YYYYmmdd
                                                 #+"_valid"+valid_time_info[0]+"to"+valid_time_info[-1]+"Z"
                                                 #+"_init"+init_time_info[0]+"to"+init_time_info[-1]+"Z"
                                                 +"_fcst"+fcst_var_name+fcst_var_level+fcst_var_extra+fcst_var_thresh
                                                 +"_obs"+obs_var_name+obs_var_level+obs_var_extra+obs_var_thresh
                                                 +"_interp"+interp
                                                 +"_region"+region
                                                 +"_CI_"+ci_method
                                                 +".txt")
                    if os.path.exists(model_ci_file):
                        nrow = sum(1 for line in open(model_ci_file))
                        if nrow == 0:
                            logger.warning("Model "+str(model_num)+" "
                                           +model_name+" with plot name "
                                           +model_plot_name+" file: "
                                           +model_ci_file+" empty")
                        else:
                            logger.debug("Model "+str(model_num)+" "
                                         +model_name+" with plot name "
                                         +model_plot_name+" file: "
                                         +model_ci_file+" exists")
                            model_ci_file_data = pd.read_csv(model_ci_file, 
                                                             sep=" ", 
                                                             header=None, 
                                                             names=ci_file_cols, 
                                                             dtype=str)
                            model_ci_file_data_leads = model_ci_file_data.loc[:]['LEADS'].tolist()
                            model_ci_file_data_vals = model_ci_file_data.loc[:]['VALS'].tolist()
                            for lead in lead_list:
                                lead_index = lead_list.index(lead)
                                if lead in model_ci_file_data_leads:
                                    model_ci_file_data_lead_index = model_ci_file_data_leads.index(lead)
                                    if model_ci_file_data_vals[model_ci_file_data_lead_index] == "--":
                                        model_ci_data[lead_index] = np.nan
                                    else:
                                        model_ci_data[lead_index] = float(model_ci_file_data_vals[model_ci_file_data_lead_index])
                    else:
                        logger.warning("Model "+str(model_num)+" "
                                       +model_name+" with plot name "
                                       +model_plot_name+" file: "
                                       +model_mean_file+" does not exist")
                    for lead in leads:
                        index = np.where(leads == lead)[0][0]
                        ax2.bar(leads[index], 2*np.absolute(model_ci_data[index]),
                                bottom=-1*np.absolute(model_ci_data[index]),
                                color='None',
                                width=CI_bar_max_widths-(CI_bar_intvl_widths*model_index),
                                edgecolor=colors[model_index], 
                                linewidth='1.5')
            else:
                ax2.set_title("Difference from "+model_plot_name, loc="left")
                ax1.plot(leads, model_mean_data, 
                         color=colors[model_index], 
                         ls='-', 
                         linewidth=3.0, 
                         marker='None', 
                         markersize=7, 
                         label=model_plot_name,
                         zorder=(nmodels-model_index)+4)
                ax2.plot(leads, np.zeros_like(leads), 
                         color=colors[model_index], 
                         ls='-', 
                         linewidth=2.0,
                         zorder=4)
                model1_mean_data = model_mean_data
        else:
            if stat == "fbar_obar":
                 ax1.plot(leads, model_mean_data[0,:], 
                          color=colors[model_index], 
                          ls='-', 
                          linewidth=2.0, 
                          marker='o', 
                          markersize=7, 
                          label=model_plot_name,
                          zorder=(nmodels-model_index)+4)
                 ax2.plot(leads, model_mean_data[0,:]-model_mean_data[1,:], 
                          color=colors[model_index], 
                          ls='-', 
                          linewidth=2.0,  
                          marker='o', 
                          markersize=7,
                          zorder=(nmodels-model_index)+4)
            else:
                ax1.plot(leads, model_mean_data, 
                         color=colors[model_index], 
                         ls='-', 
                         linewidth=2.0, 
                         marker='o', 
                         markersize=7, 
                         label=model_plot_name,
                         zorder=(nmodels-model_index)+4)
                ax2.plot(leads, model_mean_data-model1_mean_data, 
                         color=colors[model_index], 
                         ls='-', 
                         linewidth=2.0,  
                         marker='o', 
                         markersize=7,
                         zorder=(nmodels-model_index)+4)
            if ci_method != "NONE":
                model_ci_data = np.empty(len(lead_list))
                model_ci_data.fill(np.nan)
                model_ci_file = os.path.join(plotting_out_dir_data, 
                                             model_plot_name
                                             +"_"+stat
                                             #+"_"+plot_time+start_date_YYYYmmdd+"to"+end_date_YYYYmmdd
                                             #+"_valid"+valid_time_info[0]+"to"+valid_time_info[-1]+"Z"
                                             #+"_init"+init_time_info[0]+"to"+init_time_info[-1]+"Z"
                                             +"_fcst"+fcst_var_name+fcst_var_level+fcst_var_extra+fcst_var_thresh
                                             +"_obs"+obs_var_name+obs_var_level+obs_var_extra+obs_var_thresh
                                             +"_interp"+interp
                                             +"_region"+region
                                             +"_CI_"+ci_method
                                             +".txt")
                if os.path.exists(model_ci_file):
                    nrow = sum(1 for line in open(model_ci_file))
                    if nrow == 0:
                        logger.warning("Model "+str(model_num)+" "
                                       +model_name+" with plot name "
                                       +model_plot_name+" file: "
                                       +model_ci_file+" empty")
                    else:
                        logger.debug("Model "+str(model_num)+" "
                                     +model_name+" with plot name "
                                     +model_plot_name+" file: "
                                     +model_ci_file+" exists")
                        model_ci_file_data = pd.read_csv(model_ci_file, 
                                                         sep=" ", 
                                                         header=None, 
                                                         names=ci_file_cols, 
                                                         dtype=str)
                        model_ci_file_data_leads = model_ci_file_data.loc[:]['LEADS'].tolist()
                        model_ci_file_data_vals = model_ci_file_data.loc[:]['VALS'].tolist()
                        for lead in lead_list:
                            lead_index = lead_list.index(lead)
                            if lead in model_ci_file_data_leads:
                                model_ci_file_data_lead_index = model_ci_file_data_leads.index(lead)
                                if model_ci_file_data_vals[model_ci_file_data_lead_index] == "--":
                                    model_ci_data[lead_index] = np.nan
                                else:
                                    model_ci_data[lead_index] = float(model_ci_file_data_vals[model_ci_file_data_lead_index])
                else:
                    logger.warning("Model "+str(model_num)+" "
                                   +model_name+" with plot name "
                                   +model_plot_name+" file: "
                                   +model_mean_file+" does not exist")
                for lead in leads:
                    index = np.where(leads == lead)[0][0]
                    ax2.bar(leads[index], 2*np.absolute(model_ci_data[index]), 
                            bottom=-1*np.absolute(model_ci_data[index]), 
                            color='None',
                            width=CI_bar_max_widths-(CI_bar_intvl_widths*model_index), 
                            edgecolor=colors[model_index], 
                            linewidth='1')
    if stat == "fbar_obar":
        ax1.legend(bbox_to_anchor=(0.0, 1.02, 1.0, .102), 
                   loc=3, 
                   ncol=nmodels+1, 
                   fontsize='13', 
                   mode="expand", 
                   borderaxespad=0.)
    else:
        ax1.legend(bbox_to_anchor=(0.0, 1.02, 1.0, .102), 
                   loc=3, 
                   ncol=nmodels, 
                   fontsize='13', 
                   mode="expand", 
                   borderaxespad=0.)
    if grid == region:
        gridregion = grid
        gridregion_title = grid
    else:
        gridregion = grid+region
        gridregion_title = grid+"-"+region
    if interp[0:2] == 'WV':
        fcst_var_name = fcst_var_name+"_"+interp
    if plot_time == 'valid':
        savefig_name = os.path.join(plotting_out_dir_imgs, 
                                    stat
                                    +"_valid"+valid_time_info[0][0:2]+"Z"
                                    +"_"+fcst_var_name+"_"+fcst_var_level
                                    +"_fhrmean"
                                    +"_"+gridregion
                                    +".png")
        full_title = (
            stat_plot_name+"\n"
            +fcst_var_name+" "+fcst_var_level+fcst_var_extra_title+fcst_var_thresh_title
            +" "+gridregion_title+"\n"
            +plot_time+": "
            +start_date_YYYYmmdd_dt.strftime("%d%b%Y")+"-"
            +end_date_YYYYmmdd_dt.strftime("%d%b%Y")
            +" "+valid_time_info[0][0:2]+"Z"
            +", forecast hour means\n"
        ) 
    elif plot_time == 'init':
        savefig_name = os.path.join(plotting_out_dir_imgs,
                                    stat
                                    +"_init"+init_time_info[0][0:2]+"Z"
                                    +"_"+fcst_var_name+"_"+fcst_var_level
                                    +"_fhrmean"
                                    +"_"+gridregion
                                    +".png")
        full_title = (
            stat_plot_name+"\n"
            +fcst_var_name+" "+fcst_var_level+fcst_var_extra_title+fcst_var_thresh_title
            +" "+gridregion_title+"\n"
            +plot_time+": "
            +start_date_YYYYmmdd_dt.strftime("%d%b%Y")+"-"
            +end_date_YYYYmmdd_dt.strftime("%d%b%Y")
            +" "+init_time_info[0][0:2]+"Z"
            +", forecast hour means\n"
        ) 
    fig.suptitle(full_title, fontsize=14, fontweight='bold')
    fig.figimage(noaa_logo_img_array, 1, 1, zorder=1, alpha=0.5)
    logger.info("Saving image as "+savefig_name)
    plt.savefig(savefig_name, bbox_inches='tight')
    plt.close()
