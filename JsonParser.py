import json
import os

'''Iterate over all files in argument path'''
def read_json(path):
    total_rename_count = 0
    for file_name in os.listdir(path):
        if file_name.endswith('.json'):
            with open(path + file_name, 'r') as f:
                print('\nParsing File ' + file_name + '\n')
                data = f.read()
                json_object = json.loads(data)
                total_rename_count += traverse_nodes(json_object)
                total_rename_count += traverse_loom_containers(json_object)
        print('END OF FILE ' + file_name +'\n\n')
    print('TOTAL RENAME COUNT: ' + str(total_rename_count))


def traverse_loom_containers(json_object):
    all_guids = json_object['nodes']
    columns = {}

    for guid in all_guids:
        node = json_object['nodes'][guid]
        if 'loomContainer' in node:
            deep_guids = node['loomContainer']['nodes']
            for deep_guid in deep_guids:
                if 'RenameColumn' in node['loomContainer']['nodes'][deep_guid]['nodeType']:
                    old_name = node['loomContainer']['nodes'][deep_guid]['columnName']
                    new_name = node['loomContainer']['nodes'][deep_guid]['rename']
                    columns[old_name] = new_name

    print_dict(columns)
    print('\nRENAME COUNT: ' + str(len(columns)))             
    return len(columns)


def traverse_nodes(json_object):
    node_guids = json_object['initialNodes']
    columns = {}
    
    for guid in node_guids:
        for action in json_object['nodes'][guid]['actions']:
            if 'RenameColumn' in action['nodeType']:
                old_name = action['columnName']
                new_name = action['rename']
                columns[old_name] = new_name

    print_dict(columns)
    print('\nRENAME COUNT: ' + str(len(columns)))
    return len(columns)

'''
def dedupe(dictionary):
    new_dict = {}

    for key in dictionary:
        if not key in new_dict or new_dict[key] != dictionary[key]:
            new_dict[key] = dictionary[key]

    return new_dict
'''

def print_dict(dictionary):
    for key in dictionary:
        print(key, '\t', dictionary[key])


def main():
    read_json('/Users/drew.engberson/Desktop/TableauFiles/')
    

if __name__ == '__main__':
    main()
