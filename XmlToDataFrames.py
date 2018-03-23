import sys, getopt
import lxml
import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree

holding_file = "HoldingsSummary.xml"
program_name = "AdjustHolding.py"

def print_el(el):
	print(etree.tostring(el , pretty_print=True))

def el_to_dict(el):
	dict = {}
	for child in el:
		dict[child.tag] = child.text
	return dict

all_top_level_elements = etree.parse(holding_file).getroot()

unique_top_level_elements = {};
unique_top_level_elements_headers = {};

for element in all_top_level_elements:
	flat_version = el_to_dict(element)
	if not element.tag in unique_top_level_elements:
		unique_top_level_elements[element.tag] = [];
		unique_top_level_elements_headers[element.tag] = flat_version.keys()
	else:		
		unique_top_level_elements[element.tag].append(flat_version.values())

dfs = {};
for top_type_key in unique_top_level_elements.keys():
	tuple_rows = [tuple(l) for l in unique_top_level_elements[top_type_key]]	
	cols = unique_top_level_elements_headers[top_type_key]
	if(len(tuple_rows) > 0):
		df = pd.DataFrame(tuple_rows, columns=cols)
		dfs[top_type_key] = df

HoldingDataDf = dfs['HoldingsData']
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	group = HoldingDataDf.groupby('HoldingsDate')['Ticker'].count()
	print(group)
