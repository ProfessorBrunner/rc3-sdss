from sdss import SDSS
from rc3 import *
from skyserver import *
with open("sample.txt",'r') as f:
    mag_mosaic=[]
    mag_rawdata = []
    allObj=[]
    n = 0
    start=False
    for line in f:
        a = str(line)[0]
        if a[0] =="@": 
            start=True
            continue
        if (start):
            n +=1
            print (line.split())
	    ra = float(line.split()[0])
            dec = float(line.split()[1])
            new_ra = float(line.split()[2])
            new_dec = float(line.split()[3])
            radius = float(line.split()[4])
            pgc=str(line.split()[5]).replace(' ', '')
            clean=True
            rc3Obj= RC3(ra,dec,radius,pgc)
            ss = SkyServer()
            info = ss.surveyFieldConverter(rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius)
            for i in info:
                ss.getData('r',i[0],i[1],i[2])
            import glob
            # Selecting any one raw data field, no need to sum together the flux from all fields
            x= glob.glob("frame-*")
            print (x)
            print ("There are {} fields in this region".format(len(x)))
            if (len(x)==1):
                print "only one field in region"
            else:    
                print (x[0])
                import os
                # os.system("sextractor  {}".format(x[0]))
                os.system("sex {}".format(x[0]))
                k=-11 
                mag_lst = []   
                catalog = open("test.cat",'r')
                #Select 5 random sources to test
                coord = []
                import random
                for i in [random.randint(0,10) for i in range(5)]: 
                    for line in catalog:
                        line = line.split()
                        k=k+1
			print "i: {}".format(i)
			#print "k: {}".format(k)
                        if (line[0]!='#' and k==i):
                            ra = float(line[2])
                            dec = float(line[3])
                            mag=float(line[10])#*10**(9)
                            print ("[ra,dec]: {}".format([ra,dec]))
			    coord.append([ra,dec])
                            mag_lst.append(mag)
                            break
                print ("mag_lst: "+str(mag_lst))
		print ("coord: "+str(coord))
                mag_rawdata.append(sum(mag_lst))
                os.system("rm test.cat") #ensure no flow through
                #Data after mosaicing
                rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,SDSS())
                rc3Obj.source_info(rfits,SDSS()) #Generate data product
                #Find total flux in mosaiced image
                os.system("cp {0}/SDSS_r_{0}.fits .".format(rc3Obj.pgc))
                os.system("sextractor SDSS_r_{0}.fits".format(rc3Obj.pgc)) #run sextractor in the outer directory where the defaul.* files are stored
                catalog = open("test.cat",'r')
                mag_lst_r = []      
                for line in catalog:
                    line = line.split()
                    for i in coord:
			print "i: {}".format(i) 
			print "line2 : {} ".format(line[2])
			print "line3 : {} ".format(line[3])
                        if (line[0]!='#' and float(line[2])==i[0] and float(line[3])==i[1]):
                            #should be detected again inside mosaiced image.
                            print "match!"
                            mag_r = float(line[10]) 
                            mag_lst_r.append(mag_r)
                mag_mosaic.append(sum(mag_lst_r))
            # remove all the data from so that glob doesn't detect previous data files in the next run
            os.system("rm frame-*")
        print ("mag_mosaic= {}".format(mag_mosaic))
        print ("mag_rawdata= {}".format(mag_rawdata))
    print ("mag_mosaic= {}".format(mag_mosaic))
    print ("mag_rawdata= {}".format(mag_rawdata))
