"""Conversion routines for formats from COCO to others."""

import os
import glob
import datetime

import json
from tqdm import tqdm


def coco2pascalvoc(in_dir, out_dir):
    """Convert the dataset given in COCO format to PASCALVOC format"""

    # Check whether in_dir exists.
    assert os.path.exists(
        in_dir), " The directory '{}' does not exist".format(in_dir)

    # Check whether out_dir exists.
    if not os.path.exists(out_dir):
        print("Warning: The output directory '{}' does not exist".format(out_dir))
        print("Using the default directory '{}'".format(in_dir))
        out_dir = in_dir
    
    # Add a path separator at the end for consistency.
    if in_dir[-1] != os.sep:
        in_dir = in_dir + os.sep
    if out_dir[-1] != os.sep:
        out_dir = out_dir + os.sep

    ann_dir = in_dir + 'annotations' + os.sep
    # Check whether the 'annotations directory exists'.
    assert os.path.exists(ann_dir), "The directory named 'annotations' does not exist.\
        Make sure your dataset is organised in the standard COCO format."

    # Get the names of all the annotation files (JSON format).
    ann_file_names = glob.glob(ann_dir + '*.json')
    num_ann_files = len(ann_file_names)

    print("{} JSON file".format(num_ann_files) +
        ("s" if num_ann_files != 1 else "") + " found")

    # Create dir to store PASCAL VOC annotations.
    dt_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_ann_dir = out_dir + "PASCAL_VOC_" + dt_string + os.sep

    assert not os.path.exists(
        out_ann_dir), "An output directory with the time stamp {} exists".format(dt_string)
    out_ann_dir = out_ann_dir + "Annotations" + os.sep
    os.makedirs(out_ann_dir)

    # Process the COCO annotation files and create the PASCAL VOC annotations.
    for i in tqdm(range(num_ann_files)):
        pass
