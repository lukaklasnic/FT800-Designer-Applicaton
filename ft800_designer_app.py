from PyQt6.QtWidgets import ( QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QCheckBox, QColorDialog, QComboBox, QSpinBox,QSplashScreen, QFileDialog, QLineEdit )
from PyQt6.QtCore import ( Qt, QTimer )
from PyQt6.QtGui import (QPixmap, QPainter, QPen, QColor,  QIcon )
from widgets import  ( RectangleWidget, LineWidget, CircleWidget, KeysWidget, ButtonWidget, GaugeWidget, ClockWidget, ProgressBarWidget, ScrollBarWidget, DialWidget, SliderWidget, ToggleWidget, LabelWidget, ImageWidget, Widget_icon, ColorRectangle, EllipseWidget,NumericWidget  )
import sys
from callback import (showButtonProperties, updateButtonSize, showLineProperties,  generateWidgetName, renumberAllWidgets, showCircleProperties, updateCircleSize, showRectangleProperties, showClockProperties, updateClockSize, updateGaugeSize, showGaugeProperties, showDialProperties, updateDialSize, showToggleProperties, updateToggleSize, showLabelProperties, updateLabelSize, showSliderProperties, showScrollBarProperties, showProgressBarProperties, showKeysProperties, update_keys_size, updateImageSize, showImageProperties, showEllipseProperties, updateEllipseSize,showNumericProperties  )
from pathlib import Path
import struct
from PIL import Image


class MainWindow( QMainWindow ):
    def __init__( self ):
        super().__init__()
        self.setDefaultSettings()
        self.setTitleBar()
        self.setScrollArea()
        self.setMainLayouts()
        
    def setTitleBar( self ):
        
        self.setWindowTitle( "FT800 Designer application" )
        self.setWindowIcon( QIcon( "B:\Dokumenti\Fakultet\Merno Informacioni Sistemi i Smart Tehnologije\FT800-Designer-Applicaton\designer_logo_ic" ) )

    def setScrollArea( self ):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable( False )
        self.scroll_area.setHorizontalScrollBarPolicy( Qt.ScrollBarPolicy.ScrollBarAsNeeded )
        self.scroll_area.setVerticalScrollBarPolicy( Qt.ScrollBarPolicy.ScrollBarAsNeeded )
        self.scroll_area.setFrameShape( QScrollArea.Shape.NoFrame )

    def setMainLayouts( self ):
        self.main_widget = QWidget()
        self.main_widget.setMinimumSize( 1919, 1008 )
        self.main_widget.mousePressEvent = self.onMainWidgetClick
        self.main_widget.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

        main_horisontal_layout = QHBoxLayout( self.main_widget )
        main_horisontal_layout.setContentsMargins( 0, 0, 0, 0 )
        main_horisontal_layout.setSpacing( 0 )

        self.properties_widget = QWidget()
        self.properties_widget.setMinimumWidth( 248 )
        self.central_widget = QWidget()
        self.widgets_icon_widget = QWidget()
        self.widgets_icon_widget.setMinimumWidth( 248 )

        self.addWidgetsToPropertiesBar( self.properties_widget )
        self.addWidgetsToCentralLayout( self.central_widget )
        self.addWidgetsToWidgetsIconLayout( self.widgets_icon_widget )

        main_horisontal_layout.addWidget( self.properties_widget, 1 )
        separate_line_1 = QFrame()
        separate_line_1.setFrameShape( QFrame.Shape.VLine )
        separate_line_1.setFrameShadow( QFrame.Shadow.Sunken )
        separate_line_1.setStyleSheet( "background-color: #666666;" )
        separate_line_1.setLineWidth( 2 )
        main_horisontal_layout.addWidget( separate_line_1 )

        main_horisontal_layout.addWidget( self.central_widget, 4 )
        separate_line_2 = QFrame()
        separate_line_2.setFrameShape( QFrame.Shape.VLine )
        separate_line_2.setFrameShadow( QFrame.Shadow.Sunken )
        separate_line_2.setStyleSheet( "background-color: #666666;" )
        separate_line_2.setLineWidth( 2 )
        main_horisontal_layout.addWidget( separate_line_2 )

        main_horisontal_layout.addWidget( self.widgets_icon_widget, 1 )
        self.scroll_area.setWidget( self.main_widget )
        self.setCentralWidget( self.scroll_area )

    def addWidgetsToPropertiesBar( self, properties_widget ):
        self.properties_layout = QVBoxLayout( properties_widget )
        self.properties_layout.setContentsMargins( 10, 10, 10, 10 )
        self.properties_layout.setAlignment( Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft )

    def addWidgetsToCentralLayout( self, central_widget ):
        central_layout = QVBoxLayout( central_widget )
        central_layout.setContentsMargins( 10, 10, 10, 10 )
        central_layout.setAlignment( Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft )

        top_layout = QHBoxLayout()
        top_layout.addStretch( 1 )
        
        generate_button = QPushButton( "Generate" )
        generate_button.setFixedSize( 100, 50 )
        generate_button.setStyleSheet( """QPushButton {background-color: #dea24a;color: black;font-weight: bold;border: 2px solid #dea24a;border-radius: 5px;font-size: 12px;}QPushButton:hover {background-color: darkorange;border: 2px solid darkorange;}QPushButton:pressed {background-color: #cc5500;border: 2px solid #cc5500;}""" )
        generate_button.clicked.connect(self.generate_image_resources)
        
        top_layout.addWidget( generate_button )
        top_layout.addStretch( 1 )
        
        central_layout.addLayout( top_layout )
        central_layout.addStretch( 1 )

        self.canvas_container = QWidget()
        self.canvas_container.setFixedSize( 480, 272 )
        self.canvas_container.setStyleSheet( "background-color: white; border: 1px solid #ccc;" )

        self.canvas = QLabel( self.canvas_container )
        self.canvas.setGeometry( 0, 0, 480, 272 )
        self.canvas.setAlignment( Qt.AlignmentFlag.AlignCenter )

        self.canvas.setMouseTracking( True )
        self.canvas.mousePressEvent = self.onCanvasClick

        self.drawCanvas()

        canvas_outer_container = QWidget()
        canvas_layout = QHBoxLayout( canvas_outer_container )
        canvas_layout.addStretch( 1 )
        canvas_layout.addWidget( self.canvas_container )
        canvas_layout.addStretch( 1 )

        central_layout.addWidget( canvas_outer_container )
        central_layout.addStretch( 1 )

    def addWidgetsToWidgetsIconLayout( self, widgets_icon_widget ):
        widgets_layout = QVBoxLayout( widgets_icon_widget )
        widgets_layout.setContentsMargins( 10, 10, 10, 10 )
        widgets_layout.setAlignment( Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter )

        label = QLabel( "Widgets" )
        label.setStyleSheet( "color: white; font-size: 16px; font-weight: normal;" )
        widgets_layout.addWidget( label )

        icons_container = QWidget()
        icons_layout = QGridLayout( icons_container )
        icons_layout.setSpacing( 20 )
        icons_layout.setAlignment( Qt.AlignmentFlag.AlignTop )

        widgets_shapes = [ "Line","Rectangle",   "Circle", "Ellipse","Button", "Keys","Clock", "Gauge","Dial", "Toggle",  "Scroll bar",  "Slider" ,"Progress bar", "Image","Label",  "Numeric" ]

        row = 0
        col = 0

        for i, shape in enumerate( widgets_shapes ):
            widget_icon = Widget_icon( shape )
            icons_layout.addWidget( widget_icon, row, col )
            col += 1
            if col >= 2:
                col = 0
                row += 1

        widgets_layout.addWidget( icons_container )

    def drawCanvas( self ):
        pixmap = QPixmap( 480, 272 )

        if self.canvas_color == "white":
            pixmap.fill( Qt.GlobalColor.white )
        else:
            color = QColor( self.canvas_color )
            pixmap.fill( color )

        if self.canvas_grid_enable:
            painter = QPainter( pixmap )
            grid_color = QColor( self.grid_color )
            painter.setPen( QPen( grid_color, 1 ) )
            if self.grid_type == "lines":
                for x in range( 0, 481, self.grid_size ):
                    painter.drawLine( x, 0, x, 272 )
                for y in range( 0, 273, self.grid_size ):
                    painter.drawLine( 0, y, 480, y )

            elif self.grid_type == "dots":
                dot_size = 2
                for x in range( self.grid_size // 2, 481, self.grid_size ):
                    for y in range( self.grid_size // 2, 273, self.grid_size ):
                        painter.drawEllipse( x - dot_size // 2, y - dot_size // 2, dot_size, dot_size )
            painter.end()
        
        if hasattr( self, 'canvas' ):
            self.canvas.setPixmap( pixmap )

    def setDefaultSettings( self ):
        self.canvas_grid_enable = False
        self.canvas_color = "white"
        self.grid_color = "black"
        self.grid_size = 20
        self.grid_type = "lines"

        self.canvas = None
        self.properties_widget = None
        self.canvas_properties_visible = False

        self.object_attached = False
        self.selected_shape = None
        self.current_shape = None
        self.shape_properties_visible = False
        self.all_shapes = []
        
    def onCanvasClick( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.current_shape:
                self.showCanvasProperties()
        QLabel.mousePressEvent( self.canvas, event )

    def onMainWidgetClick( self, event ):
        if not hasattr( self, 'canvas_container' ):
            QWidget.mousePressEvent( self.main_widget, event )
            return
        
        conteiner_global = self.canvas_container.frameGeometry()
        conteiner_global.moveTopLeft( self.canvas_container.mapToGlobal( self.canvas_container.rect().topLeft() ) )

        properties_global = self.properties_widget.frameGeometry()
        properties_global.moveTopLeft( self.properties_widget.mapToGlobal( self.properties_widget.rect().topLeft() ) )

        global_pos = event.globalPosition().toPoint()

        if conteiner_global.contains( global_pos ):
            clicked_on_shape = False
            for shape in self.all_shapes:
                global_shape = shape.frameGeometry()
                global_shape.moveTopLeft( shape.mapToGlobal( shape.rect().topLeft() ) )
                if global_shape.contains( global_pos ):
                    clicked_on_shape = True
                    break
            if clicked_on_shape:
                pass
            elif self.selected_shape in [ "Rectangle", "Line", "Circle", "Button", "Gauge", "Clock", "Progress bar", "Scroll bar", "Dial", "Slider", "Toggle", "Label", "Image", "Keys", "Ellipse", "Numeric" ] and self.object_attached:
                self.addShapeToCanvas( global_pos )
            else:
                self.deselectAllShapes()
                self.hideShapeProperties()
        if ( not conteiner_global.contains( global_pos ) and not properties_global.contains( global_pos ) ):
            self.hideCanvasProperties()
            self.deselectAllShapes()
            self.hideShapeProperties()

        QWidget.mousePressEvent( self.main_widget, event )

    def hideCanvasProperties( self ):
        if not self.canvas_properties_visible:
            return
            
        for i in reversed(range(self.properties_layout.count() ) ):
            widget = self.properties_layout.itemAt( i ).widget()
            if widget:
                widget.hide()
                self.properties_layout.removeWidget( widget )
                widget.deleteLater()
        
        self.canvas_properties_visible = False

    def showCanvasProperties( self ):
        if self.canvas_properties_visible or self.current_shape:
            return
        
        properties_name = QLabel( "Main screen properties" )
        properties_name.setStyleSheet( "color: white; font-size: 14px; font-weight: bold; margin-top: 10px;" )
        self.properties_layout.insertWidget( 1, properties_name )

        background_color_properties_layout = QHBoxLayout()
        background_color_properties_layout.setContentsMargins( 20, 5, 10, 5 )
        
        background_color_label = QLabel( "Background color" )
        background_color_label.setStyleSheet( "color: white; font-size: 14px" )
        background_color_properties_layout.addWidget( background_color_label )
        background_color_properties_layout.addStretch( 1 )

        self.canvas_color_rect = ColorRectangle( self.canvas_color )
        self.canvas_color_rect.mousePressEvent = lambda e: self.changeCanvasColor()
        background_color_properties_layout.addWidget( self.canvas_color_rect )

        background_color_widget = QWidget()
        background_color_widget.setLayout( background_color_properties_layout )
        self.properties_layout.insertWidget( 2, background_color_widget )

        grid_main_label = QLabel( "Grid" )
        grid_main_label.setStyleSheet( "color: white; font-size: 14px; font-weight: bold; margin-top: 10px;" )
        self.properties_layout.insertWidget( 3, grid_main_label )
        
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setContentsMargins( 20, 5, 10, 5 )
        
        checkbox_enable_label = QLabel( "Enable grid" )
        checkbox_enable_label.setStyleSheet( "color: white; font-size: 14px;" )
        checkbox_layout.addWidget( checkbox_enable_label )
        
        checkbox_layout.addStretch( 1 )
        
        self.grid_checkbox = QCheckBox()
        self.grid_checkbox.stateChanged.connect( self.toggleGrid )
        self.grid_checkbox.setStyleSheet( "QCheckBox::indicator { width: 15px; height: 15px; }" )
        checkbox_layout.addWidget( self.grid_checkbox )
        
        checkbox_widget = QWidget()
        checkbox_widget.setLayout( checkbox_layout )
        self.properties_layout.insertWidget( 4, checkbox_widget )
        
        grid_color_layout = QHBoxLayout()
        grid_color_layout.setContentsMargins( 20, 5, 10, 5 )

        grid_color_label = QLabel( "Grid color" )
        grid_color_label.setStyleSheet("color: white; font-size: 14px;")
        grid_color_layout.addWidget(grid_color_label)
        grid_color_layout.addStretch( 1 )

        self.grid_color_rect = ColorRectangle( self.grid_color ) 
        self.grid_color_rect.mousePressEvent = lambda e: self.changeGridColor()
        grid_color_layout.addWidget( self.grid_color_rect )

        grid_color_widget = QWidget()
        grid_color_widget.setLayout( grid_color_layout )
        self.properties_layout.insertWidget( 5, grid_color_widget )

        grid_type_layout = QHBoxLayout()
        grid_type_layout.setContentsMargins( 20, 5, 10, 5 )

        grid_type_label = QLabel( "Grid type:" )
        grid_type_label.setStyleSheet( "color: white; font-size: 14px" )
        grid_type_layout.addWidget( grid_type_label )

        grid_type_layout.addStretch( 1 )

        self.grid_type_combobox = QComboBox()
        self.grid_type_combobox.addItems( [ "Lines", "Dots" ] )
        self.grid_type_combobox.setCurrentText( "Lines" if self.grid_type == "lines" else "Dots" )
        self.grid_type_combobox.currentTextChanged.connect( self.changeGridType )
        self.grid_type_combobox.setStyleSheet( "color: white; background-color: #383838;" )
        self.grid_type_combobox.setFixedWidth( 50 )
        grid_type_layout.addWidget( self.grid_type_combobox )

        grid_type_widget = QWidget()
        grid_type_widget.setLayout( grid_type_layout )
        self.properties_layout.insertWidget( 6, grid_type_widget )

        grid_size_layout = QHBoxLayout()
        grid_size_layout.setContentsMargins( 20, 5, 10, 5 )

        grid_size_label = QLabel( "Grid size" )
        grid_size_label.setStyleSheet( "color: white; font-size: 14px" )
        grid_size_layout.addWidget( grid_size_label )

        grid_size_layout.addStretch(1)

        self.grid_size_spinbox = QSpinBox()
        self.grid_size_spinbox.setRange( 5, 100 )
        self.grid_size_spinbox.setValue( self.grid_size )
        self.grid_size_spinbox.valueChanged.connect( self.changeGridSize )
        self.grid_size_spinbox.setStyleSheet( "color: white; background-color: 383838;" )
        self.grid_size_spinbox.setFixedWidth( 50 )
        grid_size_layout.addWidget( self.grid_size_spinbox )

        grid_size_widget = QWidget()
        grid_size_widget.setLayout( grid_size_layout )
        self.properties_layout.insertWidget( 7, grid_size_widget )

        self.canvas_properties_visible = True

    def changeCanvasColor(self, event=None):
        color = QColorDialog.getColor( QColor( self.canvas_color ) )
        if color.isValid():
            self.canvas_color = color.name()
            self.canvas_color_rect.color = self.canvas_color 
            self.drawCanvas()

    def changeGridColor(self, event=None):
        color = QColorDialog.getColor( QColor( self.grid_color ) )
        if color.isValid():
            self.grid_color = color.name()
            self.grid_color_rect.color = self.grid_color
            if self.canvas_grid_enable:
                self.drawCanvas()

    def toggleGrid( self, state ):
        self.canvas_grid_enable = ( state == Qt.CheckState.Checked.value )
        self.drawCanvas()

    def changeGridType( self, text ):
        self.grid_type = "lines" if text == "Lines" else "dots"
        if self.canvas_grid_enable:
            self.drawCanvas()

    def changeGridSize( self, value ):
        self.grid_size = value
        if self.canvas_grid_enable:
            self.drawCanvas()

    def deselectAllShapes( self ):
        for shape in self.all_shapes:
            if shape:
                shape.set_selected( False )
        self.current_shape = None

    def keyPressEvent( self, event ):

        if event.key() == Qt.Key.Key_Delete and self.current_shape:
            self.deleteSelectedShape()
        else:
            super().keyPressEvent( event )
    
    def deleteSelectedShape(self):
        if self.current_shape:
            was_button = isinstance(self.current_shape, ButtonWidget)
            was_line = isinstance(self.current_shape, LineWidget)
            was_clock = isinstance(self.current_shape, ClockWidget)
            was_gauge = isinstance(self.current_shape, GaugeWidget)  # DODAJ OVO

            if self.current_shape in self.all_shapes:
                self.all_shapes.remove(self.current_shape)

            # Ukloni iz odgovarajućeg rečnika
            if was_button and hasattr(self, 'all_button_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_button_dicts.pop(self.current_shape.custom_name, None)
            elif was_line and hasattr(self, 'all_line_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_line_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, CircleWidget) and hasattr(self, 'all_circle_dicts'):
                 if hasattr(self.current_shape, 'custom_name'):
                     self.all_circle_dicts.pop(self.current_shape.custom_name, None)
            elif was_clock and hasattr(self, 'all_clock_dicts'):  # DODAJ OVO
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_clock_dicts.pop(self.current_shape.custom_name, None)
            elif was_gauge and hasattr(self, 'all_gauge_dicts'):  # DODAJ OVO
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_gauge_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, DialWidget) and hasattr(self, 'all_dial_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_dial_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, ToggleWidget) and hasattr(self, 'all_toggle_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_toggle_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, LabelWidget) and hasattr(self, 'all_label_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_label_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, ScrollBarWidget) and hasattr(self, 'all_scrollbar_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_scrollbar_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, ProgressBarWidget) and hasattr(self, 'all_progressbar_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_progressbar_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, LineWidget) and hasattr(self, 'all_line_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_line_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, ImageWidget) and hasattr(self, 'all_image_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_image_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, EllipseWidget) and hasattr(self, 'all_ellipse_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_ellipse_dicts.pop(self.current_shape.custom_name, None)
            elif isinstance(self.current_shape, NumericWidget) and hasattr(self, 'all_numeric_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_numeric_dicts.pop(self.current_shape.custom_name, None)

            self.current_shape.deleteLater()
            self.current_shape = None

            self.hideShapeProperties()
            self.deselectAllShapes()
            self.renumberStackOrders()

            renumberAllWidgets( self )

    def renumberStackOrders(self):
        """Renumeriše stack_order vrednosti nakon brisanja widget-a"""
        if not self.all_shapes:
            return

        sorted_widgets = sorted(self.all_shapes, key=lambda x: x.stack_order)
        for i, widget in enumerate(sorted_widgets, 1):
            widget.stack_order = i

        self.sortWidgetsByStackOrder()


    def hideShapeProperties( self ):

        if not self.shape_properties_visible:
            return
        
        for i in reversed( range( self.properties_layout.count() ) ):

            widget = self.properties_layout.itemAt( i ).widget()

            if widget:

                widget.hide()
                self.properties_layout.removeWidget( widget )
                widget.deleteLater()

        self.shape_properties_visible = False

    def selectShape(self, shape):
        self.deselectAllShapes()
        shape.set_selected(True)
        self.current_shape = shape

        self.main_widget.setFocus()
        self.hideCanvasProperties()
        self.showShapeProperties()

    def addShapeToCanvas( self, global_pos ):
        container_pos = self.canvas_container.mapFromGlobal( global_pos )
        shape = None

        if self.selected_shape == "Rectangle":
            shape = RectangleWidget(100, 80, self.canvas_container)
            shape.move(container_pos.x() - 50, container_pos.y() - 40)
            shape.clicked.connect(self.selectShape)

            # Dodajte ove linije:
            shape.custom_name = generateWidgetName(self, "Rectangle")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za rectangle-ove
            if not hasattr(self, 'all_rectangle_dicts'):
                self.all_rectangle_dicts = {}
            self.all_rectangle_dicts[shape.custom_name] = shape.get_properties_dict()

        # U deleteSelectedShape metodi dodajte:
        elif isinstance(self.current_shape, RectangleWidget) and hasattr(self, 'all_rectangle_dicts'):
            if hasattr(self.current_shape, 'custom_name'):
                self.all_rectangle_dicts.pop(self.current_shape.custom_name, None)

        elif self.selected_shape == "Line":
            shape = LineWidget(self.canvas_container)

            # Postavi početne tačke linije
            start_x = container_pos.x() 
            start_y = container_pos.y()
            end_x = container_pos.x() +100
            end_y = container_pos.y()

            shape.set_line_points(start_x, start_y, end_x, end_y)
            shape.clicked.connect(self.selectShape)

            # Generiši ime
            shape.custom_name = generateWidgetName(self, "Line")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za linije
            if not hasattr(self, 'all_line_dicts'):
                self.all_line_dicts = {}
            self.all_line_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Circle":
            shape = CircleWidget(100, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Dodajte ove linije:
            shape.custom_name = generateWidgetName(self, "Circle")
            shape.stack_order = len(self.all_shapes) + 1
            shape.update_center_position()

            # Inicijalizuj rečnik za circle-ove
            if not hasattr(self, 'all_circle_dicts'):
                self.all_circle_dicts = {}
            self.all_circle_dicts[shape.custom_name] = shape.get_properties_dict()
        elif self.selected_shape == "Ellipse":
            shape = EllipseWidget(98, 78, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Generiši ime
            shape.custom_name = generateWidgetName(self, "Ellipse")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za ellipse-ove
            if not hasattr(self, 'all_ellipse_dicts'):
                self.all_ellipse_dicts = {}
            self.all_ellipse_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Numeric":
            shape = NumericWidget(100, 40, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Generiši ime
            shape.custom_name = generateWidgetName(self, "Numeric")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za numeric widgete
            if not hasattr(self, 'all_numeric_dicts'):
                self.all_numeric_dicts = {}
            self.all_numeric_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Button":

            shape = ButtonWidget( 100, 50, self.canvas_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.custom_name = generateWidgetName(self, "Button")
            shape.clicked.connect( self.selectShape )
            shape.setMouseTracking( True )
            shape.raise_()
            shape.stack_order = len( self.all_shapes ) + 1
            shape.update_properties_dict()  
            if not hasattr( self, 'all_button_dicts' ):
                self.all_button_dicts = {}
            self.all_button_dicts[ shape.custom_name ] = shape.get_properties_dict()

        elif self.selected_shape == "Gauge":
            shape = GaugeWidget(80, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "Gauge")
            shape.stack_order = len(self.all_shapes) + 1

            # Ažuriraj properties dict
            shape.update_properties_dict()

            # Inicijalizuj rečnik za gauge-ove ako ne postoji
            if not hasattr(self, 'all_gauge_dicts'):
                self.all_gauge_dicts = {}
            self.all_gauge_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Clock":

            shape = ClockWidget( 100, self.canvas_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "Clock")
            shape.stack_order = len(self.all_shapes) + 1

            # Ažuriraj properties dict
            shape.update_properties_dict()

            # Inicijalizuj rečnik za clock-ove ako ne postoji
            if not hasattr(self, 'all_clock_dicts'):
                self.all_clock_dicts = {}
            self.all_clock_dicts[shape.custom_name] = shape.get_properties_dict()
        elif self.selected_shape == "Progress bar":
            shape = ProgressBarWidget(150, 10, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "ProgressBar")
            shape.stack_order = len(self.all_shapes) + 1

            # Ažuriraj properties dict
            shape.update_properties_dict()

            # Inicijalizuj rečnik za progress bar-ove ako ne postoji
            if not hasattr(self, 'all_progressbar_dicts'):
                self.all_progressbar_dicts = {}
            self.all_progressbar_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Scroll bar":
            shape = ScrollBarWidget(150, 10, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "ScrollBar")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za scrollbar-e ako ne postoji
            if not hasattr(self, 'all_scrollbar_dicts'):
                self.all_scrollbar_dicts = {}
            self.all_scrollbar_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Dial":
            shape = DialWidget(80, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "Dial")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za dial-ove ako ne postoji
            if not hasattr(self, 'all_dial_dicts'):
                self.all_dial_dicts = {}
            self.all_dial_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Slider":
            shape = SliderWidget(200, 50, self.canvas_container)  # Povećana visina za bolji prikaz
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "Slider")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za slider-e ako ne postoji
            if not hasattr(self, 'all_slider_dicts'):
                self.all_slider_dicts = {}
            self.all_slider_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Toggle":
            shape = ToggleWidget(80, 30, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "Toggle")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za toggle-ove ako ne postoji
            if not hasattr(self, 'all_toggle_dicts'):
                self.all_toggle_dicts = {}
            self.all_toggle_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Label":
            shape = LabelWidget(100, 40, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Koristi generateWidgetName za generisanje imena
            shape.custom_name = generateWidgetName(self, "Label")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za label-e ako ne postoji
            if not hasattr(self, 'all_label_dicts'):
                self.all_label_dicts = {}
            self.all_label_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Image":
            shape = ImageWidget(100, 100, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)

            # Generiši ime
            shape.custom_name = generateWidgetName(self, "Image")
            shape.stack_order = len(self.all_shapes) + 1

            # Inicijalizuj rečnik za image-ove
            if not hasattr(self, 'all_image_dicts'):
                self.all_image_dicts = {}
            self.all_image_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Keys":
            shape = KeysWidget(200, 120, self.canvas_container)
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.selectShape)
            
            # Generiši ime
            shape.custom_name = generateWidgetName(self, "Keys")
            shape.stack_order = len(self.all_shapes) + 1
            
            # Inicijalizuj rečnik za keys
            if not hasattr(self, 'all_keys_dicts'):
                self.all_keys_dicts = {}
            self.all_keys_dicts[shape.custom_name] = shape.get_properties_dict()
            
            shape.show()
            self.all_shapes.append(shape)
            self.updateWidgetsZOrder()
            self.selectShape(shape)
            QApplication.restoreOverrideCursor()
            self.object_attached = False
            self.selected_shape = None
            return

        if shape:
            shape.custom_name = generateWidgetName(self, "Rectangle")
        
            # DODAJ OVO: Inicijalni stack_order
            if self.all_shapes:
                max_stack_order = max([s.stack_order for s in self.all_shapes])
                shape.stack_order = max_stack_order + 1
            else:
                shape.stack_order = 1

            shape.show()
            self.all_shapes.append( shape )
            self.sortWidgetsByStackOrder()
            self.selectShape( shape )
            QApplication.restoreOverrideCursor()
            self.object_attached = False
            self.selected_shape = None

    def updateWidgetsZOrder(self):
        """Sortira widget-e po stack_order i postavlja odgovarajući Z-order"""
        # Sortiraj widget-e po stack_order (manji broj = niže)
        sorted_widgets = sorted(self.all_shapes, key=lambda x: x.stack_order)

        # Postavi Z-order za svaki widget
        for i, widget in enumerate(sorted_widgets):
            widget.lower()  # Prvo sve spustimo na dno

        # Sada podignemo svaki widget redom (veći stack_order = više)
        for widget in sorted_widgets:
            widget.raise_()


    def showShapeProperties(self):
        self.hideShapeProperties()
        self.hideCanvasProperties()
        
        stack_order_attrs = [
        'stack_order_spin_rect', 'stack_order_spin_circle', 'stack_order_spin_button',
        'stack_order_spin_line', 'stack_order_spin_ellipse', 'stack_order_spin_numeric',
        'stack_order_spin_gauge', 'stack_order_spin_clock', 'stack_order_spin_progressbar',
        'stack_order_spin_scrollbar', 'stack_order_spin_dial', 'stack_order_spin_slider',
        'stack_order_spin_toggle', 'stack_order_spin_label', 'stack_order_spin_image',
        'stack_order_spin_keys'
    ]
    
        for attr in stack_order_attrs:
            if hasattr(self, attr):
                delattr(self, attr)

        if not self.current_shape:
            return

        current_index = 0 

        if isinstance(self.current_shape, RectangleWidget):
            shape_label = QLabel("Rectangle Properties")
        elif isinstance(self.current_shape, LineWidget):
            shape_label = QLabel("Line Properties")
        elif isinstance(self.current_shape, CircleWidget):
            shape_label = QLabel("Circle Properties")
        elif isinstance(self.current_shape, ButtonWidget):
            shape_label = QLabel("Button Properties")
        elif isinstance(self.current_shape, GaugeWidget):
            shape_label = QLabel("Gauge Properties") 
        elif isinstance(self.current_shape, ProgressBarWidget):
            shape_label = QLabel("Progress bar Properties")
        elif isinstance(self.current_shape, ScrollBarWidget):
            shape_label = QLabel("Scroll bar Properties")
        elif isinstance(self.current_shape, DialWidget):
            shape_label = QLabel("Dial Properties")
        elif isinstance(self.current_shape, SliderWidget):
            shape_label = QLabel("Slider Properties")
        elif isinstance(self.current_shape, ToggleWidget):
            shape_label = QLabel("Toggle Properties")
        elif isinstance(self.current_shape, LabelWidget):
            shape_label = QLabel("Label Properties")
        elif isinstance(self.current_shape, ImageWidget):
            shape_label = QLabel("Image Properties")
        elif isinstance(self.current_shape, KeysWidget):
            shape_label = QLabel("Keyboard Properties")
        elif isinstance(self.current_shape, ClockWidget):
            shape_label = QLabel("Clock Properties")
        elif isinstance(self.current_shape, EllipseWidget):
            shape_label = QLabel("Ellipse Properties")
        elif isinstance(self.current_shape, NumericWidget):
            shape_label = QLabel("Numeric Widget Properties")

        shape_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
        self.properties_layout.insertWidget(current_index, shape_label)
        current_index += 1

        # Za sve widget-e koristi njihove specifične metode
        if isinstance(self.current_shape, CircleWidget):
            current_index = showCircleProperties(self, current_index)
        elif isinstance(self.current_shape, RectangleWidget):
            current_index = showRectangleProperties(self, current_index)
        elif isinstance(self.current_shape, LineWidget):
            current_index = showLineProperties(self, current_index)
        elif isinstance(self.current_shape, ButtonWidget):
            current_index = showButtonProperties(self, current_index)
        elif isinstance(self.current_shape, GaugeWidget):
            current_index = showGaugeProperties(self, current_index)
        elif isinstance(self.current_shape, ProgressBarWidget):
            current_index = showProgressBarProperties(self, current_index)
        elif isinstance(self.current_shape, ScrollBarWidget):
            current_index = showScrollBarProperties(self, current_index)  # Koristi novu funkciju
        elif isinstance(self.current_shape, DialWidget):
            current_index = showDialProperties(self, current_index)
        elif isinstance(self.current_shape, SliderWidget):
            current_index = showSliderProperties(self, current_index)  # Koristi novu funkciju
        elif isinstance(self.current_shape, ToggleWidget):
            current_index = showToggleProperties(self, current_index)  # OVO JE PROMENJENO
        elif isinstance(self.current_shape, LabelWidget):
            current_index = showLabelProperties(self, current_index)
        elif isinstance(self.current_shape, ImageWidget):
            current_index = showImageProperties(self, current_index)
        elif isinstance(self.current_shape, KeysWidget):
            current_index = showKeysProperties(self, current_index)
        elif isinstance(self.current_shape, ClockWidget):
            current_index = showClockProperties(self, current_index)
        elif isinstance(self.current_shape, EllipseWidget):
            current_index = showEllipseProperties(self, current_index)  
        elif isinstance(self.current_shape, NumericWidget):
            current_index = showNumericProperties(self, current_index)

        self.shape_properties_visible = True


    def updateStackOrder(self, value):
        """Ažurira stack_order selektovanog widget-a i sortira widget-e"""
        if self.current_shape:
            self.current_shape.stack_order = value
            self.sortWidgetsByStackOrder()

    def sortWidgetsByStackOrder(self):
        """Sortira widget-e po stack_order i ažurira njihov z-order - JEDINA IMPLEMENTACIJA"""
        if not self.all_shapes:
            return

        # Sortiraj widget-e po stack_order (manji broj = niže, veći = više)
        sorted_widgets = sorted(self.all_shapes, key=lambda x: x.stack_order, reverse=True)

        # Debug ispis
        print(f"\n[MainWindow] Sortiranje widget-a po stack_order:")
        for i, widget in enumerate(sorted_widgets):
            widget_name = widget.custom_name if hasattr(widget, 'custom_name') else 'Unknown'
            print(f"  {i+1}. {widget_name}: stack_order={widget.stack_order}")

        # Postavi Z-order: prvo sve spusti na dno
        for widget in self.all_shapes:
            widget.lower()

        # Sada podigni widget-e redom (veći stack_order = više)
        # Obilazimo obrnutim redosledom jer lower()/raise() radi na steku
        for widget in reversed(sorted_widgets):
            widget.raise_()

        # Osiguraj da je selektovani widget na vrhu (za interakciju)
        if self.current_shape:
            self.current_shape.raise_()

    def updateShapePosition( self ):
        if self.current_shape:
            self.current_shape.move( self.pos_x_spin.value(), self.pos_y_spin.value() )


    def changeShapeColor( self ):
        if ( self.current_shape and not isinstance( self.current_shape, ( GaugeWidget, ClockWidget, ProgressBarWidget ) ) ):
            if hasattr( self.current_shape, 'color' ):
                current_color = self.current_shape.color
            elif hasattr( self.current_shape, 'line_color' ):
                current_color = self.current_shape.line_color
            else:
                return

            color = QColorDialog.getColor( current_color )
            if color.isValid():
                self.current_shape.set_color( color )
                self.color_rect.setStyleSheet( f"background-color: {color.name()}; border: 1px solid #ccc;" )

    def updateShapeBorderWidth( self ):
        if ( self.current_shape and not isinstance( self.current_shape, ( GaugeWidget, ClockWidget, ProgressBarWidget ) ) and hasattr( self.current_shape, 'set_border_width' ) ):
            self.current_shape.set_border_width( self.border_width_spin.value() )



    def generate_image_resources(self):
        """Generiše resource.h i resource.c fajlove sa hex nizovima slika (RAW format)"""
        
        # Prikupi sve image widget-e
        image_widgets = []
        for shape in self.all_shapes:
            if isinstance(shape, ImageWidget):
                # Proveri da li widget ima putanju do slike
                if hasattr(shape, 'image_path') and shape.image_path:
                    if Path(shape.image_path).exists():
                        image_widgets.append(shape)
                        print(f"Pronađen image widget: {shape.custom_name} - {shape.image_path}")
                    else:
                        print(f"Fajl ne postoji: {shape.image_path}")
                else:
                    print(f"Image widget '{shape.custom_name}' nema putanju do slike!")
        
        if not image_widgets:
            print("Nema image widget-a sa slikama na canvas-u!")
            return
        
        print(f"Pronađeno {len(image_widgets)} image widget-a sa slikama")
        
        # Postavi putanje za fajlove
        resource_h_path = "resource.h"
        resource_c_path = "resource.c"
        
        # Generisi header fajl
        self._generate_resource_header(resource_h_path, image_widgets)
        
        # Generisi source fajl
        self._generate_resource_source(resource_c_path, image_widgets)
        
        print(f"Generisani fajlovi: {resource_h_path} i {resource_c_path}")
    
    def _generate_resource_header(self, filepath, image_widgets):
        """Generiše resource.h fajl sa deklaracijama nizova"""
        
        header_content = """#ifndef NECTO_DESIGNER_RESURS_H
    #define NECTO_DESIGNER_RESURS_H
    
    #include <stdint.h>
    
    """
        
        # Dodaj deklaracije za svaki image
        for widget in image_widgets:
            width = widget.get_width()
            height = widget.get_height()
            
            # Koristi custom_name, ili generiši ime ako nije postavljeno
            if widget.custom_name and widget.custom_name.strip():
                # Očisti ime
                name = widget.custom_name.replace(" ", "_").replace("-", "_")
                # Ukloni sve ne-alfanumeričke karaktere osim podvlake
                name = ''.join(c for c in name if c.isalnum() or c == '_')
                if not name[0].isalpha():
                    name = "Image_" + name
            else:
                name = f"Image_{image_widgets.index(widget)}"
            
            # Generiši ime niza: ime_widthxheight
            array_name = f"{name}_{width}x{height}"
            header_content += f"extern const uint8_t {array_name}[];\n"
        
        header_content += """
    #endif
    """
        
        # Snimi fajl
        with open(filepath, 'w') as f:
            f.write(header_content)
        
        print(f"Generisan header fajl sa {len(image_widgets)} deklaracija")
    
    def _read_image_data(self, image_widget):
        """Čita raw podatke slike i vraća ih kao listu bajtova"""
        
        image_path = image_widget.image_path
        
        try:
            # Pročitaj ceo binarni fajl
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            file_size = len(image_bytes)
            print(f"Pročitano {file_size} bajtova iz {Path(image_path).name}")
            
            # Vrati kao listu bajtova
            return list(image_bytes)
            
        except FileNotFoundError:
            print(f"Fajl nije pronađen: {image_path}")
            return None
        except Exception as e:
            print(f"Greška pri čitanju slike {image_path}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_resource_source(self, filepath, image_widgets):
        """Generiše resource.c fajl sa RAW hex nizovima slika"""
        
        source_content = """#include <stdint.h>
    #include "resource.h"
    
    """
        
        successful_images = 0
        
        # Dodaj nizove za svaki image
        for widget in image_widgets:
            width = widget.get_width()
            height = widget.get_height()
            
            # Koristi custom_name, ili generiši ime ako nije postavljeno
            if widget.custom_name and widget.custom_name.strip():
                name = widget.custom_name.replace(" ", "_").replace("-", "_")
                name = ''.join(c for c in name if c.isalnum() or c == '_')
                if not name[0].isalpha():
                    name = "Image_" + name
            else:
                name = f"Image_{image_widgets.index(widget)}"
            
            array_name = f"{name}_{width}x{height}"
            
            # Pročitaj podatke slike
            print(f"\nGenerišem podatke za: {array_name}")
            image_data = self._read_image_data(widget)
            
            if image_data:
                successful_images += 1
                
                # Dodaj komentar sa informacijama o slici
                filename = Path(widget.image_path).name
                file_size = len(image_data)
                source_content += f"/* {array_name} */\n"
                source_content += f"/* Originalna slika: {filename} */\n"
                source_content += f"/* Prikazane dimenzije: {width}x{height} */\n"
                source_content += f"/* Veličina podataka: {file_size} bajtova */\n\n"
                
                # Dodaj deklaraciju niza
                source_content += f"const uint8_t {array_name}[{file_size}] = {{\n"
                
                # Formatiraj hex vrednosti - 16 bajtova po liniji
                bytes_per_line = 16
                total_bytes = len(image_data)
                
                for i in range(0, total_bytes, bytes_per_line):
                    line_bytes = image_data[i:min(i + bytes_per_line, total_bytes)]
                    hex_values = [f"0x{b:02x}" for b in line_bytes]
                    
                    # Dodaj liniju
                    source_content += "    " + ", ".join(hex_values)
                    
                    # Dodaj zarez ako nije poslednja linija
                    if i + bytes_per_line < total_bytes:
                        source_content += ",\n"
                
                source_content += "\n};\n\n"
                
                print(f"  Uspešno generisano: {file_size} bajtova")
            else:
                print(f"  GREŠKA: Nije moguće generisati podatke za {widget.custom_name}")
        
        # Dodaj footer komentar
        if successful_images > 0:
            source_content += f"/*\n"
            source_content += f" * Ukupno {successful_images} slika generisano\n"
            source_content += f" * Podaci su RAW format (originalni BMP/PNG fajlovi)\n"
            source_content += f" * Za korišćenje sa FT800, koristite CMD_LOADIMAGE\n"
            source_content += f" */\n"
        else:
            source_content += f"/* Nema generisanih slika */\n"
        
        # Snimi fajl
        with open(filepath, 'w') as f:
            f.write(source_content)
        
        print(f"\nGenerisan source fajl sa {successful_images} nizova")

    def _convert_to_argb1555(self, pixels):
        """Konvertuje listu RGBA piksela u ARGB1555 format"""
        argb1555_data = []

        for pixel in pixels:
            r, g, b, a = pixel

            # Konvertuj u ARGB1555
            # 1 bit alpha (0 = transparent, 1 = opaque)
            alpha_bit = 1 if a > 127 else 0

            # Skaliramo 8-bitne vrednosti na 5-bitne
            r5 = (r * 31) // 255
            g5 = (g * 31) // 255
            b5 = (b * 31) // 255

            # Spakuj u 16-bitnu vrednost
            # Format: A RRRRR GGGGG BBBBB (15: A, 14-10: R, 9-5: G, 4-0: B)
            argb1555 = (alpha_bit << 15) | (r5 << 10) | (g5 << 5) | b5

            # Razdvoj na 2 bajta (little-endian za FT800)
            argb1555_data.append(argb1555 & 0xFF)        # LSB
            argb1555_data.append((argb1555 >> 8) & 0xFF) # MSB

        return argb1555_data

    def _convert_to_rgb565(self, pixels):
        """Alternativna konverzija u RGB565 format (bez alpha)"""
        rgb565_data = []

        for pixel in pixels:
            r, g, b, _ = pixel

            # Skaliramo na 5/6/5 bitova
            r5 = (r * 31) // 255
            g6 = (g * 63) // 255
            b5 = (b * 31) // 255

            # Spakuj u 16-bitnu vrednost
            rgb565 = (r5 << 11) | (g6 << 5) | b5

            # Razdvoj na 2 bajta
            rgb565_data.append(rgb565 & 0xFF)        # LSB
            rgb565_data.append((rgb565 >> 8) & 0xFF) # MSB

        return rgb565_data

    def _convert_to_l8(self, pixels):
        """Konvertuje u L8 (grayscale 8-bit) format"""
        l8_data = []

        for pixel in pixels:
            r, g, b, _ = pixel
            # Konvertuj u grayscale
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            l8_data.append(gray)

        return l8_data
    
    def print_all_widget_dicts(self):
        """Ispisuje sve rečnike za sve widget-e"""
        print("\n" + "="*60)
        print("              COMPLETE WIDGET REPORT")
        print("="*60)
        # Prikazi sve widget-e po tipu
        widgets_by_type = {}
        for shape in self.all_shapes:
            widget_type = type(shape).__name__
            if widget_type not in widgets_by_type:
                widgets_by_type[widget_type] = []
            widgets_by_type[widget_type].append(shape)
        # Prikazi za svaki tip
        for widget_type, widgets in widgets_by_type.items():
            print(f"\n{'='*30}")
            print(f"{widget_type.upper()}S ({len(widgets)})")
            print('='*30)
            for i, widget in enumerate(widgets, 1):
                print(f"{widget.custom_name}:")
                # Pokušaj da dobiješ rečnik
                if hasattr(widget, 'get_properties_dict'):
                    props = widget.get_properties_dict()
                    for key, value in props.items():
                        print(f"  {key}: {value}")
                else:
                    # Osnovne informacije za widget-e bez rečnika
                    print(f"  Position: ({widget.x()}, {widget.y()})")
                    print(f"  Size: {widget.width()}x{widget.height()}")
                    if hasattr(widget, 'custom_name'):
                        print(f"  Name: {widget.custom_name}")
        print("\n" + "="*60)
        print(f"TOTAL WIDGETS: {len(self.all_shapes)}")
        print("="*60 + "\n")

if __name__ == "__main__":
    from pathlib import Path
    from PyQt6.QtGui import QGuiApplication

    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)

    BASE_DIR = Path(__file__).resolve().parent
    logo_path = BASE_DIR / "bootup_logo.png"

    splash_pix = QPixmap(str(logo_path))

    splash = QSplashScreen(
        splash_pix.scaled(
            800, 450,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ),
        Qt.WindowType.WindowStaysOnTopHint
    )

    splash.show()
    app.processEvents()

    window = MainWindow()

    QTimer.singleShot(3000, lambda: (
        splash.finish(window),
        window.show()
    ))
    window.resize(1024, 720)

    sys.exit(app.exec())
