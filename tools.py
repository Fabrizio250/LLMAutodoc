import subprocess, tempfile, os
import glob
from langchain_core.tools import tool

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
    
    

@tool("ask_user_input")
def ask_user_input(field: str, prompt: str) -> dict:
    """
    Chiede all'utente un'informazione mancante per uno specifico campo.
    Ritorna SEMPRE un payload strutturato minimal:
      {"field": "<campo>", "value": <string|list[str]>}
    """
    print(f"[ask_user_input] field={field} :: {prompt}", flush=True)
    # In runtime interattivo: l’UI inserirà la risposta dell’utente dentro 'value'.
    return {"field": field, "value": ""}

@tool("description")
def description() -> dict:
    """
    Esempio di tool che popola 'datasetDescription'.
    (Qui fittizio; quando avrai l’estrattore reale, basta che rispetti {field, value})
    """
    return {
        "field": "datasetDescription",
        "value": "Questa è una descrizione fittizia generata dal tool di test."
    }

@tool("detectDatasetOwners")
def detectDatasetOwners() -> dict:
    """
    Esempio di tool che popola 'DatasetOwners'.
    (Qui fittizio basta che rispetti {field, value})
    """
    return {
        "field": "owners",
        "value": "Luca Giorgione, Luca Paparella."
    }

@tool("detectDatasetStatus")
def detectDatasetStatus() -> dict:
    """
    Esempio di tool che popola 'DatasetStatus'.
    (Qui fittizio; basta che rispetti {field, value})
    """
    return {"field": "status", "value": "experimental"}