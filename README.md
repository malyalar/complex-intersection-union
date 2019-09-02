# Multi-Bounding Box Intersection-over-Union

Python script that calculates intersection over union for multi-bounding-box annotations between workers and valid experts. Works even if the number of boxes between worker and expert annotations is not equal. Also includes scripts to create an input URL .csv from buckets of images stored on Amazon S3 for manual annotation by MTurk Workers.

Also outputs approval rates and other analyses to a csv. Can loop through a csv-format MTurk submitted assignment batch, comparing all submitted assignment results to expert-validated results.

## Comments
The script converts MTurk image annotations from workers to (possibly downscaled) pixel arrays, with each element in the 2d array representing a pixel of the image that is either "marked" (1) or "unmarked" (0). For example, a 3100 * 3100 pixel image may be represented as a 310 * 310 2d array, for example. IOU is then calculated elementwise on these smaller representative arrays. Downscaling allows for large batches of images to be processed rapidly with almost no error from loss of fidelity in the annotation data.

## Outputs
<p float="left">
<img src="https://github.com/malyalar/stone_free/blob/master/intersect_ex.png">
</p>

Intersection-over-union result is 15.99%. Agreement is written to batch_results.csv.
