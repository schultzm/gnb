
"""
gnb init.py

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.

"""

__version__         = "0.0.4"
__parent_dir__      = "gnb"
__test_NCBI_up__    = "data/dummy_BiosampleBuilder.xlsx"
__test_GISAID_up__  = "data/dummy_BuilkUpload.xls"
__test_GISAID_dwn__ = "data/dummy.json"
__test_NCBI_SMPL__  = "data/attributes.tsv"
__test_SRA_up__     = "data/SRA_metadata_acc.xlsx"
__description__     = "Build metadata tables for NCBI biosample/SRA submission"
__download_url__    = "https://github.com/schultzm/gnb.git"
__author__          = "Mark B Schultz"
__author_email__    = "dr.mark.schultz@gmail.com"
__license__         = "AGPL-3.0"