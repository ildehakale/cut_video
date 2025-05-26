#!/usr/bin/env python3
import argparse, subprocess, sys, os, shutil

def find_ffmpeg():
    path = shutil.which("ffmpeg")
    if path is None:
        print("Error: ffmpeg not found. Install it and ensure it’s on your PATH.", file=sys.stderr)
        sys.exit(1)
    return path

def split_video(input_path: str, start: float, end: float, output_path: str):
    ffmpeg = find_ffmpeg()

    # if output_path is a directory, auto-generate a filename
    if os.path.isdir(output_path):
        base = os.path.splitext(os.path.basename(input_path))[0]
        s = f"{start:.2f}".replace('.', 'p')
        e = f"{end:.2f}".replace('.', 'p')
        output_path = os.path.join(output_path, f"{base}_{s}-{e}.mp4")

    if not os.path.isfile(input_path):
        print(f"Error: input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    if end <= start:
        print("Error: end time must be greater than start time.", file=sys.stderr)
        sys.exit(1)

    cmd = [
        ffmpeg, "-y",
        "-i", input_path,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Created clip: {output_path}")
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e.stderr.decode(), file=sys.stderr)
        sys.exit(e.returncode)


def main():
    p = argparse.ArgumentParser(description="Split a video segment via FFmpeg.")
    p.add_argument("-i", "--input",  required=True, help="Path to source video file")
    p.add_argument("-s", "--start",  required=True, type=float, help="Start time in seconds")
    p.add_argument("-e", "--end",    required=True, type=float, help="End time in seconds")
    p.add_argument("-o", "--output", required=True,
                   help="Output file (with extension) or directory for auto-named clip")
    args = p.parse_args()

    split_video(args.input, args.start, args.end, args.output)

if __name__ == "__main__":
    main()
