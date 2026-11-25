import numpy as np, zipfile, re, sys
from scipy.spatial import cKDTree
from scherk import build
from clip import clip
from povcam import transform, render
from PIL import Image
PI=np.pi
def window(h=2.0,half=1.5*PI,mode='swap'):
    P,T=build(nx=40,ny=40,cells=(1,1)); PP=[];TT=[];o=0
    for i in (-1,0,1):
        for j in (-1,0,1):
            PP.append(P+np.array([2*PI*i,2*PI*j,0])); TT.append(T+o); o+=len(P)
    P,T=np.concatenate(PP),np.concatenate(TT)
    P=P[:,[1,0,2]] if mode=='swap' else P*np.array([1,1,-1])
    if mode=='swap': T=T[:,::-1]   # 反射改变朝向
    else: T=T[:,::-1]
    for f in [P[:,0]-half,-P[:,0]-half,P[:,1]-half,-P[:,1]-half,P[:,2]-h,-P[:,2]-h]:
        pass
    for k in range(6):
        ax=k//2; sg=1 if k%2==0 else -1; lim=half if ax<2 else h
        P,T=clip(P,T,sg*P[:,ax]-lim)
    return P,T
if __name__=='__main__':
    ref=np.array(Image.open('/home/claude/c1/pov/scherk2a.png').convert('RGB')).astype(float)
    H,W=ref.shape[:2]
    # 原图像素分类：背景（白）、色 1（青）、色 2（橙）
    bg=(ref.min(2)>235); teal=(ref[...,1]>ref[...,0]+15)&~bg; sal=(ref[...,0]>ref[...,1]+10)&~bg
    for mode in ['swap','zflip']:
        P,T=window(mode=mode); Q=P/(1.5*PI)
        Q2=transform(Q,[(90,45,0),(-30,0,0)],scal=0.9,trans=(0,.1,0))
        img=render(Q2,T,W//4,H//4)
        im=np.array(Image.fromarray(((img+1)*100).astype(np.uint8)).resize((W,H),Image.NEAREST)).astype(int)//100-1
        sil=(im!=0); print(mode,'silhouette IoU %.3f'%((sil&~bg).sum()/((sil|~bg).sum())))
        for lab,(cp,cn) in {'+=teal':(teal,sal),'+=salmon':(sal,teal)}.items():
            ok=((im==1)&cp).sum()+((im==-1)&cn).sum(); tot=(cp|cn).sum(); print('   ',lab,'colour agree %.3f'%(ok/tot))
