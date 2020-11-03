import easygui
import xml.etree.ElementTree as ET
import os
import pandas as pd

def get_output_schema():
    return pd.DataFrame({
        'Name':prep_string(),
        'Remote Name':prep_string(),
        'Formula':prep_string(),
        'Comment':prep_string(),
       
    })

    
    # prompt user for twb file
def loader(df):    
    file = '/Users/timdries/Desktop/newf.xml'
        
        # parse the twb file
    tree = ET.parse(file)
    root = tree.getroot()
        
        # create a dictionary of name and tableau generated name
        
    calcDict = {}
        
    for item in root.findall('.//column[@caption]'):
        if item.find(".//calculation") is None:
            continue
        else:
            calcDict[item.attrib['name']] = '[' + item.attrib['caption'] + ']'

    # list of calc's name, tableau generated name, and calculation/formula
    calcList = []

    for item in root.findall('.//column[@caption]'):
        if item.find(".//calculation") is None: 
            continue
        else:
            if item.find(".//calculation[@formula]") is None:
                continue
            else:
                calc_caption = '[' + item.attrib['caption'] + ']'
                calc_name = item.attrib['name']
                calc_raw_formula = item.find(".//calculation").attrib['formula']
                calc_comment = ''
                calc_formula = ''
                for line in calc_raw_formula.split('\r\n'):
                    if line.startswith('//'):
                        calc_comment = calc_comment + line + ' '
                    else:
                        calc_formula = calc_formula + line + ' '
                for name, caption in calcDict.items():
                    calc_formula = calc_formula.replace(name, caption)

                calc_row = (calc_caption, calc_name, calc_formula, calc_comment)
                calcList.append(list(calc_row))

    # convert the list of calcs into a data frame
    df = calcList

    df = pd.DataFrame(df, columns=['Name', 'Remote Name', 'Formula', 'Comment'])

    return df