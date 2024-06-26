from .diffbir.sampler import DiffBIR_sample, DiffBIR_sample_advanced
from .diffbir.load import Stage2_load, Stage1_load, Simple_load

NODE_CLASS_MAPPINGS = {
    "DiffBIR_sample": DiffBIR_sample,
    "DiffBIR_sample_advanced": DiffBIR_sample_advanced,
    "Stage1_load": Stage1_load,
    "Stage2_load": Stage2_load,
    "Simple_load": Simple_load,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "DiffBIR_sample": "DiffBIR Sampler",
    "DiffBIR_sample_advanced": "DiffBIR Sampler (Advanced)",
    "Stage1_load": "DiffBIR stage1 loader",
    "Stage2_load": "DiffBIR stage2 loader",
    "Simple_load": "DiffBIR simple load",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]