import os
from argparse import ArgumentParser

from pathlib import Path 


def id_number(row: str):
    if (index:= row.find("4AP2-")) !=-1:
        return row[index:].split(' ')[0]
    else:
        return None

def find_new_pattern(text_dict, keys):
    rows_with_patterns: list = []
    new_patterns: list = []
    for key in keys:
 
        for i in range(key):
            key -=1
            if text_dict[key].find('if __name__ =="__main__":') !=-1:
                break
            if text_dict[key].find('def ') !=-1:
                rows_with_patterns.append(text_dict[key])
                break
    for pattern in rows_with_patterns:
        if (index:= pattern.find("def ")) !=-1:
            new_patterns.append('.' + pattern[index+4:].split('(')[0])
    return new_patterns


def find_function_name(path, find_pattern):
    key_list = []
    count = 0
    text_dict: dict = {}
    read_text = Path(path).read_text(encoding='utf-8')
    for row in read_text.split('\n'):
        text_dict[count]=row
        count+=1
    for key, value in text_dict.items():
        if value.find(find_pattern) != -1:
          key_list.append(key)
    return find_new_pattern(text_dict=text_dict, keys=key_list)


def find_tests(source_path: Path = None, find_pattern: str = None) -> list:
    id_list: list = []
    path_list: list = []
    for file_name in source_path.rglob("*.py"):
        test_id: str = None
        read_text: str = Path(file_name).read_text(encoding='utf-8')

        for row in read_text.split('\n'):
            if row.find("Polarion ID") != -1:
                test_id = id_number(row=row)
            if row.find(find_pattern) != -1:
                if test_id:
                    id_list.append(test_id)
                else:
                    path_list.append(file_name)
    
    return id_list, path_list

if __name__ =="__main__":

    # parser: ArgumentParser = ArgumentParser(description="Search for test case ID number, which contains the pattern.")
    # parser.add_argument("PATTERN", help="Pattern to search for", type=str)
    # parser.add_argument("DIR", help="Directory to search in", type=Path)
    # args = parser.parse_args()

    # file_path = Path('C:/Users/marius.sutkus.QDTEAM/Documents/training/code/TestAutomation/procedures/program/cleaning.py')
    source_path = Path("C:/Users/marius.sutkus.QDTEAM/Documents/training/code/TestAutomation")
    # pattern = 'hydraulics_connector.reconnect_shunts('
    # pattern = 'cleaning.start_cleaning('
    pattern = 'reconnect_shunts('

    # source_path = Path("C:/Users/marius.sutkus.QDTEAM/Documents/training/code/test2")
    # pattern = 'file_name).read_text('
    test_id: list = []
    id_list, path_list = find_tests(source_path=source_path, find_pattern=pattern)
    print(path_list)
    # test_id.extend([id for id in set(id_list)])
    test_id.extend(id_list)
    patterns: list = []
    for path in path_list:
        patterns.extend(find_function_name(path=path, find_pattern=pattern))
    print(patterns)
    new_patterns: list = []
    for pattern in patterns:
        id_list, path_list = find_tests(source_path=source_path, find_pattern=pattern)
        test_id.append(id_list)
        print(path_list)
        new_patterns.extend(path_list)

    
    # print(test_id)
    # print(len(test_id))
    # print(new_patterns)