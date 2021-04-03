from math import ceil
import os
def split_equal(file_path,size):
	with open(file_path,'r') as fil:
		content = fil.read()
		return (content[i : i + size] for i in range(0, len(content)))
def write_to_file(file_path,size,output_dir):
	file_parts=split_equal(file_path,size)
	for i,some in enumerate(file_parts):
		with open(output_dir+os.path.basename(file_path)+'_'+str(i+1),'w') as fil:
			fil.write(some)

def split_number(path_file,parts=None,size=None):
	if not size:
		size=os.path.getsize(path_file)
		size=size/parts
		size=int(ceil(size))
	write_to_file(file=path_file, splitsize=size,output_dir='media/')
	return os.path.getsize(path_file)/size

#split_number('new.png',2)
