import cv2
import numpy as np

# Fungsi untuk menghitung panjang garis
def calculate_line_length(x1, y1, x2, y2):
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return length

# Fungsi untuk menggambar garis dan mendapatkan koordinatnya
drawing = False  # true jika mouse sedang digerakkan
ix, iy = -1, -1  # koordinat awal

lines = []  # menyimpan koordinat garis yang digambar

# Fungsi untuk menggambar garis pada gambar
def draw_line(event, x, y, flags, param):
    global ix, iy, drawing, img, lines

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.line(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (ix, iy), (x, y), (0, 255, 0), 2)
        lines.append(((ix, iy), (x, y)))

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

# Sesuaikan parameter deteksi jika diperlukan
parameters.adaptiveThreshConstant = 7
parameters.minMarkerPerimeterRate = 0.03
parameters.maxMarkerPerimeterRate = 4.0

# Load Image
img_path = "DATA7A.jpg"  # Ganti dengan jalur gambar Anda
img = cv2.imread(img_path)

# Check if image is loaded successfully
if img is None:
    print("Error: Gambar tidak dapat dimuat. Periksa jalur file gambar.")
    exit()

# Resize image to fit screen
def resize_to_fit_screen(image):
    screen_res = 1280, 720  # resolusi layar target (atau gunakan resolusi layar perangkat Anda)
    scale_width = screen_res[0] / image.shape[1]
    scale_height = screen_res[1] / image.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(image.shape[1] * scale)
    window_height = int(image.shape[0] * scale)
    resized_image = cv2.resize(image, (window_width, window_height))
    return resized_image

img = resize_to_fit_screen(img)

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

    # Display the image and set the mouse callback function
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_line)

    print("Gambar siap. Gambarlah dua garis untuk panjang dan lebar luka.")

    # Display the image until two lines are drawn
    while True:
        cv2.imshow('image', img)
        if len(lines) >= 2:
            break
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

    if len(lines) < 2:
        print("Error: Anda harus menggambar dua garis untuk panjang dan lebar.")
        exit()

    # Extracting the coordinates of the lines
    ((x1_length, y1_length), (x2_length, y2_length)) = lines[0]
    ((x1_width, y1_width), (x2_width, y2_width)) = lines[1]

    # Menghitung panjang dan lebar luka berdasarkan garis yang digambar
    length_pixels = calculate_line_length(x1_length, y1_length, x2_length, y2_length)
    width_pixels = calculate_line_length(x1_width, y1_width, x2_width, y2_width)

    # Konversi panjang dan lebar dari piksel ke cm
    length_cm = length_pixels / pixel_cm_ratio
    width_cm = width_pixels / pixel_cm_ratio

    print(f"Panjang luka: {length_cm:.2f} cm")
    print(f"Lebar luka: {width_cm:.2f} cm")

    # Gambar yang telah ditandai
    cv2.putText(img, "Length: {:.2f} cm".format(length_cm), (x1_length, y1_length-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(img, "Width: {:.2f} cm".format(width_cm), (x1_width, y1_width-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Simpan gambar yang telah ditandai
    cv2.imwrite("marked_image.jpg", img)
    print("Gambar yang telah ditandai disimpan sebagai 'marked_image.jpg'")

    # Tampilkan gambar yang telah ditandai
    img_resized = resize_to_fit_screen(img)  # resize untuk tampilan
    cv2.imshow("Marked Image", img_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Tidak ada marker ArUco yang terdeteksi.")

# Membuat panjang dan lebar terbalik jika panjang lebih kecil dari lebar
Panjang = length_cm
Lebar = width_cm

if Panjang < Lebar:
    Panjang, Lebar = Lebar, Panjang
print("Panjang:", Panjang)
print("Lebar  :", Lebar)
