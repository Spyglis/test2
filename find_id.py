import os
from argparse import ArgumentParser

from pathlib import Path 


class TestFind:
	start_nr: str = "4AP"
	file_ext: str = "*.py"
	start_id: str = 'Polarion ID'


	def __init__(self):
		self.source_path: Path = Path("C:/Users/marius.sutkus.QDTEAM/Documents/training/code/test2") #args.DIR
		self.pattern: str = 'hydraulics_connetor.reconnect_shunts('  #args.PATTERN
		self.id_list: list = []



	def id_number(self, row):
		index = row.find(self.start_nr)
		return row[index:index+10]


	def find_files(self):
		return self.source_path.rglob(self.file_ext)

	def find_tests(self):

		list_of_files = self.find_files()
		# print(sorted(list_of_files))
		for file_name in list_of_files:
			read_text = Path(file_name).read_text()
		
			for row in read_text:
				print(row)
				if row.find(self.pattern) != -1:
					for row2 in read_text:
						if row2.find(self.start_id) != -1:
							self.id_list.append(self.id_number(row=row2))
		print(self.id_list)
		
		# return set(id_list)
	

if __name__ =="__main__":

	# parser: ArgumentParser = ArgumentParser(description="Search for test case ID number, which contains the pattern.")
	# parser.add_argument("PATTERN", help="Pattern to search for", type=str)
	# parser.add_argument("DIR", help="Directory to search in", type=Path)
	# args = parser.parse_args()
	find_tc = TestFind()
	find_tc.find_tests()

	# path = Path("C:/Users/marius.sutkus.QDTEAM/Documents/training/code/TestAutomation")
	# list_of_files = path.rglob('*.py')
	# for file in list_of_files:
	# 	print(file)
	# print(list)

	# with open('search_results.txt', 'w') as results:
	# 	results.write(str(find_tests(source_path=args.DIR, find_string=args.PATTERN)))
