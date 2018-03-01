class Fleet:
    def __init__(self, patch, vehicles, bonus):
        self.patch = patch
        self.bonus = bonus
        self.vehicles = [Vehicle() for _ in range(vehicles)]
        self.rides = []  
    
    def schedule(self, ride):
        for vehicle in self.vehicles:
            if len(vehicle.rides) == 0:
                vehicle.addRide(ride)
                return
                
    def __repr__(self):
        str_rep = "";
        for vehicle in self.vehicles:
            str_rep += str(vehicle) + "\n"
        return str_rep

class Vehicle:
    def __init__(self):
        self.rides = []

    def addRide(self, ride):
        self.rides.append(ride)

    def __repr__(self):
        str_rep = str(len(self.rides))
        for ride in self.rides:
            str_rep += " " + str(ride)
        return str_rep

class Ride:
    def __init__(self, index, start, end):
        self._id = index
        self.start = start
        self.end = end
        
    def __repr__(self):
        return str(self._id)
        

def fetchInts(l):
    return map(
        lambda x: int(x),
        l.replace("\n", "").split(" ")
    )

def main():
    i_f = open('input/e_high_bonus.in', 'r')

    rows, cols, fleet, rides, bonus, _ = fetchInts(i_f.readline())
    fleet = Fleet((rows, cols), fleet, bonus)

    for index, line in enumerate(i_f):
        start_x, start_y, end_x, end_y, start_t, end_t = fetchInts(line)
        fleet.schedule(Ride(index, 
            (start_x, start_y, start_t), 
            (end_x, end_y, end_t)
        ))
    
    outname = i_f.name.replace("in", "out")
    o_f = open(outname, "w")
    o_f.write(str(fleet))
    
if __name__ == "__main__":
    main()
