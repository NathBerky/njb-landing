from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip

video = VideoFileClip("AppVideoAvatarInApp.mov")

# Function names for right panels
functions = ["Health Score", "Pitch Readiness", "Technical Readiness", "Regulatory Crystal Ball", 
             "Investor Matcher", "Failure Predictor"]

texts = [TextClip(txt, fontsize=28, color='white', font='Arial-Bold').set_position((video.w - 250, 80 + i*70)).set_duration(video.duration) for i, txt in enumerate(functions)]

final = CompositeVideoClip([video] + texts)

final.write_videofile("Avatar_Steps_Out_Simple.mov", fps=30)

print("Done! Saved as Avatar_Steps_Out_Simple.mov")