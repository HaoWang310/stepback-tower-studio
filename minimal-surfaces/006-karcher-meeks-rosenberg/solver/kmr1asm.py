import numpy as np
from kmr1 import patch, f0
def rotline(p,d):
    d=np.asarray(d,float); d/=np.linalg.norm(d); M=2*np.outer(d,d)-np.eye(3); return M, p-M@p
def refl(n,c):
    n=np.asarray(n,float); n/=np.linalg.norm(n); M=np.eye(3)-2*np.outer(n,n); return M, 2*c*n
def grid_tris(nu,nv):
    T=[]
    for i in range(nu-1):
        for j in range(nv-1):
            p=i*nv+j; T+=[(p,p+nv,p+1),(p+1,p+nv,p+nv+1)]
    return np.array(T)
def build(a,nx=12,ny=12,r0=0.001,cells=(2,2)):
    X,Z=patch(a,r0=r0,nx=nx,ny=ny); nu,nv,_=X.shape; P0=X.reshape(-1,3); T0=grid_tris(nu,nv)
    pi_=X[-1,-1]                     # f[i]
    li=(X[0,-1],X[-1,-1]-X[0,-1])     # 虚轴像：直线
    la=(X[-1,-1],X[-1,0]-X[-1,-1])    # 单位圆弧像：直线
    S=[(np.eye(3),np.zeros(3),False)]
    def apply(S,M,o):
        return S+[(M@m,M@t+o,not f) for m,t,f in S]
    S=apply(S,*rotline(li[0],li[1])); S=apply(S,*rotline(la[0],la[1]))
    S=apply(S,*refl((1,0,0),0.0)); S=apply(S,*refl((0,1,0),0.0))
    dx=2*pi_[0]*2; dy=2*np.pi
    PP=[];TT=[];o=0
    for i in range(cells[0]):
        for j in range(cells[1]):
            for m,t,f in S:
                PP.append(P0@m.T+t+np.array([i*dx,j*dy,0])); TT.append((T0[:,::-1] if f else T0)+o); o+=len(P0)
    return np.concatenate(PP),np.concatenate(TT),(dx,dy)
if __name__=='__main__':
    from scipy.spatial import cKDTree
    a=0.1; P,T,(dx,dy)=build(a,nx=40,ny=40)
    print('periods',dx,dy,'bbox',P.min(0).round(3),P.max(0).round(3))
    c=(P.min(0)+P.max(0))/2; s=np.abs(P-c).max(); Q=(P-c)/s
    V=np.load('pov1_a=0.1_V.npy')
    best=None
    import itertools
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1,-1],repeat=3):
            Qp=Q[:,perm]*np.array(sg); d,_=cKDTree(Qp).query(V)
            if best is None or d.mean()<best[0]: best=(d.mean(),d.max(),perm,sg)
    print('best mean %.2e max %.2e'%best[:2],'perm',best[2],'sign',best[3],'scale',s)
