# Photo_Viewer

Photo-Viewer is a PyQt-based module built to give ability to show an image with options such as zooming in/out, scrolling, panning and ...

## Features
    - Zoom in/out on image
    - Fit image to window
    - Moving in image in zoom-view by drag and move ability
    - Show grid lines on image
    - Save image

## Notice
This module is completely PyQt5-based and it's not possible to be used with other non-Qt-based applications at this moment.

## Dependencies
    - PyQt5
    - OpenCV
    - Numpy

## Installation
    1- Install dependencies using pip install
    2- clone Photo-Viewer repository

## Documentation
Sphinx documents are not available at this moment.

## Quick Start
To use the Photo-Viewer module, follow these steps:

1. Import the module: 
``` python
import photo_viewer
```

2. Create a `Photo-Viewer` object inside a PyQt QMainWindow object and assign it to a frame object:
``` python
qmainwindow_obj.image_viewer = photo_viewer.PhotoViewer(raw_image_path=None, grid_shape=(15,24), need_scrollbar=False)
qmainwindow_obj.photoviewer_frame.layout().addWidget(qmainwindow_obj.image_viewer)
```
#### Input parameters:
    - raw_image_path: If any image path is enetered, the image is set to Photo-Viewerr when Photo-Viewer is empty/reset, defaults to None.
    - grid_shape: Tuple containing dims of chess-grid guide lines on image, defaults to (15,24).
    - need_scrollbar: If set as True, scrollbars are shown while zooming on image, defaults to False.

3. Add an Image
``` python
qmainwindow_obj.image_viewer.set_image(image:numpy.array, need_rgb2bgr=True, fitinview=True)
```
#### Input parameters:
    - image: Input image in numpy array format.
    - need_rgb2bgr: Used to replace red and blue channels for RGB images if needed, defaults to False.
    - fitinview: If set as True, the image will be fitted to window, defaults to False.

# Main functions

## Add an image
``` python
qmainwindow_obj.image_viewer.set_image(image:numpy.array, need_rgb2bgr=True, fitinview=True)
```
#### Input parameters:
    - image: Input image in numpy array format.
    - need_rgb2bgr: Used to replace red and blue channels for RGB images if needed, defaults to False.
    - fitinview: If set as True, the image will be fitted to window, defaults to False.


## Check for containing image
``` python
qmainwindow_obj.image_viewer.has_image()
```

## Zooming in/out
Zooming In/Out on Photo-Viewer object is a built-in function and can be applied using mouse scroll wheel.
Also, it can be applied using any PyQt event such as button clicked:

```python
qmainwindow_obj.image_viewer.zoom(zoom_in=False, zoom_out=False)
```
#### Input parameters:
    - zoom_in: Boolean determining to apply zoom in, defaults to False.
    - zoom_out: Boolean determining to apply zoom out, defaults to False

1. Zooming in
```python
qmainwindow_obj.image_viewer.zoom(zoom_in=True)
```

2. Zooming Out
```python
qmainwindow_obj.image_viewer.zoom(zoom_out=True)
```

## Fit/stretch image to Photo-Viewer window
```python
qmainwindow_obj.image_viewer.fit_in_view()
```

## Add/remove grid-lines on image
To better aligning the camera or adjusting FoV, chessboard grid-lines can be used.
2 type of grid-lines are available to use:
    - Chessboard grid-line
    - Crosshair grid-line

```python
qmainwindow_obj.image_viewer.change_grid_type(grid_type=photo_viewer.GridLine_Type.none)
```
#### Input parameters:
    - grid_type: Type of the grid-lines, defaults to photo_viewer.GridLine_Type.none.

1. Add chessboard grid-line
```python
qmainwindow_obj.image_viewer.change_grid_type(grid_type=photo_viewer.GridLine_Type.gridline)
```

2. Add crosshair grid-line
```python
qmainwindow_obj.image_viewer.change_grid_type(grid_type=photo_viewer.GridLine_Type.crosshair)
```

3. Remove grid-line
```python
qmainwindow_obj.image_viewer.change_grid_type(grid_type=photo_viewer.GridLine_Type.none)
```

Also, when a grid-line is enabled using the function, calling the function again will disable it.

## Save Photo-Viewer image
```python
qmainwindow_obj.image_viewer.save_image(save_directory)
```
#### Input parameters:
    - save_directory: Directory to save image of the Photo-Viewer object

## Remove/clear Photo-Viewer image
```python
qmainwindow_obj.image_viewer.clear_image()
```
















