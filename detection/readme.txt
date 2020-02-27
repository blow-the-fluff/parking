Detection Readme

In order to run batch process
1. Prepare a text file containing the list of file paths of the image (preferrably absolute path)
2. Go to yolo and run "Batch Run.ipynb" to get the coordinates and fields.
3. Go to yolo-inference and run "Form Field Detection.ipynb" to generate the folder containing individual images for detected field entries using the output JSON file
4. Run Tesseract to extract version