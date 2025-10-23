import random

list_range = list(range(1, 21))

rand_list = random.choices(list_range, k=10)

list_comprehension_below_10 = [data_item for data_item in rand_list if data_item < 10]

list_comprehension_below_10_with_filter = list(filter(lambda x: x < 10, rand_list))

print(rand_list, list_comprehension_below_10, list_comprehension_below_10_with_filter)
