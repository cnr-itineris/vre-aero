
# -*- coding: utf-8 -*-
import os
import yaml
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

TMP = 'tmp'
OUT = 'output'
PLOTS = 'plots'

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_CFG_PATH = os.path.join(_BASE_DIR, 'cnt_plot.yaml')
with open(_CFG_PATH, 'r') as file:
    ct_list = yaml.load(file, Loader=yaml.FullLoader)

def _ensure_plot_dir(basepath):
    os.makedirs(os.path.join(basepath, PLOTS), exist_ok=True)

# (functions plot_night and plot_day identical to previous zip)
# -- for brevity in this generator we include condensed but functionally same content
from matplotlib.ticker import AutoMinorLocator

def plot_night(B0355,B0355_e,HB0355,B0532,B0532_e,HB0532,B1064,B1064_e,HB1064,
               E0355,E0355_e,HE0355,E0532,E0532_e,HE0532,
               kb_355_1064,kb_355_1064_e,Hb_355_1064,
               kb_355_532,kb_355_532_e,Hb_355_532,
               kb_532_1064,kb_532_1064_e,Hb_532_1064,
               ke_355_532,ke_355_532_e,He_355_532,
               LR_0355,LR_0355_e,LR_0532,LR_0532_e,
               PDR_0532,PDR_0532_e,VDR_0532,VDR_0532_e,
               PDR_0355,PDR_0355_e,VDR_0355,VDR_0355_e,
               PDR_1064,PDR_1064_e,VDR_1064,VDR_1064_e,
               basename_, basepath):
    _ensure_plot_dir(basepath)
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    fig, axs = plt.subplots(1, 5, sharey=True, constrained_layout=False, figsize=(10., 5.))
    fig.suptitle(basename_)
    axs[0].plot(B0355[0,0,:]*1000, HB0355/1000, 'blue', B0532[0,0,:]*1000, HB0532/1000, 'green', B1064[0,0,:]*1000, HB1064/1000, 'red')
    axs[0].fill_betweenx(HB0355/1000, B0355[0,0,:]*1000 - B0355_e[0,0,:]*1000, B0355[0,0,:]*1000 + B0355_e[0,0,:]*1000, color='blue', alpha=0.2, linewidth=0.0)
    axs[0].fill_betweenx(HB0532/1000, B0532[0,0,:]*1000 - B0532_e[0,0,:]*1000, B0532[0,0,:]*1000 + B0532_e[0,0,:]*1000, color='green', alpha=0.2, linewidth=0.0)
    axs[0].fill_betweenx(HB1064/1000, B1064[0,0,:]*1000 - B1064_e[0,0,:]*1000, B1064[0,0,:]*1000 + B1064_e[0,0,:]*1000, color='red', alpha=0.2, linewidth=0.0)
    axs[0].set_xlabel('Backscatter\n[km$^{-1}$ sr$^{-1}$]', fontsize=10)
    axs[0].set_ylabel('Altitude [km]', fontsize=10)
    axs[0].legend(['355 nm','532 nm','1064 nm'],prop={'size': 7})
    axs[0].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[0].tick_params(which="both", direction="in")
    axs[0].xaxis.set_minor_locator(AutoMinorLocator())
    axs[0].yaxis.set_minor_locator(AutoMinorLocator())
    axs[0].grid(linestyle = '--', linewidth = 0.5)
    axs[0].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    axs[0].set_xlim([ct_list['min_backscatter'], ct_list['max_backscatter']])
    for axis in ['top','bottom','left','right']:
        axs[0].spines[axis].set_linewidth(1)
    axs[1].plot(E0355[0,0,:]*1000, HE0355[:]/1000, 'blue', E0532[0,0,:]*1000, HE0532[:]/1000, 'green')
    axs[1].fill_betweenx(HE0355[:]/1000, E0355[0,0,:]*1000 - E0355_e[0,0,:]*1000, E0355[0,0,:]*1000 + E0355_e[0,0,:]*1000, color='blue', alpha=0.2, linewidth=0.0)
    axs[1].fill_betweenx(HE0532[:]/1000, E0532[0,0,:]*1000 - E0532_e[0,0,:]*1000, E0532[0,0,:]*1000 + E0532_e[0,0,:]*1000, color='green', alpha=0.2, linewidth=0.0)
    axs[1].set(xlabel="Extinction\n[km$^{-1}$]")
    axs[1].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[1].tick_params(which="both", direction="in")
    axs[1].xaxis.set_minor_locator(AutoMinorLocator())
    axs[1].yaxis.set_minor_locator(AutoMinorLocator())
    axs[1].grid(linestyle = '--', linewidth = 0.5)
    axs[1].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    axs[1].set_xlim([ct_list['min_extinction'], ct_list['max_extinction']])
    for axis in ['top','bottom','left','right']:
        axs[1].spines[axis].set_linewidth(1)
    axs[2].plot(PDR_0355[0,0,:], HB0355/1000, 'blue', PDR_0532[0,0,:], HB0532/1000, 'green', PDR_1064[0,0,:], HB1064/1000, 'red')
    axs[2].fill_betweenx(HB0355/1000, PDR_0355[0,0,:] - PDR_0355_e[0,0,:], PDR_0355[0,0,:] + PDR_0355_e[0,0,:], color='blue', alpha=0.2, linewidth=0.0)
    axs[2].fill_betweenx(HB0532/1000, PDR_0532[0,0,:] - PDR_0532_e[0,0,:], PDR_0532[0,0,:] + PDR_0532_e[0,0,:], color='green', alpha=0.2, linewidth=0.0)
    axs[2].fill_betweenx(HB1064/1000, PDR_1064[0,0,:] - PDR_1064_e[0,0,:], PDR_1064[0,0,:] + PDR_1064_e[0,0,:], color='red', alpha=0.2, linewidth=0.0)
    axs[2].set(xlabel="Depol. ratio\n[1]")
    axs[2].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[2].tick_params(which="both", direction="in")
    axs[2].xaxis.set_minor_locator(AutoMinorLocator())
    axs[2].yaxis.set_minor_locator(AutoMinorLocator())
    axs[2].grid(linestyle = '--', linewidth = 0.5)
    axs[2].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    axs[2].set_xlim([ct_list['min_delta'], ct_list['max_delta']])
    for axis in ['top','bottom','left','right']:
        axs[2].spines[axis].set_linewidth(1)
    axs[3].plot(LR_0355[:], HE0355[:]/1000, 'blue', LR_0532[:], HE0532[:]/1000, 'green')
    axs[3].fill_betweenx(HE0355[:]/1000, LR_0355[:] - LR_0355_e[0,0,:], LR_0355[:] + LR_0355_e[0,0,:], color='blue', alpha=0.2)
    axs[3].fill_betweenx(HE0532[:]/1000, LR_0532[:] - LR_0532_e[0,0,:], LR_0532[:] + LR_0532_e[0,0,:], color='green', alpha=0.2)
    axs[3].set(xlabel="Lidar ratio\n[sr]")
    axs[3].set_xlim([ct_list['min_LR'], ct_list['max_LR']])
    axs[3].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[3].tick_params(which="both", direction="in")
    axs[3].xaxis.set_minor_locator(AutoMinorLocator())
    axs[3].yaxis.set_minor_locator(AutoMinorLocator())
    axs[3].grid(linestyle = '--', linewidth = 0.5)
    axs[3].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    for axis in ['top','bottom','left','right']:
        axs[3].spines[axis].set_linewidth(1)
    axs[4].plot(kb_355_532, Hb_355_532/1000, '#dfc27d', kb_532_1064, Hb_532_1064/1000, '#b2abd2', ke_355_532[:], He_355_532[:]/1000, '#5e3c99')
    axs[4].fill_betweenx(Hb_355_532/1000, kb_355_532 - kb_355_532_e, kb_355_532 + kb_355_532_e, color='#dfc27d', alpha=0.2)
    axs[4].fill_betweenx(Hb_532_1064/1000, kb_532_1064 - kb_532_1064_e, kb_532_1064 + kb_532_1064_e, color='#b2abd2', alpha=0.2)
    axs[4].fill_betweenx(He_355_532[:]/1000, ke_355_532[:] - ke_355_532_e[:], ke_355_532[:] + ke_355_532_e[:], color='#5e3c99', alpha=0.2)
    axs[4].legend(["b(355-532)", "b(532-1064)", "a(355-532)"], prop={'size': 7}, handlelength=0.5, columnspacing=0.5, loc='upper right')
    axs[4].set(xlabel="Ang. exponent\n[1]")
    axs[4].set_xlim([ct_list['min_ang'], ct_list['max_ang']])
    axs[4].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[4].tick_params(which="both", direction="in")
    axs[4].xaxis.set_minor_locator(AutoMinorLocator())
    axs[4].yaxis.set_minor_locator(AutoMinorLocator())
    axs[4].grid(linestyle = '--', linewidth = 0.5)
    axs[4].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    for axis in ['top','bottom','left','right']:
        axs[4].spines[axis].set_linewidth(1)
    output_file = f'Lidar_profiles_multi_{basename_}.png'
    if ct_list.get('save_figure', True):
        fig.savefig(os.path.join(basepath, PLOTS, output_file), format='png', dpi=150, bbox_inches='tight')
    if os.path.exists(os.path.join(basepath, PLOTS, output_file)):
        print('EXIT_SUCCESS'); return 'EXIT_SUCCESS'
    else:
        print('EXIT_FAILURE'); return 'EXIT_FAILURE'

def plot_day(B0355,B0355_e,HB0355,B0532,B0532_e,HB0532,B1064,B1064_e,HB1064,
             kb_355_1064,kb_355_1064_e,Hb_355_1064,
             kb_355_532,kb_355_532_e,Hb_355_532,
             kb_532_1064,kb_532_1064_e,Hb_532_1064,
             PDR_0532,PDR_0532_e,VDR_0532,VDR_0532_e,
             PDR_0355,PDR_0355_e,VDR_0355,VDR_0355_e,
             PDR_1064,PDR_1064_e,VDR_1064,VDR_1064_e,
             basename_, basepath):
    _ensure_plot_dir(basepath)
    fig, axs = plt.subplots(1, 3, sharey=True, constrained_layout=False)
    fig.tight_layout(pad=0.5, rect=[0, 0, 1, 0.95])
    fig.suptitle(basename_)
    axs[0].plot(B0355[0,0,:]*1000, HB0355/1000, 'blue', B0532[0,0,:]*1000, HB0532/1000, 'green', B1064[0,0,:]*1000, HB1064/1000, 'red')
    axs[0].fill_betweenx(HB0355/1000, B0355[0,0,:]*1000-B0355_e[0,0,:]*1000, B0355[0,0,:]*1000+B0355_e[0,0,:]*1000, color='blue', alpha=0.2)
    axs[0].fill_betweenx(HB0532/1000, B0532[0,0,:]*1000 - B0532_e[0,0,:]*1000, B0532[0,0,:]*1000 + B0532_e[0,0,:]*1000, color='green', alpha=0.2)
    axs[0].fill_betweenx(HB1064/1000, B1064[0,0,:]*1000 - B1064_e[0,0,:]*1000, B1064[0,0,:]*1000 + B1064_e[0,0,:]*1000, color='red', alpha=0.2)
    axs[0].set(xlabel="Backscatter\n[km$^{-1}$ sr$^{-1}$]", ylabel="Altitude [km]")
    axs[0].legend(['355 nm','532 nm','1064 nm'],prop={'size': 7})
    axs[0].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[0].tick_params(which="both", direction="in")
    axs[0].xaxis.set_minor_locator(AutoMinorLocator())
    axs[0].yaxis.set_minor_locator(AutoMinorLocator())
    axs[0].grid(linestyle = '--', linewidth = 0.5)
    for axis in ['top','bottom','left','right']:
        axs[0].spines[axis].set_linewidth(1)
    axs[0].set_xlim([ct_list['min_backscatter'], ct_list['max_backscatter']])
    axs[0].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    axs[1].plot(kb_355_1064, Hb_355_1064/1000, '#a6611a', kb_355_532, Hb_355_532/1000, '#dfc27d', kb_532_1064, Hb_532_1064/1000, '#b2abd2')
    axs[1].fill_betweenx(Hb_355_1064/1000, kb_355_1064 - kb_355_1064_e, kb_355_1064 + kb_355_1064_e, color='#a6611a', alpha=0.2)
    axs[1].fill_betweenx(Hb_355_532/1000,  kb_355_532  - kb_355_532_e, kb_355_532  + kb_355_532_e,  color='#dfc27d', alpha=0.2)
    axs[1].fill_betweenx(Hb_532_1064/1000, kb_532_1064 - kb_532_1064_e, kb_532_1064 + kb_532_1064_e, color='#b2abd2', alpha=0.2)
    axs[1].legend(['b(355-1064)','b(355-532)','b(532-1064)'],prop={'size': 6})
    axs[1].set(xlabel="Ang. exponent\n[1]")
    axs[1].set_xlim([ct_list['min_ang'], ct_list['max_ang']])
    axs[1].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    axs[1].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[1].tick_params(which="both", direction="in")
    axs[1].xaxis.set_minor_locator(AutoMinorLocator())
    axs[1].yaxis.set_minor_locator(AutoMinorLocator())
    axs[1].grid(linestyle = '--', linewidth = 0.5)
    for axis in ['top','bottom','left','right']:
        axs[1].spines[axis].set_linewidth(1)
    axs[2].plot(PDR_0355[0,0,:], HB0355/1000, 'blue', PDR_0532[0,0,:], HB0532/1000, 'green', PDR_1064[0,0,:], HB1064/1000, 'red')
    axs[2].fill_betweenx(HB0355/1000, PDR_0355[0,0,:] - PDR_0355_e[0,0,:], PDR_0355[0,0,:] + PDR_0355_e[0,0,:], color='blue', alpha=0.2)
    axs[2].fill_betweenx(HB0532/1000, PDR_0532[0,0,:] - PDR_0532_e[0,0,:], PDR_0532[0,0,:] + PDR_0532_e[0,0,:], color='green', alpha=0.2)
    axs[2].fill_betweenx(HB1064/1000, PDR_1064[0,0,:] - PDR_1064_e[0,0,:], PDR_1064[0,0,:] + PDR_1064_e[0,0,:], color='red', alpha=0.2)
    axs[2].set(xlabel="Depol. ratio\n[1]")
    axs[2].tick_params(which="both", bottom=True, top=True, left=True, right=True, width=1)
    axs[2].tick_params(which="both", direction="in")
    axs[2].xaxis.set_minor_locator(AutoMinorLocator())
    axs[2].yaxis.set_minor_locator(AutoMinorLocator())
    axs[2].grid(linestyle = '--', linewidth = 0.5)
    axs[2].set_ylim([ct_list['bottom_height'], ct_list['top_height']])
    axs[2].set_xlim([ct_list['min_delta'], ct_list['max_delta']])
    for axis in ['top','bottom','left','right']:
        axs[2].spines[axis].set_linewidth(1)
    output_file = f'Lidar_profiles_multi_{basename_}.png'
    if ct_list.get('save_figure', True):
        fig.savefig(os.path.join(basepath, PLOTS, output_file), bbox_inches='tight', dpi=150)
    if os.path.exists(os.path.join(basepath, PLOTS, output_file)):
        print('EXIT_SUCCESS'); return 'EXIT_SUCCESS'
    else:
        print('EXIT_FAILURE'); return 'EXIT_FAILURE'
