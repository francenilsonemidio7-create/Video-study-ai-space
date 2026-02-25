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


CSS = """
body { font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
.hero {
  background: linear-gradient(135deg,#6dd5ed 0%,#2193b0 100%);
  color: white; padding: 36px; border-radius: 12px; margin-bottom: 18px;
}
.card { background: white; border-radius: 10px; padding: 18px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
.label { font-weight: 600; color:#333 }
.output-box { background:#0f1724; color: #e6eef8; padding:12px; border-radius:8px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', monospace; }
.btn-primary { background: linear-gradient(90deg,#ff8a00,#e52e71); color: white; border: none; padding: 10px 16px; border-radius:8px }
.small { font-size: 0.9rem; color:#6b7280 }
"""

with gr.Blocks(css=CSS, title="Video Study AI") as demo:
    gr.HTML("""
    <div class='hero'>
      <h1 style='margin:0'>🎓 Video Study AI</h1>
      <p style='margin:6px 0 0 0; opacity:0.95'>Transforme vídeos do YouTube, TikTok e Instagram em provas de estudo interativas.</p>
    </div>
    """)

    with gr.Row().style(mobile_collapse=False):
        with gr.Column(scale=2):
            with gr.Card():
                url_in = gr.Textbox(label="URL do vídeo", placeholder="Cole a URL do YouTube / TikTok / Instagram aqui")
                num_q = gr.Slider(minimum=3, maximum=15, step=1, value=5, label="Número de questões")
                btn = gr.Button("Processar Vídeo", elem_classes="btn-primary")
                gr.Markdown("""<div class='small'>Exemplos: <br>https://www.youtube.com/watch?v=dQw4w9WgXcQ</div>""")
                examples = gr.Examples([
                    ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", 5],
                ], inputs=[url_in, num_q], examples_per_page=3)

        with gr.Column(scale=3):
            with gr.Card():
                gr.Markdown("**Transcrição**")
                transcription_out = gr.Textbox(label=None, lines=12, interactive=False)
            with gr.Card():
                gr.Markdown("**Questões geradas**")
                questions_out = gr.Textbox(label=None, lines=12, interactive=False)

    btn.click(process, inputs=[url_in, num_q], outputs=[transcription_out, questions_out])


if __name__ == "__main__":
    demo.launch()
