# 🎓 Video Study AI - Hugging Face Space

Transforme vídeos do YouTube, TikTok e Instagram em provas de estudo interativas!

## 🚀 O que é?

**Video Study AI** é uma aplicação de IA que:

1. **Aceita URLs de vídeos** de YouTube, TikTok e Instagram
2. **Baixa e processa** o vídeo automaticamente
3. **Extrai o áudio** e **transcreve** o conteúdo usando OpenAI Whisper
4. **Analisa o conteúdo** com modelos de linguagem do Hugging Face
5. **Gera questões de estudo** personalizadas para você praticar

## 📋 Como Usar

### Passo 1: Acesse o Space
Abra o link do Hugging Face Space no seu navegador.

### Passo 2: Cole a URL do Vídeo
Cole a URL de um vídeo do:
- ✅ YouTube
- ✅ TikTok
- ✅ Instagram

### Passo 3: Escolha o Número de Questões
Selecione quantas questões você quer gerar (3 a 15).

### Passo 4: Clique em "Processar Vídeo"
Aguarde enquanto o sistema:
- Baixa o vídeo
- Extrai o áudio
- Transcreve o conteúdo
- Gera as questões

### Passo 5: Estude!
Você receberá:
- 📄 A transcrição completa do vídeo
- 📝 Questões de estudo com múltiplas opções
- 📊 Diferentes níveis de dificuldade

## 🛠️ Tecnologias Utilizadas

- **Gradio**: Interface web interativa
- **Transformers (Hugging Face)**: Modelos de IA
- **OpenAI Whisper**: Transcrição de áudio
- **yt-dlp**: Download de vídeos
- **PyTorch**: Framework de deep learning

## 📦 Requisitos

- Python 3.8+
- GPU (recomendado para melhor desempenho)
- Conexão com a internet

## 🔧 Instalação Local (Opcional)

Se você quer rodar localmente:

```bash
# Clone ou baixe os arquivos
git clone <seu-repositório>
cd video-study-ai-space

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

A aplicação estará disponível em `http://localhost:7860`

## 📝 Exemplos de URLs

### YouTube

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### TikTok

```
https://www.tiktok.com/@usuario/video/1234567890
```

### Instagram

```
https://www.instagram.com/p/ABC123DEF456/
```

## ⚠️ Limitações

- O vídeo deve ter áudio (sem áudio = sem transcrição)
- Melhor desempenho com áudio em português ou inglês
- Vídeos muito longos podem levar mais tempo para processar
- A qualidade das questões depende da qualidade do áudio

## 🎯 Dicas para Melhores Resultados

1. **Use vídeos educativos** - Quanto mais didático, melhor as questões
2. **Áudio claro** - Evite vídeos com muito ruído de fundo
3. **Duração moderada** - Vídeos de 5-20 minutos funcionam melhor
4. **Idioma suportado** - Português ou inglês para melhor transcrição

## 🤝 Contribuições

Quer melhorar o projeto? Contribuições são bem-vindas!

## 📄 Licença

MIT License - Veja LICENSE para detalhes

## 📧 Suporte

Tem dúvidas ou encontrou um bug? Abra uma issue no repositório!

---

**Desenvolvido com ❤️ para estudantes**

Transforme seus vídeos favoritos em ferramentas de aprendizado!
