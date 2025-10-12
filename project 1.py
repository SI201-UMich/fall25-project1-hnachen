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


            self.data_dict['num'].append(int(separated[0].strip(' "')))
            self.data_dict['species'].append(separated[1].strip(' "'))
            self.data_dict['island'].append(separated[2].strip(' "'))
            self.data_dict['year'].append(int(separated[8].strip(' "')))

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
        d = self.penguin.data_dict
        self.assertIsInstance(d, dict) 
        self.assertIsInstance(d['species'], list) # check row is list
        self.assertEqual(len(d['species']), 344) #num of column = 344
        ## row 4 has five NA
        self.assertTrue(
            d['bill length'][d['num'].index(4)] is None and
            d['bill depth'][d['num'].index(4)]  is None and
            d['flipper length'][d['num'].index(4)] is None and
            d['body mass'][d['num'].index(4)]  is None and
            d['sex'][d['num'].index(4)] is None
        )
        # check the last row
        self.assertTrue(d['species'][d['num'].index(344)] == 'Chinstrap')
        self.assertTrue(d['bill length'][d['num'].index(344)]  == 50.2)
        self.assertTrue(d['year'][d['num'].index(344)]    == 2009)


        

    def test_data_species(self):
        d = self.penguin.data_dict
        g = self.penguin.data_species()

        ## check in this species, where has a record with paried bill length and depth match the table
        self.assertIn((50.4, 15.3), list(zip(g['Gentoo']['bill length'], g['Gentoo']['bill depth'])))
        self.assertIn((38.6, 21.2), list(zip(g['Adelie']['bill length'], g['Adelie']['bill depth'])))


        # no NA in species group
        self.assertTrue(all(x is not None for x in g['Adelie']['bill length']) 
                        and all(x is not None for x in g['Adelie']['bill depth']))   
        # species : out of list
        self.assertTrue('Emperor' not in g)
    

    def test_ave_species_group(self):
        g = self.penguin.data_species()
        rows = self.penguin.ave_species_group(g)
        # there are 3 species, with 3 rows
        self.assertEqual(len(rows), 3)

        # round to 3 three decimal places
        self.assertEqual(next(r for r in rows if r['species']=='Adelie')['mean bill length(mm)'], 
                         round(sum(g['Adelie']['bill length'])/len(g['Adelie']['bill length']), 3))  
        # if 2 penguin with [48.1, 19.2], [32.3, 18], calculate the mean
        self.assertEqual(self.penguin.ave_species_group({'X': {'bill length':[48.1, 32.3], 'bill depth':[19.2, 18]}})[0], 
                         {'species':'X','mean bill length(mm)':40.2,'mean bill depth(mm)':18.6})  
        # if 3 penguin with [37.7, 17.3], [35, 18], calculate the mean
        self.assertEqual(self.penguin.ave_species_group({'X': {'bill length':[37.7, 35], 'bill depth':[17.3, 18]}})[0], 
                         {'species':'X','mean bill length(mm)':36.35,'mean bill depth(mm)':17.65})  
        

        # if one penguin without Bill length
        self.assertEqual(self.penguin.ave_species_group({'Z': {'bill length':[], 'bill depth':[4.0, 6.0]}})[0], 
                         {'species':'Z','mean bill length(mm)':0,'mean bill depth(mm)':5.0})
         # empty grous with empty list
        self.assertEqual(self.penguin.ave_species_group({}), [])  


    def test_cal_BMI(self):
        d = self.penguin.data_dict
        scores = self.penguin.cal_BMI()
        scores_by_id = {s['id']: s['score'] for s in scores}

        #there is result BMI is positive
        self.assertTrue(len(scores) > 0)
        self.assertTrue(all(s['score'] > 0 for s in scores))
        # scores are same
        self.assertAlmostEqual(scores[0]['score'],
            (d['body mass'][d['num'].index(scores[0]['id'])]/1000) / ((d['flipper length'][d['num'].index(scores[0]['id'])]/1000)**2),
            places=9)
        

        # num = 38
        i = d['num'].index(38)
        expected_38 = (d['body mass'][i] / 1000) / ((d['flipper length'][i] / 1000) ** 2)
        self.assertAlmostEqual(scores_by_id[38], expected_38, places=9)

        # 337
        j = d['num'].index(337)
        expected_337 = (d['body mass'][j] / 1000) / ((d['flipper length'][j] / 1000) ** 2)
        self.assertAlmostEqual(scores_by_id[337], expected_337, places=9)   

        # num = 272 all NA
        self.assertTrue(d['body mass'][d['num'].index(272)] is None and d['flipper length'][d['num'].index(272)] is None)
        # ID not in BMI list
        self.assertNotIn(388, scores_by_id)










    



    
    









    



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






            


            









