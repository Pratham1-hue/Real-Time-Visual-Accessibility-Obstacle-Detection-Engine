# Real-Time Visual Accessibility Obstacle Detection Engine

Most of us take walking down a street for granted. We glance, we dodge, we move on.
But for someone who is blind or has low vision, every sidewalk is a series of unknowns —
a parked car here, a stray bicycle there, a pole that seems to appear out of nowhere.

This project is a small step toward changing that. It turns an ordinary webcam
(or any camera you plug in) into a pair of "smart eyes" that:

1. **See** — a YOLOv8 model detects obstacles in real time (people, cars, chairs, doors, and the other 77 classes COCO knows about).
2. **Judge** — it estimates how far each obstacle roughly is, using a simple monocular size relationship.
3. **Speak** — when something gets closer than ~1.5 meters, a calm voice says *"person ahead"* or *"chair ahead"*, so you can react without staring at a screen.

And because it runs on a single laptop with no special hardware, it's meant to be a
base to build on — squeeze it onto a Raspberry Pi, hang it on a pair of glasses, add
haptic buzzes, whatever your imagination arrives at.

## Demo / Screenshots

> 📸 *Place your screenshots in an `assets/` folder next to this README and they'll show up automatically.*

![Obstacle detection with bounding boxes and distance labels](assets/screenshot-detection.png)

*Live feed: each obstacle gets a bounding box, its class name, and an estimated distance.*

![Alert zone visualization](assets/screenshot-alert.png)

*When an object crosses the danger threshold (< 1.5 m), the audio module fires a spoken warning.*

## How it actually works

The pipeline is deliberately simple — one pass through the detector per frame, then
a tiny bit of math, then audio:

```
Camera frame ──► YOLOv8 detector ──► bounding boxes + class names
                         │
                         ▼
              Monocular distance estimate
              (known_width × focal_length) / pixel_width
                         │
                         ▼
              dist < 1.5 m ? ──yes──► gTTS speaks "person ahead"
                         │
                         no
                         ▼
                  keep scanning
```

A few design decisions worth mentioning:

- **Bounding boxes only for confident detections.** Anything under 50% confidence
  is thrown away. A blind user hearing "car ahead!" three times a minute because a
  shadow looked like a car is worse than remaining silent.
- **Distance via classic pinhole math, not deep learning.** For obstacle avoidance you
  don't need centimeter precision — you need to know *"is that thing coming at me or is
  it across the street?"* A width-based estimate does that cheaply, in microseconds.
- **Audio alerts are throttled.** A 4-second cooldown plus non-blocking threading means
  the voice won't stutter-book itself into a loop just because you're standing still
  near a stationary object.
- **The overlay is for developers, not users.** The bounding boxes on screen help you
  debug; the actual assistive interface is the speaker.

## Diving into the code

The project layout is easy to navigate — it's designed such that each piece can be
swapped out individually:

```
├── main.py              # glue: camera loop → detection → distance → audio
├── core/
│   ├── detector.py      # YOLOv8 wrapper (conf > 0.5)
│   └── distance.py      # pinhole-based distance estimation
└── audio/
    └── feedback.py      # threaded gTTS voice alerts with cooldown
```

**Want to swap in a better detector?** `core/detector.py` is one class. Pass
`yolov8s.pt` for accuracy or a `.onnx` export for edge devices — nothing else changes.

**Want to calibrate the distance?** `core/distance.py` currently guesses a 0.5 m
average width and a focal length of 600. Measure a real object, tweak those two
constants, done. (Future roadmap: per-class widths — a car really is wider than a person.)

**Want different urgency sounds?** `audio/feedback.py` handles it all in one place —
swap gTTS for a local TTS engine (like Piper) if you want offline, faster speech.

## Getting started

Requirements: Python 3.8+ and a webcam. (First run will download the YOLOv8 weights, ~6 MB.)

```bash
# 1. Clone
git clone https://github.com/Pratham1-hue/Real-Time-Visual-Accessibility-Obstacle-Detection-Engine.git
cd Real-Time-Visual-Accessibility-Obstacle-Detection-Engine

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py
```

That's it. A preview window opens up titled **"Obstacle Engine"**. Do note:

- Press **`q`** to quit.
- The first run takes a moment while YOLOv8's weights download.
- Internet is needed for the voice alerts (gTTS synthesizes audio in the cloud).
- If something is "99.9 m away," that's the code's way of saying "no reliable estimate."

## Known limitations (being honest here)

- **Distance is approximate.** It's a monocular heuristic — good enough for "close vs far,"
  nowhere near metrology-grade.
- **No depth-per-object widths yet.** A razor-thin pole reads as far away; a person
  standing sideways reads closer than they are. Per-class width tables would fix most of this.
- **gTTS needs the internet** and round-trips to Google per alert. Fine for a demo; for
  a real assistive aid, go local-TTS.
- **`yolov8n` is the fastest, not the most accurate.** Small dim objects (phone cables!)
  will be missed. That's the accuracy/latency trade.

## Roadmap

- [ ] Per-class `known_width` table + one-time calibration wizard
- [ ] ONNX / TensorRT exports for Raspberry Pi, Jetson, or phone-based inference
- [ ] Directional audio (is the obstacle left, right, or dead center?)
- [ ] Haptic wristband feedback as a silent alternative to voice
- [ ] compile to a single-file desktop app

## Contributing

Found a bug, want to add a feature, or have an accessibility angle in mind?
Pull requests are very welcome — this is a project that exists to be built upon.

## License

MIT — use it, fork it, ship it, be nice.
