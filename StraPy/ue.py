



#This is a link performance function derived from Indonesia'Highway Manual (MKJI 1997).
def lpr_idn(kapasitas,arus,freeflow=57):
    tf=1/freeflow*3600/1000
    return tf*(1+0.79*(arus/kapasitas)**3.24)

def bisection(qn,yn,xl=0,xr=1, delta=0.0001):
    n=0
    dn=yn-qn
    function=lambda x:qn-x*(dn)
    while abs((xr-xl)/2)> delta:
        n+=1
        x1=(xr+xl-delta)/2
        x2=(xr+xl+delta)/2
        f1=function(x1)
        f2=function(x2)
        if f1>f2:
            xr=x2
        elif f1<f2:
            xl=x1
        elif f1==f2:
            xr=x2
            xl=x1
        else:
            raise ValueError("Ada Kesalahan")
    print(f1)
    print(f2)
    print(n)
    return round((xr+xl)/2,3)

#Temporary list for routes.
def listtemp(routes, flow):
    saved = []
    
    for x, y in zip(routes,np.nditer(flow)):
        if isinstance(x, list):
            for number in x:
                saved.append([number,int(y)])
        elif x == None:
            continue
        else:
            saved.append([x,int(y)])
    return saved