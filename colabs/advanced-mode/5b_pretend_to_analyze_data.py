#@title <font face="Helvetica" color='#702020'><b>&lt;- Click to run EXOTIC to generate a lightcurve</b></font>
# This generation is a simulation only using unstyled logging from a HAT-P-32 b EXOTIC run

importCustomStyles()


display(HTML('<p class="bookend">START: Analyzing telescope images</p>'))

log_10 = """
Path to the inits file(s) that will be used:
/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/inits.json
!exotic -red "/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/inits.json" -ov
    Downloading __databases__.pickle_new...
    Done!
Checking exotethys database...
Checking ephemerides database...
Checking photometry database...
Checking catalogues database...

*************************************************************
Welcome to the EXOplanet Transit Interpretation Code (EXOTIC)
Version 1.10.2
*************************************************************


**************************
Complete Reduction Routine
**************************

**************************
Starting Reduction Process
**************************


Getting the plate solution for your imaging file to translate pixel coordinates on the sky. 
Please wait....

"""

log_20 = """
WCS file creation successful.
Thinking ... DONE!

Here is the path to your plate solution: /content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/wcs.fits

Checking for variability in Comparison Star #1:
    Pixel X: 493 Pixel Y: 304
 Warning: Your comparison star cannot be resolved in the SIMBAD star database; EXOTIC cannot check if it is variable or not. 
EXOTIC will still include this star in the reduction. 
Please proceed with caution as we cannot check for stellar variability.


Checking for variability in Comparison Star #2:
    Pixel X: 415 Pixel Y: 343
 Warning: Your comparison star cannot be resolved in the SIMBAD star database; EXOTIC cannot check if it is variable or not. 
EXOTIC will still include this star in the reduction. 
Please proceed with caution as we cannot check for stellar variability.


Computing best comparison star, aperture, and sky annulus. Please wait.
"""

log_30 = """

*********************************************
Best Comparison Star: None
Minimum Residual Scatter: 0.672%
Optimal Aperture: 5.02
Optimal Annulus: 7.54
*********************************************

No Barycentric Julian Dates (BJDs) in Image Headers for standardizing time format. Converting all JDs to BJD_TDBs.
Please be patient- this step can take a few minutes.
"""

log_40 = """
Thinking ... DONE!


Output File Saved


****************************************
Fitting a Light Curve Model to Your Data
****************************************

[ultranest] Sampling 400 live points from prior ...


Mono-modal Volume: ~exp(-3.81) * Expected Volume: exp(0.00) Quality: ok

rprs:   +0.0000|**********|  +0.1861
tmid: +2458107.706|**********|+2458107.716
ars :      +4.8|**********|     +5.9
a2  :      -3.0|**********|     +3.0

Z=-1659103.7(0.00%) | Like=-1655784.03..-111.41 [-8987932.8990..-176103.1770] | it/evals=80/494 eff=85.1064% N=400 

Mono-modal Volume: ~exp(-3.96) * Expected Volume: exp(-0.23) Quality: ok

rprs:   +0.0000|**********|  +0.1861
tmid: +2458107.706|**********|+2458107.716
ars :      +4.8|**********|     +5.9
a2  :      -3.0|********  |     +3.0

Z=-338377.3(0.00%) | Like=-334422.26..-111.41 [-8987932.8990..-176103.1770] | it/evals=160/609 eff=76.5550% N=400 

Mono-modal Volume: ~exp(-4.18) * Expected Volume: exp(-0.45) Quality: ok

rprs:   +0.0000|**********|  +0.1861
tmid: +2458107.706|**********|+2458107.716
ars :      +4.8|**********|     +5.9
a2  :      -3.0|*******   |     +3.0

Z=-202573.2(0.00%) | Like=-201882.30..-111.41 [-8987932.8990..-176103.1770] | it/evals=240/730 eff=72.7273% N=400 

"""

log_50 = """
Mono-modal Volume: ~exp(-20.47)   Expected Volume: exp(-17.10) Quality: ok

rprs:    +0.000|        * |   +0.186
tmid: +2458107.706|       ** |+2458107.716
ars :      +4.8|    **    |     +5.9
a2  :    -1.000|    *     |   +1.000

[ultranest] Explored until L=-7e+01  
[ultranest] Likelihood function evaluations: 15883
[ultranest]   logZ = -82.92 +- 0.141
[ultranest] Effective samples strategy satisfied (ESS = 2176.7, need >400)
[ultranest] Posterior uncertainty strategy is satisfied (KL: 0.45+-0.05 nat, need <0.50 nat)
[ultranest] Evidency uncertainty strategy is satisfied (dlogz=0.14, need <0.5)
[ultranest]   logZ error budget: single: 0.16 bs:0.14 tail:0.01 total:0.14 required:<0.50
[ultranest] done iterating.

*********************************************************
FINAL PLANETARY PARAMETERS

          Mid-Transit Time [BJD_TDB]: 2458107.7136 +/- 0.001
  Radius Ratio (Planet/Star) [Rp/Rs]: 0.1587 +/- 0.0037
           Transit depth [(Rp/Rs)^2]: 2.52 +/- 0.12 [%]
 Semi Major Axis/ Star Radius [a/Rs]: 5.36 +/- 0.11
               Airmass coefficient 1: 1.1645 +/- 0.0078
               Airmass coefficient 2: -0.1222 +/- 0.0028
                    Residual scatter: 0.67 %
                 Best Comparison Star: None
                    Optimal Aperture: 5.02
                     Optimal Annulus: 7.54
              Transit Duration [day]: 0.1311 +/- 0.0028
*********************************************************
Output Files Saved

************************
End of Reduction Process
************************
"""

log_60 = """
************************
EXOTIC has successfully run!!!
It is now safe to close this window.
************************
lightcurve: /content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/FinalLightCurve_HAT-P-32 b_2017-12-19.png
"""

import time
print(log_10)
showProgress(1)
print(log_20)
showProgress(1)
print(log_30)
showProgress(1)
print(log_40)
showProgress(1)
print(log_50)
showProgress(1)
print(log_60)

display(HTML('<h3>CONGRATULATIONS!</h3>'))
display(HTML('<p>The data for the lightcurve you see here is at /content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/AAVSO_HAT-P-32 b_2017-12-19.txt. Click the folder icon in the left nav to navigate to it.'))

display(HTML('<div class="button">Download lightcurve data</div>'))

do_download = input("Download lightcurve data? (y/N) ")
if do_download in ['Y','y']:
  if os.path.isfile('/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/AAVSO_HAT-P-32 b_2017-12-19.txt'):
    display(HTML('<p>Downloading now...</p>'))
    showProgress(2)
    files.download('/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output/AAVSO_HAT-P-32 b_2017-12-19.txt')
  else: 
    display(HTML('<p>Couldn\'t find output file. Alert the developers to ensure it is in the sample-data repo being used.</p>'))


display(HTML('<p class="bookend">DONE: Analyzing telescope images. <b>Tutorial completed!</b></p>'))



display(HTML('''
<h2>You\'re done!</h2> 
<h3>You have successfully generated a lightcurve showing the transit of HAT-P-32 b around HAT-P-32</h3>

<p>If you downloaded the data to your hard drive (as "AAVSO_HAT-P-32 b_2017-12-19.txt"), it will be in a format suitable for submission to AAVSO, though please don't submit it! This exoplanet was actually discovered in 2011, and you can <a href="https://exoplanets.nasa.gov/exoplanet-catalog/1434/HAT-P-32-b/">view it in 3D on exoplanets.nasa.gov</a>.</p>

<h3>Ready for the next step?</h3>

<div class="buttonset"><a href="https://exoplanets.nasa.gov/exoplanet-watch/how-to-contribute/how-to-observe/" target="_parent" class="button" style="font-size:20px">Create your own telescope images</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://exoplanets-5.client.mooreboeck.com/exoplanet-watch/exotic/" target="_top" class="button" style="font-size:20px">Run EXOTIC on your telescope images</a></div>
'''))
