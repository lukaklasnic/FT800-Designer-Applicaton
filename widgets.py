from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QFrame, QColorDialog, QMainWindow
from PyQt6.QtCore import Qt, QPoint, QRect, QPointF, pyqtSignal, QSize, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QLinearGradient, QFont, QBrush, QPixmap,  QCursor, QPalette, QFontMetrics
import math

class Widget_icon(QFrame):
    def __init__(self, shape):
        super().__init__()
        self.setFixedSize(100, 100)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.shape = shape

        self.setAutoFillBackground(True)
        self.default_color = QColor(0, 0, 0, 0)
        self.hover_color = QColor(202, 230, 232, 255)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self.default_color)
        self.setPalette(palette)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            main_window = self.window()
            if getattr(main_window, "object_attached", False):
                QApplication.restoreOverrideCursor()
                main_window.object_attached = False
                main_window.selected_shape = None
            else:
                self._create_custom_cursor()
                main_window.object_attached = True
                main_window.selected_shape = self.shape

    def _create_custom_cursor(self):
        pix = QPixmap(100, 100)
        pix.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix)
        painter.setPen(QPen(QColor(150, 202, 232), 2))
        
        cursor_actions = {
            "Line": lambda: painter.drawLine(10, 10, 80, 80),
            "Circle": lambda: painter.drawEllipse(QPoint(50, 50), 50, 50),
            "Gauge": lambda: painter.drawEllipse(QPoint(50, 45), 25, 25),
            "Clock": lambda: painter.drawEllipse(QPoint(50, 50), 50, 50),
            "Dial": lambda: painter.drawEllipse(QPoint(50, 45), 25, 25),
            "Rectangle": lambda: painter.drawRect(0, 0, 60, 50),
            "Image": lambda: painter.drawRect(0, 0, 60, 50),
            "Progress bar": lambda: painter.drawRoundedRect(0, 0, 60, 10, 3, 3),
            "Scroll bar": lambda: painter.drawRoundedRect(0, 0, 60, 10, 3, 3),
            "Slider": lambda: painter.drawRoundedRect(0, 0, 60, 10, 3, 3),
            "Button": lambda: painter.drawRoundedRect(0, 0, 100, 50, 5, 5),
            "Toggle": lambda: painter.drawRoundedRect(0, 0, 40, 20, 10, 10),
            "Label": lambda: painter.drawRect(0, 0, 50, 20),
            "Keys": lambda: painter.drawRect(0, 0, 40, 40),
            "Numeric":lambda: painter.drawRect(0, 0, 50, 50),
            "Ellipse":lambda: painter.drawEllipse(QPoint(50, 50), 48, 38),
        }
        
        if self.shape in cursor_actions:
            cursor_actions[self.shape]()
        
        painter.end()
        QApplication.setOverrideCursor(QCursor(pix, 16, 16))

    def enterEvent(self, event):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self.hover_color)
        self.setPalette(palette)
        super().enterEvent(event)

    def leaveEvent(self, event):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self.default_color)
        self.setPalette(palette)
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)  
        painter = QPainter(self)
        pen = QPen(QColor(255, 255, 255))
        font = QFont("Arial", 10, QFont.Weight.Normal)  
        painter.setFont(font)
        painter.setPen(pen)
        
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, self.shape)
        
        shape_drawers = {
            "Button": self._draw_button,
            "Line": self._draw_line,
            "Rectangle": self._draw_rectangle,
            "Circle": self._draw_circle,
            "Keys": self._draw_keys,
            "Gauge": self._draw_gauge,
            "Clock": self._draw_clock,
            "Progress bar": self._draw_progress_bar,
            "Scroll bar": self._draw_scroll_bar,
            "Dial": self._draw_dial,
            "Slider": self._draw_slider,
            "Toggle": self._draw_toggle,
            "Label": self._draw_label,
            "Image": self._draw_image,
            "Numeric":self._draw_numeric,
            "Ellipse":self._draw_ellipse
        }
        
        if self.shape in shape_drawers:
            shape_drawers[self.shape](painter)

    def _draw_button(self, painter):
        painter.drawRoundedRect(20, 30, 60, 30, 5, 5)
        rect = QRect(20, 30, 60, 30)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Press")

    def _draw_line(self, painter):
        painter.drawLine(20, 20, 80, 60)

    def _draw_rectangle(self, painter):
        painter.drawRect(20, 20, 60, 50)

    def _draw_circle(self, painter):
        painter.drawEllipse(QPoint(50, 45), 25, 25)

    def _draw_keys(self, painter):
        x, y = 25, 20
        for i in range(2):
            for j in range(4):
                painter.drawRoundedRect(x, y, 10, 10, 1, 1)
                x += 13
            x = 25
            y += 13
        painter.drawRoundedRect(30, 47, 40, 10, 1, 1)

    def _draw_gauge(self, painter):
        painter.drawEllipse(QPoint(50, 45), 20, 20)
        painter.translate(50, 45)
        painter.rotate(-135)
        for i in range(6):  
            painter.drawLine(0, -15, 0, -12)
            painter.rotate(54)
        painter.drawLine(0, 0, 14, 10)

    def _draw_clock(self, painter):
        painter.drawEllipse(QPoint(50, 45), 20, 20)
        painter.translate(50, 45)
        for i in range(12):  
            painter.drawPoint(0, -15)
            painter.rotate(30)
        
        painter.rotate(55) 
        needle_pen = QPen(QColor(236, 238, 241))
        needle_pen.setWidth(1)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, -2, 15) 
        
        painter.rotate(-55)
        needle_pen.setWidth(2)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, 4, -13)
        
        painter.rotate(-55)
        needle_pen.setWidth(3)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, -10, -11)

    def _draw_progress_bar(self, painter):
        painter.drawLine(25, 40, 75, 40)
        painter.drawLine(25, 50, 75, 50)
        painter.drawLine(60, 40, 60, 50)
        painter.drawArc(20, 40, 10, 10, 90*16, 16*180)
        painter.drawArc(70, 40, 10, 10, 90*16, -16*180)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawPie(22, 42, 6, 6, 90*16, 16*180)
        painter.drawRect(25, 42, 35, 6)

    def _draw_scroll_bar(self, painter):
        painter.drawLine(25, 40, 75, 40)
        painter.drawLine(25, 50, 75, 50)
        painter.drawArc(20, 40, 10, 10, 90*16, 16*180)
        painter.drawArc(70, 40, 10, 10, 90*16, -16*180)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(30, 42, 20, 6)
        painter.drawPie(27, 42, 6, 6, 90*16, 16*180)
        painter.drawPie(47, 42, 6, 6, 90*16, -16*180)

    def _draw_dial(self, painter):
        painter.drawEllipse(QPoint(50, 40), 20, 20)
        painter.drawLine(50, 25, 50, 30)

    def _draw_slider(self, painter):
        painter.drawLine(20, 42, 80, 42)
        painter.drawLine(20, 48, 80, 48)
        painter.drawArc(15, 42, 6, 6, 90*16, 16*180)
        painter.drawArc(75, 42, 6, 6, 90*16, -16*180)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(QPoint(50, 45), 6, 6)

    def _draw_toggle(self, painter):
        painter.drawLine(35, 40, 65, 40)
        painter.drawLine(35, 60, 65, 60)
        painter.drawArc(25, 40, 20, 20, 90*16, 16*180)
        painter.drawArc(55, 40, 20, 20, 90*16, -16*180)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(QPoint(63, 50), 8, 8)
        rect = QRect(25, 40, 30, 20)
        painter.setFont(QFont("Arial", 8, QFont.Weight.Normal))
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter, "ON")

    def _draw_label(self, painter):
        painter.drawLine(20, 40, 65, 40)
        painter.drawLine(20, 60, 65, 60)
        painter.drawLine(20, 40, 20, 60)
        painter.drawLine(65, 40, 80, 50)
        painter.drawLine(65, 60, 80, 50)
        painter.setFont(QFont("Arial", 8, QFont.Weight.Normal))
        rect = QRect(30, 40, 30, 20)
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter, "Text")

    def _draw_image(self, painter):
        painter.drawRoundedRect(25, 20, 50, 50, 5, 5)
        painter.drawLine(27, 68, 45, 45)
        painter.drawLine(45, 45, 65, 70)
        painter.drawLine(55, 55, 65, 45)
        painter.drawLine(65, 45, 75, 58)
        painter.drawArc(15, 10, 25, 25, 0*16, -16*90)
        painter.translate(25, 20)
        painter.rotate(110)
        for i in range(3):  
            painter.drawLine(0, -20, 0, -17)
            painter.rotate(25)
    def _draw_numeric( self, painter):
        rect = QRect(25, 20, 50, 50)
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter, "123")
        painter.drawRoundedRect(rect, 5, 5)
    def _draw_ellipse( self, painter):
        painter.drawEllipse(QPoint(50, 45), 35, 25)


class ColorRectangle( QLabel ):
    
    def __init__( self, initial_color = "white" ):
        super().__init__()
        self._color = initial_color
        self.setFixedSize( 20, 20 )
        self.update_display()
        self.setCursor( Qt.CursorShape.PointingHandCursor )
        
        
    def update_display( self ):
        self.setStyleSheet( f"background-color: {self._color}; border: 1px solid #ccc;" )
        
    @property
    def color( self ):
        return self._color
        
    @color.setter
    def color( self, value ):
        self._color = value
        self.update_display()
        
    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            new_color = QColorDialog.getColor( QColor( self._color ) )
            if new_color.isValid():
                self._color = new_color.name()
                self.update_display()
                if hasattr( self, 'colorChanged' ):
                    self.colorChanged.emit( self._color )
        super().mousePressEvent( event )

class RectangleWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, w=100, h=80, parent=None):
        super().__init__(parent)
        self.setFixedSize(w, h)
        
        # Svojstva
        self.color = QColor(0, 0, 0)  # Boja ivica
        self.is_selected = False
        
        # Resize i drag varijable
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        # Novi atributi
        self.border_width = 3
        self.filled = False  # Da li je ispunjen
        self.fill_color = QColor(200, 200, 200)  # BOJA ZA ISPUNU
        
        # Gradient atributi
        self.gradient_enabled = True  # Po default-u gradijent je enabled
        self.gradient_color1 = QColor(255, 0, 0)
        self.gradient_color2 = QColor(0, 0, 255)
        self.gradient_direction = "top_to_bottom"  # Podrazumevani smer
        
        # DODAJTE OVE ATRIBUTE ZA PROPERTIES
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        
        # Postavi atribute za mouse events
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Ako je filled (ispunjen)
        if self.filled:
            # Ako je gradijent omogućen, iscrtaj gradijentnu pozadinu
            if self.gradient_enabled:
                gradient = None
                
                # Definiši gradijent na osnovu smera
                if self.gradient_direction == "top_to_bottom":
                    gradient = QLinearGradient(0, 0, 0, self.height())
                elif self.gradient_direction == "bottom_to_top":
                    gradient = QLinearGradient(0, self.height(), 0, 0)
                elif self.gradient_direction == "left_to_right":
                    gradient = QLinearGradient(0, 0, self.width(), 0)
                elif self.gradient_direction == "right_to_left":
                    gradient = QLinearGradient(self.width(), 0, 0, 0)
                
                if gradient:
                    gradient.setColorAt(0, self.gradient_color1)
                    gradient.setColorAt(1, self.gradient_color2)
                    painter.fillRect(self.rect(), gradient)
                else:
                    # Fallback ako gradijent nije definisan
                    painter.fillRect(self.rect(), self.gradient_color1)
            else:
                # Ako nije gradijent, ispuni običnom bojom
                painter.fillRect(self.rect(), self.fill_color)
        
        # Nacrtaj ivice
        pen = QPen(self.color)
        pen.setWidth(self.border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(0, 0, self.width() , self.height() )
        
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.is_selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima"""
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi sa tamnijim okvirom
        painter.setBrush(QColor(0, 255, 0))  # Zeleno
        painter.setPen(QPen(QColor(0, 80, 200), 1))  # Tamno plavi okvir

        # 4 ugla - za pravougaonik, to su uglovi pravougaonika
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Dodajte mali beli centar za bolju vidljivost
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))  # Vratite boju
            painter.setPen(QPen(QColor(0, 80, 200), 1))  # Vratite okvir

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira oko selektovanog rectangle-a sa razmakom"""
        margin = 2  # Razmak od rectangle-a
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        # Crvena boja za selekcioni okvir
        selection_pen = QPen(QColor(255, 0, 0))  # Crvena boja
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])  # Dužina crte: 4px, razmak: 2px

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit(self)

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            # Koristite dva argumenta (x, y) umesto QPoint
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            self.move(new_x, new_y)
            
            # Ažuriraj properties bar ako postoji
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar
            self._update_properties_size()
            self._update_properties_position()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Jednostavnija verzija - menja samo veličinu, ne poziciju"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu (slično kao ButtonWidget)
        if self.resize_corner == "bottom_right":
            new_width = max(20, self.resize_start_size.width() + delta.x())
            new_height = max(20, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(20, self.resize_start_size.width() + delta.x())
            new_height = max(20, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(20, self.resize_start_size.width() - delta.x())
            new_height = max(20, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(20, self.resize_start_size.width() - delta.x())
            new_height = max(20, self.resize_start_size.height() - delta.y())

        # Ažuriraj samo veličinu (bez promene pozicije)
        self.setFixedSize(new_width, new_height)
        self.update()

        # Ažuriraj properties bar
        self._update_properties_size()

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'width_spin_rect') and 
            hasattr(main_window, 'height_spin_rect')):
            
            main_window.width_spin_rect.setValue(self.width())
            main_window.height_spin_rect.setValue(self.height())

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'pos_x_spin_rect') and 
            hasattr(main_window, 'pos_y_spin_rect')):
            
            main_window.pos_x_spin_rect.setValue(self.x())
            main_window.pos_y_spin_rect.setValue(self.y())

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def get_properties_dict(self):
        """Vraća rečnik sa svim properties-ima rectangle-a"""
        return {
            'type': 'Rectangle',
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'name': self.custom_name,
            'stack_order': self.stack_order,
            'x': self.x(),
            'y': self.y(),
            'width': self.width(),
            'height': self.height(),
            'edges_color': self.color.name(),
            'thickness': self.border_width,
            'filled': self.filled,
            'gradient_enabled': self.gradient_enabled,
            'gradient_direction': self.gradient_direction,
            'gradient_start_color': self.gradient_color1.name(),
            'gradient_end_color': self.gradient_color2.name(),
            'fill_color': self.fill_color.name()
        }
    
    def update_properties_dict(self):
        """Ažurira properties rečnik - placeholder za konzistentnost"""
        pass
    
    def set_selected(self, selected):
        self.is_selected = selected
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def set_border_width(self, width):
        self.border_width = width
        self.update()
    
    def set_filled(self, filled):
        self.filled = filled
        self.update()
    
    def set_gradient_color1(self, color):
        self.gradient_color1 = color
        self.update()
    
    def set_gradient_color2(self, color):
        self.gradient_color2 = color
        self.update()
    
    def set_gradient_direction(self, direction):
        self.gradient_direction = direction
        self.update()
    
    def set_fill_color(self, color):
        self.fill_color = color
        if not self.gradient_enabled:
            self.update()
    
    def set_active(self, active):
        self.active = active
        self.update()
    
    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()
    
    def set_static(self, static):
        self.static = static
        self.update()
    
    def set_custom_name(self, name):
        self.custom_name = name
    
    def set_stack_order(self, order):
        self.stack_order = order
        
    # Dodajte metode za move i resize da ažuriraju properties dict
    def move(self, x, y):
        super().move(x, y)
        # Ažuriraj properties bar
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            if hasattr(main_window, 'pos_x_spin_rect'):
                main_window.pos_x_spin_rect.blockSignals(True)
                main_window.pos_x_spin_rect.setValue(x)
                main_window.pos_x_spin_rect.blockSignals(False)
            if hasattr(main_window, 'pos_y_spin_rect'):
                main_window.pos_y_spin_rect.blockSignals(True)
                main_window.pos_y_spin_rect.setValue(y)
                main_window.pos_y_spin_rect.blockSignals(False)

    def resize(self, width, height):
        super().resize(width, height)
        # Ažuriraj properties bar
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            if hasattr(main_window, 'width_spin_rect'):
                main_window.width_spin_rect.blockSignals(True)
                main_window.width_spin_rect.setValue(width)
                main_window.width_spin_rect.blockSignals(False)
            if hasattr(main_window, 'height_spin_rect'):
                main_window.height_spin_rect.blockSignals(True)
                main_window.height_spin_rect.setValue(height)
                main_window.height_spin_rect.blockSignals(False)
class LineWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Početne koordinate linije (globalne)
        self._start_x = 0
        self._start_y = 0
        self._end_x = 100
        self._end_y = 100
        
        # Debljina linije
        self.line_width = 10
        
        # Boja linije
        self.line_color = QColor(255, 0, 0)  # Crvena boja
        
        # Dodatna svojstva (kao kod drugih widget-a)
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.selected = False
        
        # Resize i drag varijable (kao kod drugih widget-a)
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_points = None
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        # Ažuriraj veličinu widgeta bazirano na koordinatama
        self._update_widget_size()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.stack_order = 1
    
    def _update_widget_size(self):
        """Ažurira veličinu widgeta bazirano na koordinatama linije"""
        margin = 20  # Margin za selekcioni okvir i handle-ove
        
        # Pronađi min i max koordinate
        min_x = min(self._start_x, self._end_x) - self.x()
        min_y = min(self._start_y, self._end_y) - self.y()
        max_x = max(self._start_x, self._end_x) - self.x()
        max_y = max(self._start_y, self._end_y) - self.y()
        
        # Postavi veličinu widgeta sa marginom
        width = max(20, max_x - min_x) + 2 * margin
        height = max(20, max_y - min_y) + 2 * margin
        
        self.setFixedSize(width, height)
        
        # Ako se veličina promenila, ažuriraj poziciju
        self._update_position()
    
    def _update_position(self):
        """Ažurira poziciju widgeta da centrira liniju"""
        margin = 20
        
        # Pronađi centar linije
        center_x = (self._start_x + self._end_x) // 2
        center_y = (self._start_y + self._end_y) // 2
        
        # Pomeri widget da centrira liniju
        self.move(center_x - self.width() // 2, center_y - self.height() // 2)
    
    def set_line_points(self, start_x, start_y, end_x, end_y):
        """Postavlja globalne koordinate linije"""
        self._start_x = start_x
        self._start_y = start_y
        self._end_x = end_x
        self._end_y = end_y
        
        # Ažuriraj veličinu i poziciju widgeta
        self._update_widget_size()
        self.update()
    
    def get_line_points(self):
        """Vraća globalne koordinate linije"""
        return (self._start_x, self._start_y, self._end_x, self._end_y)
    
    def set_line_width(self, width):
        """Postavlja debljinu linije"""
        self.line_width = max(1, width)
        self.update()
    
    def set_line_color(self, color):
        """Postavlja boju linije"""
        self.line_color = color
        self.update()
    
    def set_selected(self, selected):
        """Postavlja selektovani status"""
        self.selected = selected
        self.update()
    
    def set_visible(self, visible):
        """Postavlja visible status"""
        self.visible = visible
        self.setVisible(visible)
        self.update()
    
    # Metode za resize i drag (slične drugim widget-ima ali sa tačkama linije)
    
    def _get_point_at(self, pos):
        """Proverava da li je miš preko tačaka linije za resize"""
        handle_size = 16
        
        # Globalne koordinate miša
        global_pos = QPoint(pos.x() + self.x(), pos.y() + self.y())
        
        # Proveri početnu tačku
        start_rect = QRect(self._start_x - handle_size//2, self._start_y - handle_size//2,
                          handle_size, handle_size)
        if start_rect.contains(global_pos):
            return "start"
        
        # Proveri krajnju tačku
        end_rect = QRect(self._end_x - handle_size//2, self._end_y - handle_size//2,
                        handle_size, handle_size)
        if end_rect.contains(global_pos):
            return "end"
        
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            
            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_point_at(mouse_pos)
            
            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_points = (self._start_x, self._start_y, self._end_x, self._end_y)
            else:
                # Proveri da li je klik na liniju
                if self._is_point_on_line(mouse_pos):
                    # Počni dragovanje
                    self.dragging = True
                    self.drag_start_pos = mouse_pos
                
                self.clicked.emit(self)
                # Ažuriraj properties kada se selektuje
                self.update_all_properties()

        event.accept()
    
    def _is_point_on_line(self, pos):
        """Proverava da li je tačka na liniji (za selekciju)"""
        # Konvertuj u globalne koordinate
        global_x = pos.x() + self.x()
        global_y = pos.y() + self.y()
        
        # Računaj udaljenost od linije
        import math
        
        x1, y1, x2, y2 = self._start_x, self._start_y, self._end_x, self._end_y
        
        # Ako su tačke iste, proveri samo udaljenost od tačke
        if x1 == x2 and y1 == y2:
            distance = math.sqrt((global_x - x1)**2 + (global_y - y1)**2)
            return distance <= self.line_width / 2 + 5
        
        # Računaj udaljenost od linije
        A = global_x - x1
        B = global_y - y1
        C = x2 - x1
        D = y2 - y1
        
        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1
        
        if len_sq != 0:
            param = dot / len_sq
        
        if param < 0:
            xx, yy = x1, y1
        elif param > 1:
            xx, yy = x2, y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D
        
        distance = math.sqrt((global_x - xx)**2 + (global_y - yy)**2)
        
        return distance <= self.line_width / 2 + 5
    
    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        point = self._get_point_at(mouse_pos)
        if point:
            self.setCursor(Qt.CursorShape.SizeAllCursor)
        elif self._is_point_on_line(mouse_pos):
            self.setCursor(Qt.CursorShape.SizeAllCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
            self._update_properties_points()
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje cele linije
            delta = mouse_pos - self.drag_start_pos
            
            # Pomeri obe tačke linije
            self._start_x += delta.x()
            self._start_y += delta.y()
            self._end_x += delta.x()
            self._end_y += delta.y()
            
            # Ažuriraj poziciju widgeta
            self._update_position()
            
            # Resetuj drag start position za sledeći frame
            self.drag_start_pos = mouse_pos
            
            self.update()
            self._update_properties_points()
        
        event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None
            self.resize_start_points = None
            
            self.update_properties_dict()

        event.accept()
    
    def _handle_resize(self, global_pos):
        """Menja poziciju tačke linije"""
        if not self.resize_corner or not self.resize_start_points:
            return

        # Računaj promenu u poziciji
        delta = global_pos - self.resize_start_pos
        
        start_x_start, start_y_start, end_x_start, end_y_start = self.resize_start_points
        
        if self.resize_corner == "start":
            # Pomeraj početnu tačku
            self._start_x = start_x_start + delta.x()
            self._start_y = start_y_start + delta.y()
        elif self.resize_corner == "end":
            # Pomeraj krajnju tačku
            self._end_x = end_x_start + delta.x()
            self._end_y = end_y_start + delta.y()
        
        # Ažuriraj veličinu i poziciju widgeta
        self._update_widget_size()
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Konvertuj globalne koordinate u lokalne
        local_start_x = self._start_x - self.x()
        local_start_y = self._start_y - self.y()
        local_end_x = self._end_x - self.x()
        local_end_y = self._end_y - self.y()
        
        # Nacrtaj liniju
        pen = QPen(self.line_color)
        pen.setWidth(self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(local_start_x, local_start_y, local_end_x, local_end_y)
        
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter, local_start_x, local_start_y, local_end_x, local_end_y)
    
    def _draw_selection_handles(self, painter, start_x, start_y, end_x, end_y):
        """Crtanje resize handle-ova na tačkama linije"""
        handle_size = 12
        half_size = handle_size // 2
        
        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))
        
        # Handle na početnoj tački
        painter.drawEllipse(start_x - half_size, start_y - half_size, 
                           handle_size, handle_size)
        
        # Handle na krajnjoj tački
        painter.drawEllipse(end_x - half_size, end_y - half_size, 
                           handle_size, handle_size)
        
        # Mali beli centri
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        
        painter.drawEllipse(start_x - 1, start_y - 1, 2, 2)
        painter.drawEllipse(end_x - 1, end_y - 1, 2, 2)
    
    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira oko linije"""
        margin = 10
        
        # Pronađi lokalne koordinate tačaka
        local_start_x = self._start_x - self.x()
        local_start_y = self._start_y - self.y()
        local_end_x = self._end_x - self.x()
        local_end_y = self._end_y - self.y()
        
        min_x = min(local_start_x, local_end_x) - margin
        min_y = min(local_start_y, local_end_y) - margin
        max_x = max(local_start_x, local_end_x) + margin
        max_y = max(local_start_y, local_end_y) + margin
        
        border_rect = QRect(min_x, min_y, max_x - min_x, max_y - min_y)
        
        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(2)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])
        
        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)
    
    # Metode za properties bar
    
    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None
    
    def _update_properties_points(self):
        """Ažuriraj tačke linije u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            if hasattr(main_window, 'start_x_spin_line'):
                main_window.start_x_spin_line.blockSignals(True)
                main_window.start_x_spin_line.setValue(self._start_x)
                main_window.start_x_spin_line.blockSignals(False)
                
            if hasattr(main_window, 'start_y_spin_line'):
                main_window.start_y_spin_line.blockSignals(True)
                main_window.start_y_spin_line.setValue(self._start_y)
                main_window.start_y_spin_line.blockSignals(False)
                
            if hasattr(main_window, 'end_x_spin_line'):
                main_window.end_x_spin_line.blockSignals(True)
                main_window.end_x_spin_line.setValue(self._end_x)
                main_window.end_x_spin_line.blockSignals(False)
                
            if hasattr(main_window, 'end_y_spin_line'):
                main_window.end_y_spin_line.blockSignals(True)
                main_window.end_y_spin_line.setValue(self._end_y)
                main_window.end_y_spin_line.blockSignals(False)
    
    def update_all_properties(self):
        """Ažurira sve properties u properties baru"""
        self._update_properties_points()
        
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj checkbox-ove
            if hasattr(main_window, 'active_checkbox_line'):
                main_window.active_checkbox_line.blockSignals(True)
                main_window.active_checkbox_line.setChecked(self.active)
                main_window.active_checkbox_line.blockSignals(False)
                
            if hasattr(main_window, 'visible_checkbox_line'):
                main_window.visible_checkbox_line.blockSignals(True)
                main_window.visible_checkbox_line.setChecked(self.visible)
                main_window.visible_checkbox_line.blockSignals(False)
                
            if hasattr(main_window, 'static_checkbox_line'):
                main_window.static_checkbox_line.blockSignals(True)
                main_window.static_checkbox_line.setChecked(self.static)
                main_window.static_checkbox_line.blockSignals(False)
            
            # Ažuriraj ime
            if hasattr(main_window, 'name_edit_line'):
                main_window.name_edit_line.blockSignals(True)
                main_window.name_edit_line.setText(self.custom_name)
                main_window.name_edit_line.blockSignals(False)
            
            # Ažuriraj stack order
            if hasattr(main_window, 'stack_order_spin_line'):
                main_window.stack_order_spin_line.blockSignals(True)
                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index(main_window.current_shape) + 1
                    main_window.stack_order_spin_line.setValue(index)
                main_window.stack_order_spin_line.blockSignals(False)
            
            # Ažuriraj boju
            if hasattr(main_window, 'color_rect_line'):
                main_window.color_rect_line.setStyleSheet(
                    f"background-color: {self.line_color.name()}; border: 1px solid #ccc;"
                )
            
            # Ažuriraj debljinu
            if hasattr(main_window, 'line_width_spin_line'):
                main_window.line_width_spin_line.blockSignals(True)
                main_window.line_width_spin_line.setValue(self.line_width)
                main_window.line_width_spin_line.blockSignals(False)
    
    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima linije"""
        return {
            'type': 'Line',
            'name': getattr(self, 'custom_name', 'Line_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'start_x': self._start_x,
            'start_y': self._start_y,
            'end_x': self._end_x,
            'end_y': self._end_y,
            'line_width': self.line_width,
            'color': self.line_color.name(),
            'active': getattr(self, 'active', True),
            'visible': getattr(self, 'visible', True),
            'static': getattr(self, 'static', False)
        }
    
    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        main_window = self._find_main_window()
        if not main_window:
            return
            
        if hasattr(main_window, 'all_line_dicts'):
            if self.custom_name in main_window.all_line_dicts:
                main_window.all_line_dicts[self.custom_name] = self.get_properties_dict()

class CircleWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, diameter, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        
        self.line_color = QColor(255, 0, 0)
        self.line_thickness = 2
        self.is_selected = False
        
        # DVA ATRIBUTA UMESTO JEDNOG SA ALPHA
        self.fill_color = QColor(0, 255, 0)  # BEZ ALPHA KANALA
        self.filled = False  # NOVI ATRIBUT - da li je popunjen ili ne
        
        # Atributi za properties
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.center_x = 0
        self.center_y = 0
        
        # Interakcija
        self.dragging = False
        self.drag_start_position = QPoint()
        self.resizing = False
        self.resize_corner = None
        self.resize_start_pos = QPoint()
        self.resize_start_diameter = 0
        
        self.setMouseTracking(True)
        
        # Rečnik za properties
        self.properties_dict = {}
        self.update_properties_dict()
        self.stack_order = 1
        
    def paintEvent(self, event):
        if not self.visible:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Oduzmi polovinu debljine linije da se ne bi secala
        line_half = self.line_thickness // 2

        # Kreiraj pravougaonik za krug sa uračunatom debljinom linije
        rect_size = min(self.width(), self.height()) - self.line_thickness

        # Centriraj krug
        x_offset = (self.width() - rect_size) // 2
        y_offset = (self.height() - rect_size) // 2

        # Kreiraj pravougaonik sa padding-om za liniju
        circle_rect = QRectF(x_offset, y_offset, rect_size, rect_size)

        # Popuna
        # Popuna - SAMO AKO JE FILLED = TRUE
        if self.filled:  # PROVERA NA OSNOVU BOOLEAN
            painter.setBrush(self.fill_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(circle_rect)

        # Ivica
        pen = QPen(self.line_color, self.line_thickness)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(circle_rect)

        # Selekcija
        if self.is_selected:
            # Crtaj pravougaonik oko kruga kada je selektovan
            selection_rect = QRectF(2, 2, self.width()-4, self.height()-4)
            painter.setPen(QPen(QColor(255, 0, 0), 3, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(selection_rect)
            
            # Crtaj handle-ove
            self._draw_selection_handles(painter)

    def _draw_selection_handles(self, painter):
        """Crtanje handle-ova za selektovani krug"""
        handle_size = 8
        half_handle = handle_size // 2

        # ZELENE TAČKE SA TAMNO PLAVIM OKVIROM
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 255, 0), 1))

        # 4 UGLA
        points = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(self.width()-4, self.height()-4),  # donji desni
            QPoint(4, self.height()-4),  # donji levi
        ]

        for point in points:
            # KORISTITE ELIPSE ZA OKRUGLE TAČKE
            painter.drawEllipse(point.x() - half_handle, point.y() - half_handle,
                              handle_size, handle_size)

            # DODAJTE MALI BELI CENTAR
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(point.x() - 1, point.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 255, 0), 1))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_diameter = self.diameter
            else:
                # Počni dragovanje
                self.dragging = True
                self.drag_start_position = mouse_pos
                self.clicked.emit(self)

            event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_position
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            self.move(new_x, new_y)
            
            # Ažuriraj properties bar
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None
            self.resize_start_diameter = 0

            # Ažuriraj properties
            self.update_properties_dict()
            self._update_properties_size()
            self._update_properties_position()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Resize circle widget-a"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        # Izračunaj novi dijametar
        if "right" in self.resize_corner:
            new_diameter = max(20, self.resize_start_diameter + delta.x())
        elif "left" in self.resize_corner:
            new_diameter = max(20, self.resize_start_diameter - delta.x())
        else:
            new_diameter = self.diameter

        # Postavi novi dijametar
        self.set_diameter(new_diameter)
        
        # Pomeri widget ako je resize sa leve strane
        if "left" in self.resize_corner:
            delta_x = self.resize_start_diameter - new_diameter
            self.move(self.x() + delta_x, self.y())
        
        # Pomeri widget ako je resize sa gornje strane
        if "top" in self.resize_corner:
            delta_y = self.resize_start_diameter - new_diameter
            self.move(self.x(), self.y() + delta_y)
        
        self.update()
        self._update_properties_size()

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return

        # PROVERA DA LI OBJEKAT JOŠ POSTOJI
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'width_spin') and 
            main_window.width_spin is not None):  # DODAJTE OVU PROVERU

            try:
                main_window.width_spin.setValue(self.diameter)
            except RuntimeError:
                # Objekt je obrisan, ignoriši
                pass

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return

        # PROVERE ZA SVAKI SPINBOX
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):

            if hasattr(main_window, 'pos_x_spin') and main_window.pos_x_spin is not None:
                try:
                    main_window.pos_x_spin.setValue(self.x())
                except RuntimeError:
                    pass
                
            if hasattr(main_window, 'pos_y_spin') and main_window.pos_y_spin is not None:
                try:
                    main_window.pos_y_spin.setValue(self.y())
                except RuntimeError:
                    pass
    def _find_main_window(self):
        """Pronađi glavni prozor"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    # PROPERTIES METODE
    def update_properties_dict(self):
        """Ažurira rečnik sa svojstvima"""
        self.properties_dict = {
            'type': 'Circle',
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'name': self.custom_name,
            'x': self.x(),
            'y': self.y(),
            'width': self.diameter,
            'height': self.diameter,
            'diameter': self.diameter,
            'line_color': self.line_color.name(),
            'line_thickness': self.line_thickness,
            'filled': self.filled,  # BOOLEAN, NE ALPHA
            'fill_color': self.fill_color.name(),
        }

    
    def get_properties_dict(self):
        """Vraća kopiju rečnika sa svojstvima"""
        self.update_properties_dict()  # Osveži vrednosti
        return self.properties_dict.copy()
    
    def set_filled(self, filled):
        """Postavlja da li je krug popunjen ili ne"""
        self.filled = filled
        self.update()
        self.update_properties_dict()

    def set_fill_color(self, color):
        """Postavlja boju popune"""
        self.fill_color = color
        self.update()
        self.update_properties_dict()

    # SET METODE
    def set_selected(self, selected):
        self.is_selected = selected
        self.update()
    
    def set_active(self, active):
        self.active = active
        self.update_properties_dict()
    
    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update_properties_dict()
    
    def set_static(self, static):
        self.static = static
        self.update_properties_dict()
    
    def set_custom_name(self, name):
        self.custom_name = name
        self.update_properties_dict()
    
    def set_stack_order(self, order):
        self.stack_order = order
        self.update_properties_dict()
    
    def set_color(self, color):
        self.line_color = color
        self.update()
        self.update_properties_dict()
    
    
    def set_line_thickness(self, thickness):
        self.line_thickness = thickness
        self.update()
        self.update_properties_dict()
    
    def set_diameter(self, diameter):
        """Postavlja dijametar kruga i ažurira veličinu widgeta"""
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.update()
        self.update_properties_dict()
        
        # Obavesti glavni prozor
        main_window = self._find_main_window()
        if main_window and hasattr(main_window, 'all_circle_dicts') and self.custom_name:
            main_window.all_circle_dicts[self.custom_name] = self.get_properties_dict()
    
    def set_border_width(self, width):
        self.set_line_thickness(width)
    
    def update_center_position(self):
        """Ažurira poziciju centra kruga"""
        self.center_x = self.x() + self.width() // 2
        self.center_y = self.y() + self.height() // 2
        self.update_properties_dict()
    
    # KOMPATIBILNOST
    @property
    def color(self):
        return self.line_color
    
    @property
    def border_width(self):
        return self.line_thickness
    
    def set_gradient_enabled(self, enabled):
        pass
    
    def set_gradient_color1(self, color):
        pass
    
    def set_gradient_color2(self, color):
        pass
    
    def set_gradient_direction(self, direction):
        pass
    
    def move(self, x, y):
        super().move(x, y)
        self.update_properties_dict()
    
    def resize(self, width, height):
        super().resize(width, height)
        self.update_properties_dict()
    
class KeysWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width=200, height=120, parent=None):
        super().__init__(parent)
        
        # Početne dimenzije
        self._width = width
        self._height = height
        
        # Svojstva za keys
        self.key_type = "QUERTZ"  # QUERTZ ili NUM
        self.is_3d = True
        self.font_size = 12  # Dodajemo font size
        
        # Dimenzije pojedinačnih tastera
        self.key_width = 20
        self.key_height = 20
        
        # Boje
        self.key_color_top = QColor(0, 0, 255)  # Gornja boja gradijenta (Start Color)
        self.key_color_bottom = QColor(0, 0, 136)  # Donja boja gradijenta (End Color)
        self.text_color = QColor(255, 255, 255)  # Bela boja teksta (Font Color)
        self.border_color = QColor(0, 0, 0)  # Crni border
        
        # Dodatna svojstva (kao kod drugih widget-a)
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        
        # Selekcija
        self.selected = False
        
        # Postavi fiksnu veličinu
        self.setFixedSize(self._width, self._height)
        
        # Resize i drag varijable (kao kod drugih widget-a)
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.stack_order = 1
    
    def set_size(self, width, height):
        """Postavlja veličinu widgeta"""
        self._width = max(100, width)  # Minimum 100px
        self._height = max(80, height)  # Minimum 80px
        
        # Prilagodi dimenzije tastera na osnovu nove veličine
        self._adjust_key_dimensions()
        
        self.setFixedSize(self._width, self._height)
        self.update()
    
    def get_width(self):
        """Getter za width"""
        return self._width
    
    def get_height(self):
        """Getter za height"""
        return self._height
    
    def _adjust_key_dimensions(self):
        """Prilagođava dimenzije tastera na osnovu veličine widgeta"""
        if self.key_type == "NUM":
            # Za numeričku tastaturu (3x4 - dodajemo donji red sa 0 i .)
            self.key_width = max(15, self._width // 3 - 10)
            self.key_height = max(15, self._height // 4 - 8)  # 4 reda sada
        else:  # QUERTZ
            # Za QUERTZ tastaturu (najširi red ima 10 tastera)
            self.key_width = max(12, self._width // 10 - 6)
            self.key_height = max(15, self._height // 5 - 8)
    
    def set_key_type(self, key_type):
        """Postavlja tip tastature"""
        self.key_type = key_type
        self._adjust_key_dimensions()
        self.update()
    
    def set_3d(self, is_3d):
        """Postavlja 3D efekat"""
        self.is_3d = is_3d
        self.update()
    
    def set_font_size(self, size):
        """Postavlja veličinu fonta"""
        self.font_size = max(6, min(30, size))  # Ograniči na 6-30
        self.update()
    
    def set_key_colors(self, top_color, bottom_color):
        """Postavlja boje tastera (gradijent)"""
        self.key_color_top = top_color
        self.key_color_bottom = bottom_color
        self.update()
    
    def set_text_color(self, color):
        """Postavlja boju teksta"""
        self.text_color = color
        self.update()
    
    def set_selected(self, selected):
        """Postavlja selektovani status"""
        self.selected = selected
        self.update()
    
    def set_visible(self, visible):
        """Postavlja visible status"""
        self.visible = visible
        self.setVisible(visible)
        self.update()
    
    # Metode za resize i drag (konzistentne sa drugim widget-ima)
    
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))
    
    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)
    
    def _get_corner_at(self, pos):
        """Proverava da li je miš preko resize handle-a"""
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Proveri da li je klik na taster
                clicked_key = self._get_key_at_position(mouse_pos)
                if clicked_key:
                    print(f"Key pressed: {clicked_key}")
                else:
                    # Počni dragovanje
                    self.dragging = True
                    self.drag_start_pos = mouse_pos
                
                self.clicked.emit(self)
                # Ažuriraj properties kada se selektuje
                self.update_all_properties()

        event.accept()
    
    def _get_key_at_position(self, pos):
        """Pronalazi na koji taster je kliknuto"""
        # Ovde bi se implementirala logika za detekciju tastera
        # Za sada vraća None jer je kompleksno implementirati
        return None
    
    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
            self._update_properties_size()
            self._update_properties_position()
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            self._update_properties_position()
        
        event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self._update_properties_size()
            self._update_properties_position()
            self.update_properties_dict()

        event.accept()
    
    def _handle_resize(self, global_pos):
        """Menja veličinu widget-a"""
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(80, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(80, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(100, self.resize_start_size.width() - delta.x())
            new_height = max(80, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(100, self.resize_start_size.width() - delta.x())
            new_height = max(80, self.resize_start_size.height() - delta.y())

        self.set_size(new_width, new_height)
    
    def _draw_3d_effect(self, painter, x, y, width, height):
        """Crtanje 3D efekta za taster"""
        # Svetli ivice (gornja i leva)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawLine(x, y, x + width, y)  # Gornja ivica
        painter.drawLine(x, y, x, y + height)  # Leva ivica
        
        # Tamne ivice (donja i desna)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawLine(x, y + height, x + width, y + height)  # Donja ivica
        painter.drawLine(x + width, y, x + width, y + height)  # Desna ivica
    
    def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Postavi boju teksta
            painter.setPen(self.text_color)

            # Font za brojeve/slova - koristi postavljeni font_size
            font = QFont("Arial", self.font_size, QFont.Weight.Bold)
            painter.setFont(font)

            # Margin za tastaturu
            margin_x = 10
            margin_y = 10

            current_x = margin_x
            current_y = margin_y

            if self.key_type == "NUM":
                # Numerička tastatura (3x3 + donji red sa 0 i .)
                number = 1
                for i in range(3):
                    for j in range(3):
                        # Kreiraj gradijent
                        gradient = QLinearGradient(current_x, current_y, 
                                                  current_x, current_y + self.key_height)
                        gradient.setColorAt(0, self.key_color_top)
                        gradient.setColorAt(1, self.key_color_bottom)

                        painter.setBrush(gradient)
                        painter.setPen(QPen(self.border_color, 1))
                        painter.drawRoundedRect(current_x, current_y, 
                                              self.key_width, self.key_height, 5, 5)

                        # 3D efekat
                        if self.is_3d:
                            self._draw_3d_effect(painter, current_x, current_y, 
                                               self.key_width, self.key_height)

                        # Tekst (broj)
                        text = str(number)
                        text_rect = painter.boundingRect(current_x, current_y, 
                                                        self.key_width, self.key_height, 
                                                        Qt.AlignmentFlag.AlignCenter, text)
                        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)

                        current_x += self.key_width + 4
                        number += 1

                    current_x = margin_x
                    current_y += self.key_height + 4

                # Četvrti red za NUM tastaturu (0 i .)
                # Taster 0 (zauzima širinu kao 2 obična tastera)
                key_width_0 = self.key_width * 2 + 4  # 2 tastera + spacing

                gradient = QLinearGradient(current_x, current_y, 
                                          current_x, current_y + self.key_height)
                gradient.setColorAt(0, self.key_color_top)
                gradient.setColorAt(1, self.key_color_bottom)

                painter.setBrush(gradient)
                painter.setPen(QPen(self.border_color, 1))
                painter.drawRoundedRect(current_x, current_y, 
                                      key_width_0, self.key_height, 5, 5)

                if self.is_3d:
                    self._draw_3d_effect(painter, current_x, current_y, 
                                       key_width_0, self.key_height)

                text = "0"
                text_rect = painter.boundingRect(current_x, current_y, 
                                                key_width_0, self.key_height, 
                                                Qt.AlignmentFlag.AlignCenter, text)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)

                # Taster . (tacka) - pomakni za širinu tastera 0 + spacing
                current_x += key_width_0 + 4

                gradient = QLinearGradient(current_x, current_y, 
                                          current_x, current_y + self.key_height)
                gradient.setColorAt(0, self.key_color_top)
                gradient.setColorAt(1, self.key_color_bottom)

                painter.setBrush(gradient)
                painter.setPen(QPen(self.border_color, 1))
                painter.drawRoundedRect(current_x, current_y, 
                                      self.key_width, self.key_height, 5, 5)

                if self.is_3d:
                    self._draw_3d_effect(painter, current_x, current_y, 
                                       self.key_width, self.key_height)

                text = "."
                text_rect = painter.boundingRect(current_x, current_y, 
                                                self.key_width, self.key_height, 
                                                Qt.AlignmentFlag.AlignCenter, text)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)

            elif self.key_type == "QUERTZ":
                # QUERTZ tastatura - ostaje isto kao prethodno
                # Prvi red (10 tastera)
                keys_row_1 = "QWERTZUIOP"
                for key in keys_row_1:
                    gradient = QLinearGradient(current_x, current_y, 
                                              current_x, current_y + self.key_height)
                    gradient.setColorAt(0, self.key_color_top)
                    gradient.setColorAt(1, self.key_color_bottom)

                    painter.setBrush(gradient)
                    painter.setPen(QPen(self.border_color, 1))
                    painter.drawRoundedRect(current_x, current_y, 
                                          self.key_width, self.key_height, 5, 5)

                    if self.is_3d:
                        self._draw_3d_effect(painter, current_x, current_y, 
                                           self.key_width, self.key_height)

                    text_rect = painter.boundingRect(current_x, current_y, 
                                                    self.key_width, self.key_height, 
                                                    Qt.AlignmentFlag.AlignCenter, key)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, key)

                    current_x += self.key_width + 4

                # Drugi red (9 tastera, pomeren za pola tastera)
                current_x = margin_x + self.key_width // 2
                current_y += self.key_height + 4
                keys_row_2 = "ASDFGHJKL"
                for key in keys_row_2:
                    gradient = QLinearGradient(current_x, current_y, 
                                              current_x, current_y + self.key_height)
                    gradient.setColorAt(0, self.key_color_top)
                    gradient.setColorAt(1, self.key_color_bottom)

                    painter.setBrush(gradient)
                    painter.setPen(QPen(self.border_color, 1))
                    painter.drawRoundedRect(current_x, current_y, 
                                          self.key_width, self.key_height, 5, 5)

                    if self.is_3d:
                        self._draw_3d_effect(painter, current_x, current_y, 
                                           self.key_width, self.key_height)

                    text_rect = painter.boundingRect(current_x, current_y, 
                                                    self.key_width, self.key_height, 
                                                    Qt.AlignmentFlag.AlignCenter, key)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, key)

                    current_x += self.key_width + 4

                # Treći red (posebni tasteri)
                current_x = margin_x
                current_y += self.key_height + 4
                keys_row_3 = ["Ent", "Y", "X", "C", "V", "B", "N", "M", "Del"]

                for i, key in enumerate(keys_row_3):
                    if key in ["Ent", "Del"]:
                        key_width = int(self.key_width * 1.5)
                    else:
                        key_width = self.key_width

                    gradient = QLinearGradient(current_x, current_y, 
                                              current_x, current_y + self.key_height)
                    gradient.setColorAt(0, self.key_color_top)
                    gradient.setColorAt(1, self.key_color_bottom)

                    painter.setBrush(gradient)
                    painter.setPen(QPen(self.border_color, 1))
                    painter.drawRoundedRect(current_x, current_y, 
                                          key_width, self.key_height, 5, 5)

                    if self.is_3d:
                        self._draw_3d_effect(painter, current_x, current_y, 
                                           key_width, self.key_height)

                    # Manji font za duge tastere
                    if key in ["Ent", "Del"]:
                        small_font = QFont("Arial", max(6, self.font_size - 2), QFont.Weight.Bold)
                        painter.setFont(small_font)

                    text_rect = painter.boundingRect(current_x, current_y, 
                                                    key_width, self.key_height, 
                                                    Qt.AlignmentFlag.AlignCenter, key)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, key)

                    # Vrati font za sledeći taster
                    painter.setFont(font)

                    current_x += key_width + 4

                # Space bar
                current_x = margin_x
                current_y += self.key_height + 4
                space_width = self._width - 2 * margin_x

                gradient = QLinearGradient(current_x, current_y, 
                                          current_x, current_y + self.key_height)
                gradient.setColorAt(0, self.key_color_top)
                gradient.setColorAt(1, self.key_color_bottom)

                painter.setBrush(gradient)
                painter.setPen(QPen(self.border_color, 1))
                painter.drawRoundedRect(current_x, current_y, 
                                      space_width, self.key_height, 5, 5)

                if self.is_3d:
                    self._draw_3d_effect(painter, current_x, current_y, 
                                       space_width, self.key_height)

                # Veći font za SPACE
                space_font = QFont("Arial", max(10, self.font_size), QFont.Weight.Bold)
                painter.setFont(space_font)

                text_rect = painter.boundingRect(current_x, current_y, 
                                                space_width, self.key_height, 
                                                Qt.AlignmentFlag.AlignCenter, "SPACE")
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "SPACE")

            # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
            if self.selected:
                self._draw_selection_border(painter)
                self._draw_selection_handles(painter)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None
    
    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            if hasattr(main_window, 'width_spin_keys'):
                main_window.width_spin_keys.blockSignals(True)
                main_window.width_spin_keys.setValue(self._width)
                main_window.width_spin_keys.blockSignals(False)
                
            if hasattr(main_window, 'height_spin_keys'):
                main_window.height_spin_keys.blockSignals(True)
                main_window.height_spin_keys.setValue(self._height)
                main_window.height_spin_keys.blockSignals(False)
    
    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            if hasattr(main_window, 'pos_x_spin_keys'):
                main_window.pos_x_spin_keys.blockSignals(True)
                main_window.pos_x_spin_keys.setValue(self.x())
                main_window.pos_x_spin_keys.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin_keys'):
                main_window.pos_y_spin_keys.blockSignals(True)
                main_window.pos_y_spin_keys.setValue(self.y())
                main_window.pos_y_spin_keys.blockSignals(False)
    
    def update_all_properties(self):
        """Ažurira sve properties u properties baru"""
        self._update_properties_size()
        self._update_properties_position()

        main_window = self._find_main_window()
        if not main_window:
            return

        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj checkbox-ove
            if hasattr(main_window, 'active_checkbox_keys'):
                main_window.active_checkbox_keys.blockSignals(True)
                main_window.active_checkbox_keys.setChecked(self.active)
                main_window.active_checkbox_keys.blockSignals(False)
                
            if hasattr(main_window, 'visible_checkbox_keys'):
                main_window.visible_checkbox_keys.blockSignals(True)
                main_window.visible_checkbox_keys.setChecked(self.visible)
                main_window.visible_checkbox_keys.blockSignals(False)
                
            if hasattr(main_window, 'static_checkbox_keys'):
                main_window.static_checkbox_keys.blockSignals(True)
                main_window.static_checkbox_keys.setChecked(self.static)
                main_window.static_checkbox_keys.blockSignals(False)
            
            # Ažuriraj ime
            if hasattr(main_window, 'name_edit_keys'):
                main_window.name_edit_keys.blockSignals(True)
                main_window.name_edit_keys.setText(self.custom_name)
                main_window.name_edit_keys.blockSignals(False)
            
            # Ažuriraj stack order
            if hasattr(main_window, 'stack_order_spin_keys'):
                main_window.stack_order_spin_keys.blockSignals(True)
                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index(main_window.current_shape) + 1
                    main_window.stack_order_spin_keys.setValue(index)
                main_window.stack_order_spin_keys.blockSignals(False)
            
            # Ažuriraj tip tastature
            if hasattr(main_window, 'type_combo_keys'):
                main_window.type_combo_keys.blockSignals(True)
                main_window.type_combo_keys.setCurrentText(self.key_type)
                main_window.type_combo_keys.blockSignals(False)
            
            # Ažuriraj 3D checkbox
            if hasattr(main_window, '_3d_checkbox_keys'):
                main_window._3d_checkbox_keys.blockSignals(True)
                main_window._3d_checkbox_keys.setChecked(self.is_3d)
                main_window._3d_checkbox_keys.blockSignals(False)
            
            # Ažuriraj boje
            if hasattr(main_window, 'color_top_rect_keys'):
                main_window.color_top_rect_keys.setStyleSheet(
                    f"background-color: {self.key_color_top.name()}; border: 1px solid #ccc;"
                )
            
            if hasattr(main_window, 'color_bottom_rect_keys'):
                main_window.color_bottom_rect_keys.setStyleSheet(
                    f"background-color: {self.key_color_bottom.name()}; border: 1px solid #ccc;"
                )
            if hasattr(main_window, 'font_size_spin_keys'):
                main_window.font_size_spin_keys.blockSignals(True)
                main_window.font_size_spin_keys.setValue(self.font_size)
                main_window.font_size_spin_keys.blockSignals(False)
        
            # Ažuriraj boje sa novim imenima
            if hasattr(main_window, 'start_color_rect_keys'):
                main_window.start_color_rect_keys.setStyleSheet(
                    f"background-color: {self.key_color_top.name()}; border: 1px solid #ccc;"
                )

            if hasattr(main_window, 'end_color_rect_keys'):
                main_window.end_color_rect_keys.setStyleSheet(
                    f"background-color: {self.key_color_bottom.name()}; border: 1px solid #ccc;"
                )

            if hasattr(main_window, 'font_color_rect_keys'):
                main_window.font_color_rect_keys.setStyleSheet(
                    f"background-color: {self.text_color.name()}; border: 1px solid #ccc;"
                )
    
    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima tastature"""
        return {
            'type': 'Keys',
            'name': getattr(self, 'custom_name', 'Keys_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'key_type': self.key_type,
            'is_3d': self.is_3d,
            'font_size': self.font_size,  # DODAJ OVO
            'key_color_top': self.key_color_top.name(),
            'key_color_bottom': self.key_color_bottom.name(),
            'text_color': self.text_color.name(),
            'border_color': self.border_color.name(),
            'active': getattr(self, 'active', True),
            'visible': getattr(self, 'visible', True),
            'static': getattr(self, 'static', False)
        }
    
    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        main_window = self._find_main_window()
        if not main_window:
            return
            
        if hasattr(main_window, 'all_keys_dicts'):
            if self.custom_name in main_window.all_keys_dicts:
                main_window.all_keys_dicts[self.custom_name] = self.get_properties_dict()

class ButtonWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, w=100, h=50, parent=None):
        super().__init__(parent)
        self.setFixedSize(w, h)
        
        # Svojstva
        self.start_color = QColor(0, 0, 255)
        self.end_color = QColor(0, 0, 136)
        self.text_color = QColor(255, 255, 255)
        self.border_color = QColor(0, 0, 0)
        self.border_width = 1
        self.button_text = "Press"
        self.text_size = 20
        self.is_selected = False
        self.use_3d = True
        self.custom_name = ""
        
        # Postavi atribute za mouse events
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        #self.setStyleSheet("background-color: transparent;")
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Resize i drag varijable - DODAJTE OVO!
        self.resizing = False
        self.dragging = False  # DODAJTE OVO!
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()  # DODAJTE OVO!
                # Svojstva
        self.start_color = QColor(0, 0, 255)
        self.end_color = QColor(0, 0, 136)
        self.text_color = QColor(255, 255, 255)
        self.button_text = "Press"
        self.text_size = 4
        self.is_selected = False
        self.use_3d = True
        self.custom_name = ""
        
        # DODAJTE OVE ATRIBUTE:
        self.active = True
        self.visible = True
        self.static = False
        self.stack_order = 1
        
        # Postavi atribute za mouse events
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        #self.setStyleSheet("background-color: transparent;")
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Resize i drag varijable
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        # INICIJALIZUJTE REČNIK:
        self.properties_dict = {}
        self.update_properties_dict()  # Popuni rečnik sa početnim vrednostima

    def update_properties_dict(self):
        """Ažurira rečnik sa trenutnim vrednostima svojstava"""
        self.properties_dict = {
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'name': self.custom_name,
            'stack_order': self.stack_order,
            'position_x': self.x(),
            'position_y': self.y(),
            'width': self.width(),
            'height': self.height(),
            'start_color': self.start_color.name(),  # U heksadecimalnom formatu
            'end_color': self.end_color.name(),
            '3d': self.use_3d,
            'text': self.button_text,
            'text_size': self.text_size+25,
            'text_color': self.text_color.name(),
            #'corner_radius': self.r
        }

    def get_properties_dict(self):
        """Vraća kopiju rečnika sa svojstvima"""
        self.update_properties_dict()  # Osveži vrednosti pre vraćanja
        return self.properties_dict.copy()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gradient pozadina
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, self.start_color)    # 0% - start color
        gradient.setColorAt(0.3, self.end_color)      # 10% - prelaz na end color
        gradient.setColorAt(1.0, self.end_color) 
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        
        r=int((7/5)*self.text_size+8/5)

        painter.drawRoundedRect(0, 0, self.width(), self.height(), r, r)

        # 3D efekat
        if self.use_3d:
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawLine(r, self.height()-1, self.width()-r, self.height()-1)
            painter.drawLine(self.width()-1, r, self.width()-1, self.height()-r)
            painter.drawArc(self.width() - 2*r-1, self.height() - 2*r-1, 2*r, 2*r, 270*16, 90*16)

        # TEKST
        painter.setPen(QPen(self.text_color))
        font = QFont()
        font.setPointSize(int((23/5)*self.text_size+17/5))
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.button_text)

        # Selekcija (handle-ovi)
        if self.is_selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)
            

    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima - VEĆE TAČKE"""
        handle_size = 8  # POVEĆAJTE SA 6 NA 8
        half_size = handle_size // 2

        # Svetlo plava boja za tačke sa tamno plavim okvirom
        painter.setBrush(QColor(0, 255, 0))  # Svetlo plava
        painter.setPen(QPen(QColor(0, 80, 200), 1))  # Tamno plavi okvir

        # 4 ugla - KORISTITE ELIPSE ZA OKRUGLE TAČKE
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            # Koristite drawEllipse za okrugle tačke
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Dodajte mali beli centar za bolju vidljivost
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))  # Vratite boju
            painter.setPen(QPen(QColor(0, 80, 200), 1))  # Vratite okvir
            
    def _draw_selection_border(self, painter):
        """Crtanje plavog isprekidanog okvira oko selektovanog button-a sa razmakom"""
        # Kreiraj pravougaonik sa razmakom od 2 piksela sa svih strana
        margin = 2  # Razmak od button-a
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        # Svetlija plava boja sa većom debljinom
        selection_pen = QPen(QColor(255, 0, 0))  # Svetlija plava boja
        selection_pen.setWidth(3)  # POVEĆAJTE SA 1 NA 2
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])  # Dužina crte: 4px, razmak: 2px

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos  # OVO JE VEĆ DODATO, SAMO PROVERITE
                self.clicked.emit(self)

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            # IZMENJENO: Koristite dva argumenta (x, y) umesto QPoint
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            self.move(new_x, new_y)
            
            # Ažuriraj properties bar ako postoji
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar
            self._update_properties_size()
            self._update_properties_position()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
            """Jednostavnija verzija - menja samo veličinu, ne poziciju"""
            if not self.resize_corner:
                return

            # Računaj promenu u veličini
            delta = global_pos - self.resize_start_pos

            new_width = self.resize_start_size.width()
            new_height = self.resize_start_size.height()

            # Samo donji desni ugao menja veličinu
            if self.resize_corner == "bottom_right":
                new_width = max(50, self.resize_start_size.width() + delta.x())
                new_height = max(30, self.resize_start_size.height() + delta.y())
            elif self.resize_corner == "top_right":
                new_width = max(50, self.resize_start_size.width() + delta.x())
                new_height = max(30, self.resize_start_size.height() - delta.y())
            elif self.resize_corner == "bottom_left":
                new_width = max(50, self.resize_start_size.width() - delta.x())
                new_height = max(30, self.resize_start_size.height() + delta.y())
            elif self.resize_corner == "top_left":
                new_width = max(50, self.resize_start_size.width() - delta.x())
                new_height = max(30, self.resize_start_size.height() - delta.y())

            # Ažuriraj samo veličinu (bez promene pozicije)
            self.setFixedSize(new_width, new_height)
            self.update()

            # Ažuriraj properties bar
            self._update_properties_size()

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        # Pronađi glavni prozor
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'width_spin') and 
            hasattr(main_window, 'height_spin')):
            
            main_window.width_spin.setValue(self.width())
            main_window.height_spin.setValue(self.height())

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'pos_x_spin') and 
            hasattr(main_window, 'pos_y_spin')):
            
            main_window.pos_x_spin.setValue(self.x())
            main_window.pos_y_spin.setValue(self.y())

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    # Ostale metode ostaju iste
    def set_selected(self, selected):
        self.is_selected = selected
        self.update()

    def set_bg_gradient(self, gradient):
        if gradient.stops():
            self.start_color = gradient.stops()[0][1]
            if len(gradient.stops()) > 1:
                self.end_color = gradient.stops()[-1][1]
        self.update()
        self.update_properties_dict()  # DODAJTE OVO

    def set_text_color(self, color):
        self.text_color = color
        self.update()
        self.update_properties_dict()  # DODAJTE OVO

    def set_border_color(self, color):
        self.border_color = color
        self.update()

    def set_border_width(self, width):
        self.border_width = width
        self.update()

    def set_button_text(self, text):
        self.button_text = text
        self.update()
        self.update_properties_dict()  # DODAJTE OVO

    def set_text_size(self, size):
        self.text_size = size
        self.update()
        self.update_properties_dict()  # DODAJTE OVO

    def set_radius(self, radius):
        self.r = radius
        self.update()
        self.update_properties_dict()  # DODAJTE OVO

    
    def set_active(self, active):
        self.active = active
        self.update_properties_dict()  # DODAJTE OVO

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)  # Ovo će sakriti/prikazati widget
        self.update_properties_dict()  # DODAJTE OVO

    def set_static(self, static):
        self.static = static
        self.update_properties_dict()  # DODAJTE OVO

    def set_stack_order(self, order):
        self.stack_order = order
        self.update_properties_dict()  # DODAJTE OVO

    # Dodajte i za move i resize:
    def move(self, x, y):
        super().move(x, y)
        self.update_properties_dict()  # DODAJTE OVO

    def resize(self, width, height):
        super().resize(width, height)
        self.update_properties_dict()  # DODAJTE OVO

    @property
    def color(self):
        return self.start_color

    def set_color(self, color):
        self.start_color = color
        self.update()

class GaugeWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, diameter, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        
        # Svojstva za gauge
        self.outer_color = QColor(0, 32, 64)
        self.inner_color = QColor(0, 0, 0)
        self.needle_color = QColor(0, 0, 0)
        self.background_color = QColor(0, 32, 64)
        
        # Novi atributi za properties
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.use_3d = True
        
        # Atributi za vrednosti gauge-a
        self.major_subdivision = 6  # Broj glavnih podeoka (default 6)
        self.minor_subdivision = 4  # Broj sporednih podeoka između glavnih (default 4)
        self.range_value = 100      # Maksimalna vrednost (default 100)
        self.value = 50             # Trenutna vrednost (default 50)
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Resize i drag varijable - DODAJ OVO!
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def get_scaled_value(self, original_value):
        """Vraća vrednost skaliranu u odnosu na originalni dijametar od 500"""
        scale_factor = self.diameter / 500.0
        return int(original_value * scale_factor)

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_diameter(self, diameter):
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.update()

    def set_outer_color(self, color):
        self.outer_color = color
        self.update()

    def set_inner_color(self, color):
        self.inner_color = color
        self.update()

    def set_needle_color(self, color):
        self.needle_color = color
        self.update()

    def set_background_color(self, color):
        self.background_color = color
        self.update()

    # Novi setter metodi
    def set_active(self, active):
        self.active = active
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def set_static(self, static):
        self.static = static
        self.update()

    def set_custom_name(self, name):
        self.custom_name = name

    def set_stack_order(self, order):
        self.stack_order = order

    def set_use_3d(self, use_3d):
        self.use_3d = use_3d
        self.update()

    def set_major_subdivision(self, count):
        self.major_subdivision = max(1, count)  # Minimum 1
        self.update()

    def set_minor_subdivision(self, count):
        self.minor_subdivision = max(0, count)  # Minimum 0
        self.update()

    def set_range_value(self, value):
        self.range_value = max(1, value)  # Minimum 1
        if self.value > self.range_value:
            self.value = self.range_value
        self.update()

    def set_value(self, value):
        self.value = max(0, min(value, self.range_value))  # Clamp između 0 i range_value
        self.update()

    def get_properties_dict(self):
        """Vraća rečnik sa svim properties-ima gauge-a"""
        return {
            'type': 'Gauge',
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'name': self.custom_name,
            'stack_order': self.stack_order,
            'x': self.x(),
            'y': self.y(),
            'diameter': self.diameter,
            'background_color': self.background_color.name(),
            'use_3d': self.use_3d,
            'major_subdivision': self.major_subdivision,
            'minor_subdivision': self.minor_subdivision,
            'range_value': self.range_value,
            'value': self.value,
            'outer_color': self.outer_color.name(),
            'inner_color': self.inner_color.name(),
            'needle_color': self.needle_color.name()
        }

    def update_properties_dict(self):
        """Ažurira properties rečnik"""
        pass

    # Metode za resize i drag (kao ClockWidget)
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit(self)

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            # Koristite dva argumenta (x, y) umesto QPoint
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar ako postoji
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar
            self._update_properties_size()
            self._update_properties_position()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Menja veličinu GaugeWidget-a"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu
        if self.resize_corner == "bottom_right":
            new_width = max(50, self.resize_start_size.width() + delta.x())
            new_height = max(50, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(50, self.resize_start_size.width() + delta.x())
            new_height = max(50, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(50, self.resize_start_size.width() - delta.x())
            new_height = max(50, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(50, self.resize_start_size.width() - delta.x())
            new_height = max(50, self.resize_start_size.height() - delta.y())

        # Za gauge, width i height moraju biti isti (krug je uvek kvadrat)
        size = min(new_width, new_height)
        
        # Ažuriraj samo veličinu (bez promene pozicije)
        self.setFixedSize(size, size)
        self.diameter = size
        self.update()

        # Ažuriraj properties bar
        self._update_properties_size()

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'diameter_spin_gauge')):
            
            main_window.diameter_spin_gauge.blockSignals(True)
            main_window.diameter_spin_gauge.setValue(self.diameter)
            main_window.diameter_spin_gauge.blockSignals(False)

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'pos_x_spin_gauge') and 
            hasattr(main_window, 'pos_y_spin_gauge')):
            
            main_window.pos_x_spin_gauge.blockSignals(True)
            main_window.pos_x_spin_gauge.setValue(self.x())
            main_window.pos_x_spin_gauge.blockSignals(False)
            
            main_window.pos_y_spin_gauge.blockSignals(True)
            main_window.pos_y_spin_gauge.setValue(self.y())
            main_window.pos_y_spin_gauge.blockSignals(False)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        r = self.diameter
        
        # Širine linija skalirane prema veličini
        base_line_width = max(1, self.get_scaled_value(3))
        big_mark_width = max(1, self.get_scaled_value(7))
        small_mark_width = max(1, self.get_scaled_value(3))
        needle_width = max(1, self.get_scaled_value(5))
        
        # Crtanje osnovnog kruga
        pen = QPen(self.background_color)
        pen.setWidth(base_line_width)
        painter.setPen(pen)
        painter.setBrush(self.background_color)
        painter.drawEllipse(0, 0, r, r)
        
        # --- 3D efekat ---
        if self.use_3d:
            
            pen = QPen(QColor(255,255,255))
            pen.setWidth(base_line_width)
            painter.setPen(pen)
            painter.drawArc(0, 0, r, r, 16*35, -16*175)

            pen = QPen(QColor(0, 0, 0))
            pen.setWidth(base_line_width)
            painter.setPen(pen)
            painter.drawArc(0, 0, r, r, 35*16, 16*185)
        
        # Crtanje luka


        # Translacija za oznake i iglu
        painter.translate(r // 2, r // 2)
        
        # Računanje broja ukupnih podeoka
        total_divisions = self.major_subdivision * (self.minor_subdivision + 1)
        angle_per_division = 270.0 / total_divisions  # Ukupno 270 stepeni
        
        # Rotacija za početnu poziciju
        painter.rotate(-135)

        # Dimenzije oznaka skalirane prema veličini
        big_mark_start = self.get_scaled_value(-210)
        big_mark_end = self.get_scaled_value(-190)
        
        small_mark_start = self.get_scaled_value(-205)
        small_mark_end = self.get_scaled_value(-195)
        
        needle_length = self.get_scaled_value(-210)

        # Crtanje podeoka
        for i in range(total_divisions + 1):  # +1 da uključimo i poslednji podeok
            if i % (self.minor_subdivision + 1) == 0:
                # Glavni podeoci
                big_pen = QPen(self.inner_color)
                big_pen.setWidth(big_mark_width)
                painter.setPen(big_pen)
                painter.drawLine(0, big_mark_start, 0, big_mark_end)
            else:
                # Sporedni podeoci
                small_pen = QPen(self.inner_color)
                small_pen.setWidth(small_mark_width)
                painter.setPen(small_pen)
                painter.drawLine(0, small_mark_start, 0, small_mark_end)
            
            # Rotiraj za sledeći podeok
            if i < total_divisions:
                painter.rotate(angle_per_division)

        # Vratimo na početni položaj za kazaljku
        painter.rotate(-(total_divisions * angle_per_division))
        
        # Računanje ugla za kazaljku na osnovu vrednosti
        # 0 vrednost = -135°, max vrednost = 135° (ukupno 270°)
        if self.range_value > 0:
            needle_angle =   (270 * self.value / self.range_value)
        else:
            needle_angle = -135
        
        # Crtanje igle
        painter.rotate(needle_angle)
        needle_pen = QPen(self.needle_color)
        needle_pen.setWidth(needle_width)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, 0, needle_length)

        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            painter.resetTransform()
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

class ClockWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, diameter, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        
        # Svojstva za clock
        self.outer_color = QColor(0, 32, 64)
        self.inner_color = QColor(117, 117, 115)
        self.needle_color = QColor(0, 0, 0)
        self.background_color = QColor(0, 32, 64)
        
        # Novi atributi
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.use_3d = True
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Resize i drag varijable - DODAJ OVO!
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Resize handle

        self.setMouseTracking(True)
        self.dragging = False
        self.resizing = False
        self.drag_start_position = QPoint()
        self.original_geometry = QRect()

    def move(self, x, y):
        super().move(x, y)
        # Ažuriraj properties bar ako postoji
        self._update_properties_position()

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'pos_x_spin_clock') and 
            hasattr(main_window, 'pos_y_spin_clock')):
            
            main_window.pos_x_spin_clock.blockSignals(True)
            main_window.pos_x_spin_clock.setValue(self.x())
            main_window.pos_x_spin_clock.blockSignals(False)
            
            main_window.pos_y_spin_clock.blockSignals(True)
            main_window.pos_y_spin_clock.setValue(self.y())
            main_window.pos_y_spin_clock.blockSignals(False)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def get_scaled_value(self, original_value):
        """Vraća vrednost skaliranu u odnosu na originalni dijametar od 720"""
        scale_factor = self.diameter / 720.0
        return int(original_value * scale_factor)

    def update_resize_handle(self):
        handle_size = 8
        self.resize_handle.setGeometry(
            self.width() - handle_size, 
            self.height() - handle_size, 
            handle_size, 
            handle_size
        )

    def set_selected(self, selected):
        self.selected = selected
        self.update()  # Ovo će automatski pozvati _draw_selection_handles u paintEvent

    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def set_diameter(self, diameter):
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.update()

    def set_outer_color(self, color):
        self.outer_color = color
        self.update()

    def set_inner_color(self, color):
        self.inner_color = color
        self.update()

    def set_needle_color(self, color):
        self.needle_color = color
        self.update()

    def set_background_color(self, color):
        self.background_color = color
        self.update()

    def set_active(self, active):
        self.active = active
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def set_static(self, static):
        self.static = static
        self.update()

    def set_custom_name(self, name):
        self.custom_name = name

    def set_stack_order(self, order):
        self.stack_order = order

    def set_use_3d(self, use_3d):
        self.use_3d = use_3d
        self.update()

    def set_hours(self, hours):
        self.hours = hours % 12  # Obezbedi da bude u opsegu 0-11
        self.update()

    def set_minutes(self, minutes):
        self.minutes = minutes % 60  # Obezbedi da bude u opsegu 0-59
        self.update()

    def set_seconds(self, seconds):
        self.seconds = seconds % 60  # Obezbedi da bude u opsegu 0-59
        self.update()

    def get_properties_dict(self):
        """Vraća rečnik sa svim properties-ima clock-a"""
        return {
            'type': 'Clock',
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'name': self.custom_name,
            'stack_order': self.stack_order,
            'x': self.x(),
            'y': self.y(),
            'diameter': self.diameter,
            'background_color': self.background_color.name(),
            'use_3d': self.use_3d,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds,
            'outer_color': self.outer_color.name(),
            'inner_color': self.inner_color.name(),
            'needle_color': self.needle_color.name()
        }

    def update_properties_dict(self):
        """Ažurira properties rečnik"""
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit(self)

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            # Koristite dva argumenta (x, y) umesto QPoint
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar ako postoji
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar
            self._update_properties_size()
            self._update_properties_position()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None
    
    def _handle_resize(self, global_pos):
        """Menja veličinu ClockWidget-a - slično CircleWidget"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu
        if self.resize_corner == "bottom_right":
            new_width = max(50, self.resize_start_size.width() + delta.x())
            new_height = max(50, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(50, self.resize_start_size.width() + delta.x())
            new_height = max(50, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(50, self.resize_start_size.width() - delta.x())
            new_height = max(50, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(50, self.resize_start_size.width() - delta.x())
            new_height = max(50, self.resize_start_size.height() - delta.y())

        # Za clock, width i height moraju biti isti (krug je uvek kvadrat)
        size = min(new_width, new_height)
        
        # Ažuriraj samo veličinu (bez promene pozicije)
        self.setFixedSize(size, size)
        self.diameter = size
        self.update()

        # Ažuriraj properties bar
        self._update_properties_size()
        
    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'diameter_spin_clock')):
            
            main_window.diameter_spin_clock.blockSignals(True)
            main_window.diameter_spin_clock.setValue(self.diameter)
            main_window.diameter_spin_clock.blockSignals(False)

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'pos_x_spin_clock') and 
            hasattr(main_window, 'pos_y_spin_clock')):
            
            main_window.pos_x_spin_clock.blockSignals(True)
            main_window.pos_x_spin_clock.setValue(self.x())
            main_window.pos_x_spin_clock.blockSignals(False)
            
            main_window.pos_y_spin_clock.blockSignals(True)
            main_window.pos_y_spin_clock.setValue(self.y())
            main_window.pos_y_spin_clock.blockSignals(False)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # ... postojeći kod za crtanje clock-a ...
        
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            painter.resetTransform()
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = self.diameter
        center_x = r // 2
        center_y = r // 2

        # Širine linija skalirane prema veličini
        base_line_width = max(1, self.get_scaled_value(3))
        big_mark_width = max(1, self.get_scaled_value(15))
        needle1_width = max(1, self.get_scaled_value(6))
        needle2_width = max(1, self.get_scaled_value(8))
        needle3_width = max(1, self.get_scaled_value(12))

        # Dimenzije skalirane prema veličini
        radius = self.get_scaled_value(360)
        point_radius = self.get_scaled_value(290)

        # Dužine kazaljki
        needle1_length = self.get_scaled_value(290)
        needle2_length = self.get_scaled_value(220)
        needle3_length = self.get_scaled_value(150)

        # --- Krug ---
        pen = QPen(self.background_color)
        pen.setWidth(base_line_width)
        painter.setPen(pen)
        painter.setBrush(self.background_color)
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)

        # --- 3D efekat ---
        if self.use_3d:
            pen = QPen(self.inner_color)
            pen.setWidth(base_line_width)
            painter.setPen(pen)
            painter.drawArc(center_x - radius, center_y - radius, radius * 2, radius * 2, 16*35, -16*175)

            pen = QPen(QColor(0, 0, 0))
            pen.setWidth(base_line_width)
            painter.setPen(pen)
            painter.drawArc(center_x - radius, center_y - radius, radius * 2, radius * 2, 35*16, 16*185)



        # --- Pomeraj koordinatni sistem u centar ---
        painter.translate(center_x, center_y)

        # --- Računanje ugla za kazaljke na osnovu vremena ---
        # Qt: 0° = desno, 90° = dole, 180° = levo, 270° = gore
        # Da bi 0° bio na vrhu, treba -180° (jer počinje sa 9 sati)

        seconds_angle = (self.seconds * 6) 
        minutes_angle = (self.minutes * 6) + (self.seconds * 0.1)  
        hours_angle = ((self.hours % 12) * 30) + (self.minutes * 0.5) 

        # --- Velike tačke (brojevi na satu) ---
        big_pen = QPen(self.inner_color)
        big_pen.setWidth(big_mark_width)
        painter.setPen(big_pen)

        # Crtaj tačke počevši od vrha (12 sati)
        painter.rotate(-180)  # Rotiraj za -180 da bi prva tačka bila na vrhu
        for i in range(12):  
            painter.drawPoint(0, -point_radius)
            painter.rotate(30)

        # Vrati na početni položaj
        painter.rotate(-360 + 180)

        # --- Satna kazaljka (najkraća) ---
        painter.rotate(hours_angle)
        needle_pen = QPen(self.needle_color)
        needle_pen.setWidth(needle3_width)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, 0, -needle3_length)
        painter.rotate(-hours_angle)

        # --- Minutna kazaljka (srednja) ---
        painter.rotate(minutes_angle)
        needle_pen.setWidth(needle2_width)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, 0, -needle2_length)
        painter.rotate(-minutes_angle)

        # --- Sekundna kazaljka (najduža) ---
        painter.rotate(seconds_angle)
        needle_pen.setWidth(needle1_width)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, 0, -needle1_length)

        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            painter.resetTransform()
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

class ProgressBarWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        
        # Svojstva za progress bar
        self.bar_color = QColor(0, 32, 64)      # Tamnoplava kao original
        self.progress_color = QColor(255, 255, 255)  # Bela kao original
        self.border_color = QColor(0, 0, 0)     # Crni border
        self.white_border_color = QColor(236, 238, 241)  # Svetli border kao original
        
        # Progress vrednost (0-100)
        self.progress_value = 50  # Podrazumevano 50% kao u originalu
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Default properties za properties dict
        self.custom_name = ""
        self.stack_order = 1
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True
        self.value = 50
        self.min_value = 0
        self.max_value = 100
        
        # Resize i drag varijable (kao u SliderWidget)
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_size(self, width, height):
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        self.update()

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def set_bar_color(self, color):
        self.bar_color = color
        self.update()

    def set_progress_color(self, color):
        self.progress_color = color
        self.update()

    def set_border_color(self, color):
        self.border_color = color
        self.update()

    def set_white_border_color(self, color):
        self.white_border_color = color
        self.update()

    def set_progress(self, value):
        """Postavlja vrednost progress bara (0-100)"""
        self.progress_value = max(0, min(100, value))
        self.update()

    def get_progress(self):
        """Getter za progress vrednost"""
        return self.progress_value

    # Metode za resize i drag (kao u SliderWidget)
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos
                
                self.clicked.emit(self)
                # Ažuriraj sve properties kada se selektuje
                self.update_all_properties()

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
            # Ažuriraj properties bar U TOKU resize-a
            self._update_properties_size()
            self._update_properties_position()
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar U TOKU draganja (real-time)
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar NAKON što se završi drag ili resize
            self._update_properties_size()
            self._update_properties_position()
            
            # Ažuriraj rečnik
            self.update_properties_dict()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Menja veličinu ProgressBarWidget-a"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu
        if self.resize_corner == "bottom_right":
            new_width = max(200, self.resize_start_size.width() + delta.x())
            new_height = max(10, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(200, self.resize_start_size.width() + delta.x())
            new_height = max(10, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(200, self.resize_start_size.width() - delta.x())
            new_height = max(10, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(200, self.resize_start_size.width() - delta.x())
            new_height = max(10, self.resize_start_size.height() - delta.y())

        self.set_size(new_width, new_height)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj width i height spin-ove ako postoje u properties baru
            if hasattr(main_window, 'width_spin_progressbar'):
                main_window.width_spin_progressbar.blockSignals(True)
                main_window.width_spin_progressbar.setValue(self._width)
                main_window.width_spin_progressbar.blockSignals(False)
                
            if hasattr(main_window, 'height_spin_progressbar'):
                main_window.height_spin_progressbar.blockSignals(True)
                main_window.height_spin_progressbar.setValue(self._height)
                main_window.height_spin_progressbar.blockSignals(False)

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj position spin-ove ako postoje u properties baru
            if hasattr(main_window, 'pos_x_spin_progressbar'):
                main_window.pos_x_spin_progressbar.blockSignals(True)
                main_window.pos_x_spin_progressbar.setValue(self.x())
                main_window.pos_x_spin_progressbar.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin_progressbar'):
                main_window.pos_y_spin_progressbar.blockSignals(True)
                main_window.pos_y_spin_progressbar.setValue(self.y())
                main_window.pos_y_spin_progressbar.blockSignals(False)

    def update_all_properties(self):
        """Ažurira sve properties u properties baru"""
        self._update_properties_size()
        self._update_properties_position()
        
        # Ažuriraj ostale properties ako su prikazane
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj checkbox-ove ako postoje
            if hasattr(main_window, 'active_checkbox_progressbar'):
                main_window.active_checkbox_progressbar.blockSignals(True)
                main_window.active_checkbox_progressbar.setChecked(self.active)
                main_window.active_checkbox_progressbar.blockSignals(False)
                
            if hasattr(main_window, 'visible_checkbox_progressbar'):
                main_window.visible_checkbox_progressbar.blockSignals(True)
                main_window.visible_checkbox_progressbar.setChecked(self.visible)
                main_window.visible_checkbox_progressbar.blockSignals(False)
                
            if hasattr(main_window, 'static_checkbox_progressbar'):
                main_window.static_checkbox_progressbar.blockSignals(True)
                main_window.static_checkbox_progressbar.setChecked(self.static)
                main_window.static_checkbox_progressbar.blockSignals(False)
                
            if hasattr(main_window, '_3d_checkbox_progressbar'):
                main_window._3d_checkbox_progressbar.blockSignals(True)
                main_window._3d_checkbox_progressbar.setChecked(self._3d)
                main_window._3d_checkbox_progressbar.blockSignals(False)
            
            # Ažuriraj value spin ako postoji
            if hasattr(main_window, 'value_spin_progressbar'):
                main_window.value_spin_progressbar.blockSignals(True)
                main_window.value_spin_progressbar.setValue(self.value)
                main_window.value_spin_progressbar.blockSignals(False)
            
            # Ažuriraj progress spin ako postoji
            if hasattr(main_window, 'progress_spin_progressbar'):
                main_window.progress_spin_progressbar.blockSignals(True)
                main_window.progress_spin_progressbar.setValue(self.progress_value)
                main_window.progress_spin_progressbar.blockSignals(False)
            
            # Ažuriraj min/max spin-ove ako postoje
            if hasattr(main_window, 'min_spin_progressbar'):
                main_window.min_spin_progressbar.blockSignals(True)
                main_window.min_spin_progressbar.setValue(self.min_value)
                main_window.min_spin_progressbar.blockSignals(False)
                
            if hasattr(main_window, 'max_spin_progressbar'):
                main_window.max_spin_progressbar.blockSignals(True)
                main_window.max_spin_progressbar.setValue(self.max_value)
                main_window.max_spin_progressbar.blockSignals(False)
            
            # Ažuriraj ime ako postoji
            if hasattr(main_window, 'name_edit_progressbar'):
                main_window.name_edit_progressbar.blockSignals(True)
                main_window.name_edit_progressbar.setText(self.custom_name)
                main_window.name_edit_progressbar.blockSignals(False)
            
            # Ažuriraj boje ako postoje
            if hasattr(main_window, 'bar_color_rect_progressbar'):
                main_window.bar_color_rect_progressbar.setStyleSheet(f"background-color: {self.bar_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'progress_color_rect_progressbar'):
                main_window.progress_color_rect_progressbar.setStyleSheet(f"background-color: {self.progress_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'border_color_rect_progressbar'):
                main_window.border_color_rect_progressbar.setStyleSheet(f"background-color: {self.border_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'white_border_color_rect_progressbar'):
                main_window.white_border_color_rect_progressbar.setStyleSheet(f"background-color: {self.white_border_color.name()}; border: 1px solid #ccc;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self._width
        h = self._height
        
        # Prvo crtamo celokupni progress bar (pozadina)
        # Tamnoplavi deo (pozadina) - celokupni bar
        pen = QPen(self.bar_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(self.bar_color)
        
        # Polumjer za polukrugove
        radius = h // 2
        
        # Levi polukrug
        painter.drawPie(0, 0, 2 * radius, 2 * radius, 90*16, 180*16)
        # Centralni pravougaonik
        painter.drawRect(radius, 0, w - 2 * radius, h)
        # Desni polukrug
        painter.drawPie(w - 2 * radius, 0, 2 * radius, 2 * radius, 90*16, -180*16)
        
        # Beli deo (progress) - samo deo koji je popunjen
        pen = QPen(self.progress_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(self.progress_color)
        
        # Izračunaj širinu progress dela
        progress_width = int((w - 2 * radius) * (self.progress_value / 100.0))
        
        
        # Levi beli polukrug (uvek crtamo ako ima progress)
        inner_offset = 6  # Unutrašnji offset za beli deo
        inner_radius = radius - inner_offset // 2
        
        # Levi beli polukrug
        painter.drawPie(inner_offset // 2, inner_offset // 2, 2 * inner_radius, 2 * inner_radius, 90*16, 180*16)
        
        # Centralni beli pravougaonik (progress deo)
        painter.drawRect(radius - 3 + inner_offset // 2, inner_offset // 2, progress_width, 2 * inner_radius)
        
        # Desni beli polukrug (crtamo samo ako je progress 100%)
        painter.drawPie(inner_offset // 2 + progress_width, inner_offset // 2, 2 * inner_radius, 2 * inner_radius, 90*16, -180*16)

        if self._3d:
            # Crni border (gornji deo)
            pen = QPen(self.border_color)
            pen.setWidth(2)
            painter.setPen(pen)

            # Gornja linija
            painter.drawLine(radius, 0, w - radius, 0)
            # Desni gornji luk
            painter.drawArc(w - 2 * radius, 0, 2 * radius, 2 * radius, 90*16, -45*16)
            # Levi gornji luk
            painter.drawArc(0, 0, 2 * radius, 2 * radius, 90*16, 135*16)

            # Svetli border (donji deo) - kao u originalu
            pen = QPen(self.white_border_color)
            pen.setWidth(1)
            painter.setPen(pen)

            # Donja linija
            painter.drawLine(radius, h, w - radius, h)
            # Desni donji luk
            painter.drawArc(w - 2 * radius, 0, 2 * radius, 2 * radius, 45*16, -135*16)
            # Levi donji luk
            painter.drawArc(0, 0, 2 * radius, 2 * radius, 225*16, 45*16)

        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

    # METODE ZA PROPERTIES DICT
    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima progress bar-a"""
        return {
            'type': 'ProgressBar',
            'name': self.custom_name,
            'stack_order': self.stack_order,
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'position': (self.x(), self.y()),
            'size': (self.get_width(), self.get_height()),
            'progress_color': self.progress_color.name(),
            'background_color': self.bar_color.name(),
            '_3d': self._3d,
            'value': self.value,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'border_color': self.border_color.name(),
            'white_border_color': self.white_border_color.name(),
            'progress_value': self.progress_value
        }

    def update_properties_dict(self):
        """Ažurira properties dict na osnovu trenutnih vrednosti"""
        main_window = self._find_main_window()
        if not main_window:
            return
            
        if hasattr(main_window, 'all_progressbar_dicts'):
            if self.custom_name in main_window.all_progressbar_dicts:
                main_window.all_progressbar_dicts[self.custom_name] = self.get_properties_dict()

    def set_active(self, active):
        self.active = active
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()

    def set_static(self, static):
        self.static = static
        self.update()

    def set_3d(self, _3d):
        self._3d = _3d
        self.update()

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))
        # Ažuriraj i progress vrednost ako je potrebno
        progress_range = self.max_value - self.min_value
        if progress_range > 0:
            self.progress_value = int(((self.value - self.min_value) / progress_range) * 100)
        self.update()

    def set_range(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        # Ažuriraj trenutnu vrednost da bude unutar novog opsega
        self.value = max(min_value, min(max_value, self.value))
        # Ažuriraj progress vrednost
        progress_range = self.max_value - self.min_value
        if progress_range > 0:
            self.progress_value = int(((self.value - self.min_value) / progress_range) * 100)
        self.update()

class ScrollBarWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        
        # Svojstva za scroll bar
        self.track_color = QColor(0, 32, 64)  # Tamnoplava - glavni track
        self.thumb_color = QColor(0, 64, 128)  # Svetloplava - thumb (pokazivač)
        self.border_color = QColor(0, 0, 0)    # Crni border
        self.white_border_color = QColor(236, 238, 241)  # Sivi/beli border
        
        # Dodatna svojstva (za properties bar)
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.stack_order = 1
        self._3d = True  # 3D efekat
        
        # Progress vrednosti
        self.range_value = 100  # Range za scrollbar
        self.current_value = 50  # Trenutna vrednost
        self.knob_size = 30  # Veličina thumb-a u procentima (30% track-a)
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Resize i drag varijable
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        # Za draganje thumb-a
        self.thumb_dragging = False
        self.thumb_drag_start_pos = QPoint()
        self.thumb_drag_start_value = 0

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_size(self, width, height):
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        self.update()

    def get_width(self):
        """Getter za width"""
        return self._width

    def get_height(self):
        """Getter za height"""
        return self._height

    def set_track_color(self, color):
        self.track_color = color
        self.update()

    def set_thumb_color(self, color):
        self.thumb_color = color
        self.update()

    def set_border_color(self, color):
        self.border_color = color
        self.update()

    def set_white_border_color(self, color):
        self.white_border_color = color
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()

    def set_3d(self, three_d):
        self._3d = three_d
        self.update()

    def set_range(self, value):
        """Postavlja range vrednost scroll bar-a"""
        self.range_value = max(1, value)
        self.update()

    def set_current_value(self, value):
        """Postavlja trenutnu vrednost scroll bar-a"""
        self.current_value = max(0, min(self.range_value, value))
        self.update()

    def get_current_value(self):
        """Getter za trenutnu vrednost"""
        return self.current_value

    def set_knob_size(self, size):
        """Postavlja veličinu thumb-a u procentima (0-100)"""
        self.knob_size = max(10, min(100, size))  # Minimalno 10%, maksimalno 100%
        self.update()

    def get_knob_size(self):
        """Getter za veličinu thumb-a"""
        return self.knob_size

    # Metode za resize i drag
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Proveri da li je klik na thumb (pokazivač)
                thumb_rect = self.get_thumb_rect()
                if thumb_rect.contains(event.pos()):
                    # Klik na thumb - počni draganje thumb-a
                    self.thumb_dragging = True
                    self.dragging = False
                    self.thumb_drag_start_pos = event.pos()
                    self.thumb_drag_start_value = self.current_value
                else:
                    # Počni dragovanje widgeta ili klik na track
                    self.dragging = True
                    self.thumb_dragging = False
                    self.drag_start_pos = mouse_pos
                    
                    # Klik na track - pomeri thumb na tu poziciju
                    track_rect = self.get_track_rect()
                    if track_rect.contains(event.pos()):
                        # Izračunaj novu vrednost na osnovu pozicije klika
                        new_value = self._calculate_value_from_position(event.pos().x())
                        self.set_current_value(new_value)
                
                self.clicked.emit(self)
                # Ažuriraj sve properties kada se selektuje
                self.update_all_properties()

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.thumb_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Draganje thumb-a
            delta_x = mouse_pos.x() - self.thumb_drag_start_pos.x()
            track_rect = self.get_track_rect()
            thumb_rect = self.get_thumb_rect()
            
            # Izračunaj koliko piksela odgovara jednoj jedinici vrednosti
            track_width = track_rect.width() - thumb_rect.width()
            if track_width > 0:
                pixels_per_unit = track_width / self.range_value
                delta_value = int(delta_x / pixels_per_unit)
                new_value = self.thumb_drag_start_value + delta_value
                self.set_current_value(new_value)
                
                # Ažuriraj properties bar u real-time
                self._update_properties_value()
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar U TOKU draganja (real-time)
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.thumb_dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar NAKON što se završi drag ili resize
            self._update_properties_size()
            self._update_properties_position()
            
            # Ažuriraj rečnik
            self.update_properties_dict()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Menja veličinu ScrollBarWidget-a"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu
        if self.resize_corner == "bottom_right":
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(10, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(10, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(100, self.resize_start_size.width() - delta.x())
            new_height = max(10, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(100, self.resize_start_size.width() - delta.x())
            new_height = max(10, self.resize_start_size.height() - delta.y())

        self.set_size(new_width, new_height)
        
        # Ažuriraj properties bar U TOKU resize-a
        self._update_properties_size()
        self._update_properties_position()

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj width i height spin-ove ako postoje u properties baru
            if hasattr(main_window, 'width_spin_scrollbar'):
                main_window.width_spin_scrollbar.blockSignals(True)
                main_window.width_spin_scrollbar.setValue(self._width)
                main_window.width_spin_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'height_spin_scrollbar'):
                main_window.height_spin_scrollbar.blockSignals(True)
                main_window.height_spin_scrollbar.setValue(self._height)
                main_window.height_spin_scrollbar.blockSignals(False)

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj position spin-ove ako postoje u properties baru
            if hasattr(main_window, 'pos_x_spin_scrollbar'):
                main_window.pos_x_spin_scrollbar.blockSignals(True)
                main_window.pos_x_spin_scrollbar.setValue(self.x())
                main_window.pos_x_spin_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin_scrollbar'):
                main_window.pos_y_spin_scrollbar.blockSignals(True)
                main_window.pos_y_spin_scrollbar.setValue(self.y())
                main_window.pos_y_spin_scrollbar.blockSignals(False)

    def _update_properties_value(self):
        """Ažuriraj vrednosti u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj value spin-ove ako postoje u properties baru
            if hasattr(main_window, 'current_value_spin_scrollbar'):
                main_window.current_value_spin_scrollbar.blockSignals(True)
                main_window.current_value_spin_scrollbar.setValue(self.current_value)
                main_window.current_value_spin_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'knob_size_spin_scrollbar'):
                main_window.knob_size_spin_scrollbar.blockSignals(True)
                main_window.knob_size_spin_scrollbar.setValue(self.knob_size)
                main_window.knob_size_spin_scrollbar.blockSignals(False)

    def update_all_properties(self):
        """Ažurira sve properties u properties baru"""
        self._update_properties_size()
        self._update_properties_position()
        self._update_properties_value()
        
        # Ažuriraj ostale properties ako su prikazane
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj checkbox-ove ako postoje
            if hasattr(main_window, 'active_checkbox_scrollbar'):
                main_window.active_checkbox_scrollbar.blockSignals(True)
                main_window.active_checkbox_scrollbar.setChecked(self.active)
                main_window.active_checkbox_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'visible_checkbox_scrollbar'):
                main_window.visible_checkbox_scrollbar.blockSignals(True)
                main_window.visible_checkbox_scrollbar.setChecked(self.visible)
                main_window.visible_checkbox_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'static_checkbox_scrollbar'):
                main_window.static_checkbox_scrollbar.blockSignals(True)
                main_window.static_checkbox_scrollbar.setChecked(self.static)
                main_window.static_checkbox_scrollbar.blockSignals(False)
                
            if hasattr(main_window, '_3d_checkbox_scrollbar'):
                main_window._3d_checkbox_scrollbar.blockSignals(True)
                main_window._3d_checkbox_scrollbar.setChecked(self._3d)
                main_window._3d_checkbox_scrollbar.blockSignals(False)
            
            # Ažuriraj vrednosti ako postoje
            if hasattr(main_window, 'range_spin_scrollbar'):
                main_window.range_spin_scrollbar.blockSignals(True)
                main_window.range_spin_scrollbar.setValue(self.range_value)
                main_window.range_spin_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'current_value_spin_scrollbar'):
                main_window.current_value_spin_scrollbar.blockSignals(True)
                main_window.current_value_spin_scrollbar.setValue(self.current_value)
                main_window.current_value_spin_scrollbar.blockSignals(False)
                
            if hasattr(main_window, 'knob_size_spin_scrollbar'):
                main_window.knob_size_spin_scrollbar.blockSignals(True)
                main_window.knob_size_spin_scrollbar.setValue(self.knob_size)
                main_window.knob_size_spin_scrollbar.blockSignals(False)
            
            # Ažuriraj ime ako postoji
            if hasattr(main_window, 'name_edit_scrollbar'):
                main_window.name_edit_scrollbar.blockSignals(True)
                main_window.name_edit_scrollbar.setText(self.custom_name)
                main_window.name_edit_scrollbar.blockSignals(False)
            
            # Ažuriraj stack order ako postoji
            if hasattr(main_window, 'stack_order_spin_scrollbar'):
                main_window.stack_order_spin_scrollbar.blockSignals(True)
                # Pronađi indeks u listi svih shape-ova
                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index(main_window.current_shape) + 1
                    main_window.stack_order_spin_scrollbar.setValue(index)
                main_window.stack_order_spin_scrollbar.blockSignals(False)
            
            # Ažuriraj boje ako postoje
            if hasattr(main_window, 'track_color_rect_scrollbar'):
                main_window.track_color_rect_scrollbar.setStyleSheet(f"background-color: {self.track_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'thumb_color_rect_scrollbar'):
                main_window.thumb_color_rect_scrollbar.setStyleSheet(f"background-color: {self.thumb_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'border_color_rect_scrollbar'):
                main_window.border_color_rect_scrollbar.setStyleSheet(f"background-color: {self.border_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'white_border_color_rect_scrollbar'):
                main_window.white_border_color_rect_scrollbar.setStyleSheet(f"background-color: {self.white_border_color.name()}; border: 1px solid #ccc;")

    def get_track_rect(self):
        """Vraća pravougaonik za track (glavni deo scroll bar-a)"""
        w = self._width
        h = self._height
        
        # Polumjer za polukrugove
        radius = h // 2
        
        return QRect(radius, 0, w - 2 * radius, h)

    def get_thumb_rect(self):
        """Vraća pravougaonik za thumb (pokazivač)"""
        track_rect = self.get_track_rect()
        
        # Izračunaj veličinu thumb-a u pikselima
        thumb_width = int(track_rect.width() * (self.knob_size / 100.0))
        thumb_width = max(20, min(track_rect.width(), thumb_width))  # Min 20px
        
        # Izračunaj poziciju thumb-a baziranu na current_value
        max_position = track_rect.width() - thumb_width
        if max_position > 0:
            thumb_x = track_rect.x() + int((self.current_value / self.range_value) * max_position)
        else:
            thumb_x = track_rect.x()
        
        thumb_height = int(h * 0.6) if (h := self._height) > 20 else h - 4
        thumb_y = (h - thumb_height) // 2
        
        return QRect(thumb_x, thumb_y, thumb_width, thumb_height)

    def _calculate_value_from_position(self, x):
        """Izračunava vrednost na osnovu X koordinate"""
        track_rect = self.get_track_rect()
        thumb_rect = self.get_thumb_rect()
        
        # Relativna pozicija unutar track-a
        relative_x = x - track_rect.x() - thumb_rect.width() / 2
        track_width = track_rect.width() - thumb_rect.width()
        
        if track_width > 0:
            value = int((relative_x / track_width) * self.range_value)
            return max(0, min(self.range_value, value))
        return self.current_value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self._width
        h = self._height
        
        # Polumjer za polukrugove
        radius = h // 2
        
        # 1. Glavni track (tamnoplavi)
        pen = QPen(self.track_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(self.track_color)
        
        # Levi polukrug
        painter.drawPie(0, 0, 2 * radius, 2 * radius, 90*16, 180*16)
        # Centralni pravougaonik
        painter.drawRect(radius, 0, w - 2 * radius, h)
        # Desni polukrug
        painter.drawPie(w - 2 * radius, 0, 2 * radius, 2 * radius, 90*16, -180*16)
        
        # 2. Thumb (svetloplavi pokazivač)
        thumb_rect = self.get_thumb_rect()
        pen = QPen(self.thumb_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(self.thumb_color)
        
        # Crtanje thumb-a kao zaobljenog pravougaonika
        thumb_radius = thumb_rect.height() // 2
        
        # Levi polukrug thumb-a
        painter.drawPie(thumb_rect.x(), thumb_rect.y(), 
                       2 * thumb_radius, 2 * thumb_radius, 90*16, 180*16)
        # Centralni pravougaonik thumb-a
        painter.drawRect(thumb_rect.x() + thumb_radius, thumb_rect.y(), 
                        thumb_rect.width() - 2 * thumb_radius, thumb_rect.height())
        # Desni polukrug thumb-a
        painter.drawPie(thumb_rect.x() + thumb_rect.width() - 2 * thumb_radius, 
                       thumb_rect.y(), 2 * thumb_radius, 2 * thumb_radius, 90*16, -180*16)
        
        if self._3d:
            # 3. Gornji beli border (tanak) - gornja linija thumb-a
            pen = QPen(self.white_border_color)
            pen.setWidth(1)
            painter.setPen(pen)
            
            # Gornja linija thumb-a
            painter.drawLine(thumb_rect.x() + thumb_radius, thumb_rect.y(),
                            thumb_rect.x() + thumb_rect.width() - thumb_radius, thumb_rect.y())
            
            # Levi gornji luk thumb-a
            painter.drawArc(thumb_rect.x(), thumb_rect.y(),
                          2 * thumb_radius, 2 * thumb_radius, 90*16, 135*16)
            
            # 4. Donji beli border (deblji) - donja linija track-a
            pen.setWidth(3)
            painter.setPen(pen)
            
            # Donja linija track-a
            painter.drawLine(radius, h, w - radius, h)
            
            # Desni donji luk track-a
            painter.drawArc(w - 2 * radius, 0, 2 * radius, 2 * radius, 45*16, -135*16)
            
            # Levi donji luk track-a
            painter.drawArc(0, 0, 2 * radius, 2 * radius, 225*16, 45*16)
            
            # 5. Donji crni border (tanak) - donja linija thumb-a
            pen = QPen(self.border_color)
            pen.setWidth(1)
            painter.setPen(pen)
            
            # Donja linija thumb-a
            painter.drawLine(thumb_rect.x() + thumb_radius, thumb_rect.y() + thumb_rect.height(),
                            thumb_rect.x() + thumb_rect.width() - thumb_radius, thumb_rect.y() + thumb_rect.height())
            
            # Desni donji luk thumb-a
            painter.drawArc(thumb_rect.x() + thumb_rect.width() - 2 * thumb_radius, 
                          thumb_rect.y(), 2 * thumb_radius, 2 * thumb_radius, 45*16, -135*16)
            
            # 6. Gornji crni border (deblji) - gornja linija track-a
            pen.setWidth(3)
            painter.setPen(pen)
            
            # Gornja linija track-a
            painter.drawLine(radius, 0, w - radius, 0)
            
            # Desni gornji luk track-a
            painter.drawArc(w - 2 * radius, 0, 2 * radius, 2 * radius, 90*16, -45*16)
            
            # Levi gornji luk track-a
            painter.drawArc(0, 0, 2 * radius, 2 * radius, 90*16, 135*16)
        
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima scroll bar-a"""
        return {
            'type': 'ScrollBar',
            'name': getattr(self, 'custom_name', 'ScrollBar_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'active': getattr(self, 'active', True),
            'visible': getattr(self, 'visible', True),
            'static': getattr(self, 'static', False),
            '_3d': getattr(self, '_3d', True),
            'range_value': getattr(self, 'range_value', 100),
            'current_value': getattr(self, 'current_value', 50),
            'knob_size': getattr(self, 'knob_size', 30),
            'thumb_color': self.thumb_color.name(),
            'track_color': self.track_color.name(),
            'border_color': self.border_color.name(),
            'white_border_color': self.white_border_color.name()
        }

    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        main_window = self._find_main_window()
        if not main_window:
            return
            
        if hasattr(main_window, 'all_scrollbar_dicts'):
            if self.custom_name in main_window.all_scrollbar_dicts:
                main_window.all_scrollbar_dicts[self.custom_name] = self.get_properties_dict()
# U widgets.py, ažuriraj DialWidget klasu:

class DialWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, diameter, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        
        # Svojstva za dial
        self.dial_color = QColor(32, 64, 128)  # Fiksna boja kao što je navedeno
        self.arc_color = QColor(0, 0, 0)       # Crni luk
        self.line_color = QColor(0, 0, 0)  # Siva linija (kazaljka)
        self.background_color = QColor(32, 64, 128)   # Plava pozadina (fiksna)
        
        # Dodatna svojstva
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True
        self.value = 0  # Vrednost od 0-100
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Resize i drag varijable - DODAJ OVO!
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Za rečnik
        self.custom_name = None
        self.stack_order = 1

    def get_scaled_value(self, original_value):
        """Vraća vrednost skaliranu u odnosu na originalni dijametar"""
        scale_factor = self.diameter / 100.0  # Originalni dijametar je 100
        return int(original_value * scale_factor)

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_diameter(self, diameter):
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.update()

    def set_dial_color(self, color):
        self.dial_color = color
        self.update()

    def set_arc_color(self, color):
        self.arc_color = color
        self.update()

    def set_line_color(self, color):
        self.line_color = color
        self.update()

    def set_background_color(self, color):
        self.background_color = color
        self.update()

    def set_active(self, active):
        self.active = active
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)

    def set_static(self, static):
        self.static = static
        self.update()

    def set_custom_name(self, name):
        self.custom_name = name

    def set_stack_order(self, order):
        self.stack_order = order

    def set_3d(self, _3d):
        self._3d = _3d
        self.update()

    def set_value(self, value):
        self.value = max(0, min(value, 100))  # Clamp između 0 i 100
        self.update()

    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima dial-a"""
        return {
            'type': 'Dial',
            'name': getattr(self, 'custom_name', 'Dial_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'diameter': self.diameter,
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            '3d': self._3d,
            'value': self.value,
            'dial_color': self.dial_color.name(),
            'arc_color': self.arc_color.name(),
            'line_color': self.line_color.name(),
            'background_color': self.background_color.name()
        }

    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        if hasattr(self, 'custom_name') and hasattr(self.window(), 'all_dial_dicts'):
            main_window = self.window()
            if self.custom_name in main_window.all_dial_dicts:
                main_window.all_dial_dicts[self.custom_name] = self.get_properties_dict()

    # Metode za resize i drag (kao GaugeWidget)
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos
                
                self.clicked.emit(self)
                # Ažuriraj sve properties kada se selektuje
                self.update_all_properties()

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar U TOKU draganja (real-time)
            self._update_properties_position()
        
        event.accept()

    # Izmeni mouseReleaseEvent da ažurira properties
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar NAKON što se završi drag ili resize
            self._update_properties_size()
            self._update_properties_position()
            
            # Ažuriraj rečnik
            self.update_properties_dict()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Menja veličinu DialWidget-a"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu
        if self.resize_corner == "bottom_right":
            new_width = max(50, self.resize_start_size.width() + delta.x())
            new_height = max(50, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(50, self.resize_start_size.width() + delta.x())
            new_height = max(50, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(50, self.resize_start_size.width() - delta.x())
            new_height = max(50, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(50, self.resize_start_size.width() - delta.x())
            new_height = max(50, self.resize_start_size.height() - delta.y())

        # Za dial, width i height moraju biti isti (krug je uvek kvadrat)
        size = min(new_width, new_height)
        
        # Ažuriraj samo veličinu (bez promene pozicije)
        self.setFixedSize(size, size)
        self.diameter = size
        self.update()

        # Ažuriraj properties bar U TOKU resize-a (real-time)
        self._update_properties_size()
        self._update_properties_position()  # Ovo je važno jer se pozicija menja ako resize-ujemo sa leve/gornje strane

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj diameter spin ako postoji u properties baru
            if hasattr(main_window, 'diameter_spin_dial'):
                main_window.diameter_spin_dial.blockSignals(True)
                main_window.diameter_spin_dial.setValue(self.diameter)
                main_window.diameter_spin_dial.blockSignals(False)

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj position spin-ove ako postoje u properties baru
            if hasattr(main_window, 'pos_x_spin_dial'):
                main_window.pos_x_spin_dial.blockSignals(True)
                main_window.pos_x_spin_dial.setValue(self.x())
                main_window.pos_x_spin_dial.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin_dial'):
                main_window.pos_y_spin_dial.blockSignals(True)
                main_window.pos_y_spin_dial.setValue(self.y())
                main_window.pos_y_spin_dial.blockSignals(False)

    def update_all_properties(self):
        """Ažurira sve properties u properties baru"""
        self._update_properties_size()
        self._update_properties_position()
        # Ažuriraj ostale properties ako su prikazane
        main_window = self._find_main_window()
        if not main_window:
            return
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            # Ažuriraj checkbox-ove ako postoje
            if hasattr(main_window, 'active_checkbox_dial'):
                main_window.active_checkbox_dial.blockSignals(True)
                main_window.active_checkbox_dial.setChecked(self.active)
                main_window.active_checkbox_dial.blockSignals(False)
            if hasattr(main_window, 'visible_checkbox_dial'):
                main_window.visible_checkbox_dial.blockSignals(True)
                main_window.visible_checkbox_dial.setChecked(self.visible)
                main_window.visible_checkbox_dial.blockSignals(False)
            if hasattr(main_window, '_3d_checkbox_dial'):
                main_window._3d_checkbox_dial.blockSignals(True)
                main_window._3d_checkbox_dial.setChecked(self._3d)
                main_window._3d_checkbox_dial.blockSignals(False)
            # Ažuriraj value spin ako postoji
            if hasattr(main_window, 'value_spin_dial'):
                main_window.value_spin_dial.blockSignals(True)
                main_window.value_spin_dial.setValue(self.value)
                main_window.value_spin_dial.blockSignals(False)
            # Ažuriraj ime ako postoji
            if hasattr(main_window, 'name_edit_dial'):
                main_window.name_edit_dial.blockSignals(True)
                main_window.name_edit_dial.setText(self.custom_name)
                main_window.name_edit_dial.blockSignals(False)
            # Ažuriraj stack order ako postoji
            if hasattr(main_window, 'stack_order_spin_dial'):
                main_window.stack_order_spin_dial.blockSignals(True)
                # Pronađi indeks u listi svih shape-ova
                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index(main_window.current_shape) + 1
                    main_window.stack_order_spin_dial.setValue(index)
                main_window.stack_order_spin_dial.blockSignals(False)            

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        r = self.diameter
        
        # Širine linija skalirane prema veličini
        base_line_width = max(1, int(r / 100))
        arc_line_width = max(1, self.get_scaled_value(3))
        line_width = max(1, self.get_scaled_value(3))
        
        # KORIGUJEMO: Dodaj marginu da ne bude odsečeno od selekcionog okvira
        margin = 3  # Dodaj marginu (selekcioni okvir je 2px + 1px sigurnosna margina)
        adjusted_r = r - 2 * margin
        
        # Ako je 3D efekat uključen, dodaj sjene
        if self._3d:
            # Crni luk - SA MARGINOM
            pen = QPen(self.arc_color)
            pen.setWidth(arc_line_width)
            painter.setPen(pen)
            painter.drawArc(margin, margin, adjusted_r, adjusted_r, 16*35, -16*175)
    
            # Sivi luk i linija - SA MARGINOM
            pen = QPen(QColor(255, 255, 255))
            pen.setWidth(line_width)
            painter.setPen(pen)
            painter.drawArc(margin, margin, adjusted_r, adjusted_r, 35*16, 16*185)
        
        # Glavni krug (plavi) - SA MARGINOM
        pen = QPen(self.dial_color)
        pen.setWidth(base_line_width)
        painter.setPen(pen)
        painter.setBrush(self.background_color)
        painter.drawEllipse(margin, margin, adjusted_r, adjusted_r)
        
        # Sivi luk i linija
        pen = QPen(self.line_color)
        pen.setWidth(line_width)
        painter.setPen(pen)
        
 # Kazaljka (linija) - skalirana prema vrednosti
        pen.setWidth(max(1, self.get_scaled_value(4)))
        painter.setPen(pen)

        # Centar kazaljke treba da bude u centru kruga (sa marginom)
        center_x = margin + adjusted_r // 2
        center_y = margin + adjusted_r // 2

        # Dužina kazaljke
        radius = adjusted_r // 2 - 10  # Kraj kazaljke

        # START POZICIJA KAZALJKE: pomeri od centra ka obodu
        # Umesto da počinje od centra (0% radiusa), počinje na 20% radiusa od centra
        start_radius_percentage = 0.70  # 20% od centra (0.0 = centar, 1.0 = obod)
        start_radius = radius * start_radius_percentage

        # Izračunaj ugao kazaljke prema vrednosti (0-100 mapirano na -135 do 135 stepeni)
        angle = -90+ (360 * self.value / 100)
        angle_rad = math.radians(angle)

        # START kazaljke (pomerena od centra)
        start_x = center_x + start_radius * math.cos(angle_rad)
        start_y = center_y + start_radius * math.sin(angle_rad)

        # KRAJ kazaljke (na kraju radiusa)
        end_x = center_x + radius * math.cos(angle_rad)
        end_y = center_y + radius * math.sin(angle_rad)

        # Crtanje kazaljke od start pozicije do end pozicije
        painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))
    
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            # Ukloni ovo: painter.setPen(QPen(self.selection_color, 2, Qt.PenStyle.DashLine))
            # Ukloni ovo: painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
            # Ukloni ovo: painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
            
            # Nacrtaj resize handle-ove (ovo će nacrtati i selekcioni okvir)
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

class SliderWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        
        # Svojstva za slider
        self.track_color = QColor(0, 32, 64)  # Tamnoplava - desna strana (track)
        self.thumb_color = QColor(255, 255, 255)  # Bela - leva strana (progress)
        self.progress_color = QColor(0, 32, 64)  # Tamnoplava - thumb (krug)
        self.border_color = QColor(0, 0, 0)  # Crni border
        
        # Dodatna svojstva
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True  # Dodaj 3D atribut
        self.custom_name = None
        self.stack_order = 1
        
        # Progress vrednost (0-100)
        self.value = 50
        
        # Resize i drag varijable
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        # Selekcija
        self.selected = False
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_size(self, width, height):
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        self.update()

    def get_width(self):
        """Getter za width"""
        return self._width

    def get_height(self):
        """Getter za height"""
        return self._height

    def set_track_color(self, color):
        self.track_color = color
        self.update()

    def set_thumb_color(self, color):
        self.thumb_color = color
        self.update()

    def set_progress_color(self, color):
        self.progress_color = color
        self.update()

    def set_border_color(self, color):
        self.border_color = color
        self.update()

    def set_value(self, value):
        """Postavlja vrednost slidera (0-100)"""
        self.value = max(0, min(100, value))
        self.update()

    def get_value(self):
        """Getter za vrednost slidera"""
        return self.value

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()

    def set_3d(self, three_d):
        self._3d = three_d
        self.update()  # OVO JE KLJUČNO - forsira repaint

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj width i height spin-ove ako postoje u properties baru
            if hasattr(main_window, 'width_spin_slider'):
                main_window.width_spin_slider.blockSignals(True)
                main_window.width_spin_slider.setValue(self._width)
                main_window.width_spin_slider.blockSignals(False)
                
            if hasattr(main_window, 'height_spin_slider'):
                main_window.height_spin_slider.blockSignals(True)
                main_window.height_spin_slider.setValue(self._height)
                main_window.height_spin_slider.blockSignals(False)

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        # Proveri da li je ovaj widget trenutno selektovan
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj position spin-ove ako postoje u properties baru
            if hasattr(main_window, 'pos_x_spin_slider'):
                main_window.pos_x_spin_slider.blockSignals(True)
                main_window.pos_x_spin_slider.setValue(self.x())
                main_window.pos_x_spin_slider.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin_slider'):
                main_window.pos_y_spin_slider.blockSignals(True)
                main_window.pos_y_spin_slider.setValue(self.y())
                main_window.pos_y_spin_slider.blockSignals(False)

    def update_all_properties(self):
        """Ažurira sve properties u properties baru"""
        self._update_properties_size()
        self._update_properties_position()
        
        # Ažuriraj ostale properties ako su prikazane
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj checkbox-ove ako postoje
            if hasattr(main_window, 'active_checkbox_slider'):
                main_window.active_checkbox_slider.blockSignals(True)
                main_window.active_checkbox_slider.setChecked(self.active)
                main_window.active_checkbox_slider.blockSignals(False)
                
            if hasattr(main_window, 'visible_checkbox_slider'):
                main_window.visible_checkbox_slider.blockSignals(True)
                main_window.visible_checkbox_slider.setChecked(self.visible)
                main_window.visible_checkbox_slider.blockSignals(False)
                
            if hasattr(main_window, 'static_checkbox_slider'):
                main_window.static_checkbox_slider.blockSignals(True)
                main_window.static_checkbox_slider.setChecked(self.static)
                main_window.static_checkbox_slider.blockSignals(False)
                
            if hasattr(main_window, '_3d_checkbox_slider'):
                main_window._3d_checkbox_slider.blockSignals(True)
                main_window._3d_checkbox_slider.setChecked(self._3d)
                main_window._3d_checkbox_slider.blockSignals(False)
            
            # Ažuriraj value spin ako postoji
            if hasattr(main_window, 'value_spin_slider'):
                main_window.value_spin_slider.blockSignals(True)
                main_window.value_spin_slider.setValue(self.value)
                main_window.value_spin_slider.blockSignals(False)
            
            # Ažuriraj ime ako postoji
            if hasattr(main_window, 'name_edit_slider'):
                main_window.name_edit_slider.blockSignals(True)
                main_window.name_edit_slider.setText(self.custom_name)
                main_window.name_edit_slider.blockSignals(False)
            
            # Ažuriraj stack order ako postoji
            if hasattr(main_window, 'stack_order_spin_slider'):
                main_window.stack_order_spin_slider.blockSignals(True)
                # Pronađi indeks u listi svih shape-ova
                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index(main_window.current_shape) + 1
                    main_window.stack_order_spin_slider.setValue(index)
                main_window.stack_order_spin_slider.blockSignals(False)
            
            # Ažuriraj boje ako postoje
            if hasattr(main_window, 'bg_left_color_rect_slider'):
                main_window.bg_left_color_rect_slider.setStyleSheet(f"background-color: {self.thumb_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'bg_right_color_rect_slider'):
                main_window.bg_right_color_rect_slider.setStyleSheet(f"background-color: {self.track_color.name()}; border: 1px solid #ccc;")
                
            if hasattr(main_window, 'knob_color_rect_slider'):
                main_window.knob_color_rect_slider.setStyleSheet(f"background-color: {self.progress_color.name()}; border: 1px solid #ccc;")

    # Metode za resize i drag
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos
                
                # Proveri da li je klik na thumb (krug) ili track
                thumb_rect = self.get_thumb_rect()
                if thumb_rect.contains(event.pos()):
                    # Klik na thumb - za buduću implementaciju draganja thumb-a
                    pass
                else:
                    # Klik na track - pomeri thumb na tu poziciju
                    track_rect = self.get_track_rect()
                    if track_rect.contains(event.pos()):
                        relative_x = event.pos().x() - track_rect.x()
                        new_value = int((relative_x / track_rect.width()) * 100)
                        self.set_value(new_value)
                
                self.clicked.emit(self)
                # Ažuriraj sve properties kada se selektuje
                self.update_all_properties()

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi odgovarajući kursor
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
            # Ažuriraj properties bar U TOKU resize-a
            self._update_properties_size()
            self._update_properties_position()
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar U TOKU draganja (real-time)
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj properties bar NAKON što se završi drag ili resize
            self._update_properties_size()
            self._update_properties_position()
            
            # Ažuriraj rečnik
            self.update_properties_dict()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Menja veličinu SliderWidget-a"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        # Svi uglovi mogu da menjaju veličinu
        if self.resize_corner == "bottom_right":
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(30, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(100, self.resize_start_size.width() + delta.x())
            new_height = max(30, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(100, self.resize_start_size.width() - delta.x())
            new_height = max(30, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(100, self.resize_start_size.width() - delta.x())
            new_height = max(30, self.resize_start_size.height() - delta.y())

        self.set_size(new_width, new_height)

    def get_track_rect(self):
        """Vraća pravougaonik za track (deo između polukrugova)"""
        w = self._width
        h = self._height
        
        # Track zauzima centralni deo, sa polukrugovima na krajevima
        track_height = h // 3  # Track zauzima trećinu visine
        track_y = h // 3  # Centriran vertikalno
        
        # Polukrugovi na krajevima
        radius = h // 6  # Polumjer polukrugova
        
        return QRect(radius, track_y, w - 2 * radius, track_height)

    def get_progress_rect(self):
        """Vraća pravougaonik za progress deo (leva strana)"""
        track_rect = self.get_track_rect()
        progress_width = int(track_rect.width() * self.value / 100)
        
        return QRect(track_rect.x(), track_rect.y(), progress_width, track_rect.height())

    def get_track_right_rect(self):
        """Vraća pravougaonik za desnu stranu track-a (deo desno od thumb-a)"""
        track_rect = self.get_track_rect()
        thumb_rect = self.get_thumb_rect()
        
        # Počinje od desne ivice thumb-a do kraja track-a
        start_x = thumb_rect.x() + thumb_rect.width()
        width = track_rect.x() + track_rect.width() - start_x
        
        if width > 0:
            return QRect(start_x, track_rect.y(), width, track_rect.height())
        return QRect()  # Prazan pravougaonik ako nema prostora

    def get_thumb_rect(self):
        """Vraća pravougaonik za thumb (krug)"""
        track_rect = self.get_track_rect()
        
        # Thumb je krug koji se pomera po track-u
        thumb_diameter = min(track_rect.height() * 2, self._height * 0.8)  # 80% visine ili 2x track visina
        thumb_radius = thumb_diameter // 2
        
        # Pozicija thumb-a bazirana na vrednosti
        thumb_x = track_rect.x() + int((track_rect.width() - thumb_diameter) * (self.value / 100))
        thumb_y = (self._height - thumb_diameter) // 2  # Centriran vertikalno
        
        return QRect(thumb_x, thumb_y, thumb_diameter, thumb_diameter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self._width
        h = self._height

        # Pravougaonici
        track_rect = self.get_track_rect()
        progress_rect = self.get_progress_rect()
        thumb_rect = self.get_thumb_rect()
        track_right_rect = self.get_track_right_rect()

        radius = track_rect.height() // 2

        # 1. CELI TRACK - osnova (crni outline)
        pen = QPen(self.border_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Levi polukrug track-a (outline)
        painter.drawArc(track_rect.x() - radius, track_rect.y(), 
                       radius * 2, radius * 2, 90*16, 180*16)

        # Desni polukrug track-a (outline)
        painter.drawArc(track_rect.x() + track_rect.width() - radius, track_rect.y(),
                       radius * 2, radius * 2, 90*16, -180*16)

        # Gornja i donja linija track-a (outline)
        painter.drawLine(track_rect.x(), track_rect.y(), 
                        track_rect.x() + track_rect.width(), track_rect.y())
        painter.drawLine(track_rect.x(), track_rect.y() + track_rect.height(),
                        track_rect.x() + track_rect.width(), track_rect.y() + track_rect.height())

        # 2. DESNA STRANA TRACK-A (tamnoplava) - popunjava prostor DESNO od thumb-a
        if track_right_rect.width() > 0:
            pen = QPen(self.track_color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(self.track_color)

            # Desni deo pravougaonika
            if track_right_rect.width() > radius:
                # Iscrtaj desni polukrug
                painter.drawPie(track_rect.x() + track_rect.width() - radius, track_rect.y(),
                              radius * 2, radius * 2, 90*16, -180*16)

                # Iscrtaj desni deo pravougaonika
                painter.drawRect(track_right_rect.x(), track_rect.y(),
                               track_right_rect.width(), track_rect.height())
            else:
                # Ako je mali prostor, samo popuni šta može
                painter.drawRect(track_right_rect.x(), track_rect.y(),
                               track_right_rect.width(), track_rect.height())

        # 3. LEVA STRANA TRACK-A (progress - bela) - popunjava prostor LEVO od thumb-a
        if progress_rect.width() > 0:
            pen = QPen(self.thumb_color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(self.thumb_color)

            # Levi deo pravougaonika
            if progress_rect.width() > radius:
                # Iscrtaj levi polukrug
                painter.drawPie(track_rect.x() - radius, track_rect.y(),
                              radius * 2, radius * 2, 90*16, 180*16)

                # Iscrtaj levi deo pravougaonika (do thumb-a)
                painter.drawRect(track_rect.x(), track_rect.y(),
                               progress_rect.width() - radius, track_rect.height())
            else:
                # Ako je progress mali, samo popuni šta može
                painter.drawRect(track_rect.x(), track_rect.y(),
                               progress_rect.width(), track_rect.height())

            if track_right_rect.width() > 0:
                # Tamna linija ispod desnog dela
                pen = QPen(QColor(0, 0, 0))
                pen.setWidth(2)
                painter.setPen(pen)

                painter.drawLine(track_rect.x(), track_rect.y()-1, track_rect.x() + progress_rect.width(), track_rect.y()-1)
                painter.drawLine(track_rect.x(), track_rect.y() + progress_rect.height()+1, track_rect.x() + progress_rect.width(), track_rect.y() + progress_rect.height()+1)
                painter.drawArc(track_rect.x() - radius-1, track_rect.y()-1, radius * 2+2, radius * 2+2, 90*16, 180*16)

        # 4. THUMB (tamnoplavi krug) - preklapa oba dela
        pen = QPen(self.progress_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(self.progress_color)
        painter.drawEllipse(thumb_rect)

        # 5. 3D efekti ako je uključen
        if self._3d:
            # 3D efekti za track
            if progress_rect.width() > 0:
                # Svetla linija iznad progress dela
                pen = QPen(QColor(255, 255, 255))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(track_right_rect.x(), track_rect.y()-1, track_rect.x() + track_rect.width(), track_rect.y()-1)
                painter.drawLine(track_right_rect.x(), track_rect.y() + progress_rect.height()+1, track_rect.x() + track_rect.width(), track_rect.y() + progress_rect.height()+1)
                painter.drawArc(track_rect.x() + track_rect.width() - radius-1, track_rect.y()-1, radius * 2+2, radius * 2+2, 90*16, -180*16)

            # 3D efekti za thumb - BELI LUK (gornja polovina: od 45° do 225°)
            pen = QPen(QColor(236, 238, 241))  # Svetlo siva/bela boja
            pen.setWidth(1)
            painter.setPen(pen)
            # Crtanje belog luka (gornja polovina)
            painter.drawArc(thumb_rect, 40*16, 160*16)

            # 3D efekti za thumb - CRNI LUK (donja polovina: od 225° do 45°)
            pen = QPen(QColor(0, 0, 0))  # Crna boja
            pen.setWidth(1)
            painter.setPen(pen)
            # Crtanje crnog luka (donja polovina)
            # 225° = 225 * 16 = 3600, 180° = 180 * 16 = 2880
            painter.drawArc(thumb_rect, 200*16, 180*16)


        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima slider-a"""
        return {
            'type': 'Slider',
            'name': getattr(self, 'custom_name', 'Slider_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'active': getattr(self, 'active', True),
            'visible': getattr(self, 'visible', True),
            'static': getattr(self, 'static', False),
            '_3d': getattr(self, '_3d', False),
            'value': self.value,
            'knob_color': self.progress_color.name(),           # Knob (krug)
            'background_left_color': self.thumb_color.name(),   # Leva strana (progress)
            'background_right_color': self.track_color.name(),  # Desna strana (track)
            'border_color': self.border_color.name()
        }

    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        main_window = self._find_main_window()
        if not main_window:
            return
            
        if hasattr(main_window, 'all_slider_dicts'):
            if self.custom_name in main_window.all_slider_dicts:
                main_window.all_slider_dicts[self.custom_name] = self.get_properties_dict()

class ToggleWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height  # Fiksna visina 30
        self.setFixedSize(width, height)
        
        # Svojstva za toggle
        self.track_color = QColor(0, 32, 64)  # Tamnoplava - track
        self.thumb_color = QColor(0, 64, 128)  # Svetloplava - thumb (knob)
        self.border_color = QColor(0, 0, 0)    # Crni border
        self.white_border_color = QColor(236, 238, 241)  # Sivi/beli border
        self.text_color = QColor(255, 255, 255)  # Bela boja teksta
        self.background_color = QColor(0, 32, 64)  # Background color
        
        # Stanje toggle-a (True = ON, False = OFF)
        self.is_on = True
        
        # Dodatna svojstva
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Proporcije bazirane na originalu (width=250, height=150)
        self.original_width = 250
        self.original_height = 150
        
        # Resize i drag varijable
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Za rečnik
        self.custom_name = None
        self.stack_order = 1

    def get_scaled_value(self, original_value, is_width=True):
        """Vraća vrednost skaliranu u odnosu na originalne dimenzije"""
        if is_width:
            scale_factor = self._width / self.original_width
        else:
            scale_factor = self._height / self.original_height
        return int(original_value * scale_factor)

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_size(self, width, height):
        self._width = width
        self._height = 30  # Fiksna visina
        self.setFixedSize(width, self._height)
        self.update()
    
    # OVERRIDE MOVE METODA
    def move(self, x, y):
        super().move(x, y)
        
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            try:
                if hasattr(main_window, 'pos_x_spin_toggle'):
                    main_window.pos_x_spin_toggle.blockSignals(True)
                    main_window.pos_x_spin_toggle.setValue(x)
                    main_window.pos_x_spin_toggle.blockSignals(False)
            except RuntimeError:
                pass
            
            try:
                if hasattr(main_window, 'pos_y_spin_toggle'):
                    main_window.pos_y_spin_toggle.blockSignals(True)
                    main_window.pos_y_spin_toggle.setValue(y)
                    main_window.pos_y_spin_toggle.blockSignals(False)
            except RuntimeError:
                pass

    # OVERRIDE RESIZE METODA
    def resize(self, width, height):
        super().resize(width, height)
        self._width = width
        
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            try:
                if hasattr(main_window, 'width_spin_toggle'):
                    main_window.width_spin_toggle.blockSignals(True)
                    main_window.width_spin_toggle.setValue(width)
                    main_window.width_spin_toggle.blockSignals(False)
            except RuntimeError:
                pass

    def get_width(self):
        """Getter za width"""
        return self._width

    def get_height(self):
        """Getter za height"""
        return self._height

    def set_track_color(self, color):
        self.track_color = color
        self.update()

    def set_thumb_color(self, color):
        self.thumb_color = color
        self.update()

    def set_border_color(self, color):
        self.border_color = color
        self.update()

    def set_white_border_color(self, color):
        self.white_border_color = color
        self.update()

    def set_text_color(self, color):
        self.text_color = color
        self.update()

    def set_background_color(self, color):
        self.background_color = color
        self.update()

    def set_state(self, is_on):
        """Postavlja stanje toggle-a (True = ON, False = OFF)"""
        self.is_on = is_on
        self.update()
        
        # Ažuriraj state checkbox u properties bar-u
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            try:
                if hasattr(main_window, 'state_checkbox_toggle'):
                    main_window.state_checkbox_toggle.blockSignals(True)
                    main_window.state_checkbox_toggle.setChecked(self.is_on)
                    main_window.state_checkbox_toggle.blockSignals(False)
            except RuntimeError:
                pass

    def get_state(self):
        """Getter za stanje toggle-a"""
        return self.is_on

    def set_active(self, active):
        self.active = active
        self.setEnabled(active)
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()

    def set_static(self, static):
        self.static = static
        self.update()

    def set_3d(self, _3d):
        self._3d = _3d
        self.update()

    def toggle_state(self):
        """Menja stanje toggle-a"""
        self.set_state(not self.is_on)

    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima toggle-a"""
        return {
            'type': 'Toggle',
            'name': getattr(self, 'custom_name', 'Toggle_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            '3d': self._3d,
            'state': self.is_on,
            'track_color': self.track_color.name(),
            'thumb_color': self.thumb_color.name(),
            'border_color': self.border_color.name(),
            'white_border_color': self.white_border_color.name(),
            'text_color': self.text_color.name(),
            'background_color': self.background_color.name()
        }

    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        if hasattr(self, 'custom_name') and hasattr(self.window(), 'all_toggle_dicts'):
            main_window = self.window()
            if self.custom_name in main_window.all_toggle_dicts:
                main_window.all_toggle_dicts[self.custom_name] = self.get_properties_dict()

    # Metode za resize i drag
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima kada je selektovano"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # Samo levi i desni ugao (jer može samo width da se menja)
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))

    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje ili selektuj
                self.dragging = True
                self.drag_start_pos = mouse_pos

                # Ako je klik na thumb, promeni stanje
                thumb_rect = self.get_thumb_rect()
                if thumb_rect.contains(event.pos()):
                    self.toggle_state()
                    self.update_properties_dict()

                self.clicked.emit(self)

        event.accept()

    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()

        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            # Postavi horizontalni kursor za resize
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos

            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            self.move(new_x, new_y)

        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            # Ažuriraj rečnik
            self.update_properties_dict()

        event.accept()

    def _get_corner_at(self, pos):
        """Proverava da li je miš preko nekog od uglova za resize"""
        handle_size = 12  # Veća zona za lakše hvatanje
        half_size = handle_size // 2
        
        corners = {
            "left": QPoint(0, self.height() // 2),
            "right": QPoint(self.width(), self.height() // 2)
        }
        
        for corner_name, corner_pos in corners.items():
            # Kreiraj pravougaonik oko ugla
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None

    def _handle_resize(self, global_pos):
        """Menja veličinu ToggleWidget-a (samo width)"""
        if not self.resize_corner:
            return

        # Računaj promenu u veličini
        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()

        # Samo width se menja
        if self.resize_corner == "right":
            new_width = max(80, self.resize_start_size.width() + delta.x())
        elif self.resize_corner == "left":
            new_width = max(80, self.resize_start_size.width() - delta.x())
            # Ako se menja leva strana, pomeri widget
            width_delta = self._width - new_width
            self.move(self.x() + width_delta, self.y())

        self.set_size(new_width, self._height)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def get_thumb_rect(self):
        """Vraća pravougaonik thumb-a"""
        # Visina thumb-a je fiksna proporcija
        thumb_height = self._height - 10
        thumb_width = thumb_height
        
        if self.is_on:
            # Thumb je na desnoj strani (ON pozicija)
            thumb_x = self._width - thumb_width - 5
        else:
            # Thumb je na levoj strani (OFF pozicija)
            thumb_x = 5
            
        thumb_y = 5
        
        return QRect(thumb_x, thumb_y, thumb_width, thumb_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self._width
        h = self._height
        
        # Background
        pen = QPen(self.track_color)
        painter.setPen(pen)
        painter.setBrush(self.background_color)
        
        # Polumjer polukrugova je h/2
        radius = h // 2
        
        # Centralni pravougaonik
        painter.drawRect(radius, 0, w - 2 * radius, h)
        
        # Levi polukrug
        painter.drawPie(0, 0, 2 * radius, 2 * radius, 90 * 16, 180 * 16)
        
        # Desni polukrug
        painter.drawPie(w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, -180 * 16)
        
        if self._3d:
            # Donji beli border
            pen = QPen(self.white_border_color)
            pen.setWidth(2)
            painter.setPen(pen)
            radius = h // 2
            
            # Donja linija
            painter.drawLine(radius, h, w - radius, h)

            # Desni donji luk
            painter.drawArc(w - 2 * radius, 0, 2 * radius, 2 * radius, 45 * 16, -135 * 16)

            # Levi donji luk
            painter.drawArc(0, 0, 2 * radius, 2 * radius, 225 * 16, 45 * 16)
            
            pen = QPen(self.border_color)
            pen.setWidth(3)
            painter.setPen(pen)

            # Gornja linija
            painter.drawLine(radius, 0, w - radius, 0)

            # Levi gornji luk
            painter.drawArc(0, 0, 2 * radius, 2 * radius, 90 * 16, 135 * 16)

            # Desni gornji luk
            painter.drawArc(w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, -45 * 16)
        
        # Thumb (knob)
        thumb_rect = self.get_thumb_rect()
        pen = QPen(self.thumb_color)
        painter.setPen(pen)
        painter.setBrush(self.thumb_color)
        
        # Crtanje thumb-a kao elipse
        painter.drawEllipse(thumb_rect)
        
        # Tekst (ON/OFF)
        font = QFont()
        font_size = max(8, h // 2)
        font.setPointSize(font_size)
        painter.setFont(font)
        painter.setPen(self.text_color)
        
        if self.is_on:
            # Thumb je desno, tekst "OFF" levo
            text_rect = QRect(10, 0, w - thumb_rect.width() - 20, h)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "OFF")
        else:
            # Thumb je levo, tekst "ON" desno
            text_rect = QRect(thumb_rect.width() + 10, 0, w - thumb_rect.width() - 20, h)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, "ON")
        
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)

class LabelWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        
        # Svojstva za label
        self.text_color = QColor(0, 0, 0)             # Crni tekst
        self.text = "Text"                            # Tekst labele
        
        # Dodatna svojstva
        self.active = True
        self.visible = True
        self.static = False
        
        # Text properties
        self.text_size = 12
        self.text_font = "Arial"
        self.text_alignment = "Left"  # Left, Right, Top, Bottom
        
        # Selekcija
        self.selected = False
        self.selection_color = QColor(255, 0, 0)
        
        # Drag varijable - DODAJ OVO!
        self.dragging = False
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Za rečnik
        self.custom_name = None
        self.stack_order = 1

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def set_size_based_on_text(self):
        """Postavlja veličinu widget-a na osnovu teksta"""
        painter = QPainter(self)
        font = QFont(self.text_font, self.text_size)
        font_metrics = QFontMetrics(font)
        
        text_width = font_metrics.horizontalAdvance(self.text) + 20  # +20 za margin
        text_height = font_metrics.height() + 10  # +10 za margin
        
        self._width = max(50, text_width)
        self._height = max(30, text_height)
        self.setFixedSize(self._width, self._height)
        
        painter.end()
        self.update()

    def get_width(self):
        """Getter za width"""
        return self._width

    def get_height(self):
        """Getter za height"""
        return self._height

    def set_text_color(self, color):
        self.text_color = color
        self.update()

    def set_text(self, text):
        self.text = text
        self.set_size_based_on_text()
        self.update()

    def set_text_size(self, size):
        self.text_size = size
        self.set_size_based_on_text()
        self.update()

    def set_text_font(self, font):
        self.text_font = font
        self.set_size_based_on_text()
        self.update()

    def set_text_alignment(self, alignment):
        self.text_alignment = alignment
        self.update()

    def set_active(self, active):
        self.active = active
        self.setEnabled(active)
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()

    def set_static(self, static):
        self.static = static
        self.update()

    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima label-a"""
        return {
            'type': 'Label',
            'name': getattr(self, 'custom_name', 'Label_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'text': self.text,
            'text_color': self.text_color.name(),
            'text_size': self.text_size,
            'text_font': self.text_font,
            'text_alignment': self.text_alignment
        }

    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        if hasattr(self, 'custom_name') and hasattr(self.window(), 'all_label_dicts'):
            main_window = self.window()
            if self.custom_name in main_window.all_label_dicts:
                main_window.all_label_dicts[self.custom_name] = self.get_properties_dict()

    # Metode za drag
    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.pos()
            self.clicked.emit(self)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and (event.buttons() & Qt.MouseButton.LeftButton):
            # Dragovanje widgeta
            delta = event.pos() - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar ako postoji
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            # Ažuriraj properties bar
            self._update_properties_position()
            # Ažuriraj rečnik
            self.update_properties_dict()
        event.accept()

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self and
            hasattr(main_window, 'pos_x_spin') and 
            hasattr(main_window, 'pos_y_spin')):
            
            main_window.pos_x_spin.blockSignals(True)
            main_window.pos_x_spin.setValue(self.x())
            main_window.pos_x_spin.blockSignals(False)
            
            main_window.pos_y_spin.blockSignals(True)
            main_window.pos_y_spin.setValue(self.y())
            main_window.pos_y_spin.blockSignals(False)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Crtanje teksta
        painter.setPen(self.text_color)
        font = QFont(self.text_font, self.text_size)
        painter.setFont(font)
        
        # Određivanje pozicije teksta na osnovu alignment-a
        text_rect = QRect(0, 0, self._width, self._height)
        
        alignment_flags = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        
        if self.text_alignment == "Left":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        elif self.text_alignment == "Center":
            alignment_flags =Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter 
        elif self.text_alignment == "Right":
            alignment_flags = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        elif self.text_alignment == "Top":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        elif self.text_alignment == "Bottom":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        else:
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

        painter.drawText(text_rect, alignment_flags, self.text)
        
        painter.drawText(text_rect, alignment_flags, self.text)
        
        # Ako je selektovan, nacrtaj selekcioni okvir
        if self.selected:
            self._draw_selection_border(painter)

class ImageWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width=100, height=100, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height
        
        # Status properties (konzistentno sa drugim widget-ima)
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.stack_order = 1
        
        # Geometry properties
        self._x = 0
        self._y = 0
        
        # Frame properties
        self.frame_enabled = False
        self.frame_color = QColor(255, 0, 0)  # Crna boja okvira
        self.frame_width = 3
        
        # Background color (za slučaj kad nema slike)
        self.background_color = QColor(255, 255, 255)  # Svetlo siva
        
        # Image properties
        self.image_path = ""
        self.pixmap = QPixmap()
        self.scale_to_fit = True
        
        # Selection
        self.selected = False
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        
        # Postavi fiksnu veličinu
        self.setFixedSize(self._width, self._height)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Rečnik za properties (konzistentno sa drugim widget-ima)
        self.update_properties_dict()
    
    def set_size(self, width, height):
        """Postavlja veličinu widgeta"""
        self._width = max(20, width)  # Minimum 20px
        self._height = max(20, height)  # Minimum 20px
        self.setFixedSize(self._width, self._height)
        self.update()
    
    def get_width(self):
        """Getter za width"""
        return self._width
    
    def get_height(self):
        """Getter za height"""
        return self._height
    
    def set_frame_enabled(self, enabled):
        """Postavlja da li je okvir omogućen"""
        self.frame_enabled = enabled
        self.update()
    
    def set_frame_color(self, color):
        """Postavlja boju okvira"""
        self.frame_color = color
        self.update()
    
    def set_frame_width(self, width):
        """Postavlja debljinu okvira"""
        self.frame_width = max(0, min(20, width))  # Ograniči na 0-20
        self.update()
    
    def set_background_color(self, color):
        """Postavlja boju pozadine"""
        self.background_color = color
        self.update()
    
    def set_image_path(self, path):
        """Postavlja putanju do slike i učitava je"""
        if path and (path.lower().endswith('.bmp') or path.lower().endswith('.png')):
            self.image_path = path
            self.pixmap = QPixmap(path)
            if self.pixmap.isNull():
                print(f"Greška: Ne mogu da učitam sliku iz {path}")
                self.pixmap = QPixmap()
                return False
            self.update()
            return True
        elif path:
            print("Greška: Podržani formati su samo BMP i PNG")
            return False
        return False
    
    def get_image_path(self):
        """Getter za putanju slike"""
        return self.image_path
    
    def set_scale_to_fit(self, scale):
        """Postavlja da li se slika skalira da stane u widget"""
        self.scale_to_fit = scale
        self.update()
    
    def get_scale_to_fit(self):
        """Getter za scale_to_fit"""
        return self.scale_to_fit
    
    def set_selected(self, selected):
        """Postavlja selektovani status"""
        self.selected = selected
        self.update()
    
    def set_visible(self, visible):
        """Postavlja visible status"""
        self.visible = visible
        self.setVisible(visible)
        self.update()
    
    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        main_window = self._find_main_window()
        if not main_window:
            return
            
        if hasattr(main_window, 'all_image_dicts'):
            if self.custom_name in main_window.all_image_dicts:
                main_window.all_image_dicts[self.custom_name] = self.get_properties_dict()
    
    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima slike"""
        return {
            'type': 'Image',
            'name': getattr(self, 'custom_name', 'Image_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'frame_enabled': self.frame_enabled,
            'frame_color': self.frame_color.name(),
            'frame_width': self.frame_width,
            'background_color': self.background_color.name(),
            'image_path': self.image_path,
            'scale_to_fit': self.scale_to_fit,
            'active': getattr(self, 'active', True),
            'visible': getattr(self, 'visible', True),
            'static': getattr(self, 'static', False)
        }
    
    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None
    
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima (konzistentno sa drugim widget-ima)"""
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        # Zeleni handle-ovi
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        # 4 ugla
        corners = [
            QPoint(4, 4),  # gornji levi
            QPoint(self.width()-4, 4),  # gornji desni
            QPoint(4, self.height()-4),  # donji levi
            QPoint(self.width()-4, self.height()-4)  # donji desni
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            # Mali beli centar
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))
    
    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira (konzistentno)"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)
    
    def _get_corner_at(self, pos):
        """Proverava da li je miš preko resize handle-a"""
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Proveri da li je kliknut resize handle
            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                # Počni resize
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                # Počni dragovanje
                self.dragging = True
                self.drag_start_pos = mouse_pos
                
                # Emituj signal za selekciju
                self.clicked.emit(self)
                self._update_properties()

        event.accept()
    
    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        # Proveri da li je miš preko resize handle-a
        corner = self._get_corner_at(mouse_pos)
        if corner:
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
            self._update_properties_size()
            self._update_properties_position()
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Dragovanje widgeta
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            self._update_properties_position()
        
        event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self._update_properties_size()
            self._update_properties_position()
            self.update_properties_dict()

        event.accept()
    
    def _handle_resize(self, global_pos):
        """Menja veličinu widget-a"""
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max(20, self.resize_start_size.width() + delta.x())
            new_height = max(20, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(20, self.resize_start_size.width() + delta.x())
            new_height = max(20, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(20, self.resize_start_size.width() - delta.x())
            new_height = max(20, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(20, self.resize_start_size.width() - delta.x())
            new_height = max(20, self.resize_start_size.height() - delta.y())

        self.set_size(new_width, new_height)
    
    def _update_properties_size(self):
        """Ažuriraj veličinu u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            if hasattr(main_window, 'width_spin'):
                main_window.width_spin.blockSignals(True)
                main_window.width_spin.setValue(self._width)
                main_window.width_spin.blockSignals(False)
                
            if hasattr(main_window, 'height_spin'):
                main_window.height_spin.blockSignals(True)
                main_window.height_spin.setValue(self._height)
                main_window.height_spin.blockSignals(False)
    
    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            if hasattr(main_window, 'pos_x_spin'):
                main_window.pos_x_spin.blockSignals(True)
                main_window.pos_x_spin.setValue(self.x())
                main_window.pos_x_spin.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin'):
                main_window.pos_y_spin.blockSignals(True)
                main_window.pos_y_spin.setValue(self.y())
                main_window.pos_y_spin.blockSignals(False)
    
    def _update_properties(self):
        """Ažurira sve properties u properties baru"""
        main_window = self._find_main_window()
        if not main_window:
            return

        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Ažuriraj checkbox-ove
            if hasattr(main_window, 'active_checkbox'):
                main_window.active_checkbox.blockSignals(True)
                main_window.active_checkbox.setChecked(self.active)
                main_window.active_checkbox.blockSignals(False)
                
            if hasattr(main_window, 'visible_checkbox'):
                main_window.visible_checkbox.blockSignals(True)
                main_window.visible_checkbox.setChecked(self.visible)
                main_window.visible_checkbox.blockSignals(False)
                
            if hasattr(main_window, 'static_checkbox'):
                main_window.static_checkbox.blockSignals(True)
                main_window.static_checkbox.setChecked(self.static)
                main_window.static_checkbox.blockSignals(False)
            
            # Ažuriraj ime
            if hasattr(main_window, 'name_edit'):
                main_window.name_edit.blockSignals(True)
                main_window.name_edit.setText(self.custom_name)
                main_window.name_edit.blockSignals(False)
            
            # Ažuriraj stack order
            if hasattr(main_window, 'stack_order_spin'):
                main_window.stack_order_spin.blockSignals(True)
                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index(main_window.current_shape) + 1
                    main_window.stack_order_spin.setValue(index)
                main_window.stack_order_spin.blockSignals(False)
            
            # Ažuriraj frame checkbox
            if hasattr(main_window, 'frame_checkbox'):
                main_window.frame_checkbox.blockSignals(True)
                main_window.frame_checkbox.setChecked(self.frame_enabled)
                main_window.frame_checkbox.blockSignals(False)
            
            # Ažuriraj frame width
            if hasattr(main_window, 'frame_width_spin'):
                main_window.frame_width_spin.blockSignals(True)
                main_window.frame_width_spin.setValue(self.frame_width)
                main_window.frame_width_spin.blockSignals(False)
            
            # Ažuriraj frame color
            if hasattr(main_window, 'frame_color_rect'):
                main_window.frame_color_rect.setStyleSheet(
                    f"background-color: {self.frame_color.name()}; border: 1px solid #ccc;"
                )
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Crtanje pozadine
        painter.setBrush(self.background_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, self._width, self._height)
        
        # Crtanje okvira ako je omogućen
        if self.frame_enabled and self.frame_width > 0:
            painter.setPen(QPen(self.frame_color, self.frame_width))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(0, 0, self._width, self._height)
        
        # Crtanje slike ako postoji
        if not self.pixmap.isNull():
            # Izračunaj dimenzije za sliku sa obzirom na okvir
            margin = self.frame_width if self.frame_enabled else 0
            content_rect = QRect(
                margin, 
                margin, 
                self._width - 2 * margin, 
                self._height - 2 * margin
            )
            
            if content_rect.width() > 0 and content_rect.height() > 0:
                if self.scale_to_fit:
                    # Skaliranje slike da stane u dostupni prostor
                    scaled_pixmap = self.pixmap.scaled(
                        content_rect.size(), 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                    
                    # Centriranje skalirane slike
                    x = content_rect.x() + (content_rect.width() - scaled_pixmap.width()) // 2
                    y = content_rect.y() + (content_rect.height() - scaled_pixmap.height()) // 2
                    painter.drawPixmap(x, y, scaled_pixmap)
                else:
                    # Prikaz originalne slike (može biti isečena)
                    painter.drawPixmap(content_rect, self.pixmap)
        
        # Ako nema slike, prikaži placeholder tekst
        elif self.image_path:
            painter.setPen(QColor(128, 128, 128))
            font = QFont("Arial", 8)
            painter.setFont(font)
            painter.drawText(
                self.rect(), 
                Qt.AlignmentFlag.AlignCenter, 
                "Slika nije učitana"
            )
        
        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)


class EllipseWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width=98, height=78, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height

        # Status properties
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.stack_order = 1

        # Ellipse properties
        self.border_color = QColor(0, 0, 0)
        self.border_width = 2
        self.fill_enabled = False
        self.gradient_enabled = True
        self.gradient_type = "Top-Bottom"
        self.gradient_start_color = QColor(0, 0, 255)
        self.gradient_end_color = QColor(0, 0, 128)
        
        # Selection
        self.is_selected = False
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        
        # Postavi fiksnu veličinu
        self.setFixedSize(self._width, self._height)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def set_size(self, width, height):
        """Postavlja veličinu widgeta"""
        self._width = max(20, width)
        self._height = max(20, height)
        self.setFixedSize(self._width, self._height)
        self.update()
    
    def get_width(self):
        """Getter za width"""
        return self._width
    
    def get_height(self):
        """Getter za height"""
        return self._height
    
    def set_border_color(self, color):
        """Postavlja boju border-a"""
        self.border_color = color
        self.update()
    
    def set_border_width(self, width):
        """Postavlja debljinu border-a"""
        self.border_width = max(1, min(20, width))
        self.update()
    
    def set_fill_enabled(self, enabled):
        """Omogućava ili onemogućava popunu"""
        self.fill_enabled = enabled
        if enabled:
            self.gradient_enabled = True
        self.update()
    
    def set_gradient_type(self, gradient_type):
        """Postavlja tip gradijenta"""
        self.gradient_type = gradient_type
        self.update()
    
    def set_gradient_colors(self, start_color, end_color):
        """Postavlja boje gradijenta"""
        self.gradient_start_color = start_color
        self.gradient_end_color = end_color
        self.update()
    
    def set_selected(self, selected):
        """Postavlja selektovani status"""
        self.is_selected = selected
        self.update()
    
    def set_visible(self, visible):
        """Postavlja visible status"""
        self.visible = visible
        self.setVisible(visible)
        self.update()
    
    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima elipse"""
        return {
            'type': 'Ellipse',
            'name': getattr(self, 'custom_name', 'Ellipse_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'border_color': self.border_color.name(),
            'border_width': self.border_width,
            'fill_enabled': self.fill_enabled,
            'gradient_enabled': self.gradient_enabled,
            'gradient_type': self.gradient_type,
            'gradient_start_color': self.gradient_start_color.name() if self.gradient_enabled else None,
            'gradient_end_color': self.gradient_end_color.name() if self.gradient_enabled else None,
            'active': getattr(self, 'active', True),
            'visible': getattr(self, 'visible', True),
            'static': getattr(self, 'static', False)
        }
    
    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None
    
    def _draw_selection_handles(self, painter):
        """Crtanje resize handle-ova na uglovima"""
        if not self.is_selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QPen(QColor(0, 80, 200), 1))

        corners = [
            QPoint(4, 4),
            QPoint(self.width()-4, 4),
            QPoint(4, self.height()-4),
            QPoint(self.width()-4, self.height()-4)
        ]

        for corner in corners:
            painter.drawEllipse(corner.x() - half_size, corner.y() - half_size, 
                              handle_size, handle_size)

            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(corner.x() - 1, corner.y() - 1, 2, 2)
            painter.setBrush(QColor(0, 255, 0))
            painter.setPen(QPen(QColor(0, 80, 200), 1))
    
    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira"""
        if not self.is_selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)
    
    def _get_corner_at(self, pos):
        """Proverava da li je miš preko resize handle-a"""
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint(0, 0),
            "top_right": QPoint(self.width(), 0),
            "bottom_left": QPoint(0, self.height()),
            "bottom_right": QPoint(self.width(), self.height())
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect(
                corner_pos.x() - half_size,
                corner_pos.y() - half_size,
                handle_size,
                handle_size
            )
            
            if corner_rect.contains(pos):
                return corner_name
        
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self._get_corner_at(mouse_pos)

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit(self)

        event.accept()
    
    def mouseMoveEvent(self, event):
        mouse_pos = event.pos()
        
        corner = self._get_corner_at(mouse_pos)
        if corner:
            if corner in ["top_left", "bottom_right"]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif corner in ["top_right", "bottom_left"]:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self._handle_resize(event.globalPosition().toPoint())
        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            self.move(new_x, new_y)
        
        event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

        event.accept()
    
    def _handle_resize(self, global_pos):
        """Menja veličinu widget-a"""
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max(20, self.resize_start_size.width() + delta.x())
            new_height = max(20, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_right":
            new_width = max(20, self.resize_start_size.width() + delta.x())
            new_height = max(20, self.resize_start_size.height() - delta.y())
        elif self.resize_corner == "bottom_left":
            new_width = max(20, self.resize_start_size.width() - delta.x())
            new_height = max(20, self.resize_start_size.height() + delta.y())
        elif self.resize_corner == "top_left":
            new_width = max(20, self.resize_start_size.width() - delta.x())
            new_height = max(20, self.resize_start_size.height() - delta.y())

        self.set_size(new_width, new_height)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = self.border_width // 2
        ellipse_rect = QRect(
            margin,
            margin,
            self._width - 2 * margin,
            self._height - 2 * margin
        )

        # Crtanje popune ako je omogućena
        if self.fill_enabled and self.gradient_enabled:
            if self.gradient_type == "Top-Bottom":
                gradient = QLinearGradient(0, 0, 0, self._height)
            elif self.gradient_type == "Bottom-Top":
                gradient = QLinearGradient(0, self._height, 0, 0)
            elif self.gradient_type == "Left-Right":
                gradient = QLinearGradient(0, 0, self._width, 0)
            elif self.gradient_type == "Right-Left":
                gradient = QLinearGradient(self._width, 0, 0, 0)
            else:
                gradient = QLinearGradient(0, 0, 0, self._height)

            gradient.setColorAt(0, self.gradient_start_color)
            gradient.setColorAt(1, self.gradient_end_color)
            painter.setBrush(QBrush(gradient))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)

        # Crtanje elipse
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.drawEllipse(ellipse_rect)

        # Ako je selektovan, nacrtaj selekcioni okvir i handle-ove
        if self.is_selected:
            self._draw_selection_border(painter)
            self._draw_selection_handles(painter)
    
    # KLJUČNE METODE ZA AŽURIRANJE PROPERTIES BAR-A
    def move(self, x, y):
        """Override move metode da ažurira properties bar"""
        super().move(x, y)
        
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            try:
                if hasattr(main_window, 'pos_x_spin_ellipse'):
                    main_window.pos_x_spin_ellipse.blockSignals(True)
                    main_window.pos_x_spin_ellipse.setValue(x)
                    main_window.pos_x_spin_ellipse.blockSignals(False)
            except RuntimeError:
                pass
            
            try:
                if hasattr(main_window, 'pos_y_spin_ellipse'):
                    main_window.pos_y_spin_ellipse.blockSignals(True)
                    main_window.pos_y_spin_ellipse.setValue(y)
                    main_window.pos_y_spin_ellipse.blockSignals(False)
            except RuntimeError:
                pass

    def resize(self, width, height):
        """Override resize metode da ažurira properties bar"""
        super().resize(width, height)
        self._width = width
        self._height = height
        
        main_window = self._find_main_window()
        if main_window and main_window.current_shape == self:
            try:
                if hasattr(main_window, 'width_spin_ellipse'):
                    main_window.width_spin_ellipse.blockSignals(True)
                    main_window.width_spin_ellipse.setValue(width)
                    main_window.width_spin_ellipse.blockSignals(False)
            except RuntimeError:
                pass
            
            try:
                if hasattr(main_window, 'height_spin_ellipse'):
                    main_window.height_spin_ellipse.blockSignals(True)
                    main_window.height_spin_ellipse.setValue(height)
                    main_window.height_spin_ellipse.blockSignals(False)
            except RuntimeError:
                pass
    
    # Metoda za ažuriranje properties rečnika (za konzistentnost)
    def update_properties_dict(self):
        """Ažurira properties rečnik"""
        main_window = self._find_main_window()
        if not main_window or not hasattr(main_window, 'all_ellipse_dicts'):
            return
            
        main_window.all_ellipse_dicts[self.custom_name] = self.get_properties_dict()

class NumericWidget(QWidget):
    clicked = pyqtSignal(object)
    
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.setFixedSize(width, height)
        
        # Status svojstva
        self.active = True
        self.visible = True
        self.static = False
        
        # Numerička svojstva
        self.number = 123  # Podrazumevana vrednost
        self.number_color = QColor(0, 0, 0)  # Crna boja broja
        self.number_size = 12  # Veličina fonta
        self.number_alignment = "Left"  # Left, Center, Right, Top, Bottom
        self.number_font = "Arial"  # Font
        
        # Selekcija
        self.selected = False
        
        # Drag varijable
        self.dragging = False
        self.drag_start_pos = QPoint()
        
        # Rečnik
        self.custom_name = None
        self.stack_order = 1
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Inicijalizuj display text
        self._update_display_text()
        self._update_display_size()

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def get_width(self):
        """Getter za width"""
        return self._width

    def get_height(self):
        """Getter za height"""
        return self._height

    def set_number(self, number):
        self.number = number
        self._update_display_text()
        self._update_display_size()
        self.update()

    def set_number_color(self, color):
        self.number_color = color
        self.update()

    def set_number_size(self, size):
        self.number_size = size
        self._update_display_size()
        self.update()

    def set_number_alignment(self, alignment):
        self.number_alignment = alignment
        self.update()

    def set_active(self, active):
        self.active = active
        self.setEnabled(active)
        self.update()

    def set_visible(self, visible):
        self.visible = visible
        self.setVisible(visible)
        self.update()

    def set_static(self, static):
        self.static = static
        self.update()

    def _update_display_text(self):
        """Ažurira tekst koji se prikazuje"""
        self.display_text = str(self.number)

    def _update_display_size(self):
        """Ažurira veličinu widgeta na osnovu teksta"""
        painter = QPainter(self)
        font = QFont(self.number_font, self.number_size)
        font_metrics = QFontMetrics(font)
        
        text_width = font_metrics.horizontalAdvance(self.display_text) + 20  # +20 za margin
        text_height = font_metrics.height() + 10  # +10 za margin
        
        self._width = max(50, text_width)
        self._height = max(30, text_height)
        self.setFixedSize(self._width, self._height)
        
        painter.end()

    def get_properties_dict(self):
        """Vraća rečnik sa svim svojstvima numeričkog widgeta"""
        return {
            'type': 'Numeric',
            'name': getattr(self, 'custom_name', 'Numeric_0'),
            'stack_order': getattr(self, 'stack_order', 0),
            'position': (self.x(), self.y()),
            'width': self._width,
            'height': self._height,
            'active': self.active,
            'visible': self.visible,
            'static': self.static,
            'number': self.number,
            'number_color': self.number_color.name(),
            'number_size': self.number_size,
            'number_alignment': self.number_alignment,
            'number_font': self.number_font
        }

    def update_properties_dict(self):
        """Ažurira rečnik svojstava"""
        if hasattr(self, 'custom_name'):
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'all_numeric_dicts'):
                if self.custom_name in main_window.all_numeric_dicts:
                    main_window.all_numeric_dicts[self.custom_name] = self.get_properties_dict()
                else:
                    main_window.all_numeric_dicts[self.custom_name] = self.get_properties_dict()

    # Metode za drag
    def _draw_selection_border(self, painter):
        """Crtanje crvenog isprekidanog okvira kada je selektovano"""
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect(margin, margin, 
                           self.width() - 2 * margin, 
                           self.height() - 2 * margin)

        selection_pen = QPen(QColor(255, 0, 0))
        selection_pen.setWidth(3)
        selection_pen.setStyle(Qt.PenStyle.DashLine)
        selection_pen.setDashPattern([4, 2])

        painter.setPen(selection_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.pos()
            self.clicked.emit(self)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and (event.buttons() & Qt.MouseButton.LeftButton):
            # Dragovanje widgeta
            delta = event.pos() - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move(new_x, new_y)
            
            # Ažuriraj properties bar ako postoji
            self._update_properties_position()
        
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            # Ažuriraj properties bar
            self._update_properties_position()
            # Ažuriraj rečnik
            self.update_properties_dict()
        event.accept()

    def _update_properties_position(self):
        """Ažuriraj poziciju u properties bar-u"""
        main_window = self._find_main_window()
        if not main_window:
            return
        
        if (hasattr(main_window, 'current_shape') and 
            main_window.current_shape == self):
            
            # Proveri za numeričke kontrole
            if hasattr(main_window, 'pos_x_spin_numeric'):
                main_window.pos_x_spin_numeric.blockSignals(True)
                main_window.pos_x_spin_numeric.setValue(self.x())
                main_window.pos_x_spin_numeric.blockSignals(False)
            elif hasattr(main_window, 'pos_x_spin'):
                main_window.pos_x_spin.blockSignals(True)
                main_window.pos_x_spin.setValue(self.x())
                main_window.pos_x_spin.blockSignals(False)
                
            if hasattr(main_window, 'pos_y_spin_numeric'):
                main_window.pos_y_spin_numeric.blockSignals(True)
                main_window.pos_y_spin_numeric.setValue(self.y())
                main_window.pos_y_spin_numeric.blockSignals(False)
            elif hasattr(main_window, 'pos_y_spin'):
                main_window.pos_y_spin.blockSignals(True)
                main_window.pos_y_spin.setValue(self.y())
                main_window.pos_y_spin.blockSignals(False)

    def _find_main_window(self):
        """Pronađi glavni prozor u hijerarhiji"""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Crtanje teksta (broja)
        painter.setPen(self.number_color)
        font = QFont(self.number_font, self.number_size)
        painter.setFont(font)
        
        # Određivanje pozicije teksta na osnovu alignment-a
        text_rect = QRect(0, 0, self._width, self._height)
        
        if self.number_alignment == "Left":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        elif self.number_alignment == "Center":
            alignment_flags = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        elif self.number_alignment == "Right":
            alignment_flags = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        elif self.number_alignment == "Top":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        elif self.number_alignment == "Bottom":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        else:
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

        painter.drawText(text_rect, alignment_flags, self.display_text)
        
        # Ako je selektovan, nacrtaj selekcioni okvir
        if self.selected:
            self._draw_selection_border(painter)