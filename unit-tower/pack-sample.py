import numpy as np, gzip, struct, sys
buf=open('sample-unit.stl','rb').read()
n=struct.unpack_from('<I',buf,80)[0]; assert 84+50*n==len(buf)
rec=np.frombuffer(buf,dtype=np.dtype([('n','<f4',3),('v','<f4',9),('a','<u2')]),offset=84,count=n)
V=rec['v'].reshape(-1,3).copy()                       # n*3 vertices, original order
bits=V.view(np.uint32).reshape(-1,3)
# exact weld by bit pattern, numbering vertices in order of first appearance
key=bits[:,0].astype(np.uint64)*0  # placeholder
u,first,inv=np.unique(bits,axis=0,return_index=True,return_inverse=True); inv=inv.ravel()
order=np.argsort(first); rank=np.empty_like(order); rank[order]=np.arange(len(order))
idx=rank[inv].astype(np.uint32); P=V[first[order]]                      # float32 exact
assert np.array_equal(P[idx].view(np.uint32), bits)
nv=len(P); print('tris',n,'verts',nv)
def shuffle(a): b=np.frombuffer(a.tobytes(),dtype=np.uint8).reshape(-1,a.dtype.itemsize); return b.T.copy().tobytes()
# positions: per-axis delta of the uint32 bit patterns is poor; use byte shuffle of floats (column-major by axis)
pos_bytes=shuffle(np.ascontiguousarray(P.T).ravel())
# indices: delta from running max ("new vertex" codes are 0), zigzag, byte shuffle
d=np.empty(len(idx),dtype=np.int64); mx=-1; 
run=np.maximum.accumulate(idx.astype(np.int64)); prev=np.concatenate([[-1],run[:-1]])
d=prev+1-idx.astype(np.int64)            # 0 = next new vertex, k>0 = k-th most recent... (non-negative)
assert d.min()>=0
idx_bytes=shuffle(d.astype(np.uint32))
raw=b'UTU1'+struct.pack('<II',nv,n)+pos_bytes+idx_bytes
gz=gzip.compress(raw,9,mtime=0)
print('raw',len(raw),'gz',len(gz),'orig',len(buf),'orig gz',len(gzip.compress(buf,6)))
open('sample-unit.bin','wb').write(gz)
