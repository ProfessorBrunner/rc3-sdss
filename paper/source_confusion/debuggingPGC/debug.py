from rc3 import RC3
from sdss import SDSS
pgc58 = RC3(0.184583333333,28.4013888889,0.0132388039385,58)
pgc58.mosaic_band('r',0.184583333333,28.4013888889,3*0.0132388039385,0.0132388039385,58,SDSS())
pgc58.source_info('SDSS_r_0.184583333333_28.4013888889.fits',SDSS())