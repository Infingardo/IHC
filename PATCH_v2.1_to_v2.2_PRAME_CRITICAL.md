# PATCH CRITICO v2.1 → v2.2
## Correzione PRAME Spitzoidi + Aggiunta Pannello

**Data:** 2025-02-07  
**Type:** CRITICAL FIX - Dato errato spitzoidi + PRAME disponibile FBF  
**Priority:** HIGH  
**Files affected:** `ihc_cascade_v2.1.html` (JavaScript + marker definitions)

---

## 🚨 PROBLEMA IDENTIFICATO

### Errore v2.0-v2.1 (CRITICO):
> "PRAME: sens 75%, **NEGATIVE in spitzoid**"

### Validazione NotebookLM (2025-02-07):
> "**NON è vero** che PRAME è negativo nei melanomi spitzoidi. I **Nevi di Spitz** (benigni) sono negativi (0%), ma i **Melanomi Spitzoidi** (maligni) mostrano positività diffusa. PRAME+ diffuso in tumore spitzoide è **red flag verso malignità**."

### Fonte:
- Lezcano C+ 2018 (Am J Surg Pathol 42:1456)
- Gradecki SE+ 2021 (Am J Surg Pathol 45:1249)

### Impatto Clinico:
⚠️ **ALTO** - Errore può portare a sottovalutazione malignità in melanomi spitzoidi

---

## 🎯 CORREZIONI NECESSARIE

### 1. PRAME disponibile FBF → Spostare da gaps a pannello
### 2. Correggere dato spitzoidi (negative → DDx Nevo/Melanoma)
### 3. Aggiornare sensibilità (75% → 83-94%)
### 4. Aggiungere cross-reattività (sarcoma sinoviale 80-90%, RCC)
### 5. Pattern interpretation (diffuso >50% = malignità)

---

## 📝 PATCH 1: Marker Definitions

### Location: Line ~150 (marker definitions)

**ADD PRAME to marker list:**

```javascript
const markers = [
  // ... existing markers ...
  
  // ⭐ MELANOCYTIC - ADD PRAME
  { id: 'PRAME', name: 'PRAME', cat: 'melanocytic' },
  
  // ... rest of markers ...
];
```

---

## 📝 PATCH 2: Pannello Melanocytic

### Location: Line ~200 (panels definition)

**UPDATE melanocytic panel:**

**REPLACE:**
```javascript
{ 
  id: 'melanocytic', 
  name: 'Pannello Melanocitico', 
  markers: [
    { label: 'First-line', markers: [
      { id: 'S100', name: 'S100' },
      { id: 'SOX10', name: 'SOX10' },
      { id: 'MelanA', name: 'Melan-A' },
      { id: 'HMB45', name: 'HMB-45' },
    ]},
    { label: 'Second-line', markers: [
      { id: 'MITF', name: 'MITF' },
    ]},
  ]
}
```

**WITH:**
```javascript
{ 
  id: 'melanocytic', 
  name: 'Pannello Melanocitico', 
  markers: [
    { label: 'First-line', markers: [
      { id: 'S100', name: 'S100' },
      { id: 'SOX10', name: 'SOX10' },
      { id: 'MelanA', name: 'Melan-A' },
      { id: 'HMB45', name: 'HMB-45' },
      { id: 'PRAME', name: 'PRAME' }, // ⭐ NEW - disponibile FBF
    ]},
    { label: 'Second-line', markers: [
      { id: 'MITF', name: 'MITF' },
    ]},
  ]
}
```

---

## 📝 PATCH 3: getDiagnoses()

### Location: Line ~950 (melanocytic diagnoses)

**ADD after existing melanoma diagnoses:**

```javascript
// ⭐ NEW: PRAME+ melanoma
if (p('S100') && p('SOX10') && p('PRAME')) {
  dx.push({ 
    name: 'Melanoma PRAME+', 
    conf: 'high', 
    detail: 'S100+/SOX10+/PRAME+: melanoma (sens PRAME 83-94%). Pattern PRAME <em>diffuso</em> (>50% cellule) supporta malignità. Melan-A, HMB45 possono perdersi in metastasi. PRAME mantiene espressione [Lezcano 2018].'
  });
}

// ⭐ NEW: DDx critica Nevo Spitz vs Melanoma Spitzoide
if ((p('S100') || p('SOX10')) && t('PRAME')) {
  dx.push({ 
    name: 'DDx Nevo di Spitz vs Melanoma Spitzoide', 
    conf: 'medium', 
    detail: '<strong>PRAME pattern-critical:</strong> (1) <strong>Nevo di Spitz</strong> (benigno): PRAME <em>negativo</em> (0% casi). (2) <strong>Melanoma Spitzoide</strong> (maligno): PRAME <em>positivo diffuso</em> (>50% cellule). ⚠ Pattern PRAME+ diffuso in lesione spitzoide = <strong>red flag malignità</strong>. Morfologia EE (mitosi, atipia citologica, ulcerazione) essenziale per diagnosi finale [Lezcano 2018].'
  });
}

// ⭐ NEW: PRAME+ con cross-reattività
if (p('PRAME') && !p('S100') && !p('SOX10')) {
  dx.push({ 
    name: 'PRAME+ non-melanocitico: Sarcoma vs RCC vs Altri', 
    conf: 'low', 
    detail: 'PRAME+ cross-reattività documentata: (1) <strong>Sarcoma Sinoviale</strong> 80-90% (morfologia bifasica, vasi emangiopericitoidi, traslocazione SS18-SSX). (2) <strong>RCC</strong> (clear cell, cromofobo): check PAX8. (3) <strong>Carcinoma sebaceo</strong> (raro). Pattern PRAME: se <em>diffuso</em> in contesto melanocitico → melanoma; se <em>diffuso</em> + CK+ → sarcoma sinoviale. Morfologia EE + pannello completo essenziali [Gradecki 2021].'
  });
}
```

---

## 📝 PATCH 4: getSuggestions()

### Location: Line ~1340

**ADD after melanocytic suggestions:**

```javascript
// ⭐ NEW: PRAME suggestion per melanoma
if (p('S100') && p('SOX10') && !t('PRAME')) {
  s.push('S100+/SOX10+ melanoma: aggiungere <code>PRAME</code> (sens 83-94%, spec alta vs nevi). Utile DDx: Nevo Spitz (PRAME−) vs Melanoma Spitzoide (PRAME+ diffuso >50%). Pattern diffuso supporta malignità [Lezcano 2018].');
}

// ⭐ NEW: PRAME+ lineage check
if (p('PRAME') && !t('S100') && !t('SOX10')) {
  s.push('PRAME+: verificare lineage. Se <code>CK+</code> → sarcoma sinoviale (80-90% PRAME+). Se <code>PAX8+</code> → RCC. Se <code>S100+/SOX10+</code> → melanoma. Pattern <em>diffuso</em> più specifico che <em>focale</em> [Gradecki 2021].');
}

// ⭐ NEW: Lesione spitzoide workup
if ((p('S100') || p('SOX10')) && p('PRAME')) {
  s.push('Lesione spitzoide PRAME+: Pattern PRAME critico. Se <em>diffuso</em> (>50%) → <strong>red flag melanoma spitzoide</strong>. Se <em>negativo</em> → favorisce nevo Spitz benigno. Morfologia EE (mitosi, ulcerazione) essenziale [Lezcano 2018].');
}
```

---

## 📝 PATCH 5: getGaps()

### Location: Line ~1380

**REMOVE PRAME from gaps (now available):**

**DELETE:**
```javascript
gaps.push('PRAME — Sens 75% melanoma, NEGATIVE spitzoid. Non disponibile FBF.');
```

**REPLACE with note in melanocytic context:**
```javascript
// PRAME ora disponibile FBF - nessun gap
```

---

## 📝 PATCH 6: Bibliografia

### Location: References section

**UPDATE [16] and [17]:**

**REPLACE:**
```html
[16] Lezcano C+ — <strong>PRAME</strong> in melanoma. <em>Am J Surg Pathol</em> 2018;42:1456. 
     <strong>(Sens 75%, NEGATIVE spitzoid)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
[17] Gradecki SE+ — PRAME sarcoma. <em>Am J Surg Pathol</em> 2021;45:1249. 
     <span style="color:var(--pos)">✓ NEW</span><br>
```

**WITH:**
```html
[16] Lezcano C+ — <strong>PRAME</strong> in melanoma. <em>Am J Surg Pathol</em> 2018;42:1456. 
     <strong>(Sens 83-94%. DDx critica: Nevo Spitz [benigno] PRAME <em>negativo</em> 0%, 
     Melanoma Spitzoide [maligno] PRAME <em>positivo diffuso</em> >50%. Pattern diffuso 
     = red flag malignità. Mantiene espressione in metastasi)</strong> 
     <span style="color:var(--warn)">✓ FIX CORRECTED v2.2</span><br>
[17] Gradecki SE+ — PRAME cross-reattività. <em>Am J Surg Pathol</em> 2021;45:1249. 
     <strong>(Sarcoma sinoviale 80-90%, RCC [clear cell/chromo], sebaceo. 
     Pattern diffuso + CK+ → sarcoma vs melanoma)</strong> 
     <span style="color:var(--pos)">✓ NEW v2.2</span><br>
```

---

## 📝 PATCH 7: Disclaimer

### Location: Disclaimer section

**UPDATE version number:**

**REPLACE:**
```html
<strong>⚕ Disclaimer v2.1</strong> — Supporto didattico-decisionale per CUP. 
Correzioni evidence-based: NKX3.1 80-85% mets (non 98.6%), Arginasi 
cross-reattività mammella 12%, INSM1 FP melanoma/prostata, PRAME negativo 
spitzoidi, SALL4 isolato non sempre GCT, MMR pattern-specific.
```

**WITH:**
```html
<strong>⚕ Disclaimer v2.2</strong> — Supporto didattico-decisionale per CUP. 
Correzioni evidence-based: NKX3.1 80-85% mets (non 98.6%), Arginasi 
cross-reattività mammella 12%, INSM1 FP melanoma/prostata, <strong>PRAME DDx 
Nevo Spitz (neg) vs Melanoma Spitzoide (pos diffuso)</strong>, SALL4 isolato 
non sempre GCT, MMR pattern-specific. <strong>PRAME ora disponibile FBF.</strong>
```

---

## 📝 PATCH 8: getAlerts() - Red Flag Pattern PRAME

### Location: Line ~1290 (after other red flags)

**ADD:**

```javascript
// ⭐ NEW: Red flag PRAME+ focale in melanoma
if (p('PRAME') && p('S100') && p('SOX10')) {
  // Note: questo è un "advisory" non un red flag vero, ma utile
  // Solo se vogliamo implementare pattern interpretation warning
  // OPZIONALE - può essere omesso
}

// ⭐ NEW: Red flag PRAME- in lesione spitzoide melanoma-like
if (n('PRAME') && (p('S100') || p('SOX10'))) {
  alerts.push({ 
    type: 'advisory', 
    title: 'ℹ️ ADVISORY — Lesione melanocitica PRAME−', 
    detail: 'Se morfologia spitzoide: PRAME− favorisce <strong>Nevo di Spitz</strong> (benigno). Se morfologia melanoma convenzionale PRAME−: ~10-15% melanomi PRAME-negativi esistono (sensibilità 83-94%, non 100%). Morfologia EE + clinica essenziali [Lezcano 2018].'
  });
}
```

---

## ✅ VERIFICATION CHECKLIST v2.2

After applying patches:

- [ ] PRAME presente in marker definitions
- [ ] PRAME nel pannello melanocytic (first-line)
- [ ] Diagnosi "Melanoma PRAME+" funziona
- [ ] Diagnosi "DDx Nevo Spitz vs Melanoma Spitzoide" appare
- [ ] Diagnosi "PRAME+ cross-reattività" per sarcoma/RCC
- [ ] Suggestion "aggiungere PRAME" per S100+/SOX10+
- [ ] Suggestion "verificare lineage" per PRAME+ senza S100/SOX10
- [ ] PRAME RIMOSSO da gaps (ora disponibile)
- [ ] Bibliografia [16] aggiornata (83-94%, DDx Spitz)
- [ ] Bibliografia [17] dettagliata (cross-reattività)
- [ ] Disclaimer mostra "v2.2"
- [ ] No errori JavaScript console

---

## 🔧 TROUBLESHOOTING

### Se PRAME non appare in pannello:
1. Verifica marker ID `PRAME` in definitions
2. Verifica category `melanocytic`
3. Check panel rendering logic

### Se diagnosi non appaiono:
1. Verifica helper functions `p()`, `n()`, `t()`
2. Check panel context (melanocytic vs altri)
3. Verify marker state management

### Se bibliografia non formattata:
1. Check HTML entity encoding (`<em>`, `<strong>`)
2. Verify CSS classes (var(--warn), var(--pos))

---

## 📊 IMPATTO PATCH v2.2

### Fix Totali: 4/7 → 5/7

| Fix | v2.0 | v2.1 | v2.2 | Status |
|-----|------|------|------|--------|
| NKX3.1 | ❌ | ✅ | ✅ | Validato |
| Arginasi | ❌ | ✅ | ✅ | Validato |
| INSM1 | ❌ | ✅ | ✅ | Validato |
| **PRAME** | **❌ WRONG** | **❌ WRONG** | **✅ CORRECTED** | **FIXED** |
| SALL4 | ✅ | ✅ | ✅ | Da validare |
| CD30 | ✅ | ✅ | ✅ | Da validare |
| MMR | ✅ | ✅ | ✅ | Da validare |

### Marcatori Disponibili FBF

**PRIMA (v2.1):**
- PRAME in gaps (erroneamente "non disponibile")

**DOPO (v2.2):**
- PRAME nel pannello melanocytic ✅
- Diagnosi DDx Spitz complete ✅
- Cross-reattività documentate ✅

---

## 🚨 CRITICITÀ CORRETTA

### Errore Clinico Potenziale (v2.1):
```
Patologo vede: Lesione spitzoide PRAME+ diffuso
Consulta tool v2.1: "PRAME negative in spitzoid"
Conclusione errata: "PRAME non utile, è nevo Spitz"
→ Sottovalutazione melanoma spitzoide
```

### Correzione v2.2:
```
Patologo vede: Lesione spitzoide PRAME+ diffuso
Consulta tool v2.2: "PRAME+ diffuso in spitzoide = RED FLAG malignità"
Conclusione corretta: "Melanoma spitzoide vs Nevo Spitz → melanoma"
→ Diagnosi appropriata
```

**Impact:** 🔴 **HIGH** - Previene potenziale sottodiagnosi melanoma

---

## 📈 METRICHE v2.2

### Marcatori Totali
- v2.1: 45 marcatori
- v2.2: 46 marcatori (+PRAME)

### Pannelli Aggiornati
- Melanocytic: +1 marker (PRAME first-line)

### Diagnosi Aggiunte
- +3 diagnosi PRAME-related

### Suggestions Aggiunte
- +3 suggestions PRAME-related

### Bibliografia
- [16] Lezcano: UPDATED (dettaglio completo)
- [17] Gradecki: UPDATED (cross-reattività)

---

**Patch Version:** 2.2.0  
**Apply Date:** 2025-02-07  
**Estimated Time:** 15 minutes  
**Risk Level:** Low-Medium (new marker + critical fix)  
**Priority:** HIGH (correzione dato errato + marker disponibile)

---

**READY TO APPLY** ✅
