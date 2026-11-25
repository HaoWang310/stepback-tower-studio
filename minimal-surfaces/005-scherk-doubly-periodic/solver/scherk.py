import numpy as np, itertools
from kmr1 import SX,SW
from kmr1asm import rotline, refl, grid_tris
np.seterr(all='ignore')
def forms(z):
    G=np.exp(0.5*(np.log(z+1)-np.log(z-1))); dh=1/z
    return 0.5*(1/G-G)*dh, 0.5j*(1/G+G)*dh, dh
def f0(W):
    W=np.atleast_1d(W).astype(complex); P=1j+(W[:,None]-1j)*SX[None,:]
    F=forms(P); d=(W-1j)[:,None]*SW[None,:]
    return np.stack([np.real((f*d).sum(1)) for f in F],1)
def patch(xmin=0.015,nx=30,ny=30,eps=1e-9):
    rs=np.exp(np.linspace(np.log(xmin),np.log(1-eps),nx+1)); ts=np.linspace(eps,np.pi-eps,ny+1)
    Z=rs[:,None]*np.exp(1j*ts[None,:])
    q=np.sqrt(Z-1)
    X=np.stack([-2*np.real(np.arctan(q/np.sqrt(Z+1))),-2*np.imag(np.arcsinh(q/np.sqrt(2))),np.log(np.abs(Z))],-1)
    return X
def frame(X):
    # 平移使 θ=0 与 θ=π 的边界曲线落在 x=0 / y=0 平面
    c0=X[:,0].mean(0); cp=X[:,-1].mean(0)
    def nrm(C):
        u,s,vt=np.linalg.svd(C-C.mean(0)); return vt[2]
    n0,npi=nrm(X[:,0]),nrm(X[:,-1]); print('normals',n0.round(4),npi.round(4))
    off=np.zeros(3)
    for n,c in [(n0,c0),(npi,c)  if False else (npi,cp)]:
        k=np.argmax(np.abs(n)); off[k]=-c[k]
    return X+off
def build(xmin=0.015,nx=30,ny=30,cells=(2,2)):
    X=patch(xmin,nx,ny); nu,nv,_=X.shape; P0=X.reshape(-1,3); T0=grid_tris(nu,nv)
    S=[(np.eye(3),np.zeros(3),False)]
    def apply(S,M,o): return S+[(M@m,M@t+o,not f) for m,t,f in S]
    S=apply(S,*rotline(X[-1,0],X[-1,-1]-X[-1,0]))   # 单位圆像（直线）
    S=apply(S,*refl((1,0,0),0)); S=apply(S,*refl((0,1,0),0))
    PP=[];TT=[];o=0
    for i in range(cells[0]):
        for j in range(cells[1]):
            for m,t,f in S:
                PP.append(P0@m.T+t+np.array([2*np.pi*i,2*np.pi*j,0])); TT.append((T0[:,::-1] if f else T0)+o); o+=len(P0)
    return np.concatenate(PP),np.concatenate(TT)
if __name__=='__main__':
    import zipfile,re
    from scipy.spatial import cKDTree
    P,T=build(nx=150,ny=150)
    print('bbox',P.min(0).round(4),P.max(0).round(4))
    s=zipfile.ZipFile('/home/claude/c1/pov/dummy.pov.zip').read('dummy.pov').decode(); s=s[:s.find('#declare MESHspheres')]
    nums=np.array(re.findall(r'<([-\d.e]+),\s*([-\d.e]+),\s*([-\d.e]+)>',s),float); V=np.unique(np.round(nums[0::2],4),axis=0)
    print('POV verts',len(V),'bbox',V.min(0),V.max(0))
    c=(P.min(0)+P.max(0))/2; sc=np.abs(P-c).max(); Q=(P-c)/sc
    C=Q[T].mean(1); tr=cKDTree(C); _,idx=tr.query(V,k=6)
    def ptd(p,a,b,c):
        n=np.cross(b-a,c-a); n/=np.linalg.norm(n,axis=-1,keepdims=True)+1e-30; return np.abs(((p-a)*n).sum(-1))
    D=np.min(np.stack([ptd(V,Q[T[idx[:,k],0]],Q[T[idx[:,k],1]],Q[T[idx[:,k],2]]) for k in range(6)],1),1)
    print('scale',sc,'dist mean %.2e p99 %.2e max %.2e'%(D.mean(),np.percentile(D,99),D.max()))
