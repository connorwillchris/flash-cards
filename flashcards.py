import json
from PIL import Image, ImageDraw, ImageFont
import sys

CARD_WIDTH = 3300 // 3
CARD_HEIGHT = 2550 // 3
ROWS, COLS = 3, 3
MARGIN = 20
FONT_PATH = "C:\\Windows\\fonts\\meiryo.ttc"  # adjust if needed

def create_flashcards(data, output_front, output_back):
    img_width = COLS * CARD_WIDTH + (COLS + 1) * MARGIN
    img_height = ROWS * CARD_HEIGHT + (ROWS + 1) * MARGIN

    front_img = Image.new("RGB", (img_width, img_height), "white")
    back_img = Image.new("RGB", (img_width, img_height), "white")
    draw_front = ImageDraw.Draw(front_img)
    draw_back = ImageDraw.Draw(back_img)

    try:
        font_kanji = ImageFont.truetype(FONT_PATH, 256)
        font_text = ImageFont.truetype(FONT_PATH, 96)
    except:
        font_kanji = ImageFont.load_default()
        font_text = ImageFont.load_default()

    for i, card in enumerate(data[:9]):  # only first 9 cards
        row, col = divmod(i, COLS)
        x = MARGIN + col * (CARD_WIDTH + MARGIN)
        y = MARGIN + row * (CARD_HEIGHT + MARGIN)

        # Draw card borders (shared lines for cutting)
        #draw_front.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], outline="black", width=1)
        #draw_back.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], outline="black", width=1)

        # Front side: Kanji
        kanji = card.get("kanji", "?")
        bbox = draw_front.textbbox((0, 0), kanji, font=font_kanji)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw_front.text((x + (CARD_WIDTH - w) / 2, y + (CARD_HEIGHT - h) / 2), kanji, fill="black", font=font_kanji)

        # Back side: English + POS
        # Flip the card horizontally by placing text from the mirrored column
        flipped_col = COLS - 1 - col
        x_flipped = MARGIN + flipped_col * (CARD_WIDTH + MARGIN)
        y_flipped = y

        #draw_back.rectangle([x_flipped, y_flipped, x_flipped + CARD_WIDTH, y_flipped + CARD_HEIGHT], outline="black", width=1)

        english = card.get("english", "?")
        pos = card.get("pos", "?")
        reading = card.get("reading", "?")
        text = f"{english}\n({pos})\nreading: {reading}"
        draw_back.multiline_text((x_flipped + 10, y_flipped + 10), text, fill="black", font=font_text, spacing=5)

    # Draw shared cut lines across entire grid
    for r in range(1, ROWS):
        y_line = MARGIN + r * (CARD_HEIGHT + MARGIN) - (MARGIN // 2)
        draw_front.line([(MARGIN, y_line), (img_width - MARGIN, y_line)], fill="black", width=1)
        draw_back.line([(MARGIN, y_line), (img_width - MARGIN, y_line)], fill="black", width=1)

    for c in range(1, COLS):
        x_line = MARGIN + c * (CARD_WIDTH + MARGIN) - (MARGIN // 2)
        draw_front.line([(x_line, MARGIN), (x_line, img_height - MARGIN)], fill="black", width=1)
        draw_back.line([(x_line, MARGIN), (x_line, img_height - MARGIN)], fill="black", width=1)

    front_img.save(output_front)
    back_img.save(output_back)
    print(f"Saved flashcards: {output_front}, {output_back}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python flashcards.py input.json")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    create_flashcards(data, "out/flashcards_front.png", "out/flashcards_back.png")
