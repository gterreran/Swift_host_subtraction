import argparse,os,shutil
import SwiftPhotom.help as SH
import SwiftPhotom.uvot as up


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description=SH.description,\
         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("infile",nargs='+',help=SH.infile_help)
    parser.add_argument("-s", "--sn",dest="sn_reg",type=str,default='sn.reg',help=SH.sn_reg)
    parser.add_argument("-b", "--bg",dest="bg_reg",type=str,default='snbkg.reg',help=SH.bg_reg)
    parser.add_argument("-d", "--detection",dest="det_limit",type=float,default=3.,help=SH.det_limit)
    parser.add_argument("-a", "--ab",dest="ab",default=0, action='store_true',help=SH.ab_mag)
    parser.add_argument("-f", "--filter", dest="filter",default='ALL', help=SH.filter)
    parser.add_argument("--no_combine",dest="no_combine",default=0, action='store_true',help=SH.no_combine)
    
    
    
    
    args = parser.parse_args()

    ap_size = up.get_aperture_size(args.sn_reg)
    user_ap = ap_size+'_arcsec'

    #check_heasoft()

    obj_file_list,tem_file_list=up.interpret_infile(args.infile)

    obj_file_list=up.sort_file_list(obj_file_list)
    tem_file_list=up.sort_file_list(tem_file_list)

    if os.path.isdir('reduction'):
        shutil.rmtree('reduction')
    
    os.mkdir('reduction')

    mag={user_ap:[], '5_arcsec':[]}

    filt_list=up.sort_filters(args.filter)

    for filter in filt_list:

        if filter not in obj_file_list:
            continue

        filter_dir=os.path.join('reduction',filter)
        if not os.path.isdir(filter_dir):
            os.mkdir(filter_dir)

        print('Working on filter '+filter)
        template_exists=1

        print('Creating product file for the object.')
        prod_file=up.create_product(obj_file_list[filter],filter,no_combine=args.no_combine)

        print('Running uvotmaghist on the object image.\n')
        phot_file=up.run_uvotmaghist(prod_file,args.sn_reg,args.bg_reg,filter)




        if filter not in tem_file_list:
            print('No template provided for filter '+filter+'. Simple aperture photometry will be performed.\n\n')

            template_exists=0




        if template_exists:
            print('Creating product file for the template.')
            prod_file=up.create_product(tem_file_list[filter],filter,template=1,no_combine=args.no_combine)

            print('Running uvotmaghist on the template image.\n')
            templ_file=up.run_uvotmaghist(prod_file,args.sn_reg,args.bg_reg,filter)

            mag_filter=up.extract_photometry(phot_file,args.ab,args.det_limit,ap_size,templ_file)

        else:
            mag_filter=up.extract_photometry(phot_file,args.ab,args.det_limit,ap_size)

        for ap in mag_filter:
            mag[ap] = mag[ap] + mag_filter[ap]
        
        
        print('\n')


    up.output_mags(mag,ap_size)



