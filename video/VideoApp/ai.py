import torch
import torch.nn as nn

import torch
import os
from pytorchvideo.data.encoded_video import EncodedVideo
from torchvision.transforms import Compose, Lambda, Resize
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
from pytorchvideo.transforms import (
    ApplyTransformToKey,
    ShortSideScale,
    UniformTemporalSubsample
)

import numpy as np
import pathlib

class PackPathway(torch.nn.Module):
    """
    Transform for converting video frames as a list of tensors. 
    """
    def __init__(self):
        super().__init__()
        
    def forward(self, frames: torch.Tensor):
        fast_pathway = frames
        # Perform temporal sampling from the fast pathway.
        slow_pathway = torch.index_select(
            frames,
            1,
            torch.linspace(
                0, frames.shape[1] - 1, frames.shape[1] // 4
            ).long(),
        )
        frame_list = [slow_pathway, fast_pathway]
        return frame_list


class VideoClassificationModel(nn.Module):

    def __init__(self, cfg):
        super().__init__()

        self.cfg = cfg
        self.num_classes = cfg['num_classes']
        self.path_torchvideo_model = cfg['path_torchvideo_model']
        self.name_torchvideo_model = cfg['name_torchvideo_model']
        self.n_nodes = cfg["n_nodes"]
        self.freeze_layers = cfg.get("freeze_layers", 1.0) > 0.0
        self.dropout = cfg["dropout"]
        self.base_model = torch.hub.load(self.path_torchvideo_model, self.name_torchvideo_model, pretrained=True)

        if self.freeze_layers:
            print("Freeze layers of pretrained model")
            for name, param in self.base_model.named_parameters():
                param.requires_grad = False

        
        self.base_model.blocks[6].proj = nn.Sequential(nn.Linear(2304, self.n_nodes),
                                                        nn.ReLU(),
                                                        nn.Dropout(self.dropout),
                                                        nn.Linear(self.n_nodes, self.num_classes))

        for name, param in self.base_model.named_parameters():
            print("Layer name: {} - requires_grad: {}".format(name, param.requires_grad))
            
    def forward(self, x):
        x = self.base_model(x)
        return x

def getlist(path: str, cfg):
# Митя, я нихера не понял, прости меня, если что-то пошло не так
# я в душе не знаю, что в Питоне по асинхронности, но пиши я на ASP.NET, точно не делал вызывал бы это в синхронном запросе

    video_path = path

    labelclass={0: 'golf',
 1: 'handstand',
 2: 'swing_baseball',
 3: 'throw',
 4: 'push',
 5: 'jump',
 6: 'pushup',
 7: 'hit',
 8: 'draw_sword',
 9: 'climb',
 10: 'cartwheel',
 11: 'dive',
 12: 'dribble',
 13: 'sword_exercise',
 14: 'situp',
 15: 'pick',
 16: 'pullup',
 17: 'clap',
 18: 'shoot_ball',
 19: 'flic_flac',
 20: 'sit',
 21: 'pour',
 22: 'fencing',
 23: 'catch'}
    
    class2label = dict((v,k) for k,v in labelclass.items())
    labelclass.update(class2label)

    if not os.path.exists(video_path):
        print("The video '{}' does not exist ".format(video_path))

    side_size = 256
    mean = [0.45, 0.45, 0.45]
    std = [0.225, 0.225, 0.225]
    crop_size = 256
    num_frames = cfg["num_frames"]

    transform = ApplyTransformToKey(
            key="video",
            transform=Compose(
                [
                        UniformTemporalSubsample(num_frames),
                        Lambda(lambda x: x/255.0),
                        NormalizeVideo(mean, std),
                        ShortSideScale(size=side_size),
                        CenterCropVideo(crop_size=(crop_size, crop_size)),
                        PackPathway()
                    ]
                ),
        )

    video = EncodedVideo.from_path(video_path)
    start_time = 0
    end_sec = (cfg["num_frames"] * cfg["sampling_rate"])/cfg["frames_per_second"]
    video_data = video.get_clip(start_sec=start_time, end_sec=end_sec)
    video_data = transform(video_data)
    inputs = video_data["video"]

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = VideoClassificationModel(cfg).to(device)

    model.load_state_dict(torch.load("checkpoint_1.pth", map_location=device)["model"])

    post_act = torch.nn.Softmax(dim=1)
    model.eval()
    outputs = model([i.to(device, non_blocking=True) for i in inputs])
    labels = labels.to(device)
    preds = post_act(outputs)
    _, pred_classes = torch.max(preds, 1)



    return pred_classes
