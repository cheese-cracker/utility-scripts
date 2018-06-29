"""
Assumes json file of js-array-object with dict like [{},{}]
"""
import json


def jsonmerger(mainjson, file_list):
    for auxid, file_name in enumerate(file_list, start=9):
        # Open
        with open(file_name, 'r') as working_file:
            auxjson = json.load(working_file)

        for organ in auxjson:
            mainorg = (next(org for org in mainjson if org['name'] ==
                       organ['name']), None)
            if mainorg:
                for ky, val in organ.items():
                    mainorg[ky+str(auxid).zfill(2)] = val
            # else:
                # mainorg.append(organ)


# file_name and file_list
FILE_LIST = ["gsoc"+str(x).zfill(2)+".json" for x in range(17, 8, -1)]
file_name = FILE_LIST[-1]
# Open mainjson
with open(file_name, 'r') as working_file:
        mainjsonfl = json.load(working_file)
# Run
jsonmerger(mainjsonfl, FILE_LIST[:-1])
# Close
with open(file_name, 'w') as final_file:
    final_file.write(json.dumps(mainjsonfl))
