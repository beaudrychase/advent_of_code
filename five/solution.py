import re

from .utils import input_multiline

rule_line = re.compile(r"(\d+)\|(\d+)", re.MULTILINE)
splitter = re.compile(r"^$", re.MULTILINE)
proposed_order_line = re.compile(r"(\d+)")


class PageRule:
    must_precede: set[int]

    def __init__(self, must_precede: int):
        self.must_precede = {must_precede}

    def are_preceding_pages_valid(self, proceeding_pages: set[int]) -> bool:
        return not bool(self.must_precede & proceeding_pages)


def solution(input_value: str):
    rule_part, ordering_part = splitter.split(input_value)[0:2]
    rules = make_rules(rule_part)
    valid_orderings: list[list[int]] = get_selected_orderings_from_input(
        ordering_part, rules
    )
    total = sum_of_middle_pages(valid_orderings)
    return str(total)


def make_rules(block: str):
    rules: dict[int, PageRule] = dict()

    for match in rule_line.finditer(block):
        page_number, following_page_number = match.groups()
        page_number = int(page_number)
        following_page_number = int(following_page_number)
        if page_number not in rules:
            rules[page_number] = PageRule(following_page_number)
        else:
            rules[page_number].must_precede.add(following_page_number)
    return rules


def get_selected_orderings_from_input(
    block: str, rules: dict[int, PageRule], select_valid: bool = True
) -> list[list[int]]:
    order_lines = get_all_orderings(block)
    selected_order_lines = list()
    for order_line in order_lines:
        if select_valid == is_single_ordering_valid(order_line, rules):
            selected_order_lines.append(order_line)
    return selected_order_lines


def get_all_orderings(block: str) -> list[list[int]]:
    order_lines = [
        proposed_order_line.findall(line)
        for line in block.splitlines()
        if len(proposed_order_line.findall(line)) > 0
    ]
    parsed_lines = list()
    for line_matches in order_lines:
        line_pages = list()
        for match in line_matches:
            page = match
            line_pages.append(int(page))
        parsed_lines.append(line_pages)
    return parsed_lines


def is_single_ordering_valid(order_line: list[int], rules: dict[int, PageRule]) -> bool:
    proceeding_pages = set()
    for page_number in order_line:
        if page_number in rules and not rules[page_number].are_preceding_pages_valid(
            proceeding_pages
        ):
            return False
        proceeding_pages.add(page_number)
    return True


def sum_of_middle_pages(orderings: list[list[int]]):
    return sum((ordering[len(ordering) // 2] for ordering in orderings))


def solution_two(input_value: str):
    rule_part, ordering_part = splitter.split(input_value)[0:2]
    rules = make_rules(rule_part)
    invalid_orderings: list[list[int]] = get_selected_orderings_from_input(
        ordering_part, rules, select_valid=False
    )
    fixed_orderings = fix_orderings(invalid_orderings, rules)
    total = sum_of_middle_pages(fixed_orderings)
    return str(total)


def fix_orderings(invalid_orderings: list[list[int]], rules: dict[int, PageRule]):
    result = list()
    for ordering in invalid_orderings:
        result.append(fix_single_ordering(ordering, rules))
    return result


def fix_single_ordering(ordering: list[int], rules: dict[int, PageRule]):
    unordered_pages = set(ordering)
    preceeding_pages = set()

    def order_unordered_pages(
        ordering: list[int],
    ):
        if len(unordered_pages) == 0:
            return ordering

        for page in unordered_pages:
            if page not in rules or rules[page].are_preceding_pages_valid(
                preceeding_pages
            ):
                ordering.append(page)
                preceeding_pages.add(page)
                unordered_pages.remove(page)
                path_result = order_unordered_pages(ordering)

                if len(path_result):
                    return path_result
                else:
                    ordering.pop(-1)
                    preceeding_pages.remove(page)
                    unordered_pages.add(page)
        return []

    ordering = order_unordered_pages([])
    return ordering


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
    print(solution_two(input_value))
