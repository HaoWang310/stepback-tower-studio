import numpy as np, sys
from manta import *
lv=int(sys.argv[1]) if len(sys.argv)>1 else 4
V,T,vo=initial()
for _ in range(lv): V,T,vo=refine(V,T,vo)
n=len(V)
cons=[[] for _ in range(n)]; fixed=np.zeros(n,bool)
for i,s in enumerate(vo):
    if s & {1,2,3}: fixed[i]=True           # 三条直线边固定
    elif 4 in s: cons[i]=[((1,0,1),1.0)]    # 自由边：在 x+z=1 平面上滑动
V,it,d=constrained_pp(V,T,cons,fixed,iters=200)
print('plateau: verts',n,'tris',len(T),'iters',it,'last move %.2e'%d,'area %.6f'%area(V,T))
np.savez('stage1_l%d.npz'%lv,V=V,T=T,vo=np.array([sorted(s) if s else [0] for s in vo],dtype=object))
