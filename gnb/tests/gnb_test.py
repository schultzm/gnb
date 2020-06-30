"""
Unit Tests.

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.

"""

import unittest
from .. import (__parent_dir__,
                __test_NCBI_up__,   
                __test_GISAID_up__,
                __test_GISAID_dwn__)
import pkg_resources
from ..utils.table_maker import Table, merge_biosample_dfs


class MergeTestCasePass(unittest.TestCase):
    def setUp(self):
        self.NCBIup    = pkg_resources.resource_filename(__parent_dir__,
                                                         __test_NCBI_up__)
        self.GISAIDup  = pkg_resources.resource_filename(__parent_dir__,
                                                         __test_GISAID_up__)
        self.GISAIDdwn = pkg_resources.resource_filename(__parent_dir__,
                                                         __test_GISAID_dwn__)

    def versioner(self):
        from .. import __version__
        self.assertFalse(__version__ == None)

    def read_gisaid_template(self):
        GISAIDtemplate = Table(self.GISAIDup)
        df = GISAIDtemplate.gisaid_template("missing")
        self.assertEqual(df.iloc[0].loc["submitter"], "Mark Schültz")

    def read_ncbi_template(self):
        NCBItemplate = Table(self.NCBIup)
        df = NCBItemplate.ncbi_template()
        self.assertEqual(df.columns[0], "*sample_name")

    def read_GISAID_json(self):
        GISAIDjson = Table(self.GISAIDdwn)
        df = GISAIDjson.gisaid_json("missing", "sequence")
        self.assertEqual(df.iloc[0,0], "achcov19/Xla/XC81/2121")

    def merger_BioSample_upload(self):
        ncbiup     = Table(self.NCBIup).ncbi_template()
        gisaidup   = Table(self.GISAIDup).gisaid_template("missing")
        gisaidjson = Table(self.GISAIDdwn).gisaid_json("missing")
        merged     = merge_biosample_dfs(ncbiup,
                               gisaidup,
                               gisaidjson,
                               "PRJNA613958",
                               "missing")
        self.assertEqual(merged.iloc[1].loc["host_age"], "65")
