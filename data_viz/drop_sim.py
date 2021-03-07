import matplotlib.pyplot as plt
import json
import requests
from drop import Drop
import random

#get data
census_data = requests.get('https://s3.amazonaws.com/data.careinstitute.com/censtats/json/censtats.json').json()
mortality_data = json.load(open('mortality.json','r'))
print('Fetched Data')

zip_code =  input('enter a zipcode: ')
years = int(input('enter num simulation years: '))
increment_rate = float(input('enter sim speed (0-1): '))
zip_data= [x for x in census_data if x['zcta'] == zip_code][0]
death_data = mortality_data[zip_data['state'][0]]

male_age_dist = { k:int(v) for k,v in zip_data['age_and_sex']['male'].items()}
female_age_dist = { k:int(v) for k,v in zip_data['age_and_sex']['female'].items()}

k_converter = {'age_0_to_9_years': 9,
 'age_10_to_19_years': 19,
 'age_20_to_29_years': 29,
 'age_30_to_39_years': 39,
 'age_40_to_49_years': 49,
 'age_50_to_59_years': 59,
 'age_60_to_69_years': 69,
 'age_70_years_and_over': 100}

total_age_dist = { k_converter[k]:v+male_age_dist[k] for k,v in female_age_dist.items()} 

print('Starting Sim')
#create a plot and set it up to do things
fig, ax = plt.subplots(figsize=(15,15))
ax.set_facecolor('xkcd:dark grey')
fig.patch.set_facecolor('xkcd:dark grey')
fig.show()
sim_params = {
    'age_dist' : total_age_dist,
    'death_chance' : death_data
}

birthrate = .3/increment_rate
max_pop = 75
raindrops = []
sim_length = int(years/increment_rate)
for i in range(sim_length):
    #clearing and hiding xticks and yticks
    ax.clear()
    trash = ax.set_xticks([],minor=[])
    trash = ax.set_yticks([],minor=[])
    # possibly adding a new raindrop 
    if len(raindrops) < max_pop:
        if random.random() < birthrate+len(raindrops)/max_pop:
            raindrops.append(Drop(sim_params))
    
    # looping and plotting the rain drops 
    for drop in raindrops:
        drop.loop(increment_rate)
        drop.does_die(increment_rate/1)
        if drop.age < 0:
            raindrops.remove(drop)
        else:
            patch = plt.Circle((drop.x,drop.y), drop.age/1000,  fill=False, edgecolor= 'white')
            ax.add_patch(patch)
    fig.canvas.draw()

input('sim done!')