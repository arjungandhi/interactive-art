import random
class Drop():
    def __init__(self,sim_params):
        self.sim_params = sim_params
        self.max_lifetime = self.__get_max_lifetime()
        self.age = 0
        self.x = random.random()
        self.y = random.random()
        self.dying = False
        
    def loop(self, increment = 1.):
        #each loop the age increases by one up to max_lifetime
        if self.dying:
            self.age -= increment*3
        elif self.age< self.max_lifetime:
            self.age += increment
        
        
    def does_die(self, modifier = 1):
        death_chance = self.__get_category(self.age,self.sim_params['death_chance'])
        if random.random() < death_chance*modifier:
            self.dying=True
        
    def __get_max_lifetime(self):
        age_dist = self.sim_params['age_dist']
        max_age = self.__get_max_age()
        age_list = list(age_dist.keys())
        i = age_list.index(max_age)
        age_list = [int(a) for a in age_list]
        age_list.append(0)
        age = random.randint(age_list[i-1],age_list[i])
        return age
        
        
        
    def __get_max_age(self):
        age_dist = self.sim_params['age_dist']
        total =  sum(age_dist.values())
        loc = random.random() * total
        for k, v in age_dist.items():
            loc -=  v 
            if loc < 0:
                return k
        return age_dist.keys()[-1]
        
    
    def __get_category(self, val, data):
        result = list(data.values())[0]
        for k,v in data.items():
            max_age = int(k)
            result = v
            if val > max_age:
                break
        return result
            

        
