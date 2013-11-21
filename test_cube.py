#!/usr/bin/python
"""
Image manipulation and processing using Numpy and Scipy:
http://www.tp.umu.se/~nylen/fnm/pylect/advanced/image_processing/index.html

Energy minimization with Graph Cuts (Herve Lombaert):
http://step.polymtl.ca/~rv101/energy/
"""

import numpy as np
from lib import pycrf
import itertools
import cv2

def index( i, j, img ):
    return j + img.shape[1]*i

img = cv2.imread("img/noisy_cube.png",0)
noisy = img

# Create CRF
num_pixels = img.shape[0]*img.shape[1]
num_labels = 256
crf = pycrf.CRF( num_pixels, num_labels )

# Set initial labels
crf.setLabels(noisy.flatten().astype('int32'))

# Set data cost
datacost = np.zeros(num_pixels*num_labels,dtype='float32')
for p in xrange(num_pixels):
    for l in xrange(num_labels):
        datacost[p*num_labels+l] = (noisy.flat[p]-l)**2

crf.setDataCost(datacost)

# Set label cost
smoothcost = np.zeros(num_labels*num_labels,dtype='float32')
for l1 in xrange(num_labels):
    for l2 in xrange(num_labels):
        smoothcost[l1+num_labels*l2] = float(l1 != l2)*2000

crf.setSmoothCost(smoothcost) 

r = [-1,0, 1]
neighbourhood = []
for a,b in itertools.product(r,r):
    if abs(a)+abs(b) > 0:
        neighbourhood.append((a,b))

print neighbourhood

# Build graph
for i in xrange(img.shape[0]):
    for j in xrange(img.shape[1]):
        for a,b in neighbourhood:
            if ( 0 <= i+a < img.shape[0]
                 and 0 <= j+b < img.shape[1]
                 and index(i,j,img) < index(i+a,j+b,img) ):
                crf.setNeighbors( index(i,j,img),
                                  index(i+a,j+b,img),
                                  1 )

# Solve CRF
print "initial energy: ", crf.compute_energy()
crf.expansion()
print "final energy: ", crf.compute_energy()

denoised = np.reshape( crf.getLabels(), img.shape)
cv2.imwrite("denoised_cube.png",denoised)
