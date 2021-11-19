#!/usr/bin/env python

import os, sys, random, PIL, hashlib, base64, re, json
from PIL import Image

decompose_dir = sys.argv[1].rstrip('/')
compose_dir = decompose_dir.replace('_decomposed', '_output')
num_images = 1
collision_limit = 5

if len(sys.argv) > 2:
  num_images = int(sys.argv[2])
  if len(sys.argv) > 3:
    collision_limit = int(sys.argv[3])

random.seed()

def get_layer_name(path):
  basename_with_ext = os.path.basename(path)
  basename, ext = os.path.splitext(basename_with_ext)
  layer_name = re.compile('^[0-9]+-').sub('', basename)
  return layer_name

def parse_info(layerinfo, main_dir, parent_dirs=[]):
  layer_name = layerinfo["name"]
  if layer_name.endswith('optional'):
    if random.randrange(2) == 1:
      return
    else:
      choices_made.append(layer_name)
  if layerinfo["type"] == "group":
    contents = layerinfo["contents"]
    if layer_name.startswith('choice'):
      chosen = random.choice(contents)
      choices_made.append(chosen["name"])
      parse_info(chosen, main_dir, parent_dirs + [layerinfo["filename"]])
    else:
      for sublayer in layerinfo["contents"]:
        parse_info(sublayer, main_dir, parent_dirs + [layerinfo["filename"]])
  elif layerinfo["type"] == "image":
    full_path_list = parent_dirs + [layerinfo["filename"]]
    layers_to_use.append(os.path.join(*full_path_list))

images_to_make = num_images 
collisions = 0

if not os.path.isdir(compose_dir):
  os.mkdir(compose_dir)

while images_to_make > 0 and collisions < collision_limit:
  print("images to make: %d collisions: %d" % (images_to_make, collisions))
  layers_to_use = []
  choices_made = []

  with open(os.path.join(decompose_dir, "layerinfo.json")) as f:
    imageinfo = json.load(f)
  layerinfo = imageinfo["layers"]  
  parse_info(layerinfo, decompose_dir)
  choice_string = "-".join([str(choice) for choice in choices_made])
  h = hashlib.md5()
  h.update(choice_string.encode('utf-8'))
  choice_hash = base64.b32encode(h.digest()).decode('utf-8')[0:8]
  final_fn = choice_hash + ".png"

  if os.path.exists(final_fn):
    print("whoopsie, %s already exists" % (final_fn))
    collisions = collisions + 1
  else:
    print("creating %s" % (final_fn))
    final_image = PIL.Image.open(os.path.join(decompose_dir, layers_to_use.pop(0)))
    for layer in layers_to_use:
      with PIL.Image.open(os.path.join(decompose_dir, layer)) as next_image:
        final_image = PIL.Image.alpha_composite(final_image, next_image)
    final_image.save(os.path.join(os.getcwd(), compose_dir, final_fn))
    images_to_make = images_to_make - 1

