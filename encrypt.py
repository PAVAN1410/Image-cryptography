# import Image
from PIL import Image

from random import randint
import numpy
import sys
from helper import *
import zipfile
import os

def encrypt_image(image):
	im = Image.open(image)
	im=im.resize((150,250))
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

	m = im.size[0]
	n = im.size[1]

	# Vectors Kr and Kc
	alpha = 8
	Kr = [randint(0,pow(2,alpha)-1) for i in range(m)]
	Kc = [randint(0,pow(2,alpha)-1) for i in range(n)]
	ITER_MAX = 1

	print('Vector Kr : ', Kr)
	print('Vector Kc : ', Kc)

	f = open('output/keys_kr.txt','w+')
	f.write('Vector Kr : \n')
	for a in Kr:
		f.write(str(a) + '\n')
	f.close()
	f = open('output/keys_kc.txt','w+')
	f.write('Vector Kc : \n')
	for a in Kc:
		f.write(str(a) + '\n')
	f.close()


	for iterations in range(ITER_MAX):
		# For each row
		for i in range(m):
			rTotalSum = sum(r[i])
			gTotalSum = sum(g[i])
			bTotalSum = sum(b[i])
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				r[i] = numpy.roll(r[i],Kr[i])
			else:
				r[i] = numpy.roll(r[i],-Kr[i])
			if(gModulus==0):
				g[i] = numpy.roll(g[i],Kr[i])
			else:
				g[i] = numpy.roll(g[i],-Kr[i])
			if(bModulus==0):
				b[i] = numpy.roll(b[i],Kr[i])
			else:
				b[i] = numpy.roll(b[i],-Kr[i])
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
				upshift(r,i,Kc[i])
			else:
				downshift(r,i,Kc[i])
			if(gModulus==0):
				upshift(g,i,Kc[i])
			else:
				downshift(g,i,Kc[i])
			if(bModulus==0):
				upshift(b,i,Kc[i])
			else:
				downshift(b,i,Kc[i])
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


	for i in range(m):
		for j in range(n):
			pix[i,j] = (r[i][j],g[i][j],b[i][j])

	im.save('output/secure.png')
	folder_to_be_zipped = 'output'

	with zipfile.ZipFile('webzip.zip', 'w', zipfile.ZIP_DEFLATED) as outputzip:
		for dirpath, dirnames, files in os.walk(folder_to_be_zipped):
			for file in files:
				outputzip.write(os.path.join(dirpath, file))
	

# encrypt('pic2.png')

