
from Enigma import *
import time
import itertools
alphabet = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

def Code1():
    """
    Code: DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ
    Crib: SECRETS
    Rotors: Beta Gamma V
    Reflector: Unknown
    Ring settings: 04 02 14
    Starting positions: MJM
    Plugboard pairs: KI XN FL
    """
    code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
    crib = "SECRETS"
    print("======= Crack Code 1 =======")
    print("Rotors: Beta Gamma V")
    print("Reflector: Unknown")
    print("Ring settings: 04 02 14")
    print("Starting positions: MJM")
    print("Plugboard pairs: KI XN FL")
    reflectors = ['A','B','C']
    
    for reflector in reflectors:
        rotors = [("V",14,'M'),("Gamma",2,'J'),("Beta",4,'M'),(reflector,1,'A')]
        plugBoardInputs = ["KI", "XN" ,"FL"]
        machine = EnigmaMachine(rotors, plugBoardInputs)
        decrypted = [machine.encode(c) for c in code]
        text = ''.join(decrypted)
        if crib in text:
            return f"found {text} with reflector {reflector}"

def Code2():
    """
    Code: CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH
    Crib: UNIVERSITY
    Rotors: Beta I III
    Reflector: B
    Ring settings: 23 02 10
    Starting positions: Unknown
    Plugboard pairs: VH PT ZG BJ EY FS
    """
    code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
    crib = "UNIVERSITY"
    print("======= Crack Code 2 =======")
    print("Rotors: Beta I III")
    print("Reflector: B")
    print("Ring settings: 23 02 10")
    print("Starting positions: UKNOWN")
    print("Plugboard pairs: VH PT ZG BJ EY FS")
    #using the intertools permuation function that will re
    # turn all permutations of x numbers in range of Y starting from 1, and including Y
    rotorCombinations = [[("III",10,p[0]),("I",2,p[1]),("Beta",23,p[2]),('B',1,'A')] for p in itertools.product(alphabet,repeat=3)]
    plugBoardInputs = ["VH", "PT" ,"ZG","BJ","EY","FS"]
    for combo in rotorCombinations:
        machine = EnigmaMachine(combo, plugBoardInputs)
        decrypted = [machine.encode(c) for c in code]
        text = ''.join(decrypted)
        if crib in text:   
            return f"Found {text} with rotors {combo}"

def Code3():
    """
    The department has intercepted a message from the admissions team.
    They know it contains the word "THOUSANDS" and they are worried it might relate to how many students are arriving next semester. But the admissions team are a bit unusual: they love even numbers, and hate odd numbers.
    You happen to know they will never use an odd-numbered rotor, ruling out I, III, and V. They will also never use a ring setting that has even a single odd digit: 02 is allowed but 11 is certainly not, and even 12 is banned.
    """
    code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
    crib = "THOUSANDS"
    rotorOptions = "Beta,Gamma,II,IV"
    reflectors = "A,B,C"
    print("======= Crack Code 3 =======")
    print(f"Rotor options: {rotorOptions}")
    print("Reflector: unknown")
    print("Ring settings: unknown restricted")
    print("Starting positions: EMY")
    print("Plugboard pairs: FH TS BE UQ KD AL")
    print(f"Code = {code}")
    print(f"Crib = {crib}")
    
    #Starting positions: EMY
    #Plugboard pairs: FH TS BE UQ KD AL
    #rotorPermutations = itertools.permutations(rotorOptions.split(','),3)
    ringSettings = []
    ringSettings = []
    for rs in range(1,27):
        rsStr = str(rs)
        if len(rsStr) == 2:
            if int(rsStr[0]) % 2 == 0 and int(rsStr[1]) % 2 == 0:
                ringSettings.append(rs)
            else:
                continue
        elif rs % 2 == 0:
            ringSettings.append(rs)

    #create a list of all the permutations of different rotors
    rotorPermutations = [p for p in itertools.permutations(rotorOptions.split(','),3)]
    #add on the reflectors
    rotorPlusReflector = [rp + (r,) for r in reflectors.split(',') for rp in rotorPermutations]
    #create a list of all the possible ring setting combinations
    ringSettingProducts = [rs for rs in itertools.product(ringSettings,repeat=3)]
    rotorPlusRingPlusReflector = []
    i = 0
    j = 0
    temp = []
    #join the ring settings to the rotor selections
    for rpr in rotorPlusReflector:
        for rst in ringSettingProducts:
            i = 0
            for rs in rst:
                temp += [(rpr[i],rs)]
                i += 1
            temp += [(rpr[i],1)]
            
            rotorPlusRingPlusReflector.append(temp)
            temp = []
            
    combinations = 0
    plugBoardInputs = ["FH", "TS" ,"BE","UQ","KD","AL"]
    encodings = 0
    rotorPos = ""
    #loop over all the possible combinations
    for rprs in rotorPlusRingPlusReflector:
         rotors = [(rprs[0][0],rprs[0][1],'Y'),(rprs[1][0],rprs[1][1],'M'),(rprs[2][0],rprs[2][1],'E'),(rprs[3][0],1,'A')]
         combinations += 1
         machine = EnigmaMachine(rotors, plugBoardInputs)
         text = ""
         decrypt = [machine.encode(c) for c in code]
         text = ''.join(decrypt)
         if crib in text:
            rotorPos = rotors
            break
        
         
    print(f"Found {text} with rotors {rotorPos} took {encodings} encodings from {combinations} combinations") 
    return text  
    
def Code4():
    """
    On my way home from working late as I walked past the computer science lab I saw one of the tutors playing with the Enigma machine.
    Mere tutors are not allowed to touch such important equipment! Suspicious, I open the door, but the tutor hears me, and jumps out of the nearest window.
    They left behind a coded message, but some leads have been pulled out of the machine.
    It might contain a clue, but I'll have to find the missing lead positions (marked with question marks in the settings below).
    """
    code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
    crib = "notutorswere"
    rotorOptions = "V,III,IV,A"
    print("======= Crack Code 4 =======")
    print(f"Rotor options: {rotorOptions}")
    print("Reflector: A")
    print("Ring settings: 24 12 10")
    print("Starting positions: SWU")
    print("Plugboard pairs: WP RJ A? VF I? HN CG BS")
    print(f"Code = {code}")
    print(f"Crib = {crib}")
    plugBoardInputs = ["WP","RJ","VF","HN","CG","BS"]
    #create a list of possible pairs
    incomplete = ["A","I"]
    complete = ["W","P","R","J","V","F","H","N","C","G","B","S"]
    #generate a list of plug combos that are possible from the plugs already taken and the ones incomplete
    plugsMatched = [str(f"{plug}{letter.upper()}") for plug in incomplete for letter in alphabet 
                                                            if letter.upper() not in complete
                                                            if letter.upper() not in incomplete]

    #creates a list of products of the plugs available from the plugsmatched list split in half, one half being the A's, the other being the I's
    possibleCombos = itertools.product(plugsMatched[0:12],plugsMatched[12:] )
    #this might seem like an incredibly complex permutation. But what we found is that there could be AD and ID coming from the product above in the same list, so we need to weed these out using the conditional below/
    possiblePlugCombos = [plugBoardInputs + [str(f"{plug[0]}")] + [str(f"{plug[1]}")] for plug in possibleCombos if plug[0][1] not in plug[1] and plug[0][0] not in plug[1]]
    #create a list of all the permutations of different rotors
    rotorPermutations = [p for p in itertools.permutations(rotorOptions.split(','),3)]
    combinations = 0
    #we need to loop for all rotor possibilities and then all the plugboard possibilites
    for rotor in rotorPermutations:
        #set rotors
        rotors = [(rotor[0],10,'U'),(rotor[1],12,'W'),(rotor[2],24,'S'),('A',1,'A')]
        for plugs in possiblePlugCombos:
            combinations += 1
            machine = EnigmaMachine(rotors, plugs)
            decrypt = [machine.encode(c) for c in code]
            text = ''.join(decrypt)
            if crib in text:
                return text

def Code5():
    """
    I later remembered that I had given the tutor permission to use the Enigma machine to solve some codes I'd received via email. 
    As for the window, they are just a big fan of parkour, this is always how they leave the building. 
    It seems they are stuck on one last code. It came in via email so we suspect it's just spam, probably related to a social media website, but you never know when you'll find a gem in that kind of stuff.
    The tutor has narrowed the search and found most of the settings, but it seems this code was made with a non-standard reflector. Indeed, there was a photo attached to the email along with the code.
    It appears that the sender has taken a standard reflector, cracked it open, and swapped some of the wires – two pairs of wires have been modified, by the looks of the dodgy soldering job.
    To be clear, a single wire connects two letters, e.g. mapping A to Y and Y to A. The sender has taken two wires (fours pairs of letters), e.g. A-Y and H-J, and swapped one of the ends, so one option would be H-Y and A-J.
    They did this twice, so they modified eight letters total (they did not swap the same wire more than once).
    """
    code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
    crib = ['INSTAGRAM','FACEBOOK','TUMBLR','TWITTER','YOUTUBE','REDDIT','SNAPCHAT','LINKEDIN']
    rotorOptions = "V,II,IV"
    print("======= Crack Code 4 =======")
    print(f"Rotor options: {rotorOptions}")
    print("Reflector: unknown")
    print("Ring settings: 06 18 07")
    print("Starting positions: AJL")
    print("Plugboard pairs: UG IE PO NX WT")
    print(f"Code = {code}")
    print(f"Crib = {crib}")
    
    
    rotors = [('IV',7,'L'),('II',18,'J'),('V',6,'A'),('B',1,'A')]
    machine = EnigmaMachine(rotors,[])
    

    pairs = []
    #get unique pairs
    text = ""
    foundCrib = False
    reflectors = "A,B,C"
    plugBoardInputs = ["UG","IE","PO","NX","WT"]

    for rotor in reflectors.split(','):
        rotors = [("IV",7,'L'),("II",18,'J'),("V",6,'A'),(rotor,1,'A')]
        print(rotors)
        machine = EnigmaMachine(rotors,plugBoardInputs)
        rb = machine.GetRotorBoard()
        #get the reflector rotor to access the mappings.
        rotor = rb.rotorList[3]
        #get the list of unique pairs for this reflector
        for i,e in enumerate(rotor.mapping[0]):
            pair = f"{rotor.mapping[0][i]}{rotor.mapping[1][i]}"
            pair = (rotor.mapping[0][i],rotor.mapping[1][i])
            revPair = (pair[1],pair[0])
            #make sure we aren't adding the duplicates
            if pair not in pairs and revPair not in pairs:
                pairs.append((rotor.mapping[0][i],rotor.mapping[1][i]))

        #find all permutations of these pairs
        matchedPairs = []
        matchedPairs = [perm for perm in itertools.permutations(pairs,4) if perm not in matchedPairs]

        for wires in matchedPairs:
            text = ""
            machine = EnigmaMachine(rotors,plugBoardInputs)
            #swap the wires
            SwapWires(machine,wires)
            #decrypt the message
            decrypt = [machine.encode(c) for c in code]
            #join it all back together
            text = ''.join(decrypt)
            #print(text)
            #iterate through each word in the crib
            for pf in crib:
                if pf in text:
                    return text

def SwapWires(machine, pairs):
    rb = machine.GetRotorBoard()
    rotor = rb.rotorList[3]
    #a list compormising of two lists, one labels, one pins
    mappings = rotor.mapping
     #(a,e),(b,j),(c,m),(d,j)7
    i = 0
    while i < 4:
        first = pairs[i]
        second = pairs[i+1]
        #take the index of the pin to find the position to swap for both
        sw1 = mappings[1].index(first[1])
        sw2 = mappings[1].index(second[1])
        #so now we swap the letters
        mappings[1][sw1] = second[1]
        mappings[1][sw2] = first[1]
        sw1r = mappings[1].index(first[0])
        sw2r = mappings[1].index(second[0])
        temp = mappings[1][sw1r]
        mappings[1][sw1r] = mappings[1][sw2r]
        mappings[1][sw2r] = temp
        temp = ""
        i += 2


#code 6 is about breaking the enigma machine from just output analysis. You have an encrypted bit of text, and you understand that a letter cannot become itself. So you build the machine to check all outputs against this encrypted text.
def ExtraCode6():

    #first we chose a piece of text we want to encrypt
    toEncrypt = "THEWEATHERTODAYISLOOKINGGREATFORANAIRRAIDLONGLIVETHEKING"
    #chose some random settings
    rotorOptions = "I,II,III,IV,Beta,Gamma"
    print(f"Rotor options: {rotorOptions}")
    print(f"Rotor to encrypt {rotorOptions[0]},{rotorOptions[3]},{rotorOptions[2]} reflector A")
    print(f"Ring setting 05 20 32")
    print("Plugboard pairs: AB CD EF NX WT")
    plugBoardInputs = ["AB","CD","EF","NX","WT"]
    print(f"All rotors at starting position A")
    rotors = [(rotorOptions[0],7,'A'),(rotorOptions[3],18,'A'),(rotorOptions[2],6,'A'),('A',1,'A')]
    machine = EnigmaMachine(rotors,plugBoardInputs)
    decrypt = [machine.encode(c) for c in toEncrypt]
    text = ''.join(decrypt)
    print(f"out of encryption {text}")
    machine = EnigmaMachine(rotors,plugBoardInputs)
    decrypt = [machine.encode(c) for c in text]
    output = ''.join(decrypt)
    print(f"Check it runs back through -> {output}")

    print("======= Cracking the code =======")
    print(f"======= Intercepted {toEncrypt} =======")

    print(f"Rotor options: {rotorOptions}")
    print("Reflector: unknown")
    print("Ring settings: unknown")
    print("Starting positions: uknown")
    print("Plugboard pairs: unknown")
    
    #rotor permuations with reflectors
    #rotor permutaitons with ring settings
    #rotor permutations with rings settings, and starting positions
    #plugboard inputs
    plugBoardCombinations = itertools.permutations(alphabet,2)
    plugboardcombos = []
    for perm in plugBoardCombinations:
        if (perm[1],perm[0]) not in plugboardcombos:
            plugboardcombos.append(perm)
            print(perm)
    #can have 10 inputs
    #plugboardInputs = itertools.permutations(plugboardcombos,10)
    for input in itertools.permutations(plugboardcombos,10):
        print(input)
    rotors = [('IV',7,'L'),('II',18,'J'),('V',6,'A'),('B',1,'A')]
    machine = EnigmaMachine(rotors,[])
    

if __name__ == "__main__":

    #ExtraCode6()
    start = time.time()
    #print(Code1())

    end = time.time()
    print(f" Processing took {end - start} seconds")

    start = time.time()
    #print(Code2())
    end = time.time()
    print(f" Processing took {end - start} seconds")

    start = time.time()
    #print(Code3())
    end = time.time()
    print(f" Processing took {end - start} seconds")
    
    

    start = time.time()
    #print(Code4())
    end = time.time()
    print(f" Processing took {end - start} seconds")

    start = time.time()
    print(Code5())
    end = time.time()
    print(f" Processing took {end - start} seconds")

    
