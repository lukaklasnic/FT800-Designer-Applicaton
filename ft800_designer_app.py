from PyQt6.QtWidgets import ( QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QColorDialog, QSplashScreen, QFileDialog, QMessageBox )
from generator import ( generateComponentsC, generateComponentsH, generateResources, generateComponents )
from PyQt6.QtGui import ( QPixmap, QIcon, QGuiApplication, QImage )
from PyQt6.QtCore import ( Qt, QTimer )
from ui_components import *
from pathlib import Path
from properties import * 
from widgets import *
import sys

class MainWindow( QMainWindow ):
    def __init__( self ):
        super().__init__()
        self.output_dir = None 
        self.output_dir_label = None 
        self.initMultipleCanvas()
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

        main_horizontal_layout = QHBoxLayout( self.main_widget )
        main_horizontal_layout.setContentsMargins( 0, 0, 0, 0 )
        main_horizontal_layout.setSpacing( 0 )

        self.properties_widget = QWidget()
        self.properties_widget.setMinimumWidth( 248 )
        
        self.central_widget = QWidget()
        
        self.widgets_icon_widget = QWidget()
        self.widgets_icon_widget.setMinimumWidth( 248 )

        self.addWidgetsToPropertiesBar( self.properties_widget )
        self.addWidgetsToCentralLayout( self.central_widget )
        self.addWidgetsToIconsPanel( self.widgets_icon_widget )

        main_horizontal_layout.addWidget( self.properties_widget, 1 )
        
        separate_line_1 = QFrame()
        separate_line_1.setFrameShape( QFrame.Shape.VLine )
        separate_line_1.setFrameShadow( QFrame.Shadow.Sunken )
        separate_line_1.setStyleSheet( "background-color: #666666;" )
        separate_line_1.setLineWidth( 2 )

        main_horizontal_layout.addWidget( separate_line_1 )
        main_horizontal_layout.addWidget( self.central_widget, 4 )
        
        separate_line_2 = QFrame()
        separate_line_2.setFrameShape( QFrame.Shape.VLine )
        separate_line_2.setFrameShadow( QFrame.Shadow.Sunken )
        separate_line_2.setStyleSheet( "background-color: #666666;" )
        separate_line_2.setLineWidth( 2 )

        main_horizontal_layout.addWidget( separate_line_2 )
        main_horizontal_layout.addWidget( self.widgets_icon_widget, 1 )
        
        self.scroll_area.setWidget( self.main_widget )
        self.setCentralWidget( self.scroll_area )
        
        self.canvas_properties_visible = False
        self.shape_properties_visible = False
        self.object_attached = False
        self.selected_shape = None
        self.current_shape = None
        
    def initMultipleCanvas( self ):
        self.canvases = []
        self.current_canvas_index = 0 
        self.all_canvas_dicts = {} 
        self.canvas_widgets = {}
        
        self.createNewCanvas()
        
    def createNewCanvas( self ):
        canvas_id = len( self.canvases )
        canvas = Canvas( canvas_id = canvas_id )
        canvas.clicked.connect( self.onCanvasClicked )
        canvas.properties_changed.connect( lambda: self.updateCanvasDict( canvas ) )
        
        self.canvases.append( canvas )
        self.canvas_widgets[ canvas_id ] = []
        self.all_canvas_dicts[ canvas_id ] = canvas.getCanvasProperties()
        
        return canvas_id
        
    def showCanvas( self, canvas_index ):
        if 0 <= canvas_index < len( self.canvases ):
            self.current_canvas_index = canvas_index
            
            for canvas in self.canvases:
                canvas.hide()
            
            current_canvas = self.canvases[ canvas_index ]
            current_canvas.show()
            
            if hasattr( self, 'prev_btn' ):
                self.prev_btn.setEnabled( canvas_index > 0 )

            if hasattr( self, 'next_btn' ):
                self.next_btn.setEnabled( canvas_index < len( self.canvases ) - 1 )
            
            if hasattr( self, 'canvas_counter_label' ):
                self.canvas_counter_label.setText( f"Canvas { canvas_index + 1 } / {len( self.canvases ) }" )
            
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
        generate_button.setStyleSheet( """
            QPushButton {
                background-color: #dea24a;
                color: black;
                font-weight: bold;
                border: 2px solid #dea24a;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: darkorange;
                border: 2px solid darkorange;
            }
            QPushButton:pressed {
                background-color: #cc5500;
                border: 2px solid #cc5500;
            }
        """ )
        generate_button.clicked.connect( self.generateAllFiles )

        top_layout.addWidget( generate_button )
        top_layout.addStretch( 1 )

        central_layout.addLayout( top_layout )
        central_layout.addStretch( 1 )

        self.canvas_nav_container = QWidget()
        canvas_nav_layout = QVBoxLayout( self.canvas_nav_container )
        canvas_nav_layout.setContentsMargins( 0, 0, 0, 0 )
        canvas_nav_layout.setSpacing( 10 )

        canvas_horizontal_layout = QHBoxLayout()
        canvas_horizontal_layout.setContentsMargins( 0, 0, 0, 0 )
        canvas_horizontal_layout.setSpacing( 10 )

        self.prev_btn = QPushButton( "←" )
        self.prev_btn.setFixedSize( 30, 30 )
        self.prev_btn.setStyleSheet( """
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover:enabled {
                background-color: #888888;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """ )

        self.prev_btn.clicked.connect( self.prevCanvas )
        self.prev_btn.setEnabled( False )
        canvas_horizontal_layout.addWidget( self.prev_btn )

        self.canvas_display_container = QWidget()
        self.canvas_display_container.setFixedSize( 500, 300 )
        canvas_horizontal_layout.addWidget( self.canvas_display_container )

        self.next_btn = QPushButton( "→" )
        self.next_btn.setFixedSize( 30, 30 )
        self.next_btn.setStyleSheet( """
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover:enabled {
                background-color: #888888;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """ )
        self.next_btn.clicked.connect( self.nextCanvas )
        self.next_btn.setEnabled( False )
        canvas_horizontal_layout.addWidget( self.next_btn )
        canvas_nav_layout.addLayout(canvas_horizontal_layout)

        canvas_buttons_layout = QHBoxLayout()
        canvas_buttons_layout.setContentsMargins( 0, 10, 0, 0 )
        canvas_buttons_layout.setSpacing( 10 )
        canvas_buttons_layout.setAlignment( Qt.AlignmentFlag.AlignCenter )

        add_canvas_btn = QPushButton( "+" )
        add_canvas_btn.setFixedSize( 30, 30 )
        add_canvas_btn.setStyleSheet( """
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover:enabled {
                background-color: #888888;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """ )
        add_canvas_btn.clicked.connect( self.addNewCanvas )
        add_canvas_btn.setToolTip( "Add new canvas" )
        canvas_buttons_layout.addWidget( add_canvas_btn )

        self.delete_canvas_btn = QPushButton( "-" )
        self.delete_canvas_btn.setFixedSize( 30, 30 )
        self.delete_canvas_btn.setStyleSheet( """
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover:enabled {
                background-color: #888888;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """ )
        self.delete_canvas_btn.clicked.connect( self.deleteCurrentCanvas )
        self.delete_canvas_btn.setToolTip( "Delete current canvas" )
        self.delete_canvas_btn.setEnabled( len( self.canvases) > 1 )
        canvas_buttons_layout.addWidget( self.delete_canvas_btn )

        canvas_nav_layout.addLayout( canvas_buttons_layout )

        central_layout.addWidget( self.canvas_nav_container )
        central_layout.addStretch( 1 )

        bottom_container = QWidget()
        bottom_layout = QHBoxLayout( bottom_container )
        bottom_layout.setContentsMargins( 5, 5, 5, 5 )
        bottom_layout.setSpacing( 10 )

        self.output_dir_label = QLabel( "Output: Not selected" )
        self.output_dir_label.setStyleSheet( """
            QLabel {
                color: white;
                font-size: 11px;
                background-color: #333333;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #555555;
            }
        """ )
        self.output_dir_label.setMinimumHeight( 30 )
        self.output_dir_label.setAlignment( Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter )
        bottom_layout.addWidget( self.output_dir_label, 1 ) 

        browse_button = QPushButton( "Browse..." )
        browse_button.setFixedSize( 80, 30 )
        browse_button.setStyleSheet( """
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: normal;
                border: 1px solid #777777;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #777777;
                border: 1px solid #888888;
            }
            QPushButton:pressed {
                background-color: #555555;
                border: 1px solid #666666;
            }
        """ )
        browse_button.clicked.connect( self.chooseOutputDirectory )
        browse_button.setToolTip( "Change output directory" )
        bottom_layout.addWidget( browse_button )
        central_layout.addWidget( bottom_container )

        self.setupCanvasesInContainer()

        if self.canvases:
            self.showCanvas( 0 )
            
        self.updateOutputDirLabel()

    def deleteCurrentCanvas( self ):
        if len( self.canvases ) <= 1:
            return

        current_canvas = self.getCurrentCanvas()
        if not current_canvas:
            return

        current_canvas_id = current_canvas.canvas_id

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete canvas {current_canvas_id}?\nAll widgets on this canvas will be lost.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return
        
        if self.canvas_properties_visible:
            self.hideCanvasProperties()

        self.deselectAllShapes()
        self.hideShapeProperties()

        if current_canvas_id in self.canvas_widgets:
            widgets = self.canvas_widgets[ current_canvas_id ]

            for widget in widgets:
                self.deleteWidgetFromDicts( widget )
                widget.deleteLater()

            del self.canvas_widgets[ current_canvas_id ]

        canvas_to_delete = self.canvases.pop( self.current_canvas_index )
        canvas_to_delete.deleteLater()

        if current_canvas_id in self.all_canvas_dicts:
            del self.all_canvas_dicts[ current_canvas_id ]

        self.renumberCanvases()

        if self.current_canvas_index >= len( self.canvases ):
            self.current_canvas_index = len( self.canvases ) - 1

        if self.canvases:
            self.showCanvas( self.current_canvas_index )

        self.delete_canvas_btn.setEnabled( len( self.canvases ) > 1 )

    def deleteWidgetFromDicts( self, widget ):
        if isinstance( widget, LineWidget ) and hasattr( self, 'all_line_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_line_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, RectangleWidget ) and hasattr( self, 'all_rectangle_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_rectangle_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, CircleWidget ) and hasattr( self, 'all_circle_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_circle_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, EllipseWidget ) and hasattr( self, 'all_ellipse_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_ellipse_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, ButtonWidget ) and hasattr( self, 'all_button_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_button_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, KeysWidget ) and hasattr( self, 'all_keys_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_keys_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, ClockWidget ) and hasattr( self, 'all_clock_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_clock_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, GaugeWidget ) and hasattr( self, 'all_gauge_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_gauge_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, DialWidget ) and hasattr( self, 'all_dial_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_dial_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, ToggleWidget ) and hasattr( self, 'all_toggle_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_toggle_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, ScrollBarWidget ) and hasattr( self, 'all_scrollbar_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_scrollbar_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, SliderWidget ) and hasattr( self, 'all_slider_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_label_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, ProgressBarWidget ) and hasattr( self, 'all_progressbar_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_progressbar_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, ImageWidget ) and hasattr( self, 'all_image_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_image_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, LabelWidget ) and hasattr( self, 'all_label_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_label_dicts.pop( widget.custom_name, None )

        elif isinstance( widget, NumericWidget ) and hasattr( self, 'all_numeric_dicts' ):
            if hasattr( widget, 'custom_name' ):
                self.all_numeric_dicts.pop( widget.custom_name, None )

    def renumberCanvases( self ):
        new_canvases = []
        new_canvas_widgets = {}
        new_all_canvas_dicts = {}

        for i, canvas in enumerate( self.canvases ):
            old_id = canvas.canvas_id
            canvas.canvas_id = i
            canvas.name = f"Screen_{ i }"

            if old_id in self.canvas_widgets:
                new_canvas_widgets[ i ] = self.canvas_widgets[ old_id ]

            if old_id in self.all_canvas_dicts:
                canvas_props = self.all_canvas_dicts[ old_id ]
                canvas_props[ 'id' ] = i
                canvas_props[ 'name' ] = f"Screen_{ i }"
                new_all_canvas_dicts[ i ] = canvas_props

            new_canvases.append( canvas )

        self.canvases = new_canvases
        self.canvas_widgets = new_canvas_widgets
        self.all_canvas_dicts = new_all_canvas_dicts
        
    def setupCanvasesInContainer( self ):
        if not hasattr( self, 'canvas_display_container' ) or not hasattr( self, 'canvases' ):
            return
            
        container_layout = QVBoxLayout( self.canvas_display_container )
        container_layout.setContentsMargins( 10, 10, 10, 10 )
        container_layout.setAlignment( Qt.AlignmentFlag.AlignCenter )
        
        for canvas in self.canvases:
            container_layout.addWidget( canvas )
            canvas.hide()
        
    def addWidgetsToIconsPanel( self, widgets_icon_widget ):
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

        widgets_shapes = [ "Line", "Rectangle", "Circle", "Ellipse", "Button", "Keys", "Clock", "Gauge", "Dial", "Toggle", "Scroll bar", "Slider", "Progress bar", "Image", "Label", "Numeric" ]

        row = 0
        col = 0

        for i, shape in enumerate( widgets_shapes ):
            widget_icon = WidgetIcon( shape )
            icons_layout.addWidget( widget_icon, row, col )
            col += 1
            if col >= 2:
                col = 0
                row += 1

        widgets_layout.addWidget( icons_container )
        
    def addNewCanvas( self ):
        canvas_id = self.createNewCanvas()
        
        if hasattr( self, 'canvas_display_container' ):
            self.canvas_display_container.layout().addWidget( self.canvases[ -1 ] )
        
        self.showCanvas( canvas_id )
        self.delete_canvas_btn.setEnabled( len( self.canvases ) > 1 )
        
    def prevCanvas( self ):
        if self.current_canvas_index > 0:
            self.showCanvas( self.current_canvas_index - 1 )
            
    def nextCanvas( self ):
        if self.current_canvas_index < len( self.canvases ) - 1:
            self.showCanvas( self.current_canvas_index + 1 )
            
    def getCurrentCanvas( self ):
        if 0 <= self.current_canvas_index < len( self.canvases ):
            return self.canvases[ self.current_canvas_index ]
        
        return None
        
    def getCurrentCanvasWidgets( self ):
        current_canvas = self.getCurrentCanvas()

        if current_canvas:
            return self.canvas_widgets.get( current_canvas.canvas_id, [] )
        
        return []
        
    def onCanvasClicked( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.current_shape:
                current_canvas = self.getCurrentCanvas()

                if current_canvas:
                    showCanvasProperties( self, current_canvas )
                    self.canvas_properties_visible = True
                    self.shape_properties_visible = False
                    
    def updateCanvasDict( self, canvas ):
        if hasattr( self, 'all_canvas_dicts' ):
            canvas_id = canvas.canvas_id
            
            canvas_props = canvas.getCanvasProperties()
            canvas_props[ 'widgets' ] = [ widget.getPropertiesDict() for widget in self.canvas_widgets.get( canvas_id, [] ) if hasattr( widget, 'getPropertiesDict' ) ]
            self.all_canvas_dicts[ canvas_id ] = canvas_props
            
    def onMainWidgetClick( self, event ):
        if not self.canvases:
            QWidget.mousePressEvent( self.main_widget, event )
            return

        current_canvas = self.getCurrentCanvas()

        if not current_canvas:
            QWidget.mousePressEvent( self.main_widget, event )
            return

        canvas_global = current_canvas.frameGeometry()
        canvas_global.moveTopLeft(current_canvas.mapToGlobal( current_canvas.rect().topLeft() ) )

        properties_global = self.properties_widget.frameGeometry()
        properties_global.moveTopLeft( self.properties_widget.mapToGlobal( self.properties_widget.rect().topLeft() ) )
        global_pos = event.globalPosition().toPoint()

        if canvas_global.contains( global_pos ):
            clicked_on_shape = False
            current_widgets = self.getCurrentCanvasWidgets()

            for shape in current_widgets:
                global_shape = shape.frameGeometry()
                global_shape.moveTopLeft( shape.mapToGlobal( shape.rect().topLeft() ) )
                if global_shape.contains( global_pos ):
                    clicked_on_shape = True

                    break
                
            if clicked_on_shape:
                pass

            elif self.selected_shape and self.object_attached:
                self.addShapeToCanvas( global_pos )

            else:
                self.deselectAllShapes()
                self.hideShapeProperties()

        if ( not canvas_global.contains( global_pos ) and not properties_global.contains( global_pos ) ):
            self.hideCanvasProperties()
            self.deselectAllShapes()
            self.hideShapeProperties()

        QWidget.mousePressEvent( self.main_widget, event )

    def hideCanvasProperties( self ):
        if not self.canvas_properties_visible:
            return
            
        for i in reversed( range( self.properties_layout.count() ) ):
            widget = self.properties_layout.itemAt( i ).widget()

            if widget:
                widget.hide()
                self.properties_layout.removeWidget( widget )
                widget.deleteLater()
        
        self.canvas_properties_visible = False

    def deselectAllShapes( self ):
        current_widgets = self.getCurrentCanvasWidgets()

        for shape in current_widgets:
            if shape:
                shape.setSelected( False )

        self.current_shape = None

    def keyPressEvent( self, event ):
        if event.key() == Qt.Key.Key_Delete and self.current_shape:
            self.deleteSelectedShape()

        else:
            super().keyPressEvent( event )
    
    def deleteSelectedShape( self ):
        if self.current_shape:
            current_canvas = self.getCurrentCanvas()

            if not current_canvas:
                return
                
            current_canvas_id = current_canvas.canvas_id
            current_widgets = self.canvas_widgets.get( current_canvas_id, [] )

            if self.current_shape in current_widgets:
                current_widgets.remove( self.current_shape )

            if isinstance( self.current_shape, LineWidget ) and hasattr( self, 'all_line_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_line_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, RectangleWidget ) and hasattr( self, 'all_rectangle_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_rectangle_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, CircleWidget ) and hasattr( self, 'all_circle_dicts' ):
                 if hasattr( self.current_shape, 'custom_name' ):
                     self.all_circle_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, EllipseWidget ) and hasattr( self, 'all_ellipse_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_ellipse_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, ButtonWidget ) and hasattr(self, 'all_button_dicts'):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_button_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, KeysWidget ) and hasattr( self, 'all_keys_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_keys_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, ClockWidget ) and hasattr( self, 'all_clock_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_clock_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, GaugeWidget ) and hasattr( self, 'all_gauge_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_gauge_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, DialWidget ) and hasattr( self, 'all_dial_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_dial_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, ToggleWidget ) and hasattr( self, 'all_toggle_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_toggle_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, ScrollBarWidget ) and hasattr( self, 'all_scrollbar_dicts' ):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_scrollbar_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, SliderWidget ) and hasattr( self, 'all_slider_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_slider_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, ProgressBarWidget ) and hasattr( self, 'all_progressbar_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_progressbar_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, ImageWidget ) and hasattr( self, 'all_image_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_image_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, LabelWidget ) and hasattr( self, 'all_label_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_label_dicts.pop( self.current_shape.custom_name, None )

            elif isinstance( self.current_shape, NumericWidget ) and hasattr( self, 'all_numeric_dicts' ):
                if hasattr( self.current_shape, 'custom_name' ):
                    self.all_numeric_dicts.pop( self.current_shape.custom_name, None )

            self.current_shape.deleteLater()
            self.current_shape = None
            self.hideShapeProperties()
            self.deselectAllShapes()
            self.renumberStackOrders()
            renumberAllWidgets( self )
            self.updateCanvasDict( current_canvas )

    def renumberStackOrders( self ):
        current_widgets = self.getCurrentCanvasWidgets()

        if not current_widgets:
            return

        sorted_widgets = sorted( current_widgets, key = lambda x: x.stack_order )
        for i, widget in enumerate( sorted_widgets, 1 ):
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

    def selectShape( self, shape ):
        self.deselectAllShapes()
        shape.setSelected( True )
        self.current_shape = shape
        self.main_widget.setFocus()
        self.hideCanvasProperties()
        self.showShapeProperties()

    def addShapeToCanvas( self, global_pos ):
        current_canvas = self.getCurrentCanvas()

        if not current_canvas:
            return
            
        widget_container = current_canvas.getWidgetContainer()

        if not widget_container:
            return
        
        canvas_container = current_canvas.getCanvasContainer()

        if not canvas_container:
            return
        
        canvas_global = canvas_container.frameGeometry()
        canvas_global.moveTopLeft( canvas_container.mapToGlobal( canvas_container.rect().topLeft() ) )
        
        if not canvas_global.contains( global_pos ):
            return
        
        container_pos = widget_container.mapFromGlobal( global_pos )
        shape = None

        if self.selected_shape == "Line":
            shape = LineWidget(widget_container)
            start_x = container_pos.x() 
            start_y = container_pos.y()
            end_x = container_pos.x() + 100
            end_y = container_pos.y()
            shape.setLinePoints( start_x, start_y, end_x, end_y )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Line" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr( self, 'all_line_dicts' ):
                self.all_line_dicts = {}

            self.all_line_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Rectangle":
            shape = RectangleWidget( 100, 80, widget_container )
            shape.move( container_pos.x() - 50, container_pos.y() - 40 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Rectangle" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr( self, 'all_rectangle_dicts' ):
                self.all_rectangle_dicts = {}

            self.all_rectangle_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Circle":
            shape = CircleWidget( 100, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Circle" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.updateCenterPosition()
            shape.tag = generateAutoTag( self, shape )

            if not hasattr( self, 'all_circle_dicts' ):
                self.all_circle_dicts = {}

            self.all_circle_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Ellipse":
            shape = EllipseWidget( 98, 78, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )

            shape.custom_name = generateWidgetName(self, "Ellipse")
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr( self, 'all_ellipse_dicts' ):
                self.all_ellipse_dicts = {}

            self.all_ellipse_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Button":
            shape = ButtonWidget( 100, 50, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.custom_name = generateWidgetName( self, "Button" )
            shape.clicked.connect( self.selectShape )
            shape.setMouseTracking( True )
            shape.raise_()
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.updatePropertiesDict()

            if not hasattr( self, 'all_button_dicts' ):
                self.all_button_dicts = {}

            self.all_button_dicts[ shape.custom_name ] = shape.getPropertiesDict()

            shape.tag = generateAutoTag( self, shape )

        elif self.selected_shape == "Keys":
            shape = KeysWidget( 200, 120, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Keys" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1

            if not hasattr( self, 'all_keys_dicts' ):
                self.all_keys_dicts = {}

            self.all_keys_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Clock":
            shape = ClockWidget( 100, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Clock" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.updatePropertiesDict()

            if not hasattr(self, 'all_clock_dicts'):
                self.all_clock_dicts = {}

            self.all_clock_dicts[shape.custom_name] = shape.getPropertiesDict()

        elif self.selected_shape == "Gauge":
            shape = GaugeWidget( 80, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Gauge" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )
            shape.updatePropertiesDict()

            if not hasattr( self, 'all_gauge_dicts' ):
                self.all_gauge_dicts = {}

            self.all_gauge_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Dial":
            shape = DialWidget( 80, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Dial" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr(self, 'all_dial_dicts'):
                self.all_dial_dicts = {}

            self.all_dial_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Toggle":
            shape = ToggleWidget( 80, 30, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Toggle" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr(self, 'all_toggle_dicts'):
                self.all_toggle_dicts = {}

            self.all_toggle_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Scroll bar":
            shape = ScrollBarWidget( 150, 10, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect(self.selectShape)
            shape.custom_name = generateWidgetName( self, "ScrollBar" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr( self, 'all_scrollbar_dicts' ):
                self.all_scrollbar_dicts = {}

            self.all_scrollbar_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Slider":
            shape = SliderWidget( 200, 50, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Slider" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.tag = generateAutoTag( self, shape )

            if not hasattr(self, 'all_slider_dicts'):
                self.all_slider_dicts = {}

            self.all_slider_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Progress bar":
            shape = ProgressBarWidget( 150, 10, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "ProgressBar" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1
            shape.updatePropertiesDict()

            if not hasattr( self, 'all_progressbar_dicts' ):
                self.all_progressbar_dicts = {}

            self.all_progressbar_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Image":
            shape = ImageWidget( 100, 100, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName(self, "Image")
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1

            if not hasattr( self, 'all_image_dicts' ):
                self.all_image_dicts = {}

            self.all_image_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Label":
            shape = LabelWidget( 100, 40, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect(self.selectShape)
            shape.custom_name = generateWidgetName( self, "Label" )
            shape.stack_order = len(self.getCurrentCanvasWidgets()) + 1

            if not hasattr( self, 'all_label_dicts' ):
                self.all_label_dicts = {}

            self.all_label_dicts[ shape.custom_name ] = shape.getPropertiesDict()

        elif self.selected_shape == "Numeric":
            shape = NumericWidget( 100, 40, widget_container )
            shape.move( container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2 )
            shape.clicked.connect( self.selectShape )
            shape.custom_name = generateWidgetName( self, "Numeric" )
            shape.stack_order = len( self.getCurrentCanvasWidgets() ) + 1

            if not hasattr( self, 'all_numeric_dicts' ):
                self.all_numeric_dicts = {}

            self.all_numeric_dicts[ shape.custom_name ] = shape.getPropertiesDict()

            shape.show()
            self.canvas_widgets[ current_canvas.canvas_id ].append( shape )
            self.updateWidgetsZOrder()
            self.selectShape( shape )
            QApplication.restoreOverrideCursor()
            self.object_attached = False
            self.selected_shape = None
            self.updateCanvasDict( current_canvas )
            return

        if shape:
            current_widgets_count = len( self.getCurrentCanvasWidgets() )
            shape.stack_order = current_widgets_count + 1

            shape.show()
            shape.raise_()
            
            self.canvas_widgets[ current_canvas.canvas_id ].append( shape )
            self.sortWidgetsByStackOrder()
            self.selectShape( shape )
            
            QApplication.restoreOverrideCursor()
            self.object_attached = False
            self.selected_shape = None
            
            self.updateCanvasDict( current_canvas )

    def updateWidgetsZOrder( self ):
        current_widgets = self.getCurrentCanvasWidgets()
        sorted_widgets = sorted( current_widgets, key = lambda x: x.stack_order )

        for widget in current_widgets:
            widget.lower()

        for widget in sorted_widgets:
            widget.raise_()

    def showShapeProperties( self ):
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
            if hasattr( self, attr ):
                delattr( self, attr )

        if not self.current_shape:
            return

        current_index = 0

        if isinstance( self.current_shape, LineWidget ):
            shape_label = QLabel( "Line Properties" )

        elif isinstance( self.current_shape, RectangleWidget ):
            shape_label = QLabel( "Rectangle Properties" )

        elif isinstance( self.current_shape, CircleWidget ):
            shape_label = QLabel( "Circle Properties" )

        elif isinstance( self.current_shape, EllipseWidget ):
            shape_label = QLabel( "Ellipse Properties" )

        elif isinstance( self.current_shape, ButtonWidget ):
            shape_label = QLabel( "Button Properties" )

        elif isinstance( self.current_shape, KeysWidget ):
            shape_label = QLabel( "Keyboard Properties" )

        elif isinstance( self.current_shape, ClockWidget ):
            shape_label = QLabel( "Clock Properties" )

        elif isinstance( self.current_shape, GaugeWidget ):
            shape_label = QLabel( "Gauge Properties" )

        elif isinstance( self.current_shape, DialWidget ):
            shape_label = QLabel( "Dial Properties" )

        elif isinstance( self.current_shape, ToggleWidget ):
            shape_label = QLabel( "Toggle Properties" )

        elif isinstance( self.current_shape, ScrollBarWidget ):
            shape_label = QLabel( "Scroll bar Properties" )

        elif isinstance( self.current_shape, SliderWidget ):
            shape_label = QLabel( "Slider Properties" )

        elif isinstance( self.current_shape, ProgressBarWidget ):
            shape_label = QLabel( "Progress bar Properties" )

        elif isinstance( self.current_shape, ImageWidget ):
            shape_label = QLabel( "Image Properties" )

        elif isinstance( self.current_shape, LabelWidget ):
            shape_label = QLabel( "Label Properties" )

        elif isinstance( self.current_shape, NumericWidget ):
            shape_label = QLabel( "Numeric Widget Properties" )

        shape_label.setStyleSheet( "color: white; font-size: 14px; font-weight: bold; margin-top: 10px;" )
        self.properties_layout.insertWidget( current_index, shape_label )
        current_index += 1

        if isinstance( self.current_shape, LineWidget ):
            current_index = showLineProperties( self, current_index )

        elif isinstance( self.current_shape, RectangleWidget ):
            current_index = showRectangleProperties( self, current_index )

        elif isinstance( self.current_shape, CircleWidget ):
            current_index = showCircleProperties( self, current_index )

        elif isinstance( self.current_shape, EllipseWidget ):
            current_index = showEllipseProperties( self, current_index )

        elif isinstance( self.current_shape, ButtonWidget ):
            current_index = showButtonProperties( self, current_index )

        elif isinstance( self.current_shape, KeysWidget ):
            current_index = showKeysProperties( self, current_index )

        elif isinstance( self.current_shape, ClockWidget ):
            current_index = showClockProperties( self, current_index )

        elif isinstance( self.current_shape, GaugeWidget ):
            current_index = showGaugeProperties( self, current_index )

        elif isinstance( self.current_shape, DialWidget ):
            current_index = showDialProperties( self, current_index )

        elif isinstance( self.current_shape, ToggleWidget ):
            current_index = showToggleProperties( self, current_index )

        elif isinstance( self.current_shape, ScrollBarWidget ):
            current_index = showScrollBarProperties( self, current_index )

        elif isinstance( self.current_shape, SliderWidget ):
            current_index = showSliderProperties( self, current_index )

        elif isinstance( self.current_shape, ProgressBarWidget ):
            current_index = showProgressBarProperties( self, current_index )

        elif isinstance( self.current_shape, ImageWidget ):
            current_index = showImageProperties( self, current_index )

        elif isinstance( self.current_shape, LabelWidget ):
            current_index = showLabelProperties( self, current_index )

        elif isinstance( self.current_shape, NumericWidget ):
            current_index = showNumericProperties( self, current_index )

        self.shape_properties_visible = True

    def updateStackOrder( self, value ):
        if self.current_shape:
            self.current_shape.stack_order = value
            self.sortWidgetsByStackOrder()

    def sortWidgetsByStackOrder( self ):
        current_widgets = self.getCurrentCanvasWidgets()

        if not current_widgets:
            return
    
        sorted_widgets = sorted( current_widgets, key = lambda x: x.stack_order )
    
        for widget in current_widgets:
            widget.lower()
    
        for widget in sorted_widgets:
            widget.raise_()
    
        for i, widget in enumerate( sorted_widgets ):
            if hasattr( widget, 'custom_name' ):
                widget_name = widget.custom_name 

            else:
                widget_name = 'Unknown'


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
                self.current_shape.setColor( color )
                self.color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

    def updateShapeBorderWidth( self ):
        if ( self.current_shape and not isinstance( self.current_shape, ( GaugeWidget, ClockWidget, ProgressBarWidget ) ) and  hasattr( self.current_shape, 'setBorderWidth' ) ):
            self.current_shape.setBorderWidth( self.border_width_spin.value() )

    def setTag( self, tag_value ):
        self.tag = tag_value
        self.updatePropertiesDict()
        main_window = self.findMainWindow()

        if main_window:
            if isinstance( self, LineWidget ) and hasattr( main_window, 'all_line_dicts' ):
                main_window.all_line_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, RectangleWidget ) and hasattr( main_window, 'all_rectangle_dicts' ):
                main_window.all_rectangle_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, CircleWidget ) and hasattr( main_window, 'all_circle_dicts' ):
                main_window.all_circle_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, EllipseWidget ) and hasattr( main_window, 'all_ellipse_dicts' ):
                main_window.all_ellipse_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, ButtonWidget ) and hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, KeysWidget ) and hasattr( main_window, 'all_keys_dicts' ):
                main_window.all_keys_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, ClockWidget ) and hasattr( main_window, 'all_clock_dicts' ):
                main_window.all_clock_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, GaugeWidget ) and hasattr( main_window, 'all_gauge_dicts' ):
                main_window.all_gauge_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, DialWidget ) and hasattr( main_window, 'all_dial_dicts' ):
                main_window.all_dial_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, ToggleWidget ) and hasattr( main_window, 'all_toggle_dicts' ):
                main_window.all_keys_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, ScrollBarWidget ) and hasattr( main_window, 'all_scroll_bar_dicts' ):
                main_window.all_scroll_bar_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, SliderWidget ) and hasattr( main_window, 'all_slider_dicts' ):
                main_window.all_slider_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, ProgressBarWidget ) and hasattr( main_window, 'all_progress_bar_dicts' ):
                main_window.all_prgress_bar_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, ImageWidget ) and hasattr( main_window, 'all_image_dicts' ):
                main_window.all_image_dicts[ self.custom_name ] = self.getPropertiesDict()

            elif isinstance( self, LabelWidget ) and hasattr( main_window, 'all_label_dicts' ):
                main_window.all_label_dicts[self.custom_name] = self.getPropertiesDict()

            elif isinstance( self, NumericWidget ) and hasattr( main_window, 'all_numeric_dicts' ):
                main_window.all_numeric_dicts[ self.custom_name ] = self.getPropertiesDict()

    def ensureWidgetFields( self, widget_dict ):
        widget_type = widget_dict.get( 'type' )

        if 'visible' not in widget_dict:
            widget_dict[ 'visible' ] = True
        if 'active' not in widget_dict:
            widget_dict[ 'active' ] = True
        if 'static' not in widget_dict:
            widget_dict[ 'static' ] = False
        if 'stack_order' not in widget_dict:
            widget_dict[ 'stack_order' ] = 1
        defaults = {}

        if widget_type == 'Line':
            defaults = { 'x1': 0, 'y1': 0, 'x2': 100, 'y2': 0, 'color': 0xFF0000, 'width': 1, 'tag': 1 } 

        elif widget_type == 'Rectangle':
            defaults = { 'x': 0, 'y': 0, 'width': 100, 'height': 100, 'edges_color': 0xFF0000, 'thickness': 1, 'filled': True, 'fill_color': 0x0000FF, 'tag': 2, 'gradient_enable': False, 'gradient_type': 'left_right', 'gradient_start_color': 0xFF0000, 'gradient_end_color': 0x0000FF }

        elif widget_type == 'Circle':
            defaults = { 'center_x': 100, 'center_y': 100, 'diameter': 100, 'line_color': 0xFF0000, 'line_thickness': 1, 'filled': True, 'fill_color': 0x0000FF, 'tag': 3 }

        elif widget_type == 'Ellipse':
            defaults = { 'center_x': 100, 'center_y': 100, 'width': 150, 'height': 75, 'border_color': 0xCA75FE, 'border_width': 1, 'filled': True, 'fill_color': 0x0000FF, 'tag': 4, 'gradient_enable': False, 'gradient_type': 'top_bottom', 'gradient_start_color': 0xFF0000, 'gradient_end_color': 0x0000FF }

        elif widget_type == 'Button':
            defaults = { 'x': 100, 'y': 100, 'width': 100, 'height': 100, 'start_color': 0xFF0000, 'end_color': 0x00FF00, '3d_enable': True, 'text': 'Press', 'text_size': 28, 'text_color': 0xFF0000, 'tag': 5 }

        elif widget_type == 'Keys':
            defaults = { 'x': 10, 'y': 10, 'width': 300, 'height': 60, 'key_color_top': 0xFFFF00, 'key_color_bottom': 0xFFFF00, 'text_color': 0x00FF00, '3d_enable': True, 'key_type': 'NUM', 'text_size': 27 }

        elif widget_type == 'Clock':
            defaults = { 'center_x': 240, 'center_y': 136, 'diameter': 100, 'background_color': 0x0000FF, '3d_enable': True, 'hours': 9, 'minutes': 53, 'seconds': 0 }

        elif widget_type == 'Gauge':
            defaults = { 'center_x': 100, 'center_y': 100, 'diameter': 100, 'background_color': 0xFF0000, '3d_enable': True, 'major_subdivision': 6, 'minor_subdivision': 3, 'range_value': 100, 'value': 50 }

        elif widget_type == 'Dial':
            defaults = { 'center_x': 240, 'center_y': 130, 'diameter': 50, '3d_enable': True, 'value': 0.5, 'tag': 6 }

        elif widget_type == 'Toggle':
            defaults = { 'x': 50, 'y': 50, 'width': 40, 'thumb_color': 0xFF00FF, 'background_color': 0x0000FF, '3d_enable': True, 'is_on': False, 'tag': 7 }

        elif widget_type == 'ScrollBar':
            defaults = { 'x': 100, 'y': 100, 'width': 100, 'height': 10, 'thumb_color': 0x0000FF, 'track_color': 0xFFFF00, '3d_enable': True, 'range_value': 65535, 'current_val': 32767, 'knob_size': 1000, 'tag': 8 }

        elif widget_type == 'Slider':
            defaults = { 'x': 100, 'y': 100, 'width': 100, 'height': 10, 'knob_color': 0x00FF00, 'background_left_color': 0xFF0000, 'background_right_color': 0x0000FF, '3d_enable': True, 'range_value': 65535, 'value': 32767, 'tag': 9 }

        elif widget_type == 'ProgressBar':
            defaults = { 'x': 100, 'y': 100, 'width': 100, 'height': 10, 'progress_color': 0xFFFFFF, 'background_color': 0xFF0000, '3d_enable': True, 'max_value': 100, 'value': 50 }

        elif widget_type == 'Image':
            defaults = { 'x': 50, 'y': 50, 'width': 200, 'height': 100, 'frame_enable': False, 'frame_color': 0xFF0000, 'frame_width': 2 }

        elif widget_type == 'Label':
            defaults = { 'x': 100, 'y': 100, 'text_color': 0x0000FF, 'text': 'Labela', 'text_size': 30, 'alignment': 'right' }

        elif widget_type == 'Numeric':
            defaults = { 'x': 100, 'y': 100, 'number_color': 0xFF00EF, 'number': 3110, 'number_size': 30, 'alignment': 'right' }

        for key, value in defaults.items():
            if key not in widget_dict:
                widget_dict[ key ] = value    

    def updateOutputDirLabel( self ):
        if not hasattr(self, 'output_dir_label') or not self.output_dir_label:
            return

        if hasattr( self, 'output_dir' ) and self.output_dir:
            display_path = self.output_dir

            if len( display_path ) > 50:
                display_path = display_path[ :20 ] + "..." + display_path[ -27: ]

            self.output_dir_label.setText( f"Output: { display_path }" )
            self.output_dir_label.setToolTip(self.output_dir)

        else:
            self.output_dir_label.setText( "Output: Not selected" )
            self.output_dir_label.setToolTip("")

    def chooseOutputDirectory( self ):
        dir_path = QFileDialog.getExistingDirectory( self, "Select output directory for generated files" )

        if dir_path:
            self.output_dir = dir_path
            self.updateOutputDirLabel()

    def generateAllFiles( self ):
        if not self.output_dir:
            self.chooseOutputDirectory()

        if not self.output_dir:
            return

        self.updateOutputDirLabel()
        generateResources( self, self.output_dir )
        generateComponents( self, self.output_dir )

if __name__ == "__main__":
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy( Qt.HighDpiScaleFactorRoundingPolicy.PassThrough )
    app = QApplication(sys.argv)
    BASE_DIR = Path(__file__).resolve().parent
    logo_path = BASE_DIR / "bootup_logo.png"
    splash_pix = QPixmap( str( logo_path ) )
    splash = QSplashScreen( splash_pix.scaled( 800, 450, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation ), Qt.WindowType.WindowStaysOnTopHint )
    splash.show()
    app.processEvents()
    window = MainWindow()
    QTimer.singleShot( 3000, lambda: ( splash.finish( window ), window.show() ) )
    window.resize( 1024, 720 ) 
    sys.exit( app.exec() )