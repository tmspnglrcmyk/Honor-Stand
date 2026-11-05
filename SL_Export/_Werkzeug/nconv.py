import sys, numpy as np
from PIL import Image
n=np.asarray(Image.open(sys.argv[1]).convert('RGB').resize((1024,1024)),float)/255-0.5
h=np.asarray(Image.open(sys.argv[2]).convert('L').resize((1024,1024)),float)
from scipy.ndimage import gaussian_filter
h=gaussian_filter(h,1.5)
dr=np.gradient(h,axis=0); dc=np.gradient(h,axis=1)
print(sys.argv[1].split('/')[-1], 'corrG_drow=%.3f corrR_dcol=%.3f'%(np.corrcoef(n[...,1].ravel(),dr.ravel())[0,1], np.corrcoef(n[...,0].ravel(),dc.ravel())[0,1]))
m=(np.abs(dr)>np.percentile(np.abs(dr),97))
print(' strong-gradient sign agreement G:', np.mean(np.sign(n[...,1][m])==np.sign(dr[m])).round(3), ' R(expect<0.5):', np.mean(np.sign(n[...,0][np.abs(dc)>np.percentile(np.abs(dc),97)])==np.sign(dc[np.abs(dc)>np.percentile(np.abs(dc),97)])).round(3))
