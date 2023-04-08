import os

# Define the image name and tag
image_name = 'ssenchyna/network-cron'
image_tag = '2.0'

os.system(
    f'docker buildx build --platform linux/amd64,linux/arm64 -t {image_name} --push .')
