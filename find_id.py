"""Search for test case ID numbers, which contains the pattern."""
from argparse import ArgumentParser

from pathlib import Path


def id_number(row: str) -> str:
    """Check and return test ID number."""
    index = row.find("4AP2-")
    if index != -1:
        return row[index:].split(" ")[0]
    return ""


def find_space_count(row: str, pattern: str) -> int:
    """Search for space before def and method with pattern."""
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
    """Search for function definition and returns as new pattern."""
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

    for element in rows_with_patterns:
        pats = []
        pat = element.split("(")[0]
        for text in read_text:
            if text.find(pat) != -1:
                pats.append(pat)
        if len(pats) == 1:
            index = element.find("def ")
            new_patterns.append(element[index + 4 :].split("(")[0] + "(")

    return new_patterns


def find_function_name(path: Path, find_pattern: str) -> list:
    """Search for function, which contains given pattern definition,
    and returns function name as string.
    """

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


def find_test_id(source_path: Path, find_pattern: str) -> list:
    """Search for test ID number, which contains given pattern."""
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
    """Search pattern in methods. If method contains given pattern,
    returns function name as new pattern.
    """

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


def find_tests(
    source_path: Path,
    patterns: list,
    test_ids: list = [],
    pattern_searched: list = [],
    rec: int = 6,
) -> list:
    """Find test ID numbers, which contains given pattern.
    Search for new pattern in methods, in which given pattern is used
    """

    for pattern in patterns:
        if pattern not in pattern_searched:
            test_ids.extend(find_test_id(source_path=source_path, find_pattern=pattern))
            new_patterns = find_new_patterns(
                source_path=source_path, find_pattern=pattern
            )
            pattern_searched.extend(patterns)
            rec -= 1

    if rec > 1 and new_patterns:
        find_tests(
            source_path=source_path,
            patterns=new_patterns,
            test_ids=test_ids,
            pattern_searched=pattern_searched,
            rec=rec,
        )

    print(len(set(test_ids)))
    print(pattern_searched)
    return set(test_ids)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(
        description="Search for test case ID number, which contains the pattern."
    )
    parser.add_argument("DIR", help="Directory to search in", type=Path)
    parser.add_argument("PATTERN", help="Pattern to search for", type=str)
    args = parser.parse_args()
    print(find_tests(source_path=args.DIR, patterns=[args.PATTERN]))
