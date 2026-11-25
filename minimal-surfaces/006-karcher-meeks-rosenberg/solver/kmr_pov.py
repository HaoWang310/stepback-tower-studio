import numpy as np, sys
from kmr1asm import build
from povcam import transform, render
from PIL import Image
def norm(P): c=(P.min(0)+P.max(0))/2; return (P-c)/np.abs(P-c).max()
def test(a,scal,trans_list,png):
    ref=np.array(Image.open(png).convert('RGB')).astype(int); H,W=ref.shape[:2]
    bg=ref.min(2)>235; small=np.array(Image.fromarray(~bg).resize((W//4,H//4)))
    rs=np.array(Image.fromarray(ref.astype(np.uint8)).resize((W//4,H//4))).astype(int)
    P,T,_=build(a,nx=12,ny=12); Q=norm(P)
    for ty in trans_list:
        img=render(transform(Q,[(-90,30,0),(-30,0,0)],scal=scal,trans=(0,ty,0)),T,W//4,H//4)
        s=img!=0; iou=(s&small).sum()/(s|small).sum()
        # 颜色：原图两色 meshcolor1 绿 (143,198,171) / meshcolor2 米 (244,212,181)；用 R-G 区分
        g=(rs[...,1]-rs[...,0]>-10)&small; b=(rs[...,0]-rs[...,1]>25)&small
        print(a,ty,'IoU %.3f'%iou,' +=green %.3f'%((((img==1)&g).sum()+((img==-1)&b).sum())/max(1,(g|b).sum())))
if __name__=='__main__':
    test(0.1,1.0,[0.1,0.15,0.2],'/home/claude/c5/pov1/a=0.1/mathematica.png')
