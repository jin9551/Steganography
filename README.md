Purpose and Goals
=================

PURPOSE:
--------
The purpose of our project was to hide and extract a data in a binary image using Run Length Encoding.

GOALS:
--------
Implementation of Run-length encoding on a binary image
Learn how to extract a data without destroying it.


PROCESS & RESULT :
--------

# 1. Cover Image & Hidden Message(image) :
![image](https://github.com/user-attachments/assets/17b5ab8e-469f-4746-8071-ac708a04bbc8)


# 2. Compressed Binary Image & Stego Image : 
![image](https://github.com/user-attachments/assets/34eb68b0-0da4-4634-bc9c-446332b73d1d)

# 3. Original Image & Stego Image :
![image](https://github.com/user-attachments/assets/03b7a2ea-574c-4bcb-8d7e-df29815f70c8)

# 4. Decoded Data : 

![image](https://github.com/user-attachments/assets/cbc270d2-e2d4-4323-a1ae-5ac78cbe3032)


Security, Capacity, and Robustness
------------------------------------

# Security:
You can not see any distortion in the image. (Imperceptibility)
Though the file size of the cover image changed drastically.
98,056 bytes → 350,139 bytes

# Robustness:
Recovered image from the encoded.png lost some details but we managed to extract the image successfully.

# Capacity:
As long as the size of the hidden image is equal to the cover image, you can hide anything.	

