# Paperdoll

A tool for generating indivitual images from the randomized layers
of a PSD file.

# Usage

Decompose a psd (creates `mypsd_decomposed` and inside it, the image elements
and `layerinfo.json`):

```
python decompose.py mypsd.psd
```

Create new images from decomposed psd (in `mypsd_output`):

```
python compose.py [number of images] [collision limit]
```

number of images = how many final images are desired

collision limit = how many times a duplicate result must be reached
before the program gives up and decides that it's finished

# Web "app"

`html/index.html` contains a simple script which will display created
images at a chosen resolution and re-create them on a button press.
It will be copied by `decompose.py` into the decompose directory.

It's a great way to quickly check what kinds of things your current
decomposition generates without having to spit out and view a bunch.
of real files.

You can't use it from a file:// URL because it accesses external files.
But since you're using python anyway, you can spin up a simple http server
like this:

```
python -m http.server
```

