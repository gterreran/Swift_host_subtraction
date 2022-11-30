description='---Swift photometry---\n\nThis is a python wrapper of basic headas commands for the analysis of UVOT images.\n\n'

infile_help='If one argument is provide, simple aperture photometry will be performed. If two arguments are provided, template subtraction will be performed, with the second aegument being the template reference.\nThe input arguments can be either the Swift ObsID (ex. 00013174), or a single filter image (ex. sw00013174001uuu_sk.img.gz).\n A list of the above objects is also accepted, but not a list containing a combination of them.\n Both \'.img\' and \'.gz\' images are accepted.'

sn_reg='Region file indicating the coordinates of the SN. The format is the default region file from ds9 (eg. \'fk5;circle(00:00:00.000,+00:00:00.000,3")\'). The default radius is 3", but the photometry will be also compared with a 5" aperture. If this argument is not provided, the script will assume that a file "snbkg.reg" exist.'

bg_reg='Region file indicating the area where to measure the background counts. The format is the default region file from ds9 (eg. \'fk5;circle(00:00:00.000,+00:00:00.000,20")\'). This has to be an area free from contaminating sources. If this argument is not provided, the script will assume that a file "sn.reg" exist.'

det_limit='Signal-to-noise detection limit. A signal-to-noise above this value will be treated as true detection, while anything below will be treated as an upperlimit.'

ab_mag='Change the magnitude system to AB (default is Vega).'

filter='Selection of filters to be analysed. Acceptable filters: V, B, U, UVW1, UVM2, UVW2, OPT, UV, ALL,. Default is ALL, meaning that all the filters in present in the provided list will be analysed. Flags for optical only (OPT) and ultraviolet only (UV) are also available. A custum subset of filters can be provided instead. The format should be a comma separated list, with no spaces. Example: V,U,UVM2'

no_combine='Prevents to merge different extensions of a single file. If set True, this applies to all files, including the template.'
