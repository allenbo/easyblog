import os
import Image


def resize_image(filename, height, width, save_to = None):
  img = Image.open(filename)
  
  old_width, old_height = img.size
  radio = old_height / float(height) if height > width else old_width /float(width)
  height, width = int( old_height/radio), int(old_width/radio)

  img = img.resize((width, height), Image.ANTIALIAS)
  if save_to is None:
    save_to = filename
  img.save(save_to)
