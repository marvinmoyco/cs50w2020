#class Point():
#    def __init__(self,in1,in2):
#        self.x = in1
#        self.y = in2

#p = Point(2,8)
#print(f"The coordinates of p is {p.x} and {p.y} respectively.")



class Flight():
    def __init__(self,capacity):
        self.capacity = capacity
        self.passengers = []
    def add_passenger(self,name):
        if not self.open_seats():
            print("There are no more open seats.")
            return False
        self.passengers.append(name)
        return True
    def open_seats(self):
        return self.capacity - len(self.passengers)
flight = Flight(3)
people = ["Harry", "Ron", "Hermoine", "Ginny"]

for i in people:
    success = flight.add_passenger(i)
    if success:
        print(f"The person {i} has been added to the flight.")
    else:
        print(f"Please try again when there is available seats.")