import sys
import cv2
from functools import partial
from PyQt5 import QtWidgets, uic, QtCore
import photo_viewer



class PhotoViewer_UI(QtWidgets.QMainWindow):
    """this class is used to build an example ui window for photo-viewer module

    :param QtWidgets: _description_
    """

    def __init__(self, ui_file_path):
        """this function is used to laod ui file and build GUI
        """

        super(PhotoViewer_UI, self).__init__()

        # load ui file
        uic.loadUi(ui_file_path, self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))

        self.window_is_open = False
        self._old_pos = None
        
        # image viewer module
        self.image_viewer = photo_viewer.PhotoViewer(raw_image_path='./icons/no_image.png')
        self.photoviewer_frame.layout().addWidget(self.image_viewer)

        #
        self.button_connector()
    

    def button_connector(self):
        """this function is used to connect ui buttons to their functions
        """

        self.close_header_pushButton.clicked.connect(partial(self.close_win))
        self.load_image_toolbar_pushButton.clicked.connect(partial(self.load_image))
        self.clear_image_toolbar_pushButton.clicked.connect(partial(self.image_viewer.clear_image))
        self.save_image_toolbar_pushButton.clicked.connect(partial(self.save_image))
        self.zoomin_toolbar_pushButton.clicked.connect(partial(lambda: self.image_viewer.zoom(zoom_in=True)))
        self.zoomout_toolbar_pushButton.clicked.connect(partial(lambda: self.image_viewer.zoom(zoom_out=True)))
        self.fitinview_toolbar_pushButton.clicked.connect(partial(self.image_viewer.fit_in_view))
        self.crosshair_toolbar_pushButton.clicked.connect(partial(lambda: self.image_viewer.change_grid_type(grid_type=photo_viewer.GridLine_Type.crosshair)))
        self.gridline_toolbar_pushButton.clicked.connect(partial(lambda: self.image_viewer.change_grid_type(grid_type=photo_viewer.GridLine_Type.gridline)))
        self.gridcolor_toolbar_comboBox.currentIndexChanged.connect(partial(lambda: self.change_grid_color(color=self.gridcolor_toolbar_comboBox.currentText())))
        

    def mousePressEvent(self, event):
        """mouse press event for moving window

        :param event: _description_
        """

        # accept event only on top and side bars and on top bar
        if event.button() == QtCore.Qt.LeftButton and not self.isMaximized() and event.pos().y()<=self.header.height():
            self._old_pos = event.globalPos()


    def mouseReleaseEvent(self, event):
        """mouse release event for stop moving window

        :param event: _description_
        """

        if event.button() == QtCore.Qt.LeftButton:
            self._old_pos = None


    def mouseMoveEvent(self, event):
        """mouse move event for moving window

        :param event: _description_
        """

        if self._old_pos is None:
            return

        delta = QtCore.QPoint(event.globalPos() - self._old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._old_pos = event.globalPos()
    

    def resizeEvent(self, event):
        self.image_viewer.fit_on_window_resize() 
    

    def open_win(self):
        """this function is used to show/open window
        """

        if not self.window_is_open:
            self.show()
            self.window_is_open = True


    def close_win(self):
        """
        this function closes the window
        Inputs: None
        Returns: None
        """

        # close app window and exit the program
        self.window_is_open = False
        self.close()
    

    def show_alert_window(self, title, message, need_confirm=False, level=0):
        """This function is used to create a alert/confirm window

        :param title: _description_
        :type title: _type_
        :param message: _description_
        :type message: _type_
        :param need_confirm: _description_, defaults to False
        :type need_confirm: bool, optional
        :param level: _description_, defaults to 0
        :type level: int, optional
        :return: _description_
        :rtype: _type_
        """

        level = 0 if level<0 or level>2 else level

        # create message box
        alert_window = QtWidgets.QMessageBox()

        # icon
        if level==0:
            alert_window.setIcon(QtWidgets.QMessageBox.Information)
        elif level==1:
            alert_window.setIcon(QtWidgets.QMessageBox.Warning)
        elif level==2:
            alert_window.setIcon(QtWidgets.QMessageBox.Critical)

        # message and title
        alert_window.setText(message)
        alert_window.setWindowTitle(title)

        # buttons
        if not need_confirm:
            alert_window.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert_window.button(QtWidgets.QMessageBox.Ok).setText('OK')
        else:
            alert_window.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
            alert_window.button(QtWidgets.QMessageBox.Ok).setText('Confirm')
            alert_window.button(QtWidgets.QMessageBox.Cancel).setText('Cancel')
        
        alert_window.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        # show
        returnValue = alert_window.exec()

        if not need_confirm:
            return True if returnValue == QtWidgets.QMessageBox.Ok else True
        else:
            return True if returnValue == QtWidgets.QMessageBox.Ok else False
    
    
    def load_image(self):
        """This function is used to load a user selected image from directory
        """

        # open dialog to select image from directory
        options = QtWidgets.QFileDialog.Options()
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select Image to Load', directory='./', filter='Image File(*.jpg *.png *.bmp)', options=options)
        if image_path == '':
            return

        # laod image
        try:
            image = cv2.imread(image_path)
        except:
            self.show_alert_window(title='Error', message='Failed to load image, please ensure right image format.', need_confirm=False, level=2)
        
        # set image on image-viewer
        self.image_viewer.set_image(image=image, need_rgb2bgr=True, fitinview=True)
    

    def save_image(self):
        """_summary_
        """

        if self.image_viewer.has_image():
            # open dialog to select directory to save image
            options = QtWidgets.QFileDialog.Options()
            export_directory, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Choose Directory to Save Image', directory='./', filter="JPEG Image (*.jpg)", options=options)
            if export_directory == '':
                return
            
            # save image
            res = self.image_viewer.save_image(save_directory=export_directory)
            
            if res:
                self.show_alert_window(title='Message', message='Saved image successfully.', need_confirm=False, level=0)
            else:
                self.show_alert_window(title='Error', message='Failed to save image.', need_confirm=False, level=2)
    

    def change_grid_color(self, color):
        """_summary_
        """

        if color == 'White':
            self.image_viewer.change_grid_color(grid_color=photo_viewer.GridLine_Color.white)

        elif color == 'Black':
            self.image_viewer.change_grid_color(grid_color=photo_viewer.GridLine_Color.black)

        elif color == 'Red':
            self.image_viewer.change_grid_color(grid_color=photo_viewer.GridLine_Color.red)

        elif color == 'Green':
            self.image_viewer.change_grid_color(grid_color=photo_viewer.GridLine_Color.green)

        elif color == 'Blue':
            self.image_viewer.change_grid_color(grid_color=photo_viewer.GridLine_Color.blue)
        
        else:
            return




    

    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PhotoViewer_UI(ui_file_path='example_UI.ui')
    window.open_win()
    app.exec_()