"""Kadans WASDEV — Remotion Bridge (Zero-Bloat On-Demand Engine).

Konvèti spec.json Kadans (sous inik verite a) an yon pwojè Remotion konplè
(Root.tsx, MainComposition.tsx, remotion.config.ts, package.json).
Pèmèt devlopè a preview ak rann videyo a avèk tout akselerasyon GPU Edge / Chromium.

By Getho Guerrier · GRAN LAKU COMPANY · https://wasdev.ai
"""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

# Rezolisyon ofisyèl pa rapò
RATIO_DIMS = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "1.91:1": (1200, 628),
    "16:9_4k": (3840, 2160),
    "21:9": (2560, 1080),
}


def get_dimensions(ratio_str: str | None) -> tuple[int, int]:
    """Retounen (lajè, wotè) pou yon ratio bay."""
    if not ratio_str:
        return (1920, 1080)
    key = str(ratio_str).strip()
    if key in RATIO_DIMS:
        return RATIO_DIMS[key]
    # Eseye matche si gen espas oswa fòma tankou 16/9
    key = key.replace("/", ":")
    return RATIO_DIMS.get(key, (1920, 1080))


def compute_spec_duration(spec: dict) -> float:
    """Kalkile dire total yon spec (sèn oswa tracks)."""
    # 1. Si gen yon dire dirèk
    dur = float(spec.get("duration") or spec.get("total_duration") or 0.0)
    if dur > 0:
        return dur

    # 2. Si gen tracks nan timeline nan
    tl = spec.get("timeline") or {}
    tracks = tl.get("tracks") or []
    max_track_end = 0.0
    for t in tracks:
        for c in t.get("clips") or []:
            try:
                st = float(c.get("start") or 0.0)
                d = float(c.get("dur") or c.get("duration") or 0.0)
                end = st + d
                if end > max_track_end:
                    max_track_end = end
            except (ValueError, TypeError):
                continue
    if max_track_end > 0:
        return max_track_end

    # 3. Si gen sèn
    scenes = spec.get("scenes") or []
    scene_dur = sum(float(s.get("duration") or 3.0) for s in scenes)
    if scene_dur > 0:
        return scene_dur

    return 10.0


def _generate_package_json(name: str = "kadans-remotion") -> str:
    pkg = {
        "name": name,
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "start": "remotion preview src/index.ts",
            "build": "remotion render src/index.ts KadansVideo out.mp4",
            "upgrade": "remotion upgrade"
        },
        "dependencies": {
            "@remotion/cli": "^4.0.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "remotion": "^4.0.0"
        },
        "devDependencies": {
            "@types/react": "^18.2.0",
            "typescript": "^5.0.0"
        }
    }
    return json.dumps(pkg, indent=2)


def _generate_tsconfig() -> str:
    cfg = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ESNext",
            "moduleResolution": "node",
            "jsx": "react-jsx",
            "strict": False,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True
        },
        "include": ["src"]
    }
    return json.dumps(cfg, indent=2)


def _generate_remotion_config() -> str:
    return """import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setChromiumOpenGlRenderer('angle');
"""


def _generate_index_ts() -> str:
    return """import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
"""


def _generate_root_tsx(width: int, height: int, fps: int, duration_frames: int) -> str:
    return f"""import React from 'react';
import {{ Composition }} from 'remotion';
import {{ MainComposition }} from './MainComposition';
import specData from './spec.json';

export const RemotionRoot: React.FC = () => {{
  const fps = {fps};
  const width = {width};
  const height = {height};
  const durationInFrames = {duration_frames};

  return (
    <Composition
      id="KadansVideo"
      component={{MainComposition}}
      durationInFrames={{durationInFrames}}
      fps={{fps}}
      width={{width}}
      height={{height}}
      defaultProps={{{{
        spec: specData,
      }}}}
    />
  );
}};
"""


def _generate_main_composition_tsx(spec: dict) -> str:
    return """import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from 'remotion';

export interface Scene {
  id?: string;
  type?: string;
  duration?: number;
  title?: string;
  subtitle?: string;
  voice?: string;
  html?: string;
  image?: string;
  video?: string;
  background?: any;
  transition?: string;
}

export interface TrackClip {
  id?: string;
  type?: string;
  start?: number;
  dur?: number;
  src?: string;
  name?: string;
  text?: string;
  html?: string;
  color?: string;
}

export interface Track {
  id?: string;
  name?: string;
  type?: string;
  clips?: TrackClip[];
}

export interface KadansSpec {
  brand?: {
    name?: string;
    colors?: {
      bg?: string;
      primary?: string;
      accent?: string;
      text?: string;
      muted?: string;
    };
  };
  ratio?: string;
  music?: {
    src?: string;
    file?: string;
    volume?: number;
    mood?: string;
  };
  scenes?: Scene[];
  timeline?: {
    tracks?: Track[];
  };
  captions?: {
    position?: string;
    style?: string;
  };
}

export const MainComposition: React.FC<{ spec: KadansSpec }> = ({ spec }) => {
  const { fps } = useVideoConfig();
  const brand = spec?.brand || {};
  const colors = brand.colors || {
    bg: '#0b0816',
    primary: '#8b5cf6',
    accent: '#0098ff',
    text: '#f3eefe',
    muted: '#94a3b8',
  };

  const scenes = spec?.scenes || [];
  const tracks = spec?.timeline?.tracks || [];
  const music = spec?.music;

  // Calculer début de chaque scène pour le mode scènes
  let currentSec = 0;
  const sceneItems = scenes.map((s, idx) => {
    const dur = s.duration || 3.0;
    const startSec = currentSec;
    currentSec += dur;
    return {
      scene: s,
      index: idx,
      startFrame: Math.round(startSec * fps),
      durationFrames: Math.max(1, Math.round(dur * fps)),
    };
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.bg || '#0b0816',
        color: colors.text || '#ffffff',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        overflow: 'hidden',
      }}
    >
      {/* 1. Mizik background si li egziste */}
      {music && (music.src || music.file) && (
        <Audio
          src={staticFile(music.src || music.file || '')}
          volume={typeof music.volume === 'number' ? music.volume : 0.3}
        />
      )}

      {/* 2. Si tracks egziste nan timeline nan (Multi-Pistes Mode) */}
      {tracks.length > 0 &&
        tracks.map((t, tIdx) => {
          return (
            <React.Fragment key={t.id || `track-${tIdx}`}>
              {(t.clips || []).map((c, cIdx) => {
                const startSec = c.start || 0;
                const durSec = c.dur || 3;
                const startF = Math.round(startSec * fps);
                const durF = Math.max(1, Math.round(durSec * fps));
                const isAudio = (t.type || '').toLowerCase().includes('audio') || (c.type || '').toLowerCase().includes('audio') || (c.type || '').toLowerCase().includes('voice');

                if (isAudio && c.src) {
                  return (
                    <Sequence
                      key={c.id || `clip-${tIdx}-${cIdx}`}
                      from={startF}
                      durationInFrames={durF}
                    >
                      <Audio src={staticFile(c.src)} />
                    </Sequence>
                  );
                }

                return (
                  <Sequence
                    key={c.id || `clip-${tIdx}-${cIdx}`}
                    from={startF}
                    durationInFrames={durF}
                  >
                    <ClipRenderer clip={c} colors={colors} />
                  </Sequence>
                );
              })}
            </React.Fragment>
          );
        })}

      {/* 3. Si se Mode Scènes (lè pa gen tracks oswa an paralèl) */}
      {tracks.length === 0 &&
        sceneItems.map((item) => (
          <Sequence
            key={item.scene.id || `scene-${item.index}`}
            from={item.startFrame}
            durationInFrames={item.durationFrames}
          >
            <SceneRenderer
              scene={item.scene}
              colors={colors}
              durationFrames={item.durationFrames}
            />
          </Sequence>
        ))}
    </AbsoluteFill>
  );
};

// Rann yon Clip pou Tracks
const ClipRenderer: React.FC<{ clip: TrackClip; colors: any }> = ({
  clip,
  colors,
}) => {
  const src = clip.src || '';
  const isVideo = src.match(/\\.(mp4|webm|mov|mkv)$/i) || clip.type === 'video';
  const isImage = src.match(/\\.(png|jpg|jpeg|webp|gif|svg)$/i) || clip.type === 'image';

  if (isVideo && src) {
    return (
      <AbsoluteFill>
        <Video
          src={staticFile(src)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </AbsoluteFill>
    );
  }

  if (isImage && src) {
    return (
      <AbsoluteFill>
        <Img
          src={staticFile(src)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </AbsoluteFill>
    );
  }

  // Tèks oswa HTML
  if (clip.html) {
    return (
      <AbsoluteFill
        style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
        dangerouslySetInnerHTML={{ __html: clip.html }}
      />
    );
  }

  return (
    <AbsoluteFill
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px',
        textAlign: 'center',
      }}
    >
      <div
        style={{
          fontSize: '3.5rem',
          fontWeight: 800,
          color: colors.text || '#ffffff',
          textShadow: '0 4px 24px rgba(0,0,0,0.7)',
        }}
      >
        {clip.text || clip.name || ''}
      </div>
    </AbsoluteFill>
  );
};

// Rann yon Sèn Kadans konplè
const SceneRenderer: React.FC<{
  scene: Scene;
  colors: any;
  durationFrames: number;
}> = ({ scene, colors, durationFrames }) => {
  const frame = useCurrentFrame();

  // Animasyon tranzisyon
  const opacity = interpolate(
    frame,
    [0, 10, durationFrames - 10, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const scale = interpolate(frame, [0, durationFrames], [1.0, 1.05], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const bg = scene.background;
  const bgSrc = typeof bg === 'string' ? bg : bg?.src;

  return (
    <AbsoluteFill style={{ opacity, transform: `scale(${scale})` }}>
      {/* Background imaj oswa videyo */}
      {bgSrc && (
        <AbsoluteFill>
          {bgSrc.match(/\\.(mp4|webm|mov)$/i) ? (
            <Video
              src={staticFile(bgSrc)}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          ) : (
            <Img
              src={staticFile(bgSrc)}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          )}
          <AbsoluteFill
            style={{
              backgroundColor: 'rgba(0,0,0,0.45)',
            }}
          />
        </AbsoluteFill>
      )}

      {/* Kontni HTML oswa Tit / Sou-tit */}
      {scene.html ? (
        <AbsoluteFill
          style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          dangerouslySetInnerHTML={{ __html: scene.html }}
        />
      ) : (
        <AbsoluteFill
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '60px',
            textAlign: 'center',
          }}
        >
          {scene.title && (
            <h1
              style={{
                fontSize: '4.5rem',
                fontWeight: 900,
                color: colors.primary || '#8b5cf6',
                margin: '0 0 20px 0',
                textShadow: '0 6px 30px rgba(0,0,0,0.8)',
                letterSpacing: '-0.02em',
              }}
            >
              {scene.title}
            </h1>
          )}

          {scene.subtitle && (
            <p
              style={{
                fontSize: '2.2rem',
                fontWeight: 600,
                color: colors.text || '#ffffff',
                margin: '0 0 30px 0',
                maxWidth: '85%',
                lineHeight: 1.3,
                textShadow: '0 4px 20px rgba(0,0,0,0.8)',
              }}
            >
              {scene.subtitle}
            </p>
          )}

          {scene.voice && (
            <div
              style={{
                background: 'rgba(15, 10, 30, 0.75)',
                border: '1px solid rgba(139, 92, 246, 0.4)',
                borderRadius: '16px',
                padding: '16px 28px',
                color: colors.text || '#ffffff',
                fontSize: '1.4rem',
                fontWeight: 500,
                maxWidth: '75%',
                boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
              }}
            >
              {scene.voice}
            </div>
          )}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
"""


def export_to_remotion(
    spec: dict,
    out_dir: Path | str,
    base_dir: Path | str = None,
    options: dict = None,
) -> dict:
    """Konvèti spec Kadans an yon pwojè Remotion otonòm pare pou preview oswa render."""
    out = Path(out_dir).resolve()
    src_dir = out / "src"
    public_dir = out / "public"
    src_dir.mkdir(parents=True, exist_ok=True)
    public_dir.mkdir(parents=True, exist_ok=True)

    opts = options or {}
    fps = int(opts.get("fps") or spec.get("fps") or 30)
    ratio = spec.get("ratio") or "16:9"
    width, height = get_dimensions(ratio)
    dur_sec = compute_spec_duration(spec)
    dur_frames = max(1, round(dur_sec * fps))

    # 1. package.json & tsconfig.json
    pkg_file = out / "package.json"
    if not pkg_file.exists():
        pkg_file.write_text(_generate_package_json(out.name), encoding="utf-8")

    tsconfig_file = out / "tsconfig.json"
    if not tsconfig_file.exists():
        tsconfig_file.write_text(_generate_tsconfig(), encoding="utf-8")

    remotion_cfg_file = out / "remotion.config.ts"
    if not remotion_cfg_file.exists():
        remotion_cfg_file.write_text(_generate_remotion_config(), encoding="utf-8")

    # 2. src/index.ts & src/Root.tsx & src/MainComposition.tsx
    (src_dir / "index.ts").write_text(_generate_index_ts(), encoding="utf-8")
    (src_dir / "Root.tsx").write_text(_generate_root_tsx(width, height, fps, dur_frames), encoding="utf-8")
    (src_dir / "MainComposition.tsx").write_text(_generate_main_composition_tsx(spec), encoding="utf-8")

    # 3. src/spec.json (exact copy of Kadans spec)
    (src_dir / "spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Kopye oswa symlink medya nan public/ pou staticFile travay
    if base_dir:
        base_p = Path(base_dir).resolve()
        for media_folder_name in ("medya", "media", "assets", "videos", "voices", "audio"):
            src_m = base_p / media_folder_name
            if src_m.is_dir():
                target_m = public_dir / media_folder_name
                if not target_m.exists():
                    try:
                        # Eseye kreye yon junction sou Windows oswa symlink
                        os.symlink(str(src_m), str(target_m), target_is_directory=True)
                    except (OSError, NotImplementedError):
                        try:
                            # Si symlink mande privilèj admin sou kèk vèsyon Windows, fè yon kopi lejè
                            shutil.copytree(str(src_m), str(target_m), dirs_exist_ok=True)
                        except Exception:
                            pass

    return {
        "ok": True,
        "project_dir": str(out),
        "entry": str(src_dir / "index.ts"),
        "width": width,
        "height": height,
        "fps": fps,
        "duration_seconds": dur_sec,
        "duration_frames": dur_frames,
    }
