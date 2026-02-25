import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import gradio as gr
import yt_dlp
import whisper
from transformers import pipeline

MODEL_NAME = "google/flan-t5-small"

qg_pipeline = pipeline("text2text-generation", model=MODEL_NAME)


def download_video(url: str, out_dir: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename


def convert_to_wav(input_path: str, output_path: str):
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ar",
        "16000",
        "-ac",
        "1",
        output_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def transcribe_audio(model, audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result.get("text", "")


def generate_questions(text: str, n_questions: int) -> str:
    prompt = (
        f"Gere {n_questions} questões de múltipla escolha (A-D) a partir do texto abaixo. "
        "Inclua as alternativas e marque a resposta correta no final de cada questão com 'Resposta: <letra>'.\n\n"
        f"Texto:\n{text}"
    )
    out = qg_pipeline(prompt, max_length=512, do_sample=False)
    # pipeline returns a list of dicts
    generated = out[0]["generated_text"]
    return generated


def process(url: str, num_questions: int):
    tmpdir = tempfile.mkdtemp(prefix="video_study_")
    try:
        # Download
        downloaded = download_video(url, tmpdir)

        # Convert to wav
        wav_path = os.path.join(tmpdir, "audio.wav")
        convert_to_wav(downloaded, wav_path)

        # Transcribe
        whisper_model = whisper.load_model("small")
        transcription = transcribe_audio(whisper_model, wav_path)

        # Generate questions
        questions = generate_questions(transcription, num_questions)

        return transcription, questions
    except Exception as e:
        return f"Erro: {e}", ""
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


with gr.Blocks() as demo:
    gr.Markdown("# 🎓 Video Study AI - Hugging Face Space")
    with gr.Row():
        url_in = gr.Textbox(label="URL do vídeo (YouTube / TikTok / Instagram)", placeholder="Cole a URL aqui")
        num_q = gr.Slider(minimum=3, maximum=15, step=1, value=5, label="Número de questões")
    btn = gr.Button("Processar Vídeo")
    transcription_out = gr.Textbox(label="Transcrição", lines=12)
    questions_out = gr.Textbox(label="Questões geradas", lines=12)

    btn.click(process, inputs=[url_in, num_q], outputs=[transcription_out, questions_out])


if __name__ == "__main__":
    demo.launch()
