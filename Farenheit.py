#Farenheit conversion

def F_to_C(temp):
    cel=(temp-32)*(5/9)
    return(cel)
    
def C_to_F(temp):
    far=temp*(9/5)+32
    return(far)

def K_to_F(temp):
    kel=(temp+459.67)*(5/9)
    return(kel)
    
def F_to_K(temp):
    far=temp*(9/5)-459.67
    return(far)

def R_to_F(temp):
    rank=temp+459.67
    return(rank)

def F_to_R(temp):
    far=temp-459.67
    return(far)

Farenheit=340
print(F_to_C(Farenheit))
print(F_to_K(Farenheit))
print(F_to_R(Farenheit))