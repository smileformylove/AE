# -*- coding: UTF-8 -*-
#arithmetic encoder and decoder
import numpy as np 
#import tensorflow as tf 

class arithmeticEncoding(object):
	"""docstring for arithmetic"""
	def __init__(self, code, codebook, num_code, num_codebook):
		self.code = code
		self.codebook = codebook
		self.num_code = num_code
		self.num_codebook = num_codebook
		
	def init_scope(self):
		init = [0]*self.num_codebook
		for i in np.arange(self.num_code):
			for j in np.arange(self.num_codebook):
				if(self.code[i] == self.codebook[j]):
					init[j] = init[j] + 1.0/self.num_code
					break

		scope = [[0,0] for _ in np.arange(self.num_codebook)]
		scope[0][0] = 0
		scope[0][1] = init[0]
		for i in np.arange(self.num_codebook - 1):
			scope[i+1][0] = scope[i][1]
			scope[i+1][1] = scope[i+1][0] + init[i+1]
		#init, self.codebook = QuickSort(init, 0, self.num_codebook)
		return init, scope

	def encoder(self):
		inter, scope = self.init_scope()
		interval = 1
		fore = 0
		back = 0
		for i in np.arange(self.num_code):
			for j in np.arange(self.num_codebook):
				if(self.code[i] == self.codebook[j]):
					fore = fore + interval * scope[j][0]
					back = fore + interval * scope[j][1] 
					interval = inter[j] * interval 
					break

		return fore, inter, scope

	def decoder(self, fore, inter, scope):
		r_code = [0]*self.num_code
		r_fore = 0
		r_back = 0
		r_interval = 1
		for i in np.arange(self.num_code):
			for j in np.arange(self.num_codebook):
				if fore >= scope[j][0]*r_interval+r_fore and fore < scope[j][1]*r_interval+r_fore:
					r_code[i] = self.codebook[j]
					r_fore = scope[j][0]*r_interval + r_fore
					r_back = scope[j][1]*r_interval + r_fore
					r_interval = r_interval * inter[j]
					break
		return r_code

def main():
	num_code = 8
	num_codebook = 3
	code = [2,1,3,3,2,1,3,1]
	codebook = [1,2,3]
	qq = arithmeticEncoding(code, codebook, num_code, num_codebook)

	fore, inter, scope = qq.encoder()
	r_code = qq.decoder(fore, inter, scope)
	print('encode=',fore)
	print('reconstruction=',r_code)

if __name__ == '__main__':
	main()
