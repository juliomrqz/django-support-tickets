# -*- coding: utf-8 -*-

from faker import Faker
fake = Faker()


def unique_list(seq):
    ''' Taken from: http://stackoverflow.com/a/480227/3111897 '''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def generate_fake_list(func, num, **kwargs):
    output_list = []

    # Genera fake data
    for i in range(num):
        output_list.append(func(**kwargs))

    # Remove duplicates
    output_list = unique_list(output_list)

    # Add extra item if duplicated items where founded
    tries = 0
    while len(output_list) < num:

        if tries > 100:
            break

        # Generate new item
        new_item = func(**kwargs)

        # Append new item if it's not in output_list
        if new_item not in output_list:
            output_list.append(new_item)

        tries += 1

    return output_list
