def countNumbersWith1(n) :
    result = 0
# initialize result
# One by one compute sum of digits
# in every number from 1 to n
    for x in range(1, n + 1):
         if(has1(x) == True):
           result = result + 1
         return result
# A utility function to compute sum
# of digits in a given number x
def has1(x):
    while (x != 0):
        if (x%10 == 1):
          return True
        x = x //10
        return False



# Driver Program
n = int(input("enter a number:"))
print ("Count of numbers from 1 to ", n, " that have 1 as a a digit is ",
countNumbersWith1(n))
