# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-03-15 09:41:27
# Description: 用于读取音频文件

import torchaudio
import numpy as np
from pydub import AudioSegment

def get_audio_by_audio_segment(file):
    '''使用pydub的AudioSegment读取音频'''
    audio_seg = AudioSegment.from_file(file=file)
    audio = audio_seg.get_array_of_samples()
    audio = np.array(audio, dtype=np.float32)
    sr = audio_seg.frame_rate
    return audio, sr
    
def load_audio_from_file(audio_path):
    '''从音频文件中读取音频'''
    if '.wav' in audio_path.lower():
        audio, sr = torchaudio.load(audio_path)
    else:
        audio, sr = get_audio_by_audio_segment(file=audio_path)
    return audio, sr

def load_audio_from_temporary_file(temp_file):
    '''从（网络）临时文件中读取音频'''
    if '.wav' in temp_file.filename.lower():
        audio, sr = torchaudio.load(temp_file.file)
    else:
        audio, sr = get_audio_by_audio_segment(file=temp_file.file)
    return audio, sr