# add metadata form link to lychee report
# the link is found in the .yaml version of the metadata record while we are checking the xml version for urls

import re

report_filename = './lychee/out.md'

with open(report_filename, "r") as f:
    data = f.readlines()

for index, row in enumerate(data):
    filenames = re.findall(r'### Errors in (.*)\.xml', row)
    if filenames:
        with open(f'{filenames[0]}.yaml', mode="rt", encoding="utf-8") as yamlFile:
            yaml = yamlFile.read()
            formURL = re.findall(r'maintenance_note: Generated from (.*)\n', yaml)
        if formURL:
            data[index] = f'### Errors in {filenames[0]}.xml [form link]({formURL[0]})\n'

with open(report_filename, "w") as f:
    f.writelines(data)



