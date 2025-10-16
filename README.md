# Documentation Graph (Dataset Focus)

Questo progetto dimostra come costruire un grafo con **LangGraph** per generare documentazione tecnica a partire da un repository AI/ML.  
Al momento il focus è sul documento **Dataset Documentation**, ma l’architettura è pensata per estendersi facilmente per integrare nuovi documenti regolatori, come **Model Documentation** e **Application Documentation**.
Attualmente il lavoro può essere lanciato in qualsiasi momento, eseguendo il main e passando il link del repository di cui si vuole creare la documentazione, ma in futuro potrebbe essere lanciato, tramite un workflow, tramite un evento attivante (es. pull request).

---

## 🗺️ schema del grafo
![Esecuzione del grafo](./images/graphStructure1.png)

setup node: inizializza e istanzia alcune variabili necessarie per il flow designato( es. state[config],state[dataset]....)

llm_orchestrator: orchestration LLM + tool use

toolsNode: esegue i tool definiti ed associati al nodo ( es. @tool clone_repo)

harvesterNode: colleziona tutti i risultati dei tool node e gli assegna alle corrispettive variaibli di stato

generator node:

compilerNode: finalizer che utilizza i dati forniti nello state del grafo per produrre documenti formattati tramite Jinja2

## 📂 Struttura del progetto

```text
project/
|-- states.py        # definizione dello stato
|-- nodes.py         # nodi
|-- tools.py         # tool disponibili 
|-- graph.py         # costruzione del grafo 
|-- main.py          # entry-point: esegue il grafo e stampa risultati
|-- README.md        
|-- images/          # immagini per il README 
|-- templates/       # directory template da geenrare
|-- renderedDocs/    # directory documenti renderizzati e finali
```



---

## ⚙️ Componenti

### `states.py`
Definisce lo **stato globale** del grafo:
- `Config`: configurazione iniziale (repo di origine, documenti da generare).
- `DatasetMeta`: metadati del dataset secondo il template.
- `State`: combinazione di `Config` + `DatasetMeta` + '`messages`.

### `nodes.py`
- `init_config`: inizializza lo state.
- `simple_llm_node` (llm_orchestrator): binda i tool (ask_user_input, clone_repo), ragiona e decide se invocare tool (emettendo tool_calls).
- `compile_artifacts_node` (compilerNode): usa structured output (Pydantic v2) per compilare tutti i campi del dataset solo dalle informazioni emerse in chat/tool; mappa version/status in version_and_status.

### `tools.py`
Contiene **funzioni riutilizzabili** di supporto ai nodi, come:
- `ask_user_input`: chiede input dall' utente via console (CLI)
- `clone repo`:clona la repository localmente


### `graph.py`
Costruisce il **grafo LangGraph**:
- definisce i nodi,
- stabilisce le connessioni (`edges`),
- restituisce il grafo compilato pronto all’esecuzione.

### `main.py`
È l’**entrypoint** del progetto:
- costruisce il grafo tramite `graph.build_graph()`,
- crea uno stato iniziale,
- invoca il grafo,
- stampa il risultato finale.

---

## ▶️ Esecuzione

### Prerequisiti

- python 3.11 +
- git installato
- chiave API del provider LLM(Anthropic)

### Installazione 
1. Installa i requisiti (serve [LangGraph](https://python.langchain.com/docs/langgraph/)):
   ```bash
   pip install langgraph langchain langchain-anthropic pydantic jinja2

### Avvio
  
 ```bash
   python main.py
 
```



![Esecuzione in console](./images/intermedianResults.png)


