# name Sihan Chen
# student id: 2563 8460
# email: hnachen@umich.edu
# Work with: My self. Ask ChatGPT some questions when read file in main(). 

"""
name of dataset: penguins.csv
column I used: species, bill length, bill depth, num, flipper length, body mass
Calculation 1: Group by species and compute the average bill length and bill depth
                (mm) to produce a CSV tabl.
Calculation 2: Compute BMI for each penguin then pick the top scorer and print its details.


"""

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
    
    ## Calculation 1: Bill stats by species
    def data_species(self):
        """
        Groups the data by species.
        Returns a dictionary with the grouped data.
        """

        species_group = defaultdict(lambda: {'bill length': [], 'bill depth': []})
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
                ave_length = sum(data['bill length']) / len(data['bill length'])
            else: 
                ave_length = 0

            if len(data['bill depth']) > 0:
                ave_depth = sum(data['bill depth']) / len(data['bill depth'])
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
       
        ranked = sorted(score_list, key=lambda penguin: penguin['score'], reverse=True)
        return ranked[0]
    
    
    def find_winner(self):
        """
        find all information about the winner.
        """
        scores = self.cal_BMI()
        winner = self.winner(scores)

        if winner['id'] == -1:
            return {"error": "No valid penguins found"}
        
        champion_id = winner['id']
        winner_index = self.data_dict['num'].index(champion_id)

        details = {
            'penguin id': champion_id,
            'BMI score': round(winner['score'], 3), 
            'species': self.data_dict['species'][winner_index], 
            'island': self.data_dict['island'][winner_index],
            'bill_length_mm': self.data_dict['bill length'][winner_index],
            'bill_depth_mm': self.data_dict['bill depth'][winner_index],
            'flipper_length_mm': self.data_dict['flipper length'][winner_index],
            'body_mass_g': self.data_dict['body mass'][winner_index],
            'sex': self.data_dict['sex'][winner_index]
        }

        return details
        

def write_bill_csv(rows, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    headers = ['species', 'mean bill length(mm)', 'mean bill depth(mm)']
    with open(filename, 'w', newline ='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Successfully created CSV file: {filename}")




def winner_txt(info, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")
    print(f"Successfully created TXT file: {filename}")



class Testpenguins(unittest.TestCase):
    """
    class for testing
    """
    def setUp(self):
        self.penguin = Pendata("penguins.csv")
        self.penguin.build_data_dict()


    def test_build_data_dict(self):


        


    
    



def main():
    penguin = Pendata("penguins.csv")
    penguin.build_data_dict()

    groups = penguin.data_species()
    rows = penguin.ave_species_group(groups)
    write_bill_csv(rows, 'output/penguins_bill_stats.csv')

    winner_inf = penguin.find_winner()
    winner_txt(winner_inf, 'output/winner.txt')




if __name__ == '__main__':
    unittest.main(verbosity=2)

    main()






            


            









