@echo off
echo Building tongstock-adapter-skill release package...
python build.py %*
if errorlevel 1 (
    echo Build failed!
) else (
    echo Build completed successfully!
)
pause
