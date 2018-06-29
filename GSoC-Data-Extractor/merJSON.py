"""
Assumes json file of js-array-object with dict like [{},{}]
"""
import json


def jsonmerger(mainjson, filenumzip):
    for auxid, file_name in filenumzip:
        # Open
        with open(file_name, 'r') as working_file:
            auxjson = json.load(working_file)

        for organ in auxjson:
            mainorg = next((org for org in mainjson if org['name'] ==
                            organ['name']), None)
            if mainorg:
                for ky, val in organ.items():
                    if ky != 'name':
                        mainorg[ky+str(auxid).zfill(2)] = val
            # else:
                # mainorg.append(organ)


# file_name and file_list
styrs = [str(x).zfill(2) for x in range(17, 8, -1)]
FILE_LIST = ["gsoc"+styr+".json" for styr in styrs]
file_name = FILE_LIST[0]
# Open mainjson
with open(file_name, 'r') as working_file:
        mainjsonfl = json.load(working_file)
# Run
jsonmerger(mainjsonfl, zip(styrs[1:], FILE_LIST[1:]))
# Close
with open(file_name, 'w') as final_file:
    final_file.write(json.dumps(mainjsonfl))
