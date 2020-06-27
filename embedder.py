import numpy as np
import cv2
from key import ChaoticLogisticMap
from matplotlib import pyplot as plt
from PIL import Image

# img = Image.open('cat1.jpg').convert('LA')  # convert it to gray scale while opening.
img_org = cv2.imread('cat1.jpg', 0)
# test area:
# plt.imshow(img)
# plt.show()

edges = cv2.Canny(img_org, 100, 200)

# plt.subplot(121), plt.imshow(img, cmap='gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(edges, cmap='gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()

message = "This is working. And I add some more text to embed more data and see if there will be any change in " \
          "the embedded image. This is cool. and lets repeat the message again: This is working. " \
          "And I add some more text to embed more data and see if there will be any change in " \
          "the embedded image. This is cool. and lets repeat the message again:" + "***"
# convert message to binary:
message = ''.join(format(ord(i), 'b') for i in message)

n = 3  # number of pixels in a block. [3, 4]
x = 1

img_size = img_org.shape[0] * img_org.shape[1]
assert (img_size % n == 0)  # check if image size is divisible by n, if it's not change the n.
n_blocks = (img_org.shape[0] * img_org.shape[1]) // n

img = np.reshape(img_org.copy(), [img_size, 1])  # reshape it to a 1D vector
edges = np.reshape(edges, [img_size, 1])


def lbs_substitution(pixel1, pixel2):
    """
    substitute pixel 1 with pixel 2
    """
    pixel1_0b = bin(pixel1)
    n_bits_of_pixel1 = len(pixel1_0b) - len(str(pixel2))
    new = pixel1_0b[:n_bits_of_pixel1] + pixel2
    return int(new, base=2)


key = ChaoticLogisticMap()  # Key Generator Class

for i_block in np.arange(0, n_blocks, n):
    pixels_status = ""

    try:
        for p in range(i_block + 1, i_block + n):
            if edges[p][0] == 255:  # if the pixel is edge:
                pixels_status = pixels_status + '1'
                # Embed message to the pixel based on the y:
                y = key.next_key()
                message_to_embed = message[:y]
                message = message[y:]  # Omit the embedded part of the message.

                img[p] = lbs_substitution(img[p][0], message_to_embed)
            else:
                pixels_status = pixels_status + '0'
                # embed message to the pixel based on the x:
                message_to_embed = message[:x]
                message = message[x:]  # Omit the embedded part of the message.

                img[p] = lbs_substitution(img[p][0], message_to_embed)
    except IndexError:  # if the message has done:
        break
    finally:
        img[i_block] = lbs_substitution(img[i_block][0], pixels_status)  # p1 embedded.

img = np.reshape(img, img_org.shape)


# test area:
diff = img_org - img

plt.subplot(221), plt.imshow(img_org, cmap='gray')
plt.title('Original Image')
plt.subplot(222), plt.imshow(img, cmap='gray')
plt.title('Stego Image')
plt.subplot(212), plt.imshow(diff, cmap='gray')
plt.title('Stego and original image differences')
plt.show()
