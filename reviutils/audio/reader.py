# -*- coding: utf-8 -*-
# Author: Vi
# Created on: 2024-03-15 09:41:27
# Description: 用于读取音频文件

from functools import singledispatch

try:
    import torchaudio
    import numpy as np
    from pydub import AudioSegment
except ImportError:
    # 提示安装 reviutils[audio]
    raise ImportError("Please install reviutils[audio] to use this module: pip install reviutils[audio]")

def get_audio_by_audio_segment(file):
    '''使用pydub的AudioSegment读取音频'''
    audio_seg = AudioSegment.from_file(file=file)
    audio = audio_seg.get_array_of_samples()
    audio = np.array(audio, dtype=np.float32)
    sr = audio_seg.frame_rate
    return audio, sr
    
@singledispatch
def load_audio_from_file(audio_file):
    raise NotImplementedError("Unsupported audio file format")

@load_audio_from_file.register(str)
def load_audio_from_filepath(audio_file):
    '''从音频文件中读取音频'''
    if '.wav' in audio_file.lower():
        audio, sr = torchaudio.load(audio_file)
    else:
        audio, sr = get_audio_by_audio_segment(file=audio_file)
    return audio, sr

from starlette.datastructures import UploadFile
@load_audio_from_file.register(UploadFile)
def load_audio_from_temporary_file(audio_file):
    '''从（网络）临时文件中读取音频'''
    if '.wav' in audio_file.filename.lower():
        audio, sr = torchaudio.load(audio_file.file)
    else:
        audio, sr = get_audio_by_audio_segment(file=audio_file.file)
    return audio, sr