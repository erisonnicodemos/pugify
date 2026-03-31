# SpotfyDown 🎵 - v2.0

Uma aplicação web simples e minimalista para baixar músicas do Spotify em formato MP3.

> **v2.0 - Refatorado para Render Nativo com FFmpeg Estático** ✨
> **Production-ready com Gunicorn + Cleanup Automático**

## ✅ Características Principais

- ✅ Interface intuitiva e responsiva (Mobile-first)
- ✅ Validação de URLs do Spotify
- ✅ Download direto em MP3
- ✅ Nomes de arquivo inteligentes (artista_música)
- ✅ **Limpeza automática rigorosa** de arquivos temporários
- ✅ **FFmpeg estático** (não depende de apt-get)
- ✅ **Gunicorn production-ready** (WSGI)
- ✅ Spinner + **feedback visual em tempo real**
- ✅ Otimizado para Render Free Tier (disco efêmero)

## 📋 Stack Tecnológico

- **Backend**: Flask + Gunicorn (WSGI production server)
- **Frontend**: HTML5 + CSS3 + Bootstrap 5 (CDN)
- **Download**: spotdl + yt-dlp
- **Audio**: FFmpeg (binário estático)
- **Hospedagem**: Render (Python nativo, sem Docker)

## 🆕 O Que Mudou na v2.0

### Principal: Render Nativo + FFmpeg Estático

- ❌ **Sem Docker**
- ✅ **`build.sh`** baixa FFmpeg estático (auto-detecta x86_64/ARM64)
- ✅ **Gunicorn** em vez de `python app.py` (Flask dev server)
- ✅ **Cleanup rigoroso** com `@after_this_request`
- ✅ **Frontend melhorado** com progresso em tempo real
- ✅ **Production-grade** para Render Free Tier

**Para detalhes completos da refatoração, veja [REFACTORING.md](REFACTORING.md)**

## 🚀 Quickstart

### Local - Windows

```bash
cd c:\dev\spotfydown
setup.bat

# Rodar com Gunicorn
gunicorn --workers 1 --threads 1 --worker-class gthread --bind 0.0.0.0:5000 app:app

# Acessar: http://localhost:5000
```

### Local - Linux/macOS

```bash
cd ~/spotfydown
bash setup.sh

# Rodar com Gunicorn
gunicorn --workers 1 --threads 1 --worker-class gthread --bind 0.0.0.0:5000 app:app

# Acessar: http://localhost:5000
```

### Render - Blueprint (Automático)

```bash
# 1. Push para GitHub
git push origin main

# 2. No Render Dashboard
# New → Blueprint → Selecione repositório → Deploy

# 3. Acessar URL gerada automaticamente
# https://spotfydown-xxxx.onrender.com
```

## 📁 Estrutura do Projeto

```
spotfydown/
├── app.py                     # Flask refatorado (cleanup, FFmpeg)
├── templates/
│   └── index.html            # Frontend com spinner + progresso
├── requirements.txt          # Com gunicorn
├── build.sh                  # FFmpeg estático (detecta arquitetura)
├── gunicorn.conf.py          # Config Gunicorn (novo)
├── render.yaml               # Render Blueprint (atualizado)
├── setup.sh / setup.bat      # Setup rápido
├── .flaskenv                 # Flask env vars
├── .gitignore                # Git ignore
├── README.md                 # Este arquivo
├── REFACTORING.md            # Detalhes v2.0
├── DEPLOY.md                 # Deploy passo-a-passo
├── TROUBLESHOOTING.md        # 30+ soluções
└── DELIVERY.md               # Checklist
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
PORT=5000                   # Porta (Render fornece dinamicamente)
PYTHONUNBUFFERED=1         # Logging sem buffer (necessário)
```

### FFmpeg - Auto-Detectado

```bash
# App detecta automaticamente ao iniciar:
./ffmpeg_bin/ffmpeg         # Estático (setup por build.sh)
/usr/bin/ffmpeg             # Sistema (fallback)
# Ou fallback para "ffmpeg" no PATH
```

## 🎵 Como Usar

1. **Abra a app**
   - Local: http://localhost:5000
   - Render: https://spotfydown-xxxx.onrender.com

2. **No Spotify**
   - Clique na música
   - "Compartilhar" → "Copiar link da faixa"

3. **Na app**
   - Cole o link
   - Clique "Baixar MP3"
   - Download inicia automaticamente 🎉

## 📊 API Endpoints

### GET `/`
Retorna página principal (HTML)

### POST `/api/download`
Baixa música do Spotify

**Payload:**
```json
{
  "url": "https://open.spotify.com/track/11dFghVXANMlKmJXsNCQvb"
}
```

**Response (sucesso):**
- Arquivo MP3 como attachment
- Content-Type: audio/mpeg
- Cleanup automático após envio

**Response (erro):**
```json
{
  "success": false,
  "error": "Invalid Spotify URL..."
}
```

### GET `/health`
Health check + FFmpeg status

**Response:**
```json
{
  "status": "ok",
  "ffmpeg_path": "/app/ffmpeg_bin/ffmpeg"
}
```

## 🔒 Segurança

✅ URLs validadas com regex
✅ Apenas URLs de faixas Spotify aceitas (não playlists/álbuns)
✅ Timeout: 5 minutos por download
✅ **Cleanup automático** de todos os arquivos temporários
✅ Zero dados persistentes
✅ SSL/TLS automático no Render

## 💾 Gerenciamento de Disco

### Antes (v1.0)
```
Temp dir: ./temp_downloads/
Risco: Pode encher disco do Render ⚠️
```

### Depois (v2.0)
```
Temp dir: /tmp/spotfydown_XXXXX/
Cleanup: @after_this_request (garantido)
Sistema: Render limpa /tmp periodicamente
Resultado: Zero risco de quota de disco ✅
```

Implementação:
```python
@after_this_request
def cleanup_after_download(response):
    cleanup_file(file_path)
    cleanup_temp_directory(download_dir)
    return response
```

## 🚀 Deployment no Render

### Opção 1: Blueprint (Recomendado)

1. Acesse https://dashboard.render.com
2. Clique **"New"** → **"Blueprint"**
3. Selecione seu repositório `spotfydown`
4. Render lê `render.yaml` automaticamente
5. Clique **"Deploy"** ✅

### Opção 2: Web Service Manual

1. Clique **"New"** → **"Web Service"**
2. Configure:
   - **Name**: spotfydown
   - **Environment**: Python 3
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn --workers 2 --threads 2 --worker-class gthread --bind 0.0.0.0:$PORT --timeout 300 app:app`
3. Clique **"Create Web Service"** ✅

### O que `build.sh` Faz

```bash
# 1. Instala Python packages
pip install -r requirements.txt

# 2. Detecta arquitetura (x86_64 ou ARM64)
uname -m

# 3. Baixa FFmpeg estático
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# 4. Extrai e configura permissões
tar xf ffmpeg-release-amd64-static.tar.xz
mkdir -p ffmpeg_bin
cp ffmpeg-*/ffmpeg ffmpeg_bin/
chmod +x ffmpeg_bin/ffmpeg
```

## 📈 Performance

| Métrica | Valor |
|---------|-------|
| **Workers** | 2 (dev: 1) |
| **Threads** | 2 por worker |
| **Timeout** | 300s (5 min) |
| **Max Concurrent** | 4 requisições |
| **Backlog** | 2048 |

Ajuste em `gunicorn.conf.py` ou `render.yaml` se necessário.

## 🆘 Troubleshooting Rápido

### ❌ "FFmpeg not found"
```bash
# ✅ Resolvido: build.sh já faz isso
# Manual: bash build.sh
```

### ❌ "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### ❌ "Port já em uso"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux
lsof -i :5000
kill -9 <PID>
```

### ❌ "Disco cheio no Render"
```bash
# ✅ Resolvido: cleanup automático
# Se ainda ocorrer: Restart o serviço
# Render Dashboard → Service → Restart
```

**Para 30+ soluções completas, veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## 📖 Documentação

| Arquivo | Conteúdo |
|---------|----------|
| **README.md** | 📄 Overview (este arquivo) |
| **REFACTORING.md** | 🔄 Mudanças v2.0 detalhadas |
| **DEPLOY.md** | 🚀 Deploy passo-a-passo |
| **TROUBLESHOOTING.md** | 🆘 30+ soluções |
| **DELIVERY.md** | ✅ Checklist |

## 🎯 Próximas Melhorias (Opcional)

- [ ] Cache de downloads
- [ ] Fila com Celery + Redis
- [ ] Autenticação básica
- [ ] Histórico de downloads
- [ ] Suporte a playlists
- [ ] Formatos alternativos (M4A, OPUS, FLAC)
- [ ] Dashboard de estatísticas

## 📊 Resumo da Refatoração v2.0

| Aspecto | v1.0 | v2.0 |
|---------|------|------|
| **Server** | Flask dev | Gunicorn prod ✅ |
| **FFmpeg** | apt-get | Estático ✅ |
| **Cleanup** | finally/unlink | @after_this_request ✅ |
| **Temp dirs** | ./temp_downloads | /tmp auto-cleanup ✅ |
| **Frontend** | Básico | Spinner + progresso ✅ |
| **Concorrência** | 1 | 4 ✅ |
| **Docker** | Sim | Não (nativo) ✅ |
| **Production** | ⚠️ Não | ✅ Sim |

## 📞 Suporte & Referências

- **Render Docs**: https://render.com/docs
- **Gunicorn**: https://gunicorn.org
- **FFmpeg Static**: https://johnvansickle.com/ffmpeg
- **spotdl**: https://github.com/spotDL/spotdl
- **Flask**: https://flask.palletsprojects.com

## 📜 Licença

Uso pessoal. Respeite os termos de serviço do Spotify.

---

**SpotfyDown v2.0** 🚀
*Production-ready para Render | Render nativo | FFmpeg estático | Zero Docker*

*Atualizado: March 31, 2026*
*Refatoração: Gunicorn + FFmpeg Estático + Cleanup Automático*
