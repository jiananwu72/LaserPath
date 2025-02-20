import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('LaserPath/RawImages/Raw.jpg')
hls_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

# Split & normalize channels
H, L, S = cv2.split(hls_image)
H_norm = cv2.normalize(H, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
L_norm = cv2.normalize(L, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
S_norm = cv2.normalize(S, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

np.savetxt("LaserPath/HLSmap/H_map.txt", H, delimiter=",", fmt='%d')

# Save each channel separately
cv2.imwrite("LaserPath/HLSmap/H_map.png", H_norm)  # Save Hue map
cv2.imwrite("LaserPath/HLSmap/L_map.png", L_norm)  # Save Lightness map
cv2.imwrite("LaserPath/HLSmap/S_map.png", S_norm)  # Save Saturation map

# Display results and save plots
fig, ax = plt.subplots(1, 4, figsize=(15, 5))

titles = ["Original Image", "Hue Channel", "Lightness Channel", "Saturation Channel"]
images = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB), H_norm, L_norm, S_norm]
cmaps = [None, "hsv", "gray", "gray"]

for i in range(4):
    ax[i].imshow(images[i], cmap=cmaps[i])
    ax[i].set_title(titles[i])
    ax[i].axis("off")

# Save the combined figure
plt.savefig("LaserPath/HLSmap/FEmap.png", bbox_inches="tight", dpi=300)
