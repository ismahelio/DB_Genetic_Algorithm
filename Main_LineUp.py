from Class_Padlers import Paddler
from random import shuffle
from random import sample
from random import choice
from random import randrange
import copy
import time
#Convert all the csv into Paddler objects
import csv

start = time.time()


# Shuffle pacers, engine and rockets independently
def generate_boat(paddlers):
    new_boat = copy.copy(paddlers)
    shuffle(new_boat[0])
    shuffle(new_boat[1])
    shuffle(new_boat[2])
    return new_boat

# Create a the generation
def  generationx(paddlers, fixed_paddlers, n):

    gen = []
    for i in range(n):
        new_boat = copy.copy(paddlers)
        a = mix_values(new_boat[0], fixed_paddlers[0:6])
        b = mix_values(new_boat[1], fixed_paddlers[6:14])
        c = mix_values(new_boat[2], fixed_paddlers[14:20])
        gen.append([a,b,c])
    return gen


# Check weight - Compare both sides of the division PER
def check_weight(boat):
    fitness = 0
    weight_left = 0
    weight_rigth = 0
    for zone in boat:
        weights = check_weight_zone(zone)
        fitness += abs((weights[0]-weights[1]))
        weight_left += weights[0]
        weight_rigth += weights[1]

    weight_sides_dif = abs(weight_left - weight_rigth)
    fitness += weight_sides_dif
    return fitness


def check_weight_zone(zone):
    left = 0
    right = 0
    for i in range(len(zone)):
        paddler = zone[i]
        if i %2 == 0:
            left += paddler.weight
        else:
            right += paddler.weight

    return [left, right]

def check_weight_side_dif(boat):
    weight_left = 0
    weight_rigth = 0
    for zone in boat:
        weights = check_weight_zone(zone)
        weight_left += weights[0]
        weight_rigth += weights[1]

    weight_sides_dif = abs(weight_left - weight_rigth)
    return weight_sides_dif

#Checks individual rows of the boat to get balance paddlers
def check_weight_one_row(boat):
    fitness = 0
    for zone in boat:
        for i in range(0, len(zone), 2):
            left = zone[i].weight
            rigth = zone[i+1].weight
            fitness+=(abs(left-rigth))
    return fitness


# Check Preference Side
"""bothsides_inc, multiplies the punishment if the paddler is not at the right side and can not do both sides"""
def check_preference(boat, punishment, bothsides_inc):
    fitness = 0
    for zone in boat:
        for i in range(len(zone)):
            preference = zone[i].preference
            both_sides = zone[i].bothsides
            # Left side
            if i%2 == 0:
                if preference != "L":
                    fitness += punishment
                    if both_sides != "Y":
                        fitness += (punishment*bothsides_inc)
            # Rigth side
            else:
                if preference != "R":
                    fitness += punishment
                    if both_sides != "Y":
                        fitness += (punishment*bothsides_inc)

    return fitness


def breed(boats):
    new_gen = []
    for i in range(0, len(boats), 2):
        # Get front-mid or back of the boat by 0,1,2
        boat1 = boats[i]
        boat2 = boats[i+1]
        breed1 = [boat2[0], boat1[1], boat1[2]]
        breed2 = [boat1[0], boat2[1], boat2[2]]
        breed3 = [boat1[0], boat2[1], boat1[2]]
        breed4 = [boat2[0], boat1[1], boat2[2]]
        breed5 = [boat1[0], boat1[1], boat2[2]]
        breed6 = [boat2[0], boat2[1], boat1[2]]
        breeds = [breed1, breed2, breed3, breed4, breed5, breed6]
        new_gen.extend(breeds)

    return new_gen


def mutation(boats, fixed_paddlers):
    mutations = []
    for old_boat in boats:
        #first decide how many zones to mutate
        #new_boat = copy.copy(old_boat)
        new_boat = []
        for zone in old_boat:
            n_zone = []
            for person in zone:
                n_zone.append(copy.copy(person))
            new_boat.append(n_zone)
        for i in range(len(new_boat)):
            edit = choice([True, False])
            #if yes we exchange positions of 2 paddlers in that zone
            if edit:
                change_id_1 = randrange(0, len(new_boat[i]))
                change_id_2 = randrange(0, len(new_boat[i]))
                if fixed_paddlers[change_id_1] is not None and fixed_paddlers[change_id_2] is not None:
                    paddler_1 = copy.copy(old_boat[i][change_id_1])
                    paddler_2 = copy.copy(old_boat[i][change_id_2])
                    new_boat[i][change_id_1] = paddler_2
                    new_boat[i][change_id_2] = paddler_1
        mutations.append(new_boat)

    return mutations


def fill_in(list, element):
    """ Adds the element into the first empty spot in the list """
    for i in range(len(list)):
        if not list[i]:
            list[i] = element
            break
    
    return list
    
    
def get_paddler(paddlers, name):
    """ Returns paddler according to given name """
    paddler = None
    for i in range(len(paddlers)):
        if paddlers[i].name == name:
            paddler = paddlers[i]
    
    return paddler
 

def mix_values(new_boat, fixed_paddlers):
    """ Shuffles the new_boat list by keeping fixed paddlers at their position """
    new_boat_slice = []
    result = []
    for i in range(len(new_boat)):
        if fixed_paddlers[i] is None:
            new_boat_slice.append(new_boat[i])
    shuffled_boat = sample(new_boat_slice, len(new_boat_slice))
    j = 0
    for i in range(len(new_boat)):
        if fixed_paddlers[i] is not None:
            result.append(fixed_paddlers[i])
        else:
            result.append(shuffled_boat[j])
            j += 1
    return result

    

def genetic_algorithm():
    paddlers_path = r"csv_data/Spanish Dragons paddlers.csv"
    paddlers = []
    fixed_paddlers = []
    with open(paddlers_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)  # skip header
        for row in reader:
            paddler = Paddler(row[0], row[4], float(row[3]), row[5], row[6])
            paddlers.append(paddler)

    shuffle(paddlers)

    # Divide the boat: 3 rows(pacers), 4 rows(engine) and 3 rows(rockets) - Division PER
    pacers = [None] * 6
    engine = [None] * 8
    rocket = [None] * 6
    
    # Assign fixed positions
    fixed_pos_path = r"csv_data/Fixed positions.csv"
    with open(fixed_pos_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)  # skip header
        for row in reader:
            fixed_paddlers.append(get_paddler(paddlers,row[2]))
            fixed_paddlers.append(get_paddler(paddlers,row[3]))
            if len(row[2]) > 0:
                if row[1] == "Pacers":
                    pacers[int(row[0])*2-2] = get_paddler(paddlers,row[2])
                elif row[1] == "Engine":
                    engine[int(row[0])*2-8] = get_paddler(paddlers,row[2])
                elif row[1] == "Rocket":
                    rocket[int(row[0])*2-16] = get_paddler(paddlers,row[2])
            elif len(row[3]) > 0:
                if row[1] == "Pacers":
                    pacers[int(row[0])*2-1] = get_paddler(paddlers,row[3])
                elif row[1] == "Engine":
                    engine[int(row[0])*2-7] = get_paddler(paddlers,row[3])
                elif row[1] == "Rocket":
                    rocket[int(row[0])*2-15] = get_paddler(paddlers,row[3])
    
    for paddler in paddlers:
        if paddler not in fixed_paddlers:
            if paddler.position == "P" and not all(pacers):
                pacers = fill_in(pacers, paddler)
            if paddler.position == "E" and not all(engine):
                engine = fill_in(engine, paddler)
            if paddler.position == "R" and not all(rocket):
                rocket = fill_in(rocket, paddler)

    # One of the possible boats
    boat = [pacers, engine, rocket]

    n_people =16
    iterations = 200
    gen = generationx(boat, fixed_paddlers, n_people)



    for i in range(iterations):
        sorted_boats = []
        for b in gen:
            fitness = check_weight(b) + check_preference(b, 5, 2) + check_weight_one_row(b)
            sorted_boats.append([b, fitness])
            #print (fitness)

        # Sort the boats by fitness and select half of the n_people as the best candidates
        sorted_boats = sorted(sorted_boats, key=lambda x: x[1])

        #for fitness in sorted_boats:
         #   print(fitness[1])

        half_sel = int(n_people/2)
        sorted_boats = sorted_boats[:half_sel]
        # Get only the boats with no fitness
        sorted_boats = [x[0] for x in sorted_boats]


        candidates = sorted_boats


        new_generation = breed(candidates)
        #copy_gen = copy.copy(new_generation)
        mutations = mutation(new_generation, fixed_paddlers)

        candidates.extend(new_generation)
        candidates.extend(mutations)

        #Add more random generation
        new_gen = generationx(boat, fixed_paddlers, half_sel)
        candidates.extend(new_gen)

        gen = []
        gen = candidates

    #Best option
    Best_Option = sorted_boats[0]

    print("fitness weight is: " + str(check_weight(Best_Option)))

    print("Boat Arrangement Optimized")
    line_up = []
    for zone in Best_Option:

        for i in range(0,len(zone), 2):

            line = zone[i].name + "_" + str(zone[i].weight) + " / " + zone[i+1].name + "_" + str(zone[i+1].weight)

            line_up.append(line)

    print("weigth diff: " + str(check_weight_side_dif(Best_Option)))

    print(time.time()-start)


    return line_up
