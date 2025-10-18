# nodes.py
from states import State, DatasetMeta
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from tools import clone_repo, description, detectDatasetOwners,detectDatasetStatus
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
from jinja2 import  Environment, FileSystemLoader, Undefined
import os, json


def init_config(state: State) -> State:
    """
    Nodo iniziale: prende config già passata nello stato
    e inizializza dataset vuoto
    """

    state["dataset"] = DatasetMeta(
        datasetDescription=None,
        version = None,
        status = None,
        relevantLinks=[],
        developers=[],
        owners=[],
        instructions=[]
    )

    state["messages"] = []  # inizializza lista vuota per dialogo con LLM
    return state





def define_llm(state: State):
    """
    Inizializza un LLM a partire dalla configurazione in state['config'].
    Richiede che init_config abbia già popolato:
      - llm_provider
      - llm_model
      - llm_api_key
    """
    cfg = state["config"]

    provider = cfg["llm_provider"]
    model = cfg["llm_model"]
    api_key = cfg["llm_api_key"] if "llm_api_key" in cfg else None

    if provider != "anthropic":
        raise ValueError(f"LLM provider non supportato: {provider}")

    kwargs = dict(model=model, temperature=0.0, max_tokens=800)
    if api_key:
        kwargs["anthropic_api_key"] = api_key  # override env var se presente

    return ChatAnthropic(**kwargs)


def llm_orchestrator(state: State) -> State:
    """
    Primo giro: seed (System+Human) *e* invocazione LLM nello stesso turno.
    Giri successivi: invoca LLM sulla history.
    Ritorna sempre {"messages": [ ... ]} per add_messages.
    """
    llm = define_llm(state).bind_tools([clone_repo, description, detectDatasetOwners, detectDatasetStatus])

    msgs = state.get("messages") or []

    if not msgs:
        docs_list = ", ".join((state["config"].get("documents_to_generate", [])) or [])

        system_msg = SystemMessage(
            content=(
                # — le tue regole, invarianti —
                "Sei un assistente che aiuta a scrivere report su dati di repository/progetti software."
                "Usa i tool disponibili per recuperare tutte le informazioni dei campi."
            )
        )

        user_msg = HumanMessage(
            content=(
                "Devo scrivere un report sul repository. "
                f"L'URL del repository è {state['config'].get('repo_source','')}. "
                "Concentrati solo sui campi necessari per i documenti richiesti."
            )
        )
        ai_msg: AIMessage = llm.invoke([system_msg, user_msg])
        return {"messages": [system_msg, user_msg, ai_msg]}

    ai_msg: AIMessage = llm.invoke(msgs)
    return {"messages": [ai_msg]}



def harvest_tool_results(state: State) -> State:
    """
    Prende SOLO l'ultimo ToolMessage in coda
    e aggiorna state['dataset'] sostituendo o accodando.
    """
    dataset = state.get("dataset") or {}
    msgs = state.get("messages") or []

    # ultimo messaggio della history che sia un ToolMessage
    last = None
    for m in reversed(msgs):
        if isinstance(m, ToolMessage):
            last = m
            break

    if not last:
        return state

    payload = last.content
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = None

    if isinstance(payload, dict) and "field" in payload:
        field = payload["field"]
        value = payload.get("value")

        current = dataset.get(field)
        if current is None:
            dataset[field] = value
        elif isinstance(current, list):
            dataset[field] = current + ([value] if not isinstance(value, list) else value)
        else:
            # se era stringa o altro → lo trasformo in lista per non perderlo
            dataset[field] = [current] + ([value] if not isinstance(value, list) else value)

        print(f"✅ [harvest] aggiornato {field} → {dataset[field]}")

    state["dataset"] = dataset
    return state




def _to_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i).strip() for i in x if str(i).strip()]
    else:
        s = str(x).strip()
        return [s] if s else []

def generate_contents(state: State) -> State:
    """
    Per ciascun campo di dataset che contiene una lista di spezzoni,
    chiede all'LLM di ricomporli in un unico testo leggibile.
    Per cisascun campo, in generale, migliora la scittura.
    Sostituisce il valore in state['dataset'][field] con il testo finale.
    """
    dataset = state.get("dataset") or {}
    llm = define_llm(state)
    print("✍️ [generator] dataset in ingresso:", state.get("dataset"))

    for field, raw_val in list(dataset.items()):
        snippets = _to_list(raw_val)
        if not snippets:
            continue
        if len(snippets) == 1 and isinstance(raw_val, str):
            # già stringa singola → niente da fare
            continue

        # Prompt grounded-only
        sys = SystemMessage(content=(
            f"Riscrivi in italiano scorrevole i contenuti del campo '{field}'. "
            "Usa esclusivamente i frammenti forniti, senza aggiungere nulla. "
            "Combina in un unico testo coerente."
        ))
        bullets = "\n".join(f"- {s}" for s in snippets)
        human = HumanMessage(content=f"Frammenti:\n{bullets}")

        resp = llm.invoke([sys, human])
        content = resp.content if isinstance(resp.content, str) else str(resp.content)

        dataset[field] = content  # 🔥 sostituisce la lista con il testo unico

    state["dataset"] = dataset
    print(f"✍️ [generator] campo {field}: {snippets} → {content}")
    return state



def compile_artifacts_node(state: dict) -> dict:
    """
    Sostituisce i placeholder Jinja usando *solo* le variabili nello `state`.
    il template deve usare gli stessi nomi di chiave.
    """
    cfg = state.get("config", {}) or {}
    templates_dir = cfg.get("templates_dir")
    outputs_dir  = cfg.get("outputs_doc_dir")
    docs= cfg.get("documents_to_generate")

    # convenzione nome file
    name_map = {
        "data": ("data.j2", "data.md"),
        "model": ("model.j2", "model.md"),
        "application": ("application.j2", "application.md"),    # model e application sono pensati per un' implementazione futura
    }

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=False,
        undefined=Undefined,      # NON fallisce se manca qualcosa; lascia vuoto
        trim_blocks=True,
        lstrip_blocks=True,
    )

    results, errors = [], []

    for d in docs:
        if d not in name_map:
            errors.append((d, "Documento non riconosciuto"))
            continue
        tpl_name, out_name = name_map[d]
    
        try:
            template = env.get_template(tpl_name)

            #  Selezione del context per template 
            if tpl_name == "data.j2":
                
                context = state.get("dataset", {}) or {}
            else:
                # Tutto lo state (il template può accedere a {{ dataset.* }}, {{ config.* }}, ecc.)
                context = dict(state)

            rendered = template.render(**context)

            # Salvataggio
            output_path = os.path.join(outputs_dir, out_name)
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)

                results.append(output_path)
        except Exception as e:
            errors.append((tpl_name, str(e)))

    # Log finale
    msgs = state.get("messages", [])
    if results:
        msgs.append(AIMessage(content="✅ Render completato:\n- " + "\n- ".join(results)))
    if errors:
        details = "\n".join([f"- {t}: {err}" for t, err in errors])
        msgs.append(AIMessage(content=f"⚠️ Errori durante il render:\n{details}"))
    state["messages"] = msgs

    return state

    