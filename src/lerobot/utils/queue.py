#!/usr/bin/env python

# Copyright 2025 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import platform
from contextlib import suppress
from queue import Empty
from typing import Any

from torch.multiprocessing import Queue


def get_last_item_from_queue(queue: Queue, block=True, timeout: float = 0.1) -> Any:
    if block:
        try:
            item = queue.get(timeout=timeout)
        except Empty:
            return None
    else:
        item = None

    # Drain queue and keep only the most recent parameters
    if platform.system() == "Darwin":
        # On Mac, avoid using `qsize` due to unreliable implementation.
        # There is a comment on `qsize` code in the Python source:
        # Raises NotImplementedError on Mac OSX because of broken sem_getvalue()
        try:
            while True:
                item = queue.get_nowait()
        except Empty:
            pass

        return item

    # Details about using qsize in https://github.com/huggingface/lerobot/issues/1523
    while queue.qsize() > 0:
        with suppress(Empty):
            item = queue.get_nowait()

    return item
