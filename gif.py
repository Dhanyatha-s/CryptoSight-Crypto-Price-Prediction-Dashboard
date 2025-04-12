from moviepy.editor import VideoFileClip

clip = VideoFileClip("vd.mp4").subclip(0, 20)  
clip = clip.resize(width=480)  # optional: resize
clip.write_gif("output.gif", fps=10)
