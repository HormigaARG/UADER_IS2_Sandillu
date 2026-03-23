#!/usr/bin/python3
# Python program to display all the prime numbers within an interval

lower = 1 #Numeros desde donde se buscan los primos
upper = 500 #Numeros hasta donde se buscan los primos

print("Prime numbers between", lower, "and", upper, "are (ARCHIVO EDITADO):")

for num in range(lower, upper + 1):
   # all prime numbers are greater than 1
   if num > 1:
       for i in range(2, num):
           if (num % i) == 0:
               break
       else:
           print(num)
