#!/usr/bin/env python

import argparse
import shutil
import os
from os import path as osp
import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from cv2 import cv2
import numpy as np
import random

sys.path.append('./')
from lib.annotator import Annotator

def ClearOutputDir(test_path):
    if osp.exists(test_path):
        # output dir exists
        if len(os.listdir(test_path)) != 0:
            print('Ouput dir {} exists and not empty '.format(test_path))
            # TODO: show the description of directory
            c = input('Clear?: y/n ')
            if c == 'y':
                print('Erasing...')
                shutil.rmtree(test_path)
                os.makedirs(test_path)
            else:
                print('Please check the contents of your output directory')
                sys.exit(1)
    else:
        # make new output dir
        os.makedirs(test_path)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input_file', help='the name of input file', required=True)
    parser.add_argument('--clip_start_min', help='the start minute of clip part', required=True, type=float)
    parser.add_argument('--clip_start_sec', help='the start second of clip part', required=True, type=float)
    parser.add_argument('--clip_end_min', help='the end minute of clip part', required=True, type=float)
    parser.add_argument('--clip_end_sec', help='the end second of clip part', required=True, type=float)
    parser.add_argument('--flag', nargs='+', help='the flags', required=True)
    parser.add_argument('--dur', help='the dur', required=True, type=int)
    parser.add_argument('--overlap', help='the overlap, between 0-1.0, float', required=True, type=float)
    parser.add_argument('--n_show', help='num of window per page', default=100, type=int)
    args = parser.parse_args()

    prefix = args.input_file.split('.')[0]
    start_min = args.clip_start_min
    start_sec = args.clip_start_sec
    end_min = args.clip_end_min
    end_sec = args.clip_end_sec
    start_time = start_min*60+start_sec
    end_time = end_min*60+end_sec

    target_file = prefix+'_clip.mp4'
    ffmpeg_extract_subclip(args.input_file, start_time, end_time, targetname=target_file)

    clips_folder = prefix
    ClearOutputDir(clips_folder)

    label_file = prefix +'.json'

    if osp.exists(label_file):
        os.remove(label_file)

    # Split the video into clips
    flag_list = []
    for cnt, ele in enumerate(args.flag):
        flag_color = tuple([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
        print("{} flag: {} with color {}".format(cnt, ele, flag_color))
        flag_list.append({'name':ele,'color':flag_color})
    
    # print(flag_list)

    annotator = Annotator(flag_list,
            clips_folder, sort_files_list=True, N_show_approx=args.n_show, screen_ratio=16/9, 
            image_resize=1, loop_duration=None, annotation_file=label_file)

    # annotator = Annotator([
    #        {'name': 'play', 'color': (0, 255, 0)},
    #        {'name': 'smash', 'color': (0, 0, 255)},
    #        {'name': 'serve', 'color': (0, 255, 255)},
    #        {'name': 'walk', 'color': (255, 255, 0)},
    #        {'name': 'clean', 'color': (255, 0, 255)}],
    #        clips_folder, sort_files_list=True, N_show_approx=100, screen_ratio=16/9, 
    #        image_resize=1, loop_duration=None, annotation_file=label_file)
    print('Generating clips from the video...')
    annotator.video_to_clips(target_file, clips_folder, clip_length=args.dur, overlap=args.overlap, resize=0.5)

    # Run the annotator
    annotator.main()


if __name__ == '__main__':
    main()