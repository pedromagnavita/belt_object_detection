import cv2
import numpy as np

cap = cv2.VideoCapture(r"C:\Users\patma\OneDrive\Imagens\Video 111 double0.mp4")

triangles_count = 0
squares_count = 0

counting_line = 149

counted_objects = set()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        shape = None
        if len(approx) == 3:
            shape = 'Triangulo'
        elif len(approx) == 4:
            shape = 'Quadrado'

        x, y, w, h = cv2.boundingRect(cnt)
        center_y = y + h // 2

        if shape and center_y > counting_line - 7 and center_y < counting_line + 7:
            obj_id = (x //10, y // 10)

            if obj_id not in counted_objects:
                counted_objects.add(obj_id)

                if shape == 'Triangulo':
                    triangles_count += 1
                elif shape == 'Quadrado':
                    squares_count += 1

        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
        cv2.putText(frame, shape, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    cv2.line(frame, (0, counting_line), (frame.shape[1], counting_line), (0, 0, 255), 2)

    cv2.putText(frame, f'Triangulos: {triangles_count}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f'Quadrados: {squares_count}', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Esteira', frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()