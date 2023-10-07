import time
import os
import random
import math
import torch
import numpy as np

# run `pip install scikit-image` to install skimage, if you haven't done so
from skimage import io, color
from skimage.transform import rescale

def distance(x, X):
   # print("X shape",X.shape)
   # print("x shape",x.shape)
   # print("x-X shape",(x-X).shape)
    return torch.linalg.norm(x-X,axis=1)
def distance_batch(x, X):
    X1 = x.unsqueeze(2)
    X2 = x.T
    X2 = X2.unsqueeze(0)
    #X1-X2  # d1*d2 *d1
    return torch.linalg.norm(X1-X2,axis=1)
def gaussian(dist, bandwidth):
    #print("dist shape",dist.shape) #check if the normalization is needed what happens if we remove it? todo:
    #return 1/(np.sqrt(2*np.pi)*bandwidth)*np.exp(-0.5*dist**2/bandwidth**2)
    return np.exp(-0.5*(dist**2)/(bandwidth**2))

def update_point(weight, X):
   # print("weight shape",weight.shape)
    return (weight@X)/torch.sum(weight)
def update_point_batch(weight, X):
    #print((weight@X).shape)
    #print(torch.sum(weight,axis=1).shape)
    return (weight@X)/torch.sum(weight,axis=1).reshape(-1,1)

def meanshift_step(X, bandwidth=2.5):
    X_ = X.clone()
    for i, x in enumerate(X):
        dist = distance(x, X)
        #print("dist ",dist)
        weight = gaussian(dist, bandwidth)
        #print("weight ",weight)
        X_[i] = update_point(weight, X)
    return X_

def meanshift_step_batch(X, bandwidth=2.5):
    X_ = X.clone()
   
    dist = distance_batch(X, X)
    #print("dist ",dist)
    weight = gaussian(dist, bandwidth)
    #print("weight ",weight.shape)
    X_ = update_point_batch(weight, X)
    return X_

def meanshift(X):
    X = X.clone()
    for i in range(20):
        print(i,"steps")
        #X = meanshift_step(X)   # slow implementation
        X = meanshift_step_batch(X)   # fast implementation
    return X

scale = 0.25    # downscale the image to run faster

# Load image and convert it to CIELAB space
image = rescale(io.imread('cow.jpg'), scale, multichannel=True)
image_lab = color.rgb2lab(image)
shape = image_lab.shape # record image shape
print(shape)
image_lab = image_lab.reshape([-1, 3])  # flatten the image
print(image_lab.shape,"imagelab shape")
# Run your mean-shift algorithm
t = time.time()
X = meanshift(torch.from_numpy(image_lab)).detach().cpu().numpy()
# X = meanshift(torch.from_numpy(data).cuda()).detach().cpu().numpy()  # you can use GPU if you have one
t = time.time() - t
print ('Elapsed time for mean-shift: {}'.format(t))

# Load label colors and draw labels as an image
colors = np.load('colors.npz')['colors']
colors[colors > 1.0] = 1
colors[colors < 0.0] = 0

centroids, labels = np.unique((X / 4).round(), return_inverse=True, axis=0)

result_image = colors[labels].reshape(shape)
result_image = rescale(result_image, 1 / scale, order=0, multichannel=True)     # resize result image to original resolution
result_image = (result_image * 255).astype(np.uint8)
io.imsave('result.png', result_image)
