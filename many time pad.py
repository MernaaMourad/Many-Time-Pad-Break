if __name__ == '__main__':
    # identifying ciphers as hex
    ciphers = [
        0x68AF0BEF7F39982DA975B5E6D06947E61C22748C94A2155CFCCC464DEAFB6F4844DB2D7312ED192B6B7251580C61D5A296964E824A16648B16B9,
        0x70A20FBD7E209324A979BFE2997A46E61B22749692EB1655FA995D46A9FA654F43C93F2114A21E3E227714580A6790B88BD74F9E09107D8B0EAC,
        0x6FA20DBA622CDD28EC68F0F0C16D41A7023778C29EB8455EFC894B46EDA96C46459E2D2A1CEF1239707F571604618CEB9DD85E955013628B0DAE,
        0x6FA20DBA6220893AA970A4B5CD664CE609286D8799B80010F68A0F56FAE868405BD72A2A51E118386E7214520E6994AC9D964E824A16648B16B9,
        0x71A80AAA6227DD20FB68A0E1D6695BA71C3864C285AE1445F09E4A50A9EA6B5B52D82B3F51E3192922645D5100769ABE8B965C89480F6F910BB3,
        0x7DA30ABD753A8E63FB70BEF1D66340BC0D24748D99EB065FEC804B03F9FB6F5F52D02A731CE31B24617F5B431C2496AA94DA1D865D17778109B3,
        0x75B34EA66369932CFD31A0E7D86D5DAF0F3171C283A44542FC805603FAE6664C5BC77E3C1FA204346F7B51421D6D96EB9DD85E955013628B0DAE,
        0x75E71DA771259163E774A6F0CB2E5BA3192378C283A30010EA8D4246A9F96B5A44C9312115A21823227B415A1B6D85A79D965C844A0C638C16B3,
    ]

    output = ["" for i in range(len(ciphers))]  # will be used for the 8 messages
    mainList = []  # used for xoring of ciphers
    tempList = []
    indeciesSpaces = []  # used for identifying spaces positions
    tempListIndicesSpaces = []
    s = 0
    m = 0
    n = 0
    space = 0x20  # hex of space
    # looping on each cipher and xor with other ciphers
    for i in ciphers:

        n = 0
        for j in ciphers:

            if m != n and n < 8:
                temp = hex(ciphers[m] ^ ciphers[n])  # xor of ciphers
                temp = temp[2:]  # to remove 0x of the hex
                length = len(hex(ciphers[m]))
                temp = temp.zfill(length - 2)  # in case xor result is 7 it will make it 07
                tempList.append(temp)  # add to each cipher its permutations

            n = n + 1
        mainList.append(
            tempList)  # adding to the list of lists where inside the large list there are list for each cipher and its permutations
        tempList = []
        m = m + 1
    # looping on every list in the large list by columns every 2 characters is considered a column
    for x in range(len(mainList)):
        for col in range(0, (len(mainList[0][0])), 2):
            countSpace = 0
            countLetter = 0
            l = 0
            for y in range(len(mainList[x])):
                stringTemp = mainList[x][l]
                stringTemp = stringTemp[col:col + 2]
                if (stringTemp > '40' or stringTemp == '00'):  # handling the condition of knowing spaces position
                    countSpace = countSpace + 1  # add one to space count everytime the hexadecimal is greater than 40 or 00
                    # 40 corresponds to first letter before is just numbers
                if (stringTemp < '40' and stringTemp != '00'):
                    countLetter = countLetter + 1
                l = l + 1
            if countSpace == len(mainList[x]):
                # if the total number of space count is equal to length of ciphers then there is a space located there so add to list of indices spaces
                tempListIndicesSpaces.append(col)
        indeciesSpaces.append(tempListIndicesSpaces)
        tempListIndicesSpaces = []

    print('permutations:')
    for s in range(len(output)):
        print(mainList[s])
    print('-------------------------------------------------------------------------------------')
    print('space indices:')
    for s in range(len(output)):
        print(indeciesSpaces[s])


    for col in range(0, (len(mainList[0][0])), 2):
        spaceExist = 0
        p = 0
        for p in range(len(indeciesSpaces)):
            if col in indeciesSpaces[p]: #looping on all indices and checking if space exists
                spaceExist = 1
                break
        if spaceExist == 1:
            indexMainList = 0
            # this is used to put spaces in its location and hex of small letters that were initially xored with space
            for h in range(len(output)):
                if p == h:
                    variable = bytes.fromhex("20").decode()
                    output[h] += variable #fill the messages with the spaces
                    continue
                stemp = int(mainList[p][indexMainList][col:col + 2], 16) ^ int("20", 16) # used to return the hex of small letter again from the capital letter
                stemp = hex(stemp)
                temp = stemp
                variableLetter = bytes.fromhex(stemp[2:]).decode()
                output[h] += variableLetter #fill the messages with the letters that were initially xored with spaces
                indexMainList = indexMainList + 1
        # it is neither space nor space xored with letter then add dummmy (_)to be guessed later on
        else:
            for h in range(len(output)):
                output[h] += "_"

    print('-------------------------------------------------------------------------------------')
    print('messages:')
    for s in range(len(output)):
        print(output[s])


