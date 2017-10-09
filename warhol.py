import sys
import random
import math
import PIL
from PIL import Image
from PIL import ImageFilter
import cv2
import numpy

from datetime import datetime


def sp_noise(image, prob):
  '''
  Add salt and pepper noise to image
  prob: Probability of the noise
  '''
  output = numpy.zeros(image.shape, numpy.uint8)
  thres = 1 - prob 
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      rdn = random.random()
      if rdn < prob:
        output[i][j] = 0
      elif rdn > thres:
        output[i][j] = 255
      else:
        output[i][j] = image[i][j]
  return output


image_set = ['trees.jpg', 
             'moon.jpg', 
             'moon2.jpg', 
             'close_branches.jpg',
             'branches.jpg', 
             'sunset.jpg']

images_set = [ PIL.Image.open(i) for i in image_set ]
columns = 5
rows = 5

noise_scaling_factor = 0.1

total_width = columns * images_set[0].width
total_height = rows * images_set[0].height

new_im = Image.new('RGB', (total_width, total_height))


x_offset = 0
y_offset = 0

j = 0
for j in range(j, rows):
    x_offset = 0
    i = 0
    for i in range(i, columns):
        image = images_set[math.floor(random.uniform(0, len(image_set)))]
        xfer_matrix = (
                random.random(), random.random(), random.random(), 0,
                random.random(), random.random(), random.random(), 0,
                random.random(), random.random(), random.random(), 0 )

        black_and_white = image.convert(mode="L",
                                        matrix=xfer_matrix,
                                        dither=None,
                                        palette=0,
                                        colors=256/(i*i+1))

        unsharp_image = black_and_white.filter(
                PIL.ImageFilter.UnsharpMask(radius=math.floor(random.uniform(3,100)),
                                            percent=math.floor(random.uniform(100,400)),
                                            threshold=math.floor(random.uniform(5,10))))

        opencv_image = numpy.array(unsharp_image)

        noise_image = sp_noise(opencv_image, ((i*j)/(columns*rows))*noise_scaling_factor)

        processed_image = noise_image 

        new_im.paste(Image.fromarray(processed_image),
                     (x_offset,y_offset))
        x_offset += image.width
    y_offset += image.height

filename = datetime.now().strftime('%Y-%m-%d_%H%M%Spip_black_and_white.jpg')
new_im.save(filename)
