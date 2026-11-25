#!/usr/bin/env python3
"""מרכיב רילס מקצועי מסרטון מקור + שכבות טקסט (PNG) לפי plan.json.

מה הוא עושה: מגדיל ל-1080x1920 באיכות גבוהה, מתקן צבע עדין, מכניס כל כותרת
עם החלקה קצרה למעלה ויציאה רכה, מנרמל את השמע ל-LUFS שנקבע ומוציא שתי גרסאות:
master לאינסטגרם/טיקטוק וגרסה קלה לאתר.

שימוש: python3 build_reel.py <plan.json> <תיקיית שכבות> <תיקיית פלט>
"""
import json
import subprocess
import sys
from pathlib import Path


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main():
    plan_path, ov_dir, out_dir = (Path(a) for a in sys.argv[1:4])
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    src = (plan_path.parent / plan["source"]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    W, H = plan.get("width", 1080), plan.get("height", 1920)
    total = duration(src)
    g = plan.get("grade", {})
    fade_in, fade_out, rise = 0.25, 0.2, 36

    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src)]
    overlays = plan["overlays"]
    for i, o in enumerate(overlays):
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{min(o['end'], total):.3f}",
                "-i", str(ov_dir / f"ov{i + 1:02d}.png")]

    f = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
         f"eq=contrast={g.get('contrast', 1.05)}:saturation={g.get('saturation', 1.1)}:gamma={g.get('gamma', 1.0)},"
         f"unsharp=5:5:{g.get('sharpen', 0.35)},fps=30,format=yuv420p[v0]"]
    last = "v0"
    for i, o in enumerate(overlays):
        s, e = o["start"], min(o["end"], total)
        hold = o.get("hold", False)  # כרטיס סיום נשאר עד הסוף בלי יציאה
        chain = f"[{i + 1}:v]format=rgba,fade=in:st={s}:d={fade_in}:alpha=1"
        if not hold:
            chain += f",fade=out:st={e - fade_out:.3f}:d={fade_out}:alpha=1"
        f.append(chain + f"[o{i}]")
        y = f"'if(lt(t-{s},{fade_in}),{rise}*(1-(t-{s})/{fade_in}),0)'"
        f.append(f"[{last}][o{i}]overlay=x=0:y={y}:enable='between(t,{s},{e})'[v{i + 1}]")
        last = f"v{i + 1}"

    lufs = plan.get("loudness", -16)
    f.append(f"[0:a]loudnorm=I={lufs}:TP=-1.5:LRA=11,afade=t=in:d=0.08,"
             f"afade=t=out:st={total - 0.7:.3f}:d=0.7,aresample=48000[a]")

    master = out_dir / plan.get("output", "reel-master.mp4")
    cmd += ["-filter_complex", ";".join(f), "-map", f"[{last}]", "-map", "[a]",
            "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(master)]
    subprocess.run(cmd, check=True)
    print(master)

    web = plan.get("web")
    if web:
        web_out = out_dir / web["output"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(master),
                        "-vf", f"scale={web.get('width', 720)}:-2:flags=lanczos",
                        "-c:v", "libx264", "-preset", "slow", "-crf", str(web.get("crf", 24)),
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                        "-movflags", "+faststart", str(web_out)], check=True)
        poster = out_dir / web.get("poster", "poster.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(web.get("poster_at", 0.9)), "-i", str(web_out),
                        "-frames:v", "1", "-q:v", "4", str(poster)], check=True)
        print(web_out)
        print(poster)


if __name__ == "__main__":
    main()
