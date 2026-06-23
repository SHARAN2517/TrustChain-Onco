"""ResNet18 baseline classifier for PathMNIST-224 (9-class histopathology)."""

import torch
import torch.nn as nn
from torchvision import models


def build_resnet18(num_classes: int = 9, pretrained: bool = True) -> nn.Module:
    weights = models.ResNet18_Weights.DEFAULT if pretrained else None
    model = models.resnet18(weights=weights)
    model.fc = nn.Linear(model.fc.in_features, num_cla