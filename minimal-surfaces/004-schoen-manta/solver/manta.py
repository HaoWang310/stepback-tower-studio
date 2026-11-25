import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla
from trbase import refine, cot_laplacian, area
s2=np.sqrt(2)
alpha=0.203415322692705
P0={1:(0,0,0),2:(1,0,0),3:(1-alpha,2*alpha-1,alpha),4:(0,alpha,alpha)}
# 边：1: 2→1，2: 1→4，3: 4→3（直线，固定）；4: 3→2 在平面 x+z=1 上自由滑动
# 面 1: -4 -3 -2 -1 → 顶点环 2→3→4→1
loop=[2,3,4,1]
edge_of_pair={(2,3):4,(3,4):3,(4,1):2,(1,2):1}
def initial():
    V=[np.array(P0[i],float) for i in loop]; c=np.mean(V,0); V=np.array(V+[c])
    T=np.array([(i,(i+1)%4,4) for i in range(4)])
    vo=[]
    for i,vid in enumerate(loop):
        s=set()
        for (a,b),e in edge_of_pair.items():
            if vid in (a,b): s.add(e)
        vo.append(s)
    vo.append(set())
    return V,T,vo
def basis(constraints):
    """constraints: list of (normal, offset)；返回可动方向的正交基"""
    if not constraints: return np.eye(3)
    Nm=np.array([n for n,_ in constraints],float)
    u,s,vt=np.linalg.svd(Nm); r=(s>1e-9).sum()
    return vt[r:].T  # 3 x dof
def constrained_pp(V,T,cons,fixed,iters=100,tol=1e-10):
    """cons[i]: 平面约束列表；fixed[i]: 是否固定。每步解余切能量的约束最小化（Pinkall–Polthier）"""
    n=len(V)
    for it in range(iters):
        L=cot_laplacian(V,T)                       # n x n
        cols=[];rows=[];vals=[];m=0;offs=[]
        for i in range(n):
            if fixed[i]: offs.append(None); continue
            B=basis(cons[i]); offs.append((m,B))
            for d in range(B.shape[1]):
                for k in range(3):
                    if abs(B[k,d])>0: rows.append(3*i+k); cols.append(m+d); vals.append(B[k,d])
            m+=B.shape[1]
        Bm=sp.coo_matrix((vals,(rows,cols)),shape=(3*n,m)).tocsr()
        L3=sp.kron(L,sp.eye(3)).tocsr()
        x=V.reshape(-1)
        # 新位置 = x + Bm q；最小化 (x+Bq)^T L3 (x+Bq)
        A=(Bm.T@L3@Bm).tocsc(); b=-(Bm.T@(L3@x))
        q=sla.spsolve(A,b)
        Vn=(x+Bm@q).reshape(-1,3)
        # 投影回平面（数值修正）
        for i in range(n):
            for nrm,off in cons[i]:
                nrm=np.asarray(nrm,float); k=np.dot(nrm,nrm)
                Vn[i]-= (Vn[i]@nrm-off)/k*nrm
        d=np.abs(Vn-V).max(); V=Vn
        if d<tol: break
    return V,it,d
def conjugate(V,T,sign=1):
    L=cot_laplacian(V,T); n=len(V); Vs=np.zeros_like(V)
    for k in range(3):
        u=V[:,k]; rhs=np.zeros(n)
        for (a,b,c) in [(0,1,2),(1,2,0),(2,0,1)]:
            i,j,kk=T[:,a],T[:,b],T[:,c]; np.add.at(rhs,i,(u[kk]-u[j])/2)
        A=L.tolil(); A[0,:]=0; A[0,0]=1; rhs[0]=0
        Vs[:,k]=sla.spsolve(A.tocsc(),rhs)
    return sign*Vs
