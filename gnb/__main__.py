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
    subparser1_args.add_argument("GISAID_json", help="""json metadata.json.bz2
                                 format""")
    subparser1_args.add_argument("BioProject", help="""NCBI bioproject
                                 accession.""")
    subparser1_args.add_argument("-r", "--replacement", help="""Missing value
                                 replacement string.  """, default="missing",
                                 choices=["not collected", "not applicable",
                                          "missing"],
                                 type=str, required=False)
    subparser1_args.add_argument("-b", "--bzgrep_regex", help="""Regex to
                                 pre-filter gisaid.json.bz2 file to decrease
                                 processing time.""",
                                 type=str, required=False,
                                 default='Australia|Timor\-Leste|Oceania')
    subparser2_args = argparse.ArgumentParser(add_help=False)
    subparser2_args.add_argument("BioSample_attributes", help="BioSample attributes.tsv")
    subparser2_args.add_argument("GISAID_upload", help="GISAID template")
    subparser2_args.add_argument("SRA_template", help="SRA_metadata_acc.xlsx") #Must save spreadsheet under second tab (SRA_data) as a TSV (tab-delimited file) to upload the TSV file for the SRA metadata tab.
    subparser3_args = argparse.ArgumentParser(add_help=False)
    subparser3_args.add_argument("GISAID_json", help="""json metadata.json.bz2
                                 format""") #perhaps this should be removed and subparser1 used instead
    subparser4_args = argparse.ArgumentParser(add_help=False)
    subparser4_args.add_argument("-d", "--drop", help="""Columns to drop
                                 from output table.  For more than one column,
                                 use the -d option again. For column names
                                 containing spaces, escape the space with
                                 a backslash.""",
                                 required=False)
    subparser_modules = parser.add_subparsers(
        title="Sub-commands help", help="", metavar="", dest="subparser_name")
    subparser_modules.add_parser(
        "merge_bsmp", help="Merge metadata for SARS-CoV-2 NCBI BioSample submission.",
        description="Merge metadata for SARS-CoV-2 NCBI BioSample submission.",
        parents=[subparser1_args, subparser4_args],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser_modules.add_parser(
        "merge_sra", help="Merge metadata for SARS-CoV-2 NCBI SRA submission.",
        description="Merge metadata for SARS-CoV-2 NCBI SRA submission.",
        parents=[subparser2_args],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser_modules.add_parser(
        "view_gsd", help="View the GISAID_json as a tab-delimited table.",
        description="Get tab-delimited format of GISAID_json",
        parents=[subparser3_args, subparser4_args],
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
    # print(args)
    # print(type(args.drop))
    # sys.exit()

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
        # import bz2
        # import zipfile
        # print(help(bz2))
        # infile = zipfile.ZipFile(infiles['GISAID_json'])#.ZipInfo.compress_type
        # print(infile)
        # if zipfile.ZIP_BZIP2(infiles['GISAID_json']):
            # print('ZIPPED')
        GISAIDjson     = Table(infiles['GISAID_json']).gisaid_json(args.replacement,
                                                                   args.drop,
                                                                   args.bzgrep_regex)
        # print(GISAIDjson)
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
        df = sra_to_upload.sra_builder(gisaid_upload,
                                       bsmpl_attributes,
                                       sra_table)
        print(df.to_csv(sep="\t", index_label='biosample_accession'))

    elif args.subparser_name == "view_gsd":
        from .utils.table_maker import Table
        json_f = Table(args.GISAID_json)
        # print(json_f)
        df = json_f.gisaid_json("unknown", args.drop)
        print(df.to_csv(sep="\t"))
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