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
			ra = float(line.split()[0])
			dec = float(line.split()[1])
			radius = float(line.split()[2])/2. 
			pgc=str(line.split()[3]).replace(' ', '')
			clean=True
			rc3Obj= RC3(ra,dec,radius,pgc)
			ss = SkyServer()
			info = ss.surveyFieldConverter(rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius)
			print info
			r_mosaic = ""
			for i in info:
				r_mosaic=ss.getData('r',i[0],i[1],i[2])
			#Data after mosaicing
			rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,SDSS())
			rc3Obj.source_info(rfits,SDSS())
			import os
			os.system("sextractor  {}".format(r_mosaic))
			#Find total flux in image of one field in the raw data 
			catalog = open("test.cat",'r')
			mag_lst = []    	
			for line in catalog:
				line = line.split()
				if (line[0]!='#'):
			    	#MAG_ISOCOR      Corrected isophotal magnitude                   [mag]
			    	# in MGY conver to NMGY
					mag=float(line[10])*10**(9)
					mag_lst.append(mag)
			mag_rawdata.append(sum(mag_lst))


			print ("r_mosaic: {}".format(r_mosaic))
			import glob
			x= glob.glob("frame-*")
			print (x)
			print (x[0])
			#Find total flux in mosaiced image
			os.system("sextractor {}".format(x[0]))
			catalog = open("test.cat",'r')
			mag_lst = []    	
			for line in catalog:
			    line = line.split()
			    if (line[0]!='#'):
			    	#MAG_ISOCOR Corrected isophotal magnitude [mag]
			    	# in MGY convert to NMGY 
			    	# this was actually not necessary if we are not looking at SDSS raw data's FITS header
			        mag=float(line[10])*10**(9)
			        mag_lst.append(mag)
			mag_mosaic.append(sum(mag_lst))
		os.system("rm frame-*")
		print (mag_mosaic)
		print (mag_rawdata)
	print (mag_mosaic)
	print (mag_rawdata)