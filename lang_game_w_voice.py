# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 22:31:48 2022

@author: rrmanley
"""

from gtts import gTTS
import random
import time
import os

from trans_lists import list_langs, list_langs_gTTS, list_verbs, list_nouns, list_adjs, dict_lists
from trans_dicts import dict_langs, dict_verbs, dict_nouns, dict_adjs, dict_dicts
from trans_func import input_checker


again = 'Y'
runs, score, wrong_answers = 0, 0, 0
max_runs = 10
while again in ['Y','y']: 
    mode = input('\nRun Normal Mode (medium difficulty, random lang and word types)? Y/N: ') # set quick default mode option
    if mode in ['Y', 'y']: # set expected default settings
        diff = 'm'
        lang_select = 'rr'
        type_select = 'r'
        type_choice = 'r'
    # difficulty: easy first 10, medium 50, hard 100
    if mode not in ['Y', 'y']: diff = input('Choose difficulty: E = Easy, M = Medium, H = Hard: ')
    diff = input_checker(diff, 'diff')
    max_word = 10 if diff in ['E', 'e'] else 80 if diff in ['M', 'm'] else 100
    # choose to select language or random language 
    if mode not in ['Y', 'y']: lang_select = input('Choose language. De,Fr,Es,It,La,El,Ru,Iv,Ar,Hi,Cn, R for random pick, or RR for random each question: ')
    lang_select = input_checker(lang_select, 'lang_select')
    # set a fixed random language if lang_select is R or r
    if lang_select in ['R','r'] : 
        if diff in ['H', 'h']: lang_num_fixed_rand = random.randint(0, 11) 
        if diff in ['M', 'm']: lang_num_fixed_rand = random.randint(0, 8)
        if diff in ['E', 'e']: lang_num_fixed_rand = random.randint(0, 5)
    # choose to select word group or random word group
    if mode not in ['Y', 'y']: type_select = input('Choose word group. V for Verb, N Noun, A Adj or R for random: ')
    type_select = input_checker(type_select, 'type_select')
    
    while runs < max_runs:  
        # select new random lang on each Question if RR random
        if lang_select in ['RR','rr'] : 
            if diff in ['H', 'h']: lang_num = random.randint(0, 10) 
            if diff in ['M', 'm']: lang_num = random.randint(0, 7)
            if diff in ['E', 'e']: lang_num = random.randint(0, 5)
        # use the preset rand lang if R random
        elif lang_select in ['R','r'] : 
            lang_num = lang_num_fixed_rand
        # else use chosen lang
        else: lang_num = dict_langs[lang_select]
        # select random word group if random, else chosen word group
        type_choice = ['V','N','A'][random.randint(0,2)] if type_select in ['R','r'] else type_choice
        # script select random english word
        list_of_choice = dict_lists[type_choice]
        dict_of_choice = dict_dicts[type_choice]
        randoms = random.sample(range(0, max_word-1), 4)
        word_rand = list_of_choice[randoms[0]]
        # script select correct word from foreign language, save it as a var
        word_trans = dict_of_choice[list_of_choice[randoms[0]]][lang_num]
        # scr select three wrong words from foreign language
        wrong_rand1 = dict_of_choice[list_of_choice[randoms[1]]][lang_num]
        wrong_rand2 = dict_of_choice[list_of_choice[randoms[2]]][lang_num]
        wrong_rand3 = dict_of_choice[list_of_choice[randoms[3]]][lang_num]
        # scr put them in a list,  randomise the order
        opts = [word_trans, wrong_rand1, wrong_rand2, wrong_rand3]
        random.shuffle(opts)
        # scr present the random list to the user, have user enter ABC or D
        language = list_langs[lang_num]
        lang_gTTS = list_langs_gTTS[lang_num]
        prompt = f'\'{word_rand}\' in {language} is... '
        if type_choice == 'V': print(f'\n{language} Verbs: {prompt}')
        if type_choice == 'N': print(f'\n{language} Nouns: {prompt}')
        if type_choice == 'A': print(f'\n{language} Adjectives: {prompt}')
        gTTS(text=prompt, lang='en', slow=False).save("temp_audio.mp3")
        os.system("temp_audio.mp3")
        answer = input(f'    A: {opts[0]}, B: {opts[1]}, C: {opts[2]}, D: {opts[3]} ? - ')
        answer = input_checker(answer, 'answer')
        # scr get the chosen answer ABCD/0123 from the randomised list
        ans = opts[{'A':0, 'B':1, 'C':2, 'D':3, 'a':0, 'b':1, 'c':2, 'd':3,}[answer]]
        # scr let user know if they were right or wrong
        # add score to right or wrong total and ask again
        if ans == word_trans: 
            print(f'\n    Correct - \'{word_rand}\' in {language} is \'{word_trans}\'')
            gTTS(text='Correct.', lang='en', slow=False).save("trans_audio.mp3")
            os.system("trans_audio.mp3")
            time.sleep(1)
            gTTS(text=word_trans, lang=lang_gTTS, slow=False).save("trans_audio.mp3")
            os.system("trans_audio.mp3")
            time.sleep(2)
            runs += 1
            score += 1
        else: 
            print(f'\n    Incorrect - \'{word_rand}\' in {language} is \'{word_trans}\'')
            gTTS(text=f'Not quite. {prompt}', lang='en', slow=False).save("trans_audio.mp3")
            os.system("trans_audio.mp3")
            time.sleep(3.5)
            gTTS(text=word_trans, lang=lang_gTTS, slow=False).save("trans_audio.mp3")
            os.system("trans_audio.mp3")
            time.sleep(2)
            runs += 1
            wrong_answers += 1
    # after ten runs, print score out of ten and ask if to run again
    again = input(f'\nYou scored {score}/{runs}. Enter Y to play again, or hit Enter to end: ')
    runs, score, wrong_answers = 0, 0, 0
print('Thanks for playing!')
# add all scores to an external file which keeps count and provides
# an average after finishing
# print(f'Thanks for playing, you scored an average of n/max_runs)