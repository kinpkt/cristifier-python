import requests

WCA_API_URL = 'https://www.worldcubeassociation.org/api/v0/competitions'

GENDER_DICT = {'m': 'Male', 'f': 'Female', 'o': 'Others'}

def VALIDATE_CAP(name):
    splitted = name.split(' ')
    for part in splitted:
        if not part[0].isupper():
            return False

def get_wcif(comp_id):
    response = requests.get(f'{WCA_API_URL}/{comp_id}/wcif/public')
    wcif = response.json()
    return wcif

def sort_alphabetically(arr):
    output_arr = [['ID', 'WCA ID', 'Name', 'Gender', 'Country', 'Sign', 'Remark']]
    sorted_arr = sorted(arr, key=lambda x: x[2])

    merged_arr = output_arr + sorted_arr

    return merged_arr

def sort_competitors(wcif):
    comp_name = wcif['name']
    persons = wcif['persons']

    reg_1st_arr = []
    reg_ret_arr = []

    # Looping through person list
    for cpt in persons:
        if cpt['registration'] is None or cpt['registration']['status'] != 'accepted':
            continue
        no_local = cpt['name'].split(' (')
        name_no_local = no_local[0].split(' ')[:2]

        # Checking bad cases for names
        if len(name_no_local) < 2:
            print(f'Error : {cpt["name"]} \nThis competitior has no surname.')
        elif '(' in name_no_local[1]:
            print(f'Error : {cpt["name"]} \nThis competitior has no space between English name and local name.')
        elif '  ' in cpt['name']:
            print(f'Error : {cpt["name"]} \nThis competitior has double space in their name.')
        elif VALIDATE_CAP(no_local[0]):
            print(f'Error : {cpt["name"]} \nThis competitior has incorrect capitalization in their name.')
        
        reg_row = [str(cpt['registrantId']), cpt['wcaId'], no_local[0], GENDER_DICT[cpt['gender']], cpt['countryIso2']]
        
        # Checking if person is first-timer or not
        if cpt['wcaId'] is None:
            reg_row[1] = ''
            reg_1st_arr.append(reg_row)
        else:
            reg_ret_arr.append(reg_row)

        reg_1st = sort_alphabetically(reg_1st_arr)
        reg_ret = sort_alphabetically(reg_ret_arr)

    return [comp_name, reg_1st, reg_ret]