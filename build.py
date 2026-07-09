#!/usr/bin/env python3
import os
import zipfile
import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description='Build release package for tongstock-adapter-skill')
    parser.add_argument('--version', help='Version string (default: uses timestamp)', default=None)
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.abspath(__file__))
    skill_name = 'tongstock-adapter-skill'

    if args.version:
        version = args.version
    else:
        version = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    output_filename = f'{skill_name}-{version}.zip'
    output_path = os.path.join(project_root, 'release', output_filename)

    os.makedirs(os.path.join(project_root, 'release'), exist_ok=True)

    files_to_package = [
        ('SKILL.md', 'SKILL.md'),
    ]

    src_dir = os.path.join(project_root, 'scripts', 'src')
    exclude_patterns = ['__pycache__', '.pyc']
    for root, _, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)

            skip = False
            for pattern in exclude_patterns:
                if pattern in src_file or pattern in file:
                    skip = True
                    break
            if skip:
                continue

            dest_path = os.path.join('scripts', rel_path)
            files_to_package.append((src_file, dest_path))

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for src_path, dest_path in files_to_package:
            zf.write(src_path, dest_path)
            print(f'Added: {dest_path}')

    print(f'\nRelease package created: {output_path}')
    print(f'Total files: {len(files_to_package)}')


if __name__ == '__main__':
    main()
