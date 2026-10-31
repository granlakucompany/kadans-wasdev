// kadans_i18n.js - Système d'internationalisation pour Kadans Timeline Studio (8 langues)
(function() {
  const KADANS_DICT = {
    fr: {
      "brand": "Kadans Timeline",
      "projects_btn_title": "Projets (nouveau / ouvrir / changer)",
      "projects": "Projets",
      "new_project": "Nouveau projet",
      "new_project_title": "Créer un nouveau projet Kadans (Ctrl+N)",
      "video_title_placeholder": "Titre de la vidéo",
      "video_title_title": "Titre de la vidéo",
      "video_lang_title": "Langue de la vidéo & voix",
      "preview": "Aperçu",
      "preview_title": "Rafraîchir l'aperçu",
      "html_export": "HTML",
      "html_export_title": "Exporter en un fichier HTML autonome",
      "render_mp4": "Rendu MP4",
      "render_mp4_title": "Rendre la vidéo en MP4 (Fichier vidéo final)",
      "save": "Enregistrer",
      "save_title": "Enregistrer le projet (Ctrl+S)",
      "ai_chat": "Chat IA",
      "ai_chat_title": "Ouvrir Chat IA Kadans & 1-Click MCP / CLI IA",
      "settings": "Paramètres",
      "settings_title": "Paramètres (ElevenLabs, MCP CLI IA, micro, encodage)",

      "rail_media": "Médias",
      "rail_media_title": "Médias — Projet médias",
      "rail_assets": "Ressources",
      "rail_assets_title": "Ressources — Bibliothèque graphique",
      "rail_cat": "Catalogue",
      "rail_cat_title": "Catalogue — Modèles & Scènes",
      "rail_sfx": "SFX",
      "rail_sfx_title": "SFX — Effets sonores",
      "rail_comp": "Compo",
      "rail_comp_title": "Compo — Scènes & Compositions",
      "rail_code": "Code",
      "rail_code_title": "Code — Spécification JSON",
      "rail_lint": "Lint",
      "rail_lint_title": "Lint — Vérifier le projet",

      "drop_hint": "Déposez ici pour ajouter à la scène actuelle",
      "play_title": "Lecture / Pause (Espace)",
      "replay_title": "Rejouer depuis le début",
      "zoom_out_title": "Dézoomer ScreenView (-)",
      "zoom_fit_title": "Cliquer pour revenir à 100% Fit",
      "zoom_in_title": "Zoomer ScreenView (+)",
      "fit_title": "Ajuster ScreenView à l'espace écran",
      "snapshot_title": "Exporter l'image actuelle (PNG)",

      "prop_tab": "Prop",
      "prop_tab_title": "Propriétés",
      "ai_tab": "Chat IA",
      "ai_tab_title": "Chat IA & 1-Click MCP / CLI IA",
      "color_tab": "Couleur",
      "color_tab_title": "Couleur (Étalonnage)",
      "blend_tab": "Mélange",
      "blend_tab_title": "Mélange (Modes de fusion & Opacité)",
      "sound_tab": "Son",
      "sound_tab_title": "Son (Audio & Effets)",
      "effect_tab": "Effets",
      "effect_tab_title": "Effets (Filtres & Effets visuels)",
      "lut_tab": "LUT",
      "lut_tab_title": "LUT (Filtres cinématiques)",

      "undo_title": "Annuler (Dernière action) [Ctrl+Z]",
      "redo_title": "Rétablir (Action annulée) [Ctrl+Y]",
      "select_title": "Sélectionner: Choisir, déplacer et ajuster les clips (V)",
      "split_title": "Diviser: Couper le clip ou la scène à la tête de lecture (B)",
      "del_left_title": "Supprimer à gauche: Retirer la partie avant la tête de lecture ([)",
      "del_right_title": "Supprimer à droite: Retirer la partie après la tête de lecture (])",
      "delete_title": "Supprimer: Retirer les éléments sélectionnés (Suppr)",
      "freeze_title": "Arrêt sur image: Figer une image à la position actuelle",
      "reverse_title": "Inverser: Lire la vidéo à l'envers",
      "mirror_title": "Miroir: Retourner l'image horizontalement",
      "rotate_title": "Rotation: Faire pivoter l'image (+90°)",
      "crop_title": "Recadrer: Ajuster le cadrage de l'image",
      "record_title": "Enregistrer voix off: Enregistrer un commentaire audio en direct",
      "add_track": "Ajouter Piste",
      "add_track_title": "Ajouter une piste (Vidéo, Audio, SFX, Image, Texte, Ressource)",
      "main_magnet_title": "Aimantation piste principale",
      "snap_title": "Magnétisme (Alignement des clips)",
      "linkage_title": "Liaison (Déplacement synchronisé des éléments associés)",
      "scrub_audio_title": "Écoute au défilement (Audio scrubbing)",
      "zoom_media_title": "Zoom sur média sélectionné",
      "fit_timeline_title": "Ajuster la timeline à l'écran",
      "zoom_out_tl_title": "Zoom −: Réduire l'échelle temporelle",
      "zoom_in_tl_title": "Zoom +: Agrandir l'échelle temporelle",
      "master_volume_title": "Glisser haut/bas pour régler le volume (0% - 200%) • Double-clic pour 100%",
      "mute_title": "Couper / Rétablir le son (Muet)",

      "track_video": "Piste Vidéo",
      "track_audio": "Piste Audio",
      "track_sfx": "Piste SFX (Effets sonores)",
      "track_image": "Piste Image",
      "track_text": "Piste Texte",
      "track_asset": "Piste Ressource",

      "render_modal_title": "Rendu Vidéo MP4",
      "render_preparing": "Préparation du rendu...",
      "render_init": "Initialisation...",
      "render_success": "Vidéo MP4 exportée avec succès !",
      "cancel": "Annuler",
      "download_mp4": "Télécharger MP4",
      "close": "Fermer",

      "np_modal_title": "Nouveau Projet Kadans",
      "np_modal_sub": "Entrez le nom du nouveau projet vidéo et choisissez le format d'écran.",
      "np_name_lbl": "Nom du projet",
      "np_ratio_lbl": "Format (Ratio)",
      "np_dur_lbl": "Durée de la vidéo (Minutes & Secondes)",
      "np_lang_lbl": "Langue de la vidéo",
      "np_create_btn": "Créer le Projet",

      "ai_director_title": "Kadans AI Director & MCP",
      "ai_open_wasdev": "↗ Chat WASDEV",
      "ai_open_wasdev_title": "Ouvrir dans le Chat AI WASDEV",
      "ai_mcp_btn": "1-Click MCP",
      "ai_mcp_btn_title": "Configurer MCP Kadans en 1 clic pour toutes les IA",
      "ai_checking": "Vérification de la connexion IA & MCP...",
      "ai_prompt_hint": "Écrivez ce que vous souhaitez que l'IA réalise (ex: <i>«Créez une publicité de 45s avec 4 scènes, voix ElevenLabs et sous-titres karaoké»</i>).",
      "ai_quick_4scenes": "4 Scènes Publicité",
      "ai_quick_subtitles": "Sous-titres Karaoké",
      "ai_quick_cinema": "Look Cinéma",
      "ai_input_placeholder": "Demandez à l'IA de monter ou modifier la vidéo...",
      "ai_send_btn": "Envoyer à l'IA",
      "ai_clear_title": "Effacer l'historique du chat"
    },

    ht: {
      "brand": "Kadans Timeline",
      "projects_btn_title": "Pwoje yo (nouvo / ouvri / chanje)",
      "projects": "Pwoje",
      "new_project": "Nouvo pwoje",
      "new_project_title": "Kreye yon nouvo pwoje Kadans (Ctrl+N)",
      "video_title_placeholder": "Tit videyo a",
      "video_title_title": "Tit videyo a (nan mitan ba a)",
      "video_lang_title": "Lang videyo & vwa a",
      "preview": "Apesi",
      "preview_title": "Rafrechi aperçu a",
      "html_export": "HTML",
      "html_export_title": "Ekspote yon sel fichye HTML otonom",
      "render_mp4": "Rann MP4",
      "render_mp4_title": "Rann videyo a an MP4 (Fichye videyo final)",
      "save": "Anrejistre",
      "save_title": "Anrejistre pwojè a (Ctrl+S)",
      "ai_chat": "AI Chat",
      "ai_chat_title": "Ouvri Chat AI Kadans & 1-Click MCP / AI CLI",
      "settings": "Paramèt",
      "settings_title": "Parametre (ElevenLabs, MCP AI CLI, mikro, enkodaj)",

      "rail_media": "Medya",
      "rail_media_title": "Medya — Pwojè medya",
      "rail_assets": "Asset",
      "rail_assets_title": "Asset — Libreri grafik",
      "rail_cat": "Katalog",
      "rail_cat_title": "Katalog — Modèl & Sèn",
      "rail_sfx": "SFX",
      "rail_sfx_title": "SFX — Efè Son (whoosh, pop, hit, etc.)",
      "rail_comp": "Konpo",
      "rail_comp_title": "Konpo — Sèn & Konpozisyon",
      "rail_code": "Kòd",
      "rail_code_title": "Kòd — JSON Spec",
      "rail_lint": "Lint",
      "rail_lint_title": "Lint — Verifye pwojè a",

      "drop_hint": "Lage isit la pou ajoute nan sen aktyel la",
      "play_title": "Jwe / Kanpe (Space)",
      "replay_title": "Rejwe depi 0",
      "zoom_out_title": "Dezoume ScreenView (-)",
      "zoom_fit_title": "Klike pou retounen 100% Fit",
      "zoom_in_title": "Zoume ScreenView (+)",
      "fit_title": "Fit ScreenView pou mezi espas la",
      "snapshot_title": "Ekspote frame aktyel la (PNG) — Mande kote pou anrejistre",

      "prop_tab": "Prop",
      "prop_tab_title": "Pwopriyete (Properties)",
      "ai_tab": "AI Chat",
      "ai_tab_title": "AI Chat & 1-Click MCP / AI CLI",
      "color_tab": "Koulè",
      "color_tab_title": "Koulè (Color Grading)",
      "blend_tab": "Blend",
      "blend_tab_title": "Blend (Mòd melanj & Opasite)",
      "sound_tab": "Son",
      "sound_tab_title": "Son (Odyo & Efè)",
      "effect_tab": "Efè",
      "effect_tab_title": "Efè (Filters & Efè vizyèl)",
      "lut_tab": "LUT",
      "lut_tab_title": "LUT (Filtres sinematik)",

      "undo_title": "Undo — Anile (Retounen sou dènye aksyon an) [Ctrl+Z]",
      "redo_title": "Redo — Refè (Retabli aksyon ou te anile a) [Ctrl+Y]",
      "select_title": "Select — Seleksyon: Chwazi, deplase ak ajiste clips yo (V)",
      "split_title": "Split — Divize: Koupe clip oswa sèn chwazi a kote tèt lekti a ye (B)",
      "del_left_title": "Delete left — Efase bò gòch: Retire pati clip la ki anvan tèt lekti a ([)",
      "del_right_title": "Delete right — Efase bò dwat: Retire pati clip la ki apre tèt lekti a (])",
      "delete_title": "Delete — Efase: Retire eleman chwazi yo nan timeline lan (Suppr)",
      "freeze_title": "Freeze — Fikse imaj: Kreye yon imaj fiks nan moman videyo ou chwazi a",
      "reverse_title": "Reverse — Ranvèse: Fè videyo a jwe alanvè",
      "mirror_title": "Mirror — Reflete: Vire imaj la orizontalman, tankou yon miwa",
      "rotate_title": "Rotate — Wotasyon: Chanje oryantasyon imaj la (+90°)",
      "crop_title": "Crop — Rekadre: Koupe rebò imaj la epi ajiste kad li",
      "record_title": "Record voice-over — Anrejistre vwa: Anrejistre yon kòmantè odyo dirèkteman nan montaj la",
      "add_track": "Add Track",
      "add_track_title": "Ajoute yon track (Videyo, Odyo, SFX, Imaj, Tèks, Asset)",
      "main_magnet_title": "Main track magnet — Leman piste prensipal: Ede kenbe clips piste prensipal la kole san espas",
      "snap_title": "Snapping — Aimantation: Ede bor clips yo aliyen ak lòt clips oswa tèt lekti a",
      "linkage_title": "Linkage — Lyezon: Fè eleman ki asosye yo suiv deplasman nan montaj la",
      "scrub_audio_title": "Preview audio while scrubbing: Fè w tande son pandan w ap glise tèt lekti a",
      "zoom_media_title": "Zoom sou medya: Zoom dirèkteman sou clip chwazi a (oswa Double-klike)",
      "fit_timeline_title": "Fit timeline — Ajiste afichaj: Mete tout longè montaj la vizib nan espas timeline lan",
      "zoom_out_tl_title": "Zoom −: Redui echèl tan an",
      "zoom_in_tl_title": "Zoom +: Agrandi echèl tan an pou travay pi presi",
      "master_volume_title": "Glise monte/desann pou regle volim (0% - 200%) • Woulèt sourit oswa Double-click pou 100%",
      "mute_title": "Koupe / Retabli son (Mute)",

      "track_video": "Track Video",
      "track_audio": "Track Audio",
      "track_sfx": "Track SFX (Efè son)",
      "track_image": "Track Imaj",
      "track_text": "Track Teks",
      "track_asset": "Track Asset",

      "render_modal_title": "Rann Videyo MP4",
      "render_preparing": "Ap prepare rann lan...",
      "render_init": "Inisyalizasyon...",
      "render_success": "Videyo MP4 ekspòte avèk siksè!",
      "cancel": "Kanpe",
      "download_mp4": "Telechaje MP4",
      "close": "Fèmen",

      "np_modal_title": "Nouvo Pwojè Kadans",
      "np_modal_sub": "Antre non nouvo pwojè videyo a epi chwazi fòma ekran an.",
      "np_name_lbl": "Non pwojè a",
      "np_ratio_lbl": "Fòma (Ratio)",
      "np_dur_lbl": "Dire videyo a (Minit & Segonn)",
      "np_lang_lbl": "Lang videyo a",
      "np_create_btn": "Kreye Pwojè a",

      "ai_director_title": "Kadans AI Director & MCP",
      "ai_open_wasdev": "↗ Chat WASDEV",
      "ai_open_wasdev_title": "Louvri Chat AI WASDEV la epi voye pwojè a",
      "ai_mcp_btn": "1-Click MCP",
      "ai_mcp_btn_title": "Konfigire MCP Kadans 1-Klik pou tout AI yo",
      "ai_checking": "Ap verifye koneksyon AI & MCP...",
      "ai_prompt_hint": "Ekri sa ou vle AI a fè nan videyo a (egz: <i>«Fè yon piblisite 45 segonn ak 4 sèn, vwa ElevenLabs ak sou-tit karaoke»</i>).",
      "ai_quick_4scenes": "4 Sèn Piblisite",
      "ai_quick_subtitles": "Sou-tit Karaoke",
      "ai_quick_cinema": "Look Sinema",
      "ai_input_placeholder": "Mande AI a monte oswa modifye videyo a...",
      "ai_send_btn": "Voye bay AI",
      "ai_clear_title": "Efase istwa chat la"
    },

    en: {
      "brand": "Kadans Timeline",
      "projects_btn_title": "Projects (new / open / switch)",
      "projects": "Projects",
      "new_project": "New project",
      "new_project_title": "Create a new Kadans project (Ctrl+N)",
      "video_title_placeholder": "Video title",
      "video_title_title": "Video title",
      "video_lang_title": "Video & voice language",
      "preview": "Preview",
      "preview_title": "Refresh preview",
      "html_export": "HTML",
      "html_export_title": "Export single standalone HTML file",
      "render_mp4": "Render MP4",
      "render_mp4_title": "Render video to MP4 (Final video file)",
      "save": "Save",
      "save_title": "Save project (Ctrl+S)",
      "ai_chat": "AI Chat",
      "ai_chat_title": "Open Kadans AI Chat & 1-Click MCP / AI CLI",
      "settings": "Settings",
      "settings_title": "Settings (ElevenLabs, MCP AI CLI, mic, encoding)",

      "rail_media": "Media",
      "rail_media_title": "Media — Project media",
      "rail_assets": "Assets",
      "rail_assets_title": "Assets — Graphic library",
      "rail_cat": "Catalog",
      "rail_cat_title": "Catalog — Models & Scenes",
      "rail_sfx": "SFX",
      "rail_sfx_title": "SFX — Sound effects",
      "rail_comp": "Compo",
      "rail_comp_title": "Compo — Scenes & Compositions",
      "rail_code": "Code",
      "rail_code_title": "Code — JSON Spec",
      "rail_lint": "Lint",
      "rail_lint_title": "Lint — Verify project",

      "drop_hint": "Drop here to add to current scene",
      "play_title": "Play / Pause (Space)",
      "replay_title": "Replay from 0",
      "zoom_out_title": "Zoom out ScreenView (-)",
      "zoom_fit_title": "Click to reset 100% Fit",
      "zoom_in_title": "Zoom in ScreenView (+)",
      "fit_title": "Fit ScreenView to screen",
      "snapshot_title": "Export current frame (PNG)",

      "prop_tab": "Props",
      "prop_tab_title": "Properties",
      "ai_tab": "AI Chat",
      "ai_tab_title": "AI Chat & 1-Click MCP / AI CLI",
      "color_tab": "Color",
      "color_tab_title": "Color (Color Grading)",
      "blend_tab": "Blend",
      "blend_tab_title": "Blend (Blending modes & Opacity)",
      "sound_tab": "Sound",
      "sound_tab_title": "Sound (Audio & Effects)",
      "effect_tab": "Effects",
      "effect_tab_title": "Effects (Filters & Visual effects)",
      "lut_tab": "LUT",
      "lut_tab_title": "LUT (Cinematic filters)",

      "undo_title": "Undo [Ctrl+Z]",
      "redo_title": "Redo [Ctrl+Y]",
      "select_title": "Select: Choose, move and adjust clips (V)",
      "split_title": "Split: Cut clip or scene at playhead (B)",
      "del_left_title": "Delete left: Remove clip part before playhead ([)",
      "del_right_title": "Delete right: Remove clip part after playhead (])",
      "delete_title": "Delete: Remove selected items (Del)",
      "freeze_title": "Freeze frame: Create static image at playhead",
      "reverse_title": "Reverse: Play video backwards",
      "mirror_title": "Mirror: Flip image horizontally",
      "rotate_title": "Rotate: Rotate image (+90°)",
      "crop_title": "Crop: Adjust framing",
      "record_title": "Record voice-over: Record voice directly into project",
      "add_track": "Add Track",
      "add_track_title": "Add track (Video, Audio, SFX, Image, Text, Asset)",
      "main_magnet_title": "Main track magnet",
      "snap_title": "Snapping",
      "linkage_title": "Linkage",
      "scrub_audio_title": "Audio scrubbing preview",
      "zoom_media_title": "Zoom to selected clip",
      "fit_timeline_title": "Fit timeline",
      "zoom_out_tl_title": "Zoom −",
      "zoom_in_tl_title": "Zoom +",
      "master_volume_title": "Drag up/down for master volume (0% - 200%) • Double-click for 100%",
      "mute_title": "Mute / Unmute",

      "track_video": "Video Track",
      "track_audio": "Audio Track",
      "track_sfx": "SFX Track (Sound effects)",
      "track_image": "Image Track",
      "track_text": "Text Track",
      "track_asset": "Asset Track",

      "render_modal_title": "Render Video MP4",
      "render_preparing": "Preparing render...",
      "render_init": "Initializing...",
      "render_success": "MP4 video exported successfully!",
      "cancel": "Cancel",
      "download_mp4": "Download MP4",
      "close": "Close",

      "np_modal_title": "New Kadans Project",
      "np_modal_sub": "Enter new project name and select screen ratio.",
      "np_name_lbl": "Project name",
      "np_ratio_lbl": "Ratio (Format)",
      "np_dur_lbl": "Video duration (Minutes & Seconds)",
      "np_lang_lbl": "Video language",
      "np_create_btn": "Create Project",

      "ai_director_title": "Kadans AI Director & MCP",
      "ai_open_wasdev": "↗ WASDEV Chat",
      "ai_open_wasdev_title": "Open project in WASDEV AI Chat",
      "ai_mcp_btn": "1-Click MCP",
      "ai_mcp_btn_title": "Configure Kadans MCP in 1 click for all AIs",
      "ai_checking": "Checking AI & MCP connection...",
      "ai_prompt_hint": "Type what you want the AI to do (e.g. <i>\"Create a 45s ad with 4 scenes, ElevenLabs voice, and karaoke subtitles\"</i>).",
      "ai_quick_4scenes": "4 Ad Scenes",
      "ai_quick_subtitles": "Karaoke Subtitles",
      "ai_quick_cinema": "Cinema Look",
      "ai_input_placeholder": "Ask AI to edit or create video...",
      "ai_send_btn": "Send to AI",
      "ai_clear_title": "Clear chat history"
    },

    es: {
      "brand": "Kadans Timeline",
      "projects_btn_title": "Proyectos (nuevo / abrir / cambiar)",
      "projects": "Proyectos",
      "new_project": "Nuevo proyecto",
      "new_project_title": "Crear nuevo proyecto Kadans (Ctrl+N)",
      "video_title_placeholder": "Título del vídeo",
      "video_title_title": "Título del vídeo",
      "video_lang_title": "Idioma del vídeo y voz",
      "preview": "Vista previa",
      "preview_title": "Actualizar vista previa",
      "html_export": "HTML",
      "html_export_title": "Exportar archivo HTML autónomo",
      "render_mp4": "Render MP4",
      "render_mp4_title": "Renderizar vídeo en MP4 (Archivo final)",
      "save": "Guardar",
      "save_title": "Guardar proyecto (Ctrl+S)",
      "ai_chat": "Chat IA",
      "ai_chat_title": "Abrir Chat IA Kadans y 1-Click MCP",
      "settings_title": "Configuración (ElevenLabs, MCP IA, micro, codificación)",

      "rail_media": "Medios",
      "rail_media_title": "Medios — Medios del proyecto",
      "rail_assets": "Recursos",
      "rail_assets_title": "Recursos — Biblioteca gráfica",
      "rail_cat": "Catálogo",
      "rail_cat_title": "Catálogo — Modelos y Escenas",
      "rail_sfx": "SFX",
      "rail_sfx_title": "SFX — Efectos de sonido",
      "rail_comp": "Compo",
      "rail_comp_title": "Compo — Escenas y Composiciones",
      "rail_code": "Código",
      "rail_code_title": "Código — JSON Spec",
      "rail_lint": "Lint",
      "rail_lint_title": "Lint — Verificar proyecto",

      "drop_hint": "Suelta aquí para añadir a la escena actual",
      "play_title": "Reproducir / Pausa (Espacio)",
      "replay_title": "Repetir desde 0",
      "zoom_out_title": "Alejar vista (-)",
      "zoom_fit_title": "Restablecer 100% Ajuste",
      "zoom_in_title": "Acercar vista (+)",
      "fit_title": "Ajustar al espacio",
      "snapshot_title": "Exportar fotograma (PNG)",

      "prop_tab": "Prop",
      "prop_tab_title": "Propiedades",
      "ai_tab": "Chat IA",
      "ai_tab_title": "Chat IA y 1-Click MCP",
      "color_tab": "Color",
      "color_tab_title": "Color (Gradación)",
      "blend_tab": "Mezcla",
      "blend_tab_title": "Mezcla y Opacidad",
      "sound_tab": "Sonido",
      "sound_tab_title": "Sonido y Efectos",
      "effect_tab": "Efectos",
      "effect_tab_title": "Efectos visuales",
      "lut_tab": "LUT",
      "lut_tab_title": "LUT cinematográfico",

      "undo_title": "Deshacer [Ctrl+Z]",
      "redo_title": "Rehacer [Ctrl+Y]",
      "select_title": "Seleccionar (V)",
      "split_title": "Dividir (B)",
      "del_left_title": "Eliminar a la izquierda ([)",
      "del_right_title": "Eliminar a la derecha (])",
      "delete_title": "Eliminar (Supr)",
      "freeze_title": "Congelar fotograma",
      "reverse_title": "Invertir reproducción",
      "mirror_title": "Espejo",
      "rotate_title": "Rotar (+90°)",
      "crop_title": "Recortar",
      "record_title": "Grabar voz en off",
      "add_track": "Añadir Pista",
      "add_track_title": "Añadir pista (Vídeo, Audio, SFX, Imagen, Texto, Recurso)",
      "main_magnet_title": "Imán pista principal",
      "snap_title": "Ajuste magnético",
      "linkage_title": "Vinculación",
      "scrub_audio_title": "Preescucha al arrastrar",
      "zoom_media_title": "Zoom al clip",
      "fit_timeline_title": "Ajustar línea de tiempo",
      "zoom_out_tl_title": "Zoom −",
      "zoom_in_tl_title": "Zoom +",
      "master_volume_title": "Arrastrar para volumen (0% - 200%) • Doble clic para 100%",
      "mute_title": "Silenciar / Activar sonido",

      "track_video": "Pista Vídeo",
      "track_audio": "Pista Audio",
      "track_sfx": "Pista SFX (Efectos de sonido)",
      "track_image": "Pista Imagen",
      "track_text": "Pista Texto",
      "track_asset": "Pista Recurso",

      "render_modal_title": "Renderizar Vídeo MP4",
      "render_preparing": "Preparando render...",
      "render_init": "Inicializando...",
      "render_success": "¡Vídeo MP4 exportado con éxito!",
      "cancel": "Cancelar",
      "download_mp4": "Descargar MP4",
      "close": "Cerrar",

      "np_modal_title": "Nuevo Proyecto Kadans",
      "np_modal_sub": "Ingresa el nombre del nuevo proyecto y selecciona el formato.",
      "np_name_lbl": "Nombre del proyecto",
      "np_ratio_lbl": "Formato (Ratio)",
      "np_dur_lbl": "Duración del vídeo (Minutos y Segundos)",
      "np_lang_lbl": "Idioma del vídeo",
      "np_create_btn": "Crear Proyecto",

      "ai_director_title": "Kadans AI Director y MCP",
      "ai_open_wasdev": "↗ Chat WASDEV",
      "ai_open_wasdev_title": "Abrir en el Chat IA de WASDEV",
      "ai_mcp_btn": "1-Click MCP",
      "ai_mcp_btn_title": "Configurar MCP Kadans en 1 clic",
      "ai_checking": "Comprobando conexión IA y MCP...",
      "ai_prompt_hint": "Escribe lo que quieres que la IA haga...",
      "ai_quick_4scenes": "4 Escenas Anuncio",
      "ai_quick_subtitles": "Subtítulos Karaoke",
      "ai_quick_cinema": "Look Cine",
      "ai_input_placeholder": "Pide a la IA editar el vídeo...",
      "ai_send_btn": "Enviar a la IA",
      "ai_clear_title": "Borrar historial del chat"
    },

    de: {
      "brand": "Kadans Timeline",
      "projects_btn_title": "Projekte (neu / öffnen / wechseln)",
      "projects": "Projekte",
      "new_project": "Neues Projekt",
      "new_project_title": "Neues Kadans-Projekt erstellen (Strg+N)",
      "video_title_placeholder": "Videotitel",
      "video_title_title": "Videotitel",
      "video_lang_title": "Sprache von Video & Stimme",
      "preview": "Vorschau",
      "preview_title": "Vorschau aktualisieren",
      "html_export": "HTML",
      "html_export_title": "Einzelne eigenständige HTML-Datei exportieren",
      "render_mp4": "MP4 Rendern",
      "render_mp4_title": "Video als MP4 rendern (Enddatei)",
      "save": "Speichern",
      "save_title": "Projekt speichern (Strg+S)",
      "ai_chat": "KI-Chat",
      "ai_chat_title": "Kadans KI-Chat & 1-Klick-MCP öffnen",
      "settings_title": "Einstellungen (ElevenLabs, MCP-KI, Mikro, Kodierung)",

      "rail_media": "Medien",
      "rail_media_title": "Medien — Projektmedien",
      "rail_assets": "Ressourcen",
      "rail_assets_title": "Ressourcen — Grafikbibliothek",
      "rail_cat": "Katalog",
      "rail_cat_title": "Katalog — Vorlagen & Szenen",
      "rail_sfx": "SFX",
      "rail_sfx_title": "SFX — Soundeffekte",
      "rail_comp": "Kompo",
      "rail_comp_title": "Kompo — Szenen & Kompositionen",
      "rail_code": "Code",
      "rail_code_title": "Code — JSON-Spezifikation",
      "rail_lint": "Lint",
      "rail_lint_title": "Lint — Projekt prüfen",

      "drop_hint": "Hier ablegen, um zur aktuellen Szene hinzuzufügen",
      "play_title": "Wiedergabe / Pause (Leertaste)",
      "replay_title": "Von Beginn abspielen",
      "zoom_out_title": "ScreenView verkleinern (-)",
      "zoom_fit_title": "Klicken für 100% Einpassen",
      "zoom_in_title": "ScreenView vergrößern (+)",
      "fit_title": "An Bildschirm anpassen",
      "snapshot_title": "Aktuelles Bild exportieren (PNG)",

      "prop_tab": "Eigenschaften",
      "prop_tab_title": "Eigenschaften",
      "ai_tab": "KI-Chat",
      "ai_tab_title": "KI-Chat & 1-Klick-MCP",
      "color_tab": "Farbe",
      "color_tab_title": "Farbe (Color Grading)",
      "blend_tab": "Mischung",
      "blend_tab_title": "Mischmodi & Deckkraft",
      "sound_tab": "Ton",
      "sound_tab_title": "Ton & Audioeffekte",
      "effect_tab": "Effekte",
      "effect_tab_title": "Visuelle Effekte",
      "lut_tab": "LUT",
      "lut_tab_title": "Kino-LUT-Filter",

      "undo_title": "Rückgängig [Strg+Z]",
      "redo_title": "Wiederholen [Strg+Y]",
      "select_title": "Auswählen (V)",
      "split_title": "Teilen (B)",
      "del_left_title": "Links löschen ([)",
      "del_right_title": "Rechts löschen (])",
      "delete_title": "Löschen (Entf)",
      "freeze_title": "Standbild erzeugen",
      "reverse_title": "Rückwärts abspielen",
      "mirror_title": "Spiegeln",
      "rotate_title": "Drehen (+90°)",
      "crop_title": "Zuschneiden",
      "record_title": "Voice-over aufnehmen",
      "add_track": "Spur hinzufügen",
      "add_track_title": "Spur hinzufügen (Video, Audio, SFX, Bild, Text, Ressource)",
      "main_magnet_title": "Hauptspuren-Magnet",
      "snap_title": "Einrasten",
      "linkage_title": "Verknüpfung",
      "scrub_audio_title": "Audio-Scrubbing-Vorschau",
      "zoom_media_title": "Auf Clip zoomen",
      "fit_timeline_title": "Zeitleiste anpassen",
      "zoom_out_tl_title": "Zoom −",
      "zoom_in_tl_title": "Zoom +",
      "master_volume_title": "Lautstärke ziehen (0% - 200%) • Doppelklick für 100%",
      "mute_title": "Stummschalten / Ton an",

      "track_video": "Videospur",
      "track_audio": "Audiospur",
      "track_sfx": "SFX-Spur (Soundeffekte)",
      "track_image": "Bildspur",
      "track_text": "Textspur",
      "track_asset": "Ressourcenspur",

      "render_modal_title": "Video rendern (MP4)",
      "render_preparing": "Rendering vorbereiten...",
      "render_init": "Initialisierung...",
      "render_success": "MP4-Video erfolgreich exportiert!",
      "cancel": "Abbrechen",
      "download_mp4": "MP4 herunterladen",
      "close": "Schließen",

      "np_modal_title": "Neues Kadans-Projekt",
      "np_modal_sub": "Projektnamen eingeben und Seitenverhältnis wählen.",
      "np_name_lbl": "Projektname",
      "np_ratio_lbl": "Format (Verhältnis)",
      "np_dur_lbl": "Videodauer (Minuten & Sekunden)",
      "np_lang_lbl": "Videosprache",
      "np_create_btn": "Projekt erstellen",

      "ai_director_title": "Kadans KI-Direktor & MCP",
      "ai_open_wasdev": "↗ WASDEV Chat",
      "ai_open_wasdev_title": "In WASDEV KI-Chat öffnen",
      "ai_mcp_btn": "1-Click MCP",
      "ai_mcp_btn_title": "Kadans MCP mit 1 Klick konfigurieren",
      "ai_checking": "KI- & MCP-Verbindung wird geprüft...",
      "ai_prompt_hint": "Geben Sie ein, was die KI tun soll...",
      "ai_quick_4scenes": "4 Werbeszenen",
      "ai_quick_subtitles": "Karaoke-Untertitel",
      "ai_quick_cinema": "Cinema-Look",
      "ai_input_placeholder": "KI bitten, das Video zu schneiden...",
      "ai_send_btn": "An KI senden",
      "ai_clear_title": "Chatverlauf löschen"
    }
  };

  // pt, it, ru: diksyonè konplè (anvan sa yo te tonbe sou es / fr / en pou prèske tout tèks yo)
  KADANS_DICT.pt = Object.assign({}, KADANS_DICT.en, {
    "projects_btn_title": "Projetos (novo / abrir / trocar)", "projects": "Projetos",
    "new_project": "Novo projeto", "new_project_title": "Criar um novo projeto Kadans (Ctrl+N)",
    "video_title_placeholder": "Título do vídeo", "video_title_title": "Título do vídeo",
    "video_lang_title": "Idioma do vídeo & voz", "preview": "Pré-visualizar", "preview_title": "Atualizar a pré-visualização",
    "html_export": "HTML", "html_export_title": "Exportar como um único arquivo HTML autônomo",
    "render_mp4": "Renderizar MP4", "render_mp4_title": "Renderizar o vídeo em MP4 (arquivo de vídeo final)",
    "save": "Salvar", "save_title": "Salvar o projeto (Ctrl+S)", "ai_chat": "Chat IA",
    "ai_chat_title": "Abrir Chat IA Kadans & MCP / CLI IA em 1 clique", "settings_title": "Configurações (ElevenLabs, MCP CLI IA, microfone, codificação)",
    "rail_media": "Mídia", "rail_media_title": "Mídia — Mídia do projeto",
    "rail_assets": "Recursos", "rail_assets_title": "Recursos — Biblioteca gráfica",
    "rail_cat": "Catálogo", "rail_cat_title": "Catálogo — Modelos & Cenas",
    "rail_sfx": "SFX", "rail_sfx_title": "SFX — Efeitos sonoros",
    "rail_comp": "Compo", "rail_comp_title": "Compo — Cenas & Composições",
    "rail_code": "Código", "rail_code_title": "Código — Especificação JSON",
    "rail_lint": "Lint", "rail_lint_title": "Lint — Verificar o projeto",
    "drop_hint": "Solte aqui para adicionar à cena atual",
    "play_title": "Reproduzir / Pausar (Espaço)", "replay_title": "Repetir desde o início",
    "zoom_out_title": "Afastar ScreenView (-)", "zoom_fit_title": "Clique para voltar a 100% Fit",
    "zoom_in_title": "Ampliar ScreenView (+)", "fit_title": "Ajustar ScreenView ao espaço da tela",
    "snapshot_title": "Exportar o quadro atual (PNG)",
    "prop_tab": "Prop", "prop_tab_title": "Propriedades", "ai_tab": "Chat IA", "ai_tab_title": "Chat IA & MCP / CLI IA em 1 clique",
    "color_tab": "Cor", "color_tab_title": "Cor (Correção de cor)", "blend_tab": "Mesclagem", "blend_tab_title": "Mesclagem (Modos & Opacidade)",
    "sound_tab": "Som", "sound_tab_title": "Som (Áudio & Efeitos)", "effect_tab": "Efeitos", "effect_tab_title": "Efeitos (Filtros & Efeitos visuais)",
    "lut_tab": "LUT", "lut_tab_title": "LUT (Filtros cinematográficos)",
    "undo_title": "Desfazer (Última ação) [Ctrl+Z]", "redo_title": "Refazer (Ação desfeita) [Ctrl+Y]",
    "select_title": "Selecionar: Escolher, mover e ajustar os clipes (V)",
    "split_title": "Dividir: Cortar o clipe ou a cena no cursor de reprodução (B)",
    "del_left_title": "Excluir à esquerda: Remover a parte antes do cursor ([)",
    "del_right_title": "Excluir à direita: Remover a parte depois do cursor (])",
    "delete_title": "Excluir: Remover os elementos selecionados (Del)",
    "freeze_title": "Congelar: Fixar uma imagem na posição atual", "reverse_title": "Inverter: Reproduzir o vídeo ao contrário",
    "mirror_title": "Espelhar: Inverter a imagem horizontalmente", "rotate_title": "Girar: Rodar a imagem (+90°)",
    "crop_title": "Recortar: Ajustar o enquadramento da imagem", "record_title": "Gravar narração: Gravar um comentário de áudio ao vivo",
    "add_track": "Adicionar Faixa", "add_track_title": "Adicionar uma faixa (Vídeo, Áudio, SFX, Imagem, Texto, Recurso)",
    "main_magnet_title": "Ímã da faixa principal", "snap_title": "Magnetismo (Alinhamento dos clipes)",
    "linkage_title": "Ligação (Movimento sincronizado dos elementos associados)", "scrub_audio_title": "Ouvir ao arrastar (Audio scrubbing)",
    "zoom_media_title": "Zoom na mídia selecionada", "fit_timeline_title": "Ajustar a linha do tempo à tela",
    "zoom_out_tl_title": "Zoom −: Reduzir a escala de tempo", "zoom_in_tl_title": "Zoom +: Ampliar a escala de tempo",
    "master_volume_title": "Arraste para cima/baixo para ajustar o volume (0% - 200%) • Clique duplo para 100%",
    "mute_title": "Silenciar / Ativar o som",
    "track_video": "Faixa de Vídeo", "track_audio": "Faixa de Áudio", "track_sfx": "Faixa SFX (Efeitos sonoros)",
    "track_image": "Faixa de Imagem", "track_text": "Faixa de Texto", "track_asset": "Faixa de Recurso",
    "render_modal_title": "Renderização de vídeo MP4", "render_preparing": "Preparando a renderização...",
    "render_init": "Inicializando...", "render_success": "Vídeo MP4 exportado com sucesso!",
    "cancel": "Cancelar", "download_mp4": "Baixar MP4", "close": "Fechar",
    "np_modal_title": "Novo Projeto Kadans", "np_modal_sub": "Digite o nome do novo projeto de vídeo e escolha o formato de tela.",
    "np_name_lbl": "Nome do projeto", "np_ratio_lbl": "Formato (Proporção)", "np_dur_lbl": "Duração do vídeo (Minutos & Segundos)",
    "np_lang_lbl": "Idioma do vídeo", "np_create_btn": "Criar Projeto",
    "ai_director_title": "Kadans AI Director & MCP", "ai_open_wasdev": "↗ Chat WASDEV", "ai_open_wasdev_title": "Abrir no Chat IA do WASDEV",
    "ai_mcp_btn": "MCP 1 clique", "ai_mcp_btn_title": "Configurar MCP Kadans em 1 clique para todas as IAs",
    "ai_checking": "Verificando a conexão IA & MCP...",
    "ai_prompt_hint": "Escreva o que deseja que a IA faça (ex.: <i>«Crie um anúncio de 45s com 4 cenas, voz ElevenLabs e legendas karaokê»</i>).",
    "ai_quick_4scenes": "4 Cenas Anúncio", "ai_quick_subtitles": "Legendas Karaokê", "ai_quick_cinema": "Look Cinema",
    "ai_input_placeholder": "Peça à IA para montar ou modificar o vídeo...", "ai_send_btn": "Enviar à IA", "ai_clear_title": "Apagar o histórico do chat"
  });
  KADANS_DICT.it = Object.assign({}, KADANS_DICT.en, {
    "projects_btn_title": "Progetti (nuovo / apri / cambia)", "projects": "Progetti",
    "new_project": "Nuovo progetto", "new_project_title": "Crea un nuovo progetto Kadans (Ctrl+N)",
    "video_title_placeholder": "Titolo del video", "video_title_title": "Titolo del video",
    "video_lang_title": "Lingua del video & voce", "preview": "Anteprima", "preview_title": "Aggiorna l'anteprima",
    "html_export": "HTML", "html_export_title": "Esporta in un unico file HTML autonomo",
    "render_mp4": "Rendering MP4", "render_mp4_title": "Esegui il rendering del video in MP4 (file video finale)",
    "save": "Salva", "save_title": "Salva il progetto (Ctrl+S)", "ai_chat": "Chat IA",
    "ai_chat_title": "Apri Chat IA Kadans & MCP / CLI IA in 1 clic", "settings_title": "Impostazioni (ElevenLabs, MCP CLI IA, microfono, codifica)",
    "rail_media": "Media", "rail_media_title": "Media — Media del progetto",
    "rail_assets": "Risorse", "rail_assets_title": "Risorse — Libreria grafica",
    "rail_cat": "Catalogo", "rail_cat_title": "Catalogo — Modelli & Scene",
    "rail_sfx": "SFX", "rail_sfx_title": "SFX — Effetti sonori",
    "rail_comp": "Compo", "rail_comp_title": "Compo — Scene & Composizioni",
    "rail_code": "Codice", "rail_code_title": "Codice — Specifica JSON",
    "rail_lint": "Lint", "rail_lint_title": "Lint — Verifica il progetto",
    "drop_hint": "Rilascia qui per aggiungere alla scena attuale",
    "play_title": "Riproduci / Pausa (Spazio)", "replay_title": "Riproduci dall'inizio",
    "zoom_out_title": "Rimpicciolisci ScreenView (-)", "zoom_fit_title": "Clicca per tornare al 100% Fit",
    "zoom_in_title": "Ingrandisci ScreenView (+)", "fit_title": "Adatta ScreenView allo spazio dello schermo",
    "snapshot_title": "Esporta il fotogramma attuale (PNG)",
    "prop_tab": "Prop", "prop_tab_title": "Proprietà", "ai_tab": "Chat IA", "ai_tab_title": "Chat IA & MCP / CLI IA in 1 clic",
    "color_tab": "Colore", "color_tab_title": "Colore (Correzione colore)", "blend_tab": "Fusione", "blend_tab_title": "Fusione (Modalità & Opacità)",
    "sound_tab": "Suono", "sound_tab_title": "Suono (Audio & Effetti)", "effect_tab": "Effetti", "effect_tab_title": "Effetti (Filtri & Effetti visivi)",
    "lut_tab": "LUT", "lut_tab_title": "LUT (Filtri cinematografici)",
    "undo_title": "Annulla (Ultima azione) [Ctrl+Z]", "redo_title": "Ripeti (Azione annullata) [Ctrl+Y]",
    "select_title": "Seleziona: Scegli, sposta e regola le clip (V)",
    "split_title": "Dividi: Taglia la clip o la scena alla testina (B)",
    "del_left_title": "Elimina a sinistra: Rimuovi la parte prima della testina ([)",
    "del_right_title": "Elimina a destra: Rimuovi la parte dopo la testina (])",
    "delete_title": "Elimina: Rimuovi gli elementi selezionati (Canc)",
    "freeze_title": "Fermo immagine: Blocca un'immagine nella posizione attuale", "reverse_title": "Inverti: Riproduci il video al contrario",
    "mirror_title": "Specchio: Capovolgi l'immagine orizzontalmente", "rotate_title": "Ruota: Ruota l'immagine (+90°)",
    "crop_title": "Ritaglia: Regola l'inquadratura dell'immagine", "record_title": "Registra voce fuori campo: Registra un commento audio dal vivo",
    "add_track": "Aggiungi Traccia", "add_track_title": "Aggiungi una traccia (Video, Audio, SFX, Immagine, Testo, Risorsa)",
    "main_magnet_title": "Magnete traccia principale", "snap_title": "Aggancio (Allineamento delle clip)",
    "linkage_title": "Collegamento (Spostamento sincronizzato degli elementi associati)", "scrub_audio_title": "Ascolto durante lo scorrimento (Audio scrubbing)",
    "zoom_media_title": "Zoom sul media selezionato", "fit_timeline_title": "Adatta la timeline allo schermo",
    "zoom_out_tl_title": "Zoom −: Riduci la scala temporale", "zoom_in_tl_title": "Zoom +: Ingrandisci la scala temporale",
    "master_volume_title": "Trascina su/giù per regolare il volume (0% - 200%) • Doppio clic per 100%",
    "mute_title": "Disattiva / Riattiva l'audio",
    "track_video": "Traccia Video", "track_audio": "Traccia Audio", "track_sfx": "Traccia SFX (Effetti sonori)",
    "track_image": "Traccia Immagine", "track_text": "Traccia Testo", "track_asset": "Traccia Risorsa",
    "render_modal_title": "Rendering video MP4", "render_preparing": "Preparazione del rendering...",
    "render_init": "Inizializzazione...", "render_success": "Video MP4 esportato con successo!",
    "cancel": "Annulla", "download_mp4": "Scarica MP4", "close": "Chiudi",
    "np_modal_title": "Nuovo Progetto Kadans", "np_modal_sub": "Inserisci il nome del nuovo progetto video e scegli il formato dello schermo.",
    "np_name_lbl": "Nome del progetto", "np_ratio_lbl": "Formato (Rapporto)", "np_dur_lbl": "Durata del video (Minuti & Secondi)",
    "np_lang_lbl": "Lingua del video", "np_create_btn": "Crea Progetto",
    "ai_director_title": "Kadans AI Director & MCP", "ai_open_wasdev": "↗ Chat WASDEV", "ai_open_wasdev_title": "Apri nella Chat IA di WASDEV",
    "ai_mcp_btn": "MCP 1 clic", "ai_mcp_btn_title": "Configura MCP Kadans in 1 clic per tutte le IA",
    "ai_checking": "Verifica della connessione IA & MCP...",
    "ai_prompt_hint": "Scrivi cosa vuoi che l'IA faccia (es.: <i>«Crea uno spot di 45s con 4 scene, voce ElevenLabs e sottotitoli karaoke»</i>).",
    "ai_quick_4scenes": "4 Scene Spot", "ai_quick_subtitles": "Sottotitoli Karaoke", "ai_quick_cinema": "Look Cinema",
    "ai_input_placeholder": "Chiedi all'IA di montare o modificare il video...", "ai_send_btn": "Invia all'IA", "ai_clear_title": "Cancella la cronologia della chat"
  });
  KADANS_DICT.ru = Object.assign({}, KADANS_DICT.en, {
    "projects_btn_title": "Проекты (новый / открыть / сменить)", "projects": "Проекты",
    "new_project": "Новый проект", "new_project_title": "Создать новый проект Kadans (Ctrl+N)",
    "video_title_placeholder": "Название видео", "video_title_title": "Название видео",
    "video_lang_title": "Язык видео и голоса", "preview": "Просмотр", "preview_title": "Обновить предпросмотр",
    "html_export": "HTML", "html_export_title": "Экспорт в один автономный HTML-файл",
    "render_mp4": "Рендер MP4", "render_mp4_title": "Отрендерить видео в MP4 (итоговый видеофайл)",
    "save": "Сохранить", "save_title": "Сохранить проект (Ctrl+S)", "ai_chat": "ИИ-чат",
    "ai_chat_title": "Открыть ИИ-чат Kadans и MCP / CLI ИИ в 1 клик", "settings_title": "Настройки (ElevenLabs, MCP CLI ИИ, микрофон, кодирование)",
    "rail_media": "Медиа", "rail_media_title": "Медиа — Медиа проекта",
    "rail_assets": "Ресурсы", "rail_assets_title": "Ресурсы — Графическая библиотека",
    "rail_cat": "Каталог", "rail_cat_title": "Каталог — Шаблоны и сцены",
    "rail_sfx": "SFX", "rail_sfx_title": "SFX — Звуковые эффекты",
    "rail_comp": "Компо", "rail_comp_title": "Компо — Сцены и композиции",
    "rail_code": "Код", "rail_code_title": "Код — JSON-спецификация",
    "rail_lint": "Lint", "rail_lint_title": "Lint — Проверить проект",
    "drop_hint": "Перетащите сюда, чтобы добавить в текущую сцену",
    "play_title": "Воспроизведение / Пауза (Пробел)", "replay_title": "Воспроизвести с начала",
    "zoom_out_title": "Уменьшить ScreenView (-)", "zoom_fit_title": "Нажмите, чтобы вернуть 100% Fit",
    "zoom_in_title": "Увеличить ScreenView (+)", "fit_title": "Вписать ScreenView в экран",
    "snapshot_title": "Экспорт текущего кадра (PNG)",
    "prop_tab": "Свойства", "prop_tab_title": "Свойства", "ai_tab": "ИИ-чат", "ai_tab_title": "ИИ-чат и MCP / CLI ИИ в 1 клик",
    "color_tab": "Цвет", "color_tab_title": "Цвет (Цветокоррекция)", "blend_tab": "Смешивание", "blend_tab_title": "Смешивание (Режимы и непрозрачность)",
    "sound_tab": "Звук", "sound_tab_title": "Звук (Аудио и эффекты)", "effect_tab": "Эффекты", "effect_tab_title": "Эффекты (Фильтры и визуальные эффекты)",
    "lut_tab": "LUT", "lut_tab_title": "LUT (Кинематографичные фильтры)",
    "undo_title": "Отменить (Последнее действие) [Ctrl+Z]", "redo_title": "Повторить (Отменённое действие) [Ctrl+Y]",
    "select_title": "Выделение: выбор, перемещение и настройка клипов (V)",
    "split_title": "Разрезать: разделить клип или сцену у курсора (B)",
    "del_left_title": "Удалить слева: убрать часть до курсора ([)",
    "del_right_title": "Удалить справа: убрать часть после курсора (])",
    "delete_title": "Удалить: убрать выбранные элементы (Del)",
    "freeze_title": "Стоп-кадр: зафиксировать изображение в текущей позиции", "reverse_title": "Реверс: воспроизвести видео задом наперёд",
    "mirror_title": "Зеркало: отразить изображение по горизонтали", "rotate_title": "Поворот: повернуть изображение (+90°)",
    "crop_title": "Кадрирование: настроить кадр изображения", "record_title": "Запись голоса: записать аудиокомментарий вживую",
    "add_track": "Добавить дорожку", "add_track_title": "Добавить дорожку (Видео, Аудио, SFX, Изображение, Текст, Ресурс)",
    "main_magnet_title": "Магнит основной дорожки", "snap_title": "Привязка (Выравнивание клипов)",
    "linkage_title": "Связь (Синхронное перемещение связанных элементов)", "scrub_audio_title": "Звук при перемотке (Audio scrubbing)",
    "zoom_media_title": "Масштаб выбранного медиа", "fit_timeline_title": "Вписать шкалу времени в экран",
    "zoom_out_tl_title": "Масштаб −: уменьшить шкалу времени", "zoom_in_tl_title": "Масштаб +: увеличить шкалу времени",
    "master_volume_title": "Тяните вверх/вниз для громкости (0% - 200%) • Двойной щелчок — 100%",
    "mute_title": "Выключить / Включить звук",
    "track_video": "Видеодорожка", "track_audio": "Аудиодорожка", "track_sfx": "Дорожка SFX (Звуковые эффекты)",
    "track_image": "Дорожка изображений", "track_text": "Текстовая дорожка", "track_asset": "Дорожка ресурсов",
    "render_modal_title": "Рендер видео MP4", "render_preparing": "Подготовка рендера...",
    "render_init": "Инициализация...", "render_success": "Видео MP4 успешно экспортировано!",
    "cancel": "Отмена", "download_mp4": "Скачать MP4", "close": "Закрыть",
    "np_modal_title": "Новый проект Kadans", "np_modal_sub": "Введите имя нового видеопроекта и выберите формат экрана.",
    "np_name_lbl": "Имя проекта", "np_ratio_lbl": "Формат (Соотношение)", "np_dur_lbl": "Длительность видео (Минуты и секунды)",
    "np_lang_lbl": "Язык видео", "np_create_btn": "Создать проект",
    "ai_director_title": "Kadans AI Director & MCP", "ai_open_wasdev": "↗ Чат WASDEV", "ai_open_wasdev_title": "Открыть в ИИ-чате WASDEV",
    "ai_mcp_btn": "MCP в 1 клик", "ai_mcp_btn_title": "Настроить MCP Kadans в 1 клик для всех ИИ",
    "ai_checking": "Проверка подключения ИИ и MCP...",
    "ai_prompt_hint": "Напишите, что должен сделать ИИ (напр.: <i>«Создай 45-секундную рекламу из 4 сцен с голосом ElevenLabs и караоке-субтитрами»</i>).",
    "ai_quick_4scenes": "4 рекламные сцены", "ai_quick_subtitles": "Караоке-субтитры", "ai_quick_cinema": "Кино-стиль",
    "ai_input_placeholder": "Попросите ИИ смонтировать или изменить видео...", "ai_send_btn": "Отправить ИИ", "ai_clear_title": "Очистить историю чата"
  });
  // Nouvo kle pou tout lang yo
  const _EXTRA = {
    ht: { ready: "pare", lang_name: "Kreyòl ayisyen" }, fr: { ready: "prêt", lang_name: "Français" },
    en: { ready: "ready", lang_name: "English" }, es: { ready: "listo", lang_name: "Español" },
    pt: { ready: "pronto", lang_name: "Português" }, it: { ready: "pronto", lang_name: "Italiano" },
    ru: { ready: "готово", lang_name: "Русский" }, de: { ready: "bereit", lang_name: "Deutsch" }
  };
  const _SETTINGS = { ht: { settings: "Paramèt" }, fr: { settings: "Paramètres" }, en: { settings: "Settings" }, es: { settings: "Configuración" }, pt: { settings: "Configurações" }, it: { settings: "Impostazioni" }, ru: { settings: "Настройки" }, de: { settings: "Einstellungen" } };
  for (const k in _EXTRA) Object.assign(KADANS_DICT[k], _EXTRA[k], _SETTINGS[k] || {});
  // v3.10 estabilite: konfli ak chanjman deyò, erè build
  const _STABLE = {
    ht: { conflict_text: "Montaj la chanje deyò Timeline la (AI, yon lòt onglet oswa yon script). Chanjman ou yo poko sove.",
          conflict_reload: "Pran vèsyon sou disk la", conflict_keep: "Kenbe pa m (ranplase l)", reloaded: "montaj la rechaje",
          reloaded_outside: "montaj la chanje deyò Timeline la — rechaje",
          build_errors: "Montaj la gen erè — aperçu a ak rann lan pa mete ajou jiskaske yo korije:",
          build_warnings: "Kite deyò nan aperçu a (pa yon imaj / fichye manke):",
          drop_audio_track: "son an mete sou yon track odyo (yon son pa ka yon kalk imaj)" },
    fr: { conflict_text: "Le montage a été modifié hors de la Timeline (IA, autre onglet ou script). Vos changements ne sont pas encore enregistrés.",
          conflict_reload: "Prendre la version du disque", conflict_keep: "Garder la mienne (remplacer)", reloaded: "montage rechargé",
          reloaded_outside: "le montage a changé hors de la Timeline — rechargé",
          build_errors: "Le montage contient des erreurs — l’aperçu et le rendu ne sont pas mis à jour tant qu’elles ne sont pas corrigées :",
          build_warnings: "Ignoré dans l’aperçu (pas une image / fichier manquant) :",
          drop_audio_track: "le son a été placé sur une piste audio (un son ne peut pas être un calque image)" },
    en: { conflict_text: "The edit was changed outside the Timeline (AI, another tab or a script). Your changes are not saved yet.",
          conflict_reload: "Take the version on disk", conflict_keep: "Keep mine (overwrite)", reloaded: "edit reloaded",
          reloaded_outside: "the edit changed outside the Timeline — reloaded",
          build_errors: "The edit has errors — preview and render are not updated until they are fixed:",
          build_warnings: "Left out of the preview (not a picture / missing file):",
          drop_audio_track: "the sound went on an audio track (a sound cannot be a picture layer)" },
    es: { conflict_text: "El montaje se modificó fuera de la Timeline (IA, otra pestaña o un script). Tus cambios aún no se guardaron.",
          conflict_reload: "Tomar la versión del disco", conflict_keep: "Conservar la mía (reemplazar)", reloaded: "montaje recargado",
          reloaded_outside: "el montaje cambió fuera de la Timeline — recargado",
          build_errors: "El montaje tiene errores — la vista previa y el render no se actualizan hasta corregirlos:",
          build_warnings: "Omitido en la vista previa (no es una imagen / archivo faltante):",
          drop_audio_track: "el sonido se colocó en una pista de audio (un sonido no puede ser una capa de imagen)" },
    pt: { conflict_text: "A montagem foi alterada fora da Timeline (IA, outra aba ou um script). Suas alterações ainda não foram salvas.",
          conflict_reload: "Usar a versão do disco", conflict_keep: "Manter a minha (substituir)", reloaded: "montagem recarregada",
          reloaded_outside: "a montagem mudou fora da Timeline — recarregada",
          build_errors: "A montagem tem erros — a prévia e o render não são atualizados até serem corrigidos:",
          build_warnings: "Ignorado na prévia (não é imagem / arquivo ausente):",
          drop_audio_track: "o som foi colocado numa faixa de áudio (um som não pode ser uma camada de imagem)" },
    it: { conflict_text: "Il montaggio è stato modificato fuori dalla Timeline (IA, un'altra scheda o uno script). Le tue modifiche non sono ancora salvate.",
          conflict_reload: "Usa la versione su disco", conflict_keep: "Tieni la mia (sostituisci)", reloaded: "montaggio ricaricato",
          reloaded_outside: "il montaggio è cambiato fuori dalla Timeline — ricaricato",
          build_errors: "Il montaggio contiene errori — anteprima e render non si aggiornano finché non vengono corretti:",
          build_warnings: "Escluso dall'anteprima (non è un'immagine / file mancante):",
          drop_audio_track: "il suono è stato messo su una traccia audio (un suono non può essere un livello immagine)" },
    ru: { conflict_text: "Монтаж изменён вне Timeline (ИИ, другая вкладка или скрипт). Ваши изменения ещё не сохранены.",
          conflict_reload: "Взять версию с диска", conflict_keep: "Оставить мою (заменить)", reloaded: "монтаж перезагружен",
          reloaded_outside: "монтаж изменён вне Timeline — перезагружен",
          build_errors: "В монтаже есть ошибки — превью и рендер не обновятся, пока их не исправить:",
          build_warnings: "Пропущено в превью (не изображение / файл отсутствует):",
          drop_audio_track: "звук помещён на аудиодорожку (звук не может быть слоем изображения)" },
    de: { conflict_text: "Der Schnitt wurde außerhalb der Timeline geändert (KI, anderer Tab oder ein Skript). Deine Änderungen sind noch nicht gespeichert.",
          conflict_reload: "Version auf der Festplatte nehmen", conflict_keep: "Meine behalten (ersetzen)", reloaded: "Schnitt neu geladen",
          reloaded_outside: "der Schnitt wurde außerhalb der Timeline geändert — neu geladen",
          build_errors: "Der Schnitt enthält Fehler — Vorschau und Render werden erst nach der Korrektur aktualisiert:",
          build_warnings: "In der Vorschau ausgelassen (kein Bild / Datei fehlt):",
          drop_audio_track: "der Ton wurde auf eine Audiospur gelegt (ein Ton kann keine Bildebene sein)" }
  };
  for (const k in _STABLE) Object.assign(KADANS_DICT[k], _STABLE[k]);
  // v3.12 dire estab + istorik montaj
  const _V312 = {
    ht: { dur_moved_head: "Dire chanje:", dur_moved: "Sèn {n}: {a} s → {b} s", dur_measured: "vrè vwa a",
          hist_btn: "Istorik", hist_tip: "Istorik montaj la: tout vèsyon yo (Timeline, AI, restorasyon) — remete youn",
          hist_title: "Istorik montaj la", hist_sub: "Chak vèsyon sove isit la. Remete youn = li vin vèsyon aktyèl la; vèsyon kounye a rete nan lis la.",
          hist_timeline: "Timeline", hist_outside: "Deyò (AI / script)", hist_ai: "AI", hist_restore_a: "Restorasyon", hist_ids: "ID sèn yo",
          hist_empty: "Poko gen okenn vèsyon.", hist_current: "aktyèl", hist_scenes: "sèn", hist_tracks: "pis",
          hist_restore: "Remete l", hist_restored: "vèsyon an remete", hist_close: "Fèmen" },
    fr: { dur_moved_head: "Durée modifiée :", dur_moved: "Scène {n} : {a} s → {b} s", dur_measured: "voix réelle",
          hist_btn: "Historique", hist_tip: "Historique du montage : toutes les versions (Timeline, IA, restauration) — en restaurer une",
          hist_title: "Historique du montage", hist_sub: "Chaque version est gardée ici. En restaurer une la rend actuelle ; la version actuelle reste dans la liste.",
          hist_timeline: "Timeline", hist_outside: "Extérieur (IA / script)", hist_ai: "IA", hist_restore_a: "Restauration", hist_ids: "ID des scènes",
          hist_empty: "Aucune version pour l’instant.", hist_current: "actuelle", hist_scenes: "scènes", hist_tracks: "pistes",
          hist_restore: "Restaurer", hist_restored: "version restaurée", hist_close: "Fermer" },
    en: { dur_moved_head: "Duration changed:", dur_moved: "Scene {n}: {a} s → {b} s", dur_measured: "real voice",
          hist_btn: "History", hist_tip: "Edit history: every version (Timeline, AI, restore) — restore one",
          hist_title: "Edit history", hist_sub: "Every version is kept here. Restoring one makes it current; the current version stays in the list.",
          hist_timeline: "Timeline", hist_outside: "Outside (AI / script)", hist_ai: "AI", hist_restore_a: "Restore", hist_ids: "Scene IDs",
          hist_empty: "No versions yet.", hist_current: "current", hist_scenes: "scenes", hist_tracks: "tracks",
          hist_restore: "Restore", hist_restored: "version restored", hist_close: "Close" },
    es: { dur_moved_head: "Duración cambiada:", dur_moved: "Escena {n}: {a} s → {b} s", dur_measured: "voz real",
          hist_btn: "Historial", hist_tip: "Historial del montaje: todas las versiones (Timeline, IA, restauración) — restaurar una",
          hist_title: "Historial del montaje", hist_sub: "Cada versión se guarda aquí. Restaurar una la vuelve actual; la versión actual queda en la lista.",
          hist_timeline: "Timeline", hist_outside: "Externo (IA / script)", hist_ai: "IA", hist_restore_a: "Restauración", hist_ids: "ID de escenas",
          hist_empty: "Aún no hay versiones.", hist_current: "actual", hist_scenes: "escenas", hist_tracks: "pistas",
          hist_restore: "Restaurar", hist_restored: "versión restaurada", hist_close: "Cerrar" },
    pt: { dur_moved_head: "Duração alterada:", dur_moved: "Cena {n}: {a} s → {b} s", dur_measured: "voz real",
          hist_btn: "Histórico", hist_tip: "Histórico da montagem: todas as versões (Timeline, IA, restauração) — restaurar uma",
          hist_title: "Histórico da montagem", hist_sub: "Cada versão fica guardada aqui. Restaurar uma a torna atual; a versão atual continua na lista.",
          hist_timeline: "Timeline", hist_outside: "Externo (IA / script)", hist_ai: "IA", hist_restore_a: "Restauração", hist_ids: "IDs das cenas",
          hist_empty: "Ainda não há versões.", hist_current: "atual", hist_scenes: "cenas", hist_tracks: "faixas",
          hist_restore: "Restaurar", hist_restored: "versão restaurada", hist_close: "Fechar" },
    it: { dur_moved_head: "Durata cambiata:", dur_moved: "Scena {n}: {a} s → {b} s", dur_measured: "voce reale",
          hist_btn: "Cronologia", hist_tip: "Cronologia del montaggio: tutte le versioni (Timeline, IA, ripristino) — ripristinarne una",
          hist_title: "Cronologia del montaggio", hist_sub: "Ogni versione è conservata qui. Ripristinarne una la rende attuale; la versione attuale resta nell’elenco.",
          hist_timeline: "Timeline", hist_outside: "Esterno (IA / script)", hist_ai: "IA", hist_restore_a: "Ripristino", hist_ids: "ID scene",
          hist_empty: "Ancora nessuna versione.", hist_current: "attuale", hist_scenes: "scene", hist_tracks: "tracce",
          hist_restore: "Ripristina", hist_restored: "versione ripristinata", hist_close: "Chiudi" },
    ru: { dur_moved_head: "Длительность изменена:", dur_moved: "Сцена {n}: {a} с → {b} с", dur_measured: "реальный голос",
          hist_btn: "История", hist_tip: "История монтажа: все версии (Timeline, ИИ, восстановление) — восстановить одну",
          hist_title: "История монтажа", hist_sub: "Каждая версия хранится здесь. Восстановленная становится текущей; текущая остаётся в списке.",
          hist_timeline: "Timeline", hist_outside: "Извне (ИИ / скрипт)", hist_ai: "ИИ", hist_restore_a: "Восстановление", hist_ids: "ID сцен",
          hist_empty: "Версий пока нет.", hist_current: "текущая", hist_scenes: "сцен", hist_tracks: "дорожек",
          hist_restore: "Восстановить", hist_restored: "версия восстановлена", hist_close: "Закрыть" },
    de: { dur_moved_head: "Dauer geändert:", dur_moved: "Szene {n}: {a} s → {b} s", dur_measured: "echte Stimme",
          hist_btn: "Verlauf", hist_tip: "Schnittverlauf: alle Versionen (Timeline, KI, Wiederherstellung) — eine wiederherstellen",
          hist_title: "Schnittverlauf", hist_sub: "Jede Version wird hier aufbewahrt. Wiederherstellen macht sie aktuell; die aktuelle Version bleibt in der Liste.",
          hist_timeline: "Timeline", hist_outside: "Extern (KI / Skript)", hist_ai: "KI", hist_restore_a: "Wiederherstellung", hist_ids: "Szenen-IDs",
          hist_empty: "Noch keine Versionen.", hist_current: "aktuell", hist_scenes: "Szenen", hist_tracks: "Spuren",
          hist_restore: "Wiederherstellen", hist_restored: "Version wiederhergestellt", hist_close: "Schließen" }
  };
  for (const k in _V312) Object.assign(KADANS_DICT[k], _V312[k]);
  // Pwojè vid sou Timeline la (Empty Project Support)
  const _EMPTY_PROJ = {
    fr: {
      timeline_empty_hint: "Timeline vide — Glissez une vidéo/photo ici ou cliquez sur [+] dans le catalogue pour commencer",
      timeline_empty_play_hint: "Timeline vide — ajoutez une scène ou un clip avant de lire"
    },
    ht: {
      timeline_empty_hint: "Timeline vid — Trennen yon videyo/foto isit la oswa klike [+] nan katalòg la pou kòmanse",
      timeline_empty_play_hint: "Timeline vid — ajoute yon sèn oswa yon clip anvan"
    },
    en: {
      timeline_empty_hint: "Empty timeline — Drag a video/photo here or click [+] in catalog to get started",
      timeline_empty_play_hint: "Empty timeline — add a scene or clip before playing"
    },
    es: {
      timeline_empty_hint: "Línea de tiempo vacía — Arrastra un video/foto aquí o haz clic en [+] en el catálogo para comenzar",
      timeline_empty_play_hint: "Línea de tiempo vacía — añade una escena o clip antes de reproducir"
    },
    pt: {
      timeline_empty_hint: "Linha do tempo vazia — Arraste um vídeo/foto aqui ou clique em [+] no catálogo para começar",
      timeline_empty_play_hint: "Linha do tempo vazia — adicione uma cena ou clipe antes de reproduzir"
    },
    it: {
      timeline_empty_hint: "Timeline vuota — Trascina un video/foto qui o fai clic su [+] nel catalogo per iniziare",
      timeline_empty_play_hint: "Timeline vuota — aggiungi una scena o un clip prima di riprodurre"
    },
    ru: {
      timeline_empty_hint: "Таймлайн пуст — Перетащите видео/фото сюда или нажмите [+] в каталоге, чтобы начать",
      timeline_empty_play_hint: "Таймлайн пуст — добавьте сцену или клип перед воспроизведением"
    },
    de: {
      timeline_empty_hint: "Timeline leer — Video/Foto hierher ziehen oder auf [+] im Katalog klicken, um zu beginnen",
      timeline_empty_play_hint: "Timeline leer — füge eine Szene oder einen Clip hinzu, bevor du abspielst"
    }
  };
  for (const k in _EMPTY_PROJ) Object.assign(KADANS_DICT[k], _EMPTY_PROJ[k]);

  // Remotion On-Demand Studio (8 lang)
  const _REMOTION_STRINGS = {
    fr: {
      remotion_title: "✦ Remotion Studio — Aperçu GPU dans Microsoft Edge",
      remotion_modal_title: "Moteur Remotion Studio (Zero-Bloat)",
      remotion_body: "Remotion vous permet de prévisualiser et rendre la vidéo avec toute l'accélération GPU de Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Principe Zero-Bloat : Remotion ne charge pas WASDEV ; il est installé une seule fois dans votre cache d'outils local et utilise le même spec.json Kadans.",
      remotion_installing: "⏳ Installation de Remotion sur le PC…",
      remotion_btn_install: "✦ Installer maintenant",
      remotion_btn_cancel: "Annuler"
    },
    ht: {
      remotion_title: "✦ Remotion Studio — Preview GPU nan Microsoft Edge",
      remotion_modal_title: "Motè Remotion Studio (Zero-Bloat)",
      remotion_body: "Remotion pèmèt ou jwenn yon preview an tan reyèl ak rann videyo a avèk tout akselerasyon GPU Microsoft Edge / Chromium.",
      remotion_zero_bloat_note: "✦ Prensip Zero-Bloat : Remotion pa chaje WASDEV; li enstale yon sèl fwa nan kach zouti lokal ou a epi li sèvi ak menm spec.json Kadans lan.",
      remotion_installing: "⏳ Ap enstale Remotion sou PC a…",
      remotion_btn_install: "✦ Enstale kounye a",
      remotion_btn_cancel: "Annile"
    },
    en: {
      remotion_title: "✦ Remotion Studio — GPU Preview in Microsoft Edge",
      remotion_modal_title: "Remotion Studio Engine (Zero-Bloat)",
      remotion_body: "Remotion enables real-time preview and video rendering with full GPU hardware acceleration in Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Zero-Bloat Principle: Remotion does not bloat WASDEV; it is installed once in your local tools cache and uses the exact same Kadans spec.json.",
      remotion_installing: "⏳ Installing Remotion on PC…",
      remotion_btn_install: "✦ Install now",
      remotion_btn_cancel: "Cancel"
    },
    es: {
      remotion_title: "✦ Remotion Studio — Vista previa GPU en Microsoft Edge",
      remotion_modal_title: "Motor Remotion Studio (Zero-Bloat)",
      remotion_body: "Remotion le permite previsualizar y renderizar vídeo con aceleración GPU completa en Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Principio Zero-Bloat: Remotion no recarga WASDEV; se instala una vez en la caché local de herramientas y usa el mismo spec.json de Kadans.",
      remotion_installing: "⏳ Instalando Remotion en el PC…",
      remotion_btn_install: "✦ Instalar ahora",
      remotion_btn_cancel: "Cancelar"
    },
    pt: {
      remotion_title: "✦ Remotion Studio — Pré-visualização GPU no Microsoft Edge",
      remotion_modal_title: "Motor Remotion Studio (Zero-Bloat)",
      remotion_body: "O Remotion permite pré-visualizar e renderizar vídeo com aceleração total de GPU no Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Princípio Zero-Bloat: O Remotion não sobrecarrega o WASDEV; ele é instalado uma vez no cache local de ferramentas e usa o mesmo spec.json do Kadans.",
      remotion_installing: "⏳ Instalando Remotion no PC…",
      remotion_btn_install: "✦ Instalar agora",
      remotion_btn_cancel: "Cancelar"
    },
    it: {
      remotion_title: "✦ Remotion Studio — Anteprima GPU in Microsoft Edge",
      remotion_modal_title: "Motore Remotion Studio (Zero-Bloat)",
      remotion_body: "Remotion consente di visualizzare in anteprima ed esportare video con piena accelerazione GPU in Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Principio Zero-Bloat: Remotion non appesantisce WASDEV; viene installato una sola volta nella cache degli strumenti e usa lo stesso spec.json di Kadans.",
      remotion_installing: "⏳ Installazione di Remotion sul PC…",
      remotion_btn_install: "✦ Installa ora",
      remotion_btn_cancel: "Annulla"
    },
    ru: {
      remotion_title: "✦ Remotion Studio — Предпросмотр GPU в Microsoft Edge",
      remotion_modal_title: "Движок Remotion Studio (Zero-Bloat)",
      remotion_body: "Remotion позволяет просматривать и рендерить видео с полным аппаратным ускорением GPU в Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Принцип Zero-Bloat: Remotion не перегружает WASDEV; он устанавливается один раз в локальный кэш инструментов и использует тот же spec.json Kadans.",
      remotion_installing: "⏳ Установка Remotion на ПК…",
      remotion_btn_install: "✦ Установить сейчас",
      remotion_btn_cancel: "Отмена"
    },
    de: {
      remotion_title: "✦ Remotion Studio — GPU-Vorschau in Microsoft Edge",
      remotion_modal_title: "Remotion Studio Engine (Zero-Bloat)",
      remotion_body: "Remotion ermöglicht Echtzeit-Vorschau und Video-Rendering mit voller GPU-Hardwarebeschleunigung in Microsoft Edge / Chromium (Zero-Bloat On-Demand).",
      remotion_zero_bloat_note: "✦ Zero-Bloat-Prinzip: Remotion belastet WASDEV nicht; es wird einmalig im lokalen Tool-Cache installiert und nutzt dieselbe Kadans spec.json.",
      remotion_installing: "⏳ Remotion wird auf dem PC installiert…",
      remotion_btn_install: "✦ Jetzt installieren",
      remotion_btn_cancel: "Abbrechen"
    }
  };
  for (const k in _REMOTION_STRINGS) Object.assign(KADANS_DICT[k], _REMOTION_STRINGS[k]);


  // ---- Tradiksyon tèks kreyòl ki ekri dirèkteman nan editor.js / index.html (tablo: kadans_phrases*.js) ----
  const P_IDX = { ht: 0, fr: 1, en: 2, es: 3, pt: 4, it: 5, ru: 6, de: 7 };
  let _phLang = null, _exact = new Map(), _frag = [], _fragDom = [];
  function _buildPh() {
    _phLang = currentLang; _exact = new Map(); _frag = []; _fragDom = [];
    const i = P_IDX[currentLang];
    if (!i) return; // kreyòl: tèks sous yo deja an kreyòl
    for (const r of (window.KADANS_PHRASES || [])) {
      const src = r[0], dst = r[i];
      if (!dst || dst === src) continue;
      const key = src.trim();
      if (!_exact.has(key)) _exact.set(key, dst.trim());
      if (r[8] === "m") { if (src.length >= 4) _frag.push([src, dst]); }
      else if (key.length >= 5) { _frag.push([src, dst]); if (key.length >= 6) _fragDom.push([src, dst]); }
    }
    const byLen = (a, b) => b[0].length - a[0].length;
    _frag.sort(byLen); _fragDom.sort(byLen);
  }
  // tp(s, dom): tradui yon tèks kreyòl ki an dur. dom=true: pa fragman kout (pou pa touche kontni itilizatè a)
  function tp(s, dom) {
    if (s == null) return s;
    s = String(s);
    if (_phLang !== currentLang) _buildPh();
    if (!_exact.size) return s;
    const tr = s.trim();
    if (!tr) return s;
    const ex = _exact.get(tr);
    if (ex != null) return s.replace(tr, ex);
    let out = s;
    for (const [a, b] of (dom ? _fragDom : _frag)) if (out.indexOf(a) >= 0) out = out.split(a).join(b);
    return out;
  }
  // ---- Obsèvatè DOM: chak tèks / tooltip ki parèt tradui touswit, anvan ekran an pentire ----
  const _SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, INPUT: 1, CODE: 1, PRE: 1, IFRAME: 1 };
  const _ATTRS = ["title", "placeholder"];
  const _txtSrc = new WeakMap();   // nœud tèks -> [sous kreyòl, dènye tradiksyon]
  const _attSrc = new WeakMap();   // eleman -> { title: [sous, tradiksyon], ... }
  function _trText(n) {
    const cur = n.nodeValue;
    if (!cur || cur.length > 400) return;
    const rec = _txtSrc.get(n);
    const src = (rec && rec[1] === cur) ? rec[0] : cur;
    const out = tp(src, true);
    if (out !== src || rec) {
      _txtSrc.set(n, [src, out]);
      if (out !== cur) n.nodeValue = out;
    }
  }
  function _trAttrs(el) {
    if (!el.getAttribute) return;
    let m = _attSrc.get(el);
    for (const a of _ATTRS) {
      const cur = el.getAttribute(a);
      if (!cur) continue;
      const rec = m && m[a];
      const src = (rec && rec[1] === cur) ? rec[0] : cur;
      const out = tp(src, true);
      if (out !== src || rec) {
        if (!m) { m = {}; _attSrc.set(el, m); }
        m[a] = [src, out];
        if (out !== cur) el.setAttribute(a, out);
      }
    }
  }
  function _skipEl(el) {
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      if (_SKIP[e.tagName] || e.isContentEditable) return true;
    }
    return false;
  }
  function _walk(root) {
    if (!root) return;
    if (root.nodeType === 3) { if (!_skipEl(root.parentElement)) _trText(root); return; }
    if (root.nodeType !== 1 || _skipEl(root)) return;
    _trAttrs(root);
    const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode: n => (n.nodeType === 1 && (_SKIP[n.tagName] || n.isContentEditable)) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
    });
    let n;
    while ((n = w.nextNode())) { if (n.nodeType === 3) _trText(n); else _trAttrs(n); }
  }
  let _mo = null, _touched = false;
  function _startObserver() {
    if (_mo || !document.body) return;
    _mo = new MutationObserver(muts => {
      if (currentLang === "ht" && !_touched) return;   // kreyòl: pa gen anyen pou fè (lejè)
      for (const m of muts) {
        if (m.type === "childList") m.addedNodes.forEach(_walk);
        else if (m.type === "characterData") { if (!_skipEl(m.target.parentElement)) _trText(m.target); }
        else if (m.type === "attributes" && !_skipEl(m.target)) _trAttrs(m.target);
      }
    });
    _mo.observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: _ATTRS });
  }
  function translateDom() {
    if (!document.body) return;
    if (currentLang !== "ht") _touched = true;
    if (_touched) _walk(document.body);
    _startObserver();
  }
  // Dyalòg natif yo (prompt / confirm / alert) tradui tou
  ["prompt", "confirm", "alert"].forEach(fn => {
    const orig = window[fn];
    if (typeof orig !== "function") return;
    window[fn] = function (m, ...rest) { return orig.call(window, tp(m), ...rest); };
  });

  function detectLang() {
    const urlParams = new URLSearchParams(window.location.search);
    const qLang = urlParams.get("lang");
    if (qLang && KADANS_DICT[qLang]) return qLang;
    const stored = localStorage.getItem("wasdev_kadans_lang");
    if (stored && KADANS_DICT[stored]) return stored;
    if (window.SPEC && window.SPEC.lang && KADANS_DICT[window.SPEC.lang]) return window.SPEC.lang;
    return "fr"; // Langue par défaut de l'interface
  }

  let currentLang = detectLang();

  function t(key, fallback) {
    const dict = KADANS_DICT[currentLang] || KADANS_DICT["fr"];
    return dict[key] || (KADANS_DICT["fr"] && KADANS_DICT["fr"][key]) || fallback || key;
  }

  function applyKadansI18n() {
    // Top bar
    const bProj = document.getElementById("bProj");
    if (bProj) bProj.title = t("projects_btn_title");
    const projname = document.getElementById("projname");
    if (projname && projname.textContent.trim() === "Pwoje") projname.textContent = t("projects");
    const bNewProj = document.getElementById("bNewProj");
    if (bNewProj) {
      const tip = t("new_project");
      bNewProj.title = `${tip} — ${t("new_project_title") || tip}`;
      bNewProj.setAttribute("data-tip", tip);
      bNewProj.setAttribute("data-sub", t("new_project_title") || "Ctrl+N");
      if (!bNewProj.querySelector("svg, [data-ico]")) {
        bNewProj.innerHTML = '<span data-ico="plus"></span>';
        if (typeof paintIcons === "function") paintIcons(bNewProj);
      }
    }
    const vtitle = document.getElementById("vtitle");
    if (vtitle) {
      vtitle.placeholder = t("video_title_placeholder");
      vtitle.title = t("video_title_title");
    }
    const vlang = document.getElementById("vlang");
    if (vlang) {
      vlang.title = t("video_lang_title");
      vlang.value = currentLang;
    }
    const bBuild = document.getElementById("bBuild");
    if (bBuild) {
      const tip = t("preview");
      bBuild.title = `${tip} — ${t("preview_title") || tip}`;
      bBuild.setAttribute("data-tip", tip);
      bBuild.setAttribute("data-sub", t("preview_title") || "");
      if (!bBuild.querySelector("svg, [data-ico]")) {
        bBuild.innerHTML = '<span data-ico="refresh"></span>';
        if (typeof paintIcons === "function") paintIcons(bBuild);
      }
    }
    const bExport = document.getElementById("bExport");
    if (bExport) {
      const tip = t("html_export") || "HTML";
      bExport.title = `${tip} — ${t("html_export_title") || tip}`;
      bExport.setAttribute("data-tip", tip);
      bExport.setAttribute("data-sub", t("html_export_title") || "");
      if (!bExport.querySelector("svg, [data-ico]")) {
        bExport.innerHTML = '<span data-ico="download"></span>';
        if (typeof paintIcons === "function") paintIcons(bExport);
      }
    }
    const bHistory = document.getElementById("bHistory");
    if (bHistory) {
      const tip = t("hist_btn") || "Istorik";
      bHistory.title = `${tip} — ${t("hist_tip") || tip}`;
      bHistory.setAttribute("data-tip", tip);
      bHistory.setAttribute("data-sub", t("hist_tip") || "");
      if (!bHistory.querySelector("svg, [data-ico]")) {
        bHistory.innerHTML = '<span data-ico="undo"></span>';
        if (typeof paintIcons === "function") paintIcons(bHistory);
      }
    }
    const bRender = document.getElementById("bRender");
    if (bRender) {
      const tip = t("render_mp4");
      bRender.title = `${tip} — ${t("render_mp4_title") || tip}`;
      bRender.setAttribute("data-tip", tip);
      bRender.setAttribute("data-sub", t("render_mp4_title") || "");
      if (!bRender.querySelector("svg, [data-ico]")) {
        bRender.innerHTML = '<span data-ico="film"></span>';
        if (typeof paintIcons === "function") paintIcons(bRender);
      }
    }
    const bSave = document.getElementById("bSave");
    if (bSave) {
      const tip = t("save");
      bSave.title = `${tip} — ${t("save_title") || tip}`;
      bSave.setAttribute("data-tip", tip);
      bSave.setAttribute("data-sub", t("save_title") || "Ctrl+S");
      if (!bSave.querySelector("svg, [data-ico]")) {
        bSave.innerHTML = '<span data-ico="save"></span>';
        if (typeof paintIcons === "function") paintIcons(bSave);
      }
    }
    const bTopAi = document.getElementById("bTopAi");
    if (bTopAi) {
      const tip = t("ai_chat") || "AI Chat";
      bTopAi.title = `${tip} — ${t("ai_chat_title") || tip}`;
      bTopAi.setAttribute("data-tip", tip);
      bTopAi.setAttribute("data-sub", t("ai_chat_title") || "");
      if (!bTopAi.querySelector("svg, [data-ico]")) {
        bTopAi.innerHTML = '<span data-ico="sparkles"></span>';
        if (typeof paintIcons === "function") paintIcons(bTopAi);
      }
    }
    const bSettings = document.getElementById("bSettings");
    if (bSettings) {
      const tip = t("settings") || "Paramètres";
      bSettings.title = `${tip} — ${t("settings_title") || tip}`;
      bSettings.setAttribute("data-tip", tip);
      bSettings.setAttribute("data-sub", t("settings_title") || "");
      if (!bSettings.querySelector("svg, [data-ico]")) {
        bSettings.innerHTML = '<span data-ico="settings"></span>';
        if (typeof paintIcons === "function") paintIcons(bSettings);
      }
    }

    // Rails
    const railMap = {
      media: ["rail_media", "rail_media_title"],
      assets: ["rail_assets", "rail_assets_title"],
      cat: ["rail_cat", "rail_cat_title"],
      sfx: ["rail_sfx", "rail_sfx_title"],
      comp: ["rail_comp", "rail_comp_title"],
      code: ["rail_code", "rail_code_title"],
      props: ["prop_tab", "prop_tab_title"],
      ai: ["ai_tab", "ai_tab_title"],
      color: ["color_tab", "color_tab_title"],
      blend: ["blend_tab", "blend_tab_title"],
      sound: ["sound_tab", "sound_tab_title"],
      effect: ["effect_tab", "effect_tab_title"],
      lut: ["lut_tab", "lut_tab_title"]
    };
    document.querySelectorAll(".rail-btn").forEach(btn => {
      const lt = btn.dataset.lt || btn.dataset.rt;
      if (lt && railMap[lt]) {
        btn.title = t(railMap[lt][1]);
        const rlbl = btn.querySelector(".rlbl");
        if (rlbl) rlbl.textContent = t(railMap[lt][0]);
      }
    });

    const bLint = document.getElementById("bLint");
    if (bLint) {
      bLint.title = t("rail_lint_title");
      const rlbl = bLint.querySelector(".rlbl");
      if (rlbl) rlbl.textContent = t("rail_lint");
    }

    const drophint = document.getElementById("drophint");
    if (drophint) drophint.textContent = t("drop_hint");

    // Preview bar
    const pbarMap = {
      bPlay: "play_title",
      bReplayP: "replay_title",
      pvZoomOut: "zoom_out_title",
      pvZoomLbl: "zoom_fit_title",
      pvZoomIn: "zoom_in_title",
      pvFit: "fit_title",
      bShot: "snapshot_title"
    };
    for (const [id, tkey] of Object.entries(pbarMap)) {
      const el = document.getElementById(id);
      if (el) el.title = t(tkey);
    }

    // Timeline bar
    const tlMap = {
      tUndo: "undo_title",
      tRedo: "redo_title",
      tSelect: "select_title",
      tSplit: "split_title",
      tDelLeft: "del_left_title",
      tDelRight: "del_right_title",
      tDelete: "delete_title",
      tFreeze: "freeze_title",
      tReverse: "reverse_title",
      tMirror: "mirror_title",
      tRotate: "rotate_title",
      tCrop: "crop_title",
      tRecord: "record_title",
      tMainMagnet: "main_magnet_title",
      tSnap: "snap_title",
      tLinkage: "linkage_title",
      tScrubAudio: "scrub_audio_title",
      tZoomMedia: "zoom_media_title",
      tFit: "fit_timeline_title",
      tZoomOut: "zoom_out_tl_title",
      tZoomIn: "zoom_in_tl_title",
      volTrack: "master_volume_title",
      volMute: "mute_title"
    };
    for (const [id, tkey] of Object.entries(tlMap)) {
      const el = document.getElementById(id);
      if (el) el.title = t(tkey);
    }
    const tAddTrack = document.getElementById("tAddTrack");
    if (tAddTrack) {
      tAddTrack.title = t("add_track_title");
      tAddTrack.innerHTML = `<span data-ico="plus"></span>${t("add_track")}`;
    }

    // Track menu
    const trackMenuMap = {
      video: "track_video",
      audio: "track_audio",
      sfx: "track_sfx",
      image: "track_image",
      text: "track_text",
      asset: "track_asset"
    };
    document.querySelectorAll("#trackmenu .mi").forEach(mi => {
      const tk = mi.dataset.tk;
      if (tk && trackMenuMap[tk]) {
        const ico = mi.querySelector("[data-ico]");
        const icoHtml = ico ? ico.outerHTML : "";
        mi.innerHTML = `${icoHtml}${t(trackMenuMap[tk])}`;
      }
    });

    // Render modal
    const rmTitle = document.getElementById("rmTitle");
    if (rmTitle) rmTitle.textContent = t("render_modal_title");
    const rmStageTxt = document.getElementById("rmStageTxt");
    if (rmStageTxt && rmStageTxt.textContent.includes("prepare")) rmStageTxt.textContent = t("render_preparing");
    const rmDetail = document.getElementById("rmDetail");
    if (rmDetail && rmDetail.textContent.includes("Inis")) rmDetail.textContent = t("render_init");
    const rmBtnCancel = document.getElementById("rmBtnCancel");
    if (rmBtnCancel) rmBtnCancel.textContent = t("cancel");
    const rmBtnDownload = document.getElementById("rmBtnDownload");
    if (rmBtnDownload) rmBtnDownload.textContent = t("download_mp4");
    const rmBtnClose = document.getElementById("rmBtnClose");
    if (rmBtnClose) rmBtnClose.textContent = t("close");

    // Tout rès tèks kreyòl ki an dur nan paj la (panèl, tooltip, mesaj)
    translateDom();
  }

  // Anndan WASDEV (embedded): lang entèfas la swiv lang sistèm WASDEV la — pa gen selektè lang.
  // Vèsyon GitHub (poukont li): selektè #vlang la rete, chwa a sove nan localStorage.
  let embedded = new URLSearchParams(window.location.search).has("lang");
  function setEmbedded(on) {
    embedded = !!on;
    document.documentElement.classList.toggle("kd-embedded", embedded);
    const v = document.getElementById("vlang");
    if (v) v.style.display = embedded ? "none" : "";
  }
  setEmbedded(embedded);   // touswit, anvan premye pentire a (pa gen selektè ki parèt epi disparèt)

  function setLanguage(lang) {
    if (!KADANS_DICT[lang]) lang = "fr";
    const changed = lang !== currentLang;
    currentLang = lang;
    if (!embedded) { try { localStorage.setItem("wasdev_kadans_lang", lang); } catch (e) {} }
    document.documentElement.lang = lang;
    applyKadansI18n();
    if (changed) window.dispatchEvent(new CustomEvent("kadans:lang_changed", { detail: { lang } }));
  }

  // Export to global scope
  window.KadansI18n = {
    t,
    tp,
    getLang: () => currentLang,
    setLang: setLanguage,
    apply: applyKadansI18n,
    isEmbedded: () => embedded,
    setEmbedded,
    dict: KADANS_DICT
  };

  // Run on DOM ready
  const _init = () => { document.documentElement.lang = currentLang; setEmbedded(embedded); applyKadansI18n(); };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", _init);
  } else {
    setTimeout(_init, 10);
  }
})();
