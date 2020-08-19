import sys
try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error input")
    sys.exit(1)

try:
    result = x/y
except ZeroDivisionError:
    print("Error: Cannot divide by 0.")
    sys.exit(1)

print(f"The result of {x} / {y} is {result}")