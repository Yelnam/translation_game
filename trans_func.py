# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 11:27:04 2022

@author: rrmanley
"""
from trans_dicts import dict_allowed_inputs

def input_checker(input_val, input_name):
    while input_val not in dict_allowed_inputs[input_name]:
        input_val = input(f'Unexpected input, please select from allowed inputs ({",".join(dict_allowed_inputs[input_name])})\n    Answer: ')
    return input_val    