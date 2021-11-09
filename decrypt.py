from PIL import Image
import cv2
# import Image
from random import randint
import numpy
import sys
from helper import *
import zipfile




def decrypt_image(file_name):
	# file_name = "my_python_files.zip"
	with zipfile.ZipFile(file_name, 'r') as zip:
		# printing all the contents of the zip file
		zip.printdir()
	
		# extracting all the files
		print('Extracting all the files now...')
		zip.extractall()
		print('Done!')
		
	im = Image.open('output/' + 'secure.png')
	pix = im.load()


	#Obtaining the RGB matrices
	r = []
	g = []
	b = []
	for i in range(im.size[0]):
		r.append([])
		g.append([])
		b.append([]) 
		for j in range(im.size[1]):
			rgbPerPixel = pix[i,j]
			r[i].append(rgbPerPixel[0])
			g[i].append(rgbPerPixel[1])
			b[i].append(rgbPerPixel[2])

	# print(im.size)
	m = im.size[0]
	n = im.size[1]

	Kr = []
	Kc = []
	# 
	f = open('output/keys_kr.txt','r')
	file_details_kc=f.readline()
	for a in range(m):
		Kr.append(int(f.readline().strip('\n')))
	# print(Kr)
	f.close()
	# 

	f = open('output/keys_kc.txt','r')
	file_details_kr=f.readline()
	for i in range(n):
		Kc.append(int(f.readline().strip('\n')))
	f.close()

	# print('Enter value of ITER_MAX')
	ITER_MAX = 1


	for iterations in range(ITER_MAX):
		# For each column
		for j in range(n):
			for i in range(m):
				if(j%2==0):
					r[i][j] = r[i][j] ^ Kr[i]
					g[i][j] = g[i][j] ^ Kr[i]
					b[i][j] = b[i][j] ^ Kr[i]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kr[i])
					g[i][j] = g[i][j] ^ rotate180(Kr[i])
					b[i][j] = b[i][j] ^ rotate180(Kr[i])
		# For each row
		for i in range(m):
			for j in range(n):
				if(i%2==1):
					r[i][j] = r[i][j] ^ Kc[j]
					g[i][j] = g[i][j] ^ Kc[j]
					b[i][j] = b[i][j] ^ Kc[j]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kc[j])
					g[i][j] = g[i][j] ^ rotate180(Kc[j])
					b[i][j] = b[i][j] ^ rotate180(Kc[j])
		# For each column
		for i in range(n):
			rTotalSum = 0
			gTotalSum = 0
			bTotalSum = 0
			for j in range(m):
				rTotalSum += r[j][i]
				gTotalSum += g[j][i]
				bTotalSum += b[j][i]
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				downshift(r,i,Kc[i])
			else:
				upshift(r,i,Kc[i])
			if(gModulus==0):
				downshift(g,i,Kc[i])
			else:
				upshift(g,i,Kc[i])
			if(bModulus==0):
				downshift(b,i,Kc[i])
			else:
				upshift(b,i,Kc[i])

		# For each row
		for i in range(m):
			rTotalSum = sum(r[i])
			gTotalSum = sum(g[i])
			bTotalSum = sum(b[i])
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				r[i] = numpy.roll(r[i],-Kr[i])
			else:
				r[i] = numpy.roll(r[i],Kr[i])
			if(gModulus==0):
				g[i] = numpy.roll(g[i],-Kr[i])
			else:
				g[i] = numpy.roll(g[i],Kr[i])
			if(bModulus==0):
				b[i] = numpy.roll(b[i],-Kr[i])
			else:
				b[i] = numpy.roll(b[i],Kr[i])

	for i in range(m):
		for j in range(n):
			pix[i,j] = (r[i][j],g[i][j],b[i][j])
	#

	# im=image_resize(im,width=300)
	print('sending')

	im.save('decrypted_images/' + 'decrypted_image.png')


