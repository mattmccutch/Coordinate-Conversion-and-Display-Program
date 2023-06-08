import re


def contains_degree_symbol(s):
    pattern = '°'
    if re.search(pattern, s):
        return True
    else:
        return False


# Test the function
print(contains_degree_symbol("Hello World"))  # False
print(contains_degree_symbol("Temperature is 25°"))  # True
print(contains_degree_symbol("40°42'45.9936\"N, 74°0'21.5064\"W"))  # True
