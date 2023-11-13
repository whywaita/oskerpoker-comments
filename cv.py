import cv2
import pytesseract


def ocr_on_frame(frame_data: cv2.Mat):
    """Do OCR on frame data
    Args:
        frame_data: frame data
    Returns:
        text: OCRed text
    """
    text = pytesseract.image_to_string(frame_data, lang='eng', config='--psm 6')
    return text


def is_open_flop(frame_data: cv2.Mat) -> bool:
    board_area = frame_data[720 - 67:720 - 28, 1280 - 220:1280 - 30]
    # print(board_area.shape)
    check_area = board_area[5:10, 5:10]

    # check is black in check_area
    if check_area[4][4][0] > 15 or check_area[4][4][1] > 15 or check_area[4][4][2] > 15:
        return False

    text = ocr_on_frame(board_area)
    if 'VIDEO' in text or 'POKER' in text:
        return True
    return False


# def to_binary(frame_data: cv2.Mat) -> cv2.Mat:
#     bgr_lower = (100, 100, 100)
#     bgr_upper = (255, 255, 255)
#
#     img_mask = cv2.inRange(frame_data, bgr_lower, bgr_upper)
#     contours, hierarchy = cv2.findContours(img_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     contours = list(contours)  # convert tuple to list
#     contours.sort(key=lambda x: cv2.contourArea(x), reverse=True)
#
#     return img_mask


def get_players_frame(frame_data: cv2.Mat) -> list:
    p = []

    hand_area = frame_data[38:300, 22:286]
    player1_area = (hand_area[0:36, :137])
    player2_area = (hand_area[36 + 12:36 * 2 + 12, :137])

    player1_text = ocr_on_frame(player1_area)
    if player1_text:
        p.append(player1_text)
    player2_text = ocr_on_frame(player2_area)
    if player2_text:
        p.append(player2_text)
    return p