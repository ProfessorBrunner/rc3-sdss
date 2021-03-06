# Remember to remove rc3.db everytime you rerun this. Database files (.db) can only be instantiated once.
import sqlite3
conn = sqlite3.connect("rc3.db")
c = conn.cursor()
def tableCreate():
	#this can only be done once
	# create table and specify column, primary key is auto incremnting ID number
	c.execute("CREATE TABLE rc3 (ID INT , PGC INT,rc3_ra REAL, rc3_dec REAL,rc3_radius REAL,new_ra REAL,new_dec REAL,new_radius REAL, ufits TEXT, gfits TEXT, rfits TEXT ,ifits TEXT, zfits TEXT, best TEXT, low TEXT,in_SDSS_footprint BIT ,clean BIT, source_confused BIT, detect BIT,error INT,PRIMARY KEY(ID))")
	#Using BIT to represent boolean 1=True and False = 0
	
def dataEntry():
	survey = 'sdss'
	SURVEY = 'SDSS'
	n=0
	with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
		for line in f:
			rc3_ra = float(line.split()[0])
			rc3_dec = float(line.split()[1])
			rc3_radius = float(line.split()[2])/2. #diameter -->radius
			pgc=int(str(line.split()[3]).replace(' ', ''))

			with open("rc3_galaxies_outside_SDSS_footprint")as fp:
				in_SDSS_footprint=1
				for i in fp:  
					if (int(i.split()[3])==pgc):
						in_SDSS_footprint=0

			with open("rc3_galaxies_unclean")as unclean:
				clean=1
				for i in unclean: 
					if (int(i.split()[3])==pgc):
						clean=0

			with open("source_confused_rc3.txt")as conf:
				source_confused=0
				for i in conf: 
					if (int(i.split()[4])==pgc):
						source_confused=1
			
			with open("no_detected_rc3_candidate_nearby.txt")as detect:
				detect=1
				for i in detect: 
					if (int(i.split()[4])==pgc):
						detect=0
			# Updated Coordinate Information
			with open("rc3_updated.txt")as new:
				#if no updated value, use 0
				new_ra = 0
				new_dec = 0
				new_radius= 0
				for i in new: 
					line = i.split()
					if (int(line[5])==pgc):
						new_ra =float(line[2])
						new_dec = float(line[3])
						new_radius = float(line[4])
	
			# Path to Data Products
			#require new_ra,new_dec in their string form so that + and trailing 0 is not truncated
			if (in_SDSS_footprint==1):
				# Write only if covered by survey
				path = "{}/{}/".format(pgc,survey)
				# Scientifically calibrated fits are named in form
				#  "{}_{}_{}_{}.fits".format(survey.name,band,ra,dec)
				#  where ra,dec are new positional values passed into mosaic_band
				ufits = "{}{}_{}_{}.fits".format(path,SURVEY,'u',pgc)
				gfits = "{}{}_{}_{}.fits".format(path,SURVEY,'g',pgc)
				rfits = "{}{}_{}_{}.fits".format(path,SURVEY,'r',pgc)
				ifits = "{}{}_{}_{}.fits".format(path,SURVEY,'i',pgc)
				zfits = "{}{}_{}_{}.fits".format(path,SURVEY,'z',pgc)
				# -OUTFILE_NAME  {2}_{0}_{1}_BEST.tiff {7}".format(ra,dec,survey.name,
				best = "{}{}_{}_BEST.tiff ".format(path,SURVEY,pgc)
				low  =  "{}{}_{}_LOW.tiff ".format(path,SURVEY,pgc)
			else:
				ufits = ""
				gfits = ""
				rfits = ""
				ifits = ""
				zfits = ""
				best = ""
				low = ""
			# Storing new_ra, new_dec as float .
			#new_ra = float(new_ra)
			#new_dec = float(new_dec) 
			#new_radius = float(new_radius)

			# Error Information
			# 0 = no error
			# 1 = mosaicAll error
			# 2 = stiff error (no color images produced because g,r,i band not the same size)
			# 3 = strange error (when sql region search does not included the galaxy itself)
			# 4 = Montage image reprojection failure
			# 5= msubimage failure (cropping image outside of image field)
			error =0
			with open("mosaicAll_error")as e:
				for i in e: 
					line = i.split()
					if (int(line[3])==pgc):
						error=1

			with open("stiff_error.txt")as e:
				for i in e: 
					line = i.split()
					if (int(line[3])==pgc):
						error=2
						best = "No TIFF generated"
						low  =  "No TIFF generated"


			with open("strange_error.txt")as e:
				for i in e: 
					line = i.split()
					if (int(line[3])==pgc):
						error=3

			with open("failed_projection")as e:
				for i in e: 
					line = i.split()
					if (int(line[3])==pgc):
						error=4

			with open("failed_msubimage")as e:
				for i in e: 
					line = i.split()
					if (int(line[3])==pgc):
						error=5
			print (n)
			# print (n,ra,dec,radius,pgc,new_ra, new_dec, new_radius,ufits,gfits,rfits,ifits,zfits,best,low,in_SDSS_footprint,clean,error)
			# Prevent SQL injection and path quoting issue use this notation instead
 			c.execute("INSERT INTO rc3 (ID,PGC,rc3_ra,rc3_dec,rc3_radius,new_ra, new_dec, new_radius,ufits,gfits,rfits,ifits,zfits,best,low,in_SDSS_footprint,clean,source_confused,detect, error)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(n,pgc,rc3_ra,rc3_dec,rc3_radius,new_ra,new_dec,new_radius,ufits,gfits,rfits,ifits,zfits,best,low,in_SDSS_footprint,clean,source_confused, detect,error))
			n+=1
			conn.commit()
if __name__ == "__main__":
	print ("Create TABLE")
	tableCreate()
	print ("Enter Data") 
	dataEntry()
