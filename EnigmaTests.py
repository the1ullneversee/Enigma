import pytest
from CustomExceptions import *
from Rotor import *
from Enigma import *
from Plugs import *

def test_ConfigBadLabel():
    with pytest.raises(ConfigurationException):
        rotors = [("AAA",1,'A'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
        rb = Rotorboard(rotors)

def test_ConfigBadRingSetting():
    with pytest.raises(ConfigurationException):
        rotors = [("I",28,'A'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
        rb = Rotorboard(rotors)

def test_ConfigBadOffset():
    with pytest.raises(ConfigurationException):
        rotors = [("I",1,']'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
        rb = Rotorboard(rotors)

def test_ConfigBadReflector():
    with pytest.raises(ConfigurationException):
        rotors = [("I",1,'A'),("II",1,'A'),("I",1,'A'),("D",1,'A')]
        rb = Rotorboard(rotors)

def test_OffsetAtZ():
    #Testing offset at Z
    rotors = [("III",1,'Z'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['U']
    index = 1
    for out in outputs:
        funcOutput = rb.encode(inputChoice)
        print(f"test num {index} input {inputChoice} expected {out} got {funcOutput}")
        assert(funcOutput == out)
        index += 1

def test_NotchHitting():
    #First test is testing the basic mapping is working, with rotor rotation, and eventually the 'notch' being hit and rotating the 2nd rotor from the right.
    rotors = [("III",1,'A'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['B','D','Z','G','O','W','C','X','L','T','K','S','B','T','M','C','D','L','P','B','M','U','Q']
    index = 1
    for out in outputs:
        funcOutput = rb.encode(inputChoice)
        print(f"test num {index} input {inputChoice} expected {out} got {funcOutput}")
        assert(funcOutput == out)
        index += 1

def test_RingSettingAtB():
    testLabel = "this set of tests is testing the ring setting functionality by setting the first rotor to ring setting B"
    rotors = [("I",2,"A"),("II",1,"A"),("III",1,"A"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['N','F','T','Z','M','G','I','S','X','I','P','J','W','G','D','N','E','J','C','O','Q','T']
    index = 1
    print(testLabel)
    for out in outputs:
        funcOutput = rb.encode(inputChoice)
        print(f"test num [{index}] input {inputChoice} expected {out} got {funcOutput}")
        assert(funcOutput == out)
        index += 1

def test_DoubleStepFunctionality():
    testLabel = "this set of tests is testing the double step functionality"
    rotors = [("III",1,"V"),("II",1,"D"),("I",1,"A"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['Q','I', 'B']
    print(testLabel)
    for out in outputs:
        funcOutput = rb.encode(inputChoice)
        print(f"input {inputChoice} expected {out} got {funcOutput}")
        assert(funcOutput == out)

def test_RotorVI():
    testLabel = "With rotors I II VI, reflector B, and initial"
    rotors = [("VI",1,"A"),("II",1,"A"),("I",1,"A"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['I','J','V','D','T','E','X','K','E','B','Y','N','S','R','I','D','V','H','P','B','O','J','C','G','P','B','U','F']
    print(testLabel)
    for out in outputs:
        funcOutput = rb.encode(inputChoice)
        print(f"input {inputChoice} expected {out} got {funcOutput}")
        assert(funcOutput == out)

def test_BasicPlugFunctionality():
    lead = PlugLead("AG")
    assert(lead.encode("A") == "G")
    assert(lead.encode("D") == "D")
    lead = PlugLead("DA")
    assert(lead.encode("A") == "D")
    assert(lead.encode("D") == "A")

def test_PlugConnectToSelf():
    with pytest.raises(PlugException):
        lead = PlugLead("AA")

def test_PlugCombinationTooSmall():
    with pytest.raises(PlugException):
        lead = PlugLead("A")

def test_PlugCombinationEmpty():
    with pytest.raises(PlugException):
        lead = PlugLead("")

def test_PlugCombinationTooLong():
    with pytest.raises(PlugException):
        lead = PlugLead("AAA")

def test_PlugBoardPlugAlreadyTaken():
    with pytest.raises(PlugException):
        plugboard = Plugboard("")
        plugboard.add(PlugLead("AD"))
        plugboard.add(PlugLead("DA"))

def test_PlugBoardEncoding():
    plugboard = Plugboard("")
    plugboard.add(PlugLead("AD"))
    plugboard.add(PlugLead("SZ"))
    plugboard.add(PlugLead("GT"))
    plugboard.add(PlugLead("LI"))
    plugboard.add(PlugLead("KU"))
    print(plugboard.encode("K") )
    assert(plugboard.encode("K") == "U")
    assert(plugboard.encode("A") == "D")

def test_PlugBoardMaxAmountOfLeadsAdded():
    with pytest.raises(PlugException):
        plugboard = Plugboard("")
        plugboard.add("AD")
        plugboard.add("SZ")
        plugboard.add("GT")
        plugboard.add("LI")
        plugboard.add("KU")
        plugboard.add("XQ")
        plugboard.add("CB")
        plugboard.add("FH")
        plugboard.add("ER")
        plugboard.add("OP")
        plugboard.add("NM")

def test_MultipleRotorDemonstration():
    ##### --------  Multiple Rotor Demonstration --------- #####
    testLabel = "With rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A Z, encoding an A produces a U."
    rotors = [("III",1,"Z"),("II",1,"A"),("I",1,"A"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['U']
    print("==== Start Test ====")
    print(f"{testLabel}")
    funcOutput = rb.encode(inputChoice )
    print(f"input {inputChoice} expected {outputs[0]} got {funcOutput}")
    assert(funcOutput == outputs[0])
    print("=============== END TEST ===============")

    testLabel = "With rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A A, encoding an A produces a B."
    #With rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A A, encoding an A produces a B.
    rotors = [("III",1,"A"),("II",1,"A"),("I",1,"A"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['B']
    print("==== Start Test ====")
    print(f"{testLabel}")
    funcOutput = rb.encode(inputChoice)
    print(f"input {inputChoice} expected {outputs[0]} got {funcOutput}")
    assert(funcOutput == outputs[0])
    print("=============== END TEST ===============")

    testLabel = "With rotors I II III, reflector B, ring settings 01 01 01, and initial positions Q E V, encoding an A produces an L."
    #With rotors I II III, reflector B, ring settings 01 01 01, and initial positions Q E V, encoding an A produces an L.
    rotors = [("III",1,"V"),("II",1,"E"),("I",1,"Q"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'A'
    outputs = ['L']
    print("==== Start Test ====")
    print(f"{testLabel}")
    funcOutput = rb.encode(inputChoice)
    print(f"input {inputChoice} expected {outputs[0]} got {funcOutput}")
    assert(funcOutput == outputs[0])
    print("=============== END TEST ===============")

    testLabel = "With rotors IV V Beta, reflector B, ring settings 14 09 24, and initial positions A A A, encoding an H produces a Y."
    #With rotors IV V Beta, reflector B, ring settings 14 09 24, and initial positions A A A, encoding an H produces a Y.
    rotors = [("Beta",24,"A"),("V",9,"A"),("IV",14,"A"),("B",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'H'
    outputs = ['Y']
    print("==== Start Test ====")
    print(f"{testLabel}")
    funcOutput = rb.encode(inputChoice)
    print(f"input {inputChoice} expected {outputs[0]} got {funcOutput}")
    assert(funcOutput == outputs[0])
    print("=============== END TEST ===============")

    testLabel = "With rotors I II III IV, reflector C, ring settings 07 11 15 19, and initial positions Q E V Z, encoding a Z produces a V"
    rotors = [("IV",19,"Z"),("III",15,"V"),("II",11,"E"),("I",7,"Q"),("C",1,"A")]
    rb = Rotorboard(rotors)
    inputChoice = 'Z'
    outputs = ['V']
    print("==== Start Test ====")
    print(f"{testLabel}")
    funcOutput = rb.encode(inputChoice)
    print(f"input {inputChoice} expected {outputs[0]} got {funcOutput}")
    print("=============== END TEST ===============")
    assert(funcOutput == outputs[0])

def test_EnigmaMachineDemonstration1():
    print("======= test_EnigmaMachineDemonstration1 =======")
    print("Set up your enigma machine with rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A Z.")
    print("The plugboard should map the following pairs: HL MO AJ CX BZ SR NI YW DG PK.")
    text = "HELLOWORLD"
    cipher = "RFKTMBXVVW"
    print(f"INPUT = {text}")
    rotors = [("III",1,'Z'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
    plugBoardInputs = ["HL", "MO" ,"AJ" ,"CX" ,"BZ" ,"SR" ,"NI", "YW" ,"DG" ,"PK"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    output = ""
    for ch in text:
        output += machine.encode(ch)
    print(f"OUTPUT = {output}")
    assert(output == cipher)

def test_EnigmaMachineDemonstration2():
    print("======= test_EnigmaMachineDemonstration2 =======")
    print("Set up your enigma machine with rotors IV V Beta I, reflector A, ring settings 18 24 03 05, and initial positions E Z G P.")
    print("The plugboard should map the following pairs: PC XZ FM QA ST NB HY OR EV IU.")
    cipher = "BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI"
    print(f"INPUT = {cipher}")
    rotors = [("I",5,'P'),("Beta",3,'G'),("V",24,'Z'),("IV",18,'E'),("A",1,'A')]
    plugBoardInputs = ["PC", "XZ" ,"FM" ,"QA" ,"ST" ,"NB" ,"HY", "OR" ,"EV" ,"IU"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    
    output = ""
    for ch in cipher:
        output += machine.encode(ch)
    assert(output == "congratulationsonproducingyourworkingenigmamachinesimulator".upper())
    print(f"OUTPUT = {output}")

def test_BThinPlusBetaRotor():
    print("======= test_BThinPlusBetaRotor =======")
    print("Test BThin Reflector with Beta Rotor")
    cipher = "A"
    print(f"INPUT = {cipher}")
    rotors = [("I",1,'A'),("II",1,'A'),("III",1,'A'),("Beta",1,'A'),("BThin",1,'A')]
    print(rotors)
    plugBoardInputs = []
    machine = EnigmaMachine(rotors, plugBoardInputs)

    assert(machine.encode(cipher) == "F")
    assert(machine.encode(cipher) == "T")
    assert(machine.encode(cipher) == "Z")
    assert(machine.encode(cipher) == "M")

def test_BThinPlusGammaRotor():
    print("======= test_BThinPlusGammaRotor =======")
    print("Test BThin Reflector with Gamma Rotor")
    cipher = "ABCDE"
    print(f"INPUT = {cipher}")
    rotors = [("I",1,'A'),("II",1,'A'),("III",1,'A'),("Gamma",1,'A'),("BThin",1,'A')]
    print(rotors)
    plugBoardInputs = []
    output = ["B","P","F","W","K"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    for i,e in enumerate(cipher):
        assert(machine.encode(e) == output[i])

def test_CThinPlusBetaRotor():
    print("======= test_CThinPlusBetaRotor =======")
    print("Test CThin Reflector with Beta Rotor")
    cipher = "ABCDE"
    print(f"INPUT = {cipher}")
    rotors = [("III",1,'A'),("II",1,'A'),("I",1,'A'),("Beta",1,'A'),("CThin",1,'A')]
    print(rotors)
    plugBoardInputs = []
    output = ["L","M","V","Q","K"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    for i,e in enumerate(cipher):
        assert(machine.encode(e) == output[i])

def test_CThinPlusGammaRotor():
    print("======= test_CThinPlusGammaRotor =======")
    print("Test CThin Reflector with Gamma Rotor")
    cipher = "ABCDE"
    print(f"INPUT = {cipher}")
    rotors = [("III",1,'A'),("II",1,'A'),("I",1,'A'),("Gamma",1,'A'),("CThin",1,'A')]
    print(rotors)
    plugBoardInputs = []
    output = ["P","X","S","V","V"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    for i,e in enumerate(cipher):
        assert(machine.encode(e) == output[i])
