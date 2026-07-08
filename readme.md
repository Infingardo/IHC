# 🧬 IHC Hub v3.9.1

**Motore di supporto alla diagnosi differenziale in Anatomia Patologica**  
Sviluppato per uso interno · SC Anatomia Patologica · ASST Fatebenefratelli-Sacco, Milano

---

## Cosa fa

IHC Hub è uno strumento di orientamento diagnostico basato su inferenza bayesiana applicata al profilo immunoistochimico. Dato un set di marker positivi e negativi, calcola le probabilità posteriori per 37 diagnosi differenziali e suggerisce il prossimo marker con il massimo guadagno informativo.

**Non sostituisce il giudizio del patologo.** Le percentuali prodotte sono posteriori relative al modello interno — non probabilità cliniche assolute.

---

## Struttura del tool

### Tre moduli principali

| Modulo | Funzione |
|--------|----------|
| **IHC Cascade** | Workflow guidato in 5 passi: morfologia EE → screening (CK/Vim/S100/CD45) → Big Four CK → pannello mirato → diagnosi |
| **Ricerca Inversa** | Input libero: trascina marker in POS/NEG, analisi Bayes immediata, suggerimento next marker |
| **Quiz** | Training: profilo IHC → risposta a scelta multipla su diagnosi più probabile |

### Semaforo disponibilità marker

| Colore | Significato |
|--------|-------------|
| 🟢 Verde | Disponibile FBF (eseguibile internamente) |
| 🟡 Giallo | Disponibile SACCO (inviare al presidio) |
| 🔴 Rosso | Non disponibile localmente (outsourcing / ND) |

---

## Motore bayesiano

### Algoritmo

Per ogni diagnosi `d` con prior `p(d)` e set di marker testati `M`:

```
log P(d|M) = log p(d) + Σ_m w_m · c_m · log LR_m
```

dove:
- `LR+_m = sens / (1 − spec)` per marker positivo
- `LR−_m = (1 − sens) / spec` per marker negativo  
- `w_m` = peso clinico del marker (1.0 baseline, fino a 1.6 per marker altamente specifici)
- `c_m` = fattore di penalizzazione per ridondanza informativa tra marker correlati

### Correzione correlazione

17 gruppi di marker correlati con penalizzazione progressiva (1°, 2°+ membro già testato nella stessa direzione). Esempi:
- `[CD20, PAX5, CD79A]` → penaltyPos [0.65, 0.45]
- `[HEPPAR, ARGINASI, GLYPICAN3]` → penaltyPos [0.70, 0.50]
- `[CROMOGRANINA, SINAPTOFISINA, CD56]` → penaltyPos [0.60, 0.40]

### Filtro morfologico

La morfologia EE modula i prior prima del calcolo: selezionando "Linfoide" le entità non linfomatose ricevono prior × 0.15. Riduce il rumore, non sostituisce il pannello.

### Robustezza del ranking

Metrica composita (non calibrata, uso interno):

```
score = 0.55·Δ(top1−top2) + 0.25·min(n_tested/4, 1) + 0.20·coverage − flag_penalty
```

Soglie: Alta ≥ 0.45 · Intermedia ≥ 0.25 · Incerta < 0.25

### Guadagno informativo (next marker)

Information gain ponderato sul posteriore corrente. Suggerisce il marker che massimizza la riduzione di entropia della distribuzione diagnostica. Solo marker selezionabili nella modalità UI attiva (FBF o FBF+SACCO).  
⚠ Pattern marker esclusi dall'IG binario in questa release (IG multi-stato in roadmap v3.10).

---

## Architetture speciali dei marker

### Loss-marker (oncosoppressori)

I marker con `loss:true` nel `markerDB` (BAP1, SMAD4, MMR, INI-1, BRG1/SMARCA4, ATRX, PTEN, RB1, SDHB, MTAP, H3K27me3, FH, E-Caderina, ecc.) hanno una UI dedicata con tre stati:

| Stato | Significato clinico | Come entra in Bayes |
|-------|--------------------|--------------------|
| **Retained** (mantenuto) | Espressione nucleare conservata — atteso nel normale | `s = P(loss\|dx)`, retained → LR− |
| **Lost** (perso) | Perdita di espressione con controllo interno positivo — evento patologico | `s = P(loss\|dx)`, lost → LR+ |
| **n.i.** (non interpretabile) | Controllo interno assente — risultato non valutabile | escluso dal calcolo |

Il controllo interno (CI) viene registrato separatamente dalla perdita; il badge "CI confermato" appare solo se il CI è esplicitamente positivo. Questo previene falsi-negativi da cattiva fissazione.

### Pattern-marker (β-catenina)

I marker con `type:'pattern'` nel `markerDB` accettano un pattern qualitativo al posto di positivo/negativo. Attualmente: **β-Catenina** (membranous / nuclear).

```js
// Esempio bayesDB: probabilità condizionali per pattern
'BETA_CATENIN': { type:'pattern', patternProbs:{'membranous':0.15,'nuclear':0.85}, w:1.3 }
// → P(nuclear | Fibromatosi Desmoide) = 0.85
// → P(nuclear | Adenocarcinoma Colorettale) = 0.45
// → P(nuclear | Sarcoma Sinoviale) = 0.55
```

`computeBayes` usa `patternProbs[selectedPattern]` come likelihood diretta (non come LR binario). L'architettura `type-system` è pronta per p53 (wt/mut/null), Ki-67 (basso/intermedio/alto), e MMR composito.  
⚠ Cascade non supporta pattern marker in questa release (esclusi dal pannello mirato).

---

## Archivio marker

| Sede | N | Note |
|------|---|------|
| FBF (locale) | 143 | Disponibili internamente |
| SACCO | 77 | Invio al presidio |
| ND / outsourcing | 16 | Non in lista attiva UI |
| **Totale markerDB** | **236** | Inclusi alias e sinonimi |

**37 entità diagnostiche modellate** (carcinomi, linfomi, sarcomi, tumori germinali, NEN, melanoma, mesotelioma, tumori epatici, tiroidei, prostatici, renali, adrenocorticale, Merkel, fibromatosi desmoide).

---

## Workflow consigliato

### Caso nuovo con morfologia definita

```
Cascade → Step 0 (sede anatomica / contesto)
        → Step 1 (morfologia EE)
        → Step 2 (screening CK/Vim/S100/CD45)
        → Step 3 (Big Four, solo se epiteliale)
        → Step 4 (pannello mirato)
        → Step 5 (diagnosi differenziale)
        → [opzionale] Apri in Ricerca Inversa per affinare
```

### Revisione caso / consulenza

```
Ricerca Inversa → imposta morfologia
               → trascina marker noti in POS/NEG
               → inserisci loss-marker (retained/lost/n.i.)
               → inserisci β-catenina pattern se disponibile
               → ANALIZZA
               → segui suggerimento next marker
               → [What If] testa scenari alternativi
```

### Nota sul workflow Cascade → Inverse

Quando si usa "Apri in Ricerca Inversa" dalla Cascade, i marker ND/outsourcing vengono trasferiti come selezionati. Un banner giallo avvisa della loro presenza — non sono selezionabili manualmente in Ricerca Inversa ma influenzano il calcolo.

---

## Limitazioni dichiarate

1. **Probabilità relative al modello**: le percentuali rappresentano il ranking interno tra le 37 entità modellate. Non coprono diagnosi assenti dal database.

2. **Calibrazione empirica**: prior, sensibilità e specificità sono handcrafted, non derivate da coorti validate. Il tool è concepito per orientamento, non per decisione autonoma.

3. **Assenza di classe "altro"**: un caso raro non modellato può produrre un top1 ad alta "robustezza" perché non ha competitors — non perché sia correttamente diagnosticato.

4. **Qualità preanalitica non modellata**: clone anticorpale, fissazione, cutoff, sede bioptica non sono parametri del modello.

5. **`aliasIndex`**: implementato ma non attivo nel flusso corrente. Scaffolding per futura funzionalità di input libero (es. parser `TTF1+, CK7+, CK20-`).

6. **Pattern marker e IG**: il guadagno informativo è calcolato solo per marker binari. β-catenina e futuri pattern marker sono esclusi dall'IG finché non sarà implementato l'IG multi-stato (v3.10).

---

## Changelog

| Versione | Data | Principali modifiche |
|----------|------|----------------------|
| v3.9.4 | Lug 2026 | Ricerca Inversa mobile-friendly: bottoni espliciti **+/−** sui marker disponibili (niente drag&drop né ciclo pos→neg→off ambiguo); tile selezionate con controlli **⇄ inverti** e **✕ rimuovi**; fix scroll-vs-tap (lo scorrimento della lista non attiva più i marker); barra azioni fissa con conteggio POS/NEG live e Analizza/Reset; lista "Disponibili" in cima su mobile; testi adattati a touch. Desktop invariato (drag&drop preservato) |
| v3.9.2 | Giu 2026 | Aggiunte 3 entità CUP-rilevanti: Merkel Cell Carcinoma, Carcinoma Adrenocorticale, Fibromatosi Desmoide; aggiornati TOPOGRAPHIC_PRIORS (cute, tessuti_molli, tubo_digerente, mts_cup) |
| v3.9.1 | Mag 2026 | Bug fix architettura pattern marker: `analyzeMarkers` accetta β-cat da sola; `computeBayes` protetto (pattern mai trattato come binario); `computeInfoGain` esclude pattern; `computeConfidence`/`updateCounts` includono pattern; β-cat sinoviale ricalibrata (w 1.2→0.7, probs 0.30/0.70→0.45/0.55) |
| v3.9.0 | Mag 2026 | Architettura pattern-marker: UI dedicata per β-catenina (membranous/nuclear); `computeBayes` usa `patternProbs` come likelihood diretta; type-system pronto per p53/Ki-67/MMR composito |
| v3.8.3 | Apr 2026 | Next Best dipende da `currentMode`; `computeInfoGain` filtra per modalità UI attiva |
| v3.8.2 | Apr 2026 | `computeInfoGain` include n.i. + pattern nel conteggio tested; loss-marker selezionati fuori modalità sempre inclusi nel calcolo |
| v3.8.1 | Apr 2026 | Helper `getLossState()`; toggle-off (clic su stato attivo → untested); ricalcolo automatico; sincronizzazione select Cascade; contatore loss-marker testati |
| v3.8 | Apr 2026 | UI dedicata loss-marker (retained/lost/n.i.); loss e pattern marker esclusi dai pannelli IHC generici |
| v3.7.1 | Mar 2026 | Etichette leggibili per sedi; blend logaritmico tra prior generale e prior topografico; Step 0 Sede in Cascade |
| v3.7.0 | Mar 2026 | Matrice `TOPOGRAPHIC_PRIORS`; `adjustPriorBySite()`; 11 sedi anatomiche modellate |
| v3.6.2 | Mar 2026 | Testo coerente retained/lost per loss-marker; badge controllo interno confermato |
| v3.6.1 | Mar 2026 | Tracciamento loss-marker con controllo interno positivo; `updateCounts` include loss-marker |
| v3.6.0 | Mar 2026 | IG per loss-marker (P(retained) = 1 − s); etichette semantiche nella UI |
| v3.5.0 | Mar 2026 | Loss-marker in `computeBayes` (retained/lost → LR−/LR+); fix Mesotelioma epitelioide in `adjustMorphology` |
| v3.4.3 | Mar 2026 | Banner ND marker importati da Cascade; rimosso ramo morto `nd` in `displayNextBest()`; allineamento commenti interni |
| v3.4.2 | Mar 2026 | `computeInfoGain()` filtra ND coerentemente con UI; legenda ND nascosta in inverse mode; nota esplicita ND in cascade step 4; "Robustezza del ranking"; disclaimer top-N |
| v3.4.1 | Mar 2026 | Fix `switchTab()` / `cascSelectMorph()` da `event.target`; bonifica 9 ID in `correlatedGroups`; `getSite()` default `'nd'`; `computeConfidence()` composita; flag basata su LR+ |
| v3.4 | Feb 2026 | Motore LR bayesiano; filtro morfologico; classe di confidenza; punteggio criticità; IG pesato; risparmio tessuto; modalità Tumor Board; What If |

---

## Stress test suggeriti

Casi trappola utili per validazione:

| Profilo | Atteso | Trappola |
|---------|--------|----------|
| CK+, CD45−, S100−, Vim−, CK7+, CK20−, TTF1+, Napsina+ | ADK polmonare | vs Ca tiroideo (TTF1 condiviso) |
| CK+, CK7−, CK20−, Heppar+, Arginasi+, Glypican3+ | HCC | vs Yolk sac (Glypican3 condiviso) |
| CD30+, CD15+, CD45−, PAX5 debole+ | Hodgkin classico | vs ALCL (CD30 condiviso) |
| STAT6+, CD34+, BCL2+ | TFS | robustezza alta giustificata? |
| CK+, Vim+, WT1+, Calretinina+, D240+, CEA−, BerEP4− | Mesotelioma | vs Ca ovarico sieroso (PAX8/WT1) |
| CK20+, CK7−, INSM1+ | Merkel Cell Carcinoma | vs ADK colorettale (CK20/CDX2) |
| β-catenina nuclear | Fibromatosi Desmoide | vs Sarcoma Sinoviale (entrambi nuclear-prone) |
| Inibina+, SF1+, Melan-A+, PAX8− | Ca Adrenocorticale | vs Melanoma (Melan-A condiviso) |
| Tutto negativo | — | test classe "altro non modellato" |

---

## Autore e contesto

Sviluppato da Dr. Filippo Bianchi, Direttore f.f. SC Anatomia Patologica  
ASST Fatebenefratelli-Sacco · Presidio FBF-Melloni-Territorio · Milano

Uso didattico e orientativo interno. Non validato per uso clinico autonomo.  
Feedback: `filippo.bianchi@asst-fbf-sacco.it`
