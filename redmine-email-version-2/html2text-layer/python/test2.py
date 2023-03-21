s=[1,5,10,25,100,500]
value=int(input('Enter a number'))
ans=[]
i=len(s)-1
while (i>=0):
    while(value >= s[i]):
        value=value-s[i]
        ans.append(s[i])
    i=i-1
print(len(ans))
