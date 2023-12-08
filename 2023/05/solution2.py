from typing import List,Tuple


Transforms=Tuple[int,int,int]
Ranges=Tuple[int,int]

file="05/input"
data=[line.strip() for line in open(file)]


def transform(transforms: List[Transforms],ranges:List[Ranges]):
    for n,(init,l) in enumerate(ranges):
        find=False
        for d,s,r in transforms:
            if init>=s and init<s+r:
                find=True
                t=init+d-s
                if init+l<=s+r: #TODO review this <=
                    ranges[n]=(t,l)
                else:
                    consume=s+r-init
                    ranges[n]=(t,consume)
                    ranges.append((init+consume,l-consume))
        if not find:
            ss=list(x[1] for x in transforms)
            nexts=sorted(x for x in ss if x>init)
            if len(nexts)==0 or nexts[0]-init>l:
                ranges[n]=(init,l)
            else:
                next=nexts[0]
                consume=next-init
                ranges[n]=(init,consume)
                ranges.append((t+consume,l-consume))
                


        
    



seeds=[int(x) for x in data[0].split(": ")[1].split(" ")]

initial:List[Ranges]=[(seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]

init_maps=[n+1 for n, l in enumerate(data) if l==""]

maps=list(zip(init_maps,init_maps[1:]))
maps.append((init_maps[-1],len(data)+1))

for s,e in list(maps):
    transformations:List[Transforms]=[]
    for l in range(s+1,e-1):
        t=[int(x) for x in data[l].split(" ")]
        transformations.append((t[0],t[1],t[2]))
    transform(transformations,initial)

s=min([x[0] for x in initial])

if  file=="05/example" and s!=46:
    raise Exception  
print(s)

