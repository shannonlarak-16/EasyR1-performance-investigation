# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
"""
Implement base data transfer protocol between any two functions, modules.
We can subclass Protocol to define more detailed batch info with specific keys.

NOTE: This file was modified by commit 098931530606d22f867fd121b1dcb3225a43661f 
([misc] fix data proto (#458)) - under investigation for performance regression.
"""

import copy
import io
import pickle
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Union

import numpy as np
import ray
import torch
from numpy.typing import NDArray
from tensordict import TensorDict
from torch.distributed import ProcessGroup
from torch.utils.data import DataLoader

# Full file content shadows hiyouga/EasyR1 verl/protocol.py
# Key section modified in commit 098931530606d22f867fd121b1dcb3225a43661f:
#   def to(self, device: torch.device, non_blocking: bool = False) -> 'DataProto':
#     # CHANGED from `non_blocking: bool = True` to `non_blocking: bool = False`
#     # This is suspected as one source of performance regression

__all__ = ["DataProto", "union_tensor_dict"]
