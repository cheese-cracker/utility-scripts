"""
Assumes json file of js-array-object with dict like [{},{}]
"""
import json


def mergerIO(merger_func):
    def wrapper(file_name, filenumzip):
        # Open mainjson
        with open(file_name, 'r') as working_file:
                mainjsonfl = json.load(working_file)
        # Run
        merger_func(mainjsonfl, filenumzip)
        # Close
        with open(file_name, 'w') as final_file:
            final_file.write(json.dumps(mainjsonfl))
    return wrapper


@mergerIO
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


# file_name and file_list moved to GSoCArchive
# Run File moved to GSoCArchive
