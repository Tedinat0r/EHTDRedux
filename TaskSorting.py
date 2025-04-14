def sorting_dict_struct(dictionary):
    sorting_dict = {}
    completed_tasks = {}
    for item in list(dictionary.keys()):
        if dictionary[item].complete != True:
            sorting_dict.__setitem__(item, [dictionary[item].priority,dictionary[item].urgency, dictionary[item].energy, dictionary[item].energy_quant])
            for thing in sorting_dict.keys():
                print(thing)
        else:
            completed_tasks.__setitem__(item, [dictionary[item].priority, dictionary[item].urgency])
    for thing in sorting_dict.keys():
        print(thing)
    return sorting_dict, completed_tasks


def task_sort(dictionary):
    sorted_items = []
    priority_values = [1, 2]
    dictionary = list(dictionary.items())
    for number in priority_values:
        sub_list = []
        for item in dictionary:
            if number == item[1][0]:
                sub_list.append(item)
        if len(sub_list) > 0:
            sorted_items.append(sub_list)
    for item in sorted_items:
        item = sorted(item, key= lambda x: x[1][1], reverse=True)
    return(sorted_items)


def energy_sort(task_array, type):
    sorted_by_energy = []
    for item in task_array:
        of_type = []
        not_type = []
        for element in item:
            if element[1][2] != type:
                not_type.append(element)
            else:
                of_type.append(element)
        of_type = sorted(of_type, key = lambda x: x[1][3], reverse=True)
        not_type = sorted(not_type, key=lambda x: x[1][3], reverse=True)
        final = of_type + not_type
        sorted_by_energy.append(final)
    return sorted_by_energy
