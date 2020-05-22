import re
#Metacharacters: . ^ $ * + ? { } [ ] \ | ( )

#[ ] : used to specify a charcter class. These can be specified in a range or individually
#[afgh] : match any of the characters a,f,g or h. [abcd]=[a-d]. [$] looks for $ (not a metacharacter here)

#^ : when placed after, means excepted
#[^5] means everything except 5. [5^] matches 5 or ^ (not the same!!)
#\ :used to signal special sequences (can be used also to escap [ and \ itself)
#They represent predefined sequences. \w : any alphanumeric character (equivalent to [a-zA-Z0-9_])
#\w : [a-zA-Z0-9_]
#\D : [^0-9] (any non digit character)
#\s : [ \t\n\r\f\v] : Any whitespace character
#\S : Any non whitespace character
#\W : any non alphanumeric character
#[\s,.] : matches any whitespace or , or .

#REPEATING THINGS
#* : 0 or more times. ca*t will match ct, cat, or caaaat.
#a[bcd]*f : will match a, then any letter from the group any number of time, and then f
#+ : one or more times
#? : once or zero times
#{m,n} : at least m repetitions, at most n
#a/{1,3}b: will match a/b, a//bb or a///b

#THE PYTHON re MODULE
#Always use python raw notation with r
#re.match : Determine if the RE matches at the beginning of the string
#re.search : Look for any location where the RE matches (first occ)
#re.findall : search but returns all the occurences in a lst
#re.finditer : returns an iterator
m = re.match(r'[a-z]+', "tempo::")
s = re.search(r'[a-z]+', "::tempo")
print(m.group())
print(m.span()) #first element of span is m.start(), second is m.end()
print(s.group())
print(s.span())
f = re.findall(r'\d+',"10 drummers, 12 hello")
print(f)

#FLAGS
#re.I : do case insensitive matches
#re.M : multi line matching
#re.S : makes . matches any character, including a newline, otherwise . will match any except a newline

#MORE METACHARACTERS
#^ : Matches only at beginning of lines
mystring = "Bonsoir\nbonjour et bienvenue\nbonne Bouffe"
m2 = re.findall(r'^B',mystring, re.M|re.I)
print(m2)
#¦ : or operator. Crow¦Servo will match either Crow or Servo
m1 = re.match(r'Crow|Servo',"Crow")
print(m1)
#$ : matches at the end of a line (same priciple as ^)
#\b : bounding a word (will not be matched if inside a word. Needs whitespaces
m3 = re.search(r'\bclass\b', "a subclass")
print(m3)
#() : grouping
m4 = re.match(r'(ab)*',"abababab")
print(m4)
m5 = re.match(r'(a(b)c)d',"abcd")
print(m5.group(0)) #prints the default complete match
print(m5.group(1)) #what is been matched by group 1 (abc)
print(m5.group(2)) #what is been matched by group 2 (b)
print(m5.groups()) #prints from group 1 to end
#\1: will succeed if at the current position the exact content of group 1 can be found
m6 = re.match(r'(\d+)\w+\1',"99adsfa99")
print(m6)
#Example: detect the doubled words:
m7 = re.search(r'\b(\w+)\s+\1\b',"Paris in the the spring")
print(m7)

#MODIFYING STRINGS
m8 = re.split(r'the', "Paris in the spring")
print(m8)
m9 = re.sub(r'the',"a","Paris in the spring")
print(m9)

#NOTE
#regex does by default greedy matching, i.e it uses the most text as possible.
#Use the ? for matching the least text as possible.
s = '<html><head><title>Title</title>'
print(re.match(r'<.*>', s).group())  #.* will consume the rest of the string
print(re.match(r'<.*?>', s).group())
#? can be used after every quantifier.
#If we don't want to use it with a quantifier, use ?=.
#For example, ?=\d will match a digit, but not consume it


#EXERCICES:
string1 = "*&%@#!}{"
string2 = "ABCDEFabcdef123450"
q = re.match(r'[a-zA-Z0-9]*',string2)
if q.group() == string2:
    print("ok")
else:
    print("not ok")

data = ["example (.com)", "w3resource", "github (.com)", "stackoverflow (.com)"]
for i,d in enumerate(data):
    data[i] = re.sub(r' \(\.com\)',"",d)
print(data)

#Babynames exercise https://developers.google.com/edu/python/exercises/baby-names
filename= "baby2006.html"
with open(filename,"r") as f:
    content = f.read()

year = re.search(r'\d+',filename).group()
names = re.findall(r'<tr align="right"><td>(\d+)</td><td>([a-zA-Z]+)</td><td>([a-zA-Z]+)</td>',content,re.M)
final_result= [year]
names_with_soc = []
for name in names:
    names_with_soc.append(name[1]+" "+name[0])
    names_with_soc.append(name[2]+ " " + name[0])
final_result.extend(sorted(names_with_soc))
print(final_result[:10])

#Valid postal codes
regex_integer_in_range = r"[1-9]\d{5}"
regex_alternating_repetitive_digit_pair = r"(\d)(?=\d\1)"
P="110000"
print(bool(re.match(regex_integer_in_range, P)))
fa = re.findall(regex_alternating_repetitive_digit_pair, P)
print(fa)
print((bool(re.match(regex_integer_in_range, P))
and len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2))

#Valid credit card number
cardNr1 = "4123456789123456"
cardNr2 = "5123-4567-8915-3456"
cardNr3 = "4123333789123456"
cardNr = cardNr3
no_tirets=r'([4-6]\d{15})'
with_tirets=r'([4-6]\d{3}-(\d{4}-){2}\d{4})'
match_no_tiret = re.match(no_tirets,cardNr)
match_tiret = re.match(with_tirets,cardNr)
valid_tiret = match_tiret and match_tiret.group() == cardNr
valid_no_tiret = match_no_tiret and match_no_tiret.group() == cardNr
if (not match_tiret and not match_no_tiret) or (not valid_tiret and not valid_no_tiret):
    print("Invalid!")

else:
    if match_tiret and match_tiret.group()==cardNr:
        cardNr = re.sub(r"-","",cardNr)

    repetingRegex = r"(\d)\1\1\1"
    match_repeting_nrs = re.search(repetingRegex,cardNr)
    if match_repeting_nrs:
        print("Invalid!")
    else:
        print("Valid")















