import os
import sys
# import numpy as np
# import cv2
from argparse import ArgumentParser
# import imgaug.augmenters as iaa
# import skimage
# import shutils
import subprocess
import platform

all_fonts = [
    'arial_cd_bold', # 'Arial Condensed Bold, Condensed',
    'arialblack', #: 'Arial Black',
    'arialbold', #: 'Arial Bold',
    'arialboldit', #: 'Arial Bold Italic',
    'context_extra_cond_ssi_bold', #: 'Context Extra Condensed SSi Bold',
    'dejavu_sans_bold', #: 'DejaVu Sans Bold',
    'dejavu_sans_mono_bold', #: 'DejaVu Sans Mono Bold',
    'helvetica_cd_blk', #: 'Helvetica Condensed Black, Heavy Condensed',
    'helvetica_compressed_bold', #: 'Helvetica Compressed Bold',
    'impact', #: 'Impact Condensed',
    'nimbus_sans_l_bold', #: 'Nimbus Sans L Bold',
    'nimbus_sans_l_bold_condensed', #: 'Nimbus Sans L Bold Condensed',
    'nimbus_sans_l_condensed', #: 'Nimbus Sans L Condensed',
    'oswald_bold', #: 'Oswald Bold',
    'oswald_bold_it', #: 'Oswald Bold Italic',
    'oswald_medium', #: 'Oswald Medium',
    'oswald_medium_bold', #: 'Oswald Medium Bold',
    'oswald_medium_bold_it', #: 'Oswald Medium Bold Italic',
    'oswald_semibold', #: 'Oswald Semi-Bold',
    'oswald_semibold_it', #: 'Oswald Semi-Bold Italic',
    'switzerland_cond', #: 'SwitzerlandCondensed'
]

arg_parser = ArgumentParser()
arg_parser.add_argument(
    "--directory", help="directory with images: used only if not None", default=None
)
# arg_parser.add_argument(
#     "--load_tif",
#     action="store_true",
#     help="load tif image rather than jpg/png",
#     default=False,
# )
arg_parser.add_argument(
    "--output",
    help="directory to save results",
    default=os.path.join(os.getcwd(), "output"),
)
args = arg_parser.parse_args()



def run_trainer():
    # print('Change directory')
    os.chdir(args.directory)
    #
    # Create tr file
    #
    tif_files = [f for f in os.listdir(args.directory) if 'tif' in f]
    samples_count = len(tif_files)
    print(f'Total files: {samples_count}')
    '''
    print('Create box and tr file') # tr

    with open('training_log_1.txt', 'w') as f:
        f.write('Create tr file\n')

    counter = 0
    for file in tif_files: # os.listdir(args.directory):
        file_path = os.path.join(args.directory, file)
        if counter % 300 == 0: # 300
            print(counter)
        # print(file)
        # if (
        #         not os.path.isdir(file_path)
        #         and "tif" in file
        # ):
        head, tail = os.path.split(file_path)
        file_name = os.path.splitext(tail)[0]  # tail.split(".")[0]
        # file_ext = os.path.splitext(tail)[1][1:]  # tail.split(".")[1]
        box_file_path = os.path.join(head, "{}.box".format(file_name))
        tr_file_path = os.path.join(head, "{}.box.tr".format(file_name))
        # print(os.path.isfile(tr_file_path))
        if not os.path.isfile(tr_file_path):
            # Generate box
            # generate_box_proc = subprocess.Popen(
            #     ["tesseract", file_path, file_name, "--psm", "10", "batch.nochop", "makebox"], # "box.train"
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.STDOUT,
            # )
            # stdout, stderr = generate_box_proc.communicate()
            # # print(stdout)
            # # print(stderr)
            # if stderr:
            #     print('Error occurred')
            #     print(stderr)
            # Generate tr
            # print('Generate tr file')
            generate_tr_proc = subprocess.Popen(
                ["tesseract", file_path, box_file_path, "--psm", "13", "box.train"], # 6 # 10
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            stdout, stderr = generate_tr_proc.communicate()
            # print(stdout)
            # print(stderr)
            with open('training_log_1.txt', 'w') as f:
                f.write(f'{counter}: {file_name}\n')
                f.write(str(stdout))
                f.write('\n\n')
            if stderr:
                print('Error occurred')
                print(stderr)
            if counter < 3:
                print(stdout)

        counter += 1

    sys.exit()
    '''

    # '''
    #
    # 2. Create unicharset file
    print('Create unicharset file ...')
    # Note: step should be done manually
    #
    box_files = [f for f in os.listdir(args.directory) if f.endswith('box')]
    # unicharset_extractor_command = "unicharset_extractor {}".format(' '.join(box_files))
    # with open('unicharset_command.txt', 'w') as f:
    #     f.write(unicharset_extractor_command)

    unicharset_extractor_proc = subprocess.Popen(
        "unicharset_extractor *.box", # "ls *.box | xargs unicharset_extractor",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    # unicharset_extractor_proc = subprocess.Popen(
    #         ["unicharset_extractor", ' '.join(box_files)],
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,
    # )
    stdout, stderr = unicharset_extractor_proc.communicate()
    print(stdout)
    if stderr:
        print('Error occurred')
        print(stderr)

    with open('training_log_1.txt', 'w') as f:
        f.write("Create unicharset file ...\n")
        f.write("unicharset_extractor <box_files>\n")
        f.write(str(stdout))
        f.write("\n\n\n")
    # sys.exit()
    # '''

    # '''
    # 3. Cat tr files for the same font into single tr file
    final_training_directory = "TrainData"
    if not os.path.exists(final_training_directory):
        os.makedirs(final_training_directory)

    print('Cat tr files according to font')
    for font in all_fonts:
        print(f'Font: {font}')
        font_samples = [f for f in os.listdir(args.directory) if f.endswith('tr') and font in f]
        font_tr_file = f'TrainData/amh.{font}.tr'
        # font_samples = [f for f in ]
        cat_tr_file_proc = subprocess.Popen(
            "cat {}.*.tr > {}".format(font, font_tr_file), # "cat {} > {}".format(' '.join(font_samples), font_tr_file), # "cat {}*.tr > {}".format(font, font_tr_file),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        stdout, stderr = cat_tr_file_proc.communicate()
        # print(stdout)
        if stderr:
            print('Error occurred')
            print(stderr)

        # if os.path.isfile(font_tr_file):
        #     shutils.copy(font_tr_file, os.path.join(os.getcwd(), final_training_directory, font_tr_file))

        with open('training_log_1.txt', 'a+') as f:
            f.write('\nCat tr files according to font ...\n')
            f.write("cat {}*.tr > {}.tr\n".format(font, font))
            f.write(str(stdout)+'\n')
            f.write('\n')

    # '''

    os.replace('unicharset', 'TrainData/unicharset')

    os.chdir('TrainData')

    tr_files = [f for f in os.listdir(".") if f.endswith('tr')]
    samples_count = len(tr_files)
    print(samples_count)

    # '''
    # 4. Create the font_properties file
    print('Create the font_properties file ...')

    # fontprops_file = os.path.join(args.directory, "font_properties")
    with open("font_properties", "w") as file:
        for font in range(samples_count):
            file.write("t 0 0 0 0 0\n")
    sys.exit()

    '''
    # 4. Clustering
    print('Clustering ...')

    # tr_files = [f for f in os.listdir(args.directory) if f.endswith('tr')]
    # print(f'Total tr files: {len(tr_files)}')

    # Workaround: run command manually
    clustering_command = "shapeclustering -F font_properties –U unicharset {}".format(' '.join(tr_files))
    with open('clustering_command.txt', 'w') as f:
        f.write(clustering_command)

    clustering_proc = subprocess.Popen( # 'forfiles /m *.tr /c "shapeclustering -F font_properties –U unicharset"',
        "ls amh.*.tr | xargs shapeclustering -F font_properties -U unicharset", #["shapeclustering", "-F", "font_properties", "–U", "unicharset", ' '.join(tr_files)],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = clustering_proc.communicate()
    print(stdout)
    if stderr:
        print('Error occurred')
        print(stderr)

    with open('training_log_1.txt', 'a+') as f:
        f.write('\n\nCreate unicharset file ...')
        f.write("shapeclustering -F font_properties –U unicharset <tr_files>")
        f.write(str(stdout))
        f.write("\n\n")
    # sys.exit()
    '''

    '''
    # 5. Shapetable
    print('Shapetable ...')
    # Workaround: run command manually
    # mftraining_command = "mftraining -F font_properties –U unicharset {}".format(' '.join(tr_files))
    # with open('mftraining_command.txt', 'w') as f:
    #     f.write(mftraining_command)

    mftraining_proc = subprocess.Popen(
        "ls *.tr | xargs mftraining -F font_properties –U unicharset", # ["mftraining", "-F", "font_properties", "–U", "unicharset", ' '.join(tr_files)],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = mftraining_proc.communicate()
    print(stdout)
    with open('training_log_1.txt', 'a+') as f:
        f.write('\n\nShapetable ...')
        f.write("mftraining -F font_properties –U unicharset <tr_files>")
        f.write(str(stdout))

    if stderr:
        print('Error occurred')
        print(stderr)
    # sys.exit()
    '''

    '''
    # 6. Normproto
    print('Normproto ...')
    # Workaround: run command manually
    # cntraining_command = "cntraining {}".format(' '.join(tr_files))
    # with open('cntraining_command.txt', 'w') as f:
    #     f.write(cntraining_command)

    cntraining_proc = subprocess.Popen(
        "ls *.tr | xargs cntraining", # ["cntraining", ' '.join(tr_files)],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = cntraining_proc.communicate()
    print(stdout)
    # with open('training_log_1.txt', 'a+') as f:
    #     f.write('\n\nNormproto ...')
    #     f.write("cntraining <tr_files>")
    #     f.write(str(stdout))

    if stderr:
        print('Error occurred')
        print(stderr)
    # sys.exit()
    '''

    '''
    # 7. Create unicharambigs
    print('Create unicharambigs ...')
    # unicharambigs_file = os.path.join(args.directory, "amh.unicharambigs")
    with open("amh.unicharambigs", "w") as file:
        file.write('v2\n')
    '''

    '''
    # 8. Rename files
    print('Renaming files ...')
    if os.path.isfile('font_properties'):
        os.replace('font_properties', 'amh.font_properties')

    if os.path.isfile('inttemp'):
        os.replace('inttemp', 'amh.inttemp')

    if os.path.isfile('pffmtable'):
        os.replace('pffmtable', 'amh.pffmtable')

    if os.path.isfile('normproto'):
        os.replace('normproto', 'amh.normproto')

    if os.path.isfile('shapetable'):
        os.replace('shapetable', 'amh.shapetable')

    if os.path.isfile('unicharset'):
        os.replace('unicharset', 'amh.unicharset')

    # sys.exit()
    '''

    # 8. Combine data
    print('Combine data ...')
    combine_data_proc = subprocess.Popen(
        "combine_tessdata amh.",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = combine_data_proc.communicate()
    print(stdout)
    # with open('training_log_1.txt', 'a+') as f:
    #     f.write('\n\nCombine data ...')
    #     f.write("combine_tessdata amh.")
    #     f.write(str(stdout))

    if stderr:
        print('Error occurred')
        print(stderr)
    # '''



if __name__ == "__main__":
    # global digits_count
    print(args.directory)
    
    run_trainer()
