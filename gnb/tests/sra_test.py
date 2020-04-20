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
                __test_GISAID_up__,
                __test_NCBI_SMPL__,
                __test_SRA_up__     )
import pkg_resources
from ..utils.sra_builder import SRA_table


class SRATestCasePass(unittest.TestCase):
    def setUp(self):
        self.GISAIDup  = pkg_resources.resource_filename(__parent_dir__,
                                                         __test_GISAID_up__)
        self.NCBIbsmpl = pkg_resources.resource_filename(__parent_dir__,
                                                         __test_NCBI_SMPL__)
        self.SRAup     = pkg_resources.resource_filename(__parent_dir__,
                                                         __test_SRA_up__)

    def merger_SRA_upload(self):
        sra_table = SRA_table(self.SRAup)#, self.NCBIbsmpl, self.GISAIDup)
        sra_table.sra_template()
        self.assertEqual(sra_table, 'x')

