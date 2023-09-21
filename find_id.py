import os
from argparse import ArgumentParser

from pathlib import Path


def id_number(row: str) -> str:
    index = row.find("4AP2-")
    if index != -1:
        return row[index:].split(" ")[0]
    else:
        return ""


def find_space_count(row: str, pattern: str) -> int:
    count = None
    row_split = row.split(" ")
    for string in row_split:
        if string.find(pattern) != -1:
            index = row.find(string)
            if index != -1:
                if index > 0:
                    spaces = row[:index]
                    if spaces.isspace():
                        count = len(spaces)
                else:
                    count = 0
    print(row)
    print(pattern)
    print(count)
    return count


def find_class_method(row: int, text: str) -> str:
    for i in reversed(range(row)):
        if text[i].find("class ") != -1:
            return text[i]
    return ""


def find_new_pattern(
    read_text, idx_list, pattern, path
):  # todo manage function in function by counting white spacec before def?
    rows_with_patterns: list = []
    new_patterns: list = []
    for idx in idx_list:
        count_p = find_space_count(row=read_text[idx], pattern=pattern)
        if not count_p or count_p < 4:
            continue

        for i in reversed(range(idx)):
            if read_text[i].find("def ") != -1:
                count_d = find_space_count(read_text[i], "def")
                if count_p > count_d:
                    if read_text[i - 1].find("@classmethod") == -1:
                        rows_with_patterns.append(read_text[i])
                        break
                    elif read_text[i - 1].find("@classmethod") != -1:
                        class_pattern = find_class_method(row=i, text=read_text)
                        print(path)
                        print(class_pattern)
                        print("def")
                        print(read_text[i])
                        print(count_d)
                        # rows_with_patterns.append(class_pattern)
                        break

                elif count_p <= count_d:
                    continue

    for pattern in rows_with_patterns:
        index_d = pattern.find("def ")
        # index_c = pattern.find("class ")

        if index_d != -1:
            new_patterns.append("." + pattern[index_d + 4 :].split("(")[0] + "(")
        # if index_c != -1:
        #     new_patterns.append("." + pattern[index + 4 :].split("(")[0]+"(")

    return new_patterns


def find_function_name(path, find_pattern):
    idx_list = []
    count = 0
    read_text = Path(path).read_text(encoding="utf-8").split("\n")
    for idx, text in enumerate(read_text):
        if text.find(find_pattern) != -1:
            idx_list.append(idx)
    return find_new_pattern(
        read_text=read_text, idx_list=idx_list, pattern=find_pattern, path=path
    )


def find_tests(source_path: Path, find_pattern: str) -> tuple[list, list]:
    id_list: list = []
    path_list: list = []
    for file_name in source_path.rglob("*.py"):
        test_id: str = ""
        read_text: str = Path(file_name).read_text(encoding="utf-8").split("\n")

        for row in read_text:
            if row.find("Polarion ID") != -1:  # and not test_id
                test_id = id_number(row=row)
                break

        for row in read_text:
            if row.find(find_pattern) != -1 and test_id:
                # if test_id:
                id_list.append(test_id)
                break
            if row.find(find_pattern) != -1 and not test_id:
                print(file_name)
                path_list.append(file_name)
                break
            else:
                continue

    return id_list, path_list


def start_function(source_path: Path, pattern: str) -> list:
    pattern_dict = {pattern: 0}
    test_ids: list = []

    for i in range(6):
        new_paths: list = []
        new_patterns: list = []
        for pat, value in pattern_dict.items():
            if value == 0:  #
                print(pat)
                id_list, path_list = find_tests(
                    source_path=source_path, find_pattern=pat
                )
                test_ids.extend(id_list)
                for path in path_list:
                    new_patterns.extend(find_function_name(path=path, find_pattern=pat))
                pattern_dict[pat] = 1

        for pattern in new_patterns:
            if pattern not in pattern_dict:
                pattern_dict[pattern] = 0
    print(len(test_ids))
    print(pattern_dict)
    return test_ids


if __name__ == "__main__":
    # parser: ArgumentParser = ArgumentParser(description="Search for test case ID number, which contains the pattern.")
    # parser.add_argument("PATTERN", help="Pattern to search for", type=str)
    # parser.add_argument("DIR", help="Directory to search in", type=Path)
    # args = parser.parse_args()

    # file_path = Path('C:/Users/marius.sutkus.QDTEAM/Documents/training/code/TestAutomation/procedures/program/cleaning.py')
    source_path = Path(
        "C:/Users/marius.sutkus.QDTEAM/Documents/training/code/TestAutomation"
    )
    pattern = "reconnect_shunts("
    # pattern = 'cleaning.start_cleaning('
    print(start_function(source_path=source_path, pattern=pattern))
