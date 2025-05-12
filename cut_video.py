import argparse
import cv2

def clip_video(input_path: str, output_path: str, start_sec: float, end_sec: float):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {input_path}")

    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # use "XVID" for .avi

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    start_frame = int(start_sec * fps)
    end_frame   = int(end_sec   * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_idx = start_frame

    while frame_idx < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print(f"Clipped frames {start_frame}–{frame_idx} to '{output_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trim a video by specifying start and end times (in seconds)."
    )
    parser.add_argument("input",  help="Path to input video")
    parser.add_argument("output", help="Path to save trimmed video")
    parser.add_argument(
        "--start", type=float, default=0.0,
        help="Start time in seconds (default: 0.0)"
    )
    parser.add_argument(
        "--end",   type=float, default=None,
        help="End time in seconds (default: till end of video)"
    )
    args = parser.parse_args()

    # If end not specified, read video length
    if args.end is None:
        cap = cv2.VideoCapture(args.input)
        fps    = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        args.end = frame_count / fps
        cap.release()

    if args.start < 0 or args.end <= args.start:
        parser.error("Invalid start/end times. Make sure 0 <= start < end.")

    clip_video(args.input, args.output, args.start, args.end)
