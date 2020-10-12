# WELLS-READ

Category: Coding

Points: 200

Solved by: 0xThorn

## Problem

Description: R-Boy finds the time machine, which Zer0 used to travel to another era. Nearby, lies a copy of HG Wells’ The Time Machine. Could this book from the past help R-Boy travel in time? Unfortunately, R-Boy can’t read or understand it, because the space-time continuum has changed some of the words. Help R-Boy to start his time travels!

## Writeup

### Analysis

We are provided with two files.

At first glance, the first file (`The time machine...`) looks like a book, but looking closely at the text you can see that some words have wrong characters.
Instead the second file (`words.txt`) contains a long list of words, practically a dictionary.

Looking closely at the wrong characters in the first file, you notice that some are symbols, such as curly brackets.
From there comes the intuition: the flag was hidden in the text by substituting characters in the original words!

### The script

1. Imports the book by removing the new lines, double dashes and double spaces

```python
with open('The Time Machine by H. G. Wells.txt','r') as file:   
    text = file.read().replace("\n", " ").replace('--', ' ').replace('  ', ' ')
```

2. Finds all the strings enclosed in two curly brackets (for the format flag)

```python
matches = re.findall(r'\{[^\{\}]*\}', text)
```

3. For each of the strings it is necessary to find the defects in the single words

```python
for result in matches:
  differences = ''
  for word in result.split():
    differences += find_differences(word)
  print(differences)
```

4. We create the `find_differences` function to find the defects in a word. First, punctuation characters are removed at the beginning and at the end

```python
beginning_punctation = ['"', "'"]
end_punctation = [',', '.', '!', '?', '"', "'", ';', ":"]

while len(word) > 1 and word[-1] in end_punctation:
  word = word[:-1]

while len(word) > 1 and word[0] in beginning_punctation:
  word = word[1:]
```

5. Then it checks that the word is not already perfectly contained in the dictionary. Checks are made with lowercase words to avoid false differences due to capitalization.

```python
if word.lower() in [x.lower() for x in dictionary]:
  return ''
```

6. The comparison is made with each word in the dictionary, only if the length of the words matches. It does a character-by-character check and saves the differences. If there is only one different character, the search ends.

```python
for d in dictionary:
  if len(d) == len(word):
    if word[0].islower():
      d = first_lower(d)
    else:
      d = first_upper(d)

    different_characters = ''
    for _ in range(len(word)):
      if d[_] != word[_]:
        different_characters += word[_]

    if len(different_characters) == 1:
      return different_characters

return ''
```

7. Run the script and get multiple strings. Only one respects the flag format: `{FLG:1_kn0w_3v3ryth1ng_4b0ut_t1m3_tr4v3ls}`
