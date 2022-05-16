# Swift Host Subtraction

This is a python package to perform aperture photometry on a single source in data from the Ultraviolet Optical Telescope ([UVOT](https://swift.gsfc.nasa.gov/about_swift/uvot_desc.html); [Roming et al. 2005](https://ui.adsabs.harvard.edu/abs/2005SSRv..120...95R/abstract)) on board the [Neil Gehrels Swift Observatory](https://swift.gsfc.nasa.gov) ([Gehrels et al. 2004](https://ui.adsabs.harvard.edu/abs/2004ApJ...611.1005G/abstract)). In particular, this package is oriented towards transient studies, as it can calculate template-subtracted luminosities if a template image, or a list of template images, is provided. 

This project is based greatly on [Peter J. Brown](https://pbrown801.github.io)'s work. He wrote the original code in IDL, and published it in his [PhD Thesis](https://etda.libraries.psu.edu/files/final_submissions/4865). The author of this script mainly translated that in python, adding some extra automations, controls, and features. The aperture photometry is done following the standard guidelines described in [Brown et al. (2009)](https://ui.adsabs.harvard.edu/abs/2009AJ....137.4517B/abstract). The image subtraction is performed following the prescriptions outlined in [Brown et al. (2014)](https://ui.adsabs.harvard.edu/abs/2014Ap%26SS.354...89B/abstract). See the full [Documentation](https://gterreran.github.io/Swift_host_subtraction/) (work in progress) for more details.

If you are interested in supernova light curves, check out also the Swift's Optical/Ultraviolet Supernova Archive ([SOUSA](https://pbrown801.github.io/SOUSA/)).

# HEAsoft software
The package uses [HEAsoft](https://heasarc.gsfc.nasa.gov/docs/software/heasoft/) commands like `uvotmaghist` and `uvotimsum`, which need to be installed separately. Refer to the [website](https://heasarc.gsfc.nasa.gov/docs/software/heasoft/download.html) for a standard installation. Be sure to select the Swift packages in the STEP 2 of the Download. This package has been tested within HEAsoft v6.26. The scripts should work with any version of the Swift calibrations files, but it is highly suggested to have the most updated versions in order to have reliable outputs. Follow [these](https://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/install.html) instructions to download and install the CALDB. Refer to [this](https://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/swift/) page to check that you currently have the most updated CALDB for UVOT.

# Installation

It is highly suggested (but not formally necessary) to first create and activate a separate new virtual environment. 
After cloning this repository, from the main folder simply run

```
python setup.py install
```


# Using this Code

Many things happen under the hood in this script, so to have a full grasp on what is actually happening, the user is invited to consult the full [Documentation](https://gterreran.github.io/Swift_host_subtraction/) (work in progress). 

## Preliminary steps

In order to use the package, the terminal needs to know where to find the HEAsoft commands related to UVOT. If you followed the installation available on the HEASARC website, you should just need to execute the following two lines of code

```
. path/to/your/headas-init.sh
source path/to/your/caldbinit.sh
``` 

Unless you have these 2 lines in your `.bashrc` (or equivalent), you will have to execute them every time you start a new terminal session.

To check that you have access to the UVOT scripts, and the system recognizes the CALDB folder, run

```
caldbinfo INST SWIFT XRT
```

The correct output should be 

```
** caldbinfo 1.0.2
... Local CALDB appears to be set-up & accessible
** caldbinfo 1.0.2 completed successfully
```

or with a more recent CALDB version.

## Running the code

Before running the code, the script needs to be given the exact coordinates of your transient, and of an empty region of sky without any contaminant source. The script recognizes the DS9 region format, usually saved with a `.reg` extension, which is basically a text file with the coordinates written in the following form

```
fk5;circle(15:03:49.97,+42:06:50.52,3")
```

A 3 arcseconds extraction is a sensible aperture extraction for Swift data, but does not necessarily reflect all the user cases. Therefore you can change the size of your aperture in your `.reg` file. The script will automatically extract photometry with a 5 arcseconds aperture as well in any case. The aperture of the background region instead can be much bigger, since the count rates will be averaged over the whole area. A sensible size is 20 arcseconds, but the most important aspect is that no sources must be present in this region.
The script assumes that the 2 region files are called `sn.reg` and `snbkg.reg` (the author studies mainly supernovae :-) ). If you use these names, the script will recognize them automatically, otherwise you will have to specify the alternative names using the appropriate flags. 

A common practice is to insert the path to all of the Swift images into a list. The images files are the format `sw[obsID][obsIdx]u[filter]_sk.img.gz` (you can unpack the images if you want, the script will recognize them anyway). If you are running the script from a top folder with all the observed epochs inside, you could easily create the list doing

```
ls */uvot/image/sw*_sk.img.gz > obj.lst
```

then all your images will be listed inside the `obj.lst` text file (the name and extension here are not important). You can do the same with your template images and create a second list, let's call it `templ.lst` for reference. 

Once you have the 2 `.reg` files and the lists, you can simply run

```
Swift_photom_host.py obj.lst templ.lst
```
The template file is not necessary to run the script. If no template list is provided, unsubtracted aperture photometry will be performed. You can access the script helper with the `-h` flag, which contains (hopefully) thorough descriptions of all the extra functionalities and features of the code, like different way to format the input.


## The output

The code will create a folder named `reduction` which will contain all the products of the extraction. In the top folder, the 2 `.dat` files contain the final magnitudes (by default in Vega, but you can change that with the `-a` flag) of the 2 extractions, the one with the aperture size provided by the user, and the one with a 5 arcsecond aperture. Then there will be a folder for every filter. These contain quicklook figures to check the goodness of the extraction. Check the full [Documentation](https://gterreran.github.io/Swift_host_subtraction/) (work in progress) for more info about all the product files.

*WARNING* - every time you run `Swift_photom_host`, the folder will be deleted and recreated, so if you need to compare different reductions, remember to rename that folder to avoid unwanted superscription.


# Contributions

# References

This code follows the guidelines and prescriptions described in [Brown et al. (2009)](https://ui.adsabs.harvard.edu/abs/2009AJ....137.4517B/abstract) and [Brown et al. (2014)](https://ui.adsabs.harvard.edu/abs/2014Ap%26SS.354...89B/abstract). So if you use this piece of software for your publication, you should at least cite these 2 papers.

If you also want to cite to this GitHub repository, you can.  

