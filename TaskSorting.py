






def sorting_dict_struct(dictionary):
    sorting_dict = {}
    completed_tasks = {}
    for item in list(dictionary.keys()):
        if dictionary[item].complete != True:
            sorting_dict.__setitem__(item, [dictionary[item].priority,dictionary[item].urgency])
        else:
            completed_tasks.__setitem__(item, [dictionary[item].priority, dictionary[item].urgency])
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

