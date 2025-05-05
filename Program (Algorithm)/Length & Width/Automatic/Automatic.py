import cv2
import numpy as np
from object_detector import HomogeneousBgDetector

# Fungsi untuk menghilangkan ArUco marker dari gambar
def remove_aruco_markers(image, corners):
    for corner in corners:
        int_corners = np.array(corner, dtype=np.intp)
        cv2.fillPoly(image, [int_corners], (255, 255, 255))
    return image

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

# Sesuaikan parameter deteksi jika diperlukan
parameters.adaptiveThreshConstant = 7
parameters.minMarkerPerimeterRate = 0.03
parameters.maxMarkerPerimeterRate = 4.0

# Load Image
img_path = "LUKA TERBUKA- 5cm x 3cm x 3cm.jpg"  # Ganti dengan jalur gambar Anda
img = cv2.imread(img_path)

# Check if image is loaded successfully
if img is None:
    print("Error: Gambar tidak dapat dimuat. Periksa jalur file gambar.")
    exit()

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create ArucoDetector object
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
corners, ids, rejectedImgPoints = aruco_detector.detectMarkers(gray)

print(f"Corners: {corners}")
print(f"IDs: {ids}")
print(f"Rejected: {rejectedImgPoints}")

# Ensure at least one marker is detected
if ids is not None:
    # Draw polygon around the marker
    int_corners = np.array(corners, dtype=np.intp)
    cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

    # Aruco Perimeter
    aruco_perimeter = cv2.arcLength(corners[0], True)

    # Pixel to cm ratio
    pixel_cm_ratio = aruco_perimeter / 20
    print(f"Pixel to cm ratio: {pixel_cm_ratio}")

    # Remove ArUco markers from the image
    img_no_aruco = remove_aruco_markers(img.copy(), corners)

    # Convert to grayscale for wound detection
    img_wound_gray = cv2.cvtColor(img_no_aruco, cv2.COLOR_BGR2GRAY)

    # Bluring Image
    blurimage = cv2.GaussianBlur(img_wound_gray, (15, 15), 0)

    # Threshold Image
    imw = cv2.threshold(blurimage, 60, 255, cv2.THRESH_BINARY)[1]

    # Teknik Opening (Erosi-Dilatasi) Image
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(imw, cv2.MORPH_OPEN, kernel)

    # Edge Detection Canny Image
    canny = cv2.Canny(opening, 100, 200)

    # Dilatasi Edge Image
    kernel = np.ones((3, 3), np.uint8)
    dilatasi = cv2.dilate(canny, kernel, iterations=1)

    # Mewarnai Bagian dalam Edge Image
    contours, _ = cv2.findContours(dilatasi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        big_contour = max(contours, key=cv2.contourArea)

        # Draw white filled contour on black background
        result = np.zeros_like(dilatasi)
        cv2.drawContours(result, [big_contour], 0, (255, 255, 255), cv2.FILLED)

        # Save and reload results
        cv2.imwrite('knife_edge_result.jpg', result)
        imn = cv2.imread("knife_edge_result.jpg")

        # Deteksi objek di gambar luka
        detector = HomogeneousBgDetector()
        contours = detector.detect_objects(imn)
        print(contours)

        # Draw objects boundaries
        for cnt in contours:
            # Get rect
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # Konversi panjang dan lebar dari piksel ke cm
            w_cm = round(w / pixel_cm_ratio, 1)
            h_cm = round(h / pixel_cm_ratio, 1)

            cv2.circle(img_no_aruco, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img_no_aruco, [box], True, (255, 0, 0), 2)
            cv2.putText(img_no_aruco, "Width {} cm".format(w_cm), (int(x-100), int(y-20)), cv2.FONT_HERSHEY_PLAIN, 2, (100,200,0),2)
            cv2.putText(img_no_aruco, "Height {} cm".format(h_cm), (int(x-100), int(y+15)), cv2.FONT_HERSHEY_PLAIN, 2, (100,200,0),2)

        # Save the result image
        cv2.imwrite("result_combined_image.jpg", img_no_aruco)
        print("Gambar hasil telah disimpan sebagai 'result_combined_image.jpg'")

        # Display the result
        cv2.imshow("Combined Image", img_no_aruco)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Tidak ada kontur luka yang terdeteksi.")
else:
    print("Error: Tidak ada marker ArUco yang terdeteksi.")

# Membuat panjang dan lebar terbalik jika panjang lebih kecil dari lebar
Panjang = w_cm
Lebar = h_cm

if Panjang < Lebar:
    Panjang, Lebar = Lebar, Panjang
print("Panjang:", Panjang)
print("Lebar  :", Lebar)