from __future__ import annotations

import logging
from abc import ABC, abstractproperty
from collections.abc import Iterable
from pathlib import Path

from dynamicprompts.sampling_context import SamplingContext
from dynamicprompts.wildcards import WildcardManager

# Import our custom wildcard manager
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from ordered_wildcard_manager import OrderedWildcardManager
    print("SUCCESS: OrderedWildcardManager loaded - wildcards will be in file order")
except ImportError as e:
    # Fallback to original if import fails
    OrderedWildcardManager = WildcardManager
    print(f"ERROR: Could not load OrderedWildcardManager: {e}")
    print("FALLBACK: Using default WildcardManager (alphabetical order)")

logger = logging.getLogger(__name__)


class DPAbstractSamplerNode(ABC):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "seed": ("INT", {"default": 0, "display": "number"}),
                "autorefresh": (["Yes", "No"], {"default": "No"}),
                "reset": ("BOOLEAN", {"default": False, "tooltip": "Reset to first item in sequence"}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, text: str, seed: int, autorefresh: str, reset: bool):
        # Force re-evaluation of the node
        return float("NaN")

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("prompt", "current_index")
    FUNCTION = "get_prompt"
    CATEGORY = "Dynamic Prompts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wildcards_folder = self._find_wildcards_folder()
        self._wildcard_manager = OrderedWildcardManager(path=wildcards_folder)
        # Disable sorting to preserve file order
        self._wildcard_manager.sort_wildcards = False
        print("OrderedWildcardManager: sort_wildcards disabled - wildcards will be in file order")
        self._current_prompt = None
        self._current_index = 0

    def _find_wildcards_folder(self) -> Path | None:
        """
        Find the wildcards folder.
        First look in the comfy_dynamicprompts folder, then in the custom_nodes folder, then in the Comfui base folder.
        """
        from folder_paths import base_path, folder_names_and_paths

        wildcard_path = Path(base_path) / "wildcards"

        if wildcard_path.exists():
            return wildcard_path

        extension_path = (
            Path(folder_names_and_paths["custom_nodes"][0][0])
            / "comfyui-dynamicprompts"
        )
        wildcard_path = extension_path / "wildcards"
        wildcard_path.mkdir(parents=True, exist_ok=True)

        return wildcard_path

    def _get_next_prompt(self, prompts: Iterable[str], current_prompt: str) -> str:
        """
        Get the next prompt from the prompts generator.
        """
        try:
            return next(prompts)
        except (StopIteration, RuntimeError):
            self._prompts = self.context.sample_prompts(current_prompt)
            try:
                return next(self._prompts)
            except StopIteration:
                logger.exception("No more prompts to generate!")
                return ""

    def has_prompt_changed(self, text: str) -> bool:
        """
        Check if the prompt has changed.
        """
        return self._current_prompt != text

    def get_prompt(self, text: str, seed: int, autorefresh: str, reset: bool = False) -> tuple[str, int]:
        """
        Main entrypoint for this node.
        Using the sampling context, generate a new prompt.
        """

        if seed > 0:
            self.context.rand.seed(seed)

        if text.strip() == "":
            return ("", 0)

        # Handle reset functionality
        if reset:
            self._current_index = 0
            self._current_prompt = None
            self._prompts = None
            print("Reset to first item in sequence")

        if self.has_prompt_changed(text) or reset:
            self._current_prompt = text
            self._prompts = self.context.sample_prompts(self._current_prompt)
            if reset:
                self._current_index = 0

        if self._prompts is None:
            logger.exception("Something went wrong. Prompts is None!")
            return ("", 0)

        if self._current_prompt is None:
            logger.exception("Something went wrong. Current prompt is None!")
            return ("", 0)

        new_prompt = self._get_next_prompt(self._prompts, self._current_prompt)
        
        # Increment index for next time
        self._current_index += 1
        
        print(f"New prompt: {new_prompt} (Index: {self._current_index})")

        return (str(new_prompt), self._current_index)

    @abstractproperty
    def context(self) -> SamplingContext:
        ...
