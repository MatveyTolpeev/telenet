def find_sum_idx(lst, target):

    lst_dict = {}

    for i, num in enumerate(lst):
        if target - num in lst_dict:
            return [lst_dict[target-num], i]
        else:
            lst_dict[num] = i

    return -1


lst = [1, 9, 5, 7, 3, 15]
print(find_sum_idx(lst, 10))
