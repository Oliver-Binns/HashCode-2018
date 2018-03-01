def lop(vehicles, rides, ts, bonus):
    max_vehicle = vehicles[0]
    max_ride = rides[0]
    max_lop = 0
    
    for vehicle in vehicles:
        for ride in rides:
            vehicleToRideDistance = distanceCalc(vehicle.loc(), ride.start)
    
            temp_lop = ride.getDistance() - vehicleToRideDistance + bonus if ((vehicleToRideDistance + ts) <= ride.start[2]) else 0
            
            if (ts + vehicleToRideDistance + ride.getDistance()) >= ride.end[2]:
                temp_lop = 0
            
            if temp_lop > max_lop:
                max_lop = temp_lop
                max_vehicle = vehicle
                max_ride = ride
            
    return max_vehicle, max_ride
            
class Fleet:
    def __init__(self, patch, vehicles, bonus):
        self.patch = patch
        self.bonus = bonus
        self.vehicles = [Vehicle() for _ in range(vehicles)]
        self.rides = []  
    
    def schedule(self, ride):
        self.rides.append(ride)
    
    def arrange(self, timesteps):
        timestep = 0
        
        for ts in range(timesteps):
            availableVehicles = list(filter(lambda v: v.availableAt(ts), self.vehicles))
            
            while len(self.rides) > 0 and len(availableVehicles) > 0:
                vehicle, ride = lop(availableVehicles, self.rides, ts, self.bonus)
                
                vehicle.addRide(ride)
                availableVehicles.remove(vehicle)
                self.rides.remove(ride)
                         
    def __repr__(self):
        str_rep = "";
        for vehicle in self.vehicles:
            str_rep += str(vehicle) + "\n"
        return str_rep

class Vehicle:
    def __init__(self):
        self.rides = []
                    
    def loc(self):
        if len(self.rides) == 0:
            return 0, 0
        return self.rides[-1].end
        
    def availableAt(self, timestep):
        if len(self.rides) == 0:
            return True
        if self.rides[-1].end[2] <= timestep:
            return True
        return False
        
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
        
    def getDistance(self):
        return distanceCalc(self.start, self.end)
    
    def getTimeLength(self):
        return self.end[2] - self.start[2]
              
    def __repr__(self):
        return str(self._id)
        

def distanceCalc(start, end):
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
    return x + y

def fetchInts(l):
    return map(
        lambda x: int(x),
        l.replace("\n", "").split(" ")
    )

def main(fn):
    i_f = open('input/'+fn+'.in', 'r')

    rows, cols, fleet, rides, bonus, timesteps = fetchInts(i_f.readline())
    fleet = Fleet((rows, cols), fleet, bonus)

    for index, line in enumerate(i_f):
        start_x, start_y, end_x, end_y, start_t, end_t = fetchInts(line)
        fleet.schedule(Ride(index, 
            (start_x, start_y, start_t), 
            (end_x, end_y, end_t)
        ))
    
    fleet.arrange(timesteps)
    outname = i_f.name.replace("in", "out")
    o_f = open(outname, "w")
    o_f.write(str(fleet))
    
if __name__ == "__main__":
    files = ['a_example', 'b_should_be_easy', 'c_no_hurry', 'd_metropolis', 'e_high_bonus']
    #files = ['a_example']
    for fn in files:
        main(fn)
