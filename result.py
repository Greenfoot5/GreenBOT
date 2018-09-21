while True:
    start = input(str("Starting lifetime gold value "))
    end = input(str("Finishing lifetime gold value "))
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    startLetterAValue = 0
    startLetterBValue = 0
    endLetterAValue = 0
    endLetterBValue = 0

    for val in range(0,len(alphabet)):
        if alphabet[val] == start[0]:
            startLetterAValue = val
    for val in range(0,len(alphabet)):
        if alphabet[val] == start[1]:
            startLetterBValue = val
    for val in range(0,len(alphabet)):
        if alphabet[val] == end[0]:
            endLetterAValue = val
    for val in range(0,len(alphabet)):
        if alphabet[val] == end[1]:
            endLetterBValue = val

    startValue = 15+((startLetterBValue)*3)+((startLetterAValue)*78)
    endValue = 15+((endLetterBValue)*3)+((endLetterAValue)*78)
    print("Starting worth was:",str(startValue)+".")
    print("Ending worth was:",str(endValue)+".")
    print("Final score:",str(endValue-startValue)+".")

