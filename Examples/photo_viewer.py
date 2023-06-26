"""
########################################################
This PyQt-based module is build to give ability to show an image with options such as zooming in/out, scrolling and moving in zoon-view and ...

Dependencies:
    This module is based on PyQt5 QGraphicsView. So, to use this module in your code you must have PyQt5 library installed.
    - PyQt5
    -opencv
    -numpy

Features:
    - Zoom in/out on image
    - Fit image to window
    - Moving in image in zoom-view by drag and move ability
    - Show grid lines on image
    - Save image

Notice:
    This module is completely PyQt5-based and it's not possible to be used with other non-Qt-based applications at this moment.

Designed and developed by Ali Salehi
########################################################
"""



from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import cv2
import os



class GridLine_Type():
    """This class is used to detemine type of grid line shown on Photo-Viewer object
    """

    none = 'none'
    gridline = 'gridline'
    crosshair = 'crosshair'


class GridLine_Color():
    """This class is used to determine color of grid line shown on Photo-Viewer object
    """

    white = QtCore.Qt.white
    black = QtCore.Qt.black
    red = QtCore.Qt.red
    green = QtCore.Qt.green
    blue = QtCore.Qt.blue



def convert_image_to_pixmap(image: np.array, need_rgb2bgr=False) -> QtGui.QPixmap:
    """This function is used to convert a numpy array image to PyQt pixmap

    :param image: Input image in numpy array format
    :type image: np.array
    :return: PyQt QPixmap image
    :rtype: QtGui.QPixmap
    """

    # convert to rgb if needed
    if len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif need_rgb2bgr:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # convert cv2 image to pyyqt image
    height, width, channels = image.shape
    bytesPerLine = channels * width
    qImg = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    pixmap = QtGui.QPixmap.fromImage(qImg)

    return QtGui.QPixmap(pixmap)




class PhotoViewer(QtWidgets.QGraphicsView):

    def __init__(self, raw_image_path=None, grid_shape=(15,24), grid_color=GridLine_Color.white, need_scrollbar=False):
        """This class is used to build the Photo-Viewer object to show images, with some options like zooming and panning and ...

        :param raw_image_path: If any image path is enetered, the image is set to Photo-Viewer when Photo-Viewer is empty/reset, defaults to None
        :type raw_image_path: _type_, optional
        :param grid_shape: Tuple containing dims of chess grid guide lines, defaults to (15,24)
        :type grid_shape: tuple, optional
        :param need_scrollbar: If set as True, Photo-Viewer scrollbars are shown while zooming on image, defaults to False
        :type need_scrollbar: bool, optional
        """

        super(PhotoViewer, self).__init__()

        #
        self.scene = QtWidgets.QGraphicsScene(self)
        self.photo = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.photo)
        self.setScene(self.scene)

        #
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        if not need_scrollbar:
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        #
        self.base_image = None # main image assigned to Photo-Viewer (without any grid lines)
        self.empty = True # content of Photo-Viewer (determining if photoviewer has image or not)
        try:
            if raw_image_path is None or not os.path.exists(raw_image_path):
                raise Exception
            #
            self.raw_image = cv2.imread(raw_image_path) # raw image
        except:
            self.raw_image = None
        self.image_width = 0 # width of image on Photo-Viewer
        self.image_height = 0 # height of image on Photo-Viewer
        
        # grid line features
        self.grid_shape = grid_shape # shape of grid (x, y), number of horizintal and vertical lines
        self.grid_color = grid_color
        self.crosshair_shape = [2 ,2] # shape of crosshair
        self.grid_type = GridLine_Type.none # type of grid line on image (none, grid or crosshair)
        self.grid_lines = list() # list to store pyqt grid line items added to the scene

        # reset image of Photo-Viewer
        self.clear_image() 
    

    def has_image(self) -> bool:
        """This function is used to determine if Photo-Viewer object contains image or not

        :return: boolean determining if Photo-Viewer object contains image or not
        :rtype: bool
        """

        return not self.empty
    

    def wheelEvent(self, event) -> None:
        """This function is used to enable mouse scroll for zooming in/out

        :param event: _description_
        :type event: _type_
        """
        
        # check if Photo-Viewer object conains image
        if self.has_image():
            # zoom in
            if event.angleDelta().y() > 0:
                self.zoom(zoom_in=True)
            # zoom out
            else:
                self.zoom(zoom_out=True)
    

    def keyPressEvent(self, event) -> None:
        """This function is used to capture keyboard to use + and - keys for zooming in/out

        :param event: _description_
        :type event: _type_
        """
        
        # + key
        if event.key() == QtCore.Qt.Key_Plus: 
            self.zoom(zoom_in=True)
            
        # - key
        elif event.key() == QtCore.Qt.Key_Minus: 
            self.zoom(zoom_out=True)
    

    def fit_in_view(self) -> None:
        """This function is used to fit/stretch image on photoviewer window
        """

        rect = QtCore.QRectF(self.photo.pixmap().rect())

        if not rect.isNull():
            self.setSceneRect(rect)

            if self.has_image():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
                self.scale(factor, factor)


    def zoom(self, zoom_in=False, zoom_out=False) -> None:
        """This function is used to apply zoom in/out on image

        :param zoom_in: boolean determing to apply zoom in, defaults to False
        :type zoom_in: bool, optional
        :param zoom_out: boolean determing to apply zoom out, defaults to False
        :type zoom_out: bool, optional
        """

        if zoom_in and zoom_out:
            return

        rect = QtCore.QRectF(self.photo.pixmap().rect())

        if self.has_image() and not rect.isNull():
            # zoom in
            if zoom_in:
                factor = 1.05
            # zoom out
            elif zoom_out:
                factor = 0.95
            #
            else:
                return
            
            # apply zoom
            self.scale(factor, factor)
            
            # prevent zooming-out after image fit-in-view reached
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            if zoom_out and scenerect.width()<=viewrect.width() and scenerect.height()<=viewrect.height():
                self.fit_in_view()
            
            # update grid lines thickness according to zoom value
            self.update_grid_thickness()
    

    def fit_on_window_resize(self) -> None:
        """This function is used to fit image to window when window is resized. This way image is resized along with to window resize
        """

        rect = QtCore.QRectF(self.photo.pixmap().rect())

        if self.has_image() and not rect.isNull():
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            if scenerect.width()<=viewrect.width() and scenerect.height()<=viewrect.height():
                self.fit_in_view()


    def set_image(self, image:np.array, need_rgb2bgr=False, fitinview=False) -> None:
        """This function is used to set a numpy array image to Photo-Viewer

        :param image: Input image in numpy array format
        :type image: np.array
        :param need_rgb2bgr: Used to replace red and blue channels for RGB images if needed, defaults to False
        :type need_rgb2bgr: bool, optional
        :param fitinview: If set as True, the image will be fitted to window, defaults to False
        :type fitinview: bool, optional
        """
        
        # keep basse image
        self.base_image = image

        # convert image to PyQt pixmap
        try:
            image_pixmap = convert_image_to_pixmap(image=image, need_rgb2bgr=need_rgb2bgr)
        except:
            return

        # set pixmap on Photo-Viewer
        if not image_pixmap.isNull():
            self.empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.photo.setPixmap(image_pixmap)
            if fitinview:
                self.fit_in_view()
            
            # set flag to update grid if image dimentions are changed
            if self.image_width != self.photo.pixmap().width() or self.image_height != self.photo.pixmap().height():
                self.image_width = self.photo.pixmap().width()
                self.image_height = self.photo.pixmap().height()
                self.update_grid()

        else:
            self.clear_image()
    

    def clear_image(self) -> None:
        """This function is used to clear/remove image of the Photo-Viewer
        """

        # set raw image to Photo-Viewer
        if self.raw_image is not None:
            try:
                self.set_image(image=self.raw_image, fitinview=True)
            except:
                self.photo.setPixmap(QtGui.QPixmap())
                self.image_width = 0
                self.image_height = 0

        # clear image
        else:
            self.photo.setPixmap(QtGui.QPixmap())
            self.image_width = 0
            self.image_height = 0
        
        #
        self.empty = True
        self.base_image = None
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag) # remove drag mode
        self.change_grid_type(grid_type=GridLine_Type.none) # remove grid
    

    def save_image(self, save_directory:str) -> bool:
        """This function is used to save image

        :param save_directory: Directory to save image of the Photo-Viewer
        :type save_directory: str
        """

        if not self.empty and self.base_image is not None:            
            try:
                cv2.imwrite(save_directory, self.base_image)
                return True
            
            except:
                return False
    

    def change_grid_type(self, grid_type=GridLine_Type.none) -> None:
        """This function is used to change guidance grid lines of the Photo-Viewer. Chess grid, Crosshair or no grid can be selected.

        :param grid_type: Type of the gridlines, defaults to GridLine_Type.none
        :type grid_type: _type_, optional
        """

        # remove grid if Photo-Viewer is empty
        if self.image_width==0 or self.image_height==0 or not self.has_image():
            # remove grid if exist (selected before)
            if self.grid_type != GridLine_Type.none:
                self.grid_type = GridLine_Type.none
                self.update_grid()
        
        # enable/disable grid, if input grid type is no-grid or same as current grid on Photo-Viewer, it will be disabled,
        # otherwise the input grid type will be aplied
        else:
            self.grid_type = GridLine_Type.none if self.grid_type==grid_type else grid_type
            self.update_grid()
            

    def update_grid(self) -> None:
        """This function is used to update grid when grid type is changed,
        also when image dimensions of Photo-Viewer are changed, to fit the grid to new dimensions
        """
        
        # remove last grid if enabled
        while len(self.scene.items())>1:
            for item in self.grid_lines:
                self.scene.removeItem(item)
            self.grid_lines.clear()
        
        # add new grid
        if self.grid_type != GridLine_Type.none:
            rows, cols = self.grid_shape if self.grid_type==GridLine_Type.gridline else self.crosshair_shape
            dy, dx = self.image_height / rows, self.image_width / cols
            
            # add grid lines to scene
            for x in np.linspace(start=dx, stop=self.image_width-dx, num=cols-1):
                x = int(round(x))
                line_item = QtWidgets.QGraphicsLineItem(x, 0, x, self.image_height)
                self.scene.addItem(line_item)
                self.grid_lines.append(line_item)
            #
            for y in np.linspace(start=dy, stop=self.image_height-dy, num=rows-1):
                y = int(round(y))
                line_item = QtWidgets.QGraphicsLineItem(0, y, self.image_width, y)
                self.scene.addItem(line_item)
                self.grid_lines.append(line_item)
            
            # update grid lines thickness
            self.update_grid_thickness()
            

    def update_grid_thickness(self):
        """This function is used to update grid lines thickness when zoom value on the image is changed,
        this way, when zooming out, grid thickness is increased to be visible.
        Also by zooming in, the grid thickness is reduced to have better accuracy. 
        """

        rect = QtCore.QRectF(self.photo.pixmap().rect())
        viewrect = self.viewport().rect()
        scenerect = self.transform().mapRect(rect)

        # get proper thickness according to value of zoom applied on image
        grid_thick_factor = min(self.image_width, self.image_height)/150
        new_thickness = int(grid_thick_factor * min(viewrect.width()/scenerect.width(), viewrect.height()/scenerect.height()))
        new_thickness = new_thickness if new_thickness > 0 else 1

        # apply new thickness to grid lines (if diifers from current thickness)
        for item in self.grid_lines:
            if item.pen().color()!=self.grid_color or item.pen().width()!=new_thickness:
                item.setPen(QtGui.QPen(self.grid_color, new_thickness))
    

    def change_grid_color(self, grid_color=QtCore.Qt.white):
        """This function is used to change grid-line color

        :param grid_color: _description_, defaults to QtCore.Qt.white
        :type grid_color: _type_, optional
        """

        self.grid_color = grid_color
        self.update_grid()
    

    def change_grid_shape(self, grid_shape=(15,24)):
        """_summary_

        :param grid_shape: _description_, defaults to (15,24)
        :type grid_shape: tuple, optional
        """

        self.grid_shape = grid_shape
        self.update_grid()
    


        

        
        
        

        

    





