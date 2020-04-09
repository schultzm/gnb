# Generate NCBI biosample upload

[![CircleCI](https://circleci.com/gh/schultzm/gnb.svg?style=svg&circle-token=6be92d4e84abcddc32721c2c507b07c08810e327)](https://app.circleci.com/pipelines/github/schultzm/gnb)


Generate the NCBI biosample metadata sheet to get biosample numbers.  
Created for SARS-CoV-2 submissions, in an effort to ease the work required
to routinely merge
`GISAID_upload_table.xlsx+GISAID_download_metadata.json+NCBI_biosample_upload_table.xlsx`

View the [README on github pages](https://schultzm.github.io/gnb/)

Use it like this:

```{bash}
gnb
usage: gnb [-h]  ...

Generate SARS-CoV-2 NCBI Biosample upload table.

optional arguments:
  -h, --help  show this help message and exit

Sub-commands help:
  
    merge      Merge metadata for SARS-CoV-2 NCBI submission.
    version   Get the version number.
    test      Run gnb unittests.
```

## Run it

`gnb merge NCBI_upload.xlsx GISAID_upload.xls GISAID_json.json BioProject`

## Test it

`gnb test`

On running the test, you should see something like:  

```{bash}
versioner (gnb.tests.gnb_test.MergeTestCasePass) ... ok
read_gisaid_template (gnb.tests.gnb_test.MergeTestCasePass) ... ok
read_ncbi_template (gnb.tests.gnb_test.MergeTestCasePass) ... ok
read_GISAID_json (gnb.tests.gnb_test.MergeTestCasePass) ... ok
merger (gnb.tests.gnb_test.MergeTestCasePass) ... ok

----------------------------------------------------------------------
Ran 5 tests in 2.695s

OK
```

## Version it

`gnb version`

## Install it

Global installation:

`pip3 install git+https://github.com/schultzm/gnb.git`

Local installation:

`pip3 install git+https://github.com/schultzm/gnb.git --user`
