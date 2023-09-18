import cv2

def contains_human_face(image_path):
    # Load the Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale (required for Haar Cascade)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces using Haar Cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if faces were detected
    if len(faces) > 0:
        return True
    else:
        return False

# Example usage
image_path = 'venv/1694699337281.JPEG'
if contains_human_face(image_path):
    print("The image contains a human face.")
else:
    print("No human faces were found in the image.")