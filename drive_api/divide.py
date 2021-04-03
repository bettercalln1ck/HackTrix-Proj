from math import ceil
import os
import base64

def write_to_file(file_path,size,output_dir):
	CHUNK_SIZE = size
	file_number = 1
	with open(file_path,'rb') as fil:
		chunk = fil.read(size)
		while chunk:
			with open(output_dir+os.path.basename(file_path)+'_'+str(file_number),'wb') as fip:
				fip.write(chunk)
			file_number += 1
			chunk = fil.read(CHUNK_SIZE)

def split_number(path_file,parts=None,size=None):
	if not size:
		size=os.path.getsize(path_file)
		size=size/parts
		size = size
		size=int(ceil(size))
	write_to_file(file_path=path_file, size=size,output_dir='media/')
	return os.path.getsize(path_file)/size


