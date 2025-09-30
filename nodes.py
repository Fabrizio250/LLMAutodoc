# nodes.py
from states import State, DatasetMeta
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from tools import ask_user_input, clone_repo
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
def init_config(state: State) -> State:
    """
    Nodo iniziale: prende config già passata nello stato
    e inizializza dataset vuoto
    """

    state["dataset"] = DatasetMeta(
        datasetDescription=None,
        version_and_status=(None, None),
        relevantLinks=[],
        developers=[],
        owners=[],
        Instructions=[]
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


def simple_llm_node(state: State) -> State:
    """
    Primo giro: seed (System+Human) *e* invocazione LLM nello stesso turno.
    Giri successivi: invoca LLM sulla history.
    Ritorna sempre {"messages": [ ... ]} per add_messages.
    """
    llm = define_llm(state).bind_tools([ask_user_input, clone_repo])

    msgs = state.get("messages") or []

    if not msgs:
        system_msg = SystemMessage(
            content=("Sei un assistente che aiuta a scrivere report su dati di repository/progetti software. "
                     "Usa i tool disponibili per recuperare le informazioni, e chiedi all'utente solo se necessario.")
        )
        user_msg = HumanMessage(content="Devo scrivere un report sul repository. Aiutami a raccogliere le informazioni necessarie.")
        ai_msg: AIMessage = llm.invoke([system_msg, user_msg])
        return {"messages": [system_msg, user_msg, ai_msg]}

    ai_msg: AIMessage = llm.invoke(msgs)
    return {"messages": [ai_msg]}



# === Modello strutturato per il dataset (estendibile in futuro) ===
class DatasetMetaModel(BaseModel):
    datasetDescription: Optional[str] = None
    version_and_status: Tuple[Optional[str], Optional[str]] = (None, None)
    relevantLinks: List[str] = []
    developers: List[str] = []
    owners: List[str] = []
    Instructions: List[str] = []

def compile_artifacts_node(state: State) -> State:
    """
    Nodo generico di 'compilazione artefatti'.
    Oggi compila i metadati del dataset usando SOLO le info emerse nella chat e dai tool.
    Domani potrai estenderlo per produrre/compilare altri documenti.
    """
    llm_struct = define_llm(state).with_structured_output(DatasetMetaModel)

    sys = SystemMessage(content=(
        "Compila i metadati del dataset. Usa SOLO informazioni presenti nella conversazione e nei risultati dei tool. "
        "Non inventare. Se un campo manca, lascialo None o lista vuota. Limita 'relevantLinks' a max 10."
    ))

    messages = state.get("messages") or []
    result: DatasetMetaModel = llm_struct.invoke([sys] + messages)

    # Merge nello stato esistente (schema attuale di DatasetMeta)
    ds = state.get("dataset") or {
        "datasetDescription": None,
        "version_and_status": (None, None),
        "relevantLinks": [],
        "developers": [],
        "owners": [],
        "Instructions": [],
    }
    r = result.dict()
    ds["datasetDescription"] = r.get("datasetDescription")
    ds["version_and_status"] = tuple(r.get("version_and_status") or (None, None))
    ds["relevantLinks"] = (r.get("relevantLinks") or [])[:10]
    ds["developers"] = r.get("developers") or []
    ds["owners"] = r.get("owners") or []
    ds["Instructions"] = r.get("Instructions") or []

    summary = (
        f"Compilazione completata. "
        f"Descrizione: {'OK' if ds['datasetDescription'] else 'manca'}; "
        f"Version/Status: {ds['version_and_status']}; "
        f"Links: {len(ds['relevantLinks'])}; "
        f"Developers: {len(ds['developers'])}; Owners: {len(ds['owners'])}."
    )
    return {
        "dataset": ds,
        "messages": [AIMessage(content=f"✅ {summary}")],
        "debug": {"compiled": True}
    }

    


