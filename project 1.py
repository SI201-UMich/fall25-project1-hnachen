# name Sihan Chen
# student id: 2563 8460
# email: hnachen@umich.edu

import os
import unittest

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
        for line in self.data[1:]:
            line = line.strip()
            if not line:
                continue

            separated = line.split(',')
            if len(separated) < 9:
                continue


            self.data_dict['num'].apppend(int(separated[0].strip('"')))
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


            









