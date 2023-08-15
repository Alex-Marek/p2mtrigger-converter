from collections import defaultdict
import sys
def convertCCtoNormal(path):
    invalidValues = ["load action=force_start", "flags action=stop", "sar_speedrun_cc_finish", "var:no_mtriggers=1"]
    prefix = "sar_speedrun_rule_create"
    actionName = "action=split"
    with open(path, 'r+') as file:
        with open("MtriggersFile.cfg", 'a') as Newfile:
            mapName = ""
            for line in file:
                mtrigValues = defaultdict(str)
                line = line.strip("\n")
                line = line.replace('"', "")
                validLine = True

                for invalidStrs in invalidValues:
                    if line.find(invalidStrs) > -1:
                        validLine = False

                if validLine == True:
                    values = line.split(' ')
                    for words in values:
                        if words == "sar_speedrun_cc_rule": continue
                        elif words.find("map=") > -1: mapName += words
                        elif words == "entity" or words == "zone" or words == "portal": mtrigValues["mtrig_type"] = words
                        elif words.find("targetname=") > -1: mtrigValues["targetname"] = words
                        elif words.find("center=") > -1: mtrigValues["center"] = words
                        elif words.find("size=") > -1: mtrigValues["size"] = words
                        elif words.find("radius=") > -1: mtrigValues["radius"] = words
                        elif words.find("angle=") > -1: mtrigValues["angle"] = words
                        elif words.find("inputname=") > -1: mtrigValues["inputname"] = words
                        elif words.find("parameter=") > -1: mtrigValues["parameter"] = words
                        else: mtrigValues["name"] += (f'{words} ')
                    mtrigValues["map"] = mapName
                    mtrigValues["action"] = actionName

                if len(mtrigValues) > 3:
                    if mtrigValues["mtrig_type"] == "entity" and mtrigValues["parameter"] == "":
                        Newfile.write(f'{prefix} "{mtrigValues["map"][4:]}:{mtrigValues["name"][:-1]}" "{mtrigValues["mtrig_type"]}" "{mtrigValues["map"]}" "{mtrigValues["targetname"]}" "{mtrigValues["inputname"]}" "{mtrigValues["action"]}"\n')
                    if mtrigValues["mtrig_type"] == "entity" and mtrigValues["parameter"] != "":
                        Newfile.write(f'{prefix} "{mtrigValues["map"][4:]}:{mtrigValues["name"][:-1]}" "{mtrigValues["mtrig_type"]}" "{mtrigValues["map"]}" "{mtrigValues["targetname"]}" "{mtrigValues["inputname"]}" "{mtrigValues["parameter"]}" "{mtrigValues["action"]}"\n')
                    elif mtrigValues["mtrig_type"] == "zone":
                        Newfile.write(f'{prefix} "{mtrigValues["map"][4:]}:{mtrigValues["name"][:-1]}" "{mtrigValues["mtrig_type"]}" "{mtrigValues["map"]}" "{mtrigValues["center"]}" "{mtrigValues["size"]}" "{mtrigValues["angle"]}" "{mtrigValues["action"]}"\n')
                    elif mtrigValues["mtrig_type"] == "portal":
                        Newfile.write(f'{prefix} "{mtrigValues["map"][4:]}:{mtrigValues["name"][:-1]}" "{mtrigValues["mtrig_type"]}" "{mtrigValues["map"]}" "{mtrigValues["center"]}" "{mtrigValues["size"]}" "{mtrigValues["angle"]}" "{mtrigValues["action"]}"\n')
                    Newfile.write(f'sar_speedrun_category_add_rule Singleplayer "{mtrigValues["map"][4:]}:{mtrigValues["name"][:-1]}"\n\n')
            
            Newfile.write(f'{prefix} "{mapName[4:]}:Transition Ready" "entity" "{mapName}" "targetname=@transition_script" "inputname=RunScriptCode" "parameter=TransitionReady()" "{actionName}"\n')
            Newfile.write(f'sar_speedrun_category_add_rule Singleplayer "{mapName[4:]}:Transition Ready"\n\n')
            Newfile.write(f'{prefix} "{mapName[4:]}:Transition" "entity" "{mapName}" "targetname=@transition_script" "inputname=RunScriptCode" "parameter=TransitionFromMap()" "{actionName}"\n')
            Newfile.write(f'sar_speedrun_category_add_rule Singleplayer "{mapName[4:]}:Transition"\n\n')
            Newfile.write(f'//{mapName} ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n')

files= sys.argv[1:]
for convert in files:
    convertCCtoNormal(convert)

