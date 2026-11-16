def inline_filters(code):
    start=code.index('Param tune1')
    header,body=code[:start],code[start:]
    declarations=[]; result=[];count=0
    for line in body.splitlines():
        prefix=[]
        while 'lira_hp(' in line:
            pos=line.index('lira_hp('); depth=1; end=pos+8; comma=None
            for k in range(end,len(line)):
                c=line[k]
                if c=='(':depth+=1
                elif c==')':
                    depth-=1
                    if depth==0:end=k;break
                elif c==',' and depth==1:comma=k
            x=line[pos+8:comma];f=line[comma+1:end];n=f'hpf_{count}';count+=1
            declarations.append(f'History {n}_x(0), {n}_y(0);')
            prefix.append(f'{n}_a = clamp(1 - 6.28318530718 * ({f}) / samplerate, 0, 1); {n}_input = {x}; {n}_out = (1+{n}_a)*0.5*({n}_input-{n}_x)+{n}_a*{n}_y; {n}_x={n}_input; {n}_y={n}_out;')
            line=line[:pos]+n+'_out'+line[end+1:]
        result.extend(prefix+[line])
    return header+'\n'.join(declarations)+'\n'+'\n'.join(result)+'\n'
