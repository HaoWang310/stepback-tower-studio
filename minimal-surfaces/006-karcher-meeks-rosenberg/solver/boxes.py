import re,sys
def tokenize(s):
    i=0;n=len(s)
    while i<n:
        c=s[i]
        if c=='"':
            j=i+1
            while s[j]!='"':
                j+= 2 if s[j]=='\\' else 1
            yield ('str',s[i+1:j]); i=j+1
        elif c in '[]{},': yield (c,c); i+=1
        elif c.isspace(): i+=1
        else:
            j=i
            while j<n and s[j] not in '[]{},"' and not s[j].isspace(): j+=1
            yield ('sym',s[i:j]); i=j
def parse(toks,pos=0):
    t=toks[pos]
    if t[0]=='str': return ('S',t[1]),pos+1
    if t[0]=='{':
        items=[];pos+=1
        while toks[pos][0]!='}':
            e,pos=parse(toks,pos); items.append(e)
            if toks[pos][0]==',': pos+=1
        return ('L',items),pos+1
    if t[0]=='sym':
        head=t[1];pos+=1
        if pos<len(toks) and toks[pos][0]=='[':
            args=[];pos+=1
            while toks[pos][0]!=']':
                e,pos=parse(toks,pos); args.append(e)
                if toks[pos][0]==',': pos+=1
            return ('F',head,args),pos+1
        return ('Y',head),pos
    raise ValueError(t)
SUB={'\\[Pi]':'Pi','\\[Alpha]':'alpha','\\[Phi]':'phi','\\[Theta]':'theta','\\[ImaginaryI]':'I','\\[ExponentialE]':'E','\\[Rule]':'->','\\[Equal]':'==','\\[LessEqual]':'<=','\\[Infinity]':'Infinity','\\n':' ','\\[IndentingNewLine]':' ','\\[RuleDelayed]':':>','\\[Lambda]':'lambda','\\[Rho]':'rho','\\[Omega]':'omega','\\[Delta]':'delta','\\[Tau]':'tau','\\[Mu]':'mu','\\[Gamma]':'gamma','\\[Beta]':'beta','\\[Sigma]':'sigma','\\[Epsilon]':'eps','\\[Psi]':'psi','\\[Zeta]':'zeta','\\[CapitalOmega]':'Omega'}
def txt(e):
    k=e[0]
    if k=='S':
        s=e[1]
        for a,b in SUB.items(): s=s.replace(a,b)
        return s
    if k=='L': return ''.join(txt(x) for x in e[1])
    if k=='Y': return ''
    h,a=e[1],e[2]
    if h=='RowBox': return txt(a[0])
    if h=='SuperscriptBox': return '('+txt(a[0])+')^('+txt(a[1])+')'
    if h=='SubscriptBox': return txt(a[0])+'_'+txt(a[1])
    if h=='FractionBox': return '(('+txt(a[0])+')/('+txt(a[1])+'))'
    if h=='SqrtBox': return 'Sqrt['+txt(a[0])+']'
    if h in('StyleBox','TagBox','InterpretationBox','FormBox','TooltipBox','DynamicBox','ButtonBox','AdjustmentBox','TemplateBox'): return txt(a[0]) if a else ''
    if h=='UnderoverscriptBox': return txt(a[0])+'['+txt(a[1])+','+txt(a[2])+']'
    if h=='SubsuperscriptBox': return txt(a[0])+'_'+txt(a[1])+'^'+txt(a[2])
    if h=='OverscriptBox': return txt(a[0])
    return ''
def cells(path,types=('Input',)):
    s=open(path,errors='ignore').read()
    out=[]
    for m in re.finditer(r'Cell\[BoxData\[',s):
        j=m.start(); d=0;k=j
        while k<len(s):
            ch=s[k]
            if ch=='"':
                k+=1
                while s[k]!='"': k+= 2 if s[k]=='\\' else 1
            elif ch=='[': d+=1
            elif ch==']':
                d-=1
                if d==0: break
            k+=1
        c=s[j:k+1]
        mt=re.search(r'\]\s*,\s*"(\w+)"',c)
        typ=None
        try:
            toks=list(tokenize(c)); e,_=parse(toks)
            typ=e[2][1][1] if len(e[2])>1 and e[2][1][0]=='S' else None
            if typ in types: out.append(txt(e[2][0][2][0]))
        except Exception as ex: pass
    return out
if __name__=='__main__':
    for t in cells(sys.argv[1]): print('>>',t[:1500]); print()
