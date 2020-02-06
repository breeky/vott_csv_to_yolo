import pandas as pd
import argparse
import os
import cv2
import shutil


def get_shape_img(row):
    img = cv2.imread(os.path.join(FLAGS.image_folder, row.image))
    if img is None:
        row["valid"] = False
        return row
    row["img_width"] = img.shape[1]
    row["img_height"] = img.shape[0]
    return row


image_folder = "images"
vott_csv = "vott-csv-export/annotations.csv"
output_folder = "output"
if __name__ == "__main__":
    # surpress any inhereted default values
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    Command line options
    """
    parser.add_argument(
        "--image_folder",
        type=str,
        default=image_folder,
        help="Absolute path to the image files from the image tagging step with VoTT. Default is "
             + image_folder,
    )

    parser.add_argument(
        "--vott_csv",
        type=str,
        default=vott_csv,
        help="Absolute path to the *.csv file exported from VoTT. Default is "
             + vott_csv,
    )

    parser.add_argument(
        "--output_folder",
        type=str,
        default=output_folder,
        help="Absolute path to the output folder where the annotations in YOLO format should be saved. Default is "
             + output_folder,
    )

    parser.add_argument(
        "--copy_images",
        type=str,
        default=True,
        help="Whether copying images from image_folder to output_folder. Default is True."
    )

    FLAGS = parser.parse_args()

    csv = pd.read_csv(FLAGS.vott_csv)

    csv["valid"] = [True for i in range(len(csv))]

    csv["img_width"] = [0 for i in range(len(csv))]
    csv["img_height"] = [0 for i in range(len(csv))]
    csv = csv.apply(get_shape_img, axis=1)

    print("Invalid images (", len(csv[csv.valid == False].image.unique()), ") :")
    print(csv[csv.valid == False].image.unique())
    csv = csv[csv.valid == True]

    csv["x"] = ((csv.xmin + csv.xmax)/2) / csv["img_width"]
    csv["y"] = ((csv.ymin + csv.ymax)/2) / csv["img_height"]

    csv["w"] = (csv.xmax - csv.xmin) / csv["img_width"]
    csv["h"] = (csv.ymax - csv.ymin) / csv["img_height"]

    csv.label = pd.Categorical(csv.label)
    csv['code'] = csv.label.cat.codes

    csv.sort_values(by=["image"], inplace=True)

    # write .names file
    names = {}
    for code in csv.code.unique():
        names[code] = csv[csv.code == code].iloc[0]["label"]
    with open(os.path.join(FLAGS.output_folder, "classes.names"), "w") as output:
        for i in range(len(names)):
            output.write(names[i])
            output.write("\n")

    # write list of images file
    with open(os.path.join(FLAGS.output_folder, "train.txt"), "w") as output:
        for name in csv.image.unique():
            output.write("data/images/")
            output.write(name)
            output.write("\n")

    # write yolo data
    for name in csv.image.unique():
        if FLAGS.copy_images:
            shutil.copy(os.path.join(FLAGS.image_folder, name), os.path.join(FLAGS.output_folder, name))
        with open(os.path.join(FLAGS.output_folder, os.path.splitext(name)[0]) + ".txt", "w") as output:
            for i, row in csv[csv.image == name].iterrows():
                output.write(str(row["code"]))
                output.write(" ")
                output.write(str(row["x"]))
                output.write(" ")
                output.write(str(row["y"]))
                output.write(" ")
                output.write(str(row["w"]))
                output.write(" ")
                output.write(str(row["h"]))
                output.write("\n")

