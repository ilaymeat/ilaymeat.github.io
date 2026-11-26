---
name: haim-benisty-method
description: The full method for editing video with Claude, from Haim Benisty's guide "עריכת וידאו בקלוד - המדריך המלא" (the five video types, the prompt structure, the eight magic phrases, the three tips), plus Bar's learning log of what worked and what did not. Use for any new video or edit, and when asked how to edit properly — עריכה נכונה, איך עורכים, שיטת עריכה, מושן גרפיקס, סרטון קולנועי, מוקאפ, אווטאר, edit properly, make a video.
---

# Editing video with Claude — the method

Source: the YouTube guide by Haim Benisty (@haim.benisty), "עריכת וידאו בקלוד - המדריך המלא" (youtu.be/E6fTSxKvwWw). Bar pasted its transcript on 2026-11-26. The learning log at the end holds Bar's own feedback, and it wins over everything above it.

## 1. A tidy working folder
One folder per project, for example `Claude/Projects/Video editing/`, holding:
- the brand kit: logo, colours, fonts, the design language
- images, music saved along the way, and earlier videos
Always read that folder first. Material the person put there wins over anything generic.

## 2. The five video types (decide first)
1. **Motion graphics** — every element is written in code: kinetic text, shapes, cute animations. Build it in HyperFrames (studio) with GSAP. It is the strongest type for explainers and promos.
2. **Camera video** — the person's own footage: cut it tight, then lay elements and effects over it that show what they are saying. Use the studio's talking-head flow.
3. **Cinematic** — AI-generated film clips woven into the edit, like an advert. This needs an outside generator (Magnific or Higgsfield). Those are paid, so ask Bar for approval before connecting or using one.
4. **Mockup** — a website or app shown inside realistic devices (phones, laptops), with light and reflections, for portfolios and clients. Build it in HyperFrames: a device frame with a screen recording or screenshots inside, and pseudo-3D tilt and parallax.
5. **Avatar** — talking characters, realistic or animated. This needs an outside generator, which is paid, so it also needs approval.

## 3. The prompt / brief structure (fill all six before building)
1. **Type**: which of the five types.
2. **Message**: what the video says.
3. **Goal and audience**: what it is for, and who watches it, where and how (for example, a background loop at a buffet event, so no speech is needed and the visuals must be calm and readable).
4. **Magic phrases**: pick the ones that fit (section 4).
5. **Sound**: voiceover, music, both or neither.
6. **Script first**: for a video built from scratch (motion graphics, cinematic, avatar), write a short script and storyboard and show it before the long build. Fixing the plan takes a minute; fixing an hour-long render takes an hour. For edits of existing footage, Bar prefers that work continues without stopping, so state the plan in one or two lines and build.

## 4. The eight magic phrases (what each one means in practice)
1. **Kinetic typography** — words fly in, scale, rotate and stack on the beat, one idea per screen. Use the studio effect `kinetic` and the cascade/slam patterns.
2. **Technical drawing** — blueprint grids, construction lines and diagrams that draw themselves (SVG `stroke-dashoffset`). It is ideal for explainers.
3. **3D elements** — pseudo-3D: layered parallax, perspective tilt (`rotateX`/`rotateY` with perspective), shadows and depth. It does not need real 3D.
4. **Continuous camera movement (one shot)** — no hard jumps: one virtual camera glides through all the scenes (zoom-through, pans across one large canvas).
5. **Cinematic finish** — film grain, a slightly rough background, cinematic light, vignette and a colour grade. The Color Grade recipe is in `video-codes`.
6. **Match cut** — a transition that links two shots by shape, motion or position (a circle becomes a sun, a spin out becomes a spin in, a zoom in becomes a zoom out).
7. **Beat-synced** — every cut and animation lands on the music's beat. The method is in `video-codes`, code 2.
8. **"Go all the way, don't spare effort"** — use every tool, check frames, fix what the check finds, and do not stop at the first version that renders.

## 5. The three tips
1. **Outside generators** (Magnific / Higgsfield) for cinematic clips and pro voiceover. They cost money, so ask first.
2. **A video-editing skill that learns**: after every video, write what worked and what did not into the learning log below. Praise goes in as "keep doing this"; corrections go in as rules.
3. **Device mockup models**: realistic devices for showing apps and websites. Keep any kit the person supplies in the project folder.

## 6. Learning log — Bar's feedback (these rules win)
- **Language**: every reply, report, note and on-screen explanation is in plain Hebrew only, with no English words in replies. Video titles may be English when that is the style.
- **A small animation in every video**: a doodle, a kinetic title or a motion-graphics touch.
- **Consistency**: what is on screen must match what is heard. Never show a photo with no person over someone's speech; show the speaker or the team. B-roll and photos go between the lines, over music.
- **Burned-in text in the source** must match the moment (a "YO DECIDO" banner may appear only on the "yo decido" line).
- **Captions**: plain white with a dark shadow, and no colour highlight unless asked. Make Hebrew, Spanish and bilingual versions when the speech is Spanish.
- **Music**: real, licensed tracks (Mixkit) beat synthesized ones. Music must be audible on a phone: measure the 300 Hz–8 kHz band, about 10–12 dB under the voice, full level between lines. Faster and more rhythmic is preferred for team and booth videos. Popular songs (Bad Bunny and so on) are added by Bar inside Instagram, so offer a version without sound.
- **Effects Bar liked**: zoom punch, flash, whip pan, speed ramp, spin, light leak, beat pulse, glitch, colour split, hand-drawn intro, chapter word slams, before/after sweep.
- **Effects that failed**: a tooth sparkle on a talking mouth (it looks odd when the head moves; use it only on a still, big smile); a light effect that outlives its object (end it when the object leaves the frame); transitions that reveal black edges (scale up while moving or rotating).
- **Ends**: no "until next time" while the trip is still going. Keep end titles true to the moment.
- **Always**: pull frames and look at them before sending; say plainly what was checked and what was not (audio is measured, not heard).
- **Cost and outside actions**: ask before anything paid or public (outside generators, publishing). Everything else, just do it and report.
