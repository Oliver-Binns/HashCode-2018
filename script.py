class Fleet:
    def __init__(self, patch, vehicles, bonus):
        self.patch = patch
        self.bonus = bonus
        self.vehicles = [Vehicle() for _ in range(vehicles)]
        self.rides = []  
    
    def schedule(self, ride):
        self.rides.append(ride)
    
    def arrange(self):
        self.rides.sort(key = lambda r: r.getTimeLength(), reverse=True)
        for ride in self.rides:
            available = list(filter(lambda v: v.freeDuringTime(ride), self.vehicles))
            available.sort(key = lambda v: v.distanceToRide(ride))
            for vehicle in self.vehicles:
                vehicle.addRide(ride)
                break
                
    def __repr__(self):
        str_rep = "";
        for vehicle in self.vehicles:
            str_rep += str(vehicle) + "\n"
        return str_rep

class Vehicle:
    def __init__(self):
        self.rides = []
        
    def getSurroundingRides(self, ride):
        if len(self.rides) == 0:
            return None, None
        if len(self.rides) == 1:
            if self.rides[0].end[2] <= ride.end[2]:
                return self.rides[0], None
            else:
                return None, self.rides[0]
                
        for i in range(1, len(self.rides)):
            prev = self.rides[i-1]
            next = self.rides[i]
            
            if prev.end[2] <= ride.start[2]:
                if next.start[2] >= ride.end[2]:
                    return prev, next
        
    def distanceToRide(self, ride):
        rides = self.getSurroundingRides(ride)
        x = 0
        y = 0
        
        if rides != None and rides[0] != None:
            x = rides[0].start[0]
            y = rides[0].start[1]
            
        x_diff = (x - ride.start[0])
        y_diff = (y - ride.start[1])
        return abs(x_diff) + abs(y_diff)
        
    def freeDuringTime(self, ride):
        rides = self.getSurroundingRides(ride)
        if rides == None:
            return True
        if rides[0] == None or rides[0].end[2] <= ride.start[2]:
            if rides[1] == None or rides[1].start[2] >= ride.end[2]:
                return True
        
    def addRide(self, ride):
        self.rides.append(ride)
        self.rides.sort(key = lambda r: r.start[2])

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
        
    def getTimeLength(self):
        return self.end[2] - self.start[2]
              
    def __repr__(self):
        return str(self._id)
        

def fetchInts(l):
    return map(
        lambda x: int(x),
        l.replace("\n", "").split(" ")
    )

def main(fn):
    i_f = open('input/'+fn+'.in', 'r')

    rows, cols, fleet, rides, bonus, _ = fetchInts(i_f.readline())
    fleet = Fleet((rows, cols), fleet, bonus)

    for index, line in enumerate(i_f):
        start_x, start_y, end_x, end_y, start_t, end_t = fetchInts(line)
        fleet.schedule(Ride(index, 
            (start_x, start_y, start_t), 
            (end_x, end_y, end_t)
        ))
    
    fleet.arrange()
    outname = i_f.name.replace("in", "out")
    o_f = open(outname, "w")
    o_f.write(str(fleet))
    
if __name__ == "__main__":
    files = ['a_example', 'b_should_be_easy', 'c_no_hurry', 'd_metropolis', 'e_high_bonus']
    #files = ['a_example']
    for fn in files:
        main(fn)
