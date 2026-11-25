import numpy as np
def R(ax,deg):
    t=np.radians(deg); c,s=np.cos(t),np.sin(t)
    return {'x':np.array([[1,0,0],[0,c,-s],[0,s,c]]),'y':np.array([[c,0,s],[0,1,0],[-s,0,c]]),'z':np.array([[c,-s,0],[s,c,0],[0,0,1]])}[ax]
def povrot(v):
    a,b,c=v; return R('z',c)@R('y',b)@R('x',a)
def transform(Q,rots,scal=1.0,trans=(0,0,0)):
    M=np.eye(3)
    for r in rots: M=povrot(r)@M
    return (Q*scal)@M.T+np.array(trans)
def render(P,T,W,H,angle=40,cam=-4.0):
    """POV 相机：位于 (0,0,cam)，看向 +z，水平视角 angle；返回每像素三角形朝向（+1/-1，0=背景）"""
    f=1/np.tan(np.radians(angle/2))
    Z=P[:,2]-cam; X=W/2+P[:,0]/Z*f*W/2; Y=H/2-P[:,1]/Z*f*W/2
    img=np.zeros((H,W),np.int8); zb=np.full((H,W),np.inf)
    tri=T; x0,x1,x2=X[tri[:,0]],X[tri[:,1]],X[tri[:,2]]; y0,y1,y2=Y[tri[:,0]],Y[tri[:,1]],Y[tri[:,2]]
    zz=Z[tri].mean(1)
    # 朝向：屏幕上的有向面积（POV 左手系，y 向下翻转后的符号）
    sgn=np.sign((x1-x0)*(y2-y0)-(x2-x0)*(y1-y0)).astype(np.int8)
    order=np.argsort(-zz)
    for i in order:
        xa,xb=int(max(0,np.floor(min(x0[i],x1[i],x2[i])))),int(min(W-1,np.ceil(max(x0[i],x1[i],x2[i]))))
        ya,yb=int(max(0,np.floor(min(y0[i],y1[i],y2[i])))),int(min(H-1,np.ceil(max(y0[i],y1[i],y2[i]))))
        if xb<xa or yb<ya: continue
        Xg,Yg=np.meshgrid(np.arange(xa,xb+1)+.5,np.arange(ya,yb+1)+.5)
        den=(y1[i]-y2[i])*(x0[i]-x2[i])+(x2[i]-x1[i])*(y0[i]-y2[i])
        if abs(den)<1e-12: continue
        w0=((y1[i]-y2[i])*(Xg-x2[i])+(x2[i]-x1[i])*(Yg-y2[i]))/den; w1=((y2[i]-y0[i])*(Xg-x2[i])+(x0[i]-x2[i])*(Yg-y2[i]))/den; w2=1-w0-w1
        m=(w0>=-1e-3)&(w1>=-1e-3)&(w2>=-1e-3)
        img[ya:yb+1,xa:xb+1][m]=sgn[i]   # 画家算法（远到近）
    return img
