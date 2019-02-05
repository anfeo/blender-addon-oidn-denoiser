# blender-addon-oidn-denoiser
Addon to connect the Intel Open Image Denoise to Blender 2.79. You can render ad denoise the image in one click

# How to install

- downlad the last .py file
- download and install imagemagick (if you are in Ubuntu you have it by default)
https://imagemagick.org/script/download.php
- download the oidn for your OS and extract to a location of your choice (like home in Ubuntu)
https://openimagedenoise.github.io/downloads.html
- install the addon from the user preference window
- set the oidn directory path from the addon user preferences (master directory like oidn-0.8.1.x86_64.linux if you use linux)
- active the addon and go to the 3D view in tools shelf search the Intel Denoise tab.
- you can use it only on saved file (it work with relative path)
# Option:
- Image Name: set the image name without extension
- Output: set the output directory
- Extension and other Blender image settings
- press Intel Denoise to start the render
- Look at the terminal (console) for progress and error
