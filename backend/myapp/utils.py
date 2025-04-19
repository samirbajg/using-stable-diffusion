import os
import torch
import uuid
import gc
from django.conf import settings
from .load_model import load_model


def prepare_prompt(room_type):
    """Prepare the prompt for better room generation"""
    base_prompt = (
        f"a professional interior design of a {room_type} high quality, photorealistic"
    )
    negative_prompt = (
        "low quality, blurry, bad architecture, poor lighting, bad proportions"
    )
    return base_prompt, negative_prompt


def generate_designs(room_type):
    try:
        # Clear CUDA cache before starting
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()

        # Create necessary directories
        save_dir = os.path.join(settings.MEDIA_ROOT, "generated_images")
        os.makedirs(save_dir, exist_ok=True)

        # Load model and generate image
        pipe = load_model()
        prompt, negative_prompt = prepare_prompt(room_type)

        # Generate with optimized settings
        with torch.no_grad(), torch.autocast(
            "cuda" if torch.cuda.is_available() else "cpu"
        ):
            generated_image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=5,  # Reduced from 30 cause of limimtation of gpu
                guidance_scale=7.0,  # reduced
                height=512,
                width=512,
            ).images[0]

        # Save the image
        new_img_filename = f"{room_type}_{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(save_dir, new_img_filename)
        generated_image.save(image_path)

        return f"/media/generated_images/{new_img_filename}"

    except Exception as e:
        raise Exception(f"Failed to generate design: {str(e)}")
