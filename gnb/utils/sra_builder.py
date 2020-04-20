"""
    This module does the heavy lifting of building the SRA upload table.

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.
"""

MACHINES = {"Illumina NextSeq 550": "NextSeq 550",
            "Illumina iSeq": "Illumina iSeq 100",
            "Illumina NextSeq 500": "NextSeq 500"}
METHODS = "Using minimap2, short reads mapped to SARS-CoV-2 NCBI accession MN908947.3. Using samtools, proper_pairs (samflag 2) mapping to MN908947.3 retained, unmapped reads (samflag 4) discarded (to filter out non-SARS-CoV-2 cDNA). Filtered reads submitted to NCBI"

# print(MACHINES["Illumina NextSeq 550"])
import pandas as pd

class SRA_table:
    # def __init__(self, intable):
    #     self.intable = intable

    def sra_template(self, intable):
        df = pd.read_excel(intable, header=0, sheet_name=1)
        return df
 
        # self.sra_template = sra_template
        # self.attributes_bsmpls = biosample_attributes
        # self. gisaid_upload = gisaid_upload

    def bsmpl_attributes(self, intable):
        df = pd.read_csv(intable, header=0, sep="\t", index_col=2)
        return df
    

    def read_gisaid_metadata(self, intable):
        df = pd.read_excel(intable, header=1, sheet_name=1, index_col=2)
        # df = df.drop(df.index[0])
        return df

    def sra_builder(self, gisaid_up,
                    biosample_attributes,
                    sra_table):
        df = pd.concat([gisaid_up, biosample_attributes], axis=1)
        df.set_index("accession", inplace=True)
        # below will make the sra_table and df have the same index.values
        sra_table['biosample_accession'] = pd.Series(df.index.values).apply(lambda x: f"{x}")
        # sra_table['library_ID']
        sra_table.set_index("biosample_accession", inplace=True)
        sra_table2 = pd.concat([sra_table, df], axis=1)
        sra_table2['library_ID'] = sra_table2[['isolate']].apply(lambda x: f"{x.values[0]}_illumina", axis=1)
        sra_table2['title'] = "Severe acute respiratory syndrome coronavirus 2"
        sra_table2['library_strategy'] = "AMPLICON"
        sra_table2['library_source'] = "VIRAL RNA"
        sra_table2['library_selection'] = "PCR"
        sra_table2['library_layout'] = "paired"
        sra_table2['platform'] = "ILLUMINA"
        # print(sra_table2.columns)
        # print(sra_table2[['Sequencing technology']])
        # print(sra_table2.dtypes)
        sra_table2["instrument_model"] = sra_table2[['Sequencing technology']].apply(lambda x: f"{MACHINES[x.values[0]]}", axis=1)
        sra_table2['design_description'] = sra_table2[["Assembly method"]].apply(lambda x: f"{x.values[0]}.q {METHODS}", axis=1)
        sra_table2["filetype"] = "fastq"
        sra_table2["filename"] = sra_table2[["isolate"]].apply(lambda x: f"{x.values[0]}_R1.fq.gz", axis=1)
        sra_table2["filename2"] =  sra_table2[["isolate"]].apply(lambda x: f"{x.values[0]}_R2.fq.gz", axis=1)
        # print(sra_table2["instrument_model"])
        # sra_table['library_ID'] = df[]
        return sra_table2[sra_table.columns]
    