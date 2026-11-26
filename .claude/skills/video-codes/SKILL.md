---
name: video-codes
description: Five editing "codes" you can put in a request to get a professional edit — Color Grade, Beats and Cuts, Before and After, Hand Drawn, Motion Graphics Showreel. Use when a request names one of these codes (in English or Hebrew: קולור גריידינג, חיתוך על הביט, לפני ואחרי, ציור ביד, מושן גרפיקס), or asks for a "cinematic look", "cut on the beat", "split screen", "whiteboard animation" or "showreel".
---

# Video codes

Source: the five codes from Amichai Sheqel's reel (Facebook, "5 secret codes for Claude"). Each code below is a recipe built with the tools in this repo (ffmpeg, HyperFrames from the studio, Playwright for text). Several codes can be combined in one request. Every recipe ends the same way: pull frames, look at them, and only then send the video.

## 1. Color Grade — cinematic look
A consistent, film-like colour across all shots: slightly cool shadows, warm highlights, soft contrast curve, a light vignette and very light grain.

```
colorbalance=rs=-0.04:gs=-0.01:bs=0.07:rm=0.03:gm=0.0:bm=-0.03:rh=0.07:gh=0.02:bh=-0.06,
curves=master='0/0.03 0.25/0.22 0.5/0.5 0.75/0.79 1/0.97',
eq=contrast=1.06:saturation=1.08,vignette=angle=PI/5:mode=forward,noise=alls=2:allf=t,format=yuv420p
```
- Apply it to the finished edit so every shot gets the same look; encode at crf 22-23 (grain makes files heavy).
- Skin must stay natural. On dark night footage first lift it (`eq=gamma=1.3-1.5`), then grade.
- Warm variant (food, sunsets): swap the shadow/highlight signs (`rs=0.03 bs=-0.03 ... rh=0.05 bh=-0.08`).

## 2. Beats and Cuts — cut exactly on the beat
1. Music: the person's own track, or a free-licence track (Mixkit: free for commercial video, no credit needed).
2. Find the tempo and the first beat (onset autocorrelation; `edits/foie-gras-reel/beat.py` and the trip scripts show the method) and the drops (where the bass enters after a break).
3. Every shot lasts a whole number of beats (2 beats in montages, 1 beat in a finale). Place the strongest moment on the first drop, a calm shot in a musical break, and the peak (party, reveal) on the next drop.
4. Spoken lines keep their own length but are padded to whole beats so the grid never drifts.
5. Music under speech: about 10-12 dB below the voice in the 300 Hz-8 kHz band (what a phone plays), full level between lines (sidechain ducking).

## 3. Before and After — split screen
Left half from the "before" version, right half from the "after", a thin glowing divider and two labels (לפני / אחרי):
```
[0:v]crop=540:1920:0:0[l];[1:v]crop=540:1920:540:0[r];[l][r]hstack[s];[s][labels]overlay=0:0
```
Use it to show an effect of the edit (colour grade, cleaned audio, a redesigned dish, a renovation). 6-9 seconds is enough. Labels are rendered with Playwright in the brand font (Hebrew right to left).

## 4. Hand Drawn — whiteboard animation
An idea drawn live on white paper, a hand holding a marker moving with the line.
- Build it in HyperFrames: SVG line drawing on a white background; each path animates `stroke-dashoffset` from its length to 0; a hand-with-marker PNG follows the end of the current path; text titles are written the same way, letter by letter.
- One idea per scene, 3-5 seconds, black lines plus one accent colour.
- Never trace someone else's character or logo; draw simple original shapes (icons, arrows, a figure).

## 5. Motion Graphics Showreel — fast typography and shapes
Sharp transitions, big kinetic words and geometric shapes at a fast pace, on the beat.
- HyperFrames with GSAP: words slam in (scale 2 -> 1, 0.2 s), shapes wipe the frame between scenes (rectangles and circles scaling from 0 to cover the frame), whip pans with blur, a light flash on drops, glitch and colour split (rgbashift) on 1-2 hits.
- A new visual every beat or two; no more than one big effect on the same beat.
- Check with `hf.py check` and fix every error before rendering; transitions must never reveal black edges (scale up while moving or rotating).

## Rules for all codes
- Effects serve the story; when unsure, fewer effects.
- Hebrew text: right to left, numbers and Latin in `<bdi dir="ltr">`, bundled fonts only.
- Music only with a licence (own track, Mixkit, YouTube Audio Library). Popular songs are added by the person inside Instagram/TikTok.
- Look at frames before sending, and say what was checked and what was not (Claude cannot hear audio: levels are measured, not listened to).

## See also
The five video types, the eight magic phrases (kinetic typography, technical drawing, 3D elements, continuous camera movement, cinematic finish, match cut, beat-synced, "go all the way"), the brief structure and Bar's learning log: `.claude/skills/haim-benisty-method/SKILL.md`.
