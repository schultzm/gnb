"""
Unit Test suite builder.

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.

"""

import unittest
from ..tests.gnb_test import MergeTestCasePass
from ..tests.sra_test import SRATestCasePass


def suite():
    """
    This is the test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(MergeTestCasePass("versioner"))
    suite.addTest(MergeTestCasePass("read_gisaid_template"))
    suite.addTest(MergeTestCasePass("read_ncbi_template"))
    suite.addTest(MergeTestCasePass("read_GISAID_json"))
    suite.addTest(MergeTestCasePass("merger_BioSample_upload"))
    suite.addTest(SRATestCasePass("merger_SRA_upload"))
    return suite