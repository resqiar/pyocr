import pytesseract
import cv2
import pyperclip

# Function to copy string into clipboard
def copyToClipboard(string):
    pyperclip.copy(string)
    pyperclip.paste()

# Read Images
img = cv2.imread('img/example.jpg')
textImg = cv2.imread('img/text.jpg')
plateImg = cv2.imread('img/plate.png')
codeImg = cv2.imread('img/code.png')
 
# We need to convert the image into RGB value
# since cv2 format is BGR and tesseract only accept RGB kind of type.
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
codeImg = cv2.cvtColor(codeImg, cv2.COLOR_BGR2RGB)
plateImg = cv2.cvtColor(plateImg, cv2.COLOR_BGR2RGB)

def detectChars(img):
    imgH, _ , _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    text = []
    for box in boxes.splitlines():
        cur = box.split(" ")
        x, y, w, h = int(cur[1]), int(cur[2]), int(cur[3]), int(cur[4])
        # Put a rectangle around detected image
        # the color are Blue Green Red format
        cv2.rectangle(img, (x, imgH - y), (w, imgH - h), (0, 255, 255), 1)
        # Put text 
        cv2.putText(img, cur[0], (x, imgH - y + 10), cv2.FONT_ITALIC, 0.5, (0, 0, 0), 2)
        # push text to result
        text.append(cur[0])
    result = ' '.join(map(str, text))
    copyToClipboard(result)

def detectWords(img):
    boxes = pytesseract.image_to_data(img)
    text = []
    for index, box in enumerate(boxes.splitlines()):
        if index == 0: continue
        cur = box.split()
        if len(cur) == 12:
            # push text to result
            text.append(cur[11])
            # get data from cur iteration
            x, y, w, h = int(cur[6]), int(cur[7]), int(cur[8]), int(cur[9])
            # Put a rectangle around detected image
            # the color are Blue Green Red format
            cv2.rectangle(img, (x, y), (w + x, h + y), (0, 255, 255), 2)
            # Put text 
            cv2.putText(img, cur[11], (x, y + (h + 10)), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)
    result = ' '.join(map(str, text))
    copyToClipboard(result)

def imageToText(img):
    string = pytesseract.image_to_string(img)
    print(string)


# Detect Image to Text
# imageToText(codeImg)

# Detect chars to Text
# detectChars(codeImg)

# Detect Image to Words
# detectWords(codeImg)
# Show the image 
# cv2.imshow('Text Detection', codeImg)

detectChars(plateImg)
cv2.imshow('Plate Detection', plateImg)

cv2.waitKey(0)
