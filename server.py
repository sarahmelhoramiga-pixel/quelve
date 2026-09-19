import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PORT = int(os.environ.get("PORT", "8080"))
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

SYSTEM_PROMPT = """Você é a IA educacional do aplicativo quelve. Responda em português do Brasil.
Explique o raciocínio passo a passo com linguagem adequada à série do estudante.
Não entregue apenas a resposta: ensine como pensar e inclua uma dica curta para praticar.
Se a pergunta estiver incompleta, peça somente a informação necessária.
Não incentive cola, fraude ou qualquer atividade perigosa."""


def gemini_answer(question, grade, source):
    if not GEMINI_KEY:
        raise RuntimeError("GEMINI_API_KEY ausente")
    prompt = (
        f"Série/faixa escolar: {grade or 'não informada'}\n"
        f"Origem da pergunta: {source or 'texto'}\n\n"
        f"Pergunta do estudante:\n{question}"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 900},
    }
    req = Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_KEY},
        method="POST",
    )
    with urlopen(req, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"explanation": text, "model": MODEL}


class Handler(SimpleHTTPRequestHandler):
    def _json(self, status, body):
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/ask":
            self._json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(data.get("question", "")).strip()
            if not question:
                self._json(400, {"error": "empty_question"})
                return
            self._json(200, gemini_answer(question, data.get("grade"), data.get("source")))
        except (HTTPError, URLError, KeyError, ValueError, RuntimeError, TimeoutError):
            self._json(502, {"error": "ai_unavailable"})
        except Exception:
            self._json(500, {"error": "server_error"})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"quelve em http://localhost:{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
