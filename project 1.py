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
        self.rows = []



    def build_data_dict(self):
        """
        Cleaning data using the csv.DictReader to meet project requirements.
        """
        # re-open the file here for the csv module to read it properly
        with open(self.full_path, 'r', newline='', encoding='utf-8') as file_obj:
            # Create a DictReader object.
            reader = csv.DictReader(file_obj)

            for row in reader:
                num_key = next(iter(row)) 
                num = row[num_key]
                

                species = row['species']
                island = row['island']
                year = row['year']
                sex = row['sex']
                bill_len= row['bill_length_mm']
                bill_dep = row['bill_depth_mm']
                flipper_len = row['flipper_length_mm']
                body_mass = row['body_mass_g']

                # Append cleaned data 
                self.data_dict['num'].append(int(num))
                self.data_dict['species'].append(species)
                self.data_dict['island'].append(island)
                self.data_dict['year'].append(int(year))
                
                # Use ternary operators for clean assignment
                self.data_dict['sex'].append(None if sex == 'NA' else sex)
                self.data_dict['bill length'].append(None if bill_len == 'NA' else float(bill_len))
                self.data_dict['bill depth'].append(None if bill_dep == 'NA' else float(bill_dep))
                self.data_dict['flipper length'].append(None if flipper_len == 'NA' else int(flipper_len))
                self.data_dict['body mass'].append(None if body_mass == 'NA' else int(body_mass))

            
    
    ## Calculation 1: Bill stats by species
    ## using "species", "bill length", "bill depth"
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
    # using "body_mass", "flipper length", "num"
    def cal_BMI(self):
        """
        Iteration all penguins and calculate their BMI scores. 
        """

        scores = []
        for i in range(len(self.data_dict['num'])):
            id = self.data_dict['num'][i]
            mass = self.data_dict['body mass'][i]
            flipper = self.data_dict['flipper length'][i]
            year = self.data_dict['year'][i]

            if mass is not None and flipper is not None: 
                mass_kg = mass / 1000
                flipper_m = flipper / 1000
                cur_score = mass_kg / (flipper_m * flipper_m)

                scores.append({'id': id, 'score': cur_score, 'year': year})
        
        return scores
    
    def winner(self, score_list):
        """
        find the highest score from the list. 
        if same older year first (smaller year wins).
        """

        if not score_list: 
            return {'id': -1, 'score': -1}
        
       
        ranked = sorted(score_list, key=lambda penguin: (-penguin['score'], penguin['year']))
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
            'year': self.data_dict['year'][winner_index],   
            'bill_length_mm': self.data_dict['bill length'][winner_index],
            'bill_depth_mm': self.data_dict['bill depth'][winner_index],
            'flipper_length_mm': self.data_dict['flipper length'][winner_index],
            'body_mass_g': self.data_dict['body mass'][winner_index],
            'sex': self.data_dict['sex'][winner_index]
        }

        return details
        

def write_bill_csv(rows, filename):
    headers = ['species', 'mean bill length(mm)', 'mean bill depth(mm)']
    with open(filename, 'w', newline ='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Successfully created CSV file: {filename}")




def winner_txt(info, filename):
    # minimal English, aligned columns

    def val(k):
        v = info.get(k)
        return "NA" if v is None else v

    def fmt_num(x, nd=None, unit=""):
        if x is None:
            return "NA"
        if isinstance(x, (int, float)) and nd is not None:
            return f"{x:.{nd}f}{unit}"
        return f"{x}{unit}"

    lines = []
    lines.append("Information about the highest-BMI penguin")
    lines.append("")

    # left labels aligned to width 20
    w = 20
    lines.append(f"{'penguin id:'.ljust(w)}{val('penguin id')}")
    lines.append(f"{'BMI (kg/m^2):'.ljust(w)}{fmt_num(info.get('BMI score'), 3)}")
    lines.append(f"{'species:'.ljust(w)}{val('species')}")
    lines.append(f"{'island:'.ljust(w)}{val('island')}")
    lines.append(f"{'year:'.ljust(w)}{val('year')}")
    lines.append(f"{'bill_length_mm:'.ljust(w)}{fmt_num(info.get('bill_length_mm'), 1)}")
    lines.append(f"{'bill_depth_mm:'.ljust(w)}{fmt_num(info.get('bill_depth_mm'), 1)}")
    lines.append(f"{'flipper_length_mm:'.ljust(w)}{fmt_num(info.get('flipper_length_mm'), 0)}")
    lines.append(f"{'body_mass_g:'.ljust(w)}{fmt_num(info.get('body_mass_g'), 0)}")
    lines.append(f"{'sex:'.ljust(w)}{val('sex')}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Successfully created TXT file: {filename}")





class Testpenguins(unittest.TestCase):
    """
    class for testing 
    some test is hard to use a sample of your chosen csv dataset, so I use some of re-reading 
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
        
        # self cases not from 
        # if 2 penguin with [48.1, 19.2], [32.3, 18], calculate the mean
        self.assertEqual(self.penguin.ave_species_group({'X': {'bill length':[48.1, 32.3], 'bill depth':[19.2, 18]}})[0], 
                         {'species':'X','mean bill length(mm)':40.2,'mean bill depth(mm)':18.6})  
        # if 3 penguin with [37.7, 17.3], [35, 18], calculate the mean
        self.assertEqual(self.penguin.ave_species_group({'X': {'bill length':[37.7, 35], 'bill depth':[17.3, 18]}})[0], 
                         {'species':'X','mean bill length(mm)':36.35,'mean bill depth(mm)':17.65})  
            #special case
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


    
    def test_winner(self):
    
        # check the list 
        self.assertEqual(self.penguin.winner([{'id':1,'score':33.2,'year': 2021},{'id':2,'score':31.2,'year': 2022},{'id':3,'score':30,'year': 2011}]), {'id':1,'score':33.2,'year':2021})
        self.assertEqual(self.penguin.winner([{'id':1,'score':45,'year':2011},{'id':2,'score':43.2,'year':2013},{'id':3,'score':41,'year':2011}]), {'id':1,'score':45,'year':2011})
        # check the ranking whether correct
        self.assertEqual(self.penguin.winner(self.penguin.cal_BMI()), max(self.penguin.cal_BMI(), key=lambda s: s['score']))

        # empty list should return the sentinel
        self.assertEqual(self.penguin.winner([]), {'id':-1,'score':-1})

        # when scores tie, keep the first occurrence (Python's sorted is stable)
        self.assertEqual(self.penguin.winner([{'id':10,'score':7.7,'year':2003},{'id':11,'score':7.7,'year':2013}])['id'], 10)


    def test_find_winner(self):
        details = self.penguin.find_winner()
        top = max(self.penguin.cal_BMI(), key=lambda s: s['score'])

        #  id equals argmax
        self.assertEqual(details['penguin id'], top['id'])
        # BMI equals rounded top score (3 decimals)
        self.assertEqual(details['BMI score'], round(top['score'], 3))

        #  details match the base row (species/island/year)
        idx = self.penguin.data_dict['num'].index(details['penguin id'])
        self.assertEqual(
            (details['species'], details['island'], details['year']),
            (self.penguin.data_dict['species'][idx],
             self.penguin.data_dict['island'][idx],
            self.penguin.data_dict['year'][idx])
        )

        # example 1
        p = Pendata("penguins.csv"); p.build_data_dict()
        p.data_dict = {
            'num':            [1, 2, 3],
            'species':        ['Adelie', 'Gentoo', 'Chinstrap'],
            'island':         ['Torg',   'Biscoe', 'Dream'],
            'year':           [2007,     2008,     2009],
            'bill length':    [None,     40.0,     None],
            'bill depth':     [None,     18.0,     None],
            'flipper length': [200,      200,      100],   # mm
            'body mass':      [5000,     6000,     7000],  # g
            'sex':            ['male',   'female', None],
        }
        d1 = p.find_winner()
        self.assertEqual(d1['penguin id'], 3)                                 # exact id
        self.assertEqual(d1['BMI score'], 700.0)                               # exact BMI (kg/m^2)
        self.assertEqual((d1['species'], d1['island'], d1['year']), ('Chinstrap', 'Dream', 2009))
        self.assertEqual((d1['bill_length_mm'], d1['bill_depth_mm']), (None, None))

        # example 2
        p1 = Pendata("penguins.csv")
        p1.data_dict = {
            'num':            [101, 102, 103, 104],
            'species':        ['A',  'B',  'C',  'D' ],
            'island':         ['I1', 'I2', 'I3', 'I4'],
            'year':           [2007, 2008, 2009, 2010],
            'bill length':    [39.0, 41.0, 37.5, None],
            'bill depth':     [18.5, 18.2, None, 17.9],
            'flipper length': [180,  200,  150,  220],   # mm
            'body mass':      [4500, 8000, 5000, 9000],  # g
            'sex':            [None, None, 'male', 'female'],
        }
        d2 = p1.find_winner()
        self.assertEqual(d2['penguin id'], 103)                                  # exact id
        self.assertEqual(d2['BMI score'], 222.222)                                # 5/(0.15^2) rounded to 3 decimals
        self.assertEqual((d2['species'], d2['island'], d2['year']), ('C', 'I3', 2009))
        self.assertEqual((d2['bill_length_mm'], d2['bill_depth_mm']), (37.5, None))




        # example 3 same BMI
        p2 = Pendata("penguins.csv")
        p2.data_dict = {
            'num':            [10, 11],
            'species':        ['A', 'B'],
            'island':         ['I1','I2'],
            'year':           [2007,2008],
            'bill length':    [39.0, 41.0],
            'bill depth':     [19.0, 18.0],
            'flipper length': [200, 200],
            'body mass':      [4000,4000],  # both BMI = 4.0/0.2^2 = 100
            'sex':            [None, None],
        }
        self.assertEqual(p2.find_winner()['penguin id'], 10)                    # stable tie → first wins


        # example 4 invalid row
        p3 = Pendata("penguins.csv")
        p3.data_dict = {
            'num':            [1,2],
            'species':        ['A','B'],
            'island':         ['I1','I2'],
            'year':           [2007,2008],
            'bill length':    [None, None],
            'bill depth':     [None, None],
            'flipper length': [None, None],  
            'body mass':      [None, None],   
            'sex':            [None, None],
        }
        self.assertEqual(p3.find_winner(), {"error": "No valid penguins found"})

        

    

    



def main():
    penguin = Pendata("penguins.csv")
    penguin.build_data_dict()

    groups = penguin.data_species()
    rows = penguin.ave_species_group(groups)
    write_bill_csv(rows, 'penguins_bill_stats.csv')

    winner_inf = penguin.find_winner()
    winner_txt(winner_inf, 'winner.txt')




if __name__ == '__main__':
    """
    test all methods
    """
    unittest.main(verbosity=2, exit=False)


    """
    generate the files.
    """
    main()






            


            









