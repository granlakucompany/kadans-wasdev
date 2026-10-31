# KADANS WASDEV SKILLS FOR VIDEO
## Gid Inivèsèl 201 Skills & Efè Slash Commands pou AI Video Engine (Kadans & Gemini)

Fichye sa a se referans ofisyèl ak bibliyotèk santral tout **Skills & Efè Kadans** ke yon devlopè oswa itilizatè ka enjekte dirèkteman nan Chat AI a lè l ap kreye yon videyo.

---

## 1. PRENSIP FONKSYÒNMAN AK RÈG OBLIGATWA POU AI (PROMPT STACKING)

Lè yon devlopè ap kreye yon videyo ak **Kadans** oswa **Gemini** nan WASDEV, li ka chwazi youn oswa anpile plizyè kòmand slash devan demann li an nan chat la :

### Egzanp Anpileman Kòmand (Prompt Stacking) :
```text
/videostudiopro /effectdocumentary /effectglasswidget /effectchecklist /effectaudiowaveform /effectcinematic
Mwen vle yon videyo 45 segonn ki prezante nouvo modil lojisyèl WASDEV la, ak vwa Kreyòl pwofesyonèl, mizik espwa ak yon CTA final.
```

### RÈG STRIK POU TOUT AJAN AI (CLAUDE, GEMINI, ANTIGRAVITY, OPENAI/CODEX, CURSOR, TOUT LÒT) — OBLIGATWA, SAN EKSEPSYON :
1. **Ide devlopè a se LWA a** : tèks devlopè a ekri apre (oswa ant) slash yo = KONTNI videyo a (istwa, mesaj, tèks, non, pri, dire, lang, vwa, fòma). AI a DWE swiv li EGZAKTEMAN: pa chanje istwa a, pa ajoute ni retire mesaj, pa chanje dire / fòma / non / chif yo, pa envante enfòmasyon.
2. **Skills yo se FÒM nan** : chak slash = yon fason pou fè videyo a (stil, efè, tranzisyon, son). AI a DWE aplike CHAK skill jan katalòg sa a di l la — valè Kadans egzak yo (`transition`, `sfx`, `sounds`, `speed`, `motion_blur`, sèn `html`…), dire yo, son yo. Li entèdi pou ranplase yon skill pa yon lòt "ki sanble", oswa sote youn.
3. **Slash nenpòt kote nan mesaj la** : yon skill konte menm si l nan mitan oswa nan fen mesaj la, pa sèlman nan kòmansman.
4. **Pa ajoute skills ki pa mande** : AI a pa dwe mete lòt efè/tranzisyon/son ki kontredi skills devlopè a chwazi yo. Si yon detay pa presize, chwazi sa ki an amoni ak skills yo.
5. **Prèv nan spec.json (obligatwa)** :
   - Anlè spec la : `"skills": ["/zoomin", "/soundhot", …]` = TOUT skills devlopè a mete yo, san manke youn.
   - Sou chak sèn kote yon skill aplike : `"skills": ["/zoomin"]`.
   - Chak skill anlè a DWE parèt omwen sou yon sèn. `was_video_lint` verifye sa: yon skill ki manke = erè, videyo a PA pare.
6. **Rapò final (obligatwa)** : nan fen repons lan, yon tablo `Skill | Sèn / lè | Kijan li aplike (valè Kadans)` pou CHAK skill. Si yon skill pa t ka aplike, di sa klèman ak rezon an — pa janm kache l.
7. **Koyerans Estetik** : tout efè anpile yo dwe konbine avèk amoni nan menm pwojè videyo a san konfli grafik.
8. **Respekte Règ Kadans Santral la** :
   - Fichye videyo final la dwe pwòp, 60 FPS, san okenn bar play anba (sèlman bèl ikòn play nan mitan an lè se lekti).
   - Tout tèks dwe vrè tèks HTML/SVG editab, pa imaj rasterize.
   - AI a pa rann videyo a: li louvri l nan Kadans Timeline pou devlopè a gade l.

---

## 2. REPATISYON TOUT 201 KADANS SKILLS PA KATEGORI

| Kategori | Kantite | Deskripsyon |
|---|---|---|
| **A. Mod-Estidyo & Fòma Reyalizasyon** | 10 Skills (001–010) | Estil jeneral reyalizasyon (Studio Pro, Cinema, Documentary, Reel, elatriye). |
| **B. Efè Vizyèl, UI & Glass Widgets** | 15 Skills (011–025) | Glassmorphism, checklist, orbite 3D, frames aparèy, kat enfòmasyon. |
| **C. Animasyon Tipografik & Tèks Sinetik** | 12 Skills (026–037) | Kinetic text, typewriter, gradient text, mo ki limen ak vwa, neon text. |
| **D. Patikil, Anbyans & Efè Espesyal** | 12 Skills (038–049) | Dife, lafimen, eklabousi, lapli Matrix, lens flare, cyberpunk, cosmic. |
| **E. Mouvman Kamera & Dinamik Espas** | 12 Skills (050–061) | Dolly zoom, sekous kamera, paralaks 2.5D, crash zoom, panoramic sweep. |
| **F. Tranzisyon Kadans Pro** | 10 Skills (062–071) | Seamless zoom, morphing, ink bleed, glitch wipe, flash white, radial blur. |
| **G. Son, Odyo & Ritm Synchro** | 10 Skills (072–081) | Audio waveform, beat drop, sub-bass hit, whoosh, ducking vwa otomatik. |
| **H. Animasyon Pèsonaj & Rigging** | 10 Skills (082–091) | Stickman SVG Rig 16 zo, Cut-out 2D, lipsync vwa, emodji 3D, gesture men. |
| **I. Seksyon Naratif & Estrikti Story** | 10 Skills (092–101) | Hook punch 3s, problem-solution, feature carousel, pricing, CTA final. |
| **J. Motion Design & Motion Graphics** | 25 Skills (102–126) | Motion design pro, morphism, shape layers, logo reveal, done anime, UI motion, bouk. |
| **K. Piblisite & Pub Pwofesyonèl** | 25 Skills (127–151) | /pubstore, /zoommap, pwodwi hero, manje, imobilye, flash sale, spot TV 30 s, bumper 6 s, jingle. |
| **L. Tranzisyon Vizyèl & Tranzisyon Son** | 50 Skills (152–201) | /zoomin, /zoomout, /spiral, /whippan, /glitchcut, /shatter… + /soundhot, /soundepic, /soundtyping, /soundriser, /sounddrop… |

---

## 3. KATALÒG DETAYE TOUT 201 SKILLS AK ENSTRIKSYON OBLIGATWA POU AI

### KATEGORI A : MOD-ESTIDYO & FÒMA REYALIZASYON (001–010)

#### 001. `/videostudiopro` — Pwodiksyon Estidyo Pwofesyonèl
- **Wòl** : Mete videyo a nan yon nivo estidyo emisyon televizyon kalite wo.
- **Konpozisyon Kadans** : Ekleraj 3 pwen (Key light, Fill light, Rim light mòv), lonbraj dous `box-shadow: 0 30px 60px rgba(0,0,0,0.5)`, mikwo-refleksyon sou eleman yo, tit animasyon sinetik 60 FPS, kalibrasyon koulè pwofesyonèl.
- **Obligasyon AI** : Enjekte klas `.studio-pro` nan `spec.json` ak CSS avanse pou gradyasyon koulè, ankadreman rafine ak tit santre avèk espas respirasyon laj.

#### 002. `/effectdocumentary` — Estil Dokimantè Sinematik
- **Wòl** : Kreye yon anbyans dokimantè pwofon (kalite Netflix / National Geographic).
- **Konpozisyon Kadans** : Efè Ken Burns (zoom dousman 1.05x sou 6 segonn sou imaj ak achiv), tipografi serif oswa grotesk elegant, ton koulè cho ak kontras kalme, tit anba adwat ak dat/lye.
- **Obligasyon AI** : Tout imaj dwe gen animasyon `ken-burns` dousman, vwa a dwe gen espas silans natirèl ant fraz yo, epi anbyans son dwe trankil ak reverbyasyon sibtil.

#### 003. `/effectcinema` — Sinematik Anamòfik 21:9
- **Wòl** : Rann videyo a tankou yon vrè fim sinema gran ekran.
- **Konpozisyon Kadans** : Rapò anamòfik 2.39:1 ak lèt-boks nwa anwo ak anba, frekans 24 FPS oswa 60 FPS lis, degradasyon koulè Teal & Orange (`#0284c7` nan lonbraj, `#f97316` nan limyè), grain fim 35mm lejè.
- **Obligasyon AI** : Ajoute kouch `.cinematic-letterbox`, filtè koulè sinema ak mouvman kamera dousman san chanjman brital.

#### 004. `/effectcommercial` — Piblisite Pwodwi Enpak Rapid
- **Wòl** : Estrikti piblisite pèsonèl oswa pwodwi ki kaptive epi ki konvèti vit.
- **Konpozisyon Kadans** : Ritm rapid (1.5 a 2.5 segonn pa sèn), gwo tit ki frape, koulè mak dinamik, demonstrasyon pwodwi ak zoom rapid, CTA klere nan fen an.
- **Obligasyon AI** : Sèn yo dwe kout, fraz yo dirèk san pèdi tan, chak plan dwe gen yon mouvman vizyèl kontinyèl.

#### 005. `/effectsocialreel` — Fòma Vètikal 9:16 (Shorts, Reels, TikTok)
- **Wòl** : Optimize videyo a pou konsomasyon mobil vètikal.
- **Konpozisyon Kadans** : Rezolisyon 1080x1920 (9:16), zòn sekirite santral (evite bouton like ak kòmantè sou kote yo), gwo sou-tit dinamik nan mitan an, animasyon rapid ki kenbe je a.
- **Obligasyon AI** : Fòse `ratio: "9:16"` nan spec la, pozisyone tout eleman kle yo ant 20% ak 80% wotè ekran an.

#### 006. `/effectexplainer` — Videyo Eksplikatif & Didaktik
- **Wòl** : Esplike yon sistèm konplèks, yon lide oswa yon aplikasyon yon fason fasil.
- **Konpozisyon Kadans** : Fon pwòp net, ikon vektoryèl SVG k ap parèt etap pa etap, flèch k ap konekte konsèp yo, bwat rezime k ap mete pwen kle yo an valè.
- **Obligasyon AI** : Sèvi ak animasyon `.draw-path` sou liy koneksyon yo, gwoupe lide yo an blòk 1, 2, 3 klè.

#### 007. `/effectnewsroom` — Jounal Televizyon & Flash Enfòmasyon
- **Wòl** : Bay videyo a aparans yon gwo chanèl nouvèl an dirèk.
- **Konpozisyon Kadans** : Bann anba k ap defile kontinyèlman (News Ticker), badj `FLASH INFO` oswa `LIVE` ki bat an wouj, fenèt doub (Split Screen) pou entèvyou.
- **Obligasyon AI** : Mete bann defilan `.news-ticker-bar` ak tèks k ap pase de dwat a goch, badj revèy ak tit aktyalite anba a.

#### 008. `/effectpodcastclip` — Ekstrè Podkas ak Vizyalizasyon Odyo
- **Wòl** : Transfòme yon konvèsasyon odyo an yon videyo sosyal vivan.
- **Konpozisyon Kadans** : Foto oswa videyo oratè yo nan kad won oswa vè ma, fòm onn odyo k ap danse nan mitan ekran an, sou-tit k ap chanje koulè mo pa mo.
- **Obligasyon AI** : Entegre `.audio-waveform-canvas`, mete non chak oratè ak tit epizòd la an bèl ankadreman.

#### 009. `/effecttutorialpro` — Demonstrasyon Lojisyèl ak Gid Etap pa Etap
- **Wòl** : Montre kouman pou itilize yon lojisyèl oswa yon sistèm avèk presizyon.
- **Konpozisyon Kadans** : Ekran lojisyèl la an gwo, kurseur sourit anime k ap deplase epi klike avèk yon ti halo jòn/ble, zoom sou zòn kote aksyon an ap fèt.
- **Obligasyon AI** : Ajoute eleman `.cursor-pointer` ak animasyon `translate` ak `scale(0.9)` sou klik yo, ak yon bwat eksplikasyon bò kote l.

#### 010. `/effectproductshowcase` — Prezantasyon Pwodwi 3D ak Wotasyon
- **Wòl** : Mete yon pwodwi fizik oswa yon bwat lojisyèl an valè nan tout ang li yo.
- **Konpozisyon Kadans** : Objè a santre k ap vire dousman nan yon espas 3D (`transform: rotateY()`), refleksyon limyè k ap glise sou sifas li, pwen enfòmasyon (hotspots) ki klere toutotou l.
- **Obligasyon AI** : Sèvi ak pèspektif CSS 3D (`perspective: 1200px`), limyè gradyan sou objè a, ak liy ki mennen sou espesifikasyon teknik yo.

---

### KATEGORI B : EFÈ VIZYÈL, UI & GLASS WIDGETS (011–025)

#### 011. `/effectglasswidget` — Bwat Vè Frosted (Glassmorphism)
- **Wòl** : Bay tout bwat enfòmasyon aparans vè transparan modèn.
- **Konpozisyon Kadans** : `background: rgba(255, 255, 255, 0.07)`, `backdrop-filter: blur(25px)`, bodi `1px solid rgba(255, 255, 255, 0.18)`, lonbraj difize `0 20px 40px rgba(0,0,0,0.37)`.
- **Obligasyon AI** : Vlope kat ak seksyon yo nan klas `.glass-card` ak refleksyon limyè blan sou kwen anwo a.

#### 012. `/effectchecklist` — Lis Travay Animasyon ak Tcheke Otomatik
- **Wòl** : Montre yon seri objektif ki valide youn apre lòt.
- **Konpozisyon Kadans** : Chak ranje parèt soti anba, kaz la koche ak yon animasyon vèt vivan (`#10b981`), yon ti liy vèt k ap trase kòch la (`✓`), ak tèks la ki pran yon ti klète siksè.
- **Obligasyon AI** : Kreye eleman `.checklist-item` kote chak liy gen yon delè animasyon sekansyèl (`delay: index * 0.4s`).

#### 013. `/effectorbit` — Eleman k ap Vire an Wonn Otou yon Nwayo 3D
- **Wòl** : Senbolize yon ekosistèm, satelit, teknoloji ki konekte ansanm.
- **Konpozisyon Kadans** : Yon nwayo santral (logo oswa pwodwi) ak 3 a 6 ikon oswa ti kat k ap vire sou yon sèk eliptik an 3D ak pwofondè Z.
- **Obligasyon AI** : Entegre `.orbit-container` ak animasyon `keyframes orbit3d` kote gwosè ak transparans eleman yo varye selon si yo devan oswa dèyè nwayo a.

#### 014. `/effectisometric3d` — Vi Izometrik 3D ak Kouch Anpile
- **Wòl** : Montre achitekti lojisyèl, nivo sekirite oswa kouch done an 3D.
- **Konpozisyon Kadans** : `transform: rotateX(60deg) rotateZ(-45deg)`, plan ki separe nan lè a ak espas wotè Z (`translateZ(40px)`), lonbraj anba chak plan.
- **Obligasyon AI** : Desine 3 a 4 kouch izometrik ki monte soti nan baz la pou montre kijan sistèm nan konstwi.

#### 015. `/effectdeviceframe` — Kadreyaj Telefòn oswa Laptop Reyalis
- **Wòl** : Montre yon aplikasyon web oswa mobil andedan yon vrè aparèy.
- **Konpozisyon Kadans** : Mokap iPhone 16 Pro oswa MacBook Pro ak rebò metalik, refleksyon ekran, ak videyo/sit web la k ap defile andedan ekran aparèy la.
- **Obligasyon AI** : Mete ankadreman `.device-mockup` ak kouch ekran ki koupe kòrèkteman (`overflow: hidden; border-radius: 40px`).

#### 016. `/effectdatabubbles` — Ti Boul Done ki Flote ak Chif
- **Wòl** : Bay enpresyon yon sistèm entèlijan k ap trete enfòmasyon an tan reyèl.
- **Konpozisyon Kadans** : Ti esfè oswa pilil luminesan k ap flote monte dousman ak ti balanse, chak gen yon done chif (egz: `+45%`, `99.9%`, `4K`, `AI`).
- **Obligasyon AI** : Jenere patikil `.data-bubble` ak animasyon floteman natirèl `sine` ak vitès diferan.

#### 017. `/effectcardstack` — Pil Kat k ap Glise Youn Apre Lòt
- **Wòl** : Montre plizyè temwayaj, karakteristik oswa imaj ki defile tankou kat jwèt.
- **Konpozisyon Kadans** : 3 kat anpile an bwat pèspektif, premye kat la glise sou kote oswa anwo pou kite plas pou dezyèm nan.
- **Obligasyon AI** : Sèvi ak tranzisyon `translateY` ak `rotate` dinamik pou kreye yon efè fizik natirèl.

#### 018. `/effecttimelineprog` — Ba Kwonolojik Etap pa Etap
- **Wòl** : Montre evolisyon yon pwojè, yon wout (roadmap), oswa etap yon pwosesis.
- **Konpozisyon Kadans** : Liy lumineux ki trase de goch a dwat oswa dewo anba, chak ne (node) limen lè liy lan rive sou li ak dat oswa tit etap la.
- **Obligasyon AI** : Entegre `.timeline-track` ak yon ba pwogrè `.timeline-fill` ki grandi soti nan 0% rive 100%.

#### 019. `/effectglowbadge` — Badj Luminesan ak Kwen k ap Klere
- **Wòl** : Mete aksan sou yon mo kle tankou «NOUVO», «OFISYÈL», «PREMIUM», «PRO».
- **Konpozisyon Kadans** : Ti etikèt ak kontou néon k ap voye yon limyè pulsant (`box-shadow: 0 0 20px var(--neon-color)`), tèks an majiskil gras.
- **Obligasyon AI** : Mete badj `.badge-glow` ak animasyon `pulse-glow` 2 segonn enfini sou eleman prensipal la.

#### 020. `/effectstatscounter` — Chif Statistik k ap Monte Vit
- **Wòl** : Bay prèv rezilta enpresyonan ak chif k ap defile soti nan 0 rive nan valè final la.
- **Konpozisyon Kadans** : Chif jeyan ki konte rapidman pandan 1.5 segonn ak efè ralentisman nan fen an (ease-out), senbòl `%`, `+`, oswa `$` ki parèt an koulè vivan.
- **Obligasyon AI** : Sèvi ak script konte WAAPI oswa sekans chif Kadans pou senkronize monte chif la ak yon ti son klik.

#### 021. `/effectnotifalert` — Notifikasyon Mobil / Desktop k ap Desann
- **Wòl** : Simile yon mesaj enpòtan, yon lavant, oswa yon alèt sistèm.
- **Konpozisyon Kadans** : Ti bwat notifikasyon rektangilè vè ma ki desann soti nan tèt ekran an ak yon ti rebondisman elastik, ikòn aplikasyon, non, tèks, ak lè.
- **Obligasyon AI** : Kreye `.notification-popup` ak animasyon `cubic-bezier(0.175, 0.885, 0.32, 1.275)` pou rebondisman an.

#### 022. `/effectsearchbar` — Ba Rechèch ak Tèks k ap Tape Poukont Li
- **Wòl** : Poze yon kesyon ke kliyan an ap poze sou entènèt oswa montre yon rechèch solisyon.
- **Konpozisyon Kadans** : Ba rechèch pwòp ak loup, tèks la tape lèt pa lèt ak kurseur k ap bat, bouton chèche ki klike epi rezilta a ki parèt anba a.
- **Obligasyon AI** : Sèvi ak sekans `.typing-input` ak delè pou chak lèt, epi yon tranzisyon ouvèti rezilta imedyat.

#### 023. `/effectcomparecards` — Kat Konparatif Anvan / Apre ak Splitter
- **Wòl** : Montre diferans radikal ant ansyen metòd la ak nouvo solisyon WASDEV la.
- **Konpozisyon Kadans** : De kat bò kote (Wouj / Vèt oswa Gri / Koulè), oswa yon sèl imaj ak yon liy vertikal k ap glise nan mitan an pou devwale amelyorasyon an.
- **Obligasyon AI** : Kreye konparezon klè avèk ikon `✗` pou ansyen pwoblèm yo ak `✓` pou nouvo solisyon yo.

#### 024. `/effectpiechart3d` — Graf Bar ak Kamambè Anime
- **Wòl** : Vizyalize done mache, pousantaj benefis oswa pèfòmans.
- **Konpozisyon Kadans** : Bar graf k ap monte soti anba tè ak diferan koulè, oswa sèk kamambè SVG k ap trase zòn pa li ak etikèt k ap flote.
- **Obligasyon AI** : Desine graf la ak SVG `stroke-dasharray` anime soti nan 0 jiska valè pousantaj la.

#### 025. `/effectmatrixgrid` — Kadriyaj Teknik ak Kowòdone Futuriste
- **Wòl** : Bay yon santiman teknoloji segondè, kòd avanse, oswa sistèm defans.
- **Konpozisyon Kadans** : Kadriyaj liy amann cyan oswa vèt sou fon nwa, ti pwen entèseksyon k ap klere, kowòdone chif k ap defile sou bò yo.
- **Obligasyon AI** : Ajoute kouch `.tech-grid-overlay` ak pèspektif k ap glise an dousman sou aks Y la.

---

### KATEGORI C : ANIMASYON TIPOGRAFIK & TÈKS SINETIK (026–037)

#### 026. `/effectkinetictext` — Tèks Sinetik Eksplozif sou Ritm
- **Wòl** : Fè chak mo parèt ak yon enèji fò ki kole ak ritm mizik la.
- **Konpozisyon Kadans** : Mo yo sote, elaji, vire, ak chanje pwa (Light -> Black 900) nan chak tan mizik la.
- **Obligasyon AI** : Dekoupe tèks la mo pa mo, aplike animasyon `scale` ak `rotation` sekansyèl rapid.

#### 027. `/effecttypewriter` — Machin a Tape Mekanik
- **Wòl** : Ekri tèks tankou yon rapò konfidansyèl, yon tèminal kòd, oswa yon istwa k ap ekri.
- **Konpozisyon Kadans** : Lèt yo parèt youn apre lòt a vitès fiks (~40ms pa lèt), ak yon kurseur rektangilè nwa/vèt k ap bat nan fen fraz la.
- **Obligasyon AI** : Sèvi ak sekans `.char-reveal` ak son klik klavye senkronize.

#### 028. `/effecttextgradient` — Tèks ak Degradasyon Koulè Aurora k ap Deplase
- **Wòl** : Bay gwo tit yo yon bote ekstraòdinè ak likid koulè k ap koule anndan lèt yo.
- **Konpozisyon Kadans** : `background: linear-gradient(135deg, #10b981, #0098ff, #ec4899, #8b5cf6)`, `background-clip: text`, `-webkit-text-fill-color: transparent`, animasyon `background-position` 8 segonn.
- **Obligasyon AI** : Aplike klas `.gradient-text-animated` sou tout gwo tit prensipal yo.

#### 029. `/effectmaskedtext` — Tèks Devwale pa Mask Jeyometrik
- **Wòl** : Fè tèks la monte soti anba yon liy envizib san l pa debòde.
- **Konpozisyon Kadans** : Yon veso ki gen `overflow: hidden`, kote tèks la monte soti nan `translateY(100%)` rive nan `translateY(0)` avèk yon mouvman ultra-lis.
- **Obligasyon AI** : Vlope chak liy tèks nan yon baliz `.mask-container` pou yon aparisyon pwòp san debòdman.

#### 030. `/effectwordhighlight` — Mo k ap Limen an Tan Reyèl ak Vwa a (Karaoke Pro)
- **Wòl** : Gide je odyans lan sou chak mo egzakteman lè oratè a ap pwononse l.
- **Konpozisyon Kadans** : Tout fraz la parèt an gri klè, epi chak mo limen an jòn vivan, vèt oswa ble depi vwa a rive sou li (baze sou timestamp Whisper).
- **Obligasyon AI** : Itilize done `.words.json` pou aplike klas `.active-word` nan milisegonn egzak la.

#### 031. `/effect3dtextfloat` — Gwo Tèks 3D k ap Flote nan Lè a
- **Wòl** : Kreye yon santiman pouvwa ak pwa fizik pou tit kle yo.
- **Konpozisyon Kadans** : Tèks ak plizyè kouch lonbraj `text-shadow` ki kreye yon epesè 3D reyalis, k ap vire dousman nan yon espas 3D.
- **Obligasyon AI** : Ajoute `text-shadow: 0 1px 0 #ccc, 0 2px 0 #c9c9c9, 0 3px 0 #bbb, 0 4px 0 #b9b9b9, 0 10px 20px rgba(0,0,0,0.4)` ak wotasyon 3D.

#### 032. `/effectneontext` — Tèks Néon k ap Tranble (Flicker) epi Klere
- **Wòl** : Anbyans lari lannwit, vil futurist oswa estil retro-wave.
- **Konpozisyon Kadans** : Koulè woz, cyan oswa zoranj ak gwo lonbraj luminezon, ak yon ti tranbleman (flicker) nan kòmansman kòmsi se yon tib gaz ki fèk limen.
- **Obligasyon AI** : Aplike `@keyframes neon-flicker` ak lonbraj miltip `text-shadow: 0 0 10px, 0 0 20px, 0 0 40px`.

#### 033. `/effectglitchtext` — Tèks Dijital Dechire (RGB Split)
- **Wòl** : Sèn hacking, kòd sekirite, alèt sistèm oswa aksyon teknolojik fò.
- **Konpozisyon Kadans** : Tèks la divize an de kopi (wouj ak cyan) ki dekale orizontalman pandan kèk milisegonn ak tranch liy orizontal.
- **Obligasyon AI** : Sèvi ak pseudoclasses `::before` ak `::after` ak `clip-path` pou kreye tranch glitch la.

#### 034. `/effectoutlinetext` — Tèks Kontou Sèlman ki Ranpli apre
- **Wòl** : Estil tipografi mòd oswa achitekti minimòm trè tandans.
- **Konpozisyon Kadans** : Tèks la kòmanse ak kontou sèlman `-webkit-text-stroke: 2px white` san koulè anndan, epi koulè a monte soti anba tankou likid pou ranpli l.
- **Obligasyon AI** : Anime ranpli koulè a ak yon gradyasyon de ba an wo sou 1 segonn.

#### 035. `/effectflipboard` — Lèt Mekanik k ap Vire (Pano Ayewopò)
- **Wòl** : Chanje yon mo pou yon lòt avèk yon efè mekanik satisfè.
- **Konpozisyon Kadans** : Chak lèt divize an de mwatye ki pliye an 3D soti anwo desann pou devwale nouvo lèt la.
- **Obligasyon AI** : Kreye veso `.flip-char` ak wotasyon `rotateX(-90deg)` sekansyèl sou chak karaktè.

#### 036. `/effectsupersize` — Mo Jeyan nan Background Dèyè Sijè a
- **Wòl** : Bay pwofondè sèn nan ak yon mo jeyan ki kouche dèyè karaktè a oswa pwodwi a.
- **Konpozisyon Kadans** : Tèks gwosè 200px a 300px ak transparans 10% k ap deplase dousman nan direksyon opoze kamera a.
- **Obligasyon AI** : Pozisyone tèks la ak `z-index: 1`, opasite `0.08`, ak mouvman paralaks kontinyèl.

#### 037. `/effectstampbold` — Mo ki Tonbe Tankou yon So ak Sekous
- **Wòl** : Konfime yon desizyon, yon verite, oswa yon viktwa («GARANTI», «APWOUVE», «SÈTIFYE»).
- **Konpozisyon Kadans** : Mo a kòmanse gwo anpil ak transparans zewo, li tonbe rapidman ak yon ti sekous sou tout ekran an ak yon son enpak lou.
- **Obligasyon AI** : Aplike animasyon `scale(3) -> scale(1)` ak `camerashake` 0.2 segonn sou enpak la.

---

### KATEGORI D : PATIKIL, ANBYANS & EFÈ ESPESYAL (038–049)

#### 038. `/effectparticles` — Pousyè Zetwal & Etensèl k ap Flote
- **Wòl** : Bay sèn nan lavi ak yon sans majik oswa teknoloji kalm.
- **Konpozisyon Kadans** : 40 a 60 ti patikil luminesan blan ak mòv k ap monte dousman ak mouvman Brownien sou Canvas 2D.
- **Obligasyon AI** : Entegre kouch Canvas `.particles-canvas` an aryè-plan san chaje CPU a.

#### 039. `/effectsmoke` — Lafimen Dans & Vapè Reyalis
- **Wòl** : Kreye mistè, pwofondè dramatik oswa anbyans sèn konsè.
- **Konpozisyon Kadans** : Kouch lafimen mou k ap defile soti anba monte anwo avèk modèl fractal ak melanj `mix-blend-mode: screen`.
- **Obligasyon AI** : Ajoute kouch `.smoke-overlay` ak animasyon flou ak opasite dousman.

#### 040. `/effectsplashemboss` — Eklabousi Likid ak Lank
- **Wòl** : Tranzisyon enèjik oswa prezantasyon atistik ak penti/likid ki pete.
- **Konpozisyon Kadans** : SVG likid ki fòme ti gout dlo oswa tach lank ki elaji rapidman soti nan pwen santral la.
- **Obligasyon AI** : Entegre fòm `.splash-blob` ak fizik elastik k ap louvri sèn nan.

#### 041. `/effectcyberpunkcity` — Vil Lannwit ak Limyè Néon
- **Wòl** : Anbyans segondè-teknoloji lannwit ak limyè woz ak ble syèl.
- **Konpozisyon Kadans** : Fon somb nwa/ble maren, refleksyon sou tè mouye, reyon néon vètikal, liy kouran k ap pase nan lè a.
- **Obligasyon AI** : Melanje koulè `#ec4899` ak `#0098ff` nan tout lonbraj ak limyè yo.

#### 042. `/effectmatrixrain` — Lapli Kòd Vètikal Matrix
- **Wòl** : Transmèt kòd, algoritm, oswa sekirite k ap kouri nan background.
- **Konpozisyon Kadans** : Kolòn karaktè katakana oswa alfanimerik vèt k ap desann sou fon nwa ak ti ke luminesan.
- **Obligasyon AI** : Entegre Canvas `.matrix-rain` ak karaktè vèt `#10b981` ak tèt blan luminesan.

#### 043. `/effectlightrays` — Reyon Solèy Volimetrik (God Rays)
- **Wòl** : Bay yon sans espwa, grandè, siksè oswa klète espirityèl.
- **Konpozisyon Kadans** : Faiso limyè an kòn k ap soti anwo adwat oswa agòch k ap travèse tout sèn nan avèk pousyè limyè ladan yo.
- **Obligasyon AI** : Ajoute kouch `.volumetric-rays` ak `mix-blend-mode: color-dodge` ak animasyon wotasyon mikwo.

#### 044. `/effectfireflare` — Flit Limyè Optik (Lens Flare Anamòfik)
- **Wòl** : Ajoute yon manyen sinematik reyalis lè kamera a vire fas a yon sous limyè.
- **Konpozisyon Kadans** : Liy orizontal ble anamòfik ak ti sèk luminezon ki travèse ekran an lè kamera a deplase.
- **Obligasyon AI** : Aplike `.anamorphic-flare` ki glise orizontalman pandan tranzisyon sèn yo.

#### 045. `/effectspacecosmos` — Galaksi, Nebulèz & Lespas Pwofon
- **Wòl** : Pou pwojè vizyonè, misyon gwo dimansyon, oswa lavni.
- **Konpozisyon Kadans** : Fon zetwal k ap klere, nebulèz mòv ak ble k ap vire dousman, zetwal filant k ap travèse ekran an detanzantan.
- **Obligasyon AI** : Kreye pwofondè 3 kouch zetwal (ti, mwayen, gwo) k ap deplase a diferan vitès.

#### 046. `/effectglitchcyber` — Bri Siyal & Scanlines Televizyon Katodik
- **Wòl** : Sèn entèripsyon, chòk, kase ritm oswa anbyans retro-future.
- **Konpozisyon Kadans** : Liy orizontal scanlines, ti bri nèj televizyon, desinkronizasyon vètikal pandan 0.3 segonn.
- **Obligasyon AI** : Aplike kouch `.crt-scanlines` ak ti vibrasyon vètikal rapid.

#### 047. `/effectbokehglow` — Rondèl Limyè Flou (Bokeh f/1.4)
- **Wòl** : Anbyans cho, entim, pwofesyonèl ak pwofondè chan foto prim.
- **Konpozisyon Kadans** : Ti sèk limyè flou k ap monte dousman nan aryè-plan ak koulè pastèl cho.
- **Obligasyon AI** : Kreye rondèl `.bokeh-orb` ak `filter: blur(12px)` ak opasite varyab.

#### 048. `/effectshockwave` — Ond de Chòk Sikilè sou Enpak
- **Wòl** : Akantye yon gwo moman, yon anons eksplozif oswa yon desizyon kle.
- **Konpozisyon Kadans** : Yon sèk transparan ki elaji trè vit soti nan mitan ekran an ak yon ti distosyon sou imaj ki dèyè l la.
- **Obligasyon AI** : Anime `.shockwave-ring` ak `transform: scale(0) -> scale(4)` ak opasite ki disparèt nan 0.4s.

#### 049. `/effectembersfire` — Etensèl Dife Wouj-Oranj k ap Vole
- **Wòl** : Bay pasyon, pouvwa, chalè dife ak aksyon entans.
- **Konpozisyon Kadans** : Ti etensèl dife wouj, jòn ak oranj k ap monte nan lè a tankou soti nan yon bwa dife oswa yon fòj.
- **Obligasyon AI** : Entegre patikil dife `.fire-embers` ak flit limyè cho sou kwen anba ekran an.

---

### KATEGORI E : MOUVMAN KAMERA & DINAMIK ESPAS (050–061)

#### 050. `/effectdollyzoom` — Efè Vertigo Hitchcock
- **Wòl** : Kreye yon santiman chòk sikolojik oswa yon gwo realizasyon.
- **Konpozisyon Kadans** : Kamera a rkile pandan l ap zoom devan sou sijè a : sijè a rete menm gwosè a men tout background nan detire epi vin pi lwen.
- **Obligasyon AI** : Konbine `scale()` sou sijè a nan direksyon envès ak `scale()` background nan.

#### 051. `/effectcamerashake` — Sekous Dinamik Kamera
- **Wòl** : Simile yon enpak fizik, yon tranbleman tè, oswa yon kout bas mizik lou.
- **Konpozisyon Kadans** : Kamera a vibre sou aks X ak Y pandan 0.2 a 0.5 segonn ak yon dekonpozisyon rapid (decay).
- **Obligasyon AI** : Aplike `@keyframes camera-shake` ak `transform: translate(random, random)` sou tout veso prensipal la.

#### 052. `/effectparallaxdepth` — Paralaks 2.5D Kouch pa Kouch
- **Wòl** : Transfòme yon imaj plat oswa yon ilistrasyon an yon vrè mond 3D ak pwofondè.
- **Konpozisyon Kadans** : Premye plan deplase vit, plan mwayen deplase a vitès nòmal, ak background deplase trè dousman lè kamera a vire.
- **Obligasyon AI** : Separe eleman yo an 3 kouch `.layer-fg`, `.layer-mg`, `.layer-bg` ak koefisyan vitès diferan.

#### 053. `/effectpanoramicsweep` — Baleyaj Panoramik Laj
- **Wòl** : Montre grandè yon pwojè, yon biwo, yon peyizaj oswa yon ekip konplè.
- **Konpozisyon Kadans** : Kamera a glise fiks de goch a dwat sou yon gwo konpozisyon laj (ultra-wide canvas) avèk vitès konstan ak ralantisman nan fen an.
- **Obligasyon AI** : Anime `translateX()` sou gwo veso a pandan 4 a 6 segonn.

#### 054. `/effectcrashzoom` — Zoom Eklè sou yon Detay
- **Wòl** : Pase soti nan yon plan jeneral pou ateri britalman sou yon ti detay kle (yon bouton, yon figi, yon kòd).
- **Konpozisyon Kadans** : Zoom 1x a 4x nan mwens pase 0.4 segonn avèk yon ti flou mouvman (motion blur).
- **Obligasyon AI** : Aplike `scale(4)` ak `transform-origin` egzakteman sou kowòdone eleman sib la.

#### 055. `/effectorbitcam` — Kamera k ap Vire Toutotou Sijè a
- **Wòl** : Prezantasyon dinamik yon karaktè oswa yon pwodwi pandan l rete santre.
- **Konpozisyon Kadans** : Kamera a fè yon wonn 180° oswa 360° otou sijè a pandan limyè a ap chanje bò sou sifas li.
- **Obligasyon AI** : Sèvi ak pèspektif 3D santre ak animasyon `rotateY` kontinyèl.

#### 056. `/effectfirstperson` — Vi Premye Pèsòn (POV)
- **Wòl** : Mete espektatè a nan soulye itilizatè a oswa pèsonaj prensipal la.
- **Konpozisyon Kadans** : Ti balansman natirèl mach moun (head bobbing), men ki parèt anba ekran an pou klike oswa manyen objè yo.
- **Obligasyon AI** : Ajoute ti mouvman wotasyon zewo-pwen-de degre ak deplasman Y vètikal nan ritm mach.

#### 057. `/effectdroneflyover` — Plan Vòl Dwòn soti nan Syèl la
- **Wòl** : Entwodiksyon mayifik ki desann soti nan nwaj yo pou ateri sou sijè a.
- **Konpozisyon Kadans** : Kamera anlè k ap gade anba pandan l ap desann epi redrese ang li pou vin orizontal devan pwojè a.
- **Obligasyon AI** : Konbine `translateY`, `rotateX(45deg) -> rotateX(0)` ak zoom dousman.

#### 058. `/effecttiltshift` — Efè Makèt Minyati
- **Wòl** : Fè yon vrè vil oswa yon gwo machin parèt tankou yon ti makèt jwèt sou yon tab.
- **Konpozisyon Kadans** : Yon bann etwat nan mitan ekran an ki trè nèt, pandan tout anwo ak anba a flou anpil, ak koulè ki satire plis.
- **Obligasyon AI** : Aplike mask flou vètikal ak saturation koulè `saturate(1.4)`.

#### 059. `/effectwhipcamera` — Kout Kamera Rapid (Whip Pan)
- **Wòl** : Tranzisyon enèjik ant de aksyon kote kamera a vire tèlman vit ke tout bagay vin flou.
- **Konpozisyon Kadans** : Yon kout baleyaj orizontal 0.2 segonn ak gwo flou direksyonèl `blur(30px, 0px)` ki ateri sou nouvo sèn nan.
- **Obligasyon AI** : Entegre klas `.whip-pan-transition` ant de sèn yo.

#### 060. `/effectcameraroll` — Wotasyon Kamera sou Aks li
- **Wòl** : Sèn aksyon ekstrèm, espas, oswa moman kote tout bagay tounen tèt anba.
- **Konpozisyon Kadans** : Kamera a vire 180° oswa 360° sou aks Z pandan aksyon an ap kontinye jwe nan mitan an.
- **Obligasyon AI** : Anime `rotateZ()` avèk yon ritm rapid nan mitan epi kalm nan fen an.

#### 061. `/effectslowmotion` — Ralanti Ekstrèm (Slow-Mo 120 FPS)
- **Wòl** : Dekonpoze yon ti aksyon rapid (yon ti gout dlo, yon souri, yon kout kòd) pou montre bote li.
- **Konpozisyon Kadans** : Aksyon an jwe a 25% vitès nòmal li ak lisidite total 60 FPS san sakad.
- **Obligasyon AI** : Elaji dire sèn nan nan spec la epi ralanti tout animasyon WAAPI yo pa 4x.

---

### KATEGORI F : TRANZISYON KADANS PRO (062–071)

#### 062. `/effectseamlesszoom` — Tranzisyon Zoom Enfini
- **Wòl** : Kamera antre anndan yon lèt, yon fenèt oswa yon je nan premye sèn nan pou vin tout background dezyèm sèn nan.
- **Konpozisyon Kadans** : Zoom 1x -> 50x sou yon pwen presi jiskaske koulè pwen sa a ranpli tout ekran an pou revele pwochen sèn nan.
- **Obligasyon AI** : Senkronize pwen disparisyon premye sèn nan ak pwen ouvèti dezyèm sèn nan.

#### 063. `/effectmorphshape` — Transfòmasyon Fòm Likid (Morphing)
- **Wòl** : Yon logo ki tounen yon bouton, oswa yon ikon ki fonn pou vin yon lòt fòm.
- **Konpozisyon Kadans** : SVG path k ap transfòme kowòdone li yo dousman soti nan fòm A rive nan fòm B avèk menm kantite pwen vektoryèl.
- **Obligasyon AI** : Sèvi ak animasyon SVG morphing sou chemen vektè yo.

#### 064. `/effectinkbleed` — Tach Lank k ap Gaye sou Papye
- **Wòl** : Tranzisyon natirèl, atistik oswa istorik kote lank nwa/koulè devwale sèn nan.
- **Konpozisyon Kadans** : Mask SVG ki elaji ak fòm iregilye tankou dlo ki tonbe sou papye siya pou louvri imaj la.
- **Obligasyon AI** : Aplike mask `mask-image` ak fòm likid k ap elaji soti nan sant la.

#### 065. `/effectglitchwipe` — Dechire Dijital pou Chanje Sèn
- **Wòl** : Chanje sèn tankou yon siyal satelit ki koupe epi ki rekonekte imedyatman.
- **Konpozisyon Kadans** : Premye sèn nan kraze an blòk piksèl orizontal pandan 0.2 segonn epi dezyèm sèn nan monte san pwoblèm.
- **Obligasyon AI** : Entegre tranzisyon `.glitch-wipe` ak son bri elektwonik kout.

#### 066. `/effectflashwhite` — Flash Blan Enèjik
- **Wòl** : Makè yon chanjman tan enpòtan oswa yon revelasyon gwo enpak.
- **Konpozisyon Kadans** : Ekran an vin blan total pandan 3 frames (~50ms) epi li fonn rapidman pou montre nouvo sèn nan.
- **Obligasyon AI** : Mete yon kouch blan `.flash-overlay` ak tranzisyon `opacity: 1 -> 0` nan 0.3s.

#### 067. `/effectdooropen` — Ouvèti Pòt oswa Rido soti nan Mitan
- **Wòl** : Entwodui yon nouvo chapit oswa akeyi odyans lan anndan yon nouvo espas.
- **Konpozisyon Kadans** : De panno vè ma oswa nwa k ap glise sou kote (goch ak dwat) soti nan liy mitan an.
- **Obligasyon AI** : Kreye de panno `.split-door-left` ak `.split-door-right` ak animasyon `translateX`.

#### 068. `/effectpapertear` — Papye ki Chire nan Mitan an
- **Wòl** : Kase yon ansyen règ, retire yon ansyen kontra, oswa revele verite a ki kache dèyè.
- **Konpozisyon Kadans** : Liy chire iregilye ki desann soti anwo rive anba, ak de moso papye yo ki louvri sou kote ak son chire.
- **Obligasyon AI** : Entegre mask SVG ak rebò chire reyalis ak lonbraj anba chak moso.

#### 069. `/effectblurzoom` — Flou Radyal Rapid
- **Wòl** : Chanje sèn nan yon fraksyon segonn san je a pa gen tan wè kouti a.
- **Konpozisyon Kadans** : Gwo flou sikilè `filter: blur(20px)` konbine avèk yon ti zoom rapid ki disparèt touswit sou nouvo sèn nan.
- **Obligasyon AI** : Aplike tranzisyon `.blur-zoom-in` sou 0.35 segonn.

#### 070. `/effectgeometricwipe` — Tranzisyon Fòm Jeyometrik
- **Wòl** : Style konsepsyon pwòp, jèn, modèn (triyang, dyaman oswa egzagon).
- **Konpozisyon Kadans** : Yon seri ti egzagon oswa triyang k ap vire epi kouvri ekran an pou devwale pwochen sèn nan.
- **Obligasyon AI** : Sèvi ak kadriyaj mask SVG k ap ouvri an sekans soti nan sant la.

#### 071. `/effectlumaabsorb` — Tranzisyon pa Nivo Limyè (Luma Fade)
- **Wòl** : Pati ki pi klere nan premye sèn nan fonn an premye, epi pati ki pi nwa yo fonn apre.
- **Konpozisyon Kadans** : Tranzisyon ki itilize valè nwa ak blan chak piksèl pou fè disparisyon an fèt an fòm teksti olye yon fondu plat.
- **Obligasyon AI** : Aplike filtè luma mask nan konpozisyon Kadans lan.

---

### KATEGORI G : SON, ODYO & RITM SYNCHRO (072–081)

#### 072. `/effectaudiowaveform` — Ond Odyo Dinamik k ap Danse
- **Wòl** : Montre vizyèlman son vwa a oswa mizik la an tan reyèl.
- **Konpozisyon Kadans** : Ba vètikal oswa liy koub k ap monte desann selon frekans vwa a nan chak moman videyo a.
- **Obligasyon AI** : Entegre `.audio-waveform-bars` ak animasyon wotè ki senkronize ak kouran odyo a.

#### 073. `/effectbeatdrop` — Senkronizasyon Aksyon sou Bas Mizik la
- **Wòl** : Fè tout animasyon vizyèl la eksploze oswa chanje egzakteman sou gwo kout bas la.
- **Konpozisyon Kadans** : Chanjman sèn, sekous kamera, flash limyè ak aparisyon tit la bloke egzakteman sou timestamp kout bas la.
- **Obligasyon AI** : Aliyen pwen tranzisyon an nan `spec.json` sou segonn egzak kote mizik la chanje ritm lan.

#### 074. `/effectsubbasshit` — Kout Bas Pwofon (Sub-Bass Boom)
- **Wòl** : Bay yon santiman puisans ekstrèm lè yon gwo solisyon oswa logo parèt.
- **Konpozisyon Kadans** : Son bas lou 30-40Hz ki dire 2 segonn, akonpaye de yon ti tranbleman ekran lejè.
- **Obligasyon AI** : Entegre son SFX bas nan pwojè a epi pwograme sekous vizyèl la nan menm moman an.

#### 075. `/effectsoundwhoosh` — Son Van sou Mouvman Rapid
- **Wòl** : Fè chak deplasman kat, glise tèks oswa kout kamera gen yon son van reyalis.
- **Konpozisyon Kadans** : Son Whoosh kout ki senkronize ak kòmansman chak mouvman `translateX/Y`.
- **Obligasyon AI** : Mete son Whoosh nan dosye `medya/sfx/` epi rele l sou chak gwo tranzisyon.

#### 076. `/effectsoundui` — Ti Son Klik ak Pòp pou Eleman UI
- **Wòl** : Bay yon santiman taktil satisfè lè yon bwat parèt, yon bouton klike, oswa yon chif konte.
- **Konpozisyon Kadans** : Ti son subtil kalite wo (pop, subtle click, bell chime, soft tap).
- **Obligasyon AI** : Entegre ti son UI sou chak aparisyon kat, badj, oswa kaz koche.

#### 077. `/effectvinylwarmth` — Chalè Analojik ak Ti Krakman Vinil
- **Wòl** : Bay yon anbyans nostaljik, retro, chalè moun oswa mizik jazz/lo-fi.
- **Konpozisyon Kadans** : Anbyans son disk vinil ak ti krakman byen ba nan background dèyè mizik la.
- **Obligasyon AI** : Ajoute kouch son `.vinyl-crackle` a volim 15% anba mizik prensipal la.

#### 078. `/effectvoiceisolate` — Vwa Pwòp ak Bese Mizik Otomatik (Ducking)
- **Wòl** : Garanti ke chak mo oratè a di tande klè 100% san mizik la pa kouvri l.
- **Konpozisyon Kadans** : Mizik la bese otomatikman a 20% volim li chak fwa vwa a ap pale, epi li remonte a 70% lè gen yon poz.
- **Obligasyon AI** : Konfigire koub volim mizik la (`volume_keyframes`) nan spec la selon tan vwa a.

#### 079. `/effectcrowdambience` — Anbyans Foul Moun ak Bravo
- **Wòl** : Kreye santiman yon gwo evenman, yon konferans siksè oswa yon sal ki chaje moun.
- **Konpozisyon Kadans** : Ti bri moun k ap pale dousman nan kòmansman, ak gwo bravo/aplodisman sou anons viktwa a oswa CTA final la.
- **Obligasyon AI** : Mete son foul la nan sèn entwodiksyon ak sèn konklizyon an.

#### 080. `/effectheartbeatfx` — Bat Kè k ap Akselere pou Kreye Tansyon
- **Wòl** : Mete odyans lan sou kout tansyon pandan y ap tann yon rezilta oswa yon solisyon.
- **Konpozisyon Kadans** : Son bat kè ki kòmanse dousman epi ki akselere, ak yon ti flash wouj/nwa sou chak bat.
- **Obligasyon AI** : Senkronize animasyon `scale(1.03) -> scale(1)` sou chak bat kè son an.

#### 081. `/effectreverbtrail` — Eko Espasyal sou Dènye Mo a
- **Wòl** : Kite dènye eslogan an oswa non mak la k ap flote nan lespri moun nan apre videyo a fini.
- **Konpozisyon Kadans** : Dènye silab vwa a fini ak yon gwo rekonpans eko espasyal (reverb tail) pandan logo a ap klere.
- **Obligasyon AI** : Aplike efè reverbyasyon sou dènye segman odyo a ak fondu nwa vizyèl.

---

### KATEGORI H : ANIMASYON PÈSONAJ & RIGGING (082–091)

#### 082. `/effectstickmanrig` — Stickman SVG Rig 16 Zo ak Lipsync
- **Wòl** : Rakonte yon istwa senp, amizan epi klè ak yon ti bononm baton anime pwofesyonèl.
- **Konpozisyon Kadans** : Stickman SVG konplè ak 16 zo (tèt, kou, tors, bra, koud, men, basen, kwis, jenou, pye) k ap mache, sote, montre ekran an epi pale ak lipsync fonèm WAAPI 60 FPS.
- **Obligasyon AI** : Entegre modil SVG Rig la ak kòmand mouvman (`walk`, `jump`, `point`, `explain`).

#### 083. `/effectcutout2d` — Pèsonaj Ilistre 2D Cut-Out
- **Wòl** : Style desen anime modèn kote pèsonaj la gen manb li yo k ap deplase avèk elastisite.
- **Konpozisyon Kadans** : Pèsonaj divize an moso separe (bra, kò, tèt) ki konekte nan pwen pivote natirèl ak ekspresyon figi vivan.
- **Obligasyon AI** : Mete pèsonaj la sou kote ekran an k ap entèaji ak grafik ki nan mitan an.

#### 084. `/effectavatarhost` — Prezantatè Vityèl sou Kote Ekran an
- **Wòl** : Gide itilizatè a pandan tout videyo a tankou yon prezantatè televizyon.
- **Konpozisyon Kadans** : Yon avatar pwòp nan yon kad won oswa kanpe sou bò dwat ekran an, k ap pale ak jès men natirèl pandan l ap prezante chak pwen.
- **Obligasyon AI** : Kenbe avatar a sou bò a pou l pa janm kache tèks oswa demonstrasyon pwodwi a.

#### 085. `/effecttalkinghead` — Tèt Anime ak Lipsync Egzak sou Mo
- **Wòl** : Bay yon ilistrasyon oswa yon karaktè lavi nan senkronize bouch li ak mo oratè a ap di.
- **Konpozisyon Kadans** : Bouch SVG ki chanje fòm ant fonèm `A`, `E`, `O`, `M`, `L` selon tan chak mo nan fichye `.words.json`.
- **Obligasyon AI** : Lye bouch karaktè a ak done fonèm transkripsyon Whisper la.

#### 086. `/effectemojipop` — Emodji 3D k ap Pete Otou Karaktè a
- **Wòl** : Ajoute imou, emosyon ak reyaksyon vivan sou sa karaktè a ap di.
- **Konpozisyon Kadans** : Emodji 3D (dife 🔥, fize 🚀, kè ❤️, tèt k ap panse 🤔, lajan 💰) ki sote soti bò tèt karaktè a ak yon ti rebondisman.
- **Obligasyon AI** : Deklannche emodji yo sou mo kle ki gen gwo chaj emosyonèl.

#### 087. `/effectshadowpuppet` — Silwèt Lonbraj Nwa
- **Wòl** : Estil teyat lonbraj tradisyonèl pou rakonte lejann, istwa kiltirèl oswa fab.
- **Konpozisyon Kadans** : Pèsonaj ak pyebwa an silwèt nwa total sou yon background klere zoranj oswa jòn solèy kouche.
- **Obligasyon AI** : Sèvi ak fòm SVG nwa `#000000` sou yon fon degrade solèy kouche cho.

#### 088. `/effectmascotdance` — Maskòt k ap Selebre sou CTA Final la
- **Wòl** : Kite yon dènye enpresyon jwaye ak pozitif sou odyans lan.
- **Konpozisyon Kadans** : Maskòt pwojè a k ap danse yon ti dans viktwa oswa k ap voye men a odyans lan bò kote bouton CTA a.
- **Obligasyon AI** : Ajoute animasyon `.dance-bounce` sou maskòt la nan dènye 5 segonn videyo a.

#### 089. `/effectspeechbubble` — Bil Komik (Speech Bubble) ak Tèks
- **Wòl** : Montre panse entèn yon karaktè oswa sa l ap di nan yon fòm desen anime.
- **Konpozisyon Kadans** : Ti bil blan ki monte soti nan bouch pèsonaj la ak yon pwent flèch ki vize tèt li, tèks la parèt anndan l.
- **Obligasyon AI** : Kreye bil SVG `.speech-bubble` ak animasyon `scale(0) -> scale(1)`.

#### 090. `/effectgesturesmart` — Men Anime k ap Montre oswa Klike
- **Wòl** : Dirije atansyon odyans lan sou yon bouton, yon pri oswa yon lyen enpòtan.
- **Konpozisyon Kadans** : Yon men ilistre ki parèt, lonje dwèt sou eleman an, fè yon ti jès peze oswa glise, epi disparèt.
- **Obligasyon AI** : Mete men `.gesture-hand` ak animasyon deplasman ak ti tap sou zòn sib la.

#### 091. `/effectcrowdsilhouette` — Foul Moun an Silwèt anba Ekran an
- **Wòl** : Simile yon gwo odyans nan yon estad oswa yon sal konferans k ap gade prezantasyon an.
- **Konpozisyon Kadans** : Kouch silwèt tèt ak men moun anba ekran an k ap bat men oswa k ap leve telefòn yo pou filme.
- **Obligasyon AI** : Ajoute `.crowd-silhouette-layer` anba a ak ti balanse natirèl.

---

### KATEGORI I : SEKSYON NARATIF & ESTRIKTI STORY (092–101)

#### 092. `/effecthookpunch` — Premye 3 Segonn Chòk (Hook)
- **Wòl** : Anpeche moun nan glise (swipe away) nan kòmansman videyo a.
- **Konpozisyon Kadans** : Yon kesyon pwovokan, yon imaj entans, yon deklarasyon chòk ak son enpak rapid nan premye 3 segonn yo.
- **Obligasyon AI** : Sèn 1 dwe kout, fò, vizyèlman chaje, epi lanse sijè a san okenn entwodiksyon lent.

#### 093. `/effectproblemstatement` — Prezantasyon Doulè ak Fristrasyon
- **Wòl** : Fè odyans lan rekonèt pwòp pwoblèm pa yo pou yo santi yo konsène.
- **Konpozisyon Kadans** : Koulè pi somb, mizik ki gen ti tansyon, ilistrasyon moun ki fatige oswa sistèm ki bloke.
- **Obligasyon AI** : Mete aksan sou difikilte kliyan an rankontre avan li jwenn solisyon an.

#### 094. `/effectsolutionswitch` — Chanjman Radikal kote Solisyon an Parèt
- **Wòl** : Moman transfòmasyon kote espwa retounen grasa pwodwi a.
- **Konpozisyon Kadans** : Limyè klere ki pete, koulè vivan ki ranplase nwa a, mizik ki vin gen enèji pozitif ak libète.
- **Obligasyon AI** : Tranzisyon soti nan ton somb rive nan ton liminezon ak gwo aparisyon non pwodwi a.

#### 095. `/effectfeaturecarousel` — Defilman 3 a 5 Avantaj Prensipal
- **Wòl** : Montre tout sa pwodwi a ka fè yon fason klè ak rapid.
- **Konpozisyon Kadans** : 3 a 5 kat ki defile orizontalman, chak gen yon bèl ikon 3D, yon tit 3 mo, ak yon fraz rezime.
- **Obligasyon AI** : Pase 2 a 3 segonn sou chak karakteristik avèk yon tranzisyon glise ant yo.

#### 096. `/effectsocialproof` — Temwayaj Kliyan & 5 Zetwal
- **Wòl** : Bati konfyans total nan montre ke lòt moun deja kontan ak rezilta a.
- **Konpozisyon Kadans** : Kat temwayaj ak foto kliyan, 5 zetwal an lò k ap limen (`★★★★★`), ak ti kòmantè antrepriz oswa devlopè.
- **Obligasyon AI** : Mete zetwal `.star-gold` k ap limen youn apre lòt ak foto/non itilizatè reyèl.

#### 097. `/effectpricingtable` — Tablo Pri ak Plan Popilè Klere
- **Wòl** : Ede kliyan an chwazi bon plan an fasilman.
- **Konpozisyon Kadans** : 2 oswa 3 kat pri bò kote, plan rekòmande a pi wo, li gen yon badj «PI POPILÈ» ak yon bèl bodi néon k ap klere.
- **Obligasyon AI** : Mete plan prensipal la an valè vizyèlman devan lòt plan yo.

#### 098. `/effectguaranteebadge` — Boukliye Garanti 100% Satisfè
- **Wòl** : Retire tout dout ak laperèz nan lespri kliyan an.
- **Konpozisyon Kadans** : Yon bèl boukliye lò ak vèt ak sele sekirite, tèks «100% GARANTI OUBYEN LAJAN W RETOUNEN».
- **Obligasyon AI** : Mete boukliye `.guarantee-shield` k ap parèt ak yon ti wotasyon fyè.

#### 099. `/effecturgencytimer` — Revèy Kout Tan (Countdown Timer)
- **Wòl** : Pouse odyans lan aji kounye a olye yo ranvwaye sa pou pita.
- **Konpozisyon Kadans** : Ti revèy dijital k ap konte minit ak segonn k ap fini, akonpaye de tèks «ÒF LIMITE».
- **Obligasyon AI** : Entegre revèy `.countdown-timer` k ap diminye pandan sèn nan ap jwe.

#### 100. `/effectctaultimate` — Apèl a Laksyon Final ki Fò
- **Wòl** : Di kliyan an egzakteman sa pou li fè apre videyo a fini.
- **Konpozisyon Kadans** : Gwo bouton klere k ap voye vag limyè, adrès sit web an gwo lèt klè, flèch k ap montre bouton an, vwa ki di aksyon an dirèkteman.
- **Obligasyon AI** : Santre bouton CTA a ak klas `.btn-cta-pulse`, mete lyen an gwo ak bouton klike.

#### 101. `/effectoutrologos` — Logo Fini ak Son Siyati (Audio Brand)
- **Wòl** : Fini videyo a avèk grandè sou idantite ofisyèl mak la.
- **Konpozisyon Kadans** : Logo a k ap monte nan mitan ekran an ak yon refleksyon limyè k ap pase sou li, eslogan anba l, lyen rezo sosyal, ak son siyati konpayi an.
- **Obligasyon AI** : Dènye sèn nan dwe pwòp, kalm, ak logo santre sou fon fonse ak son final la.

---

### KATEGORI J : MOTION DESIGN & MOTION GRAPHICS (102–126)

#### 102. `/motiondesign` — Motion Design Pwofesyonèl Konplè
- **Wòl** : Transfòme tout videyo a an yon pwodiksyon motion design kalite ajans (nivo Buck / Ordinary Folk).
- **Konpozisyon Kadans** : Grid 12 kolòn, palèt 3-4 koulè fiks, chak eleman antre ak easing `cubic-bezier(0.65,0,0.35,1)`, overshoot lejè, stagger 60-90 ms ant eleman, pa gen okenn eleman ki rete fiks plis pase 1.2 s.
- **Obligasyon AI** : Tout sèn yo dwe vektè HTML/SVG editab (pa imaj), ak yon rit animasyon konstan; mete klas `.motion-pro` nan `spec.json` epi itilize menm easing la toupatou.

#### 103. `/motiongraphic` — Motion Graphics Enfografik
- **Wòl** : Eksplike done ak lide ak grafik anime (ikòn, chif, flèch, diagram).
- **Konpozisyon Kadans** : Ikòn flat ki parèt ak `scale 0→1.08→1`, flèch ki desine poukont yo (`stroke-dashoffset`), chif ki konte, tèks kout 3-6 mo pa ekran.
- **Obligasyon AI** : Chak pwen vwa a di dwe gen yon grafik ki koresponn sou ekran an nan menm segonn nan (sync ak vwa); pa janm mete paragraf long.

#### 104. `/morphism` — Morphing Fòm Vektè (Shape Morph)
- **Wòl** : Fè yon fòm transfòme an yon lòt san koupe (sèk → kare → logo → ikòn).
- **Konpozisyon Kadans** : Morph SVG `path` ak menm kantite pwen (flubber / interpolasyon path), koulè ki chanje an menm tan, dire 0.6-1.2 s, easing `easeInOutQuart`.
- **Obligasyon AI** : Chak tranzisyon ant sèn dwe sòti nan yon fòm ki morph nan pwochen eleman an; pa janm cut sèk ant 2 sèn ki gen /morphism.

#### 105. `/shapelayers` — Animasyon Shape Layers
- **Wòl** : Konstwi kompozisyon ak fòm jeyometrik k ap antre, vire, ak anpile.
- **Konpozisyon Kadans** : Sèk, rektang, triyang, liy ki antre youn apre lòt (stagger), rotasyon 90°/180°, mask ant fòm yo, koulè plat san gradyan.
- **Obligasyon AI** : Itilize sèlman fòm SVG primitif; chak fòm se yon kalk separe nan spec la pou devlopè a ka modifye l.

#### 106. `/liquidmotion` — Likid & Blob Motion
- **Wòl** : Bay videyo a yon santiman òganik, mou, likid.
- **Konpozisyon Kadans** : Blob SVG ki deforme (filter `feTurbulence` + `feDisplacementMap` oswa morph path), gout ki fizyone (gooey effect), mouvman dousman 4-8 s an bouk.
- **Obligasyon AI** : Pa itilize kwen file; tout fòm dwe gen koub dous; anpile ak /gradientmotion si gen degrade.

#### 107. `/linedraw` — Liy k ap Desine Poukont li (Stroke Draw)
- **Wòl** : Montre ilistrasyon, kat, oswa logo k ap trase devan je moun nan.
- **Konpozisyon Kadans** : `stroke-dasharray` + `stroke-dashoffset` anime de 100% → 0, epesè liy konstan, fill ki parèt APRE liy lan fini (fade 0.3 s).
- **Obligasyon AI** : Tout desen yo dwe an SVG path; lòd desen an swiv lojik natirèl (soti agoch anwo → adwat anba) oswa vwa a.

#### 108. `/flatmotion` — Flat Design Anime 2D
- **Wòl** : Estil ilistrasyon plat modèn (kalite Kurzgesagt / startup explainer).
- **Konpozisyon Kadans** : Koulè plat, lonbraj long 45°, pa gen tekstur, pèsonaj ak objè senp, mouvman rebondi lejè.
- **Obligasyon AI** : Palèt maksimòm 5 koulè; tout eleman vektè; kenbe menm epesè liy nan tout videyo a.

#### 109. `/isomotion` — Izometrik Anime
- **Wòl** : Montre sistèm, vil, biwo oswa pwosesis an vi izometrik 30°.
- **Konpozisyon Kadans** : Grid izometrik, blòk ki tonbe/monte an plas, ti pèsonaj ak machin ki deplase sou chemen izometrik, kamera fiks.
- **Obligasyon AI** : Respekte ang 30° egzak (`transform: rotateX(60deg) rotateZ(45deg)` oswa SVG izometrik); pa melanje ak pèspektif nòmal.

#### 110. `/logoreveal` — Revelasyon Logo Motion
- **Wòl** : Fè logo a parèt avèk enpak nan kòmansman oswa nan fen.
- **Konpozisyon Kadans** : Mask ki louvri, patikil ki rasanble pou fòme logo a, oswa liy ki trase l; flash limyè sibtil + whoosh, dire 2-3 s.
- **Obligasyon AI** : Sèvi ak logo ORIJINAL kliyan an (SVG si posib); pa janm deforme pwopòsyon li; son whoosh/impact sync sou moman li fin parèt.

#### 111. `/logoanimation` — Logo Anime Konplè (Build-up)
- **Wòl** : Dekonpoze logo a an pyès epi rekonstwi l ak animasyon.
- **Konpozisyon Kadans** : Chak pyès logo a (senbòl, lèt, eslogan) antre separeman, rebondi, epi tout bagay estabilize; bouk opsyonèl 3-5 s.
- **Obligasyon AI** : Separe logo a an kalk SVG; ekspòte tou yon vèsyon kout 1.5 s pou ouvèti rezo sosyal.

#### 112. `/iconmotion` — Ikòn Anime (Micro-animasyon)
- **Wòl** : Bay chak ikòn yon ti lavi (kloch k ap sonnen, kè k ap bat, chèk k ap trase).
- **Konpozisyon Kadans** : Animasyon kout 0.4-0.8 s, mouvman ki fè sans ak sans ikòn nan, stroke + fill.
- **Obligasyon AI** : Chak ikòn dwe gen yon animasyon ki gen rapò ak siyifikasyon l; pa sèvi ak menm animasyon jenerik pou tout.

#### 113. `/datamotion` — Grafik Done Anime (Bar, Pie, Line)
- **Wòl** : Fè chif yo vin vivan ak grafik k ap grandi.
- **Konpozisyon Kadans** : Ba k ap monte soti 0, koub k ap desine, pie chart k ap ranpli, etikèt valè ki konte an menm tan, aks pwòp.
- **Obligasyon AI** : Done yo dwe REYÈL (sa devlopè a bay oswa sous la); pa envante chif; montre sous la an ti tèks anba.

#### 114. `/countermotion` — Chif k ap Monte (Counter)
- **Wòl** : Mete aksan sou yon chif enpòtan (kliyan, lavant, %, pri).
- **Konpozisyon Kadans** : Chif gwo (120-200 px), konte soti 0 rive valè a ak easing `easeOutExpo`, inite/sentaks ki parèt apre, ti pulse nan fen.
- **Obligasyon AI** : Chif la dwe fini sou yon son 'tick'/impact; fòma nimewo dapre lang (1 000 / 1,000).

#### 115. `/explainer` — Videyo Eksplikatif Motion
- **Wòl** : Estrikti eksplikatif klasik: pwoblèm → kijan sa mache → benefis → CTA.
- **Konpozisyon Kadans** : Sèn 4-6 s chak, pèsonaj flat, ikòn, flèch, vwa klè, mizik lejè optimis.
- **Obligasyon AI** : Swiv estrikti 4 pati a obligatwa; chak sèn yon sèl lide; vwa ElevenLabs ak soutit.

#### 116. `/lowerthirdpro` — Lower Third Motion Pro
- **Wòl** : Prezante non, tit, oswa enfòmasyon anba ekran an.
- **Konpozisyon Kadans** : Ba koulè ki glise + tèks ki parèt ak mask, aliyman agoch, rete 3-5 s, sòti nan sans envès.
- **Obligasyon AI** : Pa janm kouvri figi moun nan; respekte zòn sekirite 5% anba ak sou kote.

#### 117. `/titlesequence` — Jenerik Tit Sinema
- **Wòl** : Kreye yon jenerik ouvèti tankou yon seri televizyon oswa fim.
- **Konpozisyon Kadans** : Tipografi gwo, kreyatif, an rapò ak sijè a, sèn tit youn apre lòt sou mizik ritmik, koupe sou beat yo.
- **Obligasyon AI** : Mete non pwojè a, kreyatè yo, epi yon tit final; sync chak chanjman ak beat mizik la (/effectbeatdrop si disponib).

#### 118. `/swisstype` — Tipografi Swis / Grid Motion
- **Wòl** : Estil grafik swis: grid strik, tipografi grotesk, aliyman pafè.
- **Konpozisyon Kadans** : Font sans-serif (Inter / Helvetica-like), blòk tèks aliyen sou grid, koulè limite (nwa, blan, wouj), mouvman glisman lineyè.
- **Obligasyon AI** : Pa gen dekorasyon initil; chak mouvman swiv grid la egzakteman.

#### 119. `/bouncemotion` — Rebondi Elastik (Squash & Stretch)
- **Wòl** : Bay objè yo yon karaktè ludik ak 12 prensip animasyon yo.
- **Konpozisyon Kadans** : Squash & stretch sou chòk, anticipation anvan mouvman, follow-through, easing elastik `easeOutElastic`.
- **Obligasyon AI** : Itilize l pou objè lejè ak ton jwèt; pa itilize l sou tèks serye oswa done finansye.

#### 120. `/maskreveal` — Revelasyon pa Mask
- **Wòl** : Fè tèks ak imaj parèt dèyè yon mask ki glise.
- **Konpozisyon Kadans** : `clip-path` oswa SVG mask ki deplase, tèks ki monte soti anba yon liy envizib, imaj ki revele pa bann.
- **Obligasyon AI** : Tout revelasyon dwe gen direksyon konsistan nan menm sèn nan.

#### 121. `/splitscreen` — Ekran Divize Anime
- **Wòl** : Montre 2-4 bagay an menm tan (konparezon, plizyè pwodwi, plizyè moun).
- **Konpozisyon Kadans** : Panèl ki separe ak liy anime, chak panèl antre an dekale, separatè ki deplase pou chanje pwopòsyon.
- **Obligasyon AI** : Chak panèl dwe lizib sou mobil; pa plis pase 4 panèl.

#### 122. `/loopmotion` — Bouk Pafè (Seamless Loop)
- **Wòl** : Kreye yon animasyon ki ka repete san fen (GIF, fon, rezo sosyal).
- **Konpozisyon Kadans** : Premye ak dènye imaj idantik, mouvman siklik (rotasyon 360°, onn, pulsasyon), dire 2-8 s.
- **Obligasyon AI** : Verifye ke frame 0 = dènye frame; mete `loop: true` nan spec la.

#### 123. `/3dmotion` — Motion 3D CSS (Perspective)
- **Wòl** : Bay pwofondè ak kat, tèks ak ekran ki vire nan espas 3D.
- **Konpozisyon Kadans** : `perspective: 1200px`, `rotateY/rotateX`, kat ki vire, kamera ki deplase nan pwofondè, lonbraj dinamik.
- **Obligasyon AI** : Rete lizib: pa vire tèks plis pase 35° pandan l ap li.

#### 124. `/gradientmotion` — Degrade k ap Deplase (Mesh Gradient)
- **Wòl** : Fon degrade vivan k ap deplase dousman.
- **Konpozisyon Kadans** : Mesh gradient 3-5 koulè ki deplase (pozisyon animé), blur gwo, grain lejè anlè l.
- **Obligasyon AI** : Kontras ak tèks la dwe rete ≥ 4.5:1 tout tan.

#### 125. `/halftonemotion` — Halftone & Retro Print Motion
- **Wòl** : Estil enprime retro (tach pwen, komik, afich vintage) an mouvman.
- **Konpozisyon Kadans** : Pattern halftone SVG, dekalaj koulè CMYK, tekstur papye, animasyon 12 fps 'stop-motion'.
- **Obligasyon AI** : Jwe sou frame rate 12 fps pou eleman yo, men ekspòte final la an 60 FPS.

#### 126. `/uimotion` — Animasyon UI Pwodwi (App Walkthrough)
- **Wòl** : Montre kijan yon app oswa yon lojisyèl mache ak animasyon entèfas pwòp.
- **Konpozisyon Kadans** : Kurseur/dwèt ki klike, ekran ki glise, eleman UI ki parèt, zoom sou zòn enpòtan, aparèy (/effectdeviceframe).
- **Obligasyon AI** : Sèvi ak vrè captur oswa vrè UI rekonstwi an HTML; pa envante fonksyon ki pa egziste.

---

### KATEGORI K : PIBLISITE & PUB PWOFESYONÈL (127–151)

#### 127. `/pubstore` — Pub Magazen / Boutik (Retail Promo)
- **Wòl** : Fè pwomosyon yon magazen, boutik oswa sipèmache.
- **Konpozisyon Kadans** : Pwodwi ki parèt sou etajè anime, pri ak etikèt ki tonbe, adrès + orè, logo magazen an, CTA 'Vin jodi a'.
- **Obligasyon AI** : Mete pri ak rabè an GWO; enfòmasyon lokal (adrès, telefòn, WhatsApp) obligatwa nan sèn final la.

#### 128. `/zoommap` — Zoom sou Kat (Map Zoom Lokalizasyon)
- **Wòl** : Montre ki kote yon biznis, evènman oswa kote ye.
- **Konpozisyon Kadans** : Kat ki soti nan vi peyi → vil → katye → pin ki tonbe ak rebondi, wout ki trase, etikèt non kote a.
- **Obligasyon AI** : Itilize kat SVG/OpenStreetMap (pa Google Maps captur ki gen copyright san atribisyon); pin nan dwe nan koulè mak la.

#### 129. `/pubproduct` — Pwodwi Hero 360°
- **Wòl** : Mete yon pwodwi an vedèt kòm zetwal pub la.
- **Konpozisyon Kadans** : Pwodwi santre sou fon pwòp, rotasyon/paralaks, limyè rim, karakteristik ki parèt ak liy ki pwente pati yo.
- **Obligasyon AI** : Pwodwi a dwe pran omwen 50% ekran an nan sèn prensipal la; pa deforme koulè reyèl pwodwi a.

#### 130. `/pubfood` — Pub Restoran & Manje
- **Wòl** : Fè moun grangou: restoran, fast-food, patisri.
- **Konpozisyon Kadans** : Gwo plan manje, vapè, sòs k ap koule, slow-motion, koulè cho, son grese/kwit.
- **Obligasyon AI** : Koulè cho (wouj, jòn, oranj); mete meni / pri / livrezon nan fen.

#### 131. `/pubrealestate` — Pub Imobilye
- **Wòl** : Prezante kay, apatman oswa tè pou vann/lwe.
- **Konpozisyon Kadans** : Vi dwòn/ekstè, vizit pyès pa pyès, ikòn chanm/sal de ben/m², kat lokalizasyon, pri.
- **Obligasyon AI** : Fòma: ekstè → pyès prensipal → detay → kat → pri + kontak ajan.

#### 132. `/pubcar` — Pub Machin / Otomobil
- **Wòl** : Pub machin, konsesyonè, pyès oswa garaj.
- **Konpozisyon Kadans** : Mouvman kamera dinamik, limyè refleksyon sou karosri, vitès, son motè, tipografi agresif.
- **Obligasyon AI** : Mete modèl, ane, pri oswa ofri finansman; respekte koulè reyèl machin nan.

#### 133. `/pubfashion` — Pub Mòd & Rad
- **Wòl** : Pub boutik rad, soulye, aksesoir, koleksyon.
- **Konpozisyon Kadans** : Koupe sou beat, tipografi editoryal, look youn apre lòt, transition flash, mizik tandans.
- **Obligasyon AI** : Ritm rapid (0.5-1 s pa plan) sync ak mizik; non koleksyon an + lyen boutik la nan fen.

#### 134. `/pubbeauty` — Pub Kosmetik & Bote
- **Wòl** : Pub pwodwi bote, salon, spa.
- **Konpozisyon Kadans** : Tekstur krèm macro, gout, limyè dous, koulè pastèl/or, po klere.
- **Obligasyon AI** : Ton elegan, kalm; pa fè fo pwomès medikal.

#### 135. `/pubtech` — Pub Teknoloji / Gadget
- **Wòl** : Pub telefòn, òdinatè, gadget, sèvis teknoloji.
- **Konpozisyon Kadans** : Fon nwa, limyè neon ble/mòv, zoom sou detay, spesifikasyon ki parèt ak liy.
- **Obligasyon AI** : Spesifikasyon yo dwe reyèl; mete pri + kote pou achte.

#### 136. `/pubapp` — Pub Aplikasyon Mobil (App Promo)
- **Wòl** : Fè moun telechaje yon app.
- **Konpozisyon Kadans** : Telefòn 3D ak ekran app la, 3 fonksyon prensipal, badj App Store / Google Play, QR code.
- **Obligasyon AI** : Montre vrè ekran app la; fini ak badj magazen yo + CTA 'Telechaje kounye a'.

#### 137. `/pubevent` — Pub Evènman / Konsè
- **Wòl** : Anonse konsè, fèt, konferans, fwa.
- **Konpozisyon Kadans** : Non atis/oratè, dat & lè an gwo, kote (/zoommap si bezwen), kontè dat, mizik enèjik.
- **Obligasyon AI** : Dat, lè, kote, pri tikè ak kote pou achte = obligatwa.

#### 138. `/pubflashsale` — Vant Flash / Pwomosyon %
- **Wòl** : Kreye ijans pou yon pwomosyon limite.
- **Konpozisyon Kadans** : Gwo pousantaj (-50%), pri anvan bare, revèy kontè, koulè wouj/jòn, tèks k ap tranble.
- **Obligasyon AI** : Mete dat fen pwomosyon an; pri anvan ak apre dwe vizib klèman.

#### 139. `/pubblackfriday` — Black Friday / Gwo Rabè
- **Wòl** : Pub espesyal Black Friday, Cyber Monday, fen ane.
- **Konpozisyon Kadans** : Fon nwa, tipografi gwo lò/blan, flash, eksplozyon rabè, lis pwodwi ak pri.
- **Obligasyon AI** : Ton prestij + ijans; dat evènman an obligatwa.

#### 140. `/pubbank` — Pub Bank & Fintech
- **Wòl** : Pub bank, transfè lajan, app peman, mikwofinans.
- **Konpozisyon Kadans** : Koulè konfyans (ble, vèt), kat bankè 3D, grafik kwasans, ikòn sekirite, moun ki souri.
- **Obligasyon AI** : Mansyon legal / kondisyon an ti tèks si gen to oswa frè.

#### 141. `/pubhealth` — Pub Sante / Klinik
- **Wòl** : Pub klinik, famasi, lopital, sèvis sante.
- **Konpozisyon Kadans** : Koulè blan/ble/vèt, ikòn medikal, ekip souri, sèvis lis, kontak ijans.
- **Obligasyon AI** : Pa janm fè pwomès gerizon; enfòmasyon kontak klè.

#### 142. `/pubschool` — Pub Lekòl & Fòmasyon
- **Wòl** : Pub lekòl, inivèsite, fòmasyon, kou an liy.
- **Konpozisyon Kadans** : Etidyan, ikòn liv/diplòm, lis pwogram, dat enskripsyon, temwayaj.
- **Obligasyon AI** : Dat limit enskripsyon + kontak obligatwa.

#### 143. `/pubtravel` — Pub Vwayaj & Touris
- **Wòl** : Pub ajans vwayaj, otèl, destinasyon (Ayiti, Karayib…).
- **Konpozisyon Kadans** : Plan peyizaj, avyon ki trase wout sou kat (/zoommap), pri pakè, aktivite.
- **Obligasyon AI** : Montre pri 'apati de' + dat; peyizaj reyèl destinasyon an.

#### 144. `/pubrestaurantmenu` — Meni Dijital Anime (Menu Board)
- **Wòl** : Ekran meni pou restoran (TV nan magazen).
- **Konpozisyon Kadans** : Kolòn plat + pri, plat k ap vire youn apre lòt, pwomosyon jou a an evidans, bouk 15-30 s.
- **Obligasyon AI** : Fòma 16:9 oswa 9:16 vètikal; pri lizib a 3 mèt distans; /loopmotion otomatik.

#### 145. `/pubtestimonial` — Pub Temwayaj UGC
- **Wòl** : Pub kote kliyan pale (estil UGC rezo sosyal).
- **Konpozisyon Kadans** : Vertikal 9:16, figi kliyan, soutit mo pa mo, zetwal 5, pwodwi an plan.
- **Obligasyon AI** : Temwayaj yo dwe REYÈL (bay devlopè a); pa envante kliyan.

#### 146. `/pubbeforeafter` — Anvan / Apre
- **Wòl** : Montre rezilta yon pwodwi oswa yon sèvis.
- **Konpozisyon Kadans** : Ekran divize ak glisè ki deplase, etikèt ANVAN/APRE, menm kad pou 2 imaj yo.
- **Obligasyon AI** : 2 imaj yo dwe menm ang ak menm limyè; pa manipile rezilta a.

#### 147. `/pubunboxing` — Unboxing Pwodwi
- **Wòl** : Ouvri bwat pwodwi a devan kamera.
- **Konpozisyon Kadans** : Bwat ki louvri, pwodwi ki leve ak limyè, pyès ladan l youn pa youn, son ASMR papye.
- **Obligasyon AI** : Montre tout sa ki nan bwat la; fini ak pri + kote pou achte.

#### 148. `/pubbumper` — Bumper Ad 6 Segonn
- **Wòl** : Pub kout pou YouTube bumper / Stories.
- **Konpozisyon Kadans** : 1 mesaj, logo, CTA — dire EGZAK 6 s, hook nan premye 1 s.
- **Obligasyon AI** : Dire maksimòm 6.0 s; yon sèl lide; logo vizib tout tan oswa nan fen.

#### 149. `/pubtv30` — Spot TV 30 Segonn
- **Wòl** : Spot televizyon/radyo vizyèl klasik 30 s.
- **Konpozisyon Kadans** : Estrikti: hook (3 s) → pwoblèm (5 s) → solisyon (12 s) → prèv (5 s) → CTA + logo (5 s).
- **Obligasyon AI** : Dire egzak 30 s; fòma 16:9 1080p; nivo odyo -23 LUFS (estanda TV).

#### 150. `/pubbillboard` — Pano / DOOH Ekran Lari
- **Wòl** : Pub pou ekran dijital lari, sant komèsyal, ayewopò.
- **Konpozisyon Kadans** : Mesaj 5-7 mo maks, gwo tipografi, kontras fò, bouk 8-15 s san son.
- **Obligasyon AI** : Pa depann de son; lizib a distans; fòma dapre ekran an (pòtrè oswa peyizaj).

#### 151. `/pubjingle` — Jingle & Son Mak
- **Wòl** : Kreye siyati son mak la nan pub la.
- **Konpozisyon Kadans** : Jingle 3-5 s, slogan chante oswa pale (ElevenLabs), son logo, sync ak animasyon logo a.
- **Obligasyon AI** : Itilize ElevenLabs pou vwa/sfx; jingle la dwe repete nan fen chak pub (/effectoutrologos).

---

### KATEGORI L : TRANZISYON VIZYÈL & TRANZISYON SON (152–201)

> Tranzisyon vizyèl (152–186) + tranzisyon son (187–201). Chak skill bay valè EGZAK Kadans la (`transition`, `sfx`, `sounds`, `speed`, `motion_blur`) oswa yon sèn `html` lè Kadans pa gen valè natif.

#### 152. `/zoomin` — Zoom Antre (Zoom In)
- **Wòl** : Antre nan pwochen sèn nan pa yon zoom ki avanse.
- **Konpozisyon Kadans** : Kadans: `"transition": "zoom"` sou sèn ki vini an; dire 0.4-0.6 s; easing `inout`.
- **Obligasyon AI** : Chak koupe ant sèn ki gen /zoomin DWE gen `"transition": "zoom"`; mete `"skills": ["/zoomin"]` sou sèn sa yo.

#### 153. `/zoomout` — Zoom Sòti (Zoom Out)
- **Wòl** : Sòti nan yon sèn tankou kamera a ap rekile.
- **Konpozisyon Kadans** : Kadans: `"transition": "zoomout"`; dire 0.4-0.7 s.
- **Obligasyon AI** : Itilize `"transition": "zoomout"` egzak; pa ranplase l ak fade.

#### 154. `/spiral` — Espiral (Spin + Zoom)
- **Wòl** : Sèn nan vire an espiral pandan l ap rantre/sòti.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo: `rotate(0→720deg)` + `scale(1→0.1)` sou sèn k ap sòti, envès sou sèn k ap antre; dire 0.8 s; oswa `"transition": "rotate"` + zoom si sèn nan pa html.
- **Obligasyon AI** : Rotasyon an dwe omwen 360°; mete `"skills": ["/spiral"]` sou sèn tranzisyon an.

#### 155. `/whippan` — Whip Pan (Panoramik Rapid)
- **Wòl** : Kamera a vole sou kote ak flou mouvman ant 2 sèn.
- **Konpozisyon Kadans** : Kadans: `"transition": "slide"` + `"blur"` (motion_blur limen) oswa sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo `translateX(-120%)` + `filter: blur(18px)`; dire 0.25-0.35 s; son whoosh (`sfx.whoosh: true`).
- **Obligasyon AI** : Dire ≤ 0.35 s; whoosh obligatwa sou koupe a.

#### 156. `/spinblur` — Spin Blur
- **Wòl** : Tranzisyon rotasyon rapid ak flou.
- **Konpozisyon Kadans** : Kadans: `"transition": "rotate"` ak `"motion_blur"` limen; dire 0.4 s.
- **Obligasyon AI** : Rotasyon + flou ansanm; pa yon rotate sèk.

#### 157. `/crossfade` — Fondi Ansanm (Crossfade)
- **Wòl** : Tranzisyon dous, klasik, kalm.
- **Konpozisyon Kadans** : Kadans: `"transition": "fade"`; dire 0.6-1.0 s.
- **Obligasyon AI** : Sèvi ak li pou ton emosyonèl / dokimantè; pa pou pub rapid.

#### 158. `/dipblack` — Fonn an Nwa (Dip to Black)
- **Wòl** : Fèmen yon chapit epi louvri yon lòt.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo fon `#000` ki monte 0→1 (0.3 s), kenbe 0.2 s, desann (0.3 s); oswa sèn kout `background: #000` 0.4 s ak `"transition": "fade"`.
- **Obligasyon AI** : Ekran an dwe vin NWA nèt omwen 0.15 s.

#### 159. `/dipwhite` — Fonn an Blan (Dip to White / Flash)
- **Wòl** : Tranzisyon limyè, rèv, souvni oswa enèji.
- **Konpozisyon Kadans** : Kadans: menm jan ak /dipblack men `#fff`; dire total 0.5-0.8 s.
- **Obligasyon AI** : Ekran an dwe vin BLAN nèt omwen 1 imaj.

#### 160. `/slideleft` — Glise Agoch (Push Left)
- **Wòl** : Pwochen sèn nan pouse ansyen an sou bò goch.
- **Konpozisyon Kadans** : Kadans: `"transition": "slide"`; dire 0.4-0.5 s.
- **Obligasyon AI** : Valè egzak `slide`; direksyon konsistan nan tout seri a.

#### 161. `/slideright` — Glise Adwat (Push Right)
- **Wòl** : Pwochen sèn nan antre soti agoch.
- **Konpozisyon Kadans** : Kadans: `"transition": "slideright"`.
- **Obligasyon AI** : Valè egzak `slideright`.

#### 162. `/slideup` — Glise Anlè (Push Up)
- **Wòl** : Tranzisyon vètikal (estil Reel / TikTok).
- **Konpozisyon Kadans** : Kadans: `"transition": "slideup"`; ideyal 9:16.
- **Obligasyon AI** : Valè egzak `slideup`.

#### 163. `/slidedown` — Glise Anba (Push Down)
- **Wòl** : Tranzisyon vètikal desann.
- **Konpozisyon Kadans** : Kadans: `"transition": "slidedown"`.
- **Obligasyon AI** : Valè egzak `slidedown`.

#### 164. `/wipeline` — Wipe Liy Dwat
- **Wòl** : Yon liy travèse ekran an epi revele pwochen sèn nan.
- **Konpozisyon Kadans** : Kadans: `"transition": "wipe"` (orizontal) oswa `"wipeup"` (vètikal); liy koulè mak la sou kwen an (html).
- **Obligasyon AI** : Valè `wipe`/`wipeup` egzak; liy la nan koulè mak la si gen yon brand.

#### 165. `/circlereveal` — Revelasyon Sèk
- **Wòl** : Yon sèk ki grandi soti nan yon pwen pou revele sèn nan.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo `clip-path: circle(0% at X Y) → circle(150% at X Y)`; dire 0.6 s; sant sou sijè a.
- **Obligasyon AI** : Sant sèk la dwe sou sijè enpòtan an, pa nan mitan pa defo.

#### 166. `/irisclose` — Iris Fèmen (Estil Ansyen Fim)
- **Wòl** : Sèk ki fèmen sou yon detay (fen klasik, komik).
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo `clip-path: circle(150%) → circle(0%)` sou fon nwa; dire 0.8 s.
- **Obligasyon AI** : Fèmen sou detay final la (figi, logo).

#### 167. `/cubeflip` — Kib 3D (Cube Rotate)
- **Wòl** : 2 sèn sou 2 fas yon kib k ap vire.
- **Konpozisyon Kadans** : Kadans: `"transition": "flip"` oswa sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo `perspective: 1200px` + `rotateY(-90deg)` sou 2 fas; dire 0.7 s.
- **Obligasyon AI** : Efè 3D dwe vizib (perspective), pa yon flip plat.

#### 168. `/pageturn` — Vire Paj
- **Wòl** : Tranzisyon tankou yon paj liv k ap vire.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo `rotateY(0→-180deg)` ak `transform-origin: left` + lonbraj; son `sfx:book-flip`.
- **Obligasyon AI** : Son `sfx:book-flip` obligatwa nan moman paj la vire.

#### 169. `/lightleak` — Light Leak (Fuit Limyè Fim)
- **Wòl** : Flash limyè cho òganik ant 2 sèn.
- **Konpozisyon Kadans** : Kadans: overlay degrade oranj/woz `mix-blend-mode: screen` ki travèse (0.8 s) + `"transition": "fade"`.
- **Obligasyon AI** : Koulè cho; overlay transparan, pa yon blòk koulè.

#### 170. `/filmburn` — Fim k ap Boule
- **Wòl** : Tranzisyon vintage tankou fim ki boule.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo tach oranj/blan ki grandi (radial-gradient + blur) + grain; dire 0.8-1 s.
- **Obligasyon AI** : Grain fim + koulè cho obligatwa.

#### 171. `/pixelate` — Pikselizasyon
- **Wòl** : Sèn nan vin pikselize epi re-fòme an pwochen an.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo (canvas oswa `image-rendering: pixelated` + scale), blòk 4→48 px→4; dire 0.6 s.
- **Obligasyon AI** : Piksèl yo dwe vizib klè nan mitan tranzisyon an.

#### 172. `/rgbsplit` — RGB Split (Aberasyon Kwomatik)
- **Wòl** : Kanal wouj/vèt/ble separe pou yon koupe teknolojik.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo 3 kopi ak `mix-blend-mode: screen` dekale ±8 px; dire 0.3 s; son `sfx.hit`.
- **Obligasyon AI** : Dekalaj vizib 3 koulè; dire kout.

#### 173. `/glitchcut` — Koupe Glitch
- **Wòl** : Koupe brital ak glitch dijital.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo bann ki deplase (`clip-path` + translateX aleyatwa), 6-10 imaj; son /soundglitch.
- **Obligasyon AI** : Dire 0.2-0.4 s; anpile ak /soundglitch si son aktif.

#### 174. `/shatter` — Ekran ki Kraze (Shatter)
- **Wòl** : Sèn nan kraze an mòso vè.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo polygon `clip-path` (12-20 mòso) ki tonbe ak rotasyon; son `sfx:impact-glass`.
- **Obligasyon AI** : Son `sfx:impact-glass` obligatwa.

#### 175. `/liquidmelt` — Fonn Likid (Melt)
- **Wòl** : Sèn nan fonn tankou likid.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo SVG `feTurbulence` + `feDisplacementMap` (scale 0→80→0); dire 0.8 s.
- **Obligasyon AI** : Deformasyon òganik vizib; pa yon fade.

#### 176. `/ripple` — Onn Dlo (Ripple)
- **Wòl** : Onn ki pati nan yon pwen tankou wòch nan dlo.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo displacement radial animé; dire 0.8 s.
- **Obligasyon AI** : Onn yo dwe sòti nan yon pwen (klik / sijè).

#### 177. `/swirl` — Toubiyon (Swirl)
- **Wòl** : Sèn nan tòde an toubiyon.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo (canvas / WebGL swirl oswa `rotate` + `blur` + scale); dire 0.7 s.
- **Obligasyon AI** : Distòsyon tòde vizib.

#### 178. `/kaleidoscope` — Kalidoskòp
- **Wòl** : Tranzisyon miwa simetrik psikedelik.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo 6-8 kopi ak `clip-path` triyang + rotasyon; dire 1 s.
- **Obligasyon AI** : Sèvi ak li pou mizik / evènman; simetri vizib.

#### 179. `/stretchwarp` — Etire (Stretch Warp)
- **Wòl** : Sèn nan etire nan direksyon mouvman an.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo `scaleX(1→4)` + `blur` sou sèn k ap sòti, envès sou sa k ap antre; dire 0.35 s; whoosh.
- **Obligasyon AI** : Whoosh obligatwa (`sfx.whoosh: true`).

#### 180. `/blinds` — Pèsyèn (Venetian Blinds)
- **Wòl** : Bann orizontal ki vire pou revele sèn nan.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo 8-12 bann `rotateX(90→0deg)` an stagger 30 ms.
- **Obligasyon AI** : Stagger vizib ant bann yo.

#### 181. `/checkerboard` — Damye (Checkerboard)
- **Wòl** : Kare ki parèt youn apre lòt tankou yon damye.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo grid 8×6 kare `scale(0→1)` an stagger dyagonal.
- **Obligasyon AI** : Stagger dyagonal obligatwa.

#### 182. `/splitreveal` — Ekran ki Louvri an 2
- **Wòl** : Sèn nan fann an 2 (tankou pòt) pou revele pwochen an.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo 2 mwatye `translateX(∓100%)`; son `sfx:door-open` opsyonèl.
- **Obligasyon AI** : 2 mwatye yo dwe deplase nan sans opoze.

#### 183. `/matchcut` — Match Cut
- **Wòl** : Koupe sou 2 fòm/mouvman ki sanble (sèk → lalin).
- **Konpozisyon Kadans** : Kadans: `"transition": "none"` men pozisyon/fòm sijè a IDANTIK nan dènye imaj sèn A ak premye imaj sèn B.
- **Obligasyon AI** : Fòm, gwosè ak pozisyon dwe matche; eksplike nan rapò a ki eleman ki matche.

#### 184. `/smashcut` — Smash Cut
- **Wòl** : Koupe brital soti nan kalm → bri (oswa envès) pou efè komik/chòk.
- **Konpozisyon Kadans** : Kadans: `"transition": "none"`; son koupe nèt oswa monte sèk; kontras total ant 2 sèn yo.
- **Obligasyon AI** : PA gen tranzisyon dous; chanjman son brital.

#### 185. `/speedramp` — Speed Ramp
- **Wòl** : Videyo ralanti → akselere (oswa envès) toupre koupe a.
- **Konpozisyon Kadans** : Kadans: `"speed"` sou sèn videyo yo (egz. 1 → 0.3 → 2) + `"transition": "zoom"`; whoosh.
- **Obligasyon AI** : Itilize kle `speed` Kadans la; sèlman sou sèn ki gen vrè videyo.

#### 186. `/brushstroke` — Kou Penso (Brush Reveal)
- **Wòl** : Kou penso ki penti pwochen sèn nan.
- **Konpozisyon Kadans** : Kadans: sèn `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) ki fè tranzisyon an ant 2 sèn yo SVG mask penso (`stroke-dashoffset`) ki revele sèn nan; son `sfx:paint-brush`.
- **Obligasyon AI** : Son `sfx:paint-brush` obligatwa.

**— Tranzisyon Son (187–201) —**

#### 187. `/soundhot` — Son Cho (Hot Hit / Sizzle)
- **Wòl** : Son enèji 'cho' sou koupe a (pwodwi, manje, pub).
- **Konpozisyon Kadans** : Kadans: `sfx.hit: true` + ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «sizzle hot impact, short punchy»; volim -6 dB.
- **Obligasyon AI** : Son an dwe tonbe EGZAK sou koupe a (`at` = lè tranzisyon an).

#### 188. `/soundepic` — Son Epik (Cinematic Boom)
- **Wòl** : Gwo boom sinematik pou moman enpòtan (revelasyon, logo, tit).
- **Konpozisyon Kadans** : Kadans: ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «epic cinematic boom with deep sub and reverb tail» + `sfx:thunder` an fon; ducking vwa.
- **Obligasyon AI** : Sèvi ak li 1-3 fwa maksimòm pa videyo; sou revelasyon prensipal yo.

#### 189. `/soundtyping` — Son Klavye (Typing)
- **Wòl** : Son klavye pandan tèks parèt.
- **Konpozisyon Kadans** : Kadans: `sfx.type: true` (son tape sou chak lèt) + `sfx.text: true`; sync ak /effecttypewriter.
- **Obligasyon AI** : Chak lèt ki parèt = yon klik; pa jwe son an lè pa gen tèks k ap ekri.

#### 190. `/soundriser` — Riser (Monte Tansyon)
- **Wòl** : Son ki monte anvan yon gwo moman.
- **Konpozisyon Kadans** : Kadans: ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «cinematic riser 2 seconds building tension»; fini EGZAK sou koupe a.
- **Obligasyon AI** : Fen riser a = koupe a / drop la.

#### 191. `/sounddrop` — Drop / Bass Drop
- **Wòl** : Gwo bas apre riser la oswa sou revelasyon.
- **Konpozisyon Kadans** : Kadans: `sfx.hit: true` + ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «deep bass drop impact»; anpile ak /effectbeatdrop.
- **Obligasyon AI** : Sync ak yon chanjman vizyèl fò.

#### 192. `/soundboom` — Boom Enpak
- **Wòl** : Enpak lou sou tit, chif oswa logo.
- **Konpozisyon Kadans** : Kadans: `"sounds": [{"src": "sfx:impact-metal"}]` oswa `sfx:impact-wood` + `sfx.hit: true`.
- **Obligasyon AI** : Sou chak tit / chif gwo ki tonbe.

#### 193. `/soundglitch` — Son Glitch Dijital
- **Wòl** : Bri dijital koupe pou tranzisyon tech/glitch.
- **Konpozisyon Kadans** : Kadans: ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «digital glitch stutter short»; dire 0.2-0.4 s.
- **Obligasyon AI** : Toujou ansanm ak yon efè vizyèl glitch (/glitchcut, /effectglitchtext…).

#### 194. `/soundcamera` — Obtirasyon Kamera (Shutter)
- **Wòl** : Son foto pou chanjman imaj / slideshow.
- **Konpozisyon Kadans** : Kadans: ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «camera shutter click» + flash /dipwhite kout.
- **Obligasyon AI** : Yon klik pa foto ki parèt.

#### 195. `/soundpop` — Pop
- **Wòl** : Ti son pop pou eleman ki parèt (ikòn, bul, chip).
- **Konpozisyon Kadans** : Kadans: `sfx.pop: true` oswa `sfx:cartoon-pop`.
- **Obligasyon AI** : Yon pop pa eleman ki parèt; volim ba (-12 dB) pou pa fatige.

#### 196. `/soundswipe` — Swipe / Swoosh Rapid
- **Wòl** : Son glisman pou slide, whip pan, kat.
- **Konpozisyon Kadans** : Kadans: `sfx.whoosh: true` (sou chak tranzisyon) oswa `sfx:cloth` pou glisman dous.
- **Obligasyon AI** : Chak tranzisyon slide/whip dwe gen swoosh la.

#### 197. `/soundreverse` — Son Envèse (Reverse Swell)
- **Wòl** : Son ki aspire anvan koupe a (reverse cymbal).
- **Konpozisyon Kadans** : Kadans: ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «reverse cymbal swell 1.5 seconds»; fini sou koupe a.
- **Obligasyon AI** : Fen son an = moman koupe a egzakteman.

#### 198. `/soundmagic` — Son Majik (Shimmer)
- **Wòl** : Son klere pou revelasyon, transfòmasyon, avan/apre.
- **Konpozisyon Kadans** : Kadans: `"sounds": [{"src": "sfx:magic-sparkle"}]`.
- **Obligasyon AI** : Sync ak patikil / limyè ki parèt.

#### 199. `/soundcash` — Son Lajan (Cash / Kès)
- **Wòl** : Son pou pri, rabè, vant, fintech.
- **Konpozisyon Kadans** : Kadans: `"sounds": [{"src": "sfx:coins"}]` + ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «cash register ka-ching».
- **Obligasyon AI** : Sou chak pri / rabè ki parèt.

#### 200. `/soundtapestop` — Tape Stop
- **Wòl** : Mizik la ralanti epi kanpe tankou yon kasèt (efè komik / chòk).
- **Konpozisyon Kadans** : Kadans: ElevenLabs SFX (was_voice_engine sfx) sove nan `medya/son/`, epi `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` prompt «tape stop slow down effect»; koupe mizik la (`music` fade 0.1 s) nan menm moman an.
- **Obligasyon AI** : Mizik la DWE kanpe vre apre efè a.

#### 201. `/soundsilence` — Silans Dramatik
- **Wòl** : Koupe tout son 0.5-1.5 s anvan yon gwo revelasyon.
- **Konpozisyon Kadans** : Kadans: mizik `fade` → 0 ak vwa an poz, okenn sfx pandan silans lan, epi /soundepic oswa /sounddrop apre.
- **Obligasyon AI** : Silans lan dwe total (mizik + sfx); pa plis pase 1.5 s.

---

## 4. EGZANP PROMPTS KONBINE SOU SÈN REYÈL (STACKING PRESETS)

Men kèk egzanp kijan yon devlopè ka anpile kòmand sa yo nan Chat AI WASDEV pou pwodui videyo kalite siperyè :

### Egzanp 1 : Piblisite Lojisyèl Entènasyonal (SaaS / IDE)
```text
/videostudiopro /effectglasswidget /effectchecklist /effectaudiowaveform /effectkinetictext /effectctaultimate /effectoutrologos
Mwen bezwen yon videyo 60 segonn pou lanse WASDEV IDE v5.0. Montre vitès li, modil Docs Editor ak Kadans, epi fini ak yon gwo CTA pou telechaje l sou granlaku.com.
```

### Egzanp 2 : Dokimantè Istorik / Kiltirèl
```text
/effectdocumentary /effectcinema /effectparallaxdepth /effectsmoke /effectlightrays /effectwordhighlight
Fè yon videyo dokimantè 90 segonn sou istwa revolisyon Ayiti 1804 ak batay Vètyè, ak vwa Kreyòl pwofon, foto achiv ki gen efè Ken Burns, ak mizik sinematik espwa.
```

### Egzanp 3 : Reel / TikTok Viral pou Rezo Sosyal
```text
/effectsocialreel /effecthookpunch /effectwordhighlight /effectglitchtext /effectbeatdrop /effectemojipop
Fè yon videyo vètikal 30 segonn ki eksplike 3 rezon poukisa yon devlopè pa dwe janm sèvi ak lojisyèl ki bloke l, ak sou-tit ki chanje koulè sou chak mo ak yon kout bas sou chak pwen.
```

### Egzanp 4 : Demonstrasyon Teknik & Kòd
```text
/effecttutorialpro /effectmatrixgrid /effecttypewriter /effectdeviceframe /effectsoundui /effectsolutionswitch
Fè yon videyo demonstrasyon sou kijan pou itilize usbipd ak WSL pou flache yon tablèt Rockchip nan WASDEV san okenn erè.
```

### Egzanp 5 : Pub Magazen Lokal ak Kat (Motion + Pub)
```text
/motiondesign /pubstore /zoommap /pubflashsale /countermotion /pubjingle
Fè yon pub 20 segonn pou Boutik Lakay nan Petyonvil: -30% sou tout soulye jiska samdi, montre kote magazen an ye sou kat la, epi fini ak nimewo WhatsApp la.
```

### Egzanp 6 : Lansman App ak Motion Graphics
```text
/motiongraphic /morphism /uimotion /pubapp /logoreveal /pubbumper
Yon bumper 6 segonn epi yon vèsyon 30 segonn pou lanse app LakouPay: 3 fonksyon prensipal, badj App Store / Google Play, logo final.
```

### Egzanp 7 : Tranzisyon & Son (Pub Rapid)
```text
/pubproduct /zoomin /whippan /glitchcut /soundhot /soundswipe /soundriser /sounddrop
Pub 15 segonn pou nouvo soulye Lakay Sport: 4 plan pwodwi, chak koupe ak yon tranzisyon diferan, riser anvan revelasyon pri a, drop sou logo final la.
```

---

## 5. REZIME POU TOUT MOTÈ AI

Fichye sa a se **SOUS INIK VERITE A** pou tout efè videyo nan Kadans. Depi yon kòmand slash ki kòmanse ak `/effect*`, `/video*`, `/stickman*`, `/perso*`, `/ad*`, `/story*`, `/motion*`, `/pub*`, `/morphism`, `/zoommap` (ak tout lòt kòmand nan katalòg la) parèt nan chat la, tout modèl AI dwe aliyen konpozisyon vizyèl la ak espesifikasyon ki nan dokiman sa a obligatwaman.
