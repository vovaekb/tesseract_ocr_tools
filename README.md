# tesseract_ocr_tools

🔧 This repository provides utilities used for Optical character recognition (OCR). We use library Tesseract OCR.

Stack:

* Python
* numpy
* scikit
* imgaug

There is two scripts:
model_trainer.py - prepare dataset for training language model for Tesseract OCR.

You can find some details on training [here](https://medium.com/@vprivalov/tesseract-ocr-tips-custom-dictionary-to-improve-ocr-d2b9cd17850b).

To run training run command:

```
python model_trainer.py --directory <directory>
```

Here --directory - directory with images
