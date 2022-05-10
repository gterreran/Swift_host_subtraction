import argparse,os
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
    
    
    
    
    args = parser.parse_args()

    #check_heasoft()

    obj_file_list,tem_file_list=up.interpret_infile(args.infile)

    obj_file_list=up.sort_file_list(obj_file_list)
    tem_file_list=up.sort_file_list(tem_file_list)

    if not os.path.isdir('reduction'):
        os.mkdir('reduction')

    mag={}

    filt_list=up.sort_filters(args.filter)

    for filter in filt_list:

        filter_dir=os.path.join('reduction',filter)
        if not os.path.isdir(filter_dir):
            os.mkdir(filter_dir)

        print('Working on filter '+filter)
        template_exists=1

        print('Creating product file for the object.')
        prod_file=up.create_product(obj_file_list[filter],filter)

        print('Running uvotmaghist on the object image.\n')
        phot_file=up.run_uvotmaghist(prod_file,args.sn_reg,args.bg_reg,filter)




        if filter not in tem_file_list:
            print('No template provided for filter '+filter+'. Simple aperture photometry will be performed.\n\n')

            template_exists=0




        if template_exists:
            print('Creating product file for the template.')
            prod_file=up.create_product(tem_file_list[filter],filter,template=1)

            print('Running uvotmaghist on the template image.\n')
            templ_file=up.run_uvotmaghist(prod_file,args.sn_reg,args.bg_reg,filter)

            mag[filter]=up.extract_photometry(phot_file,args.ab,args.det_limit,templ_file)

        else:
            mag[filter]=up.extract_photometry(phot_file,args.ab,args.det_limit)

        print('\n')


    up.output_mags(mag)



