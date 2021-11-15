#!/usr/bin/env python

import psd_tools, os, sys, json

psdfile = sys.argv[1]

psd = psd_tools.PSDImage.open(psdfile)
psdbasename = os.path.splitext(psdfile)[0]

output_dir = psdbasename + '_decomposed'

if not os.path.isdir(output_dir):
  os.mkdir(output_dir)

def decompose_layer(layer, main_dir, parent_dirs, index=0):
  layer_filename =  "%d-%s" % (index, layer.name)
  full_layer_list = [main_dir] + parent_dirs + [layer_filename]
  full_layer_path = os.path.join(*full_layer_list)
  print("decomposing " + layer.name)
  if layer.kind == 'group' or layer.kind == "psdimage":
    if not os.path.isdir(full_layer_path):
      os.mkdir(full_layer_path)
    sublayers_decomposed =  [
      decompose_layer(sublayer, main_dir, parent_dirs + [layer_filename], sublayer_index)
      for sublayer_index, sublayer in enumerate(layer)
    ]
    return {
      "name" : layer.name,
      "type" : "group",
      "filename" : layer_filename,
      "contents" : sublayers_decomposed
    }
  if layer.kind == 'pixel':
    layer_filename = layer_filename + ".png"
    full_layer_path = full_layer_path + ".png"
    image = layer.composite()
    # image_size = image.size
    # print("image size is: ", image_size)
    if os.path.exists(full_layer_path):
      os.remove(full_layer_path)
    image.save(full_layer_path)
    return {
      "name" : layer.name,
      "filename" : layer_filename,
      "type" : "image"
    }

image_size = psd.composite().size
decomposed_stuff = decompose_layer(psd, output_dir, [])
output = { "layers" : decomposed_stuff, "size": image_size }

print(json.dumps(decomposed_stuff, indent=2))
with open(os.path.join(output_dir, "layerinfo.json"), "w") as fp:
  json.dump(output, fp)

if not os.path.exists(os.path.join(output_dir, "index.html")):
  shutil.copy(os.path.join("html", "index.html"), output_dir)

  
