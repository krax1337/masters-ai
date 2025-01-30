import whisper

# Load the model (defaults to "base" which is smaller and faster)
model = whisper.load_model("tiny")

# Transcribe the audio file
result = model.transcribe("recording.mp3")

# Print the transcription
# print("Transcription:")
# print(result["text"])

# Open file to write results
with open("transcription.txt", "w", encoding="utf-8") as f:
    # Write full transcription
    f.write("Full Transcription:\n")
    f.write(result["text"])
    f.write("\n\nSegments in 30-second intervals:\n")
    
    # Process segments
    current_segment = ""
    current_start = 0

    for segment in result["segments"]:
        if segment['start'] - current_start >= 30:
            if current_segment:
                f.write(f"[{current_start:.2f}s -> {segment['start']:.2f}s] {current_segment}\n")
            current_segment = segment['text']
            current_start = segment['start']
        else:
            current_segment += " " + segment['text']

    # Write final segment if any
    if current_segment:
        f.write(f"[{current_start:.2f}s -> {segment['end']:.2f}s] {current_segment}\n")
