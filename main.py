#!/bin/python3

import os
import re
import sys
import time

"""
    About the *.SRT file format please refer to https://wiki.videolan.org/SubRip/
    
    Each frame of a subtitle is formatted as follows:

        n
        h1:m1:s1,d1 --> h2:m2:s2,d2
        Line 1
        Line 2
    
    Example
    A 2-frame subtitle:

    1
    00:00:20,000 --> 00:00:24,400
    a bla bla ble a bla bla ble
    a bla bla ble

    2
    00:00:24,600 --> 00:00:27,800
    a bla bla ble…
"""

def get_srt_time(tm_val):
    if len(tm_val) > 2:
        srt_tm = f'{tm_val[0]:02d}:{tm_val[1]:02d}:{tm_val[2]:02d},000'
    else:
        srt_tm = f'00:{tm_val[0]:02d}:{tm_val[1]:02d},000'
    return srt_tm
                    
                    
if __name__ == '__main__': 
    # test passed arguments
    # print('\n'.join(sys.argv))
       
    ytsub_f_name = sys.argv[1]
    ytsub_f_title = ytsub_f_name.replace('.txt', '')
    #ytsub_f_basename = os.path.basename(ytsub_f_name)
    # print(ytsub_f_basename)
    
    srt_sub_f_name = f'{ytsub_f_title}.srt'
    
    fsrt = open(srt_sub_f_name, 'w')
    fytsub = open(ytsub_f_name, 'r')
    lno = 1
    last_tm_lno = 0
    
    last_tm_vals = []
    cur_tm_vals = []
    frame_no = 1
    content = ''
    
    for line in fytsub:
        pattern = re.compile("^[0-9]+:[0-9]+$")
        if pattern.match(line):
            if last_tm_lno != 0:
                # extract subtitle text from last time line to this line                
                cur_tm_vals = line.rstrip().split(':')
                cur_tm_vals = list(map(int, cur_tm_vals))
                
                # make a frame of subtitle
                srt_start_time = get_srt_time(last_tm_vals)
                srt_end_time = get_srt_time(cur_tm_vals)
                
                str_frame = f'{frame_no}\n{srt_start_time} --> {srt_end_time}\n{content.rstrip()}\n\n'
                fsrt.write(str_frame)
                
                content = ''
                frame_no = frame_no + 1
                print(f'Generated subtitle for {frame_no} frame...', end='', flush=True)
                print('\r', end='') # use '\r' to go back
                
            # get minute : second            
            last_tm_vals = line.rstrip().split(':')
            last_tm_vals = list(map(int, last_tm_vals))
            last_tm_lno = lno
            #print(f'{last_tm_lno} -- ({line.rstrip()})')
            
            #if frame_no > 3:
            #    break
            
        else:
            if last_tm_lno != 0:
                content = content + line
        lno = lno + 1
    else:
        # No more lines to be read from file
        pass
    
    print(f'OK! Generated subtitle for {frame_no} frame!')
    fsrt.close()
    # sys.stdout.write(str(result))