#import sys

#5.1 Taxis. Write a script that finds which company is the cheapest as a function of the distance to travel.
def Taxis(km):
    company_A=4.80
    company_B=3.20
    
    km_A=1.15
    km_B=1.20
    
    price_A = company_A+(km*km_A)
    price_B = company_B+(km*km_B)
    
    if price_A > price_B:
        print("The cheapest company is company B, it costs:","%.2f" % price_B,"€")
    else:
        print("The cheapest company is company A, it costs:","%.2f" % price_A,"€")

#5.2 Kaprekar numbers

def Krapkear_numbers(N):
    for i in range(1,N+1):
        squared=i*i
        list_sqrt=list(str(squared))
        if "." in list_sqrt:
            list_sqrt.remove(".")
        for num in range(1,len(list_sqrt)):
            left_part = int(''.join(list_sqrt[:num]))
            right_part = int(''.join(list_sqrt[num:]))    
            if left_part and right_part != 0:
                if left_part+right_part == i:
                    print("Hourra!", i, "is a Kaprekar number!:", left_part,"+", right_part,"=",i,"!!")


km=34 #km to pay
#Taxis(km)

N=708
#Krapkear_numbers(N)

#5.3 RPN calculator

#Write a reverse Polish arithmetic expression evaluator 
#(See https://en.wikipedia.org/wiki/Reverse_Polish_notation).

#E.g. 3 4 * 5 - evaluate to 7.
expression= ["3", "4", "-", "5", "x"]

for i in range(len(expression)):
    medium_list=[]
    if not expression[i].isdigit():
        print("expr[i]", expression[i])
        if expression[i] == '-':
            result = int(expression[i-2]) - int(expression[i-1])
        elif i == '+':
            result = int(expression[i-2]) + int(expression[i-1])
        elif i == '/':
            result = int(expression[i-2]) / int(expression[i-1])
        elif i == 'x':
            result = int(expression[i-2]) * int(expression[i-1])
        else:
            print("Sorry, we didn't undertand the operant",i)
        print("result=",result)
        medium_list.append(result)
        medium_list.extend(expression[i+1:])
        print("med_list=",medium_list)

#5.4 RodRego simulator

#(only for very motivated people) Write a program that simulates a RodRego machine with 10 registers (http://sites.tufts.edu/rodrego/). The program is stored in a string or in a file that is read, then executed. The program must contain a function that, given the 10 initial values of the registers and the program returns the new register values after the END instruction is reached.
