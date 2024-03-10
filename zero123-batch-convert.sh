# A simple script that takes in PNG images from the directory input_dir and converts them to models grouped in target_dir.

input_dir=content/input
target_dir=content/output
zero_output_dir=outputs/zero123-sai
config_yaml=configs/zero123.yaml

empty_target_dir=[ !-d "target_dir" ]

for input_file in "$input_dir"/*:
do
    echo "Attempting to convert input file $input_file."
    if [ empty_target_dir ]
        then
            do mkdir $target_dir
            empty_target_dir=false
            done
    fi
    # generate 3D model
    # split input and output names to remove extensions and paths
    basename=$(basename -- "$input_file")
    extension="${input_file##*.}"
    basename_without_ext=$(basename "$basename" .$extension)
    if [ "$extension" == "png" ]
        then
            do echo "Performing inference on $input_file, saving to $target_dir..."
            tmpdir="outputs/zero123-sai/$basename_without_ext"
            mkdir $tmpdir
            python launch.py --config "$config_yaml" --export --gpu 0 system.exporter_type=mesh-exporter resume="$tmpdir"
            cp -i "$tmpdir/save/it600-export/*" "$target_dir"
            rm -r "$tmpdir"
            done
        else
            do echo "Unrecognised extension $extension not compatible with expected type png, skipping file"
            done
    fi
done

