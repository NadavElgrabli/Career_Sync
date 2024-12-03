import re


def find_degree_fields(text):
    """
    Extracts academic degree fields from the given text using regular expressions.

    Parameters:
    text (str): The input text containing academic degree information.

    Returns:
    list: A list of extracted academic degree fields.
    """
    # Define a regex pattern to match degrees followed by fields of study
    pattern = r"""
        (?:
            # Matches 'Bachelor(s) or Master(s) in [Fields]'
            (?P<degree1>Bachelors?|Masters?)\s*(?:of\s+\w+)?\s*(?:or\s+Bachelors?|or\s+Masters?)?\s*in\s+(?P<fields1>[^\.]+) |
            # Matches 'Bachelor of [Degree Type] in [Field]'
            (?P<degree2>Bachelor)\s+of\s+[\w\.]+\s+in\s+(?P<field2>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches 'Master of [Degree Type] in [Field]'
            (?P<degree3>Master)\s+of\s+[\w\.]+\s+in\s+(?P<field3>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches abbreviations like 'B.S. in [Field]'
            (?P<degree4>B\.[A-Z]\.)\s+in\s+(?P<field4>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches abbreviations like 'M.A. in [Field]'
            (?P<degree5>M\.[A-Z]\.)\s+in\s+(?P<field5>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches 'PhD in [Field]' or 'Ph.D. in [Field]'
            (?P<degree6>Ph\.?D\.?)\s+in\s+(?P<field6>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches 'Doctorate in [Field]'
            (?P<degree7>Doctorate)\s+in\s+(?P<field7>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches 'degree in [Field]'
            degree\s+in\s+(?P<field8>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches 'studied [Field]'
            studied\s+(?P<field9>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$) |
            # Matches 'major in [Field]' or 'majored in [Field]'
            major(?:ed)?\s+in\s+(?P<field10>[A-Za-z\s&\-\(\)]+?)(?= and |,|\.|$)
        )
    """

    # Find all matches in the text
    matches = re.finditer(pattern, text, re.IGNORECASE | re.VERBOSE)

    fields = []

    for match in matches:
        # Check if 'fields1' group matched (handles multiple fields)
        if match.group('fields1'):
            # Split the fields by commas and conjunctions like 'and' or 'or'
            fields_list = re.split(r',|\band\b|\bor\b', match.group('fields1'))
            for field in fields_list:
                field = field.strip()
                # Exclude phrases like 'related work experience' if needed
                if 'related work experience' not in field.lower():
                    fields.append(field)
        else:
            # Extract other fields from named groups
            for key in match.groupdict():
                if key.startswith('field') and match.group(key):
                    field = match.group(key).strip()
                    fields.append(field)

    # Clean up fields by stripping whitespace and removing trailing punctuation
    cleaned_fields = [field.strip().rstrip('.,;') for field in fields if field]

    return cleaned_fields


def extract_experience(description):
        matches = re.findall(r'(\d+)\+?\s+years? of experience', description)
        if matches:
            return int(matches[0])
        else:
            return None
        
def extract_work_preference(description):
        if re.search(r'\b(remote|work from home|telecommute|fully remote|anywhere)\b', description):
            return 'Remote'
        elif re.search(r'\b(on-site|on site|office-based|in-office|in office)\b', description):
            return 'Onsite'
        elif re.search(r'\b(hybrid|flexible work|partially remote)\b', description):
            return 'Hybrid'
        else:
            return 'Onsite'