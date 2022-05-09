# Swift Host Subtraction

This is a python package to perform aperture photometry on a single source in data from the Ultraviolet Optical Telescope ([UVOT](https://swift.gsfc.nasa.gov/about_swift/uvot_desc.html); [Roming et al. 2005](https://ui.adsabs.harvard.edu/abs/2005SSRv..120...95R/abstract)) on board the [Neil Gehrels Swift Observatory](https://swift.gsfc.nasa.gov) ([Gehrels et al. 2004](https://ui.adsabs.harvard.edu/abs/2004ApJ...611.1005G/abstract)). In particular, this package is oriented towards transient studies, as it can calculate template-subtracted luminosities if a template image is provided. 

This project is based greatly on [Peter J. Brown](https://pbrown801.github.io)'s work. He wrote the original code in IDL, and published it in his [PhD Thesis](https://etda.libraries.psu.edu/files/final_submissions/4865). The aperture photometry is done following the standard guidelines described in [Brown et al. (2009)](https://ui.adsabs.harvard.edu/abs/2009AJ....137.4517B/abstract). The image subtraction is perfermed following the prescriptions outlined in [Brown et al. (2014)](https://ui.adsabs.harvard.edu/abs/2014Ap%26SS.354...89B/abstract). See the full documentation (work in progress) for more details.

If you are interested in supernova light curves, check out also the Swift's Optical/Ultraviolet Supernova Archive ([SOUSA](https://pbrown801.github.io/SOUSA/)).

# badges
[![codecov](https://codecov.io/gh/CIERA-Northwestern/template/branch/main/graph/badge.svg?token=jAAQvHfHat)](https://codecov.io/gh/CIERA-Northwestern/template)
![Unit Test Swift_host_subtraction](https://github.com/CIERA-Northwestern/template/workflows/Unit%20Test%20Swift_host_subtraction/badge.svg)

# Documentation URL
[Documentation](https://ciera-northwestern.github.io/template/)

# HEAsoft software
The package uses [HEAsoft](https://heasarc.gsfc.nasa.gov/docs/software/heasoft/) commands like `uvotmaghist` and `uvotimsum`, which need to be installed separetly. Refer to the [website](https://heasarc.gsfc.nasa.gov/docs/software/heasoft/download.html) for a standard installation. Be sure to select the Swift packages in the STEP 2 of the Download. This package has been tested within HEAsoft v6.26. The scripts should work with any version of the Swift calibrations files, but it is highly suggested to have the most updated versions in order to have reliable outputs. Follow [these](https://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/install.html) instructions to download and install the CALDB. Refer to [this](https://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/swift/) page to check that you currently have the most updated CALDB for UVOT.

# Using this Code

Consult the full Documentation (work in progress) for more details about how to run the code, interpreting  

## Preliminary steps

In order to use the package, the Swift 


# Contributions


