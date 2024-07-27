import cv2

# 動きの検出器を初期化
backSub = cv2.createBackgroundSubtractorMOG2()

# カメラのキャプチャを初期化
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

while True:
    # フレームをキャプチャする
    ret, frame = cap.read()

    if not ret:
        print("フレームを取得できませんでした")
        break

    # 背景差分を適用
    fgMask = backSub.apply(frame)

    # モルフォロジー変換でノイズを除去（オプション）
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)

    # 輪郭を検出
    contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 輪郭に対して矩形を描画
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # ノイズを除去（適切な閾値に調整）
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # フレームを表示
    cv2.imshow('Motion Detection with Bounding Box', frame)

    # 'q'キーでループを終了する
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# キャプチャとウィンドウを解放
cap.release()
cv2.destroyAllWindows()