#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""feature detection.

Usage:
    feature_detection.py
        --target_file_path=<target_file_path>
        --comparing_dir_path=<comparing_dir_path>
    feature_detection.py -h | --help
Options:
    -h --help show this screen and exit.
"""

import cv2
from docopt import docopt
import glob
import logging
import os
import sys

if __name__ == '__main__':
    # logging config
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    logging.info('%s start.' % (__file__))

    # get parameters
    args = docopt(__doc__)
    target_file_path = args['--target_file_path']
    comparing_dir_path = args['--comparing_dir_path']
    print("きちゃ！！！！！！！")

    # setting
    img_size = (200, 200)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # detector = cv2.ORB_create()
    detector = cv2.AKAZE_create()
    ret = {}
    print("きちゃ！！！！！！！")

    # get comparing files
    pattern = '%s/*.jpg'
    comparing_files = glob.glob(pattern % ("./image/T_shirt"))
    if len(comparing_files) == 0:
        logging.error('no files.')
        sys.exit(1)

    print("きちゃ！！！！！！！")

    # read target image
    target_file_name = os.path.basename(target_file_path)
    target_img = cv2.imread(target_file_path, cv2.IMREAD_GRAYSCALE)
    target_img = cv2.resize(target_img, img_size)
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)

    for i in range(len(comparing_files)):
        # read comparing image
        comparing_img_path = comparing_files
        comparing_img = cv2.imread(comparing_img_path[i], cv2.IMREAD_GRAYSCALE)
        comparing_img = cv2.resize(comparing_img, img_size)
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)

        # detect
        matches = bf.match(target_des, comparing_des)
        dist = [m.distance for m in matches]
        ret[comparing_img_path[i]] = sum(dist) / len(dist)

    # sort
    for k, v in sorted(ret.items(), reverse=False, key=lambda x: x[1]):
        logging.info('%s: %f.' % (k, v))

    logging.info('%s end.' % (__file__))
    sys.exit(0)