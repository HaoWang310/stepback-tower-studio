import numpy as np
def H(rows): return np.array(rows,float).reshape(4,4)
G={
 'a':(H([-1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]),False),
 'b':(H([0,1,0,0, 1,0,0,0, 0,0,1,0, 0,0,0,1]),False),
 'c':(H([1,0,0,0, 0,0,-1,1, 0,-1,0,1, 0,0,0,1]),False),
 'd':(H([0,0,1,0, 0,-1,0,1, 1,0,0,0, 0,0,0,1]),True),   # swap_colors
 'e':(H([-1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]),False),
 'f':(H([1,0,0,0, 0,-1,0,0, 0,0,1,0, 0,0,0,1]),False),
 'g':(H([1,0,0,0, 0,1,0,0, 0,0,-1,0, 0,0,0,1]),False),
 'h':(H([1,0,0,0, 0,1,0,0, 0,0,-1,2, 0,0,0,1]),False)}
def texpr(s):
    S=[(np.eye(4),False)]
    for ch in reversed(s):
        M,sw=G[ch]; S=S+[(M@t,f^sw) for t,f in S]
        seen=set(); u=[]
        for t,f in S:
            k=tuple(np.round(t,6).ravel())
            if k not in seen: seen.add(k); u.append((t,f))
        S=u
    return S
def build(W,T,expr):
    P=[];TT=[];off=0
    for t,sw in texpr(expr):
        Q=W@t[:3,:3].T+t[:3,3]; flip=(np.linalg.det(t[:3,:3])<0)^sw
        P.append(Q); TT.append((T[:,::-1] if flip else T)+off); off+=len(Q)
    return np.concatenate(P),np.concatenate(TT)
