import numpy as np
def clip(P,T,f):
    """保留 f<0 的部分，跨越边界的三角形按线性插值切开"""
    inside=f[T]<0; n_in=inside.sum(1)
    keep=T[n_in==3]; newP=[P]; newT=[keep]; base=len(P); extra=[]
    def ip(a,b):
        t=f[a]/(f[a]-f[b]); return P[a]+t[:,None]*(P[b]-P[a])
    for cnt in (1,2):
        S=T[n_in==cnt]
        if not len(S): continue
        I=inside[n_in==cnt]
        # 旋转使得特殊顶点在第 0 位：cnt=1 时 inside 那个，cnt=2 时 outside 那个
        sp=np.argmax(I if cnt==1 else ~I,1)
        R=np.stack([S[np.arange(len(S)),(sp+k)%3] for k in range(3)],1)
        a,b,c=R[:,0],R[:,1],R[:,2]
        pab=ip(a,b); pac=ip(a,c); m=len(S)
        i_ab=base+np.arange(m); i_ac=base+m+np.arange(m); base+=2*m; newP+=[pab,pac]
        if cnt==1: newT.append(np.stack([a,i_ab,i_ac],1))
        else: newT+= [np.stack([i_ab,b,c],1), np.stack([i_ab,c,i_ac],1)]
    P2=np.concatenate(newP); T2=np.concatenate(newT)
    used=np.unique(T2); m=-np.ones(len(P2),int); m[used]=np.arange(len(used))
    return P2[used],m[T2]
