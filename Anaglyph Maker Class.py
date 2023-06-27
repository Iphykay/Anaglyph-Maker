import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


class Anaglyph_Maker:
    def __init__(self, image, translation, MaxFeatures):
        self.image = image
        self.translation = translation
        self.MaxFeatures = MaxFeatures

    def read_image(self):
        main_image = cv.imread(self.image)
        trans_image = cv.imread(self.translation)

        # Convert to the images to RGB
        self.output_main = cv.cvtColor(main_image, cv.COLOR_BGR2RGB)
        self.output_trans = cv.cvtColor(trans_image, cv.COLOR_BGR2RGB)

        return self.output_main, self.output_trans
    
    def display_image(self, image, name: str):
        self.image = image
        plt.imshow(self.image)
        plt.title(name)
        plt.show()

    def orb_create(self):
        ORB = cv.ORB_create(self.MaxFeatures)

        # detect and compute the keypoints and descriptors with ORB
        self.kp1, self.des1 = ORB.detectAndCompute(self.output_main,None)
        self.kp2, self.des2 = ORB.detectAndCompute(self.output_trans,None)

        # Match descriptors
        mattch_desc = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = mattch_desc.match(self.des1, self.des2, None)

        match_points = cv.drawMatches(self.output_main, self.kp1, self.output_trans, self.kp2, matches, None)

        return self.display_image(match_points, name='Matched Points'), matches


    def homography_matrix(self, matches):
        matches = sorted(matches, key=lambda x:x.distance)

        # Keep only the top matches
        KeepPercent = 0.5
        Good_matches = int(len(matches) * KeepPercent)
        matches = matches[:Good_matches]

        # Take keypoints to build the Homography matrix
        ptA = np.zeros((len(matches),2), dtype=np.float32)
        ptB = np.zeros((len(matches),2), dtype=np.float32)
        for i, match in enumerate(matches):
            ptA[i,:] = self.kp1[match.queryIdx].pt
            ptB[i,:] = self.kp2[match.trainIdx].pt

        # The Homography Matrix
        H, Mask = cv.findHomography(ptA, ptB, method=cv.RANSAC)

        # use Homography to align the images
        h, w, channel = self.output_trans.shape

        # Registration or Aligning
        Align = cv.warpPerspective(self.output_main, H, (w, h))

        return self.display_image(Align, name="Registered Imaged"), Align
    
    def merge(self, Align):
        blue, green, red = cv.split(Align)
        blue1, green1, red1 = cv.split(self.output_trans)

        # Merge them
        Merged = cv.merge([red1, green, blue])

        return self.display_image(Merged, name='Anaglyph Image')
    

class Simulation(Anaglyph_Maker):
    def __init__(self, image, translation, MaxFeatures):
        super().__init__(image, translation, MaxFeatures)

    def run(self):
        read = self.read_image()

        #Display
        orig_image = self.display_image(read[0], name='Original Image')
        transl_image = self.display_image(read[1], name='Translated Image')

        orb_c = self.orb_create()

        homo_g = self.homography_matrix(orb_c[1])

        # Merge
        Merrge = self.merge(homo_g[1])


def main():
    main_image = "C:/Users/Starboy/OneDrive - rit.edu/IPCV/Assignments/HW4/Images/IMG_1681.JPG"
    trans_image = "C:/Users/Starboy/OneDrive - rit.edu/IPCV/Assignments/HW4/Images/IMG_1680.JPG"
    simulate = Simulation(main_image, trans_image, 300)
    simulate.run()

if __name__ == "__main__":
    main()

