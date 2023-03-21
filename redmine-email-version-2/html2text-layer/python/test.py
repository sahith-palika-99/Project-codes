v = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}

def numcompare(rom1,rom2):
     sum_rom1=0
     sum_rom2 = 0
     l1=len(rom1)
     l2=len(rom2)
     a=list(rom1)
     b=list(rom2)
     for i in range (0,l1):
          sum_rom1 = sum_rom1 + v[a[i]]
     for i in range (0,l2):
          sum_rom2 = sum_rom2 + v[b[i]]
     if sum_rom1 < sum_rom2:
          return True
     else:
          return False

print(numcompare("I", "I"))
print(numcompare("I", "II"))
print(numcompare("II", "I"))
print(numcompare("V", "IIII"))
print(numcompare("MDCLXV", "MDCLXVI"))
print(numcompare("MM", "MDCCCCLXXXXVIIII"))
