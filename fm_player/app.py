from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

# Set the frequency and other parameters
frequency = 162.55  # FM frequency in MHz
sample_rate = 48000
gain = 30

# Set the command for rtl_fm and ffmpeg
rtl_fm_cmd = f"rtl_fm -f {frequency}M -s {sample_rate} -g {gain} -"
ffmpeg_cmd = "ffmpeg -f s16le -ar 48k -ac 1 -i - -f mp3 -"

# Route for the index page
@app.route("/")
def index():
    return render_template("index.html")

# Route for the stream
@app.route("/stream")
def stream():
    # Start the rtl_fm and ffmpeg processes
    rtl_fm_process = subprocess.Popen(rtl_fm_cmd, shell=True, stdout=subprocess.PIPE)
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, shell=True, stdin=rtl_fm_process.stdout, stdout=subprocess.PIPE)

    # Return the stream as a response
    return Response(ffmpeg_process.stdout, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)