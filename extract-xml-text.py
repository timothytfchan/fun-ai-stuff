import re

def extract_xml_text(string: str, tag_list: list[str]) -> dict[str, list[str]]:
    """
    Extract text in between XML tags from a string. 
    Returns a dictionary with the tag names as keys and an ordered list of the text in between the tags as values.
    """
    result = {tag: [] for tag in tag_list}
    for tag in tag_list:
        # Create a regular expression pattern for the current tag
        pattern = f"<{tag}>(.*?)</{tag}>"
        # Find all matches of the pattern in the string
        matches = re.findall(pattern, string, re.DOTALL)
        # Add the matches to the corresponding tag in the result dictionary
        result[tag].extend(matches)
    return result