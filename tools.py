import subprocess, tempfile, os
import glob
from langchain.tools import tool

GITHUB_API = "https://api.github.com"  # costante fissa


#funziona bene ma se il repo è troppo grande, potrebbe bloccare il flow o interrompere il tutto per mancanza di spazio sul disco. Bisogna cambiare strategia
@tool("clone_repo")
def clone_repo(repo_url: str, branch: str = None) -> dict:
    """
    Clona un repository GitHub (o una pull request) in una cartella temporanea
    e restituisce il path locale.
    """
    print(f"[TOOL_clone_repo] Clonazione repo {repo_url} (branch={branch})...", flush=True)
    tmpdir = tempfile.mkdtemp(prefix="repo_")
    try:
        cmd = ["git", "clone"]
        if branch:
            cmd += ["--branch", branch]
        cmd += [repo_url, tmpdir]

        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"repo_url": repo_url, "local_path": tmpdir, "error": None}
    except Exception as e:
        return {"repo_url": repo_url, "local_path": tmpdir, "error": str(e)}
    
#funziona bene
@tool("ask_user_input")
def ask_user_input(prompt: str) -> str:
    
    """
    Chiedi all'utente un'informazione mancante e restituisci SOLO la risposta testuale.
    Args:
        prompt: La domanda da porre all'utente.
    Returns:
        La risposta fornita dall'utente (stringa, già ripulita).
    """
    try:
        print(f"[TOOL] {prompt}", flush=True)
        answer = input("> ")
        return (answer or "").strip()
    except KeyboardInterrupt:
        return ""  # o: "ANNULLATO_DALL_UTENTE"
    except EOFError:
        return ""  # input chiuso
    except Exception as e:
        return f"ERRORE: {e}"




@tool("list_repo_files")
def list_repo_files(root: str, patterns: list[str] = None, limit: int = 200) -> dict:
    """
    Lista i file di interesse nel repo clonato (per pattern).
    Esempi di pattern:
      ["**/README*", "**/*.md", "**/*.yml", "**/*.yaml", "**/*.json",
       "**/pyproject.toml", "**/setup.cfg", "**/CITATION.cff", "**/LICENSE",
       "**/data*/**/*"]
    """
    try:
        if not os.path.isdir(root):
            return {"files": [], "error": f"Root non valida: {root}"}
        if patterns is None:
            patterns = ["**/README*", "**/*.md", "**/*.yml", "**/*.yaml", "**/*.json",
                        "**/pyproject.toml", "**/setup.cfg", "**/CITATION.cff",
                        "**/LICENSE", "**/data*/**/*", "**/dataset*/**/*"]
        found = []
        for pat in patterns:
            found.extend(glob.glob(os.path.join(root, pat), recursive=True))
        # tieni solo file normali, dedup, ordina, e limita
        files = sorted({f for f in found if os.path.isfile(f)})
        return {"files": files[:limit], "error": None}
    except Exception as e:
        return {"files": [], "error": str(e)}

@tool("read_text_file")
def read_text_file(path: str, max_bytes: int = 400_000, encoding: str = "utf-8") -> dict:
    """
    Legge un file di testo dal filesystem e restituisce il contenuto (troncato).
    """
    try:
        if not os.path.isfile(path):
            return {"path": path, "content": "", "error": "File non trovato"}
        with open(path, "rb") as f:
            data = f.read(max_bytes)
        try:
            text = data.decode(encoding, errors="replace")
        except Exception:
            text = data.decode("utf-8", errors="replace")
        return {"path": path, "content": text, "error": None}
    except Exception as e:
        return {"path": path, "content": "", "error": str(e)}




