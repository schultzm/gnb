"""
Use this program for merging a SARS-CoV-2 GISAID metadata upload
sheet (*.xls) with a GISAID metadata download (*.json containing GISAID
accession numbers) and an NCBI biosample template upload (*.xlsx).  Reformats
missing data, fixes column headers, fixes cell values, avoids the mess of
manual handling of sheets within excel using vlookup, manual editing,
concatenations, dates, etc.
Also, use this for creating the SRA table upload. This will output a TSV
(tab-delimited file) for upload to SRA.

    Merge SARS-CoV-2 *.xls, *.xlsx and *.json files for NCBI biosample upload.
    Merge tables for SRA sample upload.
    Copyright (C) 2020 Dr Mark B Schultz dr.mark.schultz@gmail.com
    https://github.com/schultzm/gnb.git GNU Affero General Public License
    <https://www.gnu.org/licenses/>.
"""

def main():
    
    """Perform the main routine."""
    import argparse
    from pathlib import Path, PurePath
    import sys

    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description="""Generate SARS-CoV-2 NCBI Biosample 
                        or SRA upload tables.
                        """)
    subparser1_args = argparse.ArgumentParser(add_help=False)
    subparser1_args.add_argument("NCBI_upload", help="NCBI template")
    subparser1_args.add_argument("GISAID_upload", help="GISAID template")
    subparser1_args.add_argument("GISAID_json", help="json metadata")
    subparser1_args.add_argument("BioProject", help="""NCBI bioproject
                                 accession.""")
    subparser1_args.add_argument("-r", "--replacement", help="""Missing value
                                 replacement string.  """, default="missing",
                                 choices=["not collected", "not applicable",
                                          "missing"],
                                 type=str, required=False)
    subparser2_args = argparse.ArgumentParser(add_help=False)
    subparser2_args.add_argument("BioSample_attributes", help="BioSample attributes.tsv")
    subparser2_args.add_argument("GISAID_upload", help="GISAID template")
    subparser2_args.add_argument("SRA_template", help="SRA_metadata_acc.xlsx") #Must save spreadsheet under second tab (SRA_data) as a TSV (tab-delimited file) to upload the TSV file for the SRA metadata tab.
    subparser_modules = parser.add_subparsers(
        title="Sub-commands help", help="", metavar="", dest="subparser_name")
    subparser_modules.add_parser(
        "merge_bsmp", help="Merge metadata for SARS-CoV-2 NCBI BioSample submission.",
        description="Merge metadata for SARS-CoV-2 NCBI BioSample submission.",
        parents=[subparser1_args],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser_modules.add_parser(
        "merge_sra", help="Merge metadata for SARS-CoV-2 NCBI SRA submission.",
        description="Merge metadata for SARS-CoV-2 NCBI SRA submission.",
        parents=[subparser2_args],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    subparser_modules.add_parser(
        "version", help="""Get the version number.""",
        description="Get the version number.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparser_modules.add_parser(
        "test", help="""Run gnb unittests.""",
        description="Run gnb unittests.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()

    if not args.subparser_name:
        parser.print_help()
    elif args.subparser_name == "merge_bsmp":
        from .utils.table_maker import Table, merge_biosample_dfs
        infiles = {'GISAID_upload': Path(args.GISAID_upload),
                   'NCBI_upload'  : Path(args.NCBI_upload),
                   'GISAID_json'  : Path(args.GISAID_json)}
        exit_cue = False
        for key in infiles:
            if not infiles[key].is_file():
                exit_cue = True
                print(f"File not found: {infiles[key]}", file=sys.stderr)
            else:
                pass
        if exit_cue:
            sys.exit()
        GISAIDtemplate = Table(infiles['GISAID_upload']).gisaid_template(args.replacement)
        NCBItemplate   = Table(infiles['NCBI_upload']).ncbi_template()
        GISAIDjson     = Table(infiles['GISAID_json']).gisaid_json(args.replacement)
        merged = merge_biosample_dfs(NCBItemplate,
                           GISAIDtemplate,
                           GISAIDjson,
                           args.BioProject,
                           args.replacement)
        print(merged.to_csv(sep="\t", index=False))

    elif args.subparser_name == "merge_sra":
        from .utils.sra_builder import SRA_table 
        infiles = {'GISAID_upload'    : Path(args.GISAID_upload),
                   'NCBI_attributes'  : Path(args.BioSample_attributes),
                   'SRA_template'     : Path(args.SRA_template)}
        # print(infiles)
        exit_cue = False
        for key in infiles:
            if not infiles[key].is_file():
                exit_cue = True
                print(f"File not found: {infiles[key]}", file=sys.stderr)
            else:
                pass
        if exit_cue:
            sys.exit()
        gisaid_upload = SRA_table().read_gisaid_metadata(infiles['GISAID_upload'])
        bsmpl_attributes = SRA_table().bsmpl_attributes(infiles['NCBI_attributes'])
        sra_table = SRA_table().sra_template(infiles['SRA_template'])
        sra_to_upload = SRA_table()
        # print(gisaid_upload)
        # print(bsmpl_attributes)
        # print(sra_table)
        df = sra_to_upload.sra_builder(gisaid_upload,
                                       bsmpl_attributes,
                                       sra_table)
        print(df.to_csv(sep="\t", index_label='biosample_accession'))


    elif args.subparser_name == "version":
        from . import __version__
        print(__version__)
    elif args.subparser_name == "test":
        import unittest
        from .tests.test_suite import suite
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite())


if __name__ == "__main__":
    main()