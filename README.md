# stone_free
Python scripts to batch publish images, have them be manually annotated by MTurk Workers, then retrieve and analyze assignments.
Included is also a script that calculates intersection over union for multi-bounding-box annotations between workers and valid experts. Works even if the number of boxes between worker and expert annotations is not equal.

Also outputs approval rates for processed images to a csv.

## Comments
The script converts MTurk image annotations from workers to (possibly downscaled) pixel arrays, with each element in the 2d array representing a pixel of the image that is either "marked" (1) or "unmarked" (0). A 3100 * 3100 pixel image may be represented as a 310 * 310 2d array, for example. IOU is then calculated elementwise on these representative arrays. Downscaling allows for large batches of images to be processed rapidly with almost no error from loss of fidelity in the annotation data.

## Outputs


