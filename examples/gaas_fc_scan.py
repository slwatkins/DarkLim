import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

import darklim

from multihist import Hist1d
import time

##################################################################

efficiency = 1.0
tm = 'GaAs' # target name
energy_res = 0.373e-4 # energy resolution in keV

gaas_gain = 0.40 * 0.40 + 0.60 * 0.05

##################################################################

def plot_dm_rates(m_dms,dm_rates,raw_dm_rates,sigma0,savename=None):
    
    #print('Signal events at m={:0.3f} GeV & {:0.1e} cm2: {:0.3e} evts'.format(mass,sigma0,signal_rates[ii]))
    
    # plot the evt rate vs mass:
    fig, ax = plt.subplots(1,figsize=(6,4))
    plt.plot(m_dms,dm_rates)
    #plt.plot(en_interp,curr_exp(en_interp),ls='--')
    #ax.axvline(threshold,ls='--',color='red')
    ax.set_ylabel('Events')
    ax.set_xlabel('Dark Matter Mass [GeV]')
    ax.set_xlim(m_dms[0],m_dms[-1])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('Expected WIMP events at {:0.1e} cm2'.format(sigma0))
    
    if savename is not None:
        plt.savefig(savename+'_rate.png',facecolor='white',bbox_inches='tight')
    
    # plot the acceptance vs mass:
    fig, ax = plt.subplots(1,figsize=(6,4))
    plt.plot(m_dms,dm_rates/raw_dm_rates)
    ax.set_ylabel('Signal Acceptance')
    ax.set_xlabel('Dark Matter Mass [GeV]')
    ax.set_xlim(m_dms[0],m_dms[-1])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(1e-5,1)
    #ax.set_title('Signal Acceptance')
    
    if savename is not None:
        plt.savefig(savename+'_acceptance.png',facecolor='white',bbox_inches='tight')
    
    return

def run_scan_point(nexp,time_elapsed,mass_det,n_devices,coinc,window,var_threshold=False,save=True,savedir=None):
    
    if coinc==1: # if coinc is 1, LEE is 'unknown'
        known_bkgs = [0]
    else:
        known_bkgs = [0,1]
    
    m_dms = np.geomspace(0.0001, 5, 50)
    sigma0 = 1e-36
    
    ehigh = 1 # keV
    
    if var_threshold:
        nsigma = stats.norm.isf(stats.norm.sf(5)**(1/coinc))
    else:
        nsigma = 5
    
    per_device_threshold = nsigma * energy_res # threshold
    threshold = coinc*per_device_threshold
    
    SE = darklim.sensitivity.SensEst(mass_det, time_elapsed, eff=efficiency, tm=tm, gain=gaas_gain)
    SE.reset_sim()
    SE.add_flat_bkgd(1) # flat background of 1 DRU
    SE.add_nfold_lee_bkgd(m=n_devices,n=coinc,w=window)
    
    print('\nRunning with the following settings:')
    print('Mass: {:0.4f} kg; Time: {:0.3f} d => Exposure: {:0.3f} kg-d'.format(SE.m_det,time_elapsed,SE.exposure))
    print('Coincidence: {:d}-fold in {:d} devices; {:0.1f} microsecond window'.format(coinc,n_devices,window/1e-6))
    print('Energy threshold: {:0.3f} eV; {:0.2f} sigma in each device'.format(threshold*1e3,nsigma))

    # run
    sig = np.zeros_like(m_dms)
    ul = np.zeros_like(m_dms)
    dm_rates = np.zeros_like(m_dms)
    raw_dm_rates = np.zeros_like(m_dms)
    exp_bkg = np.zeros_like(m_dms)

    for i, mass in enumerate(m_dms):
        _, sig[i], ul[i], dm_rates[i], raw_dm_rates[i], exp_bkg[i] = SE.run_fast_fc_sim(
        known_bkgs,
        threshold,
        ehigh,
        e_low=1e-6, #threshold,
        m_dms=[mass],
        nexp=nexp,
        npts=int(1e5),
        plot_bkgd=True,
#        res=np.sqrt(n_devices)*energy_res,
        verbose=True,
        sigma0=sigma0,
        use_drdefunction=True,
        pltname=savedir+'/ULs_{:0.0f}d_{:d}device_{:d}fold_{:0.0f}mus'.format(time_elapsed,n_devices,coinc,window/1e-6)
        #pltname=None
        )
    
    # save results to txt file
    if save and savedir is not None:
        outname = './{:s}/HeRALD_FC_{:0.0f}d_{:d}device_{:d}fold_{:0.0f}mus.txt'.format(savedir,time_elapsed,n_devices,coinc,window/1e-6)
        tot = np.column_stack( (m_dms, sig, dm_rates/raw_dm_rates, exp_bkg) )
        np.savetxt(outname,tot,fmt=['%.5e','%0.5e','%0.5e','%0.5e'] ,delimiter=' ')
    
    # plot acceptance and DM evt rate:
    savename = \
    './{:s}/dmrate_{:0.0f}d_{:d}device_{:d}fold_{:0.0f}mus'.format(savedir,time_elapsed,n_devices,coinc,window/1e-6)
    plot_dm_rates(m_dms,dm_rates,raw_dm_rates,sigma0,savename=savename)
    
    return
    
def gaas_scan(results_dir):
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    nexp = 200 # number of toys
    
    var_threshold = True # vary 5sigma requirement based on coinc level
    
    times = np.array([1]) # d
    mass_det = 8.*5.32*1e-3 # mass in kg, = 8cc * 3.98g/cc
    exposures = times*mass_det
    
    n_devices = 4
    coinc = np.arange(2,3)
    #coinc = np.array([1])
    window = 100e-6 # s
    
    for t in times:
        for n in coinc:
            run_scan_point(
                nexp,
                t,
                mass_det,
                n_devices,
                n,
                window,
                var_threshold=var_threshold,
                save=True,
                savedir=results_dir
            )
        
    return

# ------------------------------------------------------
# ------------------------------------------------------
def main():
    
    t_start = time.time()
    try: 
        results_dir = sys.argv[1]
    except:
        print("Check inputs.\n")
        return 1
    
    gaas_scan(results_dir)
    t_end = time.time()
    print(f'Took {(t_end - t_start)/60} minutes.')

    return 0

if __name__ == "__main__":
         main()