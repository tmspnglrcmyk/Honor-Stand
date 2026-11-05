import sys, numpy as np
from PIL import Image, ImageDraw
vt=[];F=[]
for l in open(sys.argv[1]):
    if l.startswith('vt '): vt.append([float(x) for x in l.split()[1:3]])
    elif l.startswith('f '):
        F.append([int(p.split('/')[1])-1 for p in l.split()[1:]])
vt=np.array(vt); R=2048; cnt=np.zeros((R,R),int)
for f in F:
    for k in range(1,len(f)-1):
        tri=[f[0],f[k],f[k+1]]
        P=np.array([(vt[i,0]*R,(1-vt[i,1])*R) for i in tri]); c=P.mean(0)
        d=P-c; L=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; P=c+d*np.clip((L-2.5)/L,0,1)
        x0,y0=np.floor(P.min(0)).astype(int); x1,y1=np.ceil(P.max(0)).astype(int)+1
        if x1-x0<1 or y1-y0<1: continue
        im=Image.new('L',(x1-x0,y1-y0),0); ImageDraw.Draw(im).polygon([(a-x0,b-y0) for a,b in P],fill=1)
        a=np.asarray(im); xs,ys=max(x0,0),max(y0,0); xe,ye=min(x1,R),min(y1,R)
        if xe>xs and ye>ys: cnt[ys:ye,xs:xe]+=a[ys-y0:ye-y0,xs-x0:xe-x0]
cov=(cnt>0).sum(); ov=(cnt>1).sum()
print(sys.argv[1].split('/')[-2], 'UV-Abdeckung %.1f%%, Überlappung %.2f%% der belegten Fläche'%(100*cov/R/R, 100*ov/max(cov,1)))
