a=100
b=100
largestPal=0

def IsPalindrome(n):
    possiblePal=str(n)
    if possiblePal==possiblePal[::-1]:
        return 1
    else:
        return 0
for a in range(100,1000):
    for b in range(100,1000):
        if IsPalindrome(a*b)==1 and (a*b)>largestPal:
            largestPal=(a*b)
print(largestPal)
