#!/bin/bash
echo "Building tongstock-adapter-skill release package..."
python3 build.py "$@"
if [ $? -eq 0 ]; then
    echo "Build completed successfully!"
else
    echo "Build failed!"
fi
