.. _extraction:
#####################
Photometry Extraction
#####################

The following workflow describes how the photometry is extracted using `SwiftPhotom`.

==============
Pre-extraction
==============
#. **Input interpreting** - The first steps consists in interpreting the input provided by the User (see the Input types section for more details on what is an accepted input). A list of file is then created. 
#. **Checking aspect correction** - Each file is checked if an aspect correction has been executed on it or not. This is done by checking the ``ASPCORR`` label in the header of each extension. An aspect corrected file will have ``ASPCORR=DIRECT``. If this is not the case, a WARNING is printed out on the terminal, notifying that astrometry could be off. This does not necessarily mean that the astrometry will be wrong, but there is a higher chance it will be. The User must also be aware though the ``ASPCORR=DIRECT`` does not guarantee that the astrometry is going to be good either. Future improvement to the script will try to actively check and possibly correct the astrometry.
#. **Co-add multiple extensions** - Some UVOT exposures will be split in multiple extension inside the same file. In order to increase the signal to noise, the script will co-add all the extensions in each file. In this way, every file will corresponds to an epoch in the final photometry. The combined filed are saved in the ``mid-products`` folder for each filter inside the ``reduction`` directory. Some Users will want to prioritize the number of epochs over the signal to noise, so this step can be skipped with the ``--no_combine`` flag. Doing so, every extension in every file will count as an epoch in the final photometry.
#. **Creating a product file** - All the epochs are then appended to a single file, which will then contain all the epochs for a specific filter. This is saved as a ``.img`` file in each filter folder inside the ``reduction`` directory. This file will be redundant with all the raw data downloaded from the archive (as well as the co-added files created from the previous step), so although it is useful to have all the dataset for one filter gathered into a single file, this is definitely not memory efficient.



================
First extraction
================



====================
Template subtraction
====================

	#RAW_TOT_RATE -> Rate from the radius in sn.reg
	#RAW_STD_RATE -> Rate from 5" radius
	#COI_STD_FACTOR -> coincidence loss factor corrected for the aperture in sn.reg
	#COI_TOT_RATE = COI_STD_FACTOR * RAW_TOT_RATE -> total rate coincidence-loss-corrected
	#COI_SRC_RATE = COI_TOT_RATE-COI_BKG_RATE*SRC_AREA -> only source, background-subtracted

	#AP_COI_SRC_RATE = COI_SRC_RATE * AP_FACTOR
	#LSS_RATE = AP_COI_SRC_RATE / LSS_FACTOR -> large scale sensitivity
	#When photometry is done on coadded images the correction is not done, and a systematic uncertainty of 2.3% of the count rate is added in quadrature to the photometric error
	#SENSCORR_RATE = LSS_RATE * SENSCORR_FACTOR -> long-term sensitivity lost of the sensor