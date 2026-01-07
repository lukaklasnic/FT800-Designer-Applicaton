from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QCheckBox, 
                             QColorDialog, QComboBox, QSpinBox, QSplashScreen, QFileDialog, 
                             QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon, QGuiApplication
from widgets import (RectangleWidget, LineWidget, CircleWidget, KeysWidget, ButtonWidget, 
                     GaugeWidget, ClockWidget, ProgressBarWidget, ScrollBarWidget, DialWidget, 
                     SliderWidget, ToggleWidget, LabelWidget, ImageWidget, Widget_icon, 
                     ColorRectangle, EllipseWidget, NumericWidget, Canvas)
import sys
from callback import (generate_auto_tag, showButtonProperties, updateButtonSize, 
                      showLineProperties, generateWidgetName, renumberAllWidgets, 
                      showCircleProperties, updateCircleSize, showRectangleProperties, 
                      showClockProperties, updateClockSize, updateGaugeSize, 
                      showGaugeProperties, showDialProperties, updateDialSize, 
                      showToggleProperties, updateToggleSize, showLabelProperties, 
                      updateLabelSize, showSliderProperties, showScrollBarProperties, 
                      showProgressBarProperties, showKeysProperties, update_keys_size, 
                      updateImageSize, showImageProperties, showEllipseProperties, 
                      updateEllipseSize, showNumericProperties, show_canvas_properties)
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_title_bar()
        self.set_scroll_area()
        self.set_main_layouts()
        
    def set_title_bar(self):
        self.setWindowTitle("FT800 Designer application")
        self.setWindowIcon(QIcon("B:\Dokumenti\Fakultet\Merno Informacioni Sistemi i Smart Tehnologije\FT800-Designer-Applicaton\designer_logo_ic"))

    def set_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

    def set_main_layouts(self):
        self.main_widget = QWidget()
        self.main_widget.setMinimumSize(1919, 1008)
        self.main_widget.mousePressEvent = self.on_main_widget_click
        self.main_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        main_horizontal_layout = QHBoxLayout(self.main_widget)
        main_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        main_horizontal_layout.setSpacing(0)

        # Properties panel (levo)
        self.properties_widget = QWidget()
        self.properties_widget.setMinimumWidth(248)
        
        # Centralni panel sa canvasom
        self.central_widget = QWidget()
        
        # Widgets panel (desno)
        self.widgets_icon_widget = QWidget()
        self.widgets_icon_widget.setMinimumWidth(248)

        # Dodaj elemente u svaki panel
        self.add_widgets_to_properties_bar(self.properties_widget)
        self.add_widgets_to_central_layout(self.central_widget)
        self.add_widgets_to_icons_panel(self.widgets_icon_widget)

        # Sastavi glavni layout
        main_horizontal_layout.addWidget(self.properties_widget, 1)
        
        separate_line_1 = QFrame()
        separate_line_1.setFrameShape(QFrame.Shape.VLine)
        separate_line_1.setFrameShadow(QFrame.Shadow.Sunken)
        separate_line_1.setStyleSheet("background-color: #666666;")
        separate_line_1.setLineWidth(2)
        main_horizontal_layout.addWidget(separate_line_1)

        main_horizontal_layout.addWidget(self.central_widget, 4)
        
        separate_line_2 = QFrame()
        separate_line_2.setFrameShape(QFrame.Shape.VLine)
        separate_line_2.setFrameShadow(QFrame.Shadow.Sunken)
        separate_line_2.setStyleSheet("background-color: #666666;")
        separate_line_2.setLineWidth(2)
        main_horizontal_layout.addWidget(separate_line_2)

        main_horizontal_layout.addWidget(self.widgets_icon_widget, 1)
        
        self.scroll_area.setWidget(self.main_widget)
        self.setCentralWidget(self.scroll_area)
        
        # Inicijalizuj ostale atribute
        self.canvas_properties_visible = False
        self.shape_properties_visible = False
        self.object_attached = False
        self.selected_shape = None
        self.current_shape = None
        self.all_shapes = []

    def add_widgets_to_properties_bar(self, properties_widget):
        self.properties_layout = QVBoxLayout(properties_widget)
        self.properties_layout.setContentsMargins(10, 10, 10, 10)
        self.properties_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def add_widgets_to_central_layout(self, central_widget):
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(10, 10, 10, 10)
        central_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Top layout sa generate dugmetom
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)

        generate_button = QPushButton("Generate")
        generate_button.setFixedSize(100, 50)
        generate_button.setStyleSheet("""
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
        """)
        generate_button.clicked.connect(self.print_all_widget_dicts)

        top_layout.addWidget(generate_button)
        top_layout.addStretch(1)

        central_layout.addLayout(top_layout)
        central_layout.addStretch(1)

        # Canvas - SAMO Canvas objekat, bez dodatnog containera
        self.canvas = Canvas()
        self.canvas.clicked.connect(self.on_canvas_clicked)

        canvas_outer_container = QWidget()
        canvas_layout = QHBoxLayout(canvas_outer_container)
        canvas_layout.addStretch(1)
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addStretch(1)

        central_layout.addWidget(canvas_outer_container)
        central_layout.addStretch(1)

    def add_widgets_to_icons_panel(self, widgets_icon_widget):
        widgets_layout = QVBoxLayout(widgets_icon_widget)
        widgets_layout.setContentsMargins(10, 10, 10, 10)
        widgets_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Widgets")
        label.setStyleSheet("color: white; font-size: 16px; font-weight: normal;")
        widgets_layout.addWidget(label)

        icons_container = QWidget()
        icons_layout = QGridLayout(icons_container)
        icons_layout.setSpacing(20)
        icons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        widgets_shapes = ["Line", "Rectangle", "Circle", "Ellipse", "Button", "Keys", 
                         "Clock", "Gauge", "Dial", "Toggle", "Scroll bar", "Slider", 
                         "Progress bar", "Image", "Label", "Numeric"]

        row = 0
        col = 0

        for i, shape in enumerate(widgets_shapes):
            widget_icon = Widget_icon(shape)
            icons_layout.addWidget(widget_icon, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1

        widgets_layout.addWidget(icons_container)

    def on_canvas_clicked(self, event):
        """Handler za klik na canvas"""
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.current_shape:
                show_canvas_properties(self, self.canvas)
                self.canvas_properties_visible = True
                self.shape_properties_visible = False

    def on_main_widget_click(self, event):
        if not hasattr(self, 'canvas'):
            QWidget.mousePressEvent(self.main_widget, event)
            return

        # Dobij globalne pozicije
        canvas_global = self.canvas.frameGeometry()
        canvas_global.moveTopLeft(self.canvas.mapToGlobal(self.canvas.rect().topLeft()))

        properties_global = self.properties_widget.frameGeometry()
        properties_global.moveTopLeft(self.properties_widget.mapToGlobal(self.properties_widget.rect().topLeft()))

        global_pos = event.globalPosition().toPoint()

        if canvas_global.contains(global_pos):
            # Proveri da li je kliknut neki widget
            clicked_on_shape = False
            for shape in self.all_shapes:
                global_shape = shape.frameGeometry()
                global_shape.moveTopLeft(shape.mapToGlobal(shape.rect().topLeft()))
                if global_shape.contains(global_pos):
                    clicked_on_shape = True
                    break
                
            if clicked_on_shape:
                pass
            elif self.selected_shape and self.object_attached:
                self.add_shape_to_canvas(global_pos)
            else:
                self.deselect_all_shapes()
                self.hide_shape_properties()

        # Ako je klik van canvasa i properties panela
        if (not canvas_global.contains(global_pos) and 
            not properties_global.contains(global_pos)):
            self.hide_canvas_properties()
            self.deselect_all_shapes()
            self.hide_shape_properties()

        QWidget.mousePressEvent(self.main_widget, event)

    def hide_canvas_properties(self):
        if not self.canvas_properties_visible:
            return
            
        for i in reversed(range(self.properties_layout.count())):
            widget = self.properties_layout.itemAt(i).widget()
            if widget:
                widget.hide()
                self.properties_layout.removeWidget(widget)
                widget.deleteLater()
        
        self.canvas_properties_visible = False

    def deselect_all_shapes(self):
        for shape in self.all_shapes:
            if shape:
                shape.set_selected(False)
        self.current_shape = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete and self.current_shape:
            self.delete_selected_shape()
        else:
            super().keyPressEvent(event)
    
    def delete_selected_shape(self):
        if self.current_shape:
            was_button = isinstance(self.current_shape, ButtonWidget)
            was_line = isinstance(self.current_shape, LineWidget)
            was_clock = isinstance(self.current_shape, ClockWidget)
            was_gauge = isinstance(self.current_shape, GaugeWidget)

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
            elif was_clock and hasattr(self, 'all_clock_dicts'):
                if hasattr(self.current_shape, 'custom_name'):
                    self.all_clock_dicts.pop(self.current_shape.custom_name, None)
            elif was_gauge and hasattr(self, 'all_gauge_dicts'):
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

            self.hide_shape_properties()
            self.deselect_all_shapes()
            self.renumber_stack_orders()

            renumberAllWidgets(self)

    def renumber_stack_orders(self):
        """Renumeriše stack_order vrednosti nakon brisanja widget-a"""
        if not self.all_shapes:
            return

        sorted_widgets = sorted(self.all_shapes, key=lambda x: x.stack_order)
        for i, widget in enumerate(sorted_widgets, 1):
            widget.stack_order = i

        self.sort_widgets_by_stack_order()

    def hide_shape_properties(self):
        if not self.shape_properties_visible:
            return
        
        for i in reversed(range(self.properties_layout.count())):
            widget = self.properties_layout.itemAt(i).widget()
            if widget:
                widget.hide()
                self.properties_layout.removeWidget(widget)
                widget.deleteLater()

        self.shape_properties_visible = False

    def select_shape(self, shape):
        self.deselect_all_shapes()
        shape.set_selected(True)
        self.current_shape = shape

        self.main_widget.setFocus()
        self.hide_canvas_properties()
        self.show_shape_properties()

    def add_shape_to_canvas(self, global_pos):
        # Mapiraj globalnu poziciju na poziciju u canvas widget container-u
        widget_container = self.canvas.get_widget_container()
        if not widget_container:
            print("ERROR: Widget container not found!")
            return
        
        # Prvo proveri da li je klik u okviru canvasa
        canvas_container = self.canvas.get_canvas_container()
        if not canvas_container:
            print("ERROR: Canvas container not found!")
            return
        
        # Proveri da li je klik u okviru canvasa
        canvas_global = canvas_container.frameGeometry()
        canvas_global.moveTopLeft(canvas_container.mapToGlobal(canvas_container.rect().topLeft()))
        
        if not canvas_global.contains(global_pos):
            print("Click outside canvas area!")
            return
        
        container_pos = widget_container.mapFromGlobal(global_pos)
        print(f"Adding widget at position: {container_pos}")
        shape = None

        if self.selected_shape == "Rectangle":
            shape = RectangleWidget(100, 80, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - 50, container_pos.y() - 40)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Rectangle")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_rectangle_dicts'):
                self.all_rectangle_dicts = {}
            self.all_rectangle_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Line":
            shape = LineWidget(widget_container)  # widget_container umesto self.canvas

            # Postavi početne tačke linije
            start_x = container_pos.x() 
            start_y = container_pos.y()
            end_x = container_pos.x() + 100
            end_y = container_pos.y()

            shape.set_line_points(start_x, start_y, end_x, end_y)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Line")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_line_dicts'):
                self.all_line_dicts = {}
            self.all_line_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Circle":
            shape = CircleWidget(100, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Circle")
            shape.stack_order = len(self.all_shapes) + 1
            shape.update_center_position()
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_circle_dicts'):
                self.all_circle_dicts = {}
            self.all_circle_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Ellipse":
            shape = EllipseWidget(98, 78, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Ellipse")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_ellipse_dicts'):
                self.all_ellipse_dicts = {}
            self.all_ellipse_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Numeric":
            shape = NumericWidget(100, 40, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Numeric")
            shape.stack_order = len(self.all_shapes) + 1

            if not hasattr(self, 'all_numeric_dicts'):
                self.all_numeric_dicts = {}
            self.all_numeric_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Button":
            shape = ButtonWidget(100, 50, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.custom_name = generateWidgetName(self, "Button")
            shape.clicked.connect(self.select_shape)
            shape.setMouseTracking(True)
            shape.raise_()
            shape.stack_order = len(self.all_shapes) + 1
            shape.update_properties_dict()

            if not hasattr(self, 'all_button_dicts'):
                self.all_button_dicts = {}
            self.all_button_dicts[shape.custom_name] = shape.get_properties_dict()

            shape.tag = generate_auto_tag(self, shape)

        elif self.selected_shape == "Gauge":
            shape = GaugeWidget(80, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Gauge")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)
            shape.update_properties_dict()

            if not hasattr(self, 'all_gauge_dicts'):
                self.all_gauge_dicts = {}
            self.all_gauge_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Clock":
            shape = ClockWidget(100, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Clock")
            shape.stack_order = len(self.all_shapes) + 1
            shape.update_properties_dict()

            if not hasattr(self, 'all_clock_dicts'):
                self.all_clock_dicts = {}
            self.all_clock_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Progress bar":
            shape = ProgressBarWidget(150, 10, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "ProgressBar")
            shape.stack_order = len(self.all_shapes) + 1
            shape.update_properties_dict()

            if not hasattr(self, 'all_progressbar_dicts'):
                self.all_progressbar_dicts = {}
            self.all_progressbar_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Scroll bar":
            shape = ScrollBarWidget(150, 10, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "ScrollBar")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_scrollbar_dicts'):
                self.all_scrollbar_dicts = {}
            self.all_scrollbar_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Dial":
            shape = DialWidget(80, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Dial")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_dial_dicts'):
                self.all_dial_dicts = {}
            self.all_dial_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Slider":
            shape = SliderWidget(200, 50, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Slider")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_slider_dicts'):
                self.all_slider_dicts = {}
            self.all_slider_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Toggle":
            shape = ToggleWidget(80, 30, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Toggle")
            shape.stack_order = len(self.all_shapes) + 1
            shape.tag = generate_auto_tag(self, shape)

            if not hasattr(self, 'all_toggle_dicts'):
                self.all_toggle_dicts = {}
            self.all_toggle_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Label":
            shape = LabelWidget(100, 40, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Label")
            shape.stack_order = len(self.all_shapes) + 1

            if not hasattr(self, 'all_label_dicts'):
                self.all_label_dicts = {}
            self.all_label_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Image":
            shape = ImageWidget(100, 100, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Image")
            shape.stack_order = len(self.all_shapes) + 1

            if not hasattr(self, 'all_image_dicts'):
                self.all_image_dicts = {}
            self.all_image_dicts[shape.custom_name] = shape.get_properties_dict()

        elif self.selected_shape == "Keys":
            shape = KeysWidget(200, 120, widget_container)  # widget_container umesto self.canvas
            shape.move(container_pos.x() - shape.width() // 2, container_pos.y() - shape.height() // 2)
            shape.clicked.connect(self.select_shape)

            shape.custom_name = generateWidgetName(self, "Keys")
            shape.stack_order = len(self.all_shapes) + 1

            if not hasattr(self, 'all_keys_dicts'):
                self.all_keys_dicts = {}
            self.all_keys_dicts[shape.custom_name] = shape.get_properties_dict()

            shape.show()
            self.all_shapes.append(shape)
            self.update_widgets_z_order()
            self.select_shape(shape)
            QApplication.restoreOverrideCursor()
            self.object_attached = False
            self.selected_shape = None
            return

        if shape:
            if self.all_shapes:
                max_stack_order = max([s.stack_order for s in self.all_shapes])
                shape.stack_order = max_stack_order + 1
            else:
                shape.stack_order = 1

            shape.show()
            shape.raise_()  # Podigni widget na vrh
            self.all_shapes.append(shape)
            self.sort_widgets_by_stack_order()
            self.select_shape(shape)
            QApplication.restoreOverrideCursor()
            self.object_attached = False
            self.selected_shape = None

    def update_widgets_z_order(self):
        """Sortira widget-e po stack_order i postavlja odgovarajući Z-order"""
        sorted_widgets = sorted(self.all_shapes, key=lambda x: x.stack_order)

        for widget in sorted_widgets:
            widget.lower()

        for widget in sorted_widgets:
            widget.raise_()

    def show_shape_properties(self):
        self.hide_shape_properties()
        self.hide_canvas_properties()
        
        # Obriši sve postojeće stack_order spinbox-ove
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

        # Dodaj naslov za propertije
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

        # Prikaži specifične propertije za svaki widget
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
            current_index = showScrollBarProperties(self, current_index)
        elif isinstance(self.current_shape, DialWidget):
            current_index = showDialProperties(self, current_index)
        elif isinstance(self.current_shape, SliderWidget):
            current_index = showSliderProperties(self, current_index)
        elif isinstance(self.current_shape, ToggleWidget):
            current_index = showToggleProperties(self, current_index)
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

    def update_stack_order(self, value):
        """Ažurira stack_order selektovanog widget-a i sortira widget-e"""
        if self.current_shape:
            self.current_shape.stack_order = value
            self.sort_widgets_by_stack_order()

    def sort_widgets_by_stack_order(self):
        """Sortira widget-e po stack_order"""
        if not self.all_shapes:
            return
    
        sorted_widgets = sorted(self.all_shapes, key=lambda x: x.stack_order)
    
        for widget in self.all_shapes:
            widget.lower()
    
        for widget in sorted_widgets:
            widget.raise_()
    
        # Debug ispis
        print(f"\n[MainWindow] Z-order (od donjeg ka gornjem):")
        for i, widget in enumerate(sorted_widgets):
            widget_name = widget.custom_name if hasattr(widget, 'custom_name') else 'Unknown'
            print(f"  {i+1}. {widget_name}: stack_order={widget.stack_order}")

    def update_shape_position(self):
        if self.current_shape:
            self.current_shape.move(self.pos_x_spin.value(), self.pos_y_spin.value())

    def change_shape_color(self):
        if (self.current_shape and not isinstance(self.current_shape, (GaugeWidget, ClockWidget, ProgressBarWidget))):
            if hasattr(self.current_shape, 'color'):
                current_color = self.current_shape.color
            elif hasattr(self.current_shape, 'line_color'):
                current_color = self.current_shape.line_color
            else:
                return

            color = QColorDialog.getColor(current_color)
            if color.isValid():
                self.current_shape.set_color(color)
                self.color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")

    def update_shape_border_width(self):
        if (self.current_shape and not isinstance(self.current_shape, (GaugeWidget, ClockWidget, ProgressBarWidget)) and 
            hasattr(self.current_shape, 'set_border_width')):
            self.current_shape.set_border_width(self.border_width_spin.value())

    def set_tag(self, tag_value):
        """Postavlja tag vrednost za widget"""
        self.tag = tag_value
        self.update_properties_dict()

        # Ažuriraj odgovarajući rečnik u MainWindow
        main_window = self._find_main_window()
        if main_window:
            if isinstance(self, RectangleWidget) and hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, CircleWidget) and hasattr(main_window, 'all_circle_dicts'):
                main_window.all_circle_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, LineWidget) and hasattr(main_window, 'all_line_dicts'):
                main_window.all_line_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, ButtonWidget) and hasattr(main_window, 'all_button_dicts'):
                main_window.all_button_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, EllipseWidget) and hasattr(main_window, 'all_ellipse_dicts'):
                main_window.all_ellipse_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, DialWidget) and hasattr(main_window, 'all_dial_dicts'):
                main_window.all_dial_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, ScrollBarWidget) and hasattr(main_window, 'all_scroll_bar_dicts'):
                main_window.all_scroll_bar_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, SliderWidget) and hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[self.custom_name] = self.get_properties_dict()
            elif isinstance(self, ToggleWidget) and hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[self.custom_name] = self.get_properties_dict()

    def print_all_widget_dicts(self):
        """Ispisuje sve rečnike za sve widget-e"""
        print("\n" + "="*60)
        print("              COMPLETE WIDGET REPORT")
        print("="*60)
        
        widgets_by_type = {}
        for shape in self.all_shapes:
            widget_type = type(shape).__name__
            if widget_type not in widgets_by_type:
                widgets_by_type[widget_type] = []
            widgets_by_type[widget_type].append(shape)
        
        for widget_type, widgets in widgets_by_type.items():
            print(f"\n{'='*30}")
            print(f"{widget_type.upper()}S ({len(widgets)})")
            print('='*30)
            for i, widget in enumerate(widgets, 1):
                print(f"{widget.custom_name}:")
                if hasattr(widget, 'get_properties_dict'):
                    props = widget.get_properties_dict()
                    for key, value in props.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  Position: ({widget.x()}, {widget.y()})")
                    print(f"  Size: {widget.width()}x{widget.height()}")
                    if hasattr(widget, 'custom_name'):
                        print(f"  Name: {widget.custom_name}")
        
        print("\n" + "="*60)
        print(f"TOTAL WIDGETS: {len(self.all_shapes)}")
        print("="*60 + "\n")


if __name__ == "__main__":
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