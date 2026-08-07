from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import qrcode
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_qr_code")
async def generate_qr_code(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text.strip():
        return JSONResponse(content={"error": "Text is required to generate QR code."})

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white') 
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = buffer.getvalue()
    return {"qr_code": qr_base64}
    