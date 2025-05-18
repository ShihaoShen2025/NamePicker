import os
if os.name == 'nt':
    os.remove(".\\dist\\main\\_internal\\PySide6\\Qt6WebEngineCore.dll")
    os.remove(".\\dist\\main\\_internal\\PySide6\\opengl32sw.dll")
else:
    pass