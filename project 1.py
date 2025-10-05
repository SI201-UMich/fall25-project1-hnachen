# name Sihan Chen
# student id: 2563 8460
# email: hnachen@umich.edu

import os
import csv
import unittest
from collections import defaultdict

class Pendata():
    """
    class for reading and getting data 
    """

    def __init__(self, filename):

        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.full_path = os.path.join(self.base_path, filename)
        self.file_obj = open(self.full_path, 'r')
        self.raw_data = self.file_obj.readlines()
        self.file_obj.close()

        self.data_dict = {
            'num': [],
            'species': [], 
            'island': [],
            'bill length': [], 
            'bill depth': [],
            'flipper length': [], 
            'body mass': [], 
            'sex': [],
            'year': []
        }



    def build_data_dict(self):
        """
        cleaning data
        """
        for line in self.raw_data[1:]:
            line = line.strip()
            if not line:
                continue

            separated = line.split(',')
            if len(separated) < 9:
                continue


            self.data_dict['num'].append(int(separated[0].strip('"')))
            self.data_dict['species'].append(separated[1])
            self.data_dict['island'].append(separated[2])

            if separated[7] == 'NA':
                self.data_dict['sex'].append(None)
            else:
                self.data_dict['sex'].append(separated[7])

            if separated[3] == 'NA':
                self.data_dict['bill length'].append(None)
            else:
                self.data_dict['bill length'].append(float(separated[3]))

            if separated[4] == 'NA':
                self.data_dict['bill depth'].append(None)
            else:
                self.data_dict['bill depth'].append(float(separated[4]))

            if separated[5] == 'NA':
                self.data_dict['flipper length'].append(None)
            else:
                self.data_dict['flipper length'].append(int(separated[5]))

            if separated[6] == 'NA':
                self.data_dict['body mass'].append(None)
            else:
                self.data_dict['body mass'].append(int(separated[6]))
    
    ## Calculation 1: 
    def data_species(self):
        """
        Groups the data by species.
        Returns a dictionary with the grouped data.
        """

        species_group = defaultdict(lambda: {'bill lengths': [], 'bill depth': []})
        for i in range(len(self.data_dict['species'])):
            cur_species = self.data_dict['species'][i]
            cur_length = self.data_dict['bill length'][i]
            cur_depth = self.data_dict['bill depth'][i]

            if cur_length is not None:
                species_group[cur_species]['bill length'].append(cur_length)

            if cur_depth is not None:
                species_group[cur_species]['bill depth'].append(cur_depth)

        return species_group
    
    def ave_species_group(self, groups):
        """
        Takes a dictionary of grouped data and calculates the averages.
        Returns a list of result dictionaries.
        """

        final_results = []
        for species, data in groups.items():
            if len(data['bill length']) > 0:
                ave_length = sum(data['bill length']) / len(data('bill length'))
            else: 
                ave_length = 0

            if len(data['bill depth']) > 0:
                ave_depth = sum(data['bill depth']) / len(data('bill depth'))
            else: 
                ave_depth = 0

            result_dict = {
                'species': species, 
                'mean bill length(mm)': round(ave_length, 3), 
                'mean bill depth(mm)': round(ave_depth, 3)

            }
            final_results.append(result_dict)
        return final_results
    

    # Calculation 2: who is the strongest penguins. 
    def cal_BMI(self):
        """
        Iteration all penguins and calculate their BMI scores. 
        """

        scores = []
        for i in range(len(self.data_dict['num'])):
            id = self.data_dict['num'][i]
            mass = self.data_dict['body mass'][i]
            flipper = self.data_dict['flipper length'][i]

        if mass is not None and flipper is not None: 
            mass_kg = mass / 1000
            flipper_m = flipper / 1000
            cur_score = mass_kg / (flipper_m * flipper_m)

            scores.append({'id': id, 'score': cur_score})
        
        return scores
    
    def winner(self, score_list):
        """
        find the highest score from the list. 
        """

        if not score_list: 
            return {'id': -1, 'score': -1}
       
        list = sorted(score_list, key=lambda penguin: penguin['score'], reverse=True)
        champion = sorted
    
    def find_winner(self):
        """
        find all information about the winner.
        """
        scores = self.cal_BMI()
        winner = self.winner(scores)

        if winner['id'] == -1:
            return {"error": "No valid penguins found"}
        





    
    




 


class Testpenguins(unittest.TestCase):


    def main():





            


            









