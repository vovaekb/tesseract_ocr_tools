import os
import numpy as np
import cv2
from argparse import ArgumentParser
from collections import defaultdict
import subprocess

MIN_FONT_SIZE = 10
MAX_FONT_SIZE = 40

training_fonts = {
    'arial_cd_bold': 'Arial Condensed Bold, Condensed',
    'arialblack': 'Arial Black',
    'arialbold': 'Arial Bold',
    'arialboldit': 'Arial Bold Italic',
    'context_extra_cond_ssi_bold': 'Context Extra Condensed SSi Bold',
    'dejavu_sans_bold': 'DejaVu Sans Bold',
    'dejavu_sans_mono_bold': 'DejaVu Sans Mono Bold',
    'helvetica_cd_blk': 'Helvetica Condensed Black, Heavy Condensed',
    'helvetica_compressed_bold': 'Helvetica Compressed Bold',
    'impact': 'Impact Condensed',
    'nimbus_sans_l_bold': 'Nimbus Sans L Bold',
    'nimbus_sans_l_bold_condensed': 'Nimbus Sans L Bold Condensed',
    'nimbus_sans_l_condensed': 'Nimbus Sans L Condensed',
    'oswald_bold': 'Oswald Bold',
    'oswald_bold_it': 'Oswald Bold Italic',
    'oswald_medium': 'Oswald Medium',
    'oswald_medium_bold': 'Oswald Medium Bold',
    'oswald_medium_bold_it': 'Oswald Medium Bold Italic',
    'oswald_semibold': 'Oswald Semi-Bold',
    'oswald_semibold_it': 'Oswald Semi-Bold Italic',
    'switzerland_cond': 'SwitzerlandCondensed'
}

digit_counts = defaultdict(int)

arg_parser = ArgumentParser()
arg_parser.add_argument("--file", help="image to preprocess")
arg_parser.add_argument(
    "--directory", help="directory with font images: used only if not None", default=None
)
arg_parser.add_argument(
    "--gen_tif",
    action="store_true",
    help="generate tif/box files from text file",
    default=False,
)
arg_parser.add_argument(
    "--output",
    help="directory to save results",
    default=os.path.join(os.getcwd(), "output"),
)
arg_parser.add_argument(
    "--segment",
    action="store_true",
    help="segment the font tif image into images of numbers",
    default=False,
)
args = arg_parser.parse_args()



def run_tif_generator():
    for code, font in training_fonts.items():
        # TODO: Make a step 2 for iterating over font sizes
        for i in range(MIN_FONT_SIZE, MAX_FONT_SIZE):
            print('Generate tif for font size: {}'.format(i))
            generate_tif_proc = subprocess.Popen(
                ["text2image",
                 "--fonts_dir=/usr/share/fonts",
                 "--text=amh.sample1.txt",
                 "--font={}".format(font),
                 "--outputbase=amh.{}.{}.exp0".format(code, i),
                 "--ptsize={}".format(i)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            stdout, stderr = generate_tif_proc.communicate()
            print(stdout)
            print(stderr)

def segment_image(file_path):
    print(f'Preprocessing file: {file_path}')
    output_path = args.output
    image = cv2.imread(file_path)
    retval, image_pages = cv2.imreadmulti(file_path)
    # print(len(image_pages))
    if image is None:
        return

    # image_np_array = np.asarray(image)
    # (origH, origW) = image_np_array.shape[:2]
    # origW, origH = image.size

    (origH, origW) = image.shape[:2]
    # print(origH)
    # print(origW)
    head, tail = os.path.split(file_path)
    file_name = os.path.splitext(tail)[0] # tail.split(".")[0]
    file_ext = os.path.splitext(tail)[1][1:] # tail.split(".")[1]
    # print(f'file_name: {file_name}')
    # print(file_ext)
    # 
    box_file_path = os.path.join(head, "{}.box".format(file_name))
    # print(box_file_path)
    line_count = 0
    with open(box_file_path) as file:
        for line in file:
            if line != '':
                # print(line)
                line = line.replace('\t', '')
                chunks = line.split(' ')
                if chunks[0] != '': # and line_count < 5:
                    digit = chunks[0]
                    page_index = int(chunks[-1])
                    page_image = image
                    if page_index > 0:
                        page_image = image.seek(page_index)
                    page_image_np_array = np.asarray(image)
                    # page_image = image_pages[page_index]
                    left, top, right, bottom = int(chunks[1]), origH-int(chunks[4])-1, int(chunks[3]), origH-int(chunks[2])-1 #-4553 # 4570 #chunks[1:5]
                    crop = page_image.crop((left, top, right, bottom+4)) # page_image_np_array[top:bottom+4, left:right] # page_image[top:bottom+4, left:right]
                    # print(crop[:5, :10])
                    # print(f'{left}, {top}, {right}, {bottom}')
                    digit_counts[digit] += 1
                    index = digit_counts[digit]
                    # print("{}_{}".format(digit, index))
                    '''
                    if digit == '9' and index == 85:
                        print(line)
                        print(f'{left}, {top}, {right}, {bottom}')
                    '''
                    # if not digit in digit_counts.keys():
                    #     digit_counts[digit] += 1
                    # else:
                    #     index = digit_counts
                    tif_file_path = os.path.join(output_path, "{}_{}.{}".format(digit, index,  file_ext)) # file_name,
                    # print(f'Saving tif: {tif_file_path}')
                    # crop_image = Image.fromarray(crop) #  np.uint32(crop))
                    # crop_image.save(tif_file_path, "TIFF")
                    # crop.save(tif_file_path, "TIFF", dpi=dpi)
                    cv2.imwrite(tif_file_path, crop)
                    line_count += 1


def run_number_segmenter():
    print('Running number segmenter')
    counter = 0
    for file in os.listdir(args.directory):
        file_path = os.path.join(args.directory, file)
        # print(file_path)
        if (
                not os.path.isdir(file_path)
                and not "box" in file
                # and counter < 10 # 120 # 240 # 1
        ):
            print(counter)
            segment_image(file_path)
            counter = counter + 1

if __name__ == "__main__":
    output_path = args.output
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if args.gen_tif:
        run_tif_generator()
    elif args.segment:
        if args.file is not None:
            file_path = args.file
            segment_image(file_path)
        else:
            run_number_segmenter()
