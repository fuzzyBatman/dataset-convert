"""Converts a dataset in a given format to another.

COCO -> PASCAL VOC
"""

import argparse
from argparse import RawTextHelpFormatter

from convert_utils.from_coco import coco2pascalvoc

VALID_IN_FORMATS = ['COCO']
VALID_OUT_FORMATS = ['PASCALVOC']


def run_main():
    """The main function of the covert script"""

    parser = argparse.ArgumentParser(
        description="Convert the given dataset annotation to another", formatter_class=RawTextHelpFormatter)
    parser.register("type", "bool", lambda v: v.lower() == "true")

    parser.add_argument(
        "--data_dir",
        type=str,
        default="./",
        help="Path to the dataset to convert (default: .)")
    parser.add_argument(
        "--in_format",
        type=str,
        default="",
        help="Annotation format of the input dataset\
            \n\
            \n- COCO\
            ")
    parser.add_argument(
        "--out_format",
        type=str,
        default="",
        help="Annotation format of the output dataset\
            \n\
            \n- PASCALVOC\
            ")
    parser.add_argument(
        "--out_dir",
        type=str,
        default=None,
        help="Output directory (default: same as input directory)")

    args = parser.parse_args()

    data_dir = args.data_dir
    in_format = args.in_format.upper()      # coco -> COCO
    out_format = args.out_format.upper()
    out_dir = args.out_dir

    # If output directory is not provided, then set default to data_dir.
    if out_dir is None:
        out_dir = data_dir
    
    print("\n")

    # Check arguments for validity
    assert in_format in VALID_IN_FORMATS, \
        "The provided input format '{}' is not supported or is invalid".format(
            in_format)

    assert out_format in VALID_OUT_FORMATS, \
        "The provided output format '{}' is not supported or is invalid".format(
            out_format)

    # Start the conversion
    if in_format == 'COCO':
        if out_format == 'PASCALVOC':
            coco2pascalvoc(data_dir, out_dir)


if __name__ == "__main__":
    run_main()
