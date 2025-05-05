#Library
import cv2
import pandas as pd
from sklearn.svm import SVC

#Fungsi mencari fitur HSV dan LAB pada citra
def feature_extractor(dataset):
    image_dataset = pd.DataFrame()
    for image in dataset:
        df = pd.DataFrame()

        #Memastikan citra berjenis RGB
        if len(image.shape) == 2 or image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        #Konversi RGB to HSV dan LAB
        hsv_img = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lab_img = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        #Alat Kalkulasi dibagian tengah citra
        height, width, _ = hsv_img.shape
        center = (width // 2, height // 2)

        #Penggunaan alat untuk mengekstrak HSV dan LAB ditengah citra
        hsv_value = hsv_img[center[1], center[0]]
        hue = hsv_value[0]
        saturation = hsv_value[1]

        middle_pixel_lab = lab_img[center[1], center[0]]
        l_value, a_value, b_value = middle_pixel_lab

        #Input nilai HSV dan LAB pada dataframe
        df['HUE'] = [hue]
        df['Saturation'] = [saturation]

        df['L'] = [l_value]
        df['A'] = [a_value]
        df['B'] = [b_value]

        image_dataset = pd.concat([image_dataset, df], ignore_index=True)

    return image_dataset

#Input dataset training
df = pd.read_csv(r"D:/Kuliah/Semester 8/TA 2/INTI/Kedalaman/Progres 9_K(Color and Machine Learning) Part 5 END/Fitur_HSVLAB_Train.csv")

#Input fitur pada x dan kelas pada y
x = df.drop('Stage', axis=1)
y = df['Stage']

# Training SVM model
svm = SVC(kernel="linear")
svm.fit(x, y)

#Input citra yang ingin diukur
imga = cv2.imread("D:/Kuliah/Semester 8/TA 2/INTI/Kedalaman/Progres 8_K(Color and Machine Learning) Part 4/Dataset/Testing/Stage 3/LUKA TERBUKA SIKU KIRI- 3cm x 2cm x 2cm.JPG", 1)

#Mengekstrak fitur HSV dan LAB pada citra
test_dataset = [imga]
x_test = feature_extractor(test_dataset)

#Memprediksi stage kedalaman luka
y_test = svm.predict(x_test)
print(y_test)