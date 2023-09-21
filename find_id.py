import os
from argparse import ArgumentParser

from pathlib import Path


def id_number(row: str) -> str:
    index = row.find("4AP2-")
    if index != -1:
        return row[index:].split(" ")[0]
    return ""


def find_space_count(row: str, pattern: str) -> int:
    count = None
    if pattern.find(" = ") != -1:
        row_split = row.split("    ")
        for element in row_split:
            if element.find(pattern) != -1:
                index = row.find(element)
                if index != -1 and index > 0:
                    spaces = row[:index]
                    if spaces.isspace():
                        count = len(spaces)
    else:
        row_split = row.split(" ")
        for string in row_split:
            if string.find(pattern) != -1:
                index = row.find(string)
                if index != -1 and index > 0:
                    spaces = row[:index]
                    if spaces.isspace():
                        count = len(spaces)
                else:
                    count = 0
    return count


def find_new_pattern(read_text: str, idx_list: list, pattern: str) -> list:
    rows_with_patterns: list = []
    new_patterns: list = []

    for idx in idx_list:
        count_p = find_space_count(row=read_text[idx], pattern=pattern)
        if count_p is None:
            if read_text[idx].find(" = ") != -1:
                count_p = find_space_count(row=read_text[idx], pattern=" = " + pattern)
                if count_p is None:
                    continue
            else:
                continue
        for line in reversed(range(idx)):
            if read_text[line].find("def ") != -1:
                count_d = find_space_count(read_text[line], "def")
                if count_d is None:
                    continue
                if count_p > count_d:
                    rows_with_patterns.append(read_text[line])
                    break

    for pattern in rows_with_patterns:
        pats = []
        pat = pattern.split("()")[0]
        for text in read_text:
            if text.find(pat) != -1:
                pats.append(pat)
        if len(pats) == 1:
            index = pattern.find("def ")
            new_patterns.append(pattern[index + 4 :].split("(")[0] + "(")

    return new_patterns


def find_function_name(path: Path, find_pattern: str) -> list:
    idx_list = []
    read_text = Path(path).read_text(encoding="utf-8").split("\n")

    for idx, text in enumerate(read_text):
        if text.find(find_pattern) != -1:
            if text.find("def ") == -1:
                idx_list.append(idx)

    new_pattern = find_new_pattern(
        read_text=read_text, idx_list=idx_list, pattern=find_pattern
    )
    return new_pattern


def find_tests(source_path: Path, find_pattern: str) -> list:
    id_list: list = []
    source_path = source_path / "test_cases"

    for file_name in source_path.rglob("*.py"):
        test_id: str = ""

        for row in Path(file_name).read_text(encoding="utf-8").split("\n"):
            if row.find("Polarion ID") != -1:  # and not test_id
                test_id = id_number(row=row)
                break

        for row in Path(file_name).read_text(encoding="utf-8").split("\n"):
            if row.find(find_pattern) != -1 and test_id:
                id_list.append(test_id)
                break

    return id_list


def find_new_patterns(source_path: Path, find_pattern: str) -> list:
    pattern_list: list = []
    for file_name in source_path.rglob("*.py"):
        if str(file_name).find("test_cases") != -1:
            continue

        for row in Path(file_name).read_text(encoding="utf-8").split("\n"):
            if row.find(find_pattern) != -1:
                result = find_function_name(path=file_name, find_pattern=find_pattern)
                pattern_list.extend(result)
                break

    filtered_list: list = []
    for pattern in pattern_list:
        if pattern_list.count(pattern) == 1:
            filtered_list.append(pattern)

    return pattern_list


def start_function(source_path: Path, pattern: str) -> list:
    pattern_dict = {pattern: 0}
    test_ids: list = []

    for i in range(6):
        new_patterns: list = []
        for pat, value in pattern_dict.items():
            if value == 0:  #
                test_ids.extend(find_tests(source_path=source_path, find_pattern=pat))
                new_patterns.extend(
                    find_new_patterns(source_path=source_path, find_pattern=pat)
                )
                pattern_dict[pat] = 1

        for pattern in new_patterns:
            if pattern not in pattern_dict:
                pattern_dict[pattern] = 0
    print(len(set(test_ids)))
    print(pattern_dict)
    return set(test_ids)


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
