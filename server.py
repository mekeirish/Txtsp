from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import asyncio

app = FastAPI()

# Autoriser les requêtes depuis votre page HTML locale
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Voix neuronales Microsoft Azure disponibles pour l'arabe
VOICES = {
    "ar-EG-SalmaNeural": "سلمى (مصر - أنثى طبيعية)",
    "ar-SA-ZariyahNeural": "زاريَة (السعودية - أنثى)",
    "ar-SA-HamedNeural": "حامد (السعودية - ذكر)",
    "ar-AE-FatimaNeural": "فاطمة (الإمارات - أنثى)"
}

@app.get("/synthesize")
async def synthesize(text: str, voice: str = "ar-EG-SalmaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    
    return Response(content=bytes(audio_data), media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
