from cx_Freeze import setup, Executable
import cv2

setup(name="Dispersion Measurer",
      version="1.0",
      author="Sheraton MV",
      options={"build_exe": {"packages": ["cv2"]}},
      description="Analyze image for dispersion",
      executables=[Executable("easyrenamer.py")])
