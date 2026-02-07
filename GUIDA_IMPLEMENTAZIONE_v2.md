# IHC Cascade v2.0 — GUIDA IMPLEMENTAZIONE
## Fix Pratici per il Codice JavaScript

---

## 🎯 Come Applicare le Correzioni

### File originale: `index.html`
### File aggiornato: `ihc_cascade_v2.html`

---

## 📝 CORREZIONE #1: NKX3.1 sensibilità metastasi

**Localizzazione:** Funzione `getDiagnoses()`, linea ~850

### PRIMA (ERRATO):
```javascript
if (p('PSA') || p('NKX3')) {
  dx.push({ 
    name: 'Adenocarcinoma prostatico', 
    conf: 'high', 
    detail: 'NKX3.1: sens 98.6%, spec 99-100%. Mantiene espressione quando PSA si negativizza.'
  });
}
```

### DOPO (CORRETTO):
```javascript
if (p('PSA') || p('NKX3')) {
  dx.push({ 
    name: 'Adenocarcinoma prostatico', 
    conf: 'high', 
    detail: 'NKX3.1: sens 80-85% nelle metastasi (NON 98.6% che è nel primitivo), spec 99-100%. Mantiene espressione quando PSA si negativizza [Gurel 2010, Khani 2014].'
  });
  if (n('PSA') && p('NKX3')) {
    dx.push({ 
      name: 'Adenoca prostatico PSA-negativo', 
      conf: 'high', 
      detail: 'NKX3.1+/PSA−: prostata scarsamente diff. o post-terapia. Marker di scelta nei CUP CK7−/CK20− [Gurel 2010].'
    });
  }
}
```

**Bibliografia aggiunta:**
```javascript
// In sezione riferimenti
[11] Gurel B+ — NKX3.1 in mets. Am J Surg Pathol 2010;34:1097. (Sens 80.7% mets).
[12] Khani F+ — NKX3.1 expression. Clin Cancer Res 2014;20:4925.
```

---

## 📝 CORREZIONE #2: Arginasi-1 cross-reattività

**Localizzazione:** Funzione `getDiagnoses()`, linea ~890

### PRIMA (INCOMPLETO):
```javascript
if (p('HSA') || p('Arginasi')) {
  dx.push({ 
    name: 'Carcinoma epatocellulare', 
    conf: 'high', 
    detail: 'Arginasi-1: sens 95-96%, spec 96-100% vs metastasi/colangiocarcinoma, superiore a HepPar-1.'
  });
}
```

### DOPO (COMPLETO):
```javascript
if (p('HSA') || p('Arginasi')) {
  dx.push({ 
    name: 'Carcinoma epatocellulare', 
    conf: 'high', 
    detail: 'Arginasi-1: sens 95-96%, spec 96-100% vs cholangioCA/metastasi CRC, superiore a HepPar-1 nel scarsamente diff. [Yan 2010]. ⚠ Cross-reattività: mammella ~12%, prostata rara [Karamchandani 2013].'
  });
  
  // AGGIUNGI questo check
  if (p('Arginasi') && !p('NKX3') && !p('ER') && t('NKX3')) {
    dx.push({ 
      name: 'HCC confermato (NKX3.1 negativo)', 
      conf: 'high', 
      detail: 'Arginasi+ con NKX3.1−: esclude prostata. Valutare ER per mammella se morfologia atipica.'
    });
  }
}
```

**Bibliografia aggiunta:**
```javascript
[10] Yan BC+ — Arginase-1 for HCC. Am J Surg Pathol 2010;34:1147.
[26] Karamchandani JR+ — Arginase-1 in breast CA. Histopathology 2013;62:804. (12%).
```

---

## 📝 CORREZIONE #3: SALL4 isolato (non sempre GCT)

**Localizzazione:** Funzione `getDiagnoses()`, linea ~920

### AGGIUNGI questo blocco PRIMA del check GCT classico:

```javascript
// === GERM CELL ===
if (p('SALL4') || p('OCT34') || p('PLAP') || p('AFP') || p('HCG')) {
  
  // ⭐ NUOVO: Check SALL4 isolato
  if (p('SALL4') && !p('OCT34') && !p('AFP') && !p('HCG') && !p('PLAP')) {
    dx.push({ 
      name: 'SALL4+ isolato — NON GCT', 
      conf: 'medium', 
      detail: 'SALL4 senza OCT3-4/AFP/HCG/PLAP: carcinoma gastrico primitivo (~10-15%), polmonare (<5%), endometriale [Cao 2009]. Morfologia adenocarcinomatosa → NON trattare come GCT.'
    });
  } else {
    // GCT confermato con panel completo
    dx.push({ 
      name: '⚠ Tumore a cellule germinali', 
      conf: 'high', 
      detail: 'SUBSET CURABILE — chemioterapia tipo BEP, altamente efficace. Non trattare come CUP [SEOM-GECOD, ESMO 2023, Zynger 2008].'
    });
    // ... resto diagnostica GCT
  }
}
```

**Bibliografia aggiunta:**
```javascript
[24] Zynger DL+ — SALL4 in extragonadal GCT. Am J Clin Pathol 2008;129:235.
[25] Cao D+ — SALL4 in adenoCA. Mod Pathol 2009;22:1418. (10-15% gastric).
```

---

## 📝 CORREZIONE #4: CD30 in carcinoma embrionale

**Localizzazione:** Funzione `getDiagnoses()`, panel carcinoma, linea ~935

### AGGIUNGI questo check nel blocco GCT:

```javascript
if (p('HCG')) {
  dx.push({ 
    name: 'Coriocarcinoma (componente)', 
    conf: 'high', 
    detail: 'βHCG+: coriocarcinoma o componente coriocarcinomatosa [Zynger 2008].'
  });
}

// ⭐ NUOVO: CD30 in GCT
if (p('CD30') && (p('SALL4') || p('AFP'))) {
  dx.push({ 
    name: 'Carcinoma embrionale', 
    conf: 'high', 
    detail: 'CD30+/SALL4+/AFP±: carcinoma embrionale (GCT). NON ALCL [Agaimy 2012].'
  });
}
```

**Bibliografia aggiunta:**
```javascript
[27] Agaimy A+ — CD30+ carcinomas. Am J Surg Pathol 2012;36:1836.
```

---

## 📝 CORREZIONE #5: MMR pattern-specific

**Localizzazione:** Funzione `getDiagnoses()`, linea ~1050

### PRIMA (GENERICO):
```javascript
if (n('MLH1') || n('MSH2') || n('MSH6') || n('PMS2')) {
  let lost = [];
  if (n('MLH1')) lost.push('MLH1');
  if (n('MSH2')) lost.push('MSH2');
  if (n('MSH6')) lost.push('MSH6');
  if (n('PMS2')) lost.push('PMS2');
  dx.push({ 
    name: '⚠ Deficit MMR — ' + lost.join('/'), 
    conf: 'high', 
    detail: 'MSI-H. Immunoterapia (anti-PD1). MLH1 loss → escludere metilazione promotore.'
  });
}
```

### DOPO (SPECIFICO):
```javascript
if (n('MLH1') || n('MSH2') || n('MSH6') || n('PMS2')) {
  let lost = [];
  if (n('MLH1')) lost.push('MLH1');
  if (n('MSH2')) lost.push('MSH2');
  if (n('MSH6')) lost.push('MSH6');
  if (n('PMS2')) lost.push('PMS2');
  const pattern = lost.join('/');
  
  // ⭐ NUOVO: Pattern-specific counseling
  if (pattern === 'MLH1/PMS2') {
    dx.push({ 
      name: '⚠ Deficit MMR — MLH1/PMS2 loss', 
      conf: 'high', 
      detail: 'MSI-H. Se CRC/gastrico: test metilazione MLH1 e BRAF V600E per Lynch vs sporadico. Se wild-type/non metilato → Lynch. Immunoterapia anti-PD1 [Shia 2008, Haraldsdottir 2014].'
    });
  } else if (pattern === 'MSH2/MSH6' || pattern === 'MSH6' || pattern === 'PMS2') {
    dx.push({ 
      name: '⚠ Deficit MMR — ' + pattern + ' loss (Lynch)', 
      conf: 'high', 
      detail: 'MSI-H. MSH2/MSH6 o MSH6 o PMS2 isolato → sempre Lynch syndrome. Consulenza genetica. Immunoterapia anti-PD1 [Shia 2008, Haraldsdottir 2014].'
    });
  } else {
    dx.push({ 
      name: '⚠ Deficit MMR — ' + pattern, 
      conf: 'high', 
      detail: 'MSI-H. Immunoterapia (anti-PD1). Approfondire con genetica [Shia 2008].'
    });
  }
}
```

**Bibliografia aggiunta:**
```javascript
[22] Shia J — IHC vs MSI testing. J Mol Diagn 2008;10:293.
[23] Haraldsdottir S+ — MMR deficiency. Fam Cancer 2014;13:427.
```

---

## 📝 CORREZIONE #6: PRAME limitazioni

**Localizzazione:** Panel melanocytic, linea ~1200

### PRIMA:
```javascript
if (p('PRAME')) {
  dx.push({ 
    name: 'Melanoma (PRAME+)', 
    conf: 'high', 
    detail: 'PRAME+: sens ~75%, spec ~95% per melanoma vs nevo.'
  });
}
```

### DOPO:
```javascript
if (p('PRAME')) {
  dx.push({ 
    name: 'Melanoma (PRAME+)', 
    conf: 'high', 
    detail: 'PRAME+: sens ~75%, spec ~95% per melanoma vs nevo. ⚠ NEGATIVO in melanomi spitzoidi. Rara positività RCC (~25-30%) [Lezcano 2018, Gradecki 2021].'
  });
}

// ⭐ NUOVO: PRAME negativo warning
if (!p('PRAME') && t('PRAME') && p('MelanA')) {
  dx.push({ 
    name: 'Melanoma PRAME-negativo', 
    conf: 'medium', 
    detail: 'PRAME− con marcatori melanocitici+: considerare melanoma spitzoide se giovane/dermico [Lezcano 2018].'
  });
}
```

**Bibliografia aggiunta:**
```javascript
[16] Lezcano C+ — PRAME in melanoma. Am J Surg Pathol 2018;42:1456.
[17] Gradecki SE+ — PRAME in sarcoma. Am J Surg Pathol 2021;45:1249.
```

---

## 🚨 CORREZIONE #7: RED FLAGS (nuova funzione)

**Localizzazione:** Funzione `getAlerts()`, linea ~1280

### AGGIUNGI questi check:

```javascript
function getAlerts() {
  const sl = state.panel;
  const p = (id) => sl[id] === '+';
  const n = (id) => sl[id] === '-';
  const alerts = [];
  
  // Curabili (GCT, NE, SCC) — già presenti
  if (p('SALL4') && (p('OCT34') || p('AFP') || p('HCG'))) {
    alerts.push({ 
      type: 'curable', 
      title: '⚠ SUBSET POTENZIALMENTE CURABILE — GCT', 
      detail: 'GCT extragonadico: BEP, altamente curativo. Non trattare come CUP [SEOM-GECOD, Zynger 2008].'
    });
  }
  
  // ⭐ NUOVO: RED FLAGS
  if (p('PSA') && n('NKX3')) {
    alerts.push({ 
      type: 'redflag', 
      title: '⚠ RED FLAG — PSA+/NKX3.1−', 
      detail: 'Pattern improbabile. PSA sens <50% in mets, NKX3.1 mantiene 80-85%. Controllare prelievo/colorazione [Gurel 2010].'
    });
  }
  
  if (p('TTF1') && n('Napsina') && n('CK7')) {
    alerts.push({ 
      type: 'redflag', 
      title: '⚠ RED FLAG — TTF1+/Napsina−/CK7−', 
      detail: 'NON polmone. TTF1+ in: tiroide (Thyroglobulina+), endometrio (ER+/PAX8+), neuroblastoma (SYN+) [Park 2007].'
    });
  }
  
  if (p('Arginasi') && (p('NKX3') || p('ER'))) {
    alerts.push({ 
      type: 'redflag', 
      title: '⚠ RED FLAG — Arginasi+ con NKX3.1+ o ER+', 
      detail: 'Arginasi cross-reattività: mammella 12%, prostata rara. Se NKX3.1+ → prostata (Arginasi falso+). Se ER+ → mammella (Arginasi falso+) [Karamchandani 2013].'
    });
  }
  
  return alerts;
}
```

**CSS aggiuntivo per red flags:**
```css
.alert-box.redflag {
  background: var(--orange-bg);
  border: 1px solid var(--orange-border);
}
.alert-box.redflag .alert-title {
  color: var(--orange);
  font-weight: 700;
  margin-bottom: 2px;
}
.alert-box.redflag .alert-detail {
  color: var(--text-dim);
  font-size: 0.78rem;
}
```

---

## 📝 CORREZIONE #8: getSuggestions() update

**Localizzazione:** Funzione `getSuggestions()`, linea ~1320

### AGGIUNGI:

```javascript
function getSuggestions(panelId) {
  const sl = state.panel;
  const p = (id) => sl[id] === '+';
  const n = (id) => sl[id] === '-';
  const t = (id) => sl[id] === '+' || sl[id] === '-';
  const s = [];

  if (panelId === 'carcinoma') {
    if (!t('CK7') || !t('CK20')) {
      s.push('<code>CK7</code> e <code>CK20</code> come primo step CUP [SEOM-GECOD].');
    }
    
    // ⭐ AGGIORNATO: NKX3.1 priorità
    if (n('CK7') && n('CK20') && !t('Arginasi') && !t('PSA') && !t('NKX3')) {
      s.push('CK7−/CK20−: aggiungere <code>Arginasi</code>, <code>NKX3.1</code> (priorità su PSA) [SEOM-GECOD, Gurel 2010].');
    }
    
    if (n('PSA') && !t('NKX3')) {
      s.push('PSA neg: <code>NKX3.1</code> mandatoria (sens 80-85% mets, spec 99-100%) [Gurel 2010].');
    }
    
    // ⭐ NUOVO: Arginasi + HepPar-1 combo
    if (p('HSA') && !t('Arginasi')) {
      s.push('HepPar-1+: aggiungere <code>Arginasi-1</code> (superiore nel scarsamente diff.) [Yan 2010].');
    }
    
    // ⭐ NUOVO: SALL4 isolato → panel completo
    if (p('SALL4') && !t('OCT34') && !t('AFP') && !t('HCG')) {
      s.push('SALL4+ isolato: <code>OCT3-4</code>, <code>AFP</code>, <code>HCG</code> per conferma GCT vs carcinoma [Cao 2009].');
    }
    
    // ... resto suggestions
  }
  
  return s;
}
```

---

## 📝 CORREZIONE #9: getGaps() precisato

**Localizzazione:** Funzione `getGaps()`, linea ~1360

### PRIMA:
```javascript
function getGaps(panelId) {
  const gaps = [];
  if (panelId === 'carcinoma' || panelId === 'undifferentiated') {
    gaps.push('⚠ <code>INSM1</code> non in pannello FBF. Sens 96,4% nei NEN vs 87,4% del pannello SYN+CgA+CD56.');
    gaps.push('<code>MOC31</code>/<code>Claudina-4</code> — utili nel DDx mesotelioma vs adenocarcinoma.');
    gaps.push('<code>PAP</code> — complementare a PSA/NKX3.1.');
  }
  return gaps;
}
```

### DOPO:
```javascript
function getGaps(panelId) {
  const gaps = [];
  if (panelId === 'carcinoma' || panelId === 'undifferentiated') {
    gaps.push('⚠ <code>INSM1</code> non in FBF. Sens 96.4% NEN (Rooper 2017), MA falsi positivi melanoma ~15%, prostata ~35%. TMA >14.000: 89% NEN, 3.5% non-NE. Considerare attivazione per piccole biopsie polmonari/mediastiniche [Rooper 2017].');
    
    gaps.push('<code>MOC31</code>/<code>Claudina-4</code> — DDx mesotelioma vs adenoCA. Sens/spec >90% in studi validation. Non in pannello FBF [Ordóñez 2005].');
    
    gaps.push('<code>PAP</code> (prostatic acid phosphatase) — complementare PSA/NKX3.1 nel pannello SEOM-GECOD. Sens ~80% metastasi ossee [SEOM-GECOD].');
  }
  return gaps;
}
```

---

## 📚 Bibliografia Completa da Aggiungere

### In sezione `<details class="refs">`:

```html
<details class="refs">
  <summary>📚 Bibliografia v2.0 (28 voci, 12 aggiunte)</summary>
  <p style="max-height:350px;overflow-y:auto;padding-right:8px">
    <strong>Guidelines CUP:</strong><br>
    [1] Losa F+ — SEOM-GECOD 2022. Clin Transl Oncol 24:1548.<br>
    [2] Kramer A+ — ESMO CUP 2023. Ann Oncol 34:228.<br>
    [3] Bochtler T+ — Histopathology 2023;83:309.<br>
    [4] Zhao T+ — Front Oncol 2025;14:1345543.<br>
    [5] Greco FA — J Clin Oncol 2024;42:563.<br>
    [6] Fizazi K+ — Oncologist 2021;26:e769.<br>
    <br>
    <strong>IHC generale:</strong><br>
    [7] Park SY+ — Arch Pathol Lab Med 2007;131:1561.<br>
    [8] Jayagopal D+ — Bioinformation 2025;21:1.<br>
    <br>
    <strong>Organo-specifici:</strong><br>
    [9] IASLC — J Thorac Oncol 2021;16:1107.<br>
    [10] Yan BC+ — Arginase-1. Am J Surg Pathol 2010;34:1147. <span style="color:#16a34a">✓ NEW</span><br>
    [11] Gurel B+ — NKX3.1 mets. Am J Surg Pathol 2010;34:1097. <strong>(80.7% NOT 98.6%)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    [12] Khani F+ — Clin Cancer Res 2014;20:4925. <span style="color:#16a34a">✓ NEW</span><br>
    <br>
    <strong>Neuroendocrino:</strong><br>
    [13] Rooper LM+ — INSM1. Am J Surg Pathol 2017;41:1561. <strong>(FP melanoma 15%, prostata 35%)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    [14] Bellizzi AM — Arch Pathol Lab Med 2018;142:530.<br>
    <br>
    <strong>Melanoma:</strong><br>
    [15] Voiculescu VM+ — Curr Health Sci J 2025;51:5.<br>
    [16] Lezcano C+ — PRAME. Am J Surg Pathol 2018;42:1456. <strong>(Neg spitzoid)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    [17] Gradecki SE+ — Am J Surg Pathol 2021;45:1249. <span style="color:#16a34a">✓ NEW</span><br>
    <br>
    <strong>Sarcomi:</strong><br>
    [18] Wakefield CJ+ — Surg Pathol Clin 2024;17:1.<br>
    [19] Miettinen M+ — Histopathology 2021;78:146.<br>
    <br>
    <strong>Emolinfoproliferative:</strong><br>
    [20] WHO 5th ed. 2024.<br>
    [21] Hans CP+ — Blood 2004;103:275.<br>
    <br>
    <strong>MMR:</strong><br>
    [22] Shia J — J Mol Diagn 2008;10:293. <span style="color:#16a34a">✓ NEW</span><br>
    [23] Haraldsdottir S+ — Fam Cancer 2014;13:427. <strong>(MLH1 methylation vs Lynch)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    <br>
    <strong>GCT:</strong><br>
    [24] Zynger DL+ — Am J Clin Pathol 2008;129:235. <span style="color:#16a34a">✓ NEW</span><br>
    [25] Cao D+ — Mod Pathol 2009;22:1418. <strong>(10-15% gastric)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    <br>
    <strong>Pitfall:</strong><br>
    [26] Karamchandani JR+ — Histopathology 2013;62:804. <strong>(Arginasi 12% breast)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    [27] Agaimy A+ — Am J Surg Pathol 2012;36:1836. <strong>(CD30+ embryonal CA)</strong> <span style="color:#16a34a">✓ FIX</span><br>
    [28] Ordóñez NG — Am J Clin Pathol 2005;123:202.<br>
  </p>
</details>
```

---

## ✅ Checklist Implementazione

- [ ] Correggi sensibilità NKX3.1 (98.6% → 80-85% mets)
- [ ] Aggiungi cross-reattività Arginasi (mammella 12%)
- [ ] Implementa check SALL4 isolato
- [ ] Aggiungi CD30 in carcinoma embrionale
- [ ] Pattern-specific MMR (MLH1 methylation vs Lynch)
- [ ] PRAME limitazioni (negativo spitzoidi)
- [ ] RED FLAGS (PSA+/NKX3−, TTF1+/Napsina−/CK7−, Arginasi+/NKX3+)
- [ ] Update getSuggestions (NKX3.1 priorità)
- [ ] Update getGaps (INSM1 falsi positivi)
- [ ] Bibliografia 28 voci (12 nuove)
- [ ] Test funzionale tutti i percorsi diagnostici

---

## 🔬 Testing Scenarios

### Scenario 1: CUP CK7−/CK20− in giovane maschio
**Input:** CK7−, CK20−, PSA−, NKX3.1+
**Output atteso:** "Adenoca prostatico PSA-negativo" (HIGH) + "NKX3.1 marker di scelta"

### Scenario 2: CUP con Arginasi+ e ER+
**Input:** CK7+, CK20−, Arginasi+, ER+
**Output atteso:** RED FLAG "Arginasi cross-reattività mammella"

### Scenario 3: SALL4+ isolato adenocarcinoma
**Input:** SALL4+, OCT34−, AFP−, HCG−
**Output atteso:** "SALL4+ isolato — NON GCT" + Suggestion "panel GCT completo"

### Scenario 4: MMR MLH1/PMS2 loss colorettale
**Input:** CDX2+, SATB2+, MLH1−, PMS2−
**Output atteso:** "Test metilazione MLH1 e BRAF V600E per Lynch vs sporadico"

### Scenario 5: S100+ giovane PRAME−
**Input:** S100+, MelanA+, HMB45+, PRAME−, età <40
**Output atteso:** "Melanoma PRAME-negativo" + "considerare spitzoide"

---

**Version:** 2.0.0  
**Validation:** Pending clinical correlation FBF 2024-2025  
**Last Update:** 2025-02-06
