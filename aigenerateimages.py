 import os
from diffusers import DiffusionPipeline
from PIL import Image


# Load the model
model_id = "stabilityai/stable-diffusion-3-medium-diffusers"
pipe = DiffusionPipeline.from_pretrained(model_id, cache_dir="/hpcstor6/scratch01/h/huuthanhvy.nguyen001/diffusion")
pipe = pipe.to("cuda")

# Define 10 categories with mult
# iple prompts each
global_search_terms = {
    "airplane": [
        "a passenger airplane flying above the clouds during sunset",
        "a futuristic jet soaring through a clear blue sky",
        "an old vintage biplane flying over a green field",
        "a commercial airplane landing at a busy airport",
        "a fighter jet performing aerial maneuvers with smoke trails",
        "an airplane parked at an airport terminal",
        "a private jet flying over mountains",
        "a cartoon airplane flying through space",
        "a glider soaring over a canyon",
        "an airplane viewed from cockpit window"
    ],
    "automobile": [
        "a sleek sports car speeding down a coastal highway",
        "an old classic car parked beside a countryside road",
        "an electric car charging at a futuristic station",
        "a rugged SUV driving through a muddy forest trail",
        "a city taxi navigating through heavy downtown traffic",
        "a racing car drifting around a track",
        "a futuristic concept car on display",
        "a car stuck in a snowstorm",
        "a luxury limousine arriving at a red carpet event",
        "an abandoned rusty car in a desert"
    ],
    "ship": [
        "a grand cruise ship sailing across the ocean at sunset",
        "a pirate ship battling waves during a storm",
        "a cargo ship docked at an industrial port",
        "a fishing boat returning to harbor in early morning fog",
        "a historic sailing ship with tall masts and full sails",
        "a futuristic underwater exploration vessel",
        "a navy ship sailing through rough waters",
        "a shipwreck resting on the ocean floor",
        "a steamboat cruising down a river",
        "an icebreaker ship cutting through Arctic ice"
    ],
    "dog": [
        "a golden retriever playing fetch in a sunny park",
        "a small puppy sleeping in a cozy blanket",
        "a husky running through a snow-covered forest",
        "a group of playful dogs at a beach during sunset",
        "a dog wearing a superhero costume posing proudly",
        "a police dog training in a field",
        "a dog herding sheep on a farm",
        "a tiny dog in a teacup",
        "a dog hiking in the mountains",
        "a dog surfing on a small wave"
    ],
    "deer": [
        "a majestic deer standing in a misty forest at dawn",
        "a young fawn grazing in a meadow full of wildflowers",
        "a deer jumping gracefully over a fallen tree",
        "a deer drinking water from a calm forest stream",
        "a herd of deer wandering through a snowy landscape",
        "a deer standing on a rocky cliff",
        "a group of deer running across a meadow",
        "a lone deer silhouetted against the sunset",
        "a deer with antlers covered in velvet",
        "a cartoon deer smiling in a magical forest"
    ],
    "frog": [
        "a colorful tree frog on a leaf",
        "a frog sitting on a lily pad in a pond",
        "a tiny frog peeking out from under a rock",
        "a frog catching an insect mid-jump",
        "a frog resting on a mossy branch",
        "a close-up of a frog's eyes",
        "a frog blending into a rainforest background",
        "a group of frogs croaking at night",
        "a frog leaping across a river",
        "a cartoon frog wearing a crown"
    ],
    "horse": [
        "a wild horse running across a desert",
        "a black stallion rearing up on hind legs",
        "a horse grazing in a meadow at sunset",
        "a horse galloping through snow",
        "a group of horses drinking from a river",
        "a cowboy riding a horse on a ranch",
        "a horse pulling an old-fashioned carriage",
        "a horse jumping over a hurdle",
        "a pony being groomed at a stable",
        "a magical unicorn in a fantasy forest"
    ],
    "truck": [
        "a monster truck jumping over a ramp",
        "a vintage pickup truck parked by a barn",
        "a food truck serving customers in a city",
        "a big rig driving down a highway at night",
        "an off-road truck splashing through mud",
        "a construction truck working at a site",
        "an armored truck driving through desert",
        "a garbage truck collecting waste",
        "a military supply truck crossing a bridge",
        "a futuristic delivery truck in a smart city"
    ],
    "cat": [
        "a fluffy kitten playing with a ball of yarn",
        "a cat napping in a sunny window",
        "a cat climbing a tree",
        "a black cat sitting on a fence during Halloween",
        "a cat stretching after waking up",
        "a cat hiding inside a cardboard box",
        "a cat wearing a bow tie",
        "a group of cats eating together",
        "a cat lounging on a cozy chair",
        "a cartoon cat flying with balloons"
    ],
    "bird": [
        "a colorful parrot perched on a branch",
        "a flock of birds flying at sunrise",
        "a bird building a nest",
        "a hummingbird drinking nectar from a flower",
        "an owl perched on a tree at night",
        "a seagull flying over the ocean",
        "a robin hopping on a snowy ground",
        "a falcon diving through the air",
        "a bird singing on a spring morning",
        "a cartoon bird delivering a letter"
    ]
}

# Output folder for generated images
base_output_path = "./ai_generated_images_8000_diffusers"
os.makedirs(base_output_path, exist_ok=True)

# Function to generate one image
def generate_image(prompt):
    output = pipe(
        prompt=prompt,
        num_inference_steps=28,
        guidance_scale=7,
        height=512,
        width=512,
    )
    return output.images[0]

# Function to generate exactly 500 images for each category
def generate_images_for_category(category, num_images=500):
    term_folder = os.path.join(base_output_path, category)
    os.makedirs(term_folder, exist_ok=True)

    prompts = global_search_terms[category]
    total_prompts = len(prompts)

    generated_images = 0
    while generated_images < num_images:
        prompt = prompts[generated_images % total_prompts]  # Cycle through prompts
        image = generate_image(prompt)

        img_filename = f"{category}_{generated_images+1:05d}.jpg"
        img_filepath = os.path.join(term_folder, img_filename)

        image.save(img_filepath)

        print(f"✅ Generated and saved {img_filename} for {category}")

        generated_images += 1

# Main generation loop
for category in global_search_terms.keys():
    generate_images_for_category(category, num_images=1000)

print("🎯 Image generation completed! 8000 images total across 10 categories.")
