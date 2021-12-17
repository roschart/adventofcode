
for t in range(3,20):
    VY=t
    VX=6
    y=0
    x=0
    while y > -10:
       y+=VY
       x+=VX
       VY-=1
       VX-=1
       if VX<0:
           VX=0

       print("%d "%(y), end="")
    print()