# gemini-tenis

Inspiration comes from [this](https://x.com/FarzaTV/status/1928484483076087922) viral demo.

<img width="543" alt="Screenshot 2025-07-02 at 1 31 28 PM" src="https://github.com/user-attachments/assets/8d317156-f187-470c-8e26-5b7f7f60d6f2" />

'text.json' will be the file that overlays text on top of the video
`tenis.py` is mostly just an OpenCV visualizer.

To make this a real time product I'll need to:

1) Smartly send frames to Gemini (Gemini Video can only handle 1 FPS)
2) Use Gemini API to return content.
3) Render it.
