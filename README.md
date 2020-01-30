# VoTT_csv_to_yolo

This is a simple script to convert image annotated with Vott v1/v2 to a yolo compatible format:

The training/validation set for Yolo models has the following components:
    - Images with objects(that has to be detected)
    - Text file corresponding each image which has the following composition: “Label_ID X_CENTER Y_CENTER WIDTH HEIGHT”

**Label_ID** is the numeric ID given to different classes that has to be determined starting from 0 i.e. if 3 classes has to be determined, cats,dogs and monkeys, IDs can be 0,1,2.

**X_CENTER** is the X coordinate of the centre of the object that has to be detected divided by the Image_width

**Y_CENTER** is the Y coordinate of the centre of the object that has to be detected divided by the Image_height

**WIDTH** is the width of the object that has to be detected divided by the Image_width

**HEIGHT** is the height of the object that has to be detected divided by the Image_height

## Requirements

```
pandas
opencv
```

## How to use

Annotate your images with VoTT. Export with the format "Comma Separated Values (CSV)". Use this command :

```
python convert_csv_to_yolo.py 
        --image_folder <path_to_your_image_directory> 
        --vott_csv <path_to_your_csv_from_vott> 
        --output_folder <path_to_your_desired_ouput_directory>
```

Arguments :

    - image_folder, default="images"
    
    - vott_csv, default="vott-csv-export/annotations.csv"
    
    - output_folder, default="output"
    
    - copy_images (optional), default=True : copy images from the image folder to the output folder

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Sources:
  - https://medium.com/@mehulgupta_7991/image-labelling-for-yolo-using-yolo-mark-c58eb75b77fd
