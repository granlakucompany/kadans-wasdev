# Kadans WASDEV — 201 Skills Vidéo Professionnels (Édition Française)

> Documentation officielle complète des 201 compétences vidéo Kadans pour WASDEV.

---

## Catégorie A : Modes Studio & Formats de Réalisation

### 001. `/videostudiopro` — Production Studio Professionnelle

- **Rôle** : Élever la vidéo au standard d'un studio d'émission télévisée haut de gamme.
- **Composition Kadans** : Éclairage 3 points (Key light, Fill light, Rim light violet), ombres douces `box-shadow: 0 30px 60px rgba(0,0,0,0.5)`, micro-réflexions sur les éléments, titres à animation cinétique 60 FPS, étalonnage colorimétrique professionnel.
- **Obligation IA** : Injecter la classe `.studio-pro` dans `spec.json` avec du CSS avancé pour l'étalonnage des couleurs, un cadrage raffiné et des titres centrés offrant un large espace de respiration.

### 002. `/effectdocumentary` — Style Documentaire Cinématique

- **Rôle** : Créer une atmosphère documentaire immersive (qualité Netflix / National Geographic).
- **Composition Kadans** : Effet Ken Burns (zoom lent de 1.05x sur 6 secondes sur les images et archives), typographie avec empattement (serif) ou grotesque élégante, tons chauds avec contraste adouci, titre en bas à droite avec date/lieu.
- **Obligation IA** : Toutes les images doivent comporter une animation `ken-burns` fluide, la voix doit inclure des silences naturels entre les phrases, et l'ambiance sonore doit être posée avec une réverbération subtile.

### 003. `/effectcinema` — Cinématique Anamorphique 21:9

- **Rôle** : Donner à la vidéo l'allure d'un véritable film de cinéma grand écran.
- **Composition Kadans** : Format anamorphique 2.39:1 avec bandes noires (letterbox) en haut et en bas, fréquence fluide de 24 FPS ou 60 FPS, étalonnage couleur Teal & Orange (`#0284c7` dans les ombres, `#f97316` dans les hautes lumières), léger grain pellicule 35mm.
- **Obligation IA** : Ajouter la couche `.cinematic-letterbox`, des filtres de colorimétrie cinéma et des mouvements de caméra lents sans transitions brutales.

### 004. `/effectcommercial` — Publicité Produit à Fort Impact

- **Rôle** : Structurer une publicité percutante pour produit ou marque personnelle, conçue pour captiver et convertir rapidement.
- **Composition Kadans** : Rythme soutenu (1,5 à 2,5 secondes par scène), titres percutants en gros caractères, couleurs de marque dynamiques, démonstration produit avec zooms rapides, appel à l'action (CTA) éclatant à la fin.
- **Obligation IA** : Les scènes doivent être courtes, les phrases directes et percutantes, et chaque plan doit comporter un mouvement visuel continu.

### 005. `/effectsocialreel` — Format Vertical 9:16 (Shorts, Reels, TikTok)

- **Rôle** : Optimiser la vidéo pour la consommation mobile au format vertical.
- **Composition Kadans** : Résolution 1080x1920 (9:16), zone de sécurité centrale (évitant les boutons de mention j'aime et de commentaires sur les bords), sous-titres dynamiques bien visibles au centre, animations rythmées captant le regard.
- **Obligation IA** : Forcer `ratio: "9:16"` dans la spec, positionner tous les éléments clés entre 20% et 80% de la hauteur de l'écran.

### 006. `/effectexplainer` — Vidéo Explicative & Didactique

- **Rôle** : Vulgariser et expliquer clairement un système complexe, une idée ou une application.
- **Composition Kadans** : Arrière-plan épuré et neutre, icônes vectorielles SVG apparaissant pas à pas, flèches reliant les concepts, encadrés récapitulatifs mettant en valeur les points clés.
- **Obligation IA** : Utiliser l'animation `.draw-path` sur les lignes de connexion, regrouper les idées en blocs numérotés 1, 2, 3 distincts.

### 007. `/effectnewsroom` — Journal Télévisé & Flash Info

- **Rôle** : Conférer à la vidéo l'habillage visuel d'une grande chaîne d'information en direct.
- **Composition Kadans** : Bandeau défilant en continu en bas d'écran (News Ticker), badge `FLASH INFO` ou `LIVE` clignotant en rouge, écran partagé (Split Screen) pour les interviews.
- **Obligation IA** : Intégrer le bandeau défilant `.news-ticker-bar` avec texte animé de droite à gauche, badge horaire et bandeaux de titres d'actualité en bas.

### 008. `/effectpodcastclip` — Extrait de Podcast avec Visualisation Audio

- **Rôle** : Transformer un échange audio en une vidéo dynamique adaptée aux réseaux sociaux.
- **Composition Kadans** : Portraits photo ou vidéo des intervenants dans des cadres circulaires ou en verre dépoli, forme d'onde audio animée au centre de l'écran, sous-titres dynamiques changeant de couleur mot à mot.
- **Obligation IA** : Intégrer `.audio-waveform-canvas`, afficher le nom de chaque intervenant et le titre de l'épisode dans un encadré soigné.

### 009. `/effecttutorialpro` — Démonstration Logicielle & Guide Pas à Pas

- **Rôle** : Guider l'utilisateur avec précision dans l'utilisation d'un logiciel ou d'un système.
- **Composition Kadans** : Capture d'écran du logiciel en gros plan, curseur de souris animé se déplaçant et cliquant avec halo jaune/bleu, zooms ciblés sur les zones d'action.
- **Obligation IA** : Ajouter l'élément `.cursor-pointer` avec animations `translate` et `scale(0.9)` sur les clics, assorti d'une bulle explicative latérale.

### 010. `/effectproductshowcase` — Vitrine Produit 3D avec Rotation

- **Rôle** : Mettre en valeur un produit physique ou un packaging logiciel sous tous ses angles.
- **Composition Kadans** : Objet centré en rotation lente dans l'espace 3D (`transform: rotateY()`), reflets de lumière balayant sa surface, points d'intérêt interactifs (hotspots) illuminés tout autour.
- **Obligation IA** : Appliquer la perspective CSS 3D (`perspective: 1200px`), un éclairage en dégradé sur l'objet et des lignes indicatrices menant aux caractéristiques techniques.

---

## Catégorie B : Effets Visuels, UI & Widgets Glass

### 011. `/effectglasswidget` — Boîtes en Verre Dépoli (Glassmorphism)

- **Rôle** : Donner à tous les conteneurs d'information un aspect moderne en verre translucide.
- **Composition Kadans** : `background: rgba(255, 255, 255, 0.07)`, `backdrop-filter: blur(25px)`, bordure `1px solid rgba(255, 255, 255, 0.18)`, ombre diffuse `0 20px 40px rgba(0,0,0,0.37)`.
- **Obligation IA** : Envelopper les cartes et sections dans la classe `.glass-card` avec reflet lumineux blanc le long du bord supérieur.

### 012. `/effectchecklist` — Liste de Tâches Animée avec Validation Automatique

- **Rôle** : Illustrer une progression d'objectifs validés les uns après les autres.
- **Composition Kadans** : Chaque ligne émerge du bas, la case se coche avec une animation vert vif (`#10b981`), un trait vert traçant la coche (`✓`), et le texte s'illuminant d'un éclat de validation.
- **Obligation IA** : Créer les éléments `.checklist-item` où chaque ligne bénéficie d'un délai d'animation séquentiel (`delay: index * 0.4s`).

### 013. `/effectorbit` — Éléments en Orbite Autour d'un Cœur 3D

- **Rôle** : Symboliser un écosystème, des satellites ou des technologies interconnectées.
- **Composition Kadans** : Un noyau central (logo ou produit) et 3 à 6 icônes ou cartes miniatures en révolution sur une ellipse 3D avec profondeur sur l'axe Z.
- **Obligation IA** : Intégrer `.orbit-container` avec l'animation `keyframes orbit3d`, ajustant l'échelle et l'opacité selon que les éléments passent devant ou derrière le noyau.

### 014. `/effectisometric3d` — Vue Isométrique 3D avec Couches Empilées

- **Rôle** : Représenter l'architecture logicielle, les paliers de sécurité ou les couches de données en 3D.
- **Composition Kadans** : `transform: rotateX(60deg) rotateZ(-45deg)`, plans dissociés dans l'espace sur l'axe vertical Z (`translateZ(40px)`), ombres portées sous chaque niveau.
- **Obligation IA** : Dessiner 3 à 4 couches isométriques s'élevant depuis la base pour illustrer la construction modulaire du système.

### 015. `/effectdeviceframe` — Mockup Réaliste de Téléphone ou Ordinateur Portable

- **Rôle** : Présenter une application web ou mobile intégrée dans un véritable appareil.
- **Composition Kadans** : Mockup d'iPhone 16 Pro ou MacBook Pro avec contours métallisés, reflets sur l'écran, et capture vidéo/web défilant à l'intérieur de l'écran.
- **Obligation IA** : Intégrer le cadre `.device-mockup` avec une zone d'écran rognée avec précision (`overflow: hidden; border-radius: 40px`).

### 016. `/effectdatabubbles` — Bulles de Données Flottantes avec Métriques

- **Rôle** : Donner l'impression d'un système intelligent traitant des flux d'informations en temps réel.
- **Composition Kadans** : Petites sphères ou pilules luminescentes s'élevant doucement avec de légères oscillations, affichant chacune une métrique (ex: `+45%`, `99.9%`, `4K`, `AI`).
- **Obligation IA** : Générer les particules `.data-bubble` avec une animation de flottement sinusoïdale naturelle (`sine`) à vitesses différenciées.

### 017. `/effectcardstack` — Pile de Cartes Coulissantes (Card Stack)

- **Rôle** : Présenter plusieurs témoignages, fonctionnalités ou visuels qui défilent à la manière d'un jeu de cartes.
- **Composition Kadans** : 3 cartes superposées en boîte perspective, la première carte glissant sur le côté ou vers le haut pour révéler la suivante.
- **Obligation IA** : Exploiter des transitions dynamiques `translateY` et `rotate` pour reproduire un comportement physique naturel.

### 018. `/effecttimelineprog` — Frise Chronologique Pas à Pas

- **Rôle** : Illustrer l'évolution d'un projet, une feuille de route (roadmap) ou les phases successives d'un processus.
- **Composition Kadans** : Ligne lumineuse se traçant de gauche à droite ou de haut en bas, chaque nœud s'illuminant au passage du faisceau avec date ou titre d'étape.
- **Obligation IA** : Intégrer `.timeline-track` avec une jauge de progression `.timeline-fill` s'étirant de 0% à 100%.

### 019. `/effectglowbadge` — Badge Luminescent à Contours Éclatants

- **Rôle** : Mettre en exergue un mot-clé fort tel que «NOUVEAU», «OFFICIEL», «PREMIUM» ou «PRO».
- **Composition Kadans** : Étiquette compacte bordée d'un néon à halo pulsant (`box-shadow: 0 0 20px var(--neon-color)`), typographie grasse en majuscules.
- **Obligation IA** : Apposer le badge `.badge-glow` doté d'une animation continue `pulse-glow` sur un cycle de 2 secondes sur l'élément phare.

### 020. `/effectstatscounter` — Compteur de Statistiques Accéléré

- **Rôle** : Apporter la preuve de résultats marquants grâce à un défilement chiffré partant de 0 jusqu'à la valeur cible.
- **Composition Kadans** : Chiffres géants s'incrémentant rapidement sur 1,5 seconde avec décélération finale (ease-out), accompagnés de symboles `%`, `+` ou `$` aux teintes vives.
- **Obligation IA** : Exploiter un script de comptage WAAPI ou des séquences numériques Kadans pour synchroniser la montée des valeurs avec un discret clic sonore.

### 021. `/effectnotifalert` — Notification Mobile / Desktop Déroulante

- **Rôle** : Simuler la réception d'un message prioritaire, d'une conversion de vente ou d'une alerte système.
- **Composition Kadans** : Bulle de notification rectangulaire en verre dépoli glissant depuis le haut de l'écran avec un rebond élastique subtil, comprenant icône d'application, nom, texte et horodatage.
- **Obligation IA** : Créer `.notification-popup` avec la courbe d'animation `cubic-bezier(0.175, 0.885, 0.32, 1.275)` pour calibrer l'effet élastique.

### 022. `/effectsearchbar` — Barre de Recherche avec Saisie Automatique

- **Rôle** : Formuler la question que se pose l'internaute ou illustrer une recherche active de solution.
- **Composition Kadans** : Barre de recherche épurée avec icône loupe, texte tapé caractère par caractère avec curseur clignotant, clic sur le bouton de recherche puis affichage instantané du résultat en dessous.
- **Obligation IA** : Utiliser la séquence `.typing-input` avec temporisation par lettre, enchaînée d'une transition d'ouverture immédiate des résultats.

### 023. `/effectcomparecards` — Cartes Comparatives Avant / Après avec Curseur (Splitter)

- **Rôle** : Révéler le contraste saisissant entre les méthodes obsolètes et la nouvelle solution WASDEV.
- **Composition Kadans** : Deux cartes côte à côte (Rouge / Vert ou Gris / Couleur), ou une vue unique scindée par un séparateur vertical coulissant dévoilant l'amélioration.
- **Obligation IA** : Bâtir une comparaison explicite intégrant l'icône `✗` pour les contraintes passées et `✓` pour les solutions nouvelles.

### 024. `/effectpiechart3d` — Graphique à Barres & Camembert Animés

- **Rôle** : Visualiser des données de marché, des ratios de rentabilité ou des indicateurs de performance.
- **Composition Kadans** : Barres de progression s'élevant depuis la base avec couleurs distinctives, ou diagramme circulaire SVG traçant ses segments avec étiquettes flottantes.
- **Obligation IA** : Tracer le graphique avec des propriétés SVG `stroke-dasharray` animées de 0 jusqu'à la valeur cible en pourcentage.

### 025. `/effectmatrixgrid` — Grille Technique & Coordonnées Futuristes

- **Rôle** : Instaurer une esthétique haute technologie, évoquant du code sophistiqué ou un poste de commande sécurisé.
- **Composition Kadans** : Quadrillage filaire cyan ou vert sur fond noir profond, intersections illuminées de micro-points de repère, coordonnées chiffrées défilant en bordure.
- **Obligation IA** : Ajouter la surcouche `.tech-grid-overlay` en perspective avec translation fluide continue le long de l'axe Y.

---

## Catégorie C : Animation Typographique & Texte Cinétique

### 026. `/effectkinetictext` — Texte Cinétique Explosif en Rythme

- **Rôle** : Faire apparaître chaque mot avec une énergie percutante parfaitement synchronisée avec le rythme musical.
- **Composition Kadans** : Les mots sautent, s'élargissent, tournent et changent de graisse (Light -> Black 900) sur chaque temps de la musique.
- **Obligation IA** : Découper le texte mot par mot, appliquer des animations rapides séquentielles de `scale` et `rotation`.

### 027. `/effecttypewriter` — Machine à Écrire Mécanique

- **Rôle** : Écrire le texte à la manière d'un rapport confidentiel, d'un terminal de code ou d'un récit en cours de rédaction.
- **Composition Kadans** : Les lettres apparaissent l'une après l'autre à vitesse constante (~40ms par lettre), avec un curseur rectangulaire noir/vert clignotant en fin de phrase.
- **Obligation IA** : Utiliser la séquence `.char-reveal` avec des sons de frappes de clavier synchronisés.

### 028. `/effecttextgradient` — Texte Dégradé Aurore en Mouvement

- **Rôle** : Conférer aux grands titres un éclat extraordinaire grâce à un flux liquide de couleurs circulant à l'intérieur des lettres.
- **Composition Kadans** : `background: linear-gradient(135deg, #10b981, #0098ff, #ec4899, #8b5cf6)`, `background-clip: text`, `-webkit-text-fill-color: transparent`, animation `background-position` de 8 secondes.
- **Obligation IA** : Appliquer la classe `.gradient-text-animated` sur tous les grands titres principaux.

### 029. `/effectmaskedtext` — Texte Révélé par Masque Géométrique

- **Rôle** : Faire émerger le texte depuis le bas d'une ligne invisible sans aucun débordement.
- **Composition Kadans** : Un conteneur doté de `overflow: hidden`, où le texte s'élève de `translateY(100%)` à `translateY(0)` avec une transition ultra-fluide.
- **Obligation IA** : Envelopper chaque ligne de texte dans une balise `.mask-container` pour une apparition nette sans débordement.

### 030. `/effectwordhighlight` — Mots Surlignés en Temps Réel avec la Voix (Karaoké Pro)

- **Rôle** : Guider le regard de l'audience sur chaque mot précisément au moment où l'orateur le prononce.
- **Composition Kadans** : La phrase entière s'affiche en gris clair, puis chaque mot s'illumine en jaune vif, vert ou bleu dès que la voix l'atteint (d'après les horodatages Whisper).
- **Obligation IA** : Utiliser les données `.words.json` pour appliquer la classe `.active-word` à la milliseconde exacte.

### 031. `/effect3dtextfloat` — Grand Texte 3D Flottant dans les Airs

- **Rôle** : Créer un sentiment de puissance et de masse physique pour les titres clés.
- **Composition Kadans** : Texte doté de multiples couches `text-shadow` créant une épaisseur 3D réaliste, pivotant doucement dans un espace 3D.
- **Obligation IA** : Ajouter `text-shadow: 0 1px 0 #ccc, 0 2px 0 #c9c9c9, 0 3px 0 #bbb, 0 4px 0 #b9b9b9, 0 10px 20px rgba(0,0,0,0.4)` avec rotation 3D.

### 032. `/effectneontext` — Texte Néon Scintillant (Flicker) et Lumineux

- **Rôle** : Ambiance nocturne urbaine, cité futuriste ou esthétique rétro-wave.
- **Composition Kadans** : Teintes rose, cyan ou orange avec intense halo lumineux, accompagnées d'un léger vacillement (flicker) initial comme un tube de néon qui s'allume.
- **Obligation IA** : Appliquer `@keyframes neon-flicker` avec ombrages multiples `text-shadow: 0 0 10px, 0 0 20px, 0 0 40px`.

### 033. `/effectglitchtext` — Texte Numérique Déstructuré (RGB Split)

- **Rôle** : Scènes de piratage, séquences de sécurité, alertes système ou actions technologiques intenses.
- **Composition Kadans** : Le texte se scinde en deux répliques (rouge et cyan) décalées horizontalement pendant quelques millisecondes avec des découpes en tranches horizontales.
- **Obligation IA** : Utiliser les pseudo-classes `::before` et `::after` avec `clip-path` pour découper les tranches du glitch.

### 034. `/effectoutlinetext` — Texte Contour avec Remplissage Progressif

- **Rôle** : Typographie éditoriale de mode ou style architectural minimaliste ultra-tendance.
- **Composition Kadans** : Le texte débute avec un simple contour `-webkit-text-stroke: 2px white` sans remplissage, puis la couleur s'élève depuis le bas tel un liquide pour le combler.
- **Obligation IA** : Animer le remplissage de couleur avec un dégradé de bas en haut sur 1 seconde.

### 035. `/effectflipboard` — Caractères Mécaniques à Volets (Panneau d'Aéroport)

- **Rôle** : Permuter un mot par un autre avec un effet mécanique particulièrement satisfaisant.
- **Composition Kadans** : Chaque lettre se divise en deux volets qui basculent en 3D de haut en bas pour dévoiler le nouveau caractère.
- **Obligation IA** : Créer un conteneur `.flip-char` avec une rotation `rotateX(-90deg)` séquentielle sur chaque caractère.

### 036. `/effectsupersize` — Mot Géant en Arrière-Plan Derrière le Sujet

- **Rôle** : Donner de la profondeur à la scène avec un mot gigantesque placé derrière le personnage ou le produit.
- **Composition Kadans** : Texte d'une taille de 200px à 300px à 10% d'opacité, se déplaçant lentement dans la direction opposée à la caméra.
- **Obligation IA** : Positionner le texte avec `z-index: 1`, une opacité de `0.08` et un mouvement parallaxe continu.

### 037. `/effectstampbold` — Mot Frappé au Tampon avec Secousse d'Impact

- **Rôle** : Confirmer une décision, une vérité irréfutable ou une victoire (« GARANTI », « APPROUVÉ », « CERTIFIÉ »).
- **Composition Kadans** : Le mot surgit à très grande échelle sans transparence, chute violemment en provoquant une secousse d'écran assortie d'un son d'impact percutant.
- **Obligation IA** : Appliquer l'animation `scale(3) -> scale(1)` et `camerashake` de 0.2 seconde lors de l'impact.

---

## Catégorie D : Particules, Ambiances & Effets Spéciaux

### 038. `/effectparticles` — Poussière d'Étoiles et Étincelles Flottantes

- **Rôle** : Donner vie à la scène avec une touche de féerie ou une sérénité technologique.
- **Composition Kadans** : 40 à 60 particules luminescentes blanches et violettes s'élevant délicatement selon un mouvement brownien sur Canvas 2D.
- **Obligation IA** : Intégrer le calque Canvas `.particles-canvas` en arrière-plan sans surcharger le processeur.

### 039. `/effectsmoke` — Fumée Dense et Vapeur Réaliste

- **Rôle** : Instaurer du mystère, une profondeur dramatique ou l'ambiance scénique d'un concert.
- **Composition Kadans** : Volutes de fumée diffuse ondulant du bas vers le haut avec motifs fractals et fusion `mix-blend-mode: screen`.
- **Obligation IA** : Ajouter le calque `.smoke-overlay` avec animations douces de flou et d'opacité.

### 040. `/effectsplashemboss` — Éclaboussure de Liquide et Encre

- **Rôle** : Transition énergique ou présentation artistique avec projections vives de peinture et de liquide.
- **Composition Kadans** : Formes fluides en SVG composant des gouttelettes ou des taches d'encre qui se déploient vivement depuis le centre.
- **Obligation IA** : Intégrer les formes `.splash-blob` avec cinématique élastique pour ouvrir la scène.

### 041. `/effectcyberpunkcity` — Ville Nocturne Cyberpunk aux Lumières Néon

- **Rôle** : Ambiance nocturne haute technologie aux éclairages rose fuchsia et bleu cyan.
- **Composition Kadans** : Fond sombre noir et bleu nuit, reflets sur asphalte mouillé, faisceaux de néon verticaux et câbles aériens suspendus.
- **Obligation IA** : Harmoniser les teintes `#ec4899` et `#0098ff` sur toutes les ombres et reflets lumineux.

### 042. `/effectmatrixrain` — Pluie de Code Verticale Matrix

- **Rôle** : Évoquer l'exécution de code, des algorithmes ou des protocoles de sécurité en arrière-plan.
- **Composition Kadans** : Colonnes de caractères katakana ou alphanumériques verts défilant sur fond noir avec traînées luminescentes.
- **Obligation IA** : Intégrer le Canvas `.matrix-rain` avec caractères verts `#10b981` et têtes de piste blanches luminescentes.

### 043. `/effectlightrays` — Rayons Solaires Volumétriques (God Rays)

- **Rôle** : Inspirer l'espoir, la grandeur, l'accomplissement ou une clarté quasi-spirituelle.
- **Composition Kadans** : Faisceaux coniques de lumière émanant du coin supérieur droit ou gauche traversant la scène, parsemés de poussières scintillantes.
- **Obligation IA** : Ajouter le calque `.volumetric-rays` avec `mix-blend-mode: color-dodge` et micro-animation de rotation.

### 044. `/effectfireflare` — Reflet Optique Cinématique (Lens Flare Anamorphique)

- **Rôle** : Apporter une signature cinématographique authentique lorsque la caméra s'oriente face à une source lumineuse.
- **Composition Kadans** : Éclats horizontaux bleus anamorphiques et halos lumineux traversant l'écran au fil des mouvements de caméra.
- **Obligation IA** : Appliquer `.anamorphic-flare` glissant horizontalement lors des transitions de scènes.

### 045. `/effectspacecosmos` — Galaxies, Nébuleuses et Espace Lointain

- **Rôle** : Pour projets visionnaires, ambitions d'envergure galactique ou concepts d'avenir.
- **Composition Kadans** : Champ d'étoiles scintillantes, nébuleuses violettes et bleues en douce rotation, et étoiles filantes traversant ponctuellement l'écran.
- **Obligation IA** : Générer une profondeur à 3 plans d'étoiles (petites, moyennes, grandes) défilant à vitesses différenciées.

### 046. `/effectglitchcyber` — Bruit de Signal et Scanlines Cathodiques (CRT)

- **Rôle** : Scènes de rupture, d'alerte, de cassure de rythme ou ambiance rétro-futuriste.
- **Composition Kadans** : Lignes horizontales scanlines, léger souffle de neige cathodique et désynchronisation verticale fugitive de 0.3 seconde.
- **Obligation IA** : Appliquer le calque `.crt-scanlines` avec une micro-vibration verticale rapide.

### 047. `/effectbokehglow` — Disques de Flou Artistique (Bokeh f/1.4)

- **Rôle** : Ambiance chaleureuse, intime et haut de gamme avec profondeur de champ cinématographique.
- **Composition Kadans** : Disques lumineux floutés s'élevant délicatement en arrière-plan sous des nuances pastel chaleureuses.
- **Obligation IA** : Créer des orbes `.bokeh-orb` avec `filter: blur(12px)` et opacités variables.

### 048. `/effectshockwave` — Onde de Choc Circulaire à l'Impact

- **Rôle** : Accentuer un moment fort, une annonce explosive ou une décision déterminante.
- **Composition Kadans** : Un cercle translucide en expansion fulgurante depuis le centre de l'écran, générant une distorsion optique de l'arrière-plan.
- **Obligation IA** : Animer `.shockwave-ring` avec `transform: scale(0) -> scale(4)` et évanouissement de l'opacité en 0.4s.

### 049. `/effectembersfire` — Braises et Étincelles Émergentes

- **Rôle** : Insuffler passion, puissance brute, chaleur ardente et intensité d'action.
- **Composition Kadans** : Micro-escarbilles rougeoiantes, jaunes et orangées tourbillonnant vers le haut comme issues d'un brasier ou d'une forge.
- **Obligation IA** : Intégrer les particules de braises `.fire-embers` avec lueur chaleureuse rasante au bas de l'écran.

---

## Catégorie E : Mouvements de Caméra & Dynamique Spatiale

### 050. `/effectdollyzoom` — Effet Vertigo (Dolly Zoom d'Hitchcock)

- **Rôle** : Provoquer un sentiment de choc psychologique ou une prise de conscience foudroyante.
- **Composition Kadans** : Recul de la caméra combiné à un zoom avant sur le sujet : le sujet conserve sa taille apparente pendant que l'arrière-plan s'étire et semble s'éloigner.
- **Obligation IA** : Combiner `scale()` sur le sujet en direction inverse avec le `scale()` de l'arrière-plan.

### 051. `/effectcamerashake` — Secousse Dynamique de Caméra

- **Rôle** : Simuler un impact physique, un séisme ou une lourde frappe de basse musicale.
- **Composition Kadans** : La caméra vibre sur les axes X et Y pendant 0.2 à 0.5 seconde avec un amortissement rapide (decay).
- **Obligation IA** : Appliquer `@keyframes camera-shake` et `transform: translate(random, random)` sur l'ensemble du conteneur principal.

### 052. `/effectparallaxdepth` — Parallaxe 2.5D Couche par Couche

- **Rôle** : Transformer une image plate ou une illustration en un véritable univers 3D doté de profondeur.
- **Composition Kadans** : Le premier plan se déplace rapidement, le plan intermédiaire à vitesse normale et l'arrière-plan très lentement lorsque la caméra pivote.
- **Obligation IA** : Séparer les éléments en 3 calques `.layer-fg`, `.layer-mg`, `.layer-bg` avec des coefficients de vitesse distincts.

### 053. `/effectpanoramicsweep` — Balayage Panoramique Large

- **Rôle** : Montrer l'envergure d'un projet, d'un espace de travail, d'un paysage ou d'une équipe complète.
- **Composition Kadans** : La caméra glisse de manière stable de gauche à droite sur une composition ultra-large (ultra-wide canvas) à vitesse constante, avec un ralenti progressif en fin de course.
- **Obligation IA** : Animer `translateX()` sur le grand conteneur pendant 4 à 6 secondes.

### 054. `/effectcrashzoom` — Zoom Éclair sur un Détail

- **Rôle** : Passer d'un plan d'ensemble pour atterrir brutalement sur un détail clé (un bouton, un visage, une ligne de code).
- **Composition Kadans** : Zoom de 1x à 4x en moins de 0.4 seconde avec un léger flou de mouvement (motion blur).
- **Obligation IA** : Appliquer `scale(4)` et `transform-origin` précisément sur les coordonnées de l'élément cible.

### 055. `/effectorbitcam` — Caméra Orbitale Autour du Sujet

- **Rôle** : Présentation dynamique d'un personnage ou d'un produit tout en le maintenant centré.
- **Composition Kadans** : La caméra effectue une révolution de 180° ou 360° autour du sujet pendant que l'éclairage se déplace sur sa surface.
- **Obligation IA** : Utiliser une perspective 3D centrée et une animation `rotateY` continue.

### 056. `/effectfirstperson` — Vue à la Première Personne (POV)

- **Rôle** : Placer le spectateur dans la peau de l'utilisateur ou du personnage principal.
- **Composition Kadans** : Léger balancement naturel de la marche (head bobbing), mains apparaissant au bas de l'écran pour cliquer ou manipuler les objets.
- **Obligation IA** : Ajouter de légers mouvements de rotation de 0.2 degré et un déplacement vertical Y calé sur le rythme de marche.

### 057. `/effectdroneflyover` — Survol en Drone depuis le Ciel

- **Rôle** : Introduction majestueuse descendant des nuages pour atterrir sur le sujet.
- **Composition Kadans** : Caméra en plongée vers le bas descendant tout en redressant son axe pour devenir horizontale face au projet.
- **Obligation IA** : Combiner `translateY`, `rotateX(45deg) -> rotateX(0)` et un zoom fluide.

### 058. `/effecttiltshift` — Effet Maquette Miniature (Tilt-Shift)

- **Rôle** : Donner à une ville réelle ou un grand véhicule l'allure d'une maquette miniature sur une table.
- **Composition Kadans** : Une bande étroite parfaitement nette au centre de l'écran, bordée d'un fort flou en haut et en bas, avec une saturation de couleurs accentuée.
- **Obligation IA** : Appliquer un masque de flou vertical et une saturation des couleurs `saturate(1.4)`.

### 059. `/effectwhipcamera` — Coup de Caméra Éclair (Whip Pan)

- **Rôle** : Transition énergique entre deux actions où la caméra pivote si rapidement que tout devient flou.
- **Composition Kadans** : Un balayage horizontal sec de 0.2 seconde avec un fort flou directionnel `blur(30px, 0px)` qui atterrit sur la nouvelle scène.
- **Obligation IA** : Intégrer la classe `.whip-pan-transition` entre les deux scènes.

### 060. `/effectcameraroll` — Tonneau de Caméra (Camera Roll)

- **Rôle** : Scènes d'action extrême, séquences spatiales ou moments de basculement complet.
- **Composition Kadans** : La caméra pivote de 180° ou 360° sur l'axe Z pendant que l'action continue de se dérouler au centre.
- **Obligation IA** : Animer `rotateZ()` avec un rythme accéléré au milieu et un ralenti progressif en fin de course.

### 061. `/effectslowmotion` — Ralenti Extrême (Slow-Mo 120 FPS)

- **Rôle** : Décomposer une action brève et rapide (une goutte d'eau, un sourire, une frappe de code) pour en révéler la beauté.
- **Composition Kadans** : L'action se déroule à 25 % de sa vitesse normale avec une fluidité totale de 60 FPS sans aucune saccade.
- **Obligation IA** : Augmenter la durée de la scène dans la spec et ralentir toutes les animations WAAPI d'un facteur 4x.

---

## Catégorie F : Transitions Kadans Pro

### 062. `/effectseamlesszoom` — Transition Zoom Infini

- **Rôle** : La caméra plonge dans une lettre, une fenêtre ou un regard de la première scène jusqu'à ce qu'il devienne l'arrière-plan complet de la deuxième.
- **Composition Kadans** : Zoom 1x -> 50x sur un point précis jusqu'à ce que la couleur de ce point emplisse tout l'écran pour dévoiler la scène suivante.
- **Obligation IA** : Synchroniser le point de disparition de la première scène avec le point d'ouverture de la deuxième scène.

### 063. `/effectmorphshape` — Métamorphose de Forme Fluide (Morphing)

- **Rôle** : Un logo qui devient un bouton, ou une icône qui se fond pour épouser une nouvelle forme.
- **Composition Kadans** : Un tracé `path` SVG dont les coordonnées migrent en douceur de la forme A à la forme B avec un nombre identique de points vectoriels.
- **Obligation IA** : Utiliser une animation de morphing SVG sur les tracés vectoriels.

### 064. `/effectinkbleed` — Tache d'Encre se Diffusant sur Papier (Ink Bleed)

- **Rôle** : Transition organique, artistique ou historique où l'encre noire ou teintée dévoile la scène.
- **Composition Kadans** : Masque SVG aux contours irréguliers s'élargissant comme une goutte d'eau sur du papier buvard pour faire apparaître l'image.
- **Obligation IA** : Appliquer un masque `mask-image` avec une forme liquide s'étendant depuis le centre.

### 065. `/effectglitchwipe` — Déchirure Numérique de Transition (Glitch Wipe)

- **Rôle** : Changer de scène à la manière d'un signal satellite décroché puis instantanément rétabli.
- **Composition Kadans** : La première scène se fragmente en blocs de pixels horizontaux pendant 0.2 seconde, puis la deuxième scène s'installe proprement.
- **Obligation IA** : Intégrer la transition `.glitch-wipe` avec un bref bruitage d'interférence électronique.

### 066. `/effectflashwhite` — Flash Blanc Énergique

- **Rôle** : Marquer un tournant temporel majeur ou une révélation à fort impact.
- **Composition Kadans** : L'écran devient totalement blanc pendant 3 images (~50 ms), puis s'estompe rapidement pour faire place à la nouvelle scène.
- **Obligation IA** : Superposer un calque blanc `.flash-overlay` avec une transition `opacity: 1 -> 0` en 0.3s.

### 067. `/effectdooropen` — Ouverture de Portes ou Rideaux Centraux

- **Rôle** : Introduire un nouveau chapitre ou accueillir l'audience au sein d'un nouvel environnement.
- **Composition Kadans** : Deux panneaux en verre dépoli ou noirs coulissant latéralement (à gauche et à droite) depuis la médiane.
- **Obligation IA** : Créer deux panneaux `.split-door-left` et `.split-door-right` animés avec `translateX`.

### 068. `/effectpapertear` — Déchirure de Papier Centrale

- **Rôle** : Bousculer une règle établie, déchirer un vieux contrat ou dévoiler la vérité masquée à l'arrière-plan.
- **Composition Kadans** : Ligne de déchirure irrégulière fendant de haut en bas, les deux pans de papier s'écartant sur les côtés accompagnés d'un son de déchirure.
- **Obligation IA** : Intégrer un masque SVG aux bordures déchirées réalistes avec des ombres portées sous chaque fragment.

### 069. `/effectblurzoom` — Flou Radial Accéléré (Blur Zoom)

- **Rôle** : Changer de scène en une fraction de seconde sans que l'œil n'ait le temps d'en percevoir la couture.
- **Composition Kadans** : Flou circulaire prononcé `filter: blur(20px)` combiné à un zoom rapide qui s'estompe instantanément sur la nouvelle scène.
- **Obligation IA** : Appliquer la transition `.blur-zoom-in` sur une durée de 0.35 seconde.

### 070. `/effectgeometricwipe` — Balayage Géométrique (Geometric Wipe)

- **Rôle** : Style graphique épuré, dynamique et moderne (triangles, losanges ou hexagones).
- **Composition Kadans** : Une série de petits hexagones ou triangles pivotant pour recouvrir l'écran et dévoiler la scène suivante.
- **Obligation IA** : Utiliser une grille de masques SVG s'ouvrant de façon séquentielle depuis le centre.

### 071. `/effectlumaabsorb` — Fondu par Luminance (Luma Fade)

- **Rôle** : Les parties les plus lumineuses de la première scène se dissolvent en premier, suivies par les zones sombres.
- **Composition Kadans** : Transition exploitant les valeurs de noir et blanc de chaque pixel pour créer une disparition texturée plutôt qu'un fondu plat.
- **Obligation IA** : Appliquer un filtre luma mask dans la composition Kadans.

---

## Catégorie G : Son, Audio & Synchro Rythmique

### 072. `/effectaudiowaveform` — Onde Audio Dynamique Réactive

- **Rôle** : Visualiser en temps réel le spectre sonore de la voix ou de la musique.
- **Composition Kadans** : Barres verticales ou courbes sinueuses oscillant au gré des fréquences vocales tout au long de la vidéo.
- **Obligation IA** : Intégrer `.audio-waveform-bars` avec une animation de hauteur synchronisée sur le flux audio.

### 073. `/effectbeatdrop` — Synchronisation d'Impact sur la Basse (Beat Drop)

- **Rôle** : Faire exploser ou muter toute l'animation visuelle pile au moment de l'impact de basse.
- **Composition Kadans** : Changement de scène, secousse de caméra, éclat lumineux et apparition du titre verrouillés rigoureusement sur le timestamp de la frappe de basse.
- **Obligation IA** : Aligner le point de transition dans `spec.json` sur la seconde exacte où la musique change de rythme.

### 074. `/effectsubbasshit` — Impact Sous-Basse Profond (Sub-Bass Boom)

- **Rôle** : Dégager une sensation de puissance colossale lors de l'apparition d'une solution majeure ou d'un logo.
- **Composition Kadans** : Basse lourde de 30-40 Hz résonnant pendant 2 secondes, accompagnée d'un léger tremblement d'écran.
- **Obligation IA** : Intégrer le fichier SFX de basse dans le projet et planifier la secousse visuelle au même moment.

### 075. `/effectsoundwhoosh` — Effet Sonore de Souffle Rapide (Whoosh)

- **Rôle** : Accompagner chaque translation de carte, défilement de texte ou balayage de caméra d'un souffle d'air réaliste.
- **Composition Kadans** : Bruitage de whoosh court synchronisé avec le démarrage de chaque mouvement `translateX/Y`.
- **Obligation IA** : Déposer le fichier audio whoosh dans le dossier `medya/sfx/` et l'appeler à chaque transition majeure.

### 076. `/effectsoundui` — Effets sonores de clics et pops pour éléments UI

- **Rôle** : Procurer un retour tactile gratifiant lorsqu'une boîte apparaît, qu'un bouton est cliqué ou qu'un compteur défile.
- **Composition Kadans** : Effets sonores subtils de haute qualité (pop, subtle click, bell chime, soft tap).
- **Obligation IA** : Intégrer des micro-bruitages UI à chaque apparition de carte, badge ou case cochée.

### 077. `/effectvinylwarmth` — Chaleur analogique et crépitements de vinyle

- **Rôle** : Instaurer une ambiance chaleureuse, nostalgique et rétro, évoquant une présence humaine ou une musique jazz/lo-fi.
- **Composition Kadans** : Ambiance sonore de disque vinyle avec de légers craquements discrets en arrière-plan sous la musique.
- **Obligation IA** : Ajouter la piste audio `.vinyl-crackle` à un volume de 15% sous la musique principale.

### 078. `/effectvoiceisolate` — Voix cristalline et atténuation automatique de la musique (Ducking)

- **Rôle** : Garantir une intelligibilité vocale parfaite à 100% sans que la musique ne masque les paroles de l'orateur.
- **Composition Kadans** : La musique s'atténue automatiquement à 20% de son volume dès que la voix se fait entendre, puis remonte à 70% lors des pauses.
- **Obligation IA** : Configurer la courbe de volume musical (`volume_keyframes`) dans la spec en fonction des repères temporels de la voix.

### 079. `/effectcrowdambience` — Ambiance de foule et applaudissements

- **Rôle** : Créer l'atmosphère d'un événement d'envergure, d'une conférence réussie ou d'une salle comble.
- **Composition Kadans** : Murmures discrets d'une foule en ouverture, suivis d'applaudissements et d'acclamations chaleureuses lors de l'annonce d'une victoire ou du CTA final.
- **Obligation IA** : Insérer les effets sonores de foule dans la scène d'introduction et la scène de conclusion.

### 080. `/effectheartbeatfx` — Battement de cœur accéléré générateur de tension

- **Rôle** : Maintenir l'audience en haleine pendant l'attente d'un résultat critique ou d'une solution décisive.
- **Composition Kadans** : Battement de cœur audio qui démarre lentement avant de s'accélérer, accompagné d'un léger flash rouge/noir sur chaque pulsation.
- **Obligation IA** : Synchroniser l'animation `scale(1.03) -> scale(1)` sur chaque pulsation sonore du battement de cœur.

### 081. `/effectreverbtrail` — Traîne de réverbération spatiale sur le mot final

- **Rôle** : Faire résonner durablement le slogan final ou le nom de marque dans l'esprit du spectateur après la fin de la vidéo.
- **Composition Kadans** : La dernière syllabe vocale s'éteint dans une longue traîne de réverbération spatiale (reverb tail) tandis que le logo s'illumine.
- **Obligation IA** : Appliquer un effet de réverbération sur le dernier segment audio en synchronisation avec le fondu au noir visuel.

---

## Catégorie H : Animation de Personnages & Rigging

### 082. `/effectstickmanrig` — Rig de Stickman SVG à 16 os avec synchronisation labiale (Lipsync)

- **Rôle** : Raconter une histoire simple, captivante et limpide à l'aide d'un personnage bâton animé de manière professionnelle.
- **Composition Kadans** : Stickman SVG complet doté d'un squelette à 16 os (tête, cou, torse, bras, coudes, mains, bassin, cuisses, genoux, pieds) capable de marcher, sauter, pointer l'écran et parler avec lipsync phonémique WAAPI à 60 FPS.
- **Obligation IA** : Intégrer le module SVG Rig avec les commandes de mouvement (`walk`, `jump`, `point`, `explain`).

### 083. `/effectcutout2d` — Personnage illustré en animation 2D découpée (Cut-Out)

- **Rôle** : Style d'animation moderne en papier découpé où les membres du personnage s'animent avec fluidité et élasticité.
- **Composition Kadans** : Personnage articulé en calques séparés (bras, buste, tête) reliés à des points de pivot naturels avec des expressions faciales expressives.
- **Obligation IA** : Positionner le personnage sur le côté de l'écran pour interagir avec les graphismes centraux.

### 084. `/effectavatarhost` — Présentateur virtuel en incrustation latérale

- **Rôle** : Guider le spectateur tout au long de la vidéo à la manière d'un présentateur de télévision.
- **Composition Kadans** : Avatar soigné incrusté dans un médaillon circulaire ou debout sur le côté droit de l'écran, parlant avec une gestuelle naturelle tout en exposant chaque point.
- **Obligation IA** : Maintenir l'avatar sur le côté afin qu'il ne masque jamais le texte ni les démonstrations de produit.

### 085. `/effecttalkinghead` — Tête animée avec synchronisation labiale précise au mot près

- **Rôle** : Insuffler de la vie à une illustration ou un personnage en synchronisant la bouche avec les paroles de l'orateur.
- **Composition Kadans** : Bouche SVG modulant ses formes entre les phonèmes `A`, `E`, `O`, `M`, `L` selon le minutage de chaque mot extrait du fichier `.words.json`.
- **Obligation IA** : Lier la bouche du personnage aux données phonémiques fournies par la transcription Whisper.

### 086. `/effectemojipop` — Émojis 3D surgissants autour du personnage

- **Rôle** : Ajouter de l'humour, de l'émotion et des réactions expressives aux propos du personnage.
- **Composition Kadans** : Émojis 3D (flamme 🔥, fusée 🚀, cœur ❤️, réflexion 🤔, argent 💰) jaillissant autour de la tête du personnage avec un léger effet de rebond élastique.
- **Obligation IA** : Déclencher les émojis sur les mots-clés à fort impact émotionnel.

### 087. `/effectshadowpuppet` — Silhouettes en ombres chinoises

- **Rôle** : Évoquer le style traditionnel du théâtre d'ombres chinoises pour narrer des contes, légendes ou fables culturelles.
- **Composition Kadans** : Personnages et décors arborés en silhouettes d'un noir profond sur un fond lumineux orange ou jaune de coucher de soleil.
- **Obligation IA** : Utiliser des formes SVG noires `#000000` sur un dégradé chaleureux évoquant un coucher de soleil.

### 088. `/effectmascotdance` — Mascotte célébrant sur l'appel à l'action final (CTA)

- **Rôle** : Laisser une impression finale joyeuse, mémorable et positive auprès de l'audience.
- **Composition Kadans** : Mascotte du projet esquissant une danse de victoire ou saluant le public d'un signe de la main à côté du bouton d'appel à l'action (CTA).
- **Obligation IA** : Ajouter l'animation `.dance-bounce` sur la mascotte durant les 5 dernières secondes de la vidéo.

### 089. `/effectspeechbubble` — Bulle de bande dessinée (Speech Bubble) avec texte

- **Rôle** : Illustrer les pensées intérieures d'un personnage ou ses répliques dans un style bande dessinée dynamique.
- **Composition Kadans** : Bulle blanche élégante émergeant de la bouche du personnage avec une pointe orientée vers lui, le texte apparaissant à l'intérieur.
- **Obligation IA** : Créer la bulle SVG `.speech-bubble` avec une animation `scale(0) -> scale(1)`.

### 090. `/effectgesturesmart` — Main animée pointant ou cliquant sur un élément

- **Rôle** : Diriger l'attention du spectateur vers un bouton, un tarif ou un lien d'action stratégique.
- **Composition Kadans** : Main illustrée apparaissant pour pointer un élément du doigt, simulant un appui ou un glissement avant de s'effacer avec élégance.
- **Obligation IA** : Intégrer la main `.gesture-hand` avec une trajectoire de déplacement et une micro-pression sur la zone ciblée.

### 091. `/effectcrowdsilhouette` — Silhouette de foule en bas d'écran

- **Rôle** : Simuler une vaste audience dans un stade ou une salle de conférence assistant attentivement à la présentation.
- **Composition Kadans** : Calque de silhouettes en bas d'écran représentant têtes et bras applaudissant ou brandissant des smartphones pour filmer.
- **Obligation IA** : Ajouter le calque `.crowd-silhouette-layer` en bas de l'écran avec une légère oscillation naturelle.

---

## Catégorie I : Sections Narratives & Structure de Story

### 092. `/effecthookpunch` — Accroche percutante des 3 premières secondes (Hook)

- **Rôle** : Empêcher l'utilisateur de zapper (swipe away) dès les premiers instants de la vidéo.
- **Composition Kadans** : Question provocante, visuel percutant, affirmation choc et impact sonore immersif condensés dans les 3 premières secondes.
- **Obligation IA** : La scène 1 doit être concise, percutante, visuellement dense et aborder le sujet sans aucune introduction lente.

### 093. `/effectproblemstatement` — Mise en scène du problème et des frustrations

- **Rôle** : Amener l'audience à reconnaître ses propres points de douleur pour susciter une identification immédiate.
- **Composition Kadans** : Palette de couleurs plus sombres, fond musical teinté de tension, illustrations de personnes épuisées ou de systèmes bloqués.
- **Obligation IA** : Mettre en évidence les difficultés vécues par le client avant la découverte de la solution.

### 094. `/effectsolutionswitch` — Bascule vers la solution et rupture tonale

- **Rôle** : Marquer le tournant libérateur où l'espoir renaît grâce à l'intervention du produit.
- **Composition Kadans** : Éclat lumineux instantané, couleurs vives chassant la pénombre, musique insufflant optimisme, énergie et clarté.
- **Obligation IA** : Opérer une transition tranchée d'un ton sombre vers une luminosité éclatante avec apparition magistrale du nom du produit.

### 095. `/effectfeaturecarousel` — Carrousel défilant de 3 à 5 fonctionnalités clés

- **Rôle** : Présenter l'étendue des capacités du produit de manière claire, concise et structurée.
- **Composition Kadans** : 3 à 5 cartes défilant horizontalement, chacune dotée d'une icône 3D soignée, d'un titre en 3 mots et d'une phrase de synthèse percutante.
- **Obligation IA** : Consacrer 2 à 3 secondes à chaque fonctionnalité avec une transition fluide par glissement.

### 096. `/effectsocialproof` — Témoignage client et notation 5 étoiles

- **Rôle** : Bâtir une confiance absolue en démontrant la satisfaction concrète d'utilisateurs existants.
- **Composition Kadans** : Cartes de témoignage arborant la photo du client, 5 étoiles dorées s'illuminant consécutivement (`★★★★★`) et citations concises d'entreprises ou développeurs.
- **Obligation IA** : Animer les étoiles `.star-gold` s'allumant en cascade avec avatar et nom réel d'utilisateur.

### 097. `/effectpricingtable` — Grille tarifaire avec mise en avant de l'offre populaire

- **Rôle** : Faciliter la prise de décision du client dans le choix de l'offre la plus adaptée.
- **Composition Kadans** : 2 ou 3 cartes de tarifs côte à côte, l'offre recommandée apparaissant surélevée avec un badge « LE PLUS POPULAIRE » et un contour néon étincelant.
- **Obligation IA** : Valoriser visuellement l'offre vedette par rapport aux formules alternatives.

### 098. `/effectguaranteebadge` — Badge bouclier de garantie 100% satisfait

- **Rôle** : Dissiper toute hésitation ou objection résiduelle dans l'esprit du client.
- **Composition Kadans** : Bouclier élégant aux reflets dorés et verts frappé d'un sceau de sécurité, accompagné de la mention « 100% GARANTI OU REMBOURSÉ ».
- **Obligation IA** : Faire émerger le bouclier `.guarantee-shield` avec une rotation affirmative et dynamique.

### 099. `/effecturgencytimer` — Compte à rebours d'urgence (Countdown Timer)

- **Rôle** : Inciter l'audience à passer immédiatement à l'action plutôt que de reporter sa décision.
- **Composition Kadans** : Horloge numérique affichant le décompte des minutes et secondes restantes, complétée par la mention « OFFRE LIMITÉE ».
- **Obligation IA** : Intégrer le composant `.countdown-timer` s'égrenant en temps réel durant la séquence.

### 100. `/effectctaultimate` — Appel à l'action final percutant (Ultimate CTA)

- **Rôle** : Indiquer avec une précision absolue l'action exacte à accomplir dès la fin de la vidéo.
- **Composition Kadans** : Bouton d'action proéminent pulsant des ondes lumineuses, URL du site affichée en typographie grand format, flèche indicatrice et voix off formulant la consigne directe.
- **Obligation IA** : Centrer le bouton CTA avec la classe `.btn-cta-pulse`, agrandir le lien et insérer un bouton cliquable.

### 101. `/effectoutrologos` — Logo de Fin et Signature Sonore (Audio Brand)

- **Rôle** : Conclure la vidéo avec grandeur sur l'identité officielle de la marque.
- **Composition Kadans** : Le logo montant au centre de l'écran avec un reflet lumineux glissant dessus, slogan en dessous, liens vers les réseaux sociaux et signature sonore de l'entreprise.
- **Obligation IA** : La dernière scène doit être épurée, calme, avec le logo centré sur fond sombre et le son final.

---

## Catégorie J : Motion Design & Motion Graphics

### 102. `/motiondesign` — Motion Design Professionnel Intégral

- **Rôle** : Transformer l'ensemble de la vidéo en une production motion design de qualité agence (niveau Buck / Ordinary Folk).
- **Composition Kadans** : Grille 12 colonnes, palette fixe de 3-4 couleurs, chaque élément entre avec l'easing `cubic-bezier(0.65,0,0.35,1)`, léger dépassement (overshoot), décalage (stagger) de 60-90 ms entre éléments, aucun élément ne restant statique plus de 1.2 s.
- **Obligation IA** : Toutes les scènes doivent être en vecteurs HTML/SVG éditables (pas d'images), avec un rythme d'animation constant ; ajouter la classe `.motion-pro` dans `spec.json` et utiliser le même easing partout.

### 103. `/motiongraphic` — Motion Graphics Infographique

- **Rôle** : Expliquer des données et des idées à l'aide de graphiques animés (icônes, chiffres, flèches, diagrammes).
- **Composition Kadans** : Icônes flat apparaissant avec `scale 0→1.08→1`, flèches qui se dessinent d'elles-mêmes (`stroke-dashoffset`), chiffres qui défilent, texte concis de 3-6 mots par écran.
- **Obligation IA** : Chaque point énoncé par la voix doit être accompagné d'un graphique correspondant à l'écran à la même seconde (sync avec la voix) ; ne jamais afficher de longs paragraphes.

### 104. `/morphism` — Morphing de Formes Vectorielles (Shape Morph)

- **Rôle** : Métamorphoser une forme en une autre de manière fluide et continue (cercle → carré → logo → icône).
- **Composition Kadans** : Morphing de `path` SVG avec le même nombre de points (flubber / interpolation de path), changement simultané de couleur, durée 0.6-1.2 s, easing `easeInOutQuart`.
- **Obligation IA** : Chaque transition entre scènes doit naître d'une forme qui se métamorphose dans l'élément suivant ; ne jamais faire de cut sec entre 2 scènes comportant /morphism.

### 105. `/shapelayers` — Animation de Calques de Formes (Shape Layers)

- **Rôle** : Construire des compositions avec des formes géométriques qui entrent, pivotent et s'empilent.
- **Composition Kadans** : Cercles, rectangles, triangles, lignes entrant les uns après les autres (stagger), rotations à 90°/180°, masques entre les formes, couleurs en aplats sans dégradé.
- **Obligation IA** : Utiliser exclusivement des formes primitives SVG ; chaque forme est un calque séparé dans la spec afin que le développeur puisse la modifier.

### 106. `/liquidmotion` — Motion Liquide & Blobs

- **Rôle** : Donner à la vidéo une sensation organique, douce et fluide.
- **Composition Kadans** : Blob SVG qui se déforme (filtre `feTurbulence` + `feDisplacementMap` ou morphing de path), gouttes qui fusionnent (effet gooey), mouvement doux de 4-8 s en boucle.
- **Obligation IA** : Ne pas utiliser d'angles vifs ; toutes les formes doivent avoir des courbes douces ; combiner avec /gradientmotion en cas de dégradé.

### 107. `/linedraw` — Tracé de Lignes Animé (Stroke Draw)

- **Rôle** : Montrer des illustrations, cartes ou logos qui se dessinent sous les yeux du spectateur.
- **Composition Kadans** : `stroke-dasharray` + `stroke-dashoffset` animés de 100% → 0, épaisseur de trait constante, remplissage apparaissant APRÈS la fin du tracé (fondu de 0.3 s).
- **Obligation IA** : Tous les dessins doivent être en SVG path ; l'ordre du tracé doit suivre une logique naturelle (de haut à gauche → vers bas à droite) ou le rythme de la voix.

### 108. `/flatmotion` — Flat Design Animé 2D

- **Rôle** : Style d'illustration flat moderne (qualité Kurzgesagt / explainer de startup).
- **Composition Kadans** : Couleurs en aplats, ombres portées longues à 45°, aucune texture, personnages et objets épurés, mouvements de rebond légers.
- **Obligation IA** : Palette de 5 couleurs maximum ; tous les éléments en vecteurs ; conserver la même épaisseur de trait dans toute la vidéo.

### 109. `/isomotion` — Animation Isométrique

- **Rôle** : Montrer des systèmes, villes, bureaux ou processus en vue isométrique à 30°.
- **Composition Kadans** : Grille isométrique, blocs qui descendent ou montent pour se mettre en place, petits personnages et véhicules circulant sur des trajectoires isométriques, caméra fixe.
- **Obligation IA** : Respecter l'angle exact de 30° (`transform: rotateX(60deg) rotateZ(45deg)` ou SVG isométrique) ; ne pas mélanger avec une perspective ordinaire.

### 110. `/logoreveal` — Révélation de Logo en Motion

- **Rôle** : Faire apparaître le logo avec impact au début ou à la fin.
- **Composition Kadans** : Masque qui s'ouvre, particules se rassemblant pour former le logo, ou lignes qui le tracent ; éclair lumineux subtil + whoosh, durée 2-3 s.
- **Obligation IA** : Utiliser impérativement le logo ORIGINAL du client (SVG si possible) ; ne jamais déformer ses proportions ; son whoosh/impact calé sur le moment exact où il finit d'apparaître.

### 111. `/logoanimation` — Animation Complète de Logo (Build-up)

- **Rôle** : Décomposer le logo en éléments séparés puis le reconstruire avec animation.
- **Composition Kadans** : Chaque composant du logo (symbole, lettres, slogan) entre séparément, rebondit, puis l'ensemble se stabilise ; boucle optionnelle de 3-5 s.
- **Obligation IA** : Séparer le logo en calques SVG ; exporter également une version courte de 1.5 s pour les intros de réseaux sociaux.

### 112. `/iconmotion` — Icônes Animées (Micro-animation)

- **Rôle** : Insuffler une touche de vie à chaque icône (cloche qui tinte, cœur qui bat, coche qui se dessine).
- **Composition Kadans** : Animation courte de 0.4-0.8 s, mouvement porteur de sens en accord avec la fonction de l'icône, tracé + remplissage (stroke + fill).
- **Obligation IA** : Chaque icône doit avoir une animation adaptée à sa signification ; ne pas utiliser la même animation générique pour toutes.

### 113. `/datamotion` — Graphiques de Données Animés (Barres, Camembert, Lignes)

- **Rôle** : Donner vie aux chiffres grâce à des graphiques dynamiques en pleine progression.
- **Composition Kadans** : Barres s'élevant depuis 0, courbes qui se tracent, camemberts qui se remplissent, étiquettes de valeur qui s'incrémentent en simultané, axes nets et soignés.
- **Obligation IA** : Les données doivent être RÉELLES (celles fournies par le développeur ou tirées de la source) ; ne pas inventer de chiffres ; indiquer la source en petit texte en bas.

### 114. `/countermotion` — Compteur Numérique Animé (Counter)

- **Rôle** : Mettre l'accent sur un chiffre clé déterminant (clients, ventes, %, tarif).
- **Composition Kadans** : Chiffres de grande dimension (120-200 px), comptant de 0 jusqu'à la valeur finale avec l'easing `easeOutExpo`, unité/suffixe apparaissant juste après, légère pulsation à la fin.
- **Obligation IA** : Le décompte doit se terminer sur un bruitage sec de clic ou d'impact ('tick') ; formater le nombre selon la typographie de la langue (1 000 / 1,000).

### 115. `/explainer` — Vidéo Explicative en Motion Design

- **Rôle** : Structure explicative classique : problème → fonctionnement → bénéfices → appel à l'action (CTA).
- **Composition Kadans** : Scènes de 4-6 s chacune, personnages en flat design, icônes, flèches, voix off limpide, musique légère et optimiste.
- **Obligation IA** : Suivre obligatoirement la structure en 4 étapes ; une seule idée par scène ; voix ElevenLabs synchronisée avec sous-titres.

### 116. `/lowerthirdpro` — Bandeau Titre Pro (Lower Third Motion Pro)

- **Rôle** : Présenter un nom, un titre professionnel ou une précision informative en bas d'écran.
- **Composition Kadans** : Bande de couleur qui glisse + texte apparaissant sous masque, alignement à gauche, maintien à l'écran pendant 3-5 s, sortie en sens inverse.
- **Obligation IA** : Ne jamais masquer le visage des personnes à l'écran ; respecter rigoureusement la zone de sécurité de 5% en bas et sur les côtés.

### 117. `/titlesequence` — Générique de Titres Cinématographique

- **Rôle** : Créer un générique d'ouverture dans l'esprit d'une série télévisée ou d'un long métrage.
- **Composition Kadans** : Typographie grand format, créative, en parfaite cohérence avec le sujet, scènes de titres successives sur une musique rythmée, coupures calées sur les temps forts.
- **Obligation IA** : Mentionner le titre du projet, les créateurs, puis afficher un titre final ; synchroniser chaque transition avec le beat musical (/effectbeatdrop si disponible).

### 118. `/swisstype` — Typographie Suisse / Motion sur Grille

- **Rôle** : Style graphique suisse : grille stricte, typographie grotesque, alignement géométrique parfait.
- **Composition Kadans** : Police sans-serif (style Inter / Helvetica), blocs de texte rigoureusement alignés sur la grille, palette chromatique restreinte (noir, blanc, rouge), mouvements de glissement linéaire.
- **Obligation IA** : Aucune fioriture décorative superflue ; chaque translation doit suivre la grille à la lettre.

### 119. `/bouncemotion` — Rebond Élastique (Squash & Stretch)

- **Rôle** : Donner aux objets un caractère ludique et dynamique en s'appuyant sur les 12 principes de l'animation.
- **Composition Kadans** : Écrasement et étirement (squash & stretch) lors des impacts, anticipation avant le mouvement, prolongement d'inertie (follow-through), easing élastique `easeOutElastic`.
- **Obligation IA** : À utiliser pour des objets légers et un ton décontracté ; ne pas employer sur des textes sérieux ou des données financières.

### 120. `/maskreveal` — Révélation par Masque (Mask Reveal)

- **Rôle** : Faire émerger des textes et des images depuis l'arrière d'un masque en mouvement.
- **Composition Kadans** : `clip-path` ou masque SVG animé, texte s'élevant depuis le dessous d'une ligne invisible, image se révélant par bandes successives.
- **Obligation IA** : Toutes les révélations au sein d'une même scène doivent adopter une direction homogène et cohérente.

### 121. `/splitscreen` — Écran Partagé Animé (Split Screen)

- **Rôle** : Afficher simultanément 2 à 4 éléments (comparaisons avant/après, produits multiples, plusieurs intervenants).
- **Composition Kadans** : Panneaux délimités par des lignes animées, apparition décalée de chaque panneau, séparateur mobile redéfinissant dynamiquement les proportions.
- **Obligation IA** : Chaque panneau doit rester parfaitement lisible sur écran mobile ; ne jamais dépasser 4 panneaux.

### 122. `/loopmotion` — Boucle Parfaite Sans Raccord (Seamless Loop)

- **Rôle** : Créer une animation capable de se répéter indéfiniment sans transition apparente (GIF, arrière-plans, réseaux sociaux).
- **Composition Kadans** : Première et dernière images rigoureusement identiques, mouvements cycliques (rotation à 360°, onde, pulsation), durée de 2-8 s.
- **Obligation IA** : Vérifier que la frame 0 équivaut exactement à la dernière frame ; renseigner `loop: true` dans la spec.

### 123. `/3dmotion` — Motion 3D CSS (Perspective)

- **Rôle** : Apporter du relief avec des cartes, des blocs de texte et des écrans pivotant dans l'espace 3D.
- **Composition Kadans** : `perspective: 1200px`, `rotateY/rotateX`, cartes qui basculent, caméra progressant en profondeur, ombres dynamiques réactives.
- **Obligation IA** : Préserver une lisibilité parfaite : ne pas faire pivoter le texte de plus de 35° pendant sa lecture.

### 124. `/gradientmotion` — Dégradé Dynamique en Mouvement (Mesh Gradient)

- **Rôle** : Arrière-plan en dégradé vivant et dynamique se déplaçant avec douceur.
- **Composition Kadans** : Mesh gradient de 3-5 teintes en mouvement (positions animées), flou élevé, grain subtil superposé.
- **Obligation IA** : Le contraste avec le texte doit impérativement rester ≥ 4.5:1 à tout moment.

### 125. `/halftonemotion` — Halftone & Animation Imprimé Rétro

- **Rôle** : Style imprimé rétro (trames de points, bande dessinée vintage, affiches anciennes) en mouvement.
- **Composition Kadans** : Motif halftone SVG, décalage des couches chromatiques CMYK, texture de papier, animation cadencée à 12 fps esprit 'stop-motion'.
- **Obligation IA** : Caler les éléments sur une cadence de 12 fps, tout en conservant un rendu final fluide exporté en 60 FPS.

### 126. `/uimotion` — Animation UI Produit (App Walkthrough)

- **Rôle** : Montrer le fonctionnement d'une application ou d'un logiciel avec des animations d'interface soignées.
- **Composition Kadans** : Curseur/doigt qui clique, écrans qui glissent, éléments UI qui apparaissent, zoom sur les zones clés, mockup d'appareil (/effectdeviceframe).
- **Obligation IA** : Utiliser de véritables captures ou une véritable UI reconstruite en HTML ; ne pas inventer de fonctionnalités inexistantes.

---

## Catégorie K : Publicité & Spots Professionnels

### 127. `/pubstore` — Publicité Magasin / Boutique (Retail Promo)

- **Rôle** : Promouvoir un magasin, une boutique ou un supermarché.
- **Composition Kadans** : Produits apparaissant sur des étagères animées, prix et étiquettes qui tombent, adresse + horaires, logo du magasin, CTA 'Venez aujourd'hui'.
- **Obligation IA** : Afficher les prix et réductions en GRAND ; informations locales (adresse, téléphone, WhatsApp) obligatoires dans la scène finale.

### 128. `/zoommap` — Zoom sur Carte (Map Zoom Localisation)

- **Rôle** : Montrer l'emplacement d'une entreprise, d'un événement ou d'un lieu.
- **Composition Kadans** : Carte passant de la vue pays → ville → quartier → repère qui tombe avec rebond, tracé d'itinéraire, étiquette du nom du lieu.
- **Obligation IA** : Utiliser des cartes SVG/OpenStreetMap (pas de captures Google Maps sous copyright sans attribution) ; le repère (pin) doit respecter les couleurs de la marque.

### 129. `/pubproduct` — Produit Hero 360°

- **Rôle** : Mettre un produit en vedette au cœur de la publicité.
- **Composition Kadans** : Produit centré sur fond épuré, rotation/parallaxe, éclairage rim light, caractéristiques apparaissant avec des lignes indicatrices pointant les composants.
- **Obligation IA** : Le produit doit occuper au moins 50% de l'écran dans la scène principale ; ne pas dénaturer les couleurs réelles du produit.

### 130. `/pubfood` — Publicité Restaurant & Gastronomie

- **Rôle** : Ouvrir l'appétit : restaurant, fast-food, pâtisserie.
- **Composition Kadans** : Gros plans sur les plats, vapeur, sauce qui coule, ralenti (slow-motion), couleurs chaudes, sons de cuisson/grésillement.
- **Obligation IA** : Couleurs chaudes (rouge, jaune, orange) ; inclure le menu / les prix / les options de livraison à la fin.

### 131. `/pubrealestate` — Publicité Immobilière

- **Rôle** : Présenter des maisons, appartements ou terrains à vendre/à louer.
- **Composition Kadans** : Vues aériennes par drone/extérieurs, visite pièce par pièce, icônes chambres/salles de bain/m², carte de localisation, prix.
- **Obligation IA** : Format : extérieurs → pièces principales → détails → carte → prix + coordonnées de l'agent.

### 132. `/pubcar` — Publicité Automobile

- **Rôle** : Publicité pour véhicules, concessions automobiles, pièces détachées ou garages.
- **Composition Kadans** : Mouvements de caméra dynamiques, reflets lumineux sur la carrosserie, sensation de vitesse, rugissement du moteur, typographie percutante.
- **Obligation IA** : Indiquer le modèle, l'année, le prix ou les offres de financement ; respecter les teintes réelles du véhicule.

### 133. `/pubfashion` — Publicité Mode & Habillement

- **Rôle** : Publicité pour boutiques de vêtements, chaussures, accessoires et collections de mode.
- **Composition Kadans** : Cuts calés sur le beat, typographie éditoriale, enchaînement de looks, transitions au flash, musique tendance.
- **Obligation IA** : Rythme soutenu (0,5-1 s par plan) synchronisé sur la musique ; nom de la collection + lien de la boutique à la fin.

### 134. `/pubbeauty` — Publicité Cosmétique & Beauté

- **Rôle** : Publicité pour produits de beauté, salons d'esthétique et spas.
- **Composition Kadans** : Macro sur la texture des crèmes, gouttes délicates, lumière douce et enveloppante, teintes pastel/dorées, éclat naturel de la peau.
- **Obligation IA** : Ton élégant et apaisant ; ne faire aucune allégation médicale trompeuse.

### 135. `/pubtech` — Publicité Technologie / Gadget

- **Rôle** : Publicité pour smartphones, ordinateurs, gadgets et services technologiques.
- **Composition Kadans** : Arrière-plan sombre, éclairage néon bleu/violet, zooms sur les détails matériels, spécifications techniques apparaissant avec des lignes indicatrices.
- **Obligation IA** : Les caractéristiques techniques doivent être réelles ; indiquer le prix + points de vente.

### 136. `/pubapp` — Publicité Application Mobile (App Promo)

- **Rôle** : Inciter au téléchargement d'une application mobile.
- **Composition Kadans** : Smartphone 3D affichant l'écran de l'application, mise en avant de 3 fonctionnalités clés, badges App Store / Google Play, code QR.
- **Obligation IA** : Montrer les véritables écrans de l'application ; terminer par les badges des stores d'applications + le CTA 'Télécharger maintenant'.

### 137. `/pubevent` — Publicité Événement / Concert

- **Rôle** : Annoncer des concerts, festivals, conférences ou salons.
- **Composition Kadans** : Noms des artistes/intervenants, date et heure en grand format, lieu (/zoommap si nécessaire), compte à rebours, bande-son entraînante.
- **Obligation IA** : Date, heure, lieu, tarifs des billets et billetterie = obligatoires.

### 138. `/pubflashsale` — Vente Flash / Promotion %

- **Rôle** : Créer un sentiment d'urgence pour une promotion à durée limitée.
- **Composition Kadans** : Pourcentages percutants (-50%), prix d'origine barré, compte à rebours animé, palette rouge/jaune, typographie vibrante.
- **Obligation IA** : Indiquer la date d'expiration de la promotion ; les prix avant et après doivent être nettement visibles.

### 139. `/pubblackfriday` — Black Friday / Méga Soldes

- **Rôle** : Campagne publicitaire dédiée au Black Friday, Cyber Monday et fêtes de fin d'année.
- **Composition Kadans** : Arrière-plan noir profond, typographie géante or/blanc, flashs lumineux, explosions de remises, vitrine de produits avec prix.
- **Obligation IA** : Ton prestigieux allié à l'urgence ; date de l'événement obligatoire.

### 140. `/pubbank` — Publicité Banque & Fintech

- **Rôle** : Publicité pour banques, transferts d'argent, applications de paiement et microfinance.
- **Composition Kadans** : Couleurs évoquant la confiance (bleu, vert), carte bancaire 3D, graphiques de croissance, icônes de sécurité, visages souriants.
- **Obligation IA** : Mentions légales / conditions en petits caractères dès lors qu'il y a des taux ou des frais.

### 141. `/pubhealth` — Publicité Santé / Clinique

- **Rôle** : Publicité pour cliniques, pharmacies, hôpitaux et services de santé.
- **Composition Kadans** : Palette blanc/bleu/vert, pictogrammes médicaux, personnel soignant souriant, liste des prestations, coordonnées d'urgence.
- **Obligation IA** : Ne jamais promettre de guérison miraculeuse ; coordonnées de contact parfaitement claires.

### 142. `/pubschool` — Publicité École & Formation

- **Rôle** : Publicité pour écoles, universités, centres de formation et cours en ligne.
- **Composition Kadans** : Étudiants en situation, icônes de livres/diplômes, programmes d'études, dates d'inscription, témoignages d'alumni.
- **Obligation IA** : Date limite d'inscription + coordonnées obligatoires.

### 143. `/pubtravel` — Publicité Voyage & Tourisme

- **Rôle** : Publicité pour agences de voyages, hôtels et destinations touristiques (Haïti, Caraïbes…).
- **Composition Kadans** : Plans panoramiques de paysages, avion traçant son itinéraire sur carte (/zoommap), tarifs de forfaits, activités phares.
- **Obligation IA** : Afficher les tarifs avec la mention 'à partir de' + dates de validité ; paysages authentiques de la destination.

### 144. `/pubrestaurantmenu` — Menu Numérique Animé (Menu Board)

- **Rôle** : Affichage numérique de menu pour restaurants (écrans TV en salle).
- **Composition Kadans** : Colonnes de plats + tarifs, plats en rotation successive, plat du jour/promotion mis en avant, boucle de 15 à 30 s.
- **Obligation IA** : Format 16:9 ou 9:16 vertical ; prix parfaitement lisibles à 3 mètres de distance ; /loopmotion automatique.

### 145. `/pubtestimonial` — Publicité Témoignage UGC

- **Rôle** : Publicité basée sur la parole client (style UGC réseaux sociaux).
- **Composition Kadans** : Format vertical 9:16, visage du client, sous-titres mot à mot synchronisés, notation 5 étoiles, produit mis en scène.
- **Obligation IA** : Les témoignages doivent être RÉELS (fournis par le développeur) ; ne pas inventer de faux clients.

### 146. `/pubbeforeafter` — Avant / Après

- **Rôle** : Démontrer l'efficacité et les résultats d'un produit ou d'un service.
- **Composition Kadans** : Écran partagé avec curseur interactif en déplacement, étiquettes AVANT/APRÈS, cadrage rigoureusement identique pour les deux images.
- **Obligation IA** : Les deux images doivent partager le même angle et le même éclairage ; ne pas manipuler artificiellement le résultat.

### 147. `/pubunboxing` — Unboxing Produit

- **Rôle** : Déballer le packaging du produit face caméra.
- **Composition Kadans** : Ouverture de la boîte, soulèvement du produit sublimé par la lumière, présentation détaillée des accessoires un à un, effets sonores ASMR de papier/carton.
- **Obligation IA** : Montrer l'intégralité du contenu de la boîte ; conclure avec le prix + où se procurer le produit.

### 148. `/pubbumper` — Bumper Ad 6 Secondes

- **Rôle** : Spot court percutant conçu pour les bumpers YouTube / Stories.
- **Composition Kadans** : 1 message unique, logo, CTA — durée EXACTE de 6 s, accroche (hook) dès la première seconde.
- **Obligation IA** : Durée maximale de 6,0 s ; une seule idée centrale ; logo visible en continu ou sur l'écran de fin.

### 149. `/pubtv30` — Spot TV 30 Secondes

- **Rôle** : Spot télévisuel/radio visuelle classique de 30 secondes.
- **Composition Kadans** : Structure : accroche (3 s) → problème (5 s) → solution (12 s) → preuve (5 s) → CTA + logo (5 s).
- **Obligation IA** : Durée exacte de 30 s ; format 16:9 1080p ; niveau sonore normalisé à -23 LUFS (norme broadcast TV).

### 150. `/pubbillboard` — Panneau d'Affichage / DOOH Écran Urbain

- **Rôle** : Publicité pour affichage dynamique urbain (DOOH), centres commerciaux et aéroports.
- **Composition Kadans** : Message concis de 5 à 7 mots max, typographie grand format, fort contraste visuel, boucle muette de 8 à 15 s.
- **Obligation IA** : Aucune dépendance sonore ; lisible à grande distance ; ratio d'aspect adapté à l'écran (portrait ou paysage).

### 151. `/pubjingle` — Jingle & Son de Marque

- **Rôle** : Créer la signature sonore de la marque dans la publicité.
- **Composition Kadans** : Jingle 3-5 s, slogan chanté ou parlé (ElevenLabs), son logo, sync avec l'animation du logo.
- **Obligation IA** : Utiliser ElevenLabs pour la voix/sfx ; le jingle doit être répété à la fin de chaque pub (/effectoutrologos).

---

## Catégorie L : Transitions Visuelles & Transitions Sonores

### 152. `/zoomin` — Zoom Avant (Zoom In)

- **Rôle** : Entrer dans la scène suivante via un zoom avant.
- **Composition Kadans** : Kadans : `"transition": "zoom"` sur la scène entrante ; durée 0.4-0.6 s ; easing `inout`.
- **Obligation IA** : Chaque coupe entre scènes avec /zoomin DOIT avoir `"transition": "zoom"` ; définir `"skills": ["/zoomin"]` sur ces scènes.

### 153. `/zoomout` — Zoom Arrière (Zoom Out)

- **Rôle** : Sortir d'une scène comme si la caméra reculait.
- **Composition Kadans** : Kadans : `"transition": "zoomout"` ; durée 0.4-0.7 s.
- **Obligation IA** : Utiliser la valeur exacte `"transition": "zoomout"` ; ne pas remplacer par un fade.

### 154. `/spiral` — Spirale (Spin + Zoom)

- **Rôle** : La scène tourne en spirale pendant son entrée/sortie.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes : `rotate(0→720deg)` + `scale(1→0.1)` sur la scène sortante, inverse sur la scène entrante ; durée 0.8 s ; ou `"transition": "rotate"` + zoom si la scène n'est pas html.
- **Obligation IA** : La rotation doit être d'au moins 360° ; définir `"skills": ["/spiral"]` sur la scène de transition.

### 155. `/whippan` — Whip Pan (Panoramique Rapide)

- **Rôle** : La caméra balaie latéralement à toute vitesse avec flou de mouvement entre 2 scènes.
- **Composition Kadans** : Kadans : `"transition": "slide"` + `"blur"` (motion_blur activé) ou scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes `translateX(-120%)` + `filter: blur(18px)` ; durée 0.25-0.35 s ; son whoosh (`sfx.whoosh: true`).
- **Obligation IA** : Durée ≤ 0.35 s ; whoosh obligatoire sur la coupe.

### 156. `/spinblur` — Spin Blur

- **Rôle** : Transition en rotation rapide avec flou.
- **Composition Kadans** : Kadans : `"transition": "rotate"` avec `"motion_blur"` activé ; durée 0.4 s.
- **Obligation IA** : Rotation + flou combinés ; pas une simple rotation nette.

### 157. `/crossfade` — Fondu Enchaîné (Crossfade)

- **Rôle** : Transition douce, classique et sereine.
- **Composition Kadans** : Kadans : `"transition": "fade"` ; durée 0.6-1.0 s.
- **Obligation IA** : À utiliser pour un ton émotionnel / documentaire ; pas pour une publicité au rythme rapide.

### 158. `/dipblack` — Fondu au Noir (Dip to Black)

- **Rôle** : Fermer un chapitre et en ouvrir un autre.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes avec fond `#000` montant de 0→1 (0.3 s), maintenu 0.2 s, redescendant (0.3 s) ; ou scène courte `background: #000` de 0.4 s avec `"transition": "fade"`.
- **Obligation IA** : L'écran doit devenir entièrement NOIR pendant au moins 0.15 s.

### 159. `/dipwhite` — Fondu au Blanc (Dip to White / Flash)

- **Rôle** : Transition lumineuse, évocation de rêve, souvenir ou regain d'énergie.
- **Composition Kadans** : Kadans : identique à /dipblack mais avec `#fff` ; durée totale 0.5-0.8 s.
- **Obligation IA** : L'écran doit devenir entièrement BLANC pendant au moins 1 image.

### 160. `/slideleft` — Glissement vers la Gauche (Push Left)

- **Rôle** : La scène suivante pousse la précédente vers la gauche.
- **Composition Kadans** : Kadans : `"transition": "slide"` ; durée 0.4-0.5 s.
- **Obligation IA** : Valeur exacte `slide` ; direction cohérente sur l'ensemble de la série.

### 161. `/slideright` — Glissement vers la Droite (Push Right)

- **Rôle** : La scène suivante entre depuis la gauche.
- **Composition Kadans** : Kadans : `"transition": "slideright"`.
- **Obligation IA** : Valeur exacte `slideright`.

### 162. `/slideup` — Glissement vers le Haut (Push Up)

- **Rôle** : Transition verticale (style Reel / TikTok).
- **Composition Kadans** : Kadans : `"transition": "slideup"` ; idéal pour 9:16.
- **Obligation IA** : Valeur exacte `slideup`.

### 163. `/slidedown` — Glissement vers le Bas (Push Down)

- **Rôle** : Transition verticale vers le bas.
- **Composition Kadans** : Kadans : `"transition": "slidedown"`.
- **Obligation IA** : Valeur exacte `slidedown`.

### 164. `/wipeline` — Balayage Linéaire (Line Wipe)

- **Rôle** : Une ligne traverse l'écran et révèle la scène suivante.
- **Composition Kadans** : Kadans : `"transition": "wipe"` (horizontal) ou `"wipeup"` (vertical) ; ligne à la couleur de la marque sur la bordure (html).
- **Obligation IA** : Valeur exacte `wipe`/`wipeup` ; ligne aux couleurs de la marque si une marque est définie.

### 165. `/circlereveal` — Révélation Circulaire (Circle Reveal)

- **Rôle** : Un cercle qui grandit depuis un point pour révéler la scène.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes `clip-path: circle(0% at X Y) → circle(150% at X Y)` ; durée 0.6 s ; centré sur le sujet.
- **Obligation IA** : Le centre du cercle doit être sur le sujet important, pas au milieu par défaut.

### 166. `/irisclose` — Fermeture Iris (Style Film Ancien)

- **Rôle** : Cercle qui se referme sur un détail (fin classique, comédie).
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes `clip-path: circle(150%) → circle(0%)` sur fond noir ; durée 0.8 s.
- **Obligation IA** : Fermer sur le détail final (visage, logo).

### 167. `/cubeflip` — Cube 3D (Cube Rotate)

- **Rôle** : 2 scènes sur 2 faces d'un cube en rotation.
- **Composition Kadans** : Kadans : `"transition": "flip"` ou scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes `perspective: 1200px` + `rotateY(-90deg)` sur 2 faces ; durée 0.7 s.
- **Obligation IA** : L'effet 3D doit être visible (perspective), pas un simple retournement à plat.

### 168. `/pageturn` — Tourner de Page (Page Turn)

- **Rôle** : Transition imitant une page de livre qui se tourne.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes `rotateY(0→-180deg)` avec `transform-origin: left` + ombre ; son `sfx:book-flip`.
- **Obligation IA** : Son `sfx:book-flip` obligatoire au moment où la page tourne.

### 169. `/lightleak` — Fuite de Lumière (Light Leak)

- **Rôle** : Flash lumineux chaud et organique entre 2 scènes.
- **Composition Kadans** : Kadans : calque de superposition dégradé orange/rose `mix-blend-mode: screen` qui traverse (0.8 s) + `"transition": "fade"`.
- **Obligation IA** : Couleurs chaudes ; superposition transparente, pas un bloc de couleur uni.

### 170. `/filmburn` — Brûlure de Pellicule (Film Burn)

- **Rôle** : Transition vintage imitant un film qui brûle.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes avec taches orange/blanc en expansion (radial-gradient + blur) + grain ; durée 0.8-1 s.
- **Obligation IA** : Grain argentique + couleurs chaudes obligatoires.

### 171. `/pixelate` — Pixellisation (Pixelate)

- **Rôle** : La scène devient pixellisée puis se reforme dans la suivante.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes (canvas ou `image-rendering: pixelated` + scale), blocs de 4→48 px→4 ; durée 0.6 s.
- **Obligation IA** : Les pixels doivent être nettement visibles au milieu de la transition.

### 172. `/rgbsplit` — Séparation RVB (RGB Split / Aberration Chromatique)

- **Rôle** : Canaux rouge/vert/bleu séparés pour une coupe technologique.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes avec 3 copies en `mix-blend-mode: screen` décalées de ±8 px ; durée 0.3 s ; son `sfx.hit`.
- **Obligation IA** : Décalage bien visible des 3 couleurs ; durée courte.

### 173. `/glitchcut` — Coupe Glitch

- **Rôle** : Coupe brutale avec glitch numérique.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes avec bandes en déplacement (`clip-path` + translateX aléatoire), 6-10 images ; son /soundglitch.
- **Obligation IA** : Durée 0.2-0.4 s ; superposer avec /soundglitch si le son est activé.

### 174. `/shatter` — Écran Brisé (Shatter)

- **Rôle** : La scène se brise en morceaux de verre.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes avec polygon `clip-path` (12-20 morceaux) tombant en rotation ; son `sfx:impact-glass`.
- **Obligation IA** : Son `sfx:impact-glass` obligatoire.

### 175. `/liquidmelt` — Fusion Liquide (Liquid Melt)

- **Rôle** : La scène fond comme un liquide.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) effectuant la transition entre les 2 scènes avec SVG `feTurbulence` + `feDisplacementMap` (scale 0→80→0) ; durée 0.8 s.
- **Obligation IA** : Déformation organique visible ; pas un simple fade.

### 176. `/ripple` — Ondulation d'Eau (Ripple)

- **Rôle** : Ondes se propageant depuis un point précis comme une pierre jetée dans l'eau.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes par un déplacement radial animé ; durée 0.8 s.
- **Obligation IA** : Les ondes doivent émaner d'un point précis (clic / sujet).

### 177. `/swirl` — Tourbillon (Swirl)

- **Rôle** : La scène se tord en un tourbillon dynamique.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes (canvas / WebGL swirl ou `rotate` + `blur` + scale) ; durée 0.7 s.
- **Obligation IA** : Distorsion de torsion nettement visible.

### 178. `/kaleidoscope` — Kaléidoscope

- **Rôle** : Transition en miroir symétrique psychédélique.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes avec 6-8 copies et `clip-path` triangulaire + rotation ; durée 1 s.
- **Obligation IA** : À utiliser pour la musique / les événements ; symétrie nettement visible.

### 179. `/stretchwarp` — Étirement Dynamique (Stretch Warp)

- **Rôle** : La scène s'étire dans la direction du mouvement.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes par `scaleX(1→4)` + `blur` sur la scène sortante, inverse sur la scène entrante ; durée 0.35 s ; whoosh.
- **Obligation IA** : Whoosh obligatoire (`sfx.whoosh: true`).

### 180. `/blinds` — Persiennes Vénitiennes (Venetian Blinds)

- **Rôle** : Lamelles horizontales pivotant pour révéler la scène.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes avec 8-12 bandes `rotateX(90→0deg)` en décalage stagger de 30 ms.
- **Obligation IA** : Décalage (stagger) visible entre les bandes.

### 181. `/checkerboard` — Damier (Checkerboard)

- **Rôle** : Cases apparaissant successivement à la manière d'un damier.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes par une grille de 8×6 cases `scale(0→1)` en décalage diagonal stagger.
- **Obligation IA** : Décalage diagonal (stagger) obligatoire.

### 182. `/splitreveal` — Écran Séparé en Deux (Split Reveal)

- **Rôle** : La scène s'ouvre en deux moitiés (comme une porte) pour révéler la suivante.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes par 2 moitiés `translateX(∓100%)` ; son `sfx:door-open` optionnel.
- **Obligation IA** : Les 2 moitiés doivent se déplacer dans des directions opposées.

### 183. `/matchcut` — Raccord Graphique (Match Cut)

- **Rôle** : Coupe sur 2 formes ou mouvements similaires (cercle → lune).
- **Composition Kadans** : Kadans : `"transition": "none"` mais la position/forme du sujet est IDENTIQUE dans la dernière image de la scène A et la première image de la scène B.
- **Obligation IA** : La forme, la taille et la position doivent correspondre ; préciser dans le rapport quels éléments concordent.

### 184. `/smashcut` — Coupe Franche (Smash Cut)

- **Rôle** : Coupe brutale passant du calme au bruit (ou inversement) pour un effet comique ou de choc.
- **Composition Kadans** : Kadans : `"transition": "none"` ; son coupé net ou montant brusquement ; contraste total entre les 2 scènes.
- **Obligation IA** : AUCUNE transition douce ; changement sonore brutal.

### 185. `/speedramp` — Variation de Vitesse (Speed Ramp)

- **Rôle** : Ralentissement puis accélération de la vidéo (ou inversement) à proximité de la coupe.
- **Composition Kadans** : Kadans : `"speed"` sur les scènes vidéo (ex. 1 → 0.3 → 2) + `"transition": "zoom"` ; whoosh.
- **Obligation IA** : Utiliser la clé `speed` de Kadans ; uniquement sur les scènes contenant de véritables vidéos.

### 186. `/brushstroke` — Coup de Pinceau (Brush Reveal)

- **Rôle** : Coup de pinceau peignant la scène suivante.
- **Composition Kadans** : Kadans : scène `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) réalisant la transition entre 2 scènes par un masque SVG de pinceau (`stroke-dashoffset`) qui révèle la scène ; son `sfx:paint-brush`.
- **Obligation IA** : Son `sfx:paint-brush` obligatoire.

### 187. `/soundhot` — Son Chaud (Hot Hit / Sizzle)

- **Rôle** : Son d'impact énergique et chaud sur la coupe (produits, nourriture, publicités).
- **Composition Kadans** : Kadans : `sfx.hit: true` + SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «sizzle hot impact, short punchy» ; volume -6 dB.
- **Obligation IA** : Le son doit tomber EXACTEMENT sur la coupe (`at` = instant de la transition).

### 188. `/soundepic` — Son Épique (Cinematic Boom)

- **Rôle** : Puissant boom cinématographique pour les temps forts (révélation, logo, grand titre).
- **Composition Kadans** : Kadans : SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «epic cinematic boom with deep sub and reverb tail» + `sfx:thunder` en arrière-plan ; ducking de la voix.
- **Obligation IA** : L'utiliser 1 à 3 fois maximum par vidéo ; lors des révélations principales.

### 189. `/soundtyping` — Frappe au Clavier (Typing)

- **Rôle** : Son de frappe au clavier pendant l'apparition du texte.
- **Composition Kadans** : Kadans : `sfx.type: true` (son de frappe sur chaque lettre) + `sfx.text: true` ; synchronisé avec /effecttypewriter.
- **Obligation IA** : Chaque lettre affichée = un clic sonore ; ne pas jouer le son lorsqu'aucun texte n'est écrit.

### 190. `/soundriser` — Montée de Tension (Riser)

- **Rôle** : Son montant crescendo avant un temps fort.
- **Composition Kadans** : Kadans : SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «cinematic riser 2 seconds building tension» ; se termine EXACTEMENT sur la coupe.
- **Obligation IA** : La fin du riser = la coupe / le drop.

### 191. `/sounddrop` — Descente de Basse (Bass Drop)

- **Rôle** : Lourde déflagration de basse après un riser ou lors d'une révélation.
- **Composition Kadans** : Kadans : `sfx.hit: true` + SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «deep bass drop impact» ; superposé avec /effectbeatdrop.
- **Obligation IA** : Synchronisé avec un impact ou changement visuel fort.

### 192. `/soundboom` — Boom d'Impact

- **Rôle** : Impact lourd sur titres, chiffres ou logo.
- **Composition Kadans** : Kadans : `"sounds": [{"src": "sfx:impact-metal"}]` ou `sfx:impact-wood` + `sfx.hit: true`.
- **Obligation IA** : Sur chaque grand titre / chiffre qui atterrit à l'écran.

### 193. `/soundglitch` — Son Glitch Numérique

- **Rôle** : Bruit numérique haché pour transitions tech/glitch.
- **Composition Kadans** : Kadans : SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «digital glitch stutter short» ; durée 0.2-0.4 s.
- **Obligation IA** : Toujours associé à un effet visuel de glitch (/glitchcut, /effectglitchtext…).

### 194. `/soundcamera` — Obturateur d'Appareil Photo (Shutter)

- **Rôle** : Son d'obturateur photo pour changements d'images / diaporamas.
- **Composition Kadans** : Kadans : SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «camera shutter click» + flash /dipwhite court.
- **Obligation IA** : Un clic sonore par photo affichée.

### 195. `/soundpop` — Pop Graphique

- **Rôle** : Léger son pop pour éléments apparaissant à l'écran (icônes, bulles, puces/chips).
- **Composition Kadans** : Kadans : `sfx.pop: true` ou `sfx:cartoon-pop`.
- **Obligation IA** : Un son pop par élément affiché ; volume bas (-12 dB) pour éviter la fatigue auditive.

### 196. `/soundswipe` — Balayage / Swoosh Rapide

- **Rôle** : Son de glissement pour slides, whip pans et cartes.
- **Composition Kadans** : Kadans : `sfx.whoosh: true` (sur chaque transition) ou `sfx:cloth` pour un glissement doux.
- **Obligation IA** : Chaque transition slide/whip doit intégrer le swoosh.

### 197. `/soundreverse` — Son Inversé (Reverse Swell)

- **Rôle** : Son d'aspiration inversée avant la coupe (cymbale inversée).
- **Composition Kadans** : Kadans : SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «reverse cymbal swell 1.5 seconds» ; s'achève sur la coupe.
- **Obligation IA** : La fin du son correspond exactement au moment de la coupe.

### 198. `/soundmagic` — Son Magique (Shimmer)

- **Rôle** : Son scintillant pour révélations, transformations, avant/après.
- **Composition Kadans** : Kadans : `"sounds": [{"src": "sfx:magic-sparkle"}]`.
- **Obligation IA** : Synchronisé avec les particules / la lumière qui apparaît.

### 199. `/soundcash` — Bruitage de Caisse / Monnaie (Cash)

- **Rôle** : Son pour prix, réductions, ventes, fintech.
- **Composition Kadans** : Kadans : `"sounds": [{"src": "sfx:coins"}]` + SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «cash register ka-ching».
- **Obligation IA** : À déclencher sur chaque prix / réduction affiché.

### 200. `/soundtapestop` — Arrêt de Bande (Tape Stop)

- **Rôle** : La musique ralentit puis s'arrête net comme une cassette (effet comique / choc).
- **Composition Kadans** : Kadans : SFX ElevenLabs (was_voice_engine sfx) enregistré dans `medya/son/`, puis `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` avec le prompt «tape stop slow down effect» ; couper la musique (`music` fade 0.1 s) au même moment.
- **Obligation IA** : La musique DOIT réellement s'arrêter après l'effet.

### 201. `/soundsilence` — Silence Dramatique

- **Rôle** : Couper tout le son durant 0.5-1.5 s avant une grande révélation.
- **Composition Kadans** : Kadans : `fade` musique → 0 et voix en pause, aucun sfx durant le silence, puis /soundepic ou /sounddrop par la suite.
- **Obligation IA** : Le silence doit être total (musique + sfx) ; pas plus de 1.5 s.

---
