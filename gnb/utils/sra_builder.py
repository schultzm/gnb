"""
    This module does the heavy lifting of building the SRA upload table.

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.
"""

import pandas as pd

class SRA_table:
    def __init__(self, intable):
        self.intable = intable

    def sra_template(self):
        df = pd.read_excel(self.intable, header=0, sheet_name=1)
        self.sra_table_in = df
 
        # self.sra_template = sra_template
        # self.attributes_bsmpls = biosample_attributes
        # self. gisaid_upload = gisaid_upload

    def bsmpl_attributes(self):
        df = pd.read_csv(self.intable, header=0, sep="\t")
        self.bs_attr = df
    

    def create_sra_table(self):
        pass
    