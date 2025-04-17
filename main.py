from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
from fastapi import FastAPI, Response
from io import BytesIO

app = FastAPI()

origins = ["https://app.glintsolar.com", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
)


@app.get("/XYZ/{z}/{x}/{y}")
async def get_image(x: int, y: int, z: int):
    image = Image.new(
        "RGBA", (256, 256), color=(0, 0, 0, 0)
    )  # 'RGBA' mode for transparent background
    draw = ImageDraw.Draw(image)

    draw.text(
        xy=(10, 10),
        text=f"Tilenames",
        fill="black",
        font=ImageFont.truetype("OpenSans_SemiCondensed-Regular.ttf", 16),
    )  # download from: https://fonts.google.com/
    draw.text(
        xy=(10, 36),
        text=f"XYZ or slippy map, z/x/y:",
        fill="black",
        font=ImageFont.truetype("OpenSans_SemiCondensed-Regular.ttf", 24),
    )
    draw.text(
        xy=(20, 72),
        text=f"{z}/{x}/{y}",
        fill="black",
        font=ImageFont.truetype("OpenSans_SemiCondensed-Regular.ttf", 32),
    )

    if z > 0:
        draw.text(
            xy=(10, 120),
            text=f"TMS (default mapproxy),",
            fill="black",
            font=ImageFont.truetype("OpenSans_SemiCondensed-Regular.ttf", 24),
        )
        draw.text(
            xy=(10, 150),
            text=f"z/x/y:",
            fill="black",
            font=ImageFont.truetype("OpenSans_SemiCondensed-Regular.ttf", 24),
        )
        draw.text(
            xy=(20, 190),
            text=f"{z-1}/{x}/{2**z-1-y}",
            fill="black",
            font=ImageFont.truetype("OpenSans_SemiCondensed-Regular.ttf", 32),
        )

    border_width = 2
    draw.rectangle([(0, 0), (256, 256)], outline="red", width=border_width)

    buffer = BytesIO()
    image.save(buffer, format="PNG")  # Save as 'PNG' format
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="image/png")
