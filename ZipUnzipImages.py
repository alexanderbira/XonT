import os
import zipfile
import glob
import subprocess
import urllib3

INPUT_ZIP_FILEPATH = "inputs.zip"
INPUT_EXTRACTED_FILEPATH = "inputs"
TARGET_ZIP_FILEPATH = "outputs.zip"
TARGET_EXTRACTED_FILEPATH = "outputs"
ZERO_OUTPUT_DIR = "outputs/zero123-sai"
CONFIG_YAML = "configs/zero123.yaml"

with zipfile.ZipFile(INPUT_ZIP_FILEPATH, "r") as zip_ref:
    zip_ref.extractall(INPUT_EXTRACTED_FILEPATH)

with glob.glob(INPUT_EXTRACTED_FILEPATH + "/*") as input_files:
    for input_file in input_files:
        if input_file.endswith(".png"):
            print(f"Performing inference on {input_file}, saving to {TARGET_EXTRACTED_FILEPATH}")
            basename = os.path.basename(input_file)
            basename_without_extension = os.path.splitext(basename)[0]
            tmpdir = f"{ZERO_OUTPUT_DIR}/{basename_without_extension}"
            subprocess.Popen(f"mkdir {tmpdir}")
            subprocess.Popen(
                f"python launch.py --config {CONFIG_YAML} --export --gpu 0 "
                f"system.exporter_type=mesh-exporter resume={tmpdir}")

            subprocess.Popen(f"cp -i \"{tmpdir}/save/it600-export/*\" \"{TARGET_EXTRACTED_FILEPATH}\"")
            subprocess.Popen(f"rm -r \"{tmpdir}\"")

with glob.glob(TARGET_EXTRACTED_FILEPATH) as output_files:
    with zipfile.ZipFile(TARGET_ZIP_FILEPATH, "w") as output_zip:
        for output_file in output_files:
            output_basename = os.path.basename(output_file)
            output_zip.write(output_file, output_basename)
    output_zip.close()

subprocess.Popen(f"rm -r \"{INPUT_EXTRACTED_FILEPATH}\"")
subprocess.Popen(f"rm -r \"{TARGET_EXTRACTED_FILEPATH}\"")