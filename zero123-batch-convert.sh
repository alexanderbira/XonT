#!/bin/bash
# A simple script that takes in PNG images from the directory input_dir and converts them to models grouped in target_dir.

input_dir=content/input
target_dir=content/output
zero_output_dir=outputs/zero123-sai
config_yaml=configs/zero123.yaml

while getopts ":i:o:" opt; do
  case $opt in
    i)
      input_zip="$OPTARG"
      if [[ ( "$input_zip" == *.tar.gz ) ]]
        then
          echo "Using input archive $input_zip..."
          tar -xvf "$input_zip" -C "$target_dir"
          echo "Extraction complete."
        else
          echo "Input file $input_zip is not a tar.gz archive."
          exit 1
      fi
      ;;
    o)
      output_zip="$OPTARG"
      if [[ ! "$output_zip" == *.tar.gz ]]
        then
          echo "Output file $input_zip is not a tar.gz archive."
          exit 1
      fi
      ;;
    ?:)
      echo "Invalid option: -$OPTARG"
      exit 1
      ;;
    :)
      echo "Required format of this script is:"
      echo "sh zero123-batch-convert -i INPUT_FILE.tar.gz -o OUTPUT_FILE.tar.gz."
      exit 1
      ;;
    esac
done

mkdir "$input_dir"
mkdir "$target_dir"

if [ ! -d "target_dir" ]
  then
    empty_target_dir=true
  else
    empty_target_dir=false
fi

for input_file in "$input_dir"/*:
do
    echo "Attempting to convert input file $input_file."
    if [ "$empty_target_dir" ]
      then
        mkdir $target_dir
        empty_target_dir=false
    fi
    # generate 3D model
    # split input and output names to remove extensions and paths
    basename=$(basename -- "$input_file")
    extension="${input_file##*.}"
    basename_without_ext=$(basename "$basename" ."$extension")
    if [ "$extension" == "png" ]
        then
          echo "Performing inference on $input_file, saving to $target_dir..."
          tmpdir="$zero_output_dir/$basename_without_ext"
          mkdir "$tmpdir"
          python launch.py --config "$config_yaml" --export --gpu 0 system.exporter_type=mesh-exporter resume="$tmpdir"
          cp -i "$tmpdir/save/it600-export/*" "$target_dir"
          rm -r "$tmpdir"
        else
          echo "Unrecognised extension $extension not compatible with expected type png, skipping file"
    fi
done

echo "Compressing files to $output_zip..."
tar -czvf "$output_zip" "$target_dir"
echo "Done!"

echo "Deleting input and output temporary folders..."
rm -r "$input_dir"
rm -r "$target_dir"
echo "Done!"

echo "Generation complete. Your converted files should be in $output_zip."