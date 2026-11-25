import numpy as np, sys
from manta import conjugate
from trbase import area
lv=int(sys.argv[1])
d=np.load('stage1_l%d.npz'%lv,allow_pickle=True); V,T,vo=d['V'],d['T'],[set(x)-{0} for x in d['vo']]
c3=[i for i,s in enumerate(vo) if s=={3,4}][0]
W=conjugate(V,T,1)
W[:,2]-=W[:,2].min(); W[:,0]-=W[:,0].min(); W[:,1]-=(W[:,1]-W[:,0]).min()
W/= (W[c3,1]+W[c3,2])
P={1:[((1,0,0),0.0)], 2:[((0,1,1),1.0)], 3:[((-1,1,0),0.0)], 4:[((1,0,-1),0.0),((0,1,0),0.5)]}
for i,s in enumerate(vo):
    if not s: continue
    C=[c for e in sorted(s) for c in P[e]]
    N=np.array([c[0] for c in C],float); b=np.array([c[1] for c in C])
    # 最小改动投影到所有约束的交集：p' = p - N^T (N N^T)^+ (N p - b)
    p=W[i]; W[i]=p-N.T@np.linalg.pinv(N@N.T)@(N@p-b)
print('area',area(W,T),'bbox',W.min(0).round(4),W.max(0).round(4))
np.savez('manta_l%d.npz'%lv,W=W,T=T,vo=d['vo'])
