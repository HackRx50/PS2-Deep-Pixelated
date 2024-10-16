import re
import difflib

def load_abbreviations(file_path):
    abbreviations_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                abbreviation, full_form = parts
                abbreviations_dict[abbreviation.upper()] = full_form
    return abbreviations_dict

def clean_text(text):
    # Remove symbols and unnecessary spaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Keep only alphanumeric characters and spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Remove extra spaces
    
    # Remove units of time (e.g., "36 weeks", "2 days", "5 hours", "week 36")
    cleaned_text = re.sub(r'\b\d+\s*(weeks?|days?|hours?|minutes?|seconds?|min?|month?|months?|hr?)\b', '', cleaned_text)
    cleaned_text = re.sub(r'\b(weeks?|days?|hours?|minutes?|seconds?|min?|month?|months?|hr?)\s*\d+\b', '', cleaned_text)

    return cleaned_text

def find_longest_match(word, abbreviations_dict):
    """Find the longest abbreviation match starting from the first character."""
    word = word.upper()
    max_match = ""
    for abbr in abbreviations_dict.keys():
        if word.startswith(abbr) and len(abbr) > len(max_match):
            max_match = abbr
    return max_match

def replace_abbreviations(sentence, abbreviations_dict):
    cleaned_sentence = clean_text(sentence)
    words = cleaned_sentence.split()
    updated_words = []
    
    for word in words:
        stripped_word = re.sub(r'[^\w\s]', '', word) 
        
        if len(words) > 1:
            
            full_form = abbreviations_dict.get(stripped_word.upper(), None)
            
            if not full_form:
                
                possible_matches = difflib.get_close_matches(stripped_word.upper(), abbreviations_dict.keys(), n=1, cutoff=0.9)
                if possible_matches:
                    full_form = abbreviations_dict.get(possible_matches[0])
            
            if full_form:
                updated_word = word.replace(stripped_word, full_form)
                updated_words.append(updated_word)
            else:
                updated_words.append(word)
        else:
            
            longest_match = find_longest_match(stripped_word, abbreviations_dict)
            if longest_match:
                full_form = abbreviations_dict.get(longest_match)
                updated_word = full_form  
                updated_words.append(updated_word)
            else:
                updated_words.append(word)
    
    return ' '.join(updated_words)
