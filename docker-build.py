import os

# Define the image name and tag
image_name = 'network'
image_tag = 'Test'
os.system(f"docker image prune -y")
os.system(
    f'docker build -t {image_name}:{image_tag} .')
os.system(
    f'docker run --rm -it --entrypoint /bin/sh {image_name}:{image_tag}')
