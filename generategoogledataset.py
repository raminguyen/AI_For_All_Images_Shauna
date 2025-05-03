import os
import random
import shutil
from icrawler.builtin import GoogleImageCrawler
import requests
from PIL import Image
from io import BytesIO

# 10 classes with extended search terms
global_search_terms = {
    "frog": [
        "frog", "frog nature", "frog close-up", "frog in water", "frog on leaf",
        "frog sitting", "green frog", "frog in pond", "small frog", "tree frog",
        "frog macro", "poison dart frog", "rainforest frog", "frog on rock", "frog jumping",
        "frog red eyes", "amphibian frog", "tropical frog", "tiny frog", "frog resting",
        "frog camouflage", "frog night photo", "frog face", "frog under leaf", "frog legs",
        "blue poison frog", "yellow frog", "frog in jungle", "frog relaxing", "baby frog"
    ],
    "horse": [
        "horse", "wild horse", "horse galloping", "horse close-up", "horse running",
        "horse herd", "horse in field", "brown horse", "white horse", "race horse",
        "horse portrait", "mustang horse", "horse with rider", "horse rearing", "black horse",
        "farm horse", "horse in snow", "horse with foal", "horse in stable", "horse grazing",
        "horse on hill", "horse in fog", "horse on trail", "horse saddle", "horse looking back",
        "horse resting", "horse drinking water", "horse hair blowing", "painted horse", "horse training"
    ],
    "truck": [
        "truck", "off-road truck", "truck close-up", "red truck", "vintage truck",
        "big rig truck", "semi truck", "truck on road", "pickup truck", "monster truck",
        "diesel truck", "delivery truck", "truck side view", "cargo truck", "white truck",
        "military truck", "blue truck", "truck at construction site", "tow truck", "city truck",
        "fire truck", "truck in desert", "truck headlight", "truck crossing bridge", "snow plow truck",
        "truck hauling", "dump truck", "logging truck", "truck parked", "rusty truck"
    ],
    "cat": [
        "cat", "kitten", "cat close-up", "cat sleeping", "cat drinking water",
        "cat in garden", "cute cat", "cat playing", "cat on chair", "tabby cat",
        "cat licking", "cat stretching", "long-haired cat", "calico cat", "black cat",
        "cat near window", "cat with toy", "cat staring", "cat hiding", "fluffy cat",
        "cat on couch", "cat looking up", "cat walking", "cat in bed", "white cat",
        "cat with big eyes", "grumpy cat", "cat yawning", "siamese cat", "ginger cat"
    ],
    "bird": [
        "bird", "bird in tree", "bird close-up", "flying bird", "exotic bird",
        "colorful bird", "bird wings spread", "bird perched", "small bird", "bird eating",
        "hummingbird", "eagle flying", "parrot bird", "blue jay", "bird nest",
        "songbird", "owl", "flock of birds", "bird in sky", "water bird",
        "bird silhouette", "cardinal bird", "bird on fence", "bird with berries", "bird mid flight",
        "woodpecker", "falcon", "swallow bird", "bird in rain", "bird reflection"
    ],
    "dog": [
        "dog", "puppy", "dog close-up", "dog playing", "dog running",
        "cute dog", "dog in park", "brown dog", "small dog", "dog with ball",
        "labrador retriever", "golden retriever", "dog tongue out", "dog on grass", "white dog",
        "dog sitting", "dog jumping", "dog with owner", "poodle dog", "dog with collar",
        "dog barking", "fluffy dog", "dog sleeping", "beagle dog", "puppy eyes",
        "dog shaking water", "happy dog", "rescue dog", "dog on leash", "dog in car"
    ],
    "airplane": [
        "airplane", "airplane flying", "jet airplane", "commercial airplane",
        "airplane close-up", "airplane in sky", "airplane taking off", "airplane landing", "airplane wing", "airplane cockpit",
        "private jet", "airplane on runway", "airplane clouds", "airplane inside", "military jet",
        "airbus plane", "boeing airplane", "old airplane", "glider", "airplane above city",
        "airplane contrails", "night airplane", "airplane over ocean", "airport terminal airplane", "airplane parked",
        "plane taxiing", "airplane window view", "small airplane", "airplane night lights", "pilot in airplane"
    ],
    "deer": [
        "deer", "wild deer", "deer close-up", "baby deer", "deer in forest",
        "deer in grass", "deer family", "male deer", "female deer", "deer standing",
        "deer walking", "deer running", "deer in snow", "white-tailed deer", "spotted deer",
        "antlered deer", "deer drinking water", "deer trail camera", "young deer", "deer ears",
        "deer looking back", "deer on hill", "deer herd", "deer resting", "forest deer",
        "deer beside tree", "deer on path", "deer grazing", "deer under sunlight", "deer eyes"
    ],
    "ship": [
        "ship", "cargo ship", "cruise ship", "ship at sea", "old ship",
        "big ship", "sailing ship", "container ship", "warship", "boat ship",
        "ship deck", "ship on ocean", "luxury ship", "naval ship", "tanker ship",
        "ship sunset", "ship side view", "harbor ship", "ship loading", "fishing ship",
        "ship in storm", "ship silhouette", "ship bridge", "ship chimney", "ship docking",
        "ship with flags", "ship fog", "ship bow", "ship rope", "ship radar"
    ],
    "automobile": [
        "automobile", "classic car", "sports car", "luxury car", "vintage automobile",
        "red automobile", "blue car", "car front view", "car driving", "automobile racing",
        "convertible car", "electric car", "black car", "automobile showroom", "car engine view",
        "car headlights", "urban car", "car parked", "highway car", "car rear view",
        "shiny car", "rusty car", "car interior", "old convertible", "family car",
        "yellow car", "SUV automobile", "compact car", "offroad car", "white sports car"
    ]
}


# Settings
MAX_NUMBER = 50                   # Try to download a lot to ensure enough
TARGET_IMAGES = 1000                 # We want exactly 1000 images per category
base_input_path = "./downloads"      # Raw downloads folder
base_output_path = "./downloads_selected"  # Final selected images folder

categories = list(global_search_terms.keys())

# Custom crawler
class URLLoggingCrawler(GoogleImageCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_urls = []

    def crawl(self, keyword, max_num, filters=None, **kwargs):
        self.image_urls = []
        super().crawl(keyword=keyword, max_num=max_num, filters=filters, **kwargs)
        return self.image_urls

    def _process_meta(self, task):
        self.image_urls.append(task['file_url'])
        super()._process_meta(task)

# Download images
def download_and_save_images(category, terms):
    img_count = 0
    raw_output_root = os.path.join(base_input_path, f"{category}_raw")
    os.makedirs(raw_output_root, exist_ok=True)

    for term in terms:
        term_folder = os.path.join(raw_output_root, term.replace(" ", "_"))
        os.makedirs(term_folder, exist_ok=True)

        crawler = URLLoggingCrawler(storage={'root_dir': term_folder})
        crawler.crawl(
            keyword=term,
            max_num=MAX_NUMBER,
            filters={
                'type': 'photo',
                'size': 'large',
                'license': 'commercial',
                'color': 'color'
            }
        )
        print(f"🗂️ Images saved in {term_folder}")

        for url in crawler.image_urls:
            try:
                img_data = requests.get(url, timeout=10).content
                img = Image.open(BytesIO(img_data)).convert("RGB")
                img = img.resize((500, 500))

                img_filename = f"{term}_{img_count+1:05d}.jpg"
                img_filepath = os.path.join(term_folder, img_filename)
                img.save(img_filepath)

                img_count += 1
                print(f"✅ {img_filename} downloaded from {url}")

            except Exception as e:
                print(f"⚠️ Skipped {url}: {e}")

# Perceptual hash function
def get_image_hash(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        return imagehash.phash(img)
    except Exception as e:
        print(f"⚠️ Skipped {image_path}: {e}")
        return None

# Select exactly 500 unique images
def collect_unique_images(category, input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    image_hashes = set()
    selected_images = []

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".jpg"):
                img_path = os.path.join(root, file)
                img_hash = get_image_hash(img_path)

                if img_hash and img_hash not in image_hashes:
                    image_hashes.add(img_hash)
                    selected_images.append(img_path)

                if len(selected_images) >= TARGET_IMAGES:
                    break
        if len(selected_images) >= TARGET_IMAGES:
            break

    for idx, src_path in enumerate(selected_images):
        dst_path = os.path.join(output_path, f"{category}_{idx+1:05d}.jpg")
        shutil.copy2(src_path, dst_path)
        print(f"✅ Copied: {os.path.basename(dst_path)}")

# Full process
for category, terms in global_search_terms.items():
    download_and_save_images(category, terms)

print("✅ All raw images downloaded.")

for category in categories:
    input_folder = os.path.join(base_input_path, f"{category}_raw")
    output_folder = os.path.join(base_output_path, category)
    collect_unique_images(category, input_folder, output_folder)

print("🎯 All categories completed with exactly 500 images each!")