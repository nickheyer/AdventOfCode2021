import os
import sys
from time import sleep

#------------- ~ INPUT HANDLING ~ --------------

def parse_input(txt):
    inp = txt.splitlines() #Grabbing input
    """Converting lines to usable input"""
    inp = [list(map(str.split, x.split("|"))) for x in inp]
    return inp

def get_input(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, "r") as fp:
        return parse_input(fp.read())

#-------------- ~ SOLUTIONS ~ -------------------

def part_one():
    inp = get_input("input.txt")

    digits = {"abcefg": 0, "cf": 1, "acdfg": 2, "acdfg": 3, "bcdf": 4, "abdfg": 5, "abdefg": 6, "acf": 7, "abcdefg": 8, "abcdfg": 9}

    count = 0

    for signal, output in inp:
        for values in output:
            if len(values) in [2, 3, 4, 7]:
                count += 1

    return count


def part_two():
    inp = get_input("input.txt")

    digits = ["abcefg", "cf", "acdfg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]

    atlas = [[True, True, True, False, True, True, True], #0
    [False, False, True, False, False, True, False], #1
    [True, False, True, True, True, False, True], #2
    [True, False, True, True, False, True, True], #3
    [False, True, True, True, False, True, False], #4
    [True, True, False, True, False, True, True], #5
    [True, True, False, True, True, True, True], #6
    [True, False, True, False, False, True, False], #7
    [True, True, True, True, True, True, True], #8
    [True, True, True, True, False, True, True] #9
    ]

    digi_map = {digits[x]:atlas[x] for x in range(len(digits))}

    answer = 0

    for signal, output in inp:

        segments = dict()


        for value in signal:
            if value not in segments and len(value) in [2, 3, 4, 7]:
                segments[value] = list(filter(lambda x: bool(len(x) == len(value)), digits))[0]

        known_digits_mapped = {"".join(sorted(x)):digi_map[segments[x]] for x in segments}


        translations = dict()

        def check_output(out_list):    
            translated_out_str = ""          
            for num in out_list:
                alph_num = "".join(sorted(num))
                try:
                    translated_out_str += str(atlas.index(known_digits_mapped[alph_num]))
                except Exception as e:
                    print(f"Encountered an error while translating ({e}): {alph_num}\n\nHere are the current mappings / translations: {known_digits_mapped}\n\n{translations}")
                    sys.exit()
            return int(translated_out_str)
            
        def check_progress():
            for x in output:
                t_out = "".join(sorted(x))
                if t_out not in known_digits_mapped:
                    return True
            return False

        while(check_progress()):       
            for i in range(len(known_digits_mapped)):
                d = list(known_digits_mapped)
                prev_s = d[i]
                for k in range(i, len(known_digits_mapped)):
                    

                    current_s = d[k]


                    prev_b = known_digits_mapped[prev_s]
                    current_b = known_digits_mapped[current_s]

                    prev_set, current_set = set(prev_s), set(current_s)

                    #Find common signals between both sets
                    intersections = prev_set.intersection(current_set)
                    intersecting_booleans = [False]*7

                    for b in range(7):
                        if prev_b[b] and current_b[b]:
                            intersecting_booleans[b] = True



                    alph_inter = "".join(sorted(list(intersections)))
                    if len(intersections) == 1 and alph_inter not in known_digits_mapped:
                        translations[alph_inter] = intersecting_booleans
                        known_digits_mapped[alph_inter] = intersecting_booleans

                    elif len(intersections) > 1 and alph_inter not in known_digits_mapped:
                        known_digits_mapped[alph_inter] = intersecting_booleans

                    non_inter = {k for k in "abcdefg"}.symmetric_difference(intersections)

                    non_inter_bool = [False]*7

                    for a in range(7):
                        if not intersecting_booleans[a]:
                            non_inter_bool[a] = True

                    alph_non_inter = "".join(sorted(list(non_inter)))
                    if len(non_inter) == 1 and alph_non_inter not in known_digits_mapped:
                        translations[alph_non_inter] = non_inter_bool
                        known_digits_mapped[alph_non_inter] = non_inter_bool

                    elif len(non_inter) > 1 and alph_non_inter not in known_digits_mapped:
                        known_digits_mapped[alph_non_inter] = non_inter_bool
                    

                    debug = f"""Prev Set:{prev_s}, Prev Bool:{prev_b}
Current Set:{current_s}, Current Bool: {current_b}
Common Set (Intersecting): {intersections}, Common Bools: {intersecting_booleans}

Single Digit Translations: {translations}

List of fully mapped digits: {[atlas.index(x) for x in known_digits_mapped.values() if x in atlas]}\n\n"""

                    #print(debug)

            sig_map = dict()

            for sig in signal:

                #Comparing the information we have with the signals to find the difference

                alph_sig = "".join(sorted(sig))
                partial_bool = [False]*7

                for known_val in known_digits_mapped: #We only have the bool mappings for 1, 4, 7, 8

                    
                    contain_flag = True

                    for char in known_val:
                        if char not in sig:
                            contain_flag = False
                            break           


                    if contain_flag: #If all the characters in one of our known mappings are in one of the signals, append all True bools to map
                        k = known_digits_mapped[known_val]
                        for l in range(7):
                            if k[l] == True:
                                partial_bool[l] = True

                sig_map[sig] = partial_bool

                #
            #Calculate likeliehood based on number of differences

            sig_like = dict()

            for sig in sig_map:

                likeness = list() # A sorted list of tuples containing (The number it is being compared to, The difference of True values in it's bool array (by addition))

                
                for i, digit in enumerate(atlas):
                    #compare current digit to partial sig bool and save each in likeness dict with number as key
                    
                    dif = 0

                    sig

                    for r in range(7): #For each "numbers" standard boolean array, iterating through each bool
                        std_bool = atlas[i]

                        if std_bool[r] == True and sig_map[sig][r] == False:
                            dif += 1
                        elif std_bool[r] == False and sig_map[sig][r] == True:
                            dif = 10
                            break

                    likeness.append((i, dif))

                sig_like[sig] = sorted(likeness, key=lambda x: x[1])

            for sig, likeness in sig_like.items():

                alph_sig = "".join(sorted(sig))

                if likeness[0][1] < 10 and likeness[0][1] < likeness[1][1] and likeness[0][1] + sig_map[sig].count(True) == len(sig):
                    known_digits_mapped[alph_sig] = atlas[likeness[0][0]]

        answer += check_output(output)
    return answer

#-------------- ~ RESULTS ~ -------------------

print(f"Part One: {part_one()}\nPart Two: {part_two()}")