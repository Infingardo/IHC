# PATCH v2.0 → v2.1
## Code Changes Ready-to-Apply

**Date:** 2025-02-06  
**Type:** Evidence-based corrections + NotebookLM integrations  
**Files affected:** `ihc_cascade_v2.html` (JavaScript section)

---

## 🎯 APPLY ORDER

1. getDiagnoses() - 7 fixes
2. getAlerts() - 3 red flags
3. getSuggestions() - 3 additions
4. getGaps() - 6 updates
5. Bibliografia - 12 additions
6. Disclaimer - 1 update

---

## 📝 PATCH 1: getDiagnoses()

### Location: Line ~850 (NKX3.1)

**REPLACE:**
```javascript
if (p('PSA') || p('NKX3')) {
  dx.push({ 
    name: 'Adenocarcinoma prostatico', 
    conf: 'high', 
    detail: 'NKX3.1: sens 80-85% nelle metastasi (NON 98.6% che è nel primitivo), spec 99-100%. Mantiene espressione quando PSA si negativizza [Gurel 2010, Khani 2014].'
  });
}
```

**WITH:**
```javascript
if (p('PSA') || p('NKX3')) {
  dx.push({ 
    name: 'Adenocarcinoma prostatico', 
    conf: 'high', 
    detail: 'NKX3.1: sens 80-85% nelle metastasi (vs 95-100% primitivo), spec 99-100%. Mantiene espressione meglio di PSA. ⚠ Perdita in NE (<20%), post-ADT, alto grado [Gurel 2010, Khani 2014].'
  });
  
  // ⭐ NEW: NKX3.1 negativo warning
  if (n('PSA') && p('NKX3')) {
    dx.push({ 
      name: 'Adenoca prostatico PSA-negativo', 
      conf: 'high', 
      detail: 'NKX3.1+/PSA−: prostata scarsamente diff. o post-terapia. NKX3.1 marker di scelta nei CUP CK7−/CK20− [Gurel 2010].'
    });
  }
}

// ⭐ NEW: Warning NKX3.1−/PSA− non esclude prostata
if (n('PSA') && n('NKX3') && t('PSA') && t('NKX3')) {
  dx.push({ 
    name: 'Esclusione prostata incompleta', 
    conf: 'low', 
    detail: 'PSA−/NKX3.1− in CK7−/CK20− non esclude prostata: ~20% metastasi PSA−, ~15-20% NKX3.1− (post-ADT, alto grado, NE). Morfologia EE critica. Considerare ERG, Prosteina (P501S) se disponibili [Gurel 2010].'
  });
}
```

---

### Location: Line ~890 (Arginasi)

**REPLACE:**
```javascript
if (p('HSA') || p('Arginasi')) {
  dx.push({ 
    name: 'Carcinoma epatocellulare', 
    conf: 'high', 
    detail: 'Arginasi-1: sens 95-96%, spec 96-100% vs cholangioCA/CRC, superiore a HepPar-1 nel scarsamente diff. [Yan 2010]. ⚠ Cross-reattività: mammella ~12%, prostata rara [Karamchandani 2013].'
  });
}
```

**WITH:**
```javascript
if (p('HSA') || p('Arginasi')) {
  dx.push({ 
    name: 'Carcinoma epatocellulare', 
    conf: 'high', 
    detail: 'Arginasi-1: sens 80-96% HCC (53.6% poorly diff. vs HepPar-1 14.3%), spec 96-100% vs cholangioCA/CRC [Yan 2010]. ⚠ Cross-reattività: breast 12.3% (pattern granulare citoplasmatico identico HCC), prostata <10%, CCA raro. Morfologia EE + coerenza clinica essenziali [Karamchandani 2013].'
  });
  
  // ⭐ NEW: HCC GATA3+ vs metastasi breast
  if (p('Arginasi') && p('GATA3') && n('ER')) {
    dx.push({ 
      name: 'HCC GATA3+ (raro) vs Metastasi breast', 
      conf: 'medium', 
      detail: 'Arg+/GATA3+/ER−: Pattern raro. HCC può essere GATA3+ in ~2%. Se ER− e morfologia trabecolare → HCC. Se ER+ o morfologia atipica → metastasi breast Arg+ (12.3%) [Karamchandani 2013].'
    });
  }
}
```

---

### Location: Line ~920 (INSM1 - NEW)

**ADD AFTER existing NE panel:**
```javascript
// ⭐ NEW: S100+/INSM1+ algoritmo
if (p('S100') && p('INSM1')) {
  dx.push({ 
    name: 'S100+/INSM1+: Paraganglioma vs Melanoma vs NEC', 
    conf: 'medium', 
    detail: 'DDx critica: (1) Paraganglioma: CK−, GATA3+, S100 periferico (sustentacolare), nidi Zellballen. (2) Melanoma: SOX10+, Melan-A+, HMB45+, S100 diffuso, INSM1 focale (13%). (3) NEC pigmentato (raro). Morfologia EE essenziale [Rooper 2017].'
  });
}

// ⭐ NEW: Adenocarcinoma prostata con NE
if ((p('PSA') || p('NKX3')) && p('INSM1')) {
  dx.push({ 
    name: 'Adenocarcinoma prostatico con differenziazione NE', 
    conf: 'high', 
    detail: 'PSA+/NKX3.1+/INSM1+: adenoCA prostata con firma NE (36% adenoCA esprimono INSM1, riflette differenziazione NE epigenetica). Pattern INSM1 critico: <em>focale</em> (<30%) = NE subclinica; <em>diffuso</em> (>70%) + small-cell = NEC. Comune post-ADT, alto grado [Rooper 2017].'
  });
}

// ⭐ NEW: NEC prostatico vs altri siti
if (p('INSM1') && n('PSA') && n('NKX3') && t('PSA') && t('NKX3') && (p('Synapt') || p('Cromo'))) {
  dx.push({ 
    name: 'NEC prostatico vs NEC altri siti', 
    conf: 'medium', 
    detail: 'INSM1+/SYN+/PSA−/NKX3.1−: NEC prostatico perde marcatori (sens PSA/NKX3.1 <20% in NEC). DDx: NEC polmone (TTF1+ 90%), NEC GI (CDX2/ISL1). Marcatori terza linea: ERG (30-40% prostata), AR. Morfologia small-cell + sede metastasi (ossee favoriscono prostata) [Rooper 2017].'
  });
}
```

---

## 📝 PATCH 2: getAlerts()

### Location: Line ~1280

**ADD AFTER existing curable alerts:**
```javascript
// ⭐ NEW: RED FLAGS
if (p('PSA') && n('NKX3')) {
  alerts.push({ 
    type: 'redflag', 
    title: '⚠ RED FLAG — PSA+/NKX3.1−', 
    detail: 'Pattern improbabile. PSA sens <50% mets, NKX3.1 mantiene 80-85%. Controllare prelievo/colorazione [Gurel 2010].'
  });
}

if (p('TTF1') && n('Napsina') && n('CK7')) {
  alerts.push({ 
    type: 'redflag', 
    title: '⚠ RED FLAG — TTF1+/Napsina−/CK7−', 
    detail: 'NON polmone. TTF1+ in: tiroide (Thyroglobulina+), endometrio (ER+/PAX8+), neuroblastoma (SYN+) [Park 2007].'
  });
}

if (p('Arginasi') && (p('ER') || p('GATA3'))) {
  alerts.push({ 
    type: 'redflag', 
    title: '⚠ RED FLAG — Arginasi+/GATA3+ o Arginasi+/ER+', 
    detail: 'Pattern sospetto metastasi mammaria Arginasi+ (12.3% breast CA). Morfologia EE critica: se ≠ HCC tipico → metastasi breast. Se = HCC → HCC GATA3+ (2% raro) [Karamchandani 2013].'
  });
}
```

---

## 📝 PATCH 3: getSuggestions()

### Location: Line ~1320

**ADD to suggestions logic:**
```javascript
// ⭐ NEW: NKX3.1 priorità in CK7−/CK20−
if (n('CK7') && n('CK20') && !t('Arginasi') && !t('PSA') && !t('NKX3')) {
  s.push('CK7−/CK20−: aggiungere <code>Arginasi</code>, <code>NKX3.1</code> (priorità su PSA: sens 80-85% mets vs PSA <50%) [SEOM-GECOD, Gurel 2010].');
}

if (n('PSA') && !t('NKX3')) {
  s.push('PSA neg: <code>NKX3.1</code> mandatoria (sens 80-85% mets, spec 99-100%). PSA−/NKX3.1− non esclude prostata: 20% falsi neg (post-ADT, NE, alto grado) [Gurel 2010].');
}

// ⭐ NEW: Arginasi reflex panel
if (p('Arginasi') && !t('ER') && !t('GATA3')) {
  s.push('Arginasi+: se lesione epatica in donna, aggiungere <code>ER</code>, <code>GATA3</code>, <code>Mammoglobin</code> per escludere metastasi breast Arg+ (12.3%) [Karamchandani 2013].');
}

// ⭐ NEW: ERG/AR per NEC CUP
if (p('INSM1') && n('PSA') && n('NKX3') && (p('Synapt') || p('Cromo'))) {
  s.push('NEC PSA−/NKX3.1− in uomo con metastasi ossee: considerare <code>ERG</code> (30-40% prostata TMPRSS2-ERG) o <code>AR</code> per escludere NEC prostatico. TTF1 ambiguo (60% prostata, 90% polmone).');
}
```

---

## 📝 PATCH 4: getGaps()

### Location: Line ~1360

**REPLACE entire gaps block:**
```javascript
function getGaps(panelId) {
  const gaps = [];
  if (panelId === 'carcinoma' || panelId === 'undifferentiated') {
    // ⭐ UPDATED: INSM1 dettagliato
    gaps.push('⚠ <code>INSM1</code> non in FBF. Sens 96.4% NEN (superiore a SYN+CgA+CD56: 87.4%), spec 96.2% [Rooper 2017]. <strong>Falsi+:</strong> melanoma 13%, prostata adenoCA 36% (firma NE epigenetica), sarcomi. <strong>Pattern:</strong> <em>diffuso</em> (>50% NEN), <em>focale</em> (<30% falsi+). TMA >14k: 3.8% non-NE. Attivazione consigliata per biopsie mediastiniche/polmonari.');
    
    // ⭐ NEW: TRPS1
    gaps.push('<code>TRPS1</code> — marcatore breast CA (spec TN), surrogato GCDFP-15/Mammoglobin. Citato PDF CUP 2023. Non disponibile FBF.');
    
    // ⭐ UPDATED: MOC31/Claudina-4
    gaps.push('<code>MOC31</code>/<code>Claudina-4</code> — DDx mesotelioma vs adenoCA. Sens/spec >90% [Ordóñez 2005]. Non disponibili FBF.');
    
    // ⭐ UNCHANGED: PAP
    gaps.push('<code>PAP</code> (prostatic acid phosphatase) — complementare PSA/NKX3.1 [SEOM-GECOD]. Non disponibile FBF.');
    
    // ⭐ NEW: ERG
    gaps.push('<code>ERG</code> — prostata 30-40% (TMPRSS2-ERG). Complementare NKX3.1 in NEC CUP, MA marker endoteliale (cross-reattività tumori vascolari). Non disponibile FBF.');
    
    // ⭐ NEW: Prosteina
    gaps.push('<code>Prosteina (P501S)</code> — sens ~95% prostata, spec ~98%. Superiore PSA in scarsamente diff., mantiene espressione post-ADT. Non disponibile FBF.');
  }
  return gaps;
}
```

---

## 📝 PATCH 5: Bibliografia

### Location: References section in HTML

**ADD these 12 new entries:**
```html
<strong>Organo-specifici:</strong><br>
[9] IASLC — IHC in lung cancer. <em>J Thorac Oncol</em> 2021;16:1107.<br>
[10] Yan BC+ — <strong>Arginase-1</strong> for HCC. <em>Am J Surg Pathol</em> 2010;34:1147. <span style="color:var(--pos)">✓ NEW</span><br>
[11] Gurel B+ — <strong>NKX3.1</strong> in mets. <em>Am J Surg Pathol</em> 2010;34:1097. <strong>(Sens 80.7% mets, NOT 98.6%)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
[12] Khani F+ — NKX3.1 validation. <em>Clin Cancer Res</em> 2014;20:4925. <span style="color:var(--pos)">✓ NEW</span><br>
<br>
<strong>Neuroendocrino:</strong><br>
[13] Rooper LM+ — <strong>INSM1</strong> superior. <em>Am J Surg Pathol</em> 2017;41:1561. <strong>(Sens 96.4%, FP melanoma 13%, prostata 36%)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
[14] Bellizzi AM — NEN site assignment. <em>Arch Pathol Lab Med</em> 2018;142:530.<br>
<br>
<strong>Melanoma:</strong><br>
[15] Voiculescu VM+ — IHC skin cancers. <em>Curr Health Sci J</em> 2025;51:5.<br>
[16] Lezcano C+ — <strong>PRAME</strong> in melanoma. <em>Am J Surg Pathol</em> 2018;42:1456. <strong>(Sens 75%, NEGATIVE spitzoid)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
[17] Gradecki SE+ — PRAME sarcoma. <em>Am J Surg Pathol</em> 2021;45:1249. <span style="color:var(--pos)">✓ NEW</span><br>
<br>
<strong>MMR:</strong><br>
[22] Shia J — IHC vs MSI. <em>J Mol Diagn</em> 2008;10:293. <span style="color:var(--pos)">✓ NEW</span><br>
[23] Haraldsdottir S+ — <strong>MMR deficiency</strong>. <em>Fam Cancer</em> 2014;13:427. <strong>(MLH1 methylation vs Lynch)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
<br>
<strong>GCT:</strong><br>
[24] Zynger DL+ — <strong>SALL4</strong> in GCT. <em>Am J Clin Pathol</em> 2008;129:235. <span style="color:var(--pos)">✓ NEW</span><br>
[25] Cao D+ — SALL4 in adenoCA. <em>Mod Pathol</em> 2009;22:1418. <strong>(10-15% gastric)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
<br>
<strong>Pitfall:</strong><br>
[26] Karamchandani JR+ — <strong>Arginase-1 in breast</strong>. <em>Histopathology</em> 2013;62:804. <strong>(12% positive)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
[27] Agaimy A+ — <strong>CD30+ carcinomas</strong>. <em>Am J Surg Pathol</em> 2012;36:1836. <strong>(Embryonal CA)</strong> <span style="color:var(--pos)">✓ FIX</span><br>
[28] Ordóñez NG — IHC mesothelioma. <em>Am J Clin Pathol</em> 2005;123:202.<br>
```

---

## 📝 PATCH 6: Disclaimer

### Location: Disclaimer section

**REPLACE:**
```html
<div class="disclaimer">
  <strong>⚕ Disclaimer</strong> — Supporto didattico-decisionale per CUP. Non sostituisce giudizio clinico-patologico integrato (morfologia EE, correlazione clinica, molecolare). Accuratezza IHC ~70-80%, scende nei tumori scarsamente differenziati. <strong>Il vetrino non mente, il reagente sì.</strong>
</div>
```

**WITH:**
```html
<div class="disclaimer">
  <strong>⚕ Disclaimer v2.1</strong> — Supporto didattico-decisionale per CUP. Correzioni evidence-based: NKX3.1 80-85% mets (non 98.6%), Arginasi cross-reattività mammella 12%, INSM1 FP melanoma/prostata, PRAME negativo spitzoidi, SALL4 isolato non sempre GCT, MMR pattern-specific. Non sostituisce giudizio clinico-patologico integrato. Accuratezza IHC ~70-80%. <strong>Il vetrino non mente, i dati vanno verificati.</strong>
</div>
```

---

## ✅ VERIFICATION CHECKLIST

After applying patches:

- [ ] Big Four rendering correctly
- [ ] CK7/CK20 panels load properly
- [ ] NKX3.1 diagnosis shows "80-85% mets"
- [ ] Arginasi diagnosis mentions "12.3% breast"
- [ ] INSM1 in gaps shows "melanoma 13%, prostata 36%"
- [ ] Red flags trigger on correct patterns
- [ ] S100+/INSM1+ shows Paraganglioma vs Melanoma
- [ ] Bibliografia shows 28 voci (12 with ✓ NEW or ✓ FIX)
- [ ] Disclaimer shows "v2.1"
- [ ] No JavaScript errors in console

---

## 🔧 TROUBLESHOOTING

### If red flags not showing:
Check `getAlerts()` is called in rendering pipeline and `alertsContainer` exists in HTML.

### If new diagnoses not appearing:
Verify panel IDs match (e.g., 'carcinoma', 'undifferentiated') and marker IDs are correct.

### If gaps text too long:
Reduce gap descriptions or implement collapsible sections.

---

**Patch Version:** 2.1.0  
**Apply Date:** 2025-02-06  
**Estimated Time:** 15-20 minutes  
**Risk Level:** Low (additive changes, no breaking changes)
