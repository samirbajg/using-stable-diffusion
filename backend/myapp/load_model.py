import os
import torch
from diffusers import StableDiffusionPipeline
from peft import PeftModel, LoraConfig


def load_model():
    try:
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    #if device have enough gpu
        device = "cpu"
        model_id = "CompVis/stable-diffusion-v1-4"

        # Enable memory efficient attention
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            use_safetensors=True,
            variant=None,
            low_cpu_mem_usage=True,
        )

        pipe = pipe.to(device)

        # Load LoRA weights with memory optimization
        lora_weights_path = os.path.join(os.path.dirname(__file__), "fine_tuned_model")

        if os.path.exists(lora_weights_path):
            config_path = os.path.join(lora_weights_path, "adapter_config.json")
            weights_path = os.path.join(lora_weights_path, "adapter_model.safetensors")

            if os.path.exists(config_path) and os.path.exists(weights_path):
                config = LoraConfig.from_pretrained(lora_weights_path)
                # Load LoRA weights with CPU offloading
                pipe.unet = PeftModel.from_pretrained(
                    pipe.unet,
                    lora_weights_path,
                    config=config,
                    torch_dtype=(torch.float32),
                )

        return pipe

    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")
