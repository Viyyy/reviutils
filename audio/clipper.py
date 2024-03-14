import os
import sys
# 添加当前路径到环境变量
if not sys.path.__contains__(os.getcwd()):
    sys.path.append(os.getcwd())

import numpy as np
import librosa
import soundfile
from torch import Tensor
from numpy import ndarray
# 裁剪音频
def clip_signal(signal:Tensor|ndarray,sr,start_time,end_time):
    samples = signal.shape[1]
    start_postion = int(sr * start_time)
    end_position = int(sr * end_time)
    duration = samples * 1.0 /(sr*1.0)
    
    if  start_postion>end_position or start_postion>samples or end_position>samples or start_postion<0:
        raise ValueError(f'起始时间需小于结束时间，且结束时间需要小于音频持续时间{duration}s')
    
    result = signal[:,start_postion:end_position]
    if not  isinstance(result, Tensor):
        result = Tensor(result)
    return result

# 裁剪音频
def _clip_signal_by_samples(signal:Tensor|ndarray,start_postion,end_position):
    samples = signal.shape[0]
    
    if  start_postion>end_position or start_postion>samples or end_position>samples or start_postion<0:
        raise ValueError(f'起始位置需小于结束位置，且结束位置需要小于音频采样点数量：{samples}')
    
    signal=signal[start_postion:end_position]
    return signal

# 随机裁剪/填充音频
def rand_clip(signal:Tensor|ndarray,sr,target_len,need_time_returned:bool=False):
    samples =  len(signal)
    target_samples = sr * target_len
    # 随机裁剪
    if samples > target_samples:
        random_start = np.random.randint(0,samples-target_samples)
        if need_time_returned:
            start_time = random_start/sr
            end_time = start_time+target_len
            return _clip_signal_by_samples(signal,random_start,random_start+target_samples),start_time,end_time
        else:
            return _clip_signal_by_samples(signal,random_start,random_start+target_samples)
    # 随机填充
    if samples < target_samples:
        target_samples = target_len * sr
        new_signal = np.zeros(target_samples)
        random_start = np.random.randint(0,target_samples-samples)
        new_signal[random_start:random_start+samples-1] = signal[0:samples-1]
        if need_time_returned:
            start_time = random_start/sr
            end_time = start_time + samples/sr
            return new_signal,start_time,end_time
        else:
            return new_signal
    if samples == target_samples:
        return signal
        
# 裁剪音频并保存
def rand_clip_file(audio_path,target_len,save_path):
    signal,sr = librosa.load(audio_path)
    signal = rand_clip(signal=signal,sr=sr,target_len=target_len)
    try:
        soundfile.write(file=save_path,data=signal,samplerate=sr)
        return save_path
    except Exception as e:
        print(audio_path,e)