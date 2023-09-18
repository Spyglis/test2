import os
import argparse

from pathlib import Path 


def id_number(row):
	index = row.find('4AP')
	return row[index:index+10]


def find_tests(source_path, find_string):
	id_list = []
	for root, dirs, files in os.walk(source_path):
		root = Path(root)
		for filex in files:
			if filex[-3:] == '.py':
				file_open = root / filex

			with open(file_open, 'r') as fl:
				lines = fl.readlines()
				for row in lines:
					if row.find(find_string) != -1:
						for row2 in lines:
							if row2.find("Polarion ID") != -1:
								id_list.append(id_number(row=row2))
	
	return set(id_list)
	

if __name__ =="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("PATTERN", help="Pattern to search for", type=str)
	parser.add_argument("DIR", help="Directory to search in", type=str)
	args = parser.parse_args()

	with open('search_results.txt', 'w') as results:
		results.write(str(find_tests(source_path=args.DIR, find_string=args.PATTERN)))
