# annotation_tool
annotation tool for pose recognition

## 请先压缩

```
ffmpeg -i input.mp4 -vf "scale=iw/4:ih/4" output.mp4
```

## 然后用标注工具进行标注

```
python DataprepareVideo.py --input_file output.mp4 --clip_start_min 0 --clip_start_sec 0 --clip_end_min 40 --clip_end_sec 0 --flag play jump smash walk --dur 90
```

## 参数含义

#### --input_file 输入文件的名字，请将输入文件放在与脚本同一目录下。该程序会同时创立以输入文件命名的文件夹存放截取视频和标签文件
#### --clip_start_min --clip_start_sec --clip_end_min --clip_end_sec 整段样本视频的开始和结束时间（分钟/秒）。以上面为例，从output.mp4里面选取了从0分种开始40分钟结束的视频,然后存在本地为output_clip.mp4
#### --flag 需要标注的标签。以上面的代码为例，定义了三种标签，play/jump/smash/walk
#### --dur 每段小视频的帧数。以上面的代码为例，每段小视频90帧

## 操作手册

1. 在终端会显示出操作的方式
![image](http://https://github.com/oilpig/annotation_tool/edit/master/images/operate.jpg)
2. 最终会生成以output命名的标签文件（output.json）和存放截取视频的文件夹output

核心工具包来源于https://github.com/ale152/muvilab

