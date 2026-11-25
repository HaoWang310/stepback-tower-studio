import numpy as np
np.seterr(all='ignore')
PI=np.pi
x_,w_=np.polynomial.legendre.leggauss(1)  # 占位
def ts():
    k=np.arange(-80,81)*0.045
    x=0.5*(1+np.tanh(PI/2*np.sinh(k))); w=0.5*0.045*PI/2*np.cosh(k)/np.cosh(PI/2*np.sinh(k))**2
    m=(x>0)&(x<1); return x[m],w[m]
SX,SW=ts()
def forms(z,a):
    # 第一象限内的连续分支：各因子主值对数（z 在上半平面）
    L=lambda c: np.log(z-c)
    # G = sqrt((z-a)(z-1/a)/((z+a)(z+1/a)))，dh = dz/z
    lg=0.5*(L(a)+L(1/a)-L(-a)-L(-1/a)); G=np.exp(lg)
    dh=1/z
    return 0.5*(1/G-G)*dh, 0.5j*(1/G+G)*dh, dh
def f0(W,a,base=1j):
    """从 base 沿直线积分到 W（W 在闭第一象限，避开 0）"""
    W=np.atleast_1d(W).astype(complex); P=base+(W[:,None]-base)*SX[None,:]
    F=forms(P,a); d=(W-base)[:,None]*SW[None,:]
    return np.stack([np.real((f*d).sum(1)) for f in F],1)
def patch(a,r0=0.001,nx=4,ny=4,facx=1):
    xs=np.unique(np.concatenate([np.linspace(np.log(r0),np.log(a),nx*facx+1),np.linspace(np.log(a),0,nx*facx+1)]))
    ys=np.linspace(1e-6,PI/2-1e-6,ny+1)
    Z=np.exp(xs[:,None]+1j*ys[None,:])
    X=f0(Z.ravel(),a).reshape(len(xs),len(ys),3)-f0(np.array([a+0j]),a)[0]
    return X,Z
if __name__=='__main__':
    a=0.1; X,Z=patch(a,nx=20,ny=20)
    def fit(C,name):
        c=C.mean(0); u,s,vt=np.linalg.svd(C-c)
        print(name,'line resid %.2e'%(s[1]/s[0]),'plane resid %.2e'%(s[2]/s[0]),'dir',vt[0].round(4),'normal',vt[2].round(4),'pt',c.round(4))
    fit(X[:,0],'real axis (θ=0)'); fit(X[:,-1],'imag axis (θ=π/2)'); fit(X[-1,:],'unit arc'); 
    ia=np.argmin(abs(np.exp(np.unique(np.concatenate([np.linspace(np.log(0.001),np.log(a),21),np.linspace(np.log(a),0,21)])))-a))
    fit(X[:ia+1,0],'real [r0,a]'); fit(X[ia:,0],'real [a,1]')
