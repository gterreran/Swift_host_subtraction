import sys,glob,os
import astropy.io.fits as pf
import SwiftPhotom.commands as sc
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time

ZP={'V':[17.88,0.01],'B':[18.98,0.02],'U':[19.36,0.02],'UVW1':[18.95,0.03],'UVM2':[18.54,0.03],'UVW2':[19.11,0.03]}
Vega={'V':-0.01,'B':-0.13,'U':1.02,'UVW1':1.51,'UVM2':1.69,'UVW2':1.73}

mjdref = 51910.0  #  jd reference used by swift

def sort_filters(_filt_list):
    full_filter_list=['V','B','U','UVW1','UVM2','UVW2']
    if _filt_list=='ALL':
        return full_filter_list
    elif _filt_list=='OPT':
        return ['V','B','U']
    elif _filt_list=='UV':
        return ['UVW1','UVM2','UVW2']
    else:
        out_filter_list=[]
        for _f in _filt_list.split(','):
            if _f.upper() not in full_filter_list:
                print('WARNING - Filter %s not recognized. Skipped.\n' % _f)
                continue
            out_filter_list.append(_f.upper())
        return out_filter_list


def interpret_infile(_infile):
    #file_list[0] will be the object file list
    #file_list[1] will be the template file list
    #creating a single list, I can fill them both
    #with a for loop, even if only the object is provided.
    file_list=[[],[]]
    
    for i in range(len(_infile)):
        if os.path.isfile(_infile[i]):
            file_exist=1
        else:
            file_exist=0
        
        if file_exist:
            if _infile[i].endswith('gz') or _infile[i].endswith('img'):
                file_list[i].append(_infile[i])
            else:
                with open(_infile[i]) as inp:
                    for line in inp:
                        ff=line.strip('\n')
                        if os.path.isfile(ff):
                            file_list[i].append(ff)
                        else:
                            print(ff+' not found. Skipped.')

        else:
            file_string=os.path.join(_infile[i]+'*','uvot','image','sw'+_infile[i]+'*_sk.img*')
            file_list[i]=glob.glob(file_string)
            if len(file_list[i])==0:
                print('Cannot interpret '+_infile[i]+'. Interrupt.')

    return file_list

def check_aspect_correction(_infile):
    hdu=pf.open(_infile)
    for i in range(len(hdu)):
        if hdu[i].name=='PRIMARY': continue
        #print(hdu[i].header['FRAMTIME'])
        if hdu[i].header['ASPCORR'] !='DIRECT':
            ext = hdu[i].header['EXTNAME']
            print('WARNING - Extension '+str(i)+ ' '+ext+' of '+_infile+' has not been aspect corrected. You should check the astrometry.')
    hdu.close()
    del hdu

def sort_file_list(_flist):
    out_file_list={}
    for file in _flist:
        filter=pf.getheader(file)['FILTER']
        if filter not in out_file_list:
            out_file_list[filter]=[]
        out_file_list[filter].append(file)

    return out_file_list

def combine(_list,_outfile):
    for i,img in enumerate(_list):
        if i==0:
            os.system('cp '+img+' '+_outfile)
        else:
            sc.fappend(img,_outfile)

def create_product(_flist,_filter,template=0):
    out_dir=os.path.join('reduction',_filter,'mid-products')
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    fig_dir=os.path.join('reduction'+_filter+'figures')
    if not os.path.isdir(fig_dir):
        os.mkdir(fig_dir)

    prod_list=[]
    for file in _flist:
        check_aspect_correction(file)
        hdu=pf.open(file)
        obsID=hdu[0].header['OBS_ID']
        out_file=os.path.join(out_dir,obsID+'_'+_filter+'.fits')
        if os.path.isfile(out_file):
            os.remove(out_file)
        framtime=[]

        for i in range(len(hdu)):
            if hdu[i].name=='PRIMARY': continue
            framtime.append(hdu[i].header['FRAMTIME'])
        if len(set(framtime))==1:
            sc.uvotimsum(file,out_file,_exclude='none')
            prod_list.append(out_file)
        else:
            print('WARNING - extensions of '+file+' have different FRAMTIMEs. Left unmerged.')
            for i in range(len(hdu)):
                if hdu[i].name=='PRIMARY': continue
                prod_list.append(file+'['+str(i)+']')
        hdu.close()
        del hdu

    if not template:
        prod_out_file= os.path.join('reduction',_filter,pf.getheader(file)['OBJECT']+'_'+_filter+'.img')
    else:
        prod_out_file= os.path.join('reduction',_filter,'templ_'+_filter+'.img')
    if os.path.isfile(prod_out_file):
        os.remove(prod_out_file)

    combine(prod_list,prod_out_file)

    return prod_out_file

def run_uvotmaghist(_prod_file,_sn_reg,_bg_reg,_filter):
    fig_dir=os.path.join('reduction',_filter,'figures')
    photo_out=_prod_file[:-4]+'_phot.fits'
    gif_out=os.path.join(fig_dir,_prod_file.split('/')[-1][:-4]+'_phot.gif')
    if os.path.isfile(photo_out):
        os.remove(photo_out)
    if os.path.isfile(gif_out):
        os.remove(gif_out)
    sc.uvotmaghist(_prod_file,_sn_reg,_bg_reg, photo_out,gif_out)

    return photo_out

def extract_photometry(_phot_file,_ab,_det_limit,_templ_file=None):

    ####
    #The default aperture of uvotmahist is 5 arcsec.
    #Corrections to retrieve this fluxes are provide.
    #We can compare the 2 apertures.
    ####
    
    if _templ_file!=None:
        template=1

    if _ab==1:
        Vega_corr={'V':0,'B':0,'U':0,'UVW1':0,'UVM2':0,'UVW2':0}
    else:
        Vega_corr=Vega

    col={'3_arcsec':'b','5_arcsec':'r'}
    mag={'3_arcsec':{'p':[],'u':[]},'5_arcsec':{'p':[],'u':[]}}

    BCR_temp={}
    BCRe_temp={}

    for i,file in enumerate([_templ_file,_phot_file]):
        if file==None:
            #In case there is no template, nothing will be subtracted.
            BCR_temp={'3_arcsec':0.,'5_arcsec':0.}
            BCRe_temp={'3_arcsec':0.,'5_arcsec':0.}
            template=0
            continue
    
        hdu=pf.open(file)
        dd=hdu[1].data
        filter=dd['FILTER'][0]
        hdu.close()

        SC=dd['SENSCORR_FACTOR']

        #These is the count rate for 3arcsec
        S3BCR=dd['COI_SRC_RATE']*SC
        
        #adding 3% error on count rate of the source in quadrature to poission error
        if template and i==1:
            S3BCRe=np.sqrt((dd['COI_SRC_RATE_ERR'])**2+(S3BCR*0.03)**2)
        else:
            S3BCRe=dd['COI_SRC_RATE_ERR']
        
        #These is the count rate for 3arcsec
        S5CR=dd['RAW_STD_RATE']*dd['COI_STD_FACTOR']
        S5CRe=dd['RAW_STD_RATE_ERR']*dd['COI_STD_FACTOR']
        S5BCR=((dd['RAW_STD_RATE'] *dd['COI_STD_FACTOR'] * SC) - (dd['COI_BKG_RATE'] * SC * dd['STD_AREA']))
        if template and i==1:
            S5BCRe=np.sqrt((S5CRe)**2+(S5CR*0.03)**2+(dd['COI_BKG_RATE_ERR']*dd['STD_AREA'])**2)
        else:
            S5BCRe=np.sqrt((S5CRe)**2+(dd['COI_BKG_RATE_ERR']*dd['STD_AREA'])**2)
        
        
        
        fig_dir=os.path.join('reduction',filter,'figures')
        fig=plt.figure()
        ax=fig.add_subplot(111)
        
        if template:
            fig_mag=plt.figure()
            ax_mag=fig_mag.add_subplot(111)
        
        fig_sub=plt.figure()
        ax_sub=fig_sub.add_subplot(111)

        for BCR,BCRe,label in [[S3BCR,S3BCRe,'3_arcsec'] , [S5BCR,S5BCRe,'5_arcsec']]:
        



            if i==0:
                epochs=range(len(BCR))
                ax.errorbar(epochs,BCR,yerr=BCRe,marker='o', color=col[label],label=label)
            
                #weighed avarage the template fluxes
                BCR_temp[label]=np.sum(BCR/BCRe**2)/np.sum(1./BCRe**2)
                BCRe_temp[label]=np.sqrt(1./np.sum(1./BCRe**2))
                
                xx=[0,len(BCR)-1]
                ax.plot(xx,[BCR_temp[label]]*2,color=col[label],lw=2)
                ax.fill_between(xx, [BCR_temp[label]+BCRe_temp[label]]*2,  [BCR_temp[label]-BCRe_temp[label]]*2, color=col[label],lw=2, alpha=0.2)
            
                ax.set_xlabel('Epoch')
            
                print('Galaxy count rates in '+label[0]+'"aperture: %.3f +- %.3f' %(BCR_temp[label],BCRe_temp[label]))

            else:
                all_point=[]
                mjd=mjdref+(dd['TSTART']+dd['TSTOP'])/2./86400.
                ax.errorbar(mjd,BCR,yerr=BCRe,marker='o', color=col[label],label=label)
                
                ax.set_xlabel('MJD')
                
                
                #subtract galaxy, propogate error
                BCGR=(BCR-BCR_temp[label])
                BCGRe=np.sqrt((BCRe)**2+(BCRe_temp[label])**2)

                if label=='3_arcsec':
                    # apply aperture correction
                    BCGAR=BCGR*dd['AP_FACTOR']
                    BCGARe=BCGRe*dd['AP_FACTOR_ERR']
                    BCAR=BCR*dd['AP_FACTOR']
                    BCARe=BCRe*dd['AP_FACTOR_ERR']
                else:
                    BCGAR=BCGR
                    BCGARe=BCGRe
                    BCAR=BCR
                    BCARe=BCRe
                
                if template:
                    #Not subtracted magnitudes
                    or_mag=-2.5*np.log10(BCAR)+ZP[filter][0]-Vega_corr[filter]
                    or_mage=np.sqrt(((2.5/np.log(10.))*((BCRe/BCAR)))**2+ZP[filter][1]**2)
                
                    mag_host=-2.5*np.log10(BCR_temp[label])+ZP[filter][0]-Vega_corr[filter]
                    mag_hoste=np.sqrt(((2.5/np.log(10.))*((BCRe_temp[label]/BCR_temp[label])))**2+ZP[filter][1]**2)
                
                    ax_mag.errorbar(mjd,or_mag,yerr=or_mage,marker='o', color=col[label],label=label)

                    ax_mag.plot([min(mjd),max(mjd)],[mag_host]*2,color=col[label],lw=2)
                    ax_mag.fill_between([min(mjd),max(mjd)], [mag_host+mag_hoste]*2,  [mag_host-mag_hoste]*2, color=col[label],lw=2, alpha=0.2)

                
            



                # determine significance/3 sigma upper limit
                BCGARs=BCGAR/BCGARe
                BCGAMl=(-2.5*np.log10(3.*BCGARe))+ZP[filter][0]-Vega_corr[filter]

                #convert rate,err to magnitudes"
                for j,CR in enumerate(BCGARs):
                    if BCGARs[j]>=_det_limit:
                        BCGAM=-2.5*np.log10(BCGAR[j])+ZP[filter][0]-Vega_corr[filter]
                        BCGAMe=np.sqrt(((2.5/np.log(10.))*((BCGARe[j]/BCGAR[j])))**2+ZP[filter][1]**2)
                        mag[label]['p'].append([mjd[j],BCGAM,BCGAMe])
                        print('%.2f\t%.3f\t%.3f' % (mjd[j],BCGAM,BCGAMe))
                    else:
                        BCGAM=BCGAMl[j]
                        BCGAMe=0.2
                        mag[label]['u'].append([mjd[j],BCGAM,BCGAMe])
                        print('%.2f\t> %.3f (%.2f)' % (mjd[j],BCGAM,np.fabs(BCGARs[j])))
                    all_point.append([mjd[j],BCGAM])
                    
                if len(mag[label]['p'])>0:
                    xx,yy,ee=zip(*sorted(mag[label]['p']))
                    ax_sub.errorbar(xx,yy,yerr=ee,marker='o', color=col[label],label=label,ls='')

                
                if len(mag[label]['u'])>0:
                    xx,yy,ee=zip(*sorted(mag[label]['u']))
                    ax_sub.errorbar(xx,yy, yerr=[-1.*np.array(ee),[0]*len(ee)], uplims=True, marker='o', color=col[label],label=label,ls='')

                xx,yy=zip(*sorted(all_point))
                ax_sub.plot(xx,yy, color=col[label])
                
                

                print('\n'+label[0]+'"aperture done!\n')
        
        if i==1:
        
            ax_sub.set_title(file.split('/')[-1])
            ax_sub.set_xlabel('MJD')
            ax_sub.set_ylabel('Mag')
            ax_sub.invert_yaxis()
            ax_sub.legend()
            
            
            out_fig=os.path.join(fig_dir,file.split('/')[-1][:-5]+'_mag_final.png')
            if os.path.isfile(out_fig):
                os.remove(out_fig)

            fig_sub.savefig(out_fig)
            del fig_sub
            del ax_sub
            
            
            if template:
                ax_mag.set_title(file.split('/')[-1])
                ax_mag.set_xlabel('MJD')
                ax_mag.set_ylabel('Mag')
                ax_mag.invert_yaxis()
                ax_mag.legend()


                out_fig=os.path.join(fig_dir,file.split('/')[-1][:-5]+'_mag.png')
                if os.path.isfile(out_fig):
                    os.remove(out_fig)

                fig_mag.savefig(out_fig)
                del fig_mag
                del ax_mag

        ax.set_title(file.split('/')[-1])
        ax.set_ylabel('Coincident-corrected count rates')
        ax.legend()
        
        

        out_fig=os.path.join(fig_dir,file.split('/')[-1][:-5]+'_counts.png')
        if os.path.isfile(out_fig):
            os.remove(out_fig)

        fig.savefig(out_fig)
        plt.close()
        del fig
        del ax
        


    return mag


def output_mags(_mag):

    #This is neither clever nor fast, but it works.

    out_mag={}
    epochs=[]
    for ap in ['3_arcsec','5_arcsec']:
        #for f in ['UVW2','UVM2','UVW1','U','B','V','R','I']:
        for f in _mag:
            for t in _mag[f][ap]:
                for el in _mag[f][ap][t]:
                    m=round(el[0],2)
                    if m not in epochs:
                        out_mag[m]={}
    
        for m in out_mag:
            for f in ['UVW2','UVM2','UVW1','U','B','V','R','I']:
                if f not in out_mag[m]:
                    out_mag[m][f]={'p':(9999,0),'u':(9999,0)}

        for f in _mag:
            for t in _mag[f][ap]:
                for el in _mag[f][ap][t]:
                    m=round(el[0],2)
                    out_mag[m][f][t]=(el[1], el[2])
        

        tag={'p':' 1','u':'-1'}


#        for e in _mag:
#            for f in _mag[e]:
#                for t in _mag[e][f]:
#                    #print e,f,t
#                    pass

        #'A':'UVW1','D':'UVM2','S':'UVW2'

        eps=sorted([el for el in out_mag])

        snlc =open('reduction/'+ap+'snlc.dat','w')
        snlc.write('      Date        JD            S           D           A            S notes\n')
        for j in eps:
            for t in ['p','u']:
                if len(list(set([out_mag[j][ff][t][1] for ff in ['UVW2','UVM2','UVW1']])))==1: continue
                date=''.join(Time(j, format='mjd').iso.split()[0].split('-'))
                snlc.write("%s %.2f"%(date,j))
                for f in ['UVW2','UVM2','UVW1']:
                    if out_mag[j][f][t][0]==9999:
                        snlc.write('   9999  0.00 ')
                    else:
                        snlc.write(' %6.2f %5.2f '%(abs(out_mag[j][f][t][0]),out_mag[j][f][t][1]))
                snlc.write(' '+tag[t]+' Swift \n')

        snlc.write('\n')

        snlc.write('      Date        JD            U           B           V            R          I           S  notes\n')
        for j in eps:
            for t in ['p','u']:
                if len(list(set([out_mag[j][ff][t][1] for ff in 'UBVRI'])))==1: continue
                date=''.join(Time(j, format='mjd').iso.split()[0].split('-'))
                snlc.write("%s %.2f"%(date,j))
                for f in 'UBVRI':
                    if out_mag[j][f][t][0]==9999:
                        snlc.write('   9999  0.00 ')
                    else:
                        snlc.write(' %6.2f %5.2f '%(abs(out_mag[j][f][t][0]),out_mag[j][f][t][1]))
                snlc.write(' '+tag[t]+' Swift \n')
        snlc.close()
        del snlc

