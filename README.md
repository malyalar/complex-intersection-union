# Multi-Bounding Box Intersection-over-Union

Python script that calculates intersection over union for axis-aligned multi-bounding-box annotations between workers and valid experts. Works even if the number of boxes between worker and expert annotations is not equal. Also includes scripts to create an input_url.csv from buckets of images stored on Amazon S3 for manual annotation by MTurk Workers.

Also outputs approval rates and other analyses to a csv. Can loop through a csv-format MTurk submitted assignment batch, comparing all submitted assignment results to expert-validated results.

## Comments
The script converts MTurk image annotations from workers to downscaled pixel arrays, with each element in the 2d array representing a pixel of the image that is either "marked" (1) or "unmarked" (0). For example, a 3100 * 3100 pixel image may be represented as a 310 * 310 2d array of T/F values. IOU is then calculated elementwise on these smaller representative arrays. Downscaling allows for large batches of images to be processed rapidly with insignificant error from loss of fidelity in the annotation data. The downscaling factor can be set to 1 for fully accurate calculations, which will still run reasonably quickly even on "large" (e.g. 3100 * 3100px) images.

IoU calculation function, calculate_IOU(), can be easily modified to output F1/Dice coefficient instead.

### Inputs

MTurk bounding-box worker annotations are written into batch_results.csv's as strings, representing an array of variable length (depending on how many boxes are drawn by the Worker):

[{"height":465,"label":"Stone","left":841,"top":570,"width":409}, {"height":637,"label":"Stone","left":1703,"top":1680,"width":382},{"height":944,"label":"Stone","left":1186,"top":1801,"width":1518},
{"height":287,"label":"Stone","left":1620,"top":1386,"width":472}]

"Expert" or ground-truth annotations are expected to be in the same format, under a column in the .csv titled, "expertAnswer" (you have to add this yourself, MTurk will of course not provide these for you). Edit the "expert" section of the parse_dataframe() function to parse different string formats.

### Outputs
<p float="left">
<img src="https://github.com/malyalar/complex-intersection-union/blob/master/intersect_example.png">
</p>

Intersection-over-union result is 15.99%. Agreement is written to batch_results.csv. (The image does not correspond to the input labels given above.)

## Scraping bounding box annotations in image format

RGBannotationscraper.py included to take images with drawings of bounding boxes over them, and determine and output l/t/w/h numeric format annotation of the bounding box. Works only with single bounding boxes.

## Other

Two other scripts are included in this repo: create_csv_imageURLs.py and assess_workers.py. The former script references a selected Amazon S3 bucket of images (or any file, really) and creates a list of URLs for every item in the bucket. This can be fed to MTurk to link Workers to the images. 

The latter script assesses the average accuracy of unique Workers who have completed assignments that can be compared to the experts. Then, it not only approves or rejects individual HITs/annotations based on whether they match up with the expert answer (which only some HITs might have) but will reject all assignments submitted by Workers with averages below a threshold percent accuracy.

A sample batch_results.csv generated from playing around in the MTurk Requester/Worker sandbox is also provided, with the HIT image URLs removed.
