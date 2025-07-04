# Anaglyph-Maker
Anaglyph images are created by combining two offset images, one for the left eye and 
one for the right eye, using different color channels (typically red and cyan). 

A left image

![left_image](https://github.com/user-attachments/assets/079d09f2-e904-44f8-88f8-e0861a634e0a)

and 
right images 

![right_image](https://github.com/user-attachments/assets/58571e9a-8699-4693-83e7-45c7b63379bd)

are taken, with the right image pushed to a translated distance.

Key features are obtained using ORB, with matched.

![matched_keypoints](https://github.com/user-attachments/assets/22ad9333-5105-422a-a887-199d9fff829d)

Homography matrix used to register those images together.

![registered_image](https://github.com/user-attachments/assets/4b4a8b6e-1cce-4392-8293-682dad3ad9b0)


Output: 


![output](https://github.com/user-attachments/assets/ce502868-9581-4ad5-8748-d8a2ab14cdc5)
