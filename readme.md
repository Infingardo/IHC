# 🧬 IHC Hub v3.4.3

**Motore di supporto alla diagnosi differenziale in Anatomia Patologica**  
Sviluppato per uso interno · SC Anatomia Patologica · ASST Fatebenefratelli-Sacco, Milano

---

## Cosa fa

IHC Hub è uno strumento di orientamento diagnostico basato su inferenza bayesiana applicata al profilo immunoistochimico. Dato un set di marker positivi e negativi, calcola le probabilità posteriori per 33 diagnosi differenziali e suggerisce il prossimo marker con il massimo guadagno informativo.

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

---

## Archivio marker

| Sede | N | Note |
|------|---|------|
| FBF (locale) | 143 | Disponibili internamente |
| SACCO | 77 | Invio al presidio |
| ND / outsourcing | 16 | Non in lista attiva UI |
| **Totale markerDB** | **236** | Inclusi alias e sinonimi |

**33 entità diagnostiche modellate** (carcinomi, linfomi, sarcomi, tumori germinali, NEN, melanoma, mesotelioma, tumori epatici, tiroidei, prostatici, renali).

---

## Workflow consigliato

### Caso nuovo con morfologia definita

```
Cascade → Step 1 (morfologia EE)
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
               → ANALIZZA
               → segui suggerimento next marker
               → [What If] testa scenari alternativi
```

### Nota sul workflow Cascade → Inverse

Quando si usa "Apri in Ricerca Inversa" dalla Cascade, i marker ND/outsourcing vengono trasferiti come selezionati. Un banner giallo avvisa della loro presenza — non sono selezionabili manualmente in Ricerca Inversa ma influenzano il calcolo.

---

## Limitazioni dichiarate

1. **Probabilità relative al modello**: le percentuali rappresentano il ranking interno tra le 33 entità modellate. Non coprono diagnosi assenti dal database.

2. **Calibrazione empirica**: prior, sensibilità e specificità sono handcrafted, non derivate da coorti validate. Il tool è concepito per orientamento, non per decisione autonoma.

3. **Assenza di classe "altro"**: un caso raro non modellato può produrre un top1 ad alta "robustezza" perché non ha competitors — non perché sia correttamente diagnosticato.

4. **Qualità preanalitica non modellata**: clone anticorpale, fissazione, cutoff, sede bioptica non sono parametri del modello.

5. **`aliasIndex`**: implementato ma non attivo nel flusso corrente. Scaffolding per futura funzionalità di input libero (es. parser `TTF1+, CK7+, CK20-`).

---

## Changelog

| Versione | Data | Principali modifiche |
|----------|------|----------------------|
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
| Tutto negativo | — | test classe "altro non modellato" |

---

## Autore e contesto

Sviluppato da Dr. Filippo Bianchi, Direttore f.f. SC Anatomia Patologica  
ASST Fatebenefratelli-Sacco · Presidio FBF-Melloni-Territorio · Milano

Uso didattico e orientativo interno. Non validato per uso clinico autonomo.  
Feedback: `filippo.bianchi@asst-fbf-sacco.it`
