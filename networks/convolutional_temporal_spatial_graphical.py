import torch
import torch.nn as nn
from networks.

class ConvTemporalSpatialGraphical(nn.module):
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride = 1,
        dropout = 0,
        residual = True
    ):
        super().__init__()

        assert len(kernel_size) == 2
        assert kernel_size[0] % 2 == 1
        padding = ((kernel_size[0] - 1) // 2, 0)

