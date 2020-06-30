#!/usr/bin/env python3 

"""
    This module does the heavy lifting of building the tables.

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.
"""

import pandas as pd


class Table():
    def __init__(self, indata):
        self.indata = indata

    def gisaid_template(self, unknown):
        df = pd.read_excel(self.indata, header=0, sheet_name=1)
        df.set_index("covv_virus_name", inplace=True)
        df = df.drop(df.index[0]) #drops the first row (=duplicated header)
        df.replace("unknown", unknown, inplace=True)
        return df

    def ncbi_template(self):
        df = pd.read_excel(self.indata, skiprows=12)
        return df

    def gisaid_json(self, unknown, todrop=None, bzgrep_regex=None):
        import json
        import bz2
        import os
        import shlex
        import re
        import sys
        from subprocess import Popen, PIPE
        if bzgrep_regex:
            bzgrep_regex = re.compile(rf"{bzgrep_regex}")
        # else:
        #     bzgrep_regex = re.compile(rf"")
        dfs = []
        with bz2.BZ2File(self.indata, "r") as file:
            for index, line in enumerate(file):
                df_dict = json.loads(line)
                if todrop:
                    for drop in todrop:
                        df_dict.pop(drop, None)
                else:
                    pass
                if bzgrep_regex and bzgrep_regex.search(' '.join(list(map(str, df_dict.values()))), re.IGNORECASE):
                    dfs.append(pd.DataFrame(df_dict, index=[df_dict["covv_virus_name"]]))
                elif bzgrep_regex is None:
                    dfs.append(pd.DataFrame(df_dict, index=[df_dict["covv_virus_name"]]))
                else:
                    pass
        dfs = pd.concat(dfs)
        dfs.replace("unknown", unknown, inplace=True)
        return dfs


def merge_biosample_dfs(ncbiup, gisaidup, gisaidjson, bioproject, unknown,
              organism="Severe acute respiratory syndrome coronavirus 2",
              host="Homo sapiens",
              host_disease="COVID-19"):
    """Merge the three tables
    
    Arguments:
        ncbiup {pd.DataFrame} -- The input template, to be populated for upload
        gisaidup {pd.DataFrame} -- The metadata as uploaded to GISAID
        gisaidjson {pd.DataFrame} -- The metadata including the GISAID number
                                     as downloaded from GISAID
        bioproject {str} -- NCBI bioproject accession
    
    Returns:
        pd.DataFrame -- stdout as TSV for NCBI biosample generation
    """
    # 1 get the epi numbers from gisaidjson into gisaidup
    ncbi = gisaidup.join(gisaidjson[["covv_accession_id"]])
    headers_NCBI_template = list(ncbiup.columns.values)
    for header in headers_NCBI_template:
        ncbi[header] = pd.Series()
    ncbi['sample_title'] = ncbi[["covv_accession_id"]].apply(lambda x: f"SARS-Cov-2 {x.name.split('/')[2]}" if x.isnull().any().any() else f"SARS-Cov-2 {x.name.split('/')[2]} (GISAID {x.values[0]})", axis=1)
    # 2 get and keep the headers for column order at end of table build
    ncbi["bioproject_accession"] = bioproject
    ncbi["*organism"] = organism
    ncbi["isolate"] = ncbi[["covv_accession_id"]].apply(lambda x: f"{x.name.split('/')[2]}", axis=1)
    ncbi["description"] = ncbi[["covv_accession_id"]].apply(lambda x: f"{unknown}" if x.isnull().any().any() else f"{x.values[0]}", axis=1)
    ncbi["*collected_by"] = ncbi[["covv_orig_lab"]].apply(lambda x: f"{x.values[0]}", axis=1)
    ncbi["*collection_date"] = ncbi[["covv_collection_date"]].apply(lambda x: f"'{x.values[0]}", axis=1)
    ncbi["*geo_loc_name"] = ncbi[["covv_location"]].apply(lambda x: f"{unknown}" if x.isnull().any().any() else f"{': '.join(x.values[0].split('/')[1:3])}", axis=1)
    ncbi["*host"] = host
    ncbi["*host_disease"] = host_disease
    ncbi["*isolation_source"] = unknown
    ncbi["*lat_lon"] = unknown
    ncbi["host_age"] = ncbi[["covv_patient_age"]].apply(lambda x: f"{unknown}" if x.isnull().any().any() else f"{x.values[0]}", axis=1)
    ncbi["host_sex"] = ncbi[["covv_gender"]].apply(lambda x: f"{unknown}" if x.isnull().any().any() else f"{x.values[0]}", axis=1)
    ncbi["*sample_name"] = ncbi.index.values
    ncbi["passage_history"] = ncbi[["covv_passage"]].apply(lambda x: f"{unknown}" if x.isnull().any().any() else f"{x.values[0]}", axis=1)
    ncbi2 = ncbi[headers_NCBI_template]
    return ncbi2
