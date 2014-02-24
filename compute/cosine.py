'''
Created on Feb 20, 2014

@author: svalmiki
'''
import re, math
from collections import Counter

WORD = re.compile(r'\w+')
'''
Gets the cosine product of the two strings
'''
def get_cosine(text1, text2):
    vec1 = text_to_vector(text1.lower())
    vec2 = text_to_vector(text2.lower())
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
    
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

