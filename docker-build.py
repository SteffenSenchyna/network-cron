import os

# Define the image name and tag
image_name = 'ssenchyna/network-cron'
image_tag = '2.0'
# # Build the Docker image\
# os.system(f'docker build -t {image_name}:{image_tag} .')
# # # Log in to Docker Hub
# os.system('docker login')
# # # Push the Docker image to Docker Hub
# os.system(f'docker push {image_name}:{image_tag}')
os.system(
    f'docker buildx build --platform linux/amd64,linux/arm64 -t {image_name} --push .')
# # Log in to Docker Hub
