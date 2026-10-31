# Pakè son CC0 Kadans (`kadans/assets/sfx/`)

1. `python -I tools/sfx/fs_pick.py <dl>` — chèche chak son nan Freesound ak filtè «Creative Commons 0», verifye
   lisans lan sou paj son an, telechaje apèsi HQ a + `picks.json` (tit, otè, sous).
2. Telechaje pakè Kenney yo (CC0): https://kenney.nl/assets/rpg-audio ak https://kenney.nl/assets/impact-sounds,
   dezipe yo nan `<kenney>/rpg-audio` ak `<kenney>/impact-sounds`.
3. `python -I tools/sfx/build_pack.py <ffmpeg> <dl> <kenney> kadans/assets/sfx` — OGG Vorbis q5, SFX: silans devan
   retire + pik −3 dBFS; ambyans: bouk san koupi (fen an melanje ak kòmansman an), −22 LUFS; `index.json`.
4. `CREDITS.md` (tablo otè / sous) — pa obligatwa pou CC0, men pou respè otè yo.
5. SON AYISYEN (v2.90): `python -I tools/sfx/fs_pick_ht.py <dl2>` epi `python -I tools/sfx/add_pack.py <ffmpeg> <dl2>
   kadans/assets/sfx` (ajoute sèlman son ki poko nan index.json la). Ambyans ak pawòl yo verifye ak Whisper
   (lang moun k ap pale yo): sa ki pale yon lang ki pa koresponn ak Ayiti retire. `drum-rara` (tanbou men, pa rara)
   pa gen tag «rara».
