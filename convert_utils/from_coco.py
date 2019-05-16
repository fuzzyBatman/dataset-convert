"""Conversion routines for formats from COCO to others."""

import os
import glob
import datetime

import json
from lxml import etree
from tqdm import tqdm


def get_coco_category_name(categories, category_id):
    for cat in categories:
        if cat['id'] == category_id:
            return cat['name']

    print('Category unknown for ID', category_id)
    return 'Unknown'


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
        # Load the i-th annotation file.
        ann_file = open(ann_file_names[i], "r")
        coco_ann_data = json.load(ann_file)

        # Get category data.
        ann_categories = coco_ann_data['categories']

        for img in coco_ann_data['images']:
            # Iterate over images in the i-th annotation file.
            image_id = img['id']
            category_ids = img['category_ids']

            pvoc_ann = {}
            pvoc_ann['root'] = etree.Element("annotation")

            # Add file name subelement
            pvoc_ann['filename'] = etree.SubElement(pvoc_ann['root'], "filename")
            pvoc_ann['filename'].text = img['file_name']

            # Image size subelement.
            pvoc_ann['size'] = etree.SubElement(pvoc_ann['root'], "size")
            pvoc_ann['width'] = etree.SubElement(pvoc_ann['size'], "width")
            pvoc_ann['height'] = etree.SubElement(pvoc_ann['size'], "height")
            pvoc_ann['depth'] = etree.SubElement(pvoc_ann['size'], "depth")

            pvoc_ann['width'].text = str(img['width'])
            pvoc_ann['height'].text = str(img['height'])
            # Image depth is set to 3 for now.
            pvoc_ann['depth'].text = "3"

            # Is segmented? True for COCO.
            # TODO: Add segmentations.
            pvoc_ann['segmented'] = etree.SubElement(pvoc_ann['root'], "segmented")
            pvoc_ann['segmented'].text = "0"    # ! For COCO the annotations are segmented

            # ! PASCAL VOC contains segmented annotations as well.
            # ! We currently focus on bounding boxes.

            # Add object annotations
            for ann in coco_ann_data['annotations']:
                # If the object is not for the current image.
                if ann['image_id'] != image_id:
                    pass

                obj = {}
                obj['root'] = etree.SubElement(pvoc_ann['root'], "object")
                # Add object name
                obj['name'] = etree.SubElement(obj['root'], "name")
                obj['name'].text = get_coco_category_name(ann_categories, ann['category_id'])

                # Truncated and Difficult elements
                obj['truncated'] = etree.SubElement(obj['root'], "truncated")
                obj['truncated'].text = "0"
                obj['difficult'] = etree.SubElement(obj['root'], "difficult")
                obj['difficult'].text = "0"

                # Add bounding box coordinates
                obj['bndbox'] = etree.SubElement(obj['root'], "bndbox")
                obj['xmin'] = etree.SubElement(obj['bndbox'], "xmin")
                obj['ymin'] = etree.SubElement(obj['bndbox'], "ymin")
                obj['xmax'] = etree.SubElement(obj['bndbox'], "xmax")
                obj['ymax'] = etree.SubElement(obj['bndbox'], "ymax")

                obj['xmin'].text = str(ann['bbox'][0])
                obj['ymin'].text = str(ann['bbox'][1])
                obj['xmax'].text = str(ann['bbox'][2])
                obj['ymax'].text = str(ann['bbox'][3])

            # Write the annotation data to its XML file.
            pvoc_ann_file_name = img['file_name'].split(".")[0] + ".xml"
            pvoc_ann_file = open(out_ann_dir + pvoc_ann_file_name, "wb")
            pvoc_ann_file.write(etree.tostring(pvoc_ann['root'], pretty_print=True))
            pvoc_ann_file.close()
    
    # End of coco2pascalvoc()
