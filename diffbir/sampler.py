import argparse

import torch

def check_device(device: str) -> str:
    if device == "cuda":
        if not torch.cuda.is_available():
            print("CUDA not available because the current PyTorch install was not "
                  "built with CUDA enabled.")
            device = "cpu"
    else:
        if device == "mps":
            if not torch.backends.mps.is_available():
                if not torch.backends.mps.is_built():
                    print("MPS not available because the current PyTorch install was not "
                          "built with MPS enabled.")
                    device = "cpu"
                else:
                    print("MPS not available because the current MacOS version is not 12.3+ "
                          "and/or you do not have an MPS-enabled device on this machine.")
                    device = "cpu"
    print(f"using device {device}")
    return device


class DiffBIR_sample_advanced:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "stage1_model": ("STAGE1",),
            "task": ("TASK", ),
            "cldm": ("CLDM",),
            "diffusion": ("DIFFUSION",),
            "infer_type": ("INFER_TYPE",),
            "image": ("IMAGE",),
            "upscale_ratio": ("FLOAT", {"default": 2, "min": 0.1, "max": 8.0, "step": 0.1}),
            "steps": ("INT", {"default": 20, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "cfg": ("FLOAT", {"default": 4.0, "min": 0, "max": 100, "step": 0.1}),
            "better_start": ("BOOLEAN", {"default": True}),
            "tiled": ("BOOLEAN", {"default": True}),
            "tile_size": ("INT", {"default": 512, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "tile_stride": ("INT", {"default": 256, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "keep_stage1_loaded": ("BOOLEAN", {"default": True}),
            "stage1_tile": ("BOOLEAN", {"default": True}),
            "stage1_tile_size": ("INT", {"default": 512, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "stage1_tile_stride": ("INT", {"default": 256, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "pos_prompt": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            "neg_prompt": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            "seed": ("INT", {"default": 123, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
            "device": (
                    [
                        'cuda',
                        'cpu',
                        'mps',
                    ], {
                        "default": 'cuda'
                    }),

        }, "optional": {

            "guidance": ("BOOLEAN", {"default": False}),
            "g_loss": (
                    [
                        'mse',
                        'w_mse',
                    ], {
                        "default": 'w_mse'
                    }),
            "g_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            "g_start": ("INT", {"default": 1001, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
            "g_stop": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff, "step": 1}),
            "g_space": (
                    [
                        'latent',
                        'rgb',
                    ], {
                        "default": 'latent'
                    }),
            "g_repeat": ("INT", {"default": 1, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "sample"
    CATEGORY = "DiffBIR"
    DESCRIPTION = """"""

    def sample(self, stage1_model, task, cldm, diffusion, infer_type, image, upscale_ratio, steps, cfg, 
               better_start, tiled, tile_size, tile_stride, keep_stage1_loaded, stage1_tile, stage1_tile_size, 
               stage1_tile_stride, pos_prompt, neg_prompt, seed, device, guidance, g_loss, 
               g_scale, g_start, g_stop, g_space, g_repeat):
        from ..utils.sr_inference import BSRInferenceLoop, BFRInferenceLoop, BIDInferenceLoop
        device = check_device(device)
        print(image.shape)

        args = argparse.Namespace(
            task='sr',
            upscale=upscale_ratio,
            version='v2',
            steps=steps,
            better_start=better_start,
            tiled=tiled,
            tile_size=tile_size,
            tile_stride=tile_stride,
            stage1_tile=stage1_tile,
            stage1_tile_size=stage1_tile_size,
            stage1_tile_stride=stage1_tile_stride,
            pos_prompt=pos_prompt,
            neg_prompt=neg_prompt,
            cfg_scale=cfg,
            input=image,
            n_samples=1,
            guidance=guidance,
            g_loss=g_loss,
            g_scale=g_scale,
            g_start=g_start,
            g_stop=g_stop,
            g_space=g_space,
            g_repeat=g_repeat,
            output='',
            seed=seed,
            device=device
        )

        if task == 'bsr':
            pipe = BSRInferenceLoop(args)
        elif task == 'bfr':
            pipe = BFRInferenceLoop(args)
        elif task == 'bid':
            pipe = BIDInferenceLoop(args)
        else:
            raise NotImplementedError(f'task {task} not implemented')
        
        pipe.init_stage1_model(stage1_model, infer_type, keep_stage1_loaded)
        pipe.init_stage2_model(cldm, diffusion, infer_type)
        pipe.init_pipeline()

        image = pipe.run()
        
        return (image,)
    

class DiffBIR_sample:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "stage1_model": ("STAGE1",),
            "cldm": ("CLDM",),
            "diffusion": ("DIFFUSION",),
            "infer_type": ("INFER_TYPE",),
            "image": ("IMAGE",),
            "upscale_ratio": ("FLOAT", {"default": 2, "min": 0.1, "max": 8.0, "step": 0.1}),
            "steps": ("INT", {"default": 20, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "cfg": ("FLOAT", {"default": 4.0, "min": 0, "max": 100, "step": 0.1}),
            "better_start": ("BOOLEAN", {"default": True}),
            "tiled": ("BOOLEAN", {"default": True}),
            "tile_size": ("INT", {"default": 512, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "tile_stride": ("INT", {"default": 256, "min": 1, "max": 0xffffffffffffffff, "step": 1}),
            "pos_prompt": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            "neg_prompt": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            "seed": ("INT", {"default": 123, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
            "device": (
                    [
                        'cuda',
                        'cpu',
                        'mps',
                    ], {
                        "default": 'cuda'
                    }),

            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "sample"
    CATEGORY = "DiffBIR"
    DESCRIPTION = """"""

    def sample(self, stage1_model, cldm, diffusion, infer_type, image, upscale_ratio, steps, cfg, 
               better_start, tiled, tile_size, tile_stride, pos_prompt, neg_prompt, 
               seed, device):
        from ..utils.sr_inference import BSRInferenceLoop
        device = check_device(device)
        keep_stage1_loaded = True
        print(image.shape)

        args = argparse.Namespace(
            task='sr',
            upscale=upscale_ratio,
            version='v2',
            steps=steps,
            better_start=better_start,
            tiled=tiled,
            tile_size=tile_size,
            tile_stride=tile_stride,
            stage1_tile=tiled,
            stage1_tile_size=tile_size,
            stage1_tile_stride=tile_stride,
            pos_prompt=pos_prompt,
            neg_prompt=neg_prompt,
            cfg_scale=cfg,
            input=image,
            n_samples=1,
            guidance=False,
            g_loss="w_mse",
            g_scale=1.00,
            g_start=1001,
            g_stop=-1,
            g_space="latent",
            g_repeat=1,
            output='',
            seed=seed,
            device=device
        )
        
        pipe = BSRInferenceLoop(args)
        pipe.init_stage1_model(stage1_model, infer_type, keep_stage1_loaded)
        pipe.init_stage2_model(cldm, diffusion, infer_type)
        pipe.init_pipeline()

        image = pipe.run()
        
        return (image,)