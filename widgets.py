from PyQt6.QtGui import ( QPainter, QPen, QColor, QLinearGradient, QFont, QBrush, QPixmap, QFontMetrics )
from PyQt6.QtCore import ( Qt, QPoint, QRect, QPointF, pyqtSignal, QSize, QRectF )
from PyQt6.QtWidgets import ( QWidget, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox )
import math
import os
        
class LineWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, parent = None ):
        super().__init__( parent )

        self.defaultValues()
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def defaultValues( self ):
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.tag = 0
        self.start_x = 0
        self.start_y = 0
        self.end_x = 100
        self.end_y = 100
        self.line_color = QColor( 0, 0, 0 ) 
        self.line_width = 5

        self.selected = False
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QPoint()
        self.resize_corner = None
        self.drag_start_pos = QPoint()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        local_start_x = self.start_x - self.x()
        local_start_y = self.start_y - self.y()
        local_end_x = self.end_x - self.x()
        local_end_y = self.end_y - self.y()
        
        pen = QPen( self.line_color )
        pen.setWidth( 2 * self.line_width )
        pen.setCapStyle( Qt.PenCapStyle.RoundCap )
        painter.setPen( pen )
        painter.drawLine( local_start_x, local_start_y, local_end_x, local_end_y )
        
        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter, local_start_x, local_start_y, local_end_x, local_end_y )
    
    def drawSelectionHandles( self, painter, start_x, start_y, end_x, end_y ):
        handle_size = 10
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )
        painter.drawEllipse( start_x - half_size, start_y - half_size, handle_size, handle_size )
        painter.drawEllipse( end_x - half_size, end_y - half_size, handle_size, handle_size )
        painter.setBrush( QColor( 255, 255, 255 ) )
        painter.setPen( Qt.PenStyle.NoPen )
        painter.drawEllipse( start_x - 1, start_y - 1, 2, 2 )
        painter.drawEllipse( end_x - 1, end_y - 1, 2, 2 )
    
    def drawSelectionBorder(self, painter):
        margin = 2
    
        local_start_x = self.start_x - self.x()
        local_start_y = self.start_y - self.y()
        local_end_x = self.end_x - self.x()
        local_end_y = self.end_y - self.y()
        
        min_x = min( local_start_x, local_end_x ) - margin
        min_y = min( local_start_y, local_end_y ) - margin
        max_x = max( local_start_x, local_end_x ) + margin
        max_y = max( local_start_y, local_end_y ) + margin
        
        selection_rect = QRect( min_x, min_y, max_x - min_x, max_y - min_y )
        
        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 2 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )
        
        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( selection_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner or not self.resize_start_size:
            return

        delta = global_pos - self.resize_start_pos
        
        start_x_start, start_y_start, end_x_start, end_y_start = self.resize_start_size
        
        if self.resize_corner == "start":
            self.start_x = start_x_start + delta.x()
            self.start_y = start_y_start + delta.y()

        elif self.resize_corner == "end":
            self.end_x = end_x_start + delta.x()
            self.end_y = end_y_start + delta.y()
        
        self.updateLineSize()
        self.update()

    def isPointOnLine( self, pos ):
        global_x = pos.x() + self.x()
        global_y = pos.y() + self.y()
        
        x1, y1, x2, y2 = self.start_x, self.start_y, self.end_x, self.end_y
        
        if x1 == x2 and y1 == y2:
            distance = math.sqrt( ( global_x - x1 ) ** 2 + ( global_y - y1 ) ** 2 )
            return distance <= self.line_width / 2 + 5
        
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
        
        distance = math.sqrt( ( global_x - xx ) ** 2 + ( global_y - yy ) ** 2 )
        
        return distance <= self.line_width / 2 + 5

    def getCornerAt( self, pos ):
        handle_size = 16
        
        global_pos = QPoint( pos.x() + self.x(), pos.y() + self.y() )
        
        start_rect = QRect( self.start_x - handle_size // 2, self.start_y - handle_size // 2, handle_size, handle_size )

        if start_rect.contains( global_pos ):
            return "start"
        
        end_rect = QRect( self.end_x - handle_size // 2, self.end_y - handle_size // 2, handle_size, handle_size ) 

        if end_rect.contains( global_pos ):
            return "end"
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update()



    def setLinePosition( self, start_x, start_y, end_x, end_y ):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.updateLineSize()
        self.update()

    def updateLineSize( self ):
        margin = 20 
        
        min_x = min( self.start_x, self.end_x ) - self.x()
        min_y = min( self.start_y, self.end_y ) - self.y()
        max_x = max( self.start_x, self.end_x ) - self.x()
        max_y = max( self.start_y, self.end_y ) - self.y()
        
        width = max( 20, max_x - min_x ) + 2 * margin
        height = max( 20, max_y - min_y ) + 2 * margin
        
        self.setFixedSize( width, height )
        center_x = ( self.start_x + self.end_x ) // 2
        center_y = ( self.start_y + self.end_y ) // 2
        self.move( center_x - self.width() // 2, center_y - self.height() // 2 )

    def updateLinePositionPropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if (hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'start_x_spin_line' ):
                main_window.start_x_spin_line.blockSignals( True )
                main_window.start_x_spin_line.setValue( self.start_x )
                main_window.start_x_spin_line.blockSignals( False )
                
            if hasattr( main_window, 'start_y_spin_line' ):
                main_window.start_y_spin_line.blockSignals( True )
                main_window.start_y_spin_line.setValue( self.start_y )
                main_window.start_y_spin_line.blockSignals( False )
                
            if hasattr( main_window, 'end_x_spin_line' ):
                main_window.end_x_spin_line.blockSignals( True )
                main_window.end_x_spin_line.setValue( self.end_x )
                main_window.end_x_spin_line.blockSignals( False )
                
            if hasattr( main_window, 'end_y_spin_line' ):
                main_window.end_y_spin_line.blockSignals( True )
                main_window.end_y_spin_line.setValue( self.end_y )
                main_window.end_y_spin_line.blockSignals( False )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            self.resize_corner = self.getCornerAt( mouse_pos )
            
            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = ( self.start_x, self.start_y, self.end_x, self.end_y )

            else:
                if self.isPointOnLine( mouse_pos ):
                    self.dragging = True
                    self.drag_start_pos = mouse_pos
                
                self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None
            self.resize_start_size = None

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        point = self.getCornerAt( mouse_pos )

        if point:
            self.setCursor( Qt.CursorShape.SizeAllCursor )

        elif self.isPointOnLine( mouse_pos ):
            self.setCursor( Qt.CursorShape.SizeAllCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )
            self.updateLinePositionPropertiesPosition()

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            self.start_x += delta.x()
            self.start_y += delta.y()
            self.end_x += delta.x()
            self.end_y += delta.y()

            self.drag_start_pos = mouse_pos
                    
            center_x = ( self.start_x + self.end_x ) // 2
            center_y = ( self.start_y + self.end_y ) // 2
            self.move( center_x - self.width() // 2, center_y - self.height() // 2 )

            self.update()
            self.updateLinePositionPropertiesPosition()
        
        event.accept()

class RectangleWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, parent = None ):
        super().__init__( parent )

        self.defaultValues()
        self.setFixedSize( self.rectangle_width, self.rectangle_height )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
        
    def defaultValues( self ):
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.tag = 0
        self.rectangle_width = 100 
        self.rectangle_height = 80 
        self.edges_color = QColor( 0, 0, 0 )
        self.edges_width = 5
        self.filled = False 
        self.gradient_direction = "Top-Bottom"
        self.start_color = QColor( 255, 0, 0 )
        self.end_color = QColor( 0, 0, 255 )

        self.selected = False
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        if self.filled:
            gradient = None
            
            if self.gradient_direction == "Top-Bottom":
                gradient = QLinearGradient( 0, 0, 0, self.height() )

            elif self.gradient_direction == "Bottom-Top":
                gradient = QLinearGradient( 0, self.height(), 0, 0 )

            elif self.gradient_direction == "Left-Right":
                gradient = QLinearGradient( 0, 0, self.width(), 0 )

            elif self.gradient_direction == "Right-Left":
                gradient = QLinearGradient( self.width(), 0, 0, 0 )

            gradient.setColorAt( 0.0, self.start_color )
            gradient.setColorAt( 0.6, self.end_color )
            gradient.setColorAt( 1.0, self.end_color )    
            painter.fillRect( self.rect(), gradient )

        
        pen = QPen( self.edges_color )
        pen.setWidth( 2* self.edges_width )
        painter.setPen( pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( 0, 0, self.width() , self.height() )
        
        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        handle_size = 10
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )
        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder(  self, painter ):
        margin = 2
        selection_rect = QRect(margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( selection_rect )

    def handleResize( self, global_pos ):

        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 20, self.resize_start_size.width() + delta.x() )
            new_height = max( 20, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 20, self.resize_start_size.width() + delta.x() )
            new_height = max( 20, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 20, self.resize_start_size.width() - delta.x() )
            new_height = max( 20, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 20, self.resize_start_size.width() - delta.x() )
            new_height = max( 20, self.resize_start_size.height() - delta.y() )

        self.rectangle_width = new_width
        self.rectangle_height = new_height

        self.setFixedSize( new_width, new_height )
        self.updateRectanglePropertiesSize()

    def getCornerAt( self, pos ):
        handle_size = 16
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def updateRectanglePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'width_spin_rect' ) and hasattr( main_window, 'height_spin_rect' ) ):
            main_window.width_spin_rect.blockSignals( True )
            main_window.width_spin_rect.setValue( self.rectangle_width )
            main_window.width_spin_rect.blockSignals( False )

        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and  hasattr( main_window, 'height_spin_rect' ) ):
            main_window.height_spin_rect.blockSignals( True )
            main_window.height_spin_rect.setValue( self.rectangle_height )
            main_window.height_spin_rect.blockSignals( False )

    def updateRectanglePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'pos_x_spin_rect' ) and hasattr( main_window, 'pos_y_spin_rect' ) ):
            main_window.pos_x_spin_rect.setValue( self.x() )
            main_window.pos_y_spin_rect.setValue( self.y() )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updateRectanglePropertiesSize()
            self.updateRectanglePropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )
        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            new_x = max( 0, self.x() + delta.x() )
            new_y = max( 0, self.y() + delta.y() )

            self.move( new_x, new_y )
            self.updateRectanglePropertiesPosition()
        
        event.accept()

class CircleWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, parent = None ):
        super().__init__( parent )

        self.defaultValues()
        self.setFixedSize( self.diameter, self.diameter )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
    def defaultValues( self ):
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.tag = 0
        self.center_x = 0
        self.center_y = 0
        self.diameter = 100
        self.edges_color = QColor( 0, 0, 0 )
        self.edges_width = 5
        self.filled = False 
        self.fill_color = QColor( 255, 0, 0 ) 

        self.selected = False
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.drag_start_pos = QPoint()
        self.resize_corner = None
        self.resize_start_diameter = QPoint()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        rect_size = min( self.width(), self.height() ) - 2 * self.edges_width

        x_offset = ( self.width() - rect_size ) // 2
        y_offset = ( self.height() - rect_size ) // 2

        circle_rect = QRectF( x_offset, y_offset, rect_size, rect_size )

        if self.filled:
            painter.setBrush( self.fill_color )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( circle_rect )

        pen = QPen( self.edges_color, 2 * self.edges_width )
        pen.setJoinStyle( Qt.PenJoinStyle.RoundJoin )
        pen.setCapStyle( Qt.PenCapStyle.RoundCap )
        painter.setPen( pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawEllipse( circle_rect )

        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )
            
    def drawSelectionHandles( self, painter ):
        handle_size = 10
        half_handle = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 255, 0 ), 1 ) )

        points = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( self.width() - 4, self.height() - 4 ), QPoint( 4, self.height() - 4 ), ]

        for point in points:
            painter.drawEllipse(point.x() - half_handle, point.y() - half_handle, handle_size, handle_size )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( point.x() - 1, point.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 255, 0 ), 1 ) )

    def drawSelectionBorder(  self, painter ):
        margin = 2

        selection_rect = QRectF( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )
        painter.setPen( QPen( QColor( 255, 0, 0 ), 3, Qt.PenStyle.DashLine ) )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( selection_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        if "right" in self.resize_corner:
            new_diameter = max( 20, self.resize_start_diameter + delta.x() )

        elif "left" in self.resize_corner:
            new_diameter = max( 20, self.resize_start_diameter - delta.x() )

        else:
            new_diameter = self.diameter

        self.diameter = new_diameter
        self.setFixedSize( new_diameter, new_diameter )
        self.update()


        if "left" in self.resize_corner:
            delta_x = self.resize_start_diameter - new_diameter
            self.move( self.x() + delta_x, self.y() )

        if "top" in self.resize_corner:
            delta_y = self.resize_start_diameter - new_diameter
            self.move( self.x(), self.y() + delta_y )

        self.updateCirclePropertiesSize()
        self.updateCirclePropertiesCenterPosition()

    def getCornerAt( self, pos ):
        handle_size = 12 
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update()
    
    def updateCirclePropertiesSize( self ):
        main_window = self.findMainWindow()

        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr(main_window, 'diameter_spin_circle' ) ):
            main_window.diameter_spin_circle.blockSignals( True )
            main_window.diameter_spin_circle.setValue( self.diameter )
            main_window.diameter_spin_circle.blockSignals( False )

    def updateCircleCenterPositionProperties( self ):
        main_window = self.findMainWindow()

        self.center_x = self.x() + self.diameter // 2
        self.center_y = self.y() + self.diameter // 2

        if hasattr( main_window, 'pos_x_spin_circle' ) and main_window.pos_x_spin_circle:
            main_window.pos_x_spin_circle.blockSignals( True )
            main_window.pos_x_spin_circle.setValue( self.center_x )
            main_window.pos_x_spin_circle.blockSignals( False )

        if hasattr( main_window, 'pos_y_spin_circle' ) and main_window.pos_y_spin_circle:
            main_window.pos_y_spin_circle.blockSignals( True )
            main_window.pos_y_spin_circle.setValue( self.center_y )
            main_window.pos_y_spin_circle.blockSignals( False )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            self.resize_corner = self.getCornerAt( mouse_pos )
            
            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_diameter = self.diameter

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )
                
            self.updateCircleCenterPositionProperties()
            event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None
            self.resize_start_diameter = 0

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()

        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )

        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint())

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            new_x = max( 0, self.x() + delta.x() )
            new_y = max( 0, self.y() + delta.y() )
            self.move( new_x, new_y )
            self.updateCircleCenterPositionProperties()

        event.accept()

class EllipseWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, parent = None ):
        super().__init__( parent )

        self.defaultValues()
        self.setFixedSize( self.ellipse_width, self.ellipse_height )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def defaultValues( self ):
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.stack_order = 1
        self.tag = 0
        self.ellipse_width = 120
        self.ellipse_height = 80
        self.center_x = 0
        self.center_y = 0
        self.edges_color = QColor( 0, 0, 0 )
        self.edges_width = 5
        self.filled = False
        self.show_ellipse_warning = True
        self.gradient_direction = "Top-Bottom"
        self.gradient_start_color = QColor( 255, 0, 0 )
        self.gradient_end_color = QColor( 0, 0, 255 )

        self.selected = False
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.drag_start_pos = QPoint()
        self.resize_corner = None
        self.resize_start_size = QSize()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )

        margin = self.edges_width
        ellipse_rect = QRect( margin, margin, self.ellipse_width - 2 * margin, self.ellipse_height - 2 * margin )

        if self.filled:
            if self.gradient_direction == "Top-Bottom":
                gradient = QLinearGradient( 0, 0, 0, self.ellipse_height )

            elif self.gradient_direction == "Bottom-Top":
                gradient = QLinearGradient( 0, self.ellipse_height, 0, 0 )

            elif self.gradient_direction == "Left-Right":
                gradient = QLinearGradient( 0, 0, self.ellipse_width, 0 )

            elif self.gradient_direction == "Right-Left":
                gradient = QLinearGradient( self.ellipse_width, 0, 0, 0 )

            else:
                gradient = QLinearGradient( 0, 0, 0, self._height )

            gradient.setColorAt( 0, self.gradient_start_color )
            gradient.setColorAt( 1, self.gradient_end_color )
            painter.setBrush( QBrush( gradient ) )
            
        else:
            painter.setBrush( Qt.BrushStyle.NoBrush )

        painter.setPen( QPen( self.edges_color, 2 * self.edges_width ) )
        painter.drawEllipse( ellipse_rect )

        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        handle_size = 10
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )
    
    def drawSelectionBorder( self, painter ):
        margin = 2
        border_rect = QRect(margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        self.setFixedSize( self.ellipse_width, self.ellipse_height )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        delta = global_pos - self.resize_start_pos
        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 20, self.resize_start_size.width() + delta.x() )
            new_height = max( 20, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 20, self.resize_start_size.width() + delta.x() )
            new_height = max( 20, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 20, self.resize_start_size.width() - delta.x() )
            new_height = max( 20, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 20, self.resize_start_size.width() - delta.x() )
            new_height = max( 20, self.resize_start_size.height() - delta.y() )

        self.ellipse_width = max( 20, new_width )
        self.ellipse_height = max( 20, new_height )

        self.setFixedSize( self.ellipse_width, self.ellipse_height )
        self.updateEllipsePropertiesCenterPosition()
        self.updateEllipsePropertiesSize()
    
    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None
    
    def setSelected( self, selected ):
        self.selected = selected
        self.update()
    
    def updateEllipsePropertiesSize( self ):
        main_window = self.findMainWindow()

        if main_window and main_window.current_shape == self:
            if hasattr( main_window, 'width_spin_ellipse' ):
                main_window.width_spin_ellipse.blockSignals( True )
                main_window.width_spin_ellipse.setValue( self.ellipse_width )
                main_window.width_spin_ellipse.blockSignals( False )
            
            if hasattr( main_window, 'height_spin_ellipse' ):
                main_window.height_spin_ellipse.blockSignals( True )
                main_window.height_spin_ellipse.setValue( self.ellipse_height )
                main_window.height_spin_ellipse.blockSignals( False )
            
    def updateEllipsePropertiesCenterPosition( self ):
        main_window = self.findMainWindow()
        
        self.center_x = self.x() + self.ellipse_width // 2
        self.center_y = self.y() + self.ellipse_height // 2

        if hasattr( main_window, 'pos_x_spin_ellipse' ):
            main_window.pos_x_spin_ellipse.blockSignals( True )
            main_window.pos_x_spin_ellipse.setValue( self.center_x )
            main_window.pos_x_spin_ellipse.blockSignals( False )

        if hasattr( main_window, 'pos_y_spin_ellipse' ):
            main_window.pos_y_spin_ellipse.blockSignals( True )
            main_window.pos_y_spin_ellipse.setValue( self.center_y )
            main_window.pos_y_spin_ellipse.blockSignals( False )

    def showFilledWarning( self, state ):
        state == Qt.CheckState.Checked.value 

        if state and self.show_ellipse_warning:
            warning_dialog = QDialog( self )
            warning_dialog.setWindowTitle( "Information" )
            warning_dialog.setFixedSize( 400, 200 )
            warning_dialog.setStyleSheet( "QDialog {background-color: #2b2b2b; border: 1px solid #555555;}" )
            layout = QVBoxLayout( warning_dialog )
            info_label = QLabel( "This option is resource intensive and may cause unpredictable display behavior." )
            info_label.setWordWrap( True )
            info_label.setStyleSheet( "color: white; font-size: 12px; padding: 10px; border: none;" )
            layout.addWidget( info_label )

            dont_show_layout = QHBoxLayout()
            dont_show_checkbox = QCheckBox( "Do not show again" )
            dont_show_checkbox.setStyleSheet( "color: white; border: none;" )
            dont_show_layout.addWidget( dont_show_checkbox )
            dont_show_layout.addStretch(1)
            layout.addLayout( dont_show_layout )

            button_layout = QHBoxLayout()
            ok_button = QPushButton( "OK" )
            ok_button.clicked.connect( warning_dialog.accept )
            ok_button.setFixedWidth( 80 )
            button_layout.addStretch( 1 )
            button_layout.addWidget( ok_button )
            layout.addLayout( button_layout )
            warning_dialog.exec()

            if dont_show_checkbox.isChecked():
                self.show_ellipse_warning = False

        if hasattr( self, 'gradient_combo_ellipse' ):
            self.gradient_combo_ellipse.setEnabled( state )

        if hasattr( self, 'start_color_rect_ellipse' ):
            self.start_color_rect_ellipse.setEnabled( state )

        if hasattr( self, 'end_color_rect_ellipse' ):
            self.end_color_rect_ellipse.setEnabled( state )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            parent = parent.parent()

        return None
    
    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )

            self.updateEllipsePropertiesCenterPosition()
            event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )
            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )
        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            new_x = max( 0, self.x() + delta.x() )
            new_y = max( 0, self.y() + delta.y() )
            self.move( new_x, new_y )
            self.updateEllipsePropertiesCenterPosition()
        
        event.accept()
    
class ButtonWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, parent = None ):
        super().__init__( parent )
        
        self.defaultValues()
        self.setFixedSize( self.button_width, self.button_height )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
    def defaultValues( self ):
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.tag = 0
        self.button_width = 100
        self.button_height = 50
        self.gradient_start_color = QColor( 255, 255, 255 )
        self.gradient_end_color = QColor( 0, 0, 255 )
        self.color_press = QColor( 0, 0, 255 )
        self.effect_3d = True
        self.effect_3d_press = True
        self.button_text = "Press"
        self.text_size = 28
        self.text_color = QColor( 255, 255, 255 )

        self.selected = False
        self.resizing = False
        self.dragging = False 
        self.resize_start_pos = QPoint()
        self.drag_start_pos = QPoint()
        self.resize_corner = None
        self.resize_start_size = QSize()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )

  
        r = int( 4 / 5 * self.text_size - 89 / 5 )

        if self.effect_3d and self.effect_3d_press:
            gradient = QLinearGradient( 0, 0, 0, self.height() )
            self.gradient_start_color.setAlpha( 100 )
            gradient.setColorAt( 0.0, self.gradient_start_color )
            gradient.setColorAt( 0.4, self.gradient_end_color )   
            gradient.setColorAt( 1.0, self.gradient_end_color ) 
            painter.setBrush( QBrush( gradient ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawRoundedRect( 0, 0, self.width(), self.height(), r, r )

            painter.setPen( QPen( QColor( 0, 0, 0 ), 2 ) )
            painter.drawLine( r, self.height() - 1, self.width() - r, self.height() - 1 )
            painter.drawLine( self.width() - 1, r, self.width() - 1, self.height() - r )
            painter.drawArc( self.width() - 2 * r - 1, self.height() - 2 * r - 1, 2 * r, 2 * r, 270 * 16, 90 * 16 )

        else:
            painter.setBrush( QBrush( self.color_press ) )
            painter.drawRoundedRect( 0, 0, self.width(), self.height(), r, r )

        painter.setPen( QPen( self.text_color ) )
        font = QFont()
        font.setPointSize( int( ( 23 / 5 ) * self.text_size - 548 / 5) )
        painter.setFont( font )
        painter.drawText( self.rect(), Qt.AlignmentFlag.AlignCenter, self.button_text )

        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )
            
    def drawSelectionHandles( self, painter ):
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )
            
    def drawSelectionBorder(self, painter):
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
            if not self.resize_corner:
                return

            delta = global_pos - self.resize_start_pos
            new_width = self.resize_start_size.width()
            new_height = self.resize_start_size.height()

            if self.resize_corner == "bottom_right":
                new_width = max( 50, self.resize_start_size.width() + delta.x() )
                new_height = max( 30, self.resize_start_size.height() + delta.y() )

            elif self.resize_corner == "top_right":
                new_width = max( 50, self.resize_start_size.width() + delta.x() )
                new_height = max( 30, self.resize_start_size.height() - delta.y() )

            elif self.resize_corner == "bottom_left":
                new_width = max( 50, self.resize_start_size.width() - delta.x() )
                new_height = max( 30, self.resize_start_size.height() + delta.y() )

            elif self.resize_corner == "top_left":
                new_width = max( 50, self.resize_start_size.width() - delta.x() )
                new_height = max( 30, self.resize_start_size.height() - delta.y() )

            self.setFixedSize( new_width, new_height )
            self.update()
            self.updateButtonPropertiesSize()

    def getCornerAt( self, pos ):
        handle_size = 12 
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None
    

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def updateButtonProperties3D( self ):
        main_window = self.findMainWindow()

        main_window.effect_3d_checkbox.blockSignals( True )
        main_window.effect_3d_checkbox.setChecked( self.effect_3d )
        main_window.effect_3d_checkbox.blockSignals( False )

    def updateButtonPropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'width_spin' ) and hasattr(main_window, 'height_spin' ) ):
            main_window.width_spin.setValue( self.width() )
            main_window.height_spin.setValue( self.height() )
        
    def updateButtonPropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'pos_x_spin' ) and hasattr( main_window, 'pos_y_spin' ) ):
            main_window.pos_x_spin.setValue( self.x() )
            main_window.pos_y_spin.setValue( self.y() )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
        
            mouse_pos = event.pos()
            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos 
                self.clicked.emit( self )
                if self.effect_3d:
                    self.effect_3d_press = False
                    self.updateButtonProperties3D()
                    self.update()         

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            
            self.resizing = False
            self.dragging = False
            self.resize_corner = None
            if self.effect_3d:
                self.effect_3d_press = True
                self.updateButtonProperties3D()
                self.update()
            self.updateButtonPropertiesSize()
            self.updateButtonPropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )
        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            new_x = max( 0, self.x() + delta.x() )
            new_y = max( 0, self.y() + delta.y() )

            self.move(new_x, new_y)
            self.updateButtonPropertiesPosition()
        
        event.accept()

class KeysWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, parent = None ):
        super().__init__( parent )

        self.border_color = QColor( 0, 0, 0 ) 
        self.defaultValues()
        self.setFixedSize( self.keys_width, self.keys_height )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
    def defaultValues( self ):
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.keys_width = 200
        self.keys_height = 120
        self.gradient_start_color = QColor( 255, 255, 255 ) 
        self.gradient_end_color = QColor( 0, 0, 255 )
        self.text_color = QColor( 255, 255, 255 ) 
        self.effect_3d = True
        self.key_type = "QUERTZ"
        self.font_size = 12

        self.key_width = 20
        self.key_height = 20

        self.selected = False
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.drag_start_pos = QPoint()
        self.resize_corner = None
        self.resize_start_size = QSize()

    def paintEvent( self, event ):
            painter = QPainter( self )
            painter.setRenderHint( QPainter.RenderHint.Antialiasing )

            font = QFont()
            font.setPointSize( int( ( 23 / 5 ) * self.font_size - 548 / 5) )
            painter.setFont( font )

            margin_x = 10
            margin_y = 10

            current_x = margin_x
            current_y = margin_y

            r = int( 4 / 5 * self.font_size - 89 / 5 )
            

            if self.key_type == "NUM":
                number = 1
                for i in range( 3 ):
                    for j in range( 3 ):
                        gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                        self.gradient_start_color.setAlpha( 100 )
                        gradient.setColorAt( 0.0, self.gradient_start_color )
                        gradient.setColorAt( 0.4, self.gradient_end_color )   
                        gradient.setColorAt( 1.0, self.gradient_end_color ) 

                        painter.setBrush( gradient )
                        painter.drawRoundedRect( current_x, current_y, self.key_width, self.key_height, r, r )

                        if self.effect_3d:
                            self.draw3dEffect( painter, current_x, current_y, self.key_width, self.key_height )

                        text = str( number )
                        text_rect = painter.boundingRect( current_x, current_y, self.key_width, self.key_height, Qt.AlignmentFlag.AlignCenter, text )
                        painter.setPen( QPen( self.text_color ) )
                        painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, text )

                        current_x += self.key_width + 4
                        number += 1

                    current_x = margin_x
                    current_y += self.key_height + 4

                key_width_0 = self.key_width * 2 + 4 

                gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                self.gradient_start_color.setAlpha( 100 )
                gradient.setColorAt( 0.0, self.gradient_start_color )
                gradient.setColorAt( 0.4, self.gradient_end_color )   
                gradient.setColorAt( 1.0, self.gradient_end_color ) 

                painter.setBrush( gradient )
                painter.drawRoundedRect( current_x, current_y, key_width_0, self.key_height, r, r )

                if self.effect_3d:
                    self.draw3dEffect( painter, current_x, current_y, key_width_0, self.key_height )

                text = "0"
                text_rect = painter.boundingRect( current_x, current_y, key_width_0, self.key_height, Qt.AlignmentFlag.AlignCenter, text )
                painter.setPen( QPen( self.text_color ) )
                painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, text )

                current_x += key_width_0 + 4

                gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                self.gradient_start_color.setAlpha( 100 )
                gradient.setColorAt( 0.0, self.gradient_start_color )
                gradient.setColorAt( 0.4, self.gradient_end_color )   
                gradient.setColorAt( 1.0, self.gradient_end_color ) 

                painter.setBrush( gradient )
                painter.drawRoundedRect( current_x, current_y, self.key_width, self.key_height, r, r )

                if self.effect_3d:
                    self.draw3dEffect( painter, current_x, current_y, self.key_width, self.key_height )

                text = "."
                painter.setPen( QPen( self.text_color ) )
                text_rect = painter.boundingRect( current_x, current_y, self.key_width, self.key_height, Qt.AlignmentFlag.AlignCenter, text )
                painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, text )

            elif self.key_type == "QUERTZ":
                keys_row_1 = "QWERTZUIOP"

                for key in keys_row_1:
                    gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                    self.gradient_start_color.setAlpha( 100 )
                    gradient.setColorAt( 0.0, self.gradient_start_color )
                    gradient.setColorAt( 0.4, self.gradient_end_color )   
                    gradient.setColorAt( 1.0, self.gradient_end_color ) 

                    painter.setBrush( gradient )
                    painter.setPen( QPen( self.border_color, 1 ) )
                    painter.drawRoundedRect( current_x, current_y, self.key_width, self.key_height, r, r )

                    if self.effect_3d:
                        self.draw3dEffect( painter, current_x, current_y, self.key_width, self.key_height )

                    text_rect = painter.boundingRect( current_x, current_y, self.key_width, self.key_height, Qt.AlignmentFlag.AlignCenter, key )
                    painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, key )

                    current_x += self.key_width + 4

                current_x = margin_x + self.key_width // 2
                current_y += self.key_height + 4
                keys_row_2 = "ASDFGHJKL"
                for key in keys_row_2:
                    gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                    self.gradient_start_color.setAlpha( 100 )
                    gradient.setColorAt( 0.0, self.gradient_start_color )
                    gradient.setColorAt( 0.4, self.gradient_end_color )   
                    gradient.setColorAt( 1.0, self.gradient_end_color ) 

                    painter.setBrush( gradient )
                    painter.setPen( QPen( self.border_color, 1 ) )
                    painter.drawRoundedRect( current_x, current_y, self.key_width, self.key_height, r, r )

                    if self.effect_3d:
                        self.draw3dEffect(painter, current_x, current_y, self.key_width, self.key_height )

                    text_rect = painter.boundingRect( current_x, current_y, self.key_width, self.key_height, Qt.AlignmentFlag.AlignCenter, key )
                    painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, key )

                    current_x += self.key_width + 4

                current_x = margin_x
                current_y += self.key_height + 4
                keys_row_3 = [ "Ent", "Y", "X", "C", "V", "B", "N", "M", "Del" ]

                for i, key in enumerate( keys_row_3 ):
                    if key in [ "Ent", "Del" ]:
                        key_width = int( self.key_width * 1.5 )
                    else:
                        key_width = self.key_width

                    gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                    self.gradient_start_color.setAlpha( 100 )
                    gradient.setColorAt( 0.0, self.gradient_start_color )
                    gradient.setColorAt( 0.4, self.gradient_end_color )   
                    gradient.setColorAt( 1.0, self.gradient_end_color ) 

                    painter.setBrush( gradient )
                    painter.setPen( QPen( self.border_color, 1 ) )
                    painter.drawRoundedRect( current_x, current_y, key_width, self.key_height, r, r )

                    if self.effect_3d:
                        self.draw3dEffect( painter, current_x, current_y, key_width, self.key_height )

                    if key in [ "Ent", "Del" ]:
                        small_font = QFont( "Arial", max( 6, self.font_size - 2 ), QFont.Weight.Bold )
                        painter.setFont( small_font )

                    text_rect = painter.boundingRect( current_x, current_y, key_width, self.key_height, Qt.AlignmentFlag.AlignCenter, key )
                    painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, key )

                    painter.setFont( font )

                    current_x += key_width + 4

                current_x = margin_x
                current_y += self.key_height + 4
                space_width = self.keys_width - 2 * margin_x

                gradient = QLinearGradient( current_x, current_y, current_x, current_y + self.key_height )
                self.gradient_start_color.setAlpha( 100 )
                gradient.setColorAt( 0.0, self.gradient_start_color )
                gradient.setColorAt( 0.4, self.gradient_end_color )   
                gradient.setColorAt( 1.0, self.gradient_end_color ) 

                painter.setBrush( gradient )
                painter.setPen( QPen( self.border_color, 1 ) )
                painter.drawRoundedRect( current_x, current_y, space_width, self.key_height, r, r )

                if self.effect_3d:
                    self.draw3dEffect( painter, current_x, current_y, space_width, self.key_height )

                space_font = QFont( "Arial", max( 10, self.font_size ), QFont.Weight.Bold )
                painter.setFont( space_font )

                text_rect = painter.boundingRect( current_x, current_y, space_width, self.key_height, Qt.AlignmentFlag.AlignCenter, "SPACE" )
                painter.drawText( text_rect, Qt.AlignmentFlag.AlignCenter, "SPACE")

            if self.selected:
                self.drawSelectionBorder( painter )
                self.drawSelectionHandles( painter )

    def draw3dEffect( self, painter, x, y, width, height ):
        painter.setPen( QPen( QColor( 255, 255, 255 ), 1 ) )
        painter.drawLine( x, y, x + width, y )
        painter.drawLine( x, y, x, y + height )
        
        painter.setPen( QPen( QColor( 0, 0, 0 ), 1 ) )
        painter.drawLine( x, y + height, x + width, y + height )
        painter.drawLine( x + width, y, x + width, y + height )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
        
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )
    
    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )
    
    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 100, self.resize_start_size.width() + delta.x() )
            new_height = max( 80, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 100, self.resize_start_size.width() + delta.x() )
            new_height = max( 80, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 100, self.resize_start_size.width() - delta.x() )
            new_height = max( 80, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 100, self.resize_start_size.width() - delta.x() )
            new_height = max( 80, self.resize_start_size.height() - delta.y() )

        self.keys_width = max( 100, new_width )
        self.keys_height = max( 80, new_height )
        
        if self.key_type == "NUM":
            self.key_width = max( 15, self.keys_width // 3 - 10 )
            self.key_height = max( 15, self.keys_height // 4 - 8 )

        elif self.key_type == "QUERTZ":
            self.key_width = max( 12, self.keys_width // 10 - 6 )
            self.key_height = max( 15, self.keys_height // 5 - 8 )
        
        self.setFixedSize( self.keys_width, self.keys_height )
        self.update()

    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update()
    
    def updateKeysPropertiesSize( self ):
        main_window = self.findMainWindow()
        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and  main_window.current_shape == self ):
            
            if hasattr( main_window, 'width_spin_keys' ):
                main_window.width_spin_keys.blockSignals( True )
                main_window.width_spin_keys.setValue( self.keys_width )
                main_window.width_spin_keys.blockSignals( False )
                
            if hasattr( main_window, 'height_spin_keys' ):
                main_window.height_spin_keys.blockSignals( True )
                main_window.height_spin_keys.setValue( self.keys_height )
                main_window.height_spin_keys.blockSignals( False )
    
    def updateKeysPropertiesPosition( self ):
        main_window = self.findMainWindow()
        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'pos_x_spin_keys' ):
                main_window.pos_x_spin_keys.blockSignals( True )
                main_window.pos_x_spin_keys.setValue( self.x() )
                main_window.pos_x_spin_keys.blockSignals( False )
                
            if hasattr( main_window, 'pos_y_spin_keys' ):
                main_window.pos_y_spin_keys.blockSignals( True )
                main_window.pos_y_spin_keys.setValue( self.y() )
                main_window.pos_y_spin_keys.blockSignals( False )
    
    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updateKeysPropertiesSize()
            self.updateKeysPropertiesPosition()

        event.accept()
    
    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        
        corner = self.getCornerAt( mouse_pos )
        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )
            self.updateKeysPropertiesSize()
            self.updateKeysPropertiesPosition()

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()

            super().move( new_x, new_y )
            
            self.updateKeysPropertiesPosition()
        
        event.accept()

class ClockWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, diameter, parent = None ):
        super().__init__( parent )

        self.diameter = diameter
        self.setFixedSize( diameter, diameter )
        
        self.background_color = QColor( 0, 0, 255 )
        
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.effect_3d = True
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

        self.setMouseTracking( True )
        self.dragging = False
        self.resizing = False
        self.drag_start_pos = QPoint()
        self.original_geometry = QRect()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )

        r = self.diameter
        center_x = r // 2
        center_y = r // 2

        base_line_width = max( 1, self.getScaledValue( 3 ) )
        big_mark_width = max( 1, self.getScaledValue( 15 ) )
        needle1_width = max( 1, self.getScaledValue( 6 ) )
        needle2_width = max( 1, self.getScaledValue( 8 ) )
        needle3_width = max( 1, self.getScaledValue( 12 ) )

        radius = self.getScaledValue( 360 )
        point_radius = self.getScaledValue( 290 )

        needle1_length = self.getScaledValue( 290 )
        needle2_length = self.getScaledValue( 220 )
        needle3_length = self.getScaledValue( 150 )

        pen = QPen( self.background_color )
        pen.setWidth( base_line_width )
        painter.setPen( pen )
        painter.setBrush( self.background_color )
        painter.drawEllipse( QPointF( center_x, center_y ), radius, radius )

        if self.effect_3d:
            pen = QPen( QColor( 0, 0, 0 ) )
            pen.setWidth( base_line_width )
            painter.setPen( pen )
            painter.drawArc( center_x - radius, center_y - radius, radius * 2, radius * 2, 16 * 35, -16 * 175 )

            pen = QPen( QColor( 0, 0, 0 ) )
            pen.setWidth( base_line_width )
            painter.setPen( pen )
            painter.drawArc( center_x - radius, center_y - radius, radius * 2, radius * 2, 35 * 16, 16 * 185 )

        painter.translate(center_x, center_y)

        seconds_angle = ( self.seconds * 6 ) 
        minutes_angle = ( self.minutes * 6 ) + ( self.seconds * 0.1 )  
        hours_angle = ( ( self.hours % 12 ) * 30 ) + ( self.minutes * 0.5 ) 

        big_pen = QPen( QColor( 0, 0, 0 ) )
        big_pen.setWidth( big_mark_width )
        painter.setPen( big_pen )
        painter.rotate(-180)

        for i in range( 12 ):  
            painter.drawPoint( 0, -point_radius )
            painter.rotate( 30 )

        painter.rotate(-360 + 180)

        painter.rotate( hours_angle )
        needle_pen = QPen( QColor( 0, 0, 0 ) )
        needle_pen.setWidth( needle3_width )
        painter.setPen( needle_pen )
        painter.drawLine( 0, 0, 0, -needle3_length )
        painter.rotate( -hours_angle )

        painter.rotate( minutes_angle )
        needle_pen.setWidth( needle2_width )
        painter.setPen( needle_pen )
        painter.drawLine( 0, 0, 0, -needle2_length )
        painter.rotate( -minutes_angle )

        painter.rotate( seconds_angle )
        needle_pen.setWidth( needle1_width )
        painter.setPen( needle_pen )
        painter.drawLine(0, 0, 0, -needle1_length)

        if self.selected:
            painter.resetTransform()
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint(4, 4), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 50, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 50, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 50, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 50, self.resize_start_size.height() - delta.y() )

        size = min( new_width, new_height )
        
        self.setFixedSize( size, size )
        self.diameter = size
        self.update()

        self.updatePropertiesSize()

    def move( self, x, y ):
        super().move( x, y )
        self.updatePropertiesPosition()

    def getScaledValue( self, original_value ):
        scale_factor = self.diameter / 720.0
        return int( original_value * scale_factor )

    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update() 

    def setDiameter( self, diameter ):
        self.diameter = diameter
        self.setFixedSize( diameter, diameter )
        self.update()

    def setNeedleColor( self, color ):
        self.needle_color = color
        self.update()

    def setBackgroundColor( self, color ):
        self.background_color = color
        self.update()

    def setActive( self, active ):
        self.active = active
        self.update()

    def setVisibleClock( self, visible ):
        self.visible = visible
        self.setVisible( visible )

    def setStatic( self, static ):
        self.static = static
        self.update()

    def setCustomName( self, name ):
        self.custom_name = name

    def setStackOrder( self, order ):
        self.stack_order = order

    def set3d( self, effect_3d ):
        self.effect_3d = effect_3d
        self.update()

    def setHours( self, hours ):
        self.hours = hours % 12
        self.update()

    def setMinutes( self, minutes ):
        self.minutes = minutes % 60
        self.update()

    def setSeconds( self, seconds ):
        self.seconds = seconds % 60 
        self.update()

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'pos_x_spin_clock' ) and hasattr( main_window, 'pos_y_spin_clock' ) ):
            main_window.pos_x_spin_clock.blockSignals( True )
            main_window.pos_x_spin_clock.setValue( self.x() )
            main_window.pos_x_spin_clock.blockSignals( False )
            
            main_window.pos_y_spin_clock.blockSignals( True )
            main_window.pos_y_spin_clock.setValue( self.y() )
            main_window.pos_y_spin_clock.blockSignals( False )

    def updateResizeHandle( self ):
        handle_size = 8
        self.resize_handle.setGeometry( self.width() - handle_size, self.height() - handle_size, handle_size, handle_size )

    def updatePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr(main_window, 'diameter_spin_clock' ) ):
            main_window.diameter_spin_clock.blockSignals( True )
            main_window.diameter_spin_clock.setValue( self.diameter )
            main_window.diameter_spin_clock.blockSignals( False )

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'pos_x_spin_clock' ) and hasattr( main_window, 'pos_y_spin_clock' ) ):
            main_window.pos_x_spin_clock.blockSignals( True )
            main_window.pos_x_spin_clock.setValue( self.x() )
            main_window.pos_x_spin_clock.blockSignals( False )
            
            main_window.pos_y_spin_clock.blockSignals( True )
            main_window.pos_y_spin_clock.setValue( self.y() )
            main_window.pos_y_spin_clock.blockSignals( False )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()
            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        
        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            
            self.updatePropertiesPosition()
            super().move( new_x, new_y )
        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        event.accept()

class GaugeWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, diameter, parent = None ):
        super().__init__( parent )

        self.diameter = diameter
        self.setFixedSize( diameter, diameter )
        
        self.background_color = QColor( 0, 0, 255 )
        
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = ""
        self.stack_order = 1
        self.effect_3d = True
        
        self.major_subdivision = 6 
        self.minor_subdivision = 4
        self.range_value = 100 
        self.value = 50
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        r = self.diameter
        
        base_line_width = max( 1, self.getScaledValue( 3 ) )
        big_mark_width = max( 1, self.getScaledValue( 7 ) )
        small_mark_width = max( 1, self.getScaledValue( 3 ) )
        needle_width = max( 1, self.getScaledValue( 5 ) )
        
        pen = QPen( self.background_color )
        pen.setWidth( base_line_width )
        painter.setPen( pen )
        painter.setBrush( self.background_color )
        painter.drawEllipse( 0, 0, r, r )
        
        if self.effect_3d:
            pen = QPen( QColor( 255, 255, 255 ) )
            pen.setWidth( base_line_width )
            painter.setPen( pen )
            painter.drawArc( 0, 0, r, r, 16 * 35, - 16 * 175 )

            pen = QPen( QColor( 0, 0, 0 ) )
            pen.setWidth( base_line_width )
            painter.setPen( pen )
            painter.drawArc( 0, 0, r, r, 35 * 16, 16 * 185 )
        
        painter.translate( r // 2, r // 2 )
        
        total_divisions = self.major_subdivision * ( self.minor_subdivision + 1 )
        angle_per_division = 270.0 / total_divisions
        
        painter.rotate(-135)

        big_mark_start = self.getScaledValue( - 210 )
        big_mark_end = self.getScaledValue( - 190 )
        
        small_mark_start = self.getScaledValue( - 205 )
        small_mark_end = self.getScaledValue( - 195 )
        
        needle_length = self.getScaledValue( - 210 )

        for i in range( total_divisions + 1 ):
            if i % ( self.minor_subdivision + 1 ) == 0:
                big_pen = QPen( QColor( 0, 0, 0 ) )
                big_pen.setWidth( big_mark_width )
                painter.setPen( big_pen )
                painter.drawLine( 0, big_mark_start, 0, big_mark_end )

            else:
                small_pen = QPen( QColor( 0, 0, 0 ) )
                small_pen.setWidth( small_mark_width )
                painter.setPen( small_pen )
                painter.drawLine( 0, small_mark_start, 0, small_mark_end )
            
            if i < total_divisions:
                painter.rotate( angle_per_division )

        painter.rotate( - ( total_divisions * angle_per_division ) )

        if self.range_value > 0:
            needle_angle = ( 270 * self.value / self.range_value ) 
        else:
            needle_angle = - 135

        painter.rotate( needle_angle )
        needle_pen = QPen( QColor( 0, 0, 0 ) )
        needle_pen.setWidth( needle_width )
        painter.setPen( needle_pen )
        painter.drawLine( 0, 0, 0, needle_length )

        if self.selected:
            painter.resetTransform()
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 50, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 50, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 50, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 50, self.resize_start_size.height() - delta.y() )

        size = min(new_width, new_height)
        self.setFixedSize(size, size)
        self.diameter = size

        self.update()
        self.updatePropertiesSize()

    def getCornerAt( self, pos ):
        handle_size = 12 
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def getScaledValue( self, original_value ):
        scale_factor = self.diameter / 500.0
        return int( original_value * scale_factor )

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setDiameter( self, diameter ):
        self.diameter = diameter
        self.setFixedSize( diameter, diameter )
        self.update()

    def setBackgroundColor( self, color ):
        self.background_color = color
        self.update()

    def setActive( self, active ):
        self.active = active
        self.update()

    def setVisibleGauge( self, visible ):
        self.visible = visible
        self.setVisible( visible )

    def setStatic( self, static ):
        self.static = static
        self.update()

    def setCustomName( self, name ):
        self.custom_name = name

    def setStackOrder( self, order ):
        self.stack_order = order

    def set3d( self, effect_3d ):
        self.effect_3d = effect_3d
        self.update()

    def setMajorSubdivision( self, count ):
        self.major_subdivision = max( 1, count )
        self.update()

    def setMinorSubdivision( self, count ):
        self.minor_subdivision = max( 0, count )
        self.update()

    def setRangeValue( self, value ):
        self.range_value = max( 1, value )

        if self.value > self.range_value:
            self.value = self.range_value

        self.update()

    def setValue( self, value ):
        self.value = max( 0, min( value, self.range_value ) )
        self.update()

    def updatePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'diameter_spin_gauge' ) ):
            main_window.diameter_spin_gauge.blockSignals( True )
            main_window.diameter_spin_gauge.setValue( self.diameter )
            main_window.diameter_spin_gauge.blockSignals( False )

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self and hasattr( main_window, 'pos_x_spin_gauge' ) and hasattr( main_window, 'pos_y_spin_gauge' ) ):
            main_window.pos_x_spin_gauge.blockSignals( True )
            main_window.pos_x_spin_gauge.setValue( self.x() )
            main_window.pos_x_spin_gauge.blockSignals( False )
            
            main_window.pos_y_spin_gauge.blockSignals( True )
            main_window.pos_y_spin_gauge.setValue( self.y() )
            main_window.pos_y_spin_gauge.blockSignals( False )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()
        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            
            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        
        corner = self.getCornerAt( mouse_pos )
        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move( new_x, new_y )
            
            self.updatePropertiesPosition()
        
        event.accept()

class DialWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, diameter, parent = None ):
        super().__init__( parent )
        self.diameter = diameter
        self.setFixedSize( diameter, diameter )
        
        self.dial_color = QColor( 32, 64, 128 )
        self.arc_color = QColor( 0, 0, 0 )   
        self.line_color = QColor( 0, 0, 0 )
        self.background_color = QColor( 32, 64, 128 )
        
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True
        self.value = 0 
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
        self.custom_name = None
        self.stack_order = 1

        self.tag = 0

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        r = self.diameter
        
        base_line_width = max( 1, int( r / 100 ) )
        arc_line_width = max( 1, self.getScaledValue( 3 ) )
        line_width = max( 1, self.getScaledValue( 3 ) )
        
        margin = 3 
        adjusted_r = r - 2 * margin
 
        if self._3d:
            pen = QPen( self.arc_color )
            pen.setWidth( arc_line_width )
            painter.setPen( pen )
            painter.drawArc( margin, margin, adjusted_r, adjusted_r, 16 * 35, - 16 * 175 )
    
            pen = QPen( QColor( 255, 255, 255 ) )
            pen.setWidth( line_width )
            painter.setPen( pen )
            painter.drawArc( margin, margin, adjusted_r, adjusted_r, 35 * 16, 16 * 185 )
        
        pen = QPen( self.dial_color )
        pen.setWidth( base_line_width )
        painter.setPen( pen )
        painter.setBrush( self.background_color )
        painter.drawEllipse( margin, margin, adjusted_r, adjusted_r )
        
        pen = QPen( self.line_color )
        pen.setWidth( line_width )
        painter.setPen( pen )
        
        pen.setWidth( max( 1, self.getScaledValue( 4 ) ) )
        painter.setPen(pen)

        center_x = margin + adjusted_r // 2
        center_y = margin + adjusted_r // 2

        radius = adjusted_r // 2 - 10

        start_radius_percentage = 0.70 
        start_radius = radius * start_radius_percentage

        angle = - 90+ ( 360 * self.value / 100 )
        angle_rad = math.radians( angle )

        start_x = center_x + start_radius * math.cos( angle_rad )
        start_y = center_y + start_radius * math.sin( angle_rad )

        end_x = center_x + radius * math.cos( angle_rad )
        end_y = center_y + radius * math.sin( angle_rad )

        painter.drawLine( int( start_x ), int( start_y ), int( end_x ), int( end_y ) )
    
        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):

        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint(4, 4), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 50, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 50, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 50, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 50, self.resize_start_size.height() - delta.y() )

        size = min( new_width, new_height )
        
        self.setFixedSize( size, size )
        self.diameter = size
        self.update()

        self.updatePropertiesSize()
        self.updatePropertiesPosition()

    def getScaledValue( self, original_value ):
        scale_factor = self.diameter / 100.0
        return int( original_value * scale_factor )

    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setDiameter( self, diameter ):
        self.diameter = diameter
        self.setFixedSize( diameter, diameter )
        self.update()

    def set_dial_color( self, color ):
        self.dial_color = color
        self.update()

    def set_arc_color( self, color ):
        self.arc_color = color
        self.update()

    def setLineColor( self, color ):
        self.line_color = color
        self.update()

    def setBackgroundColor( self, color ):
        self.background_color = color
        self.update()

    def setActive( self, active ):
        self.active = active
        self.update()

    def setVisibleDial( self, visible ):
        self.visible = visible
        self.setVisible( visible )

    def setStatic( self, static ):
        self.static = static
        self.update()

    def setCustomName( self, name ):
        self.custom_name = name

    def setStackOrder( self, order ):
        self.stack_order = order

    def set3d( self, _3d ):
        self._3d = _3d
        self.update()

    def setValue( self, value ):
        self.value = max( 0, min( value, 100 ) )
        self.update()

    def updatePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'diameter_spin_dial' ):
                main_window.diameter_spin_dial.blockSignals( True )
                main_window.diameter_spin_dial.setValue( self.diameter )
                main_window.diameter_spin_dial.blockSignals( False )

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'pos_x_spin_dial' ):
                main_window.pos_x_spin_dial.blockSignals( True )
                main_window.pos_x_spin_dial.setValue( self.x() )
                main_window.pos_x_spin_dial.blockSignals( False )
                
            if hasattr( main_window, 'pos_y_spin_dial' ):
                main_window.pos_y_spin_dial.blockSignals( True )
                main_window.pos_y_spin_dial.setValue( self.y() )
                main_window.pos_y_spin_dial.blockSignals( False )

    def updateAllProperties( self ): 
        self.updatePropertiesSize()
        self.updatePropertiesPosition()

        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            if hasattr( main_window, 'active_checkbox_dial' ):
                main_window.active_checkbox_dial.blockSignals( True )
                main_window.active_checkbox_dial.setChecked( self.active )
                main_window.active_checkbox_dial.blockSignals( False )

            if hasattr( main_window, 'visible_checkbox_dial' ):
                main_window.visible_checkbox_dial.blockSignals( True )
                main_window.visible_checkbox_dial.setChecked( self.visible )
                main_window.visible_checkbox_dial.blockSignals( False )

            if hasattr( main_window, '_3d_checkbox_dial' ):
                main_window._3d_checkbox_dial.blockSignals( True )
                main_window._3d_checkbox_dial.setChecked( self._3d )
                main_window._3d_checkbox_dial.blockSignals( False )

            if hasattr( main_window, 'value_spin_dial' ):
                main_window.value_spin_dial.blockSignals( True )
                main_window.value_spin_dial.setValue( self.value )
                main_window.value_spin_dial.blockSignals( False )

            if hasattr( main_window, 'name_edit_dial' ):
                main_window.name_edit_dial.blockSignals( True )
                main_window.name_edit_dial.setText( self.custom_name )
                main_window.name_edit_dial.blockSignals( False )

            if hasattr( main_window, 'stack_order_spin_dial' ):
                main_window.stack_order_spin_dial.blockSignals( True )

                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index( main_window.current_shape ) + 1
                    main_window.stack_order_spin_dial.setValue( index )

                main_window.stack_order_spin_dial.blockSignals( False )            

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit( self )

                self.updateAllProperties()

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        
        corner = self.getCornerAt( mouse_pos )
        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move( new_x, new_y )
            
            self.updatePropertiesPosition()
        
        event.accept()

class ToggleWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width, height, parent = None ):
        super().__init__( parent )
        self._width = width
        self._height = height 
        self.setFixedSize( width, height )
        
        self.track_color = QColor( 0, 32, 64 ) 
        self.thumb_color = QColor( 0, 64, 128 )
        self.border_color = QColor( 0, 0, 0 ) 
        self.white_border_color = QColor( 236, 238, 241 )
        self.text_color = QColor( 255, 255, 255 ) 
        self.background_color = QColor( 0, 0, 255 )
        
        self.is_on = True
        
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.original_width = 250
        self.original_height = 150

        self.tag=0
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
        self.custom_name = None
        self.stack_order = 1

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        w = self._width
        h = self._height
        
        pen = QPen( self.track_color )
        painter.setPen( pen )
        painter.setBrush( self.background_color )
        
        radius = h // 2
        
        painter.drawRect( radius, 0, w - 2 * radius, h )
        painter.drawPie( 0, 0, 2 * radius, 2 * radius, 90 * 16, 180 * 16 )
        painter.drawPie( w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, - 180 * 16 )
        
        if self._3d:
            pen = QPen( self.white_border_color )
            pen.setWidth( 2 )
            painter.setPen( pen )
            radius = h // 2
            
            painter.drawLine( radius, h, w - radius, h )
            painter.drawArc( w - 2 * radius, 0, 2 * radius, 2 * radius, 45 * 16, - 135 * 16 )
            painter.drawArc( 0, 0, 2 * radius, 2 * radius, 225 * 16, 45 * 16 )
            
            pen = QPen( self.border_color )
            pen.setWidth( 3 )
            painter.setPen( pen )

            painter.drawLine( radius, 0, w - radius, 0 )
            painter.drawArc( 0, 0, 2 * radius, 2 * radius, 90 * 16, 135 * 16 )
            painter.drawArc( w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, - 45 * 16 )
        
        thumb_rect = self.getThumbRect()
        pen = QPen( self.thumb_color )
        painter.setPen( pen )
        painter.setBrush( self.thumb_color )
        
        painter.drawEllipse( thumb_rect )
        
        font = QFont()
        font_size = max( 8, h // 2 )
        font.setPointSize( font_size )
        painter.setFont( font )
        painter.setPen( self.text_color )
        
        if self.is_on:
            text_rect = QRect( 10, 0, w - thumb_rect.width() - 20, h )
            painter.drawText( text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "OFF" )
        else:
            text_rect = QRect( thumb_rect.width() + 10, 0, w - thumb_rect.width() - 20, h )
            painter.drawText( text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, "ON" )
        
        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint(4, 4), QPoint(self.width()-4, 4), ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) ) 
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos
        new_width = self.resize_start_size.width()

        if self.resize_corner == "right":
            new_width = max( 80, self.resize_start_size.width() + delta.x() )

        elif self.resize_corner == "left":
            new_width = max( 80, self.resize_start_size.width() - delta.x() )
            width_delta = self._width - new_width
            self.move( self.x() + width_delta, self.y() )

        self.setSize( new_width, self._height )

    def move( self, x, y ):
        super().move( x, y )
        
        main_window = self.findMainWindow()

        if main_window and main_window.current_shape == self:
            try:
                if hasattr( main_window, 'pos_x_spin_toggle' ):
                    main_window.pos_x_spin_toggle.blockSignals( True )
                    main_window.pos_x_spin_toggle.setValue( x )
                    main_window.pos_x_spin_toggle.blockSignals( False )

            except RuntimeError:
                pass
            
            try:
                if hasattr( main_window, 'pos_y_spin_toggle' ):
                    main_window.pos_y_spin_toggle.blockSignals( True )
                    main_window.pos_y_spin_toggle.setValue( y )
                    main_window.pos_y_spin_toggle.blockSignals( False )

            except RuntimeError:
                pass

    def toggleState( self ):
        self.setState( not self.is_on )

    def getScaledValue( self, original_value, is_width = True ):
        if is_width:
            scale_factor = self._width / self.original_width

        else:
            scale_factor = self._height / self.original_height

        return int( original_value * scale_factor )
    
    def getWidth( self ):
        return self._width

    def getHeight( self ):
        return self._height
    
    def getState( self ):
        return self.is_on

    def getCornerAt( self, pos ):
        handle_size = 12 
        half_size = handle_size // 2
        
        corners = {
            "left": QPoint( 0, self.height() // 2 ),
            "right": QPoint( self.width(), self.height() // 2 )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def getThumbRect( self ):
        thumb_height = self._height - 10
        thumb_width = thumb_height
        
        if self.is_on:
            thumb_x = self._width - thumb_width - 5

        else:
            thumb_x = 5
            
        thumb_y = 5
        
        return QRect( thumb_x, thumb_y, thumb_width, thumb_height )

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setSize( self, width, height ):
        self._width = width
        self._height = 30 
        self.setFixedSize( width, self._height )
        
        main_window = self.findMainWindow()

        if main_window and hasattr( main_window, 'current_shape' ) and main_window.current_shape == self:
            try:
                if hasattr( main_window, 'width_spin_toggle' ):
                    main_window.width_spin_toggle.blockSignals( True )
                    main_window.width_spin_toggle.setValue( width )
                    main_window.width_spin_toggle.blockSignals( False )

            except RuntimeError:
                pass
        
        self.update()

    def setTrackColor( self, color ):
        self.track_color = color
        self.update()

    def setThumbColor( self, color ):
        self.thumb_color = color
        self.update()

    def setBorderColor( self, color ):
        self.border_color = color
        self.update()

    def setWhiteBorderColor( self, color ):
        self.white_border_color = color
        self.update()

    def setTextColor( self, color ):
        self.text_color = color
        self.update()

    def setBackgroundColor( self, color ):
        self.background_color = color
        self.update()

    def setState( self, is_on ):
        self.is_on = is_on
        self.update()
        
        main_window = self.findMainWindow()

        if main_window and main_window.current_shape == self:
            try:
                if hasattr( main_window, 'state_checkbox_toggle' ):
                    main_window.state_checkbox_toggle.blockSignals( True )
                    main_window.state_checkbox_toggle.setChecked( self.is_on )
                    main_window.state_checkbox_toggle.blockSignals( False )

            except RuntimeError:
                pass

    def setActive( self, active ):
        self.active = active
        self.setEnabled( active )
        self.update()

    def setVisibleToggle( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def setStatic( self, static ):
        self.static = static
        self.update()

    def set3d( self, _3d ):
        self._3d = _3d
        self.update()

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos

                thumb_rect = self.getThumbRect()

                if thumb_rect.contains( event.pos() ):
                    self.toggleState()

                self.clicked.emit(self)

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()

        corner = self.getCornerAt( mouse_pos )
        if corner:
            self.setCursor( Qt.CursorShape.SizeHorCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )

        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos

            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            self.move( new_x, new_y )

        event.accept()

class ScrollBarWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width, height, parent = None ):
        super().__init__( parent )
        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        
        self.track_color = QColor( 0, 0, 255 ) 
        self.thumb_color = QColor( 0, 64, 128 )
        self.border_color = QColor( 0, 0, 0 )
        self.white_border_color = QColor( 236, 238, 241 )
        
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.stack_order = 1
        self._3d = True 
        
        self.range_value = 100 
        self.current_value = 50
        self.thumb_size = 30
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.thumb_dragging = False
        self.thumb_drag_start_pos = QPoint()
        self.thumb_drag_start_value = 0

        self.tag = 0

        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        w = self._width
        h = self._height
        
        radius = h // 2
        
        pen = QPen( self.track_color )
        pen.setWidth( 3 )
        painter.setPen( pen )
        painter.setBrush( self.track_color )
        
        painter.drawPie( 0, 0, 2 * radius, 2 * radius, 90 * 16, 180 * 16 )
        painter.drawRect( radius, 0, w - 2 * radius, h )
        painter.drawPie( w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, - 180 * 16 )
        
        thumb_rect = self.getThumbRect()
        pen = QPen( self.thumb_color )
        pen.setWidth( 2 )
        painter.setPen( pen )
        painter.setBrush( self.thumb_color )
        
        thumb_radius = thumb_rect.height() // 2
        
        painter.drawPie( thumb_rect.x(), thumb_rect.y(), 2 * thumb_radius, 2 * thumb_radius, 90 * 16, 180 * 16 )
        painter.drawRect( thumb_rect.x() + thumb_radius, thumb_rect.y(), thumb_rect.width() - 2 * thumb_radius, thumb_rect.height() )
        painter.drawPie( thumb_rect.x() + thumb_rect.width() - 2 * thumb_radius, thumb_rect.y(), 2 * thumb_radius, 2 * thumb_radius, 90 * 16, -180 * 16 )
        
        if self._3d:
            pen = QPen( self.white_border_color )
            pen.setWidth( 1 )
            painter.setPen( pen )
            
            painter.drawLine( thumb_rect.x() + thumb_radius, thumb_rect.y(), thumb_rect.x() + thumb_rect.width() - thumb_radius, thumb_rect.y())
            painter.drawArc( thumb_rect.x(), thumb_rect.y(), 2 * thumb_radius, 2 * thumb_radius, 90 * 16, 135 * 16 )
            
            pen.setWidth( 3 )
            painter.setPen( pen )
            
            painter.drawLine( radius, h, w - radius, h )
            painter.drawArc( w - 2 * radius, 0, 2 * radius, 2 * radius, 45 * 16, - 135 * 16 )
            painter.drawArc( 0, 0, 2 * radius, 2 * radius, 225 * 16, 45 * 16 )
            
            pen = QPen( self.border_color )
            pen.setWidth( 1 )
            painter.setPen( pen )

            painter.drawLine( thumb_rect.x() + thumb_radius, thumb_rect.y() + thumb_rect.height(), thumb_rect.x() + thumb_rect.width() - thumb_radius, thumb_rect.y() + thumb_rect.height() )
            painter.drawArc( thumb_rect.x() + thumb_rect.width() - 2 * thumb_radius, thumb_rect.y(), 2 * thumb_radius, 2 * thumb_radius, 45 * 16, - 135 * 16 )
            
            pen.setWidth( 3 )
            painter.setPen( pen )
            
            painter.drawLine( radius, 0, w - radius, 0 )
            painter.drawArc( w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, - 45 * 16 )
            painter.drawArc( 0, 0, 2 * radius, 2 * radius, 90 * 16, 135 * 16 )
        
        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )

            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 100, self.resize_start_size.width() + delta.x() )
            new_height = max( 10, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 100, self.resize_start_size.width() + delta.x() )
            new_height = max( 10, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 100, self.resize_start_size.width() - delta.x() )
            new_height = max( 10, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 100, self.resize_start_size.width() - delta.x() )
            new_height = max( 10, self.resize_start_size.height() - delta.y() )

        self.setSize(new_width, new_height)
        self.updatePropertiesSize()
        self.updatePropertiesPosition()

    def calculateValueFromPosition( self, x ):
        track_rect = self.getTrackRect()
        thumb_rect = self.getThumbRect()
        
        relative_x = x - track_rect.x() - thumb_rect.width() / 2
        track_width = track_rect.width() - thumb_rect.width()
        
        if track_width > 0:
            value = int( ( relative_x / track_width ) * self.range_value )

            return max( 0, min( self.range_value, value ) )
        
        return self.current_value

    def getCurrentValue( self ):
        return self.current_value

    def getThumbSize( self ):
        return self.thumb_size
    
    def getWidth( self ):
        return self._width

    def getHeight( self ):
        return self._height

    def getCurrentValue( self ):
        return self.current_value

    def getCornerAt( self, pos ):
        handle_size = 12 
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def getTrackRect( self ):
        w = self._width
        h = self._height
        
        radius = h // 2
        
        return QRect( radius, 0, w - 2 * radius, h )

    def getThumbRect( self ):
        track_rect = self.getTrackRect()
        
        thumb_width = int( track_rect.width() * ( self.thumb_size / 100.0 ) )
        thumb_width = max( 20, min( track_rect.width(), thumb_width ) )
        
        max_position = track_rect.width() - thumb_width

        if max_position > 0:
            thumb_x = track_rect.x() + int( ( self.current_value / self.range_value ) * max_position )

        else:
            thumb_x = track_rect.x()
        
        thumb_height = int( h * 0.6 ) if ( h := self._height ) > 20 else h - 4
        thumb_y = ( h - thumb_height ) // 2
        
        return QRect( thumb_x, thumb_y, thumb_width, thumb_height )
    
    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setSize( self, width, height ):
        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        self.update()

    def setTrackColor( self, color ):
        self.track_color = color
        self.update()

    def setThumbColor( self, color ):
        self.thumb_color = color
        self.update()

    def setBorderColor( self, color ):
        self.border_color = color
        self.update()

    def setWhiteBorderColor( self, color ):
        self.white_border_color = color
        self.update()

    def setVisibleScrollBar( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def set3d( self, _3d ):
        self._3d = _3d
        self.update()

    def setRange( self, value ):
        self.range_value = max(1, value)
        self.update()

    def setCurrentValue( self, value ):
        self.current_value = max( 0, min( self.range_value, value ) )
        self.update()

    def setThumbSize( self, size ):
        self.thumb_size = max( 10, min( 100, size ) )
        self.update()

    def updatePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'width_spin_scrollbar' ):
                main_window.width_spin_scrollbar.blockSignals( True )
                main_window.width_spin_scrollbar.setValue( self._width )
                main_window.width_spin_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'height_spin_scrollbar' ):
                main_window.height_spin_scrollbar.blockSignals( True )
                main_window.height_spin_scrollbar.setValue( self._height )
                main_window.height_spin_scrollbar.blockSignals( False )

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'pos_x_spin_scrollbar' ):
                main_window.pos_x_spin_scrollbar.blockSignals( True )
                main_window.pos_x_spin_scrollbar.setValue( self.x() )
                main_window.pos_x_spin_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'pos_y_spin_scrollbar' ):
                main_window.pos_y_spin_scrollbar.blockSignals( True )
                main_window.pos_y_spin_scrollbar.setValue( self.y() )
                main_window.pos_y_spin_scrollbar.blockSignals( False )

    def updatePropertiesValue( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if (hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'current_value_spin_scrollbar' ):
                main_window.current_value_spin_scrollbar.blockSignals( True )
                main_window.current_value_spin_scrollbar.setValue( self.current_value )
                main_window.current_value_spin_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'thumb_size_spin_scrollbar' ):
                main_window.thumb_size_spin_scrollbar.blockSignals( True )
                main_window.thumb_size_spin_scrollbar.setValue( self.thumb_size )
                main_window.thumb_size_spin_scrollbar.blockSignals( False )

    def updateAllProperties( self ):
        self.updatePropertiesSize()
        self.updatePropertiesPosition()
        self.updatePropertiesValue()
        
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'active_checkbox_scrollbar' ):
                main_window.active_checkbox_scrollbar.blockSignals( True )
                main_window.active_checkbox_scrollbar.setChecked( self.active )
                main_window.active_checkbox_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'visible_checkbox_scrollbar' ):
                main_window.visible_checkbox_scrollbar.blockSignals( True )
                main_window.visible_checkbox_scrollbar.setChecked( self.visible )
                main_window.visible_checkbox_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'static_checkbox_scrollbar' ):
                main_window.static_checkbox_scrollbar.blockSignals( True )
                main_window.static_checkbox_scrollbar.setChecked( self.static )
                main_window.static_checkbox_scrollbar.blockSignals( False )
                
            if hasattr(main_window, '_3d_checkbox_scrollbar'):
                main_window._3d_checkbox_scrollbar.blockSignals( True )
                main_window._3d_checkbox_scrollbar.setChecked( self._3d )
                main_window._3d_checkbox_scrollbar.blockSignals( False )
            
            if hasattr( main_window, 'range_spin_scrollbar' ):
                main_window.range_spin_scrollbar.blockSignals( True )
                main_window.range_spin_scrollbar.setValue( self.range_value )
                main_window.range_spin_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'current_value_spin_scrollbar' ):
                main_window.current_value_spin_scrollbar.blockSignals( True )
                main_window.current_value_spin_scrollbar.setValue( self.current_value )
                main_window.current_value_spin_scrollbar.blockSignals( False )
                
            if hasattr( main_window, 'thumb_size_spin_scrollbar' ):
                main_window.thumb_size_spin_scrollbar.blockSignals( True )
                main_window.thumb_size_spin_scrollbar.setValue( self.thumb_size )
                main_window.thumb_size_spin_scrollbar.blockSignals( False )
            
            if hasattr( main_window, 'name_edit_scrollbar' ):
                main_window.name_edit_scrollbar.blockSignals( True )
                main_window.name_edit_scrollbar.setText( self.custom_name )
                main_window.name_edit_scrollbar.blockSignals( False )
            
            if hasattr( main_window, 'stack_order_spin_scrollbar' ):
                main_window.stack_order_spin_scrollbar.blockSignals( True )

                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index( main_window.current_shape ) + 1
                    main_window.stack_order_spin_scrollbar.setValue( index )

                main_window.stack_order_spin_scrollbar.blockSignals( False )
            
            if hasattr( main_window, 'track_color_rect_scrollbar' ):
                main_window.track_color_rect_scrollbar.setStyleSheet( f"background-color: { self.track_color.name() }; border: 1px solid #ccc;" )
                
            if hasattr( main_window, 'thumb_color_rect_scrollbar' ):
                main_window.thumb_color_rect_scrollbar.setStyleSheet( f"background-color: { self.thumb_color.name() }; border: 1px solid #ccc;" )
                
            if hasattr( main_window, 'border_color_rect_scrollbar' ):
                main_window.border_color_rect_scrollbar.setStyleSheet( f"background-color: { self.border_color.name() }; border: 1px solid #ccc;" )
                
            if hasattr( main_window, 'white_border_color_rect_scrollbar' ):
                main_window.white_border_color_rect_scrollbar.setStyleSheet( f"background-color: { self.white_border_color.name() }; border: 1px solid #ccc;" )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                thumb_rect = self.getThumbRect()

                if thumb_rect.contains( event.pos() ):
                    self.thumb_dragging = True
                    self.dragging = False
                    self.thumb_drag_start_pos = event.pos()
                    self.thumb_drag_start_value = self.current_value

                else:
                    self.dragging = True
                    self.thumb_dragging = False
                    self.drag_start_pos = mouse_pos
                    track_rect = self.getTrackRect()

                    if track_rect.contains( event.pos() ):
                        new_value = self.calculateValueFromPosition( event.pos().x() )
                        self.setCurrentValue( new_value )
                
                self.clicked.emit( self )
                self.updateAllProperties()

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.thumb_dragging = False
            self.resize_corner = None

            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        
        corner = self.getCornerAt( mouse_pos )
        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )

        elif self.thumb_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta_x = mouse_pos.x() - self.thumb_drag_start_pos.x()
            track_rect = self.getTrackRect()
            thumb_rect = self.getThumbRect()
            
            track_width = track_rect.width() - thumb_rect.width()
            
            if track_width > 0:
                pixels_per_unit = track_width / self.range_value
                delta_value = int( delta_x / pixels_per_unit )
                new_value = self.thumb_drag_start_value + delta_value
                self.setCurrentValue( new_value )
                
                self.updatePropertiesValue()

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move( new_x, new_y )
            
            self.updatePropertiesPosition()
        
        event.accept()


class SliderWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width, height, parent = None ):
        super().__init__( parent )

        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        
        self.track_color = QColor( 0, 32, 64 )
        self.thumb_color = QColor( 255, 255, 255 )
        self.progress_color = QColor( 0, 32, 64 )
        self.border_color = QColor( 0, 0, 0 ) 
        
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True  
        self.custom_name = None
        self.stack_order = 1

        self.tag = 0
        
        self.value = 50
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.selected = False
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )

        track_rect = self.getTrackRect()
        progress_rect = self.getProgressRect()
        thumb_rect = self.getThumbRect()
        track_right_rect = self.getTrackRightRect()

        radius = track_rect.height() // 2

        pen = QPen( self.border_color )
        pen.setWidth( 3 )
        painter.setPen( pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )

        painter.drawArc( track_rect.x() - radius, track_rect.y(), radius * 2, radius * 2, 90 * 16, 180 * 16 )
        painter.drawArc( track_rect.x() + track_rect.width() - radius, track_rect.y(), radius * 2, radius * 2, 90 * 16, - 180 * 16 )
        painter.drawLine( track_rect.x(), track_rect.y(), track_rect.x() + track_rect.width(), track_rect.y())
        painter.drawLine( track_rect.x(), track_rect.y() + track_rect.height(), track_rect.x() + track_rect.width(), track_rect.y() + track_rect.height() )

        if track_right_rect.width() > 0:
            pen = QPen( self.track_color )
            pen.setWidth( 3 )
            painter.setPen( pen )
            painter.setBrush( self.track_color )

            if track_right_rect.width() > radius:
                painter.drawPie( track_rect.x() + track_rect.width() - radius, track_rect.y(), radius * 2, radius * 2, 90 * 16, - 180 * 16 )
                painter.drawRect( track_right_rect.x(), track_rect.y(), track_right_rect.width(), track_rect.height() )

            else:
                painter.drawRect( track_right_rect.x(), track_rect.y(), track_right_rect.width(), track_rect.height() )

        if progress_rect.width() > 0:
            pen = QPen( self.thumb_color )
            pen.setWidth( 3 )
            painter.setPen( pen )
            painter.setBrush( self.thumb_color )

            if progress_rect.width() > radius:
                painter.drawPie( track_rect.x() - radius, track_rect.y(), radius * 2, radius * 2, 90 * 16, 180 * 16 )
                painter.drawRect( track_rect.x(), track_rect.y(), progress_rect.width() - radius, track_rect.height() )

            else:
                painter.drawRect( track_rect.x(), track_rect.y(), progress_rect.width(), track_rect.height() )

            if track_right_rect.width() > 0:
                pen = QPen( QColor(0, 0, 0) )
                pen.setWidth( 2 )
                painter.setPen( pen )

                painter.drawLine( track_rect.x(), track_rect.y()-1, track_rect.x() + progress_rect.width(), track_rect.y() - 1 )
                painter.drawLine( track_rect.x(), track_rect.y() + progress_rect.height()+1, track_rect.x() + progress_rect.width(), track_rect.y() + progress_rect.height() + 1 )
                painter.drawArc( track_rect.x() - radius - 1, track_rect.y() - 1, radius * 2 + 2, radius * 2 + 2, 90 * 16, 180 * 16 )

        pen = QPen( self.progress_color )
        pen.setWidth( 3 )
        painter.setPen( pen )
        painter.setBrush( self.progress_color )
        painter.drawEllipse( thumb_rect )

        if self._3d:
            if progress_rect.width() > 0:
                pen = QPen( QColor( 255, 255, 255 ) )
                pen.setWidth( 1 )
                painter.setPen( pen )
                painter.drawLine( track_right_rect.x(), track_rect.y() - 1, track_rect.x() + track_rect.width(), track_rect.y() - 1 )
                painter.drawLine( track_right_rect.x(), track_rect.y() + progress_rect.height() + 1, track_rect.x() + track_rect.width(), track_rect.y() + progress_rect.height() + 1 )
                painter.drawArc( track_rect.x() + track_rect.width() - radius - 1, track_rect.y() - 1, radius * 2 + 2, radius * 2 + 2, 90 * 16, - 180 * 16 )

            pen = QPen( QColor( 236, 238, 241 ) )
            pen.setWidth( 1 )
            painter.setPen( pen )
            painter.drawArc( thumb_rect, 40 * 16, 160 * 16 )

            pen = QPen( QColor( 0, 0, 0 ) )
            pen.setWidth( 1 )
            painter.setPen( pen )
            painter.drawArc( thumb_rect, 200 * 16, 180 * 16 )

        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):

        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ): 

        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos
        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 100, self.resize_start_size.width() + delta.x() )
            new_height = max( 30, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 100, self.resize_start_size.width() + delta.x() )
            new_height = max( 30, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 100, self.resize_start_size.width() - delta.x() )
            new_height = max( 30, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 100, self.resize_start_size.width() - delta.x() )
            new_height = max( 30, self.resize_start_size.height() - delta.y() )

        self.setSize( new_width, new_height )

    def getValue( self ):
        return self.value

    def getWidth( self ):
        return self._width

    def getHeight( self ):
        return self._height

    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def getTrackRect( self ):
        w = self._width
        h = self._height
        
        track_height = h // 3
        track_y = h // 3
        radius = h // 6 
        
        return QRect( radius, track_y, w - 2 * radius, track_height )

    def getProgressRect( self ):
        track_rect = self.getTrackRect()
        progress_width = int( track_rect.width() * self.value / 100 )
        
        return QRect( track_rect.x(), track_rect.y(), progress_width, track_rect.height() )

    def getTrackRightRect( self ):
        track_rect = self.getTrackRect()
        thumb_rect = self.getThumbRect()
        
        start_x = thumb_rect.x() + thumb_rect.width()
        width = track_rect.x() + track_rect.width() - start_x
        
        if width > 0:
            return QRect( start_x, track_rect.y(), width, track_rect.height() )
        return QRect()

    def getThumbRect( self ):
        track_rect = self.getTrackRect()
        
        thumb_diameter = min( track_rect.height() * 2, self._height * 0.8 )
        
        thumb_x = track_rect.x() + int( ( track_rect.width() - thumb_diameter ) * ( self.value / 100 ) )
        thumb_y = ( self._height - thumb_diameter ) // 2
        
        return QRect( thumb_x, thumb_y, thumb_diameter, thumb_diameter )

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setSize( self, width, height ):
        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        self.update()

    def setTrackColor( self, color ):
        self.track_color = color
        self.update()

    def setThumbColor( self, color ):
        self.thumb_color = color
        self.update()

    def setProgressColor( self, color ):
        self.progress_color = color
        self.update()

    def setBorderColor( self, color ):
        self.border_color = color
        self.update()

    def setRange( self, value ):
        self.range_value = max(1, value)
        self.update()

    def setValue( self, value ):
        self.value = max( 0, min( 100, value ) )
        self.update()

    def setVisibleSlider( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def set3d( self, _3d ):
        self._3d = _3d
        self.update()

    def updatePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            
            if hasattr( main_window, 'width_spin_slider' ):
                main_window.width_spin_slider.blockSignals( True )
                main_window.width_spin_slider.setValue( self._width )
                main_window.width_spin_slider.blockSignals( False )
                
            if hasattr( main_window, 'height_spin_slider' ):
                main_window.height_spin_slider.blockSignals( True )
                main_window.height_spin_slider.setValue( self._height )
                main_window.height_spin_slider.blockSignals( False )

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            if hasattr( main_window, 'pos_x_spin_slider' ):
                main_window.pos_x_spin_slider.blockSignals( True )
                main_window.pos_x_spin_slider.setValue( self.x() )
                main_window.pos_x_spin_slider.blockSignals( False )
                
            if hasattr( main_window, 'pos_y_spin_slider' ):
                main_window.pos_y_spin_slider.blockSignals( True )
                main_window.pos_y_spin_slider.setValue( self.y() )
                main_window.pos_y_spin_slider.blockSignals( False )

    def updateAllProperties( self ):
        self.updatePropertiesSize()
        self.updatePropertiesPosition()
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            if hasattr( main_window, 'active_checkbox_slider' ):
                main_window.active_checkbox_slider.blockSignals( True )
                main_window.active_checkbox_slider.setChecked( self.active )
                main_window.active_checkbox_slider.blockSignals( False )
                
            if hasattr( main_window, 'visible_checkbox_slider' ):
                main_window.visible_checkbox_slider.blockSignals( True )
                main_window.visible_checkbox_slider.setChecked( self.visible )
                main_window.visible_checkbox_slider.blockSignals( False )
                
            if hasattr( main_window, 'static_checkbox_slider' ):
                main_window.static_checkbox_slider.blockSignals( True )
                main_window.static_checkbox_slider.setChecked( self.static )
                main_window.static_checkbox_slider.blockSignals( False )
                
            if hasattr( main_window, '_3d_checkbox_slider' ):
                main_window._3d_checkbox_slider.blockSignals( True )
                main_window._3d_checkbox_slider.setChecked( self._3d )
                main_window._3d_checkbox_slider.blockSignals( False )

            if hasattr( main_window, 'range_spin_slider' ):
                main_window.value_spin_dial.blockSignals( True )
                main_window.value_spin_dial.setValue( self.value )
                main_window.value_spin_dial.blockSignals( False )

            if hasattr( main_window, 'value_spin_slider' ):
                main_window.value_spin_slider.blockSignals( True )
                main_window.value_spin_slider.setValue( self.value )
                main_window.value_spin_slider.blockSignals( False )
            
            if hasattr( main_window, 'name_edit_slider' ):
                main_window.name_edit_slider.blockSignals( True )
                main_window.name_edit_slider.setText( self.custom_name )
                main_window.name_edit_slider.blockSignals( False )
            
            if hasattr( main_window, 'stack_order_spin_slider' ):
                main_window.stack_order_spin_slider.blockSignals( True )

                if main_window.current_shape in main_window.all_shapes:
                    index = main_window.all_shapes.index( main_window.current_shape ) + 1
                    main_window.stack_order_spin_slider.setValue( index )

                main_window.stack_order_spin_slider.blockSignals( False )
            
            if hasattr( main_window, 'bg_left_color_rect_slider' ):
                main_window.bg_left_color_rect_slider.setStyleSheet( f"background-color: { self.thumb_color.name() }; border: 1px solid #ccc;" )
                
            if hasattr( main_window, 'bg_right_color_rect_slider' ):
                main_window.bg_right_color_rect_slider.setStyleSheet( f"background-color: { self.track_color.name()} ; border: 1px solid #ccc;" )
                
            if hasattr(main_window, 'thumb_color_rect_slider'):
                main_window.thumb_color_rect_slider.setStyleSheet( f"background-color: { self.progress_color.name() }; border: 1px solid #ccc;" )


    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                thumb_rect = self.getThumbRect()

                if thumb_rect.contains(event.pos()):
                    pass

                else:
                    track_rect = self.getTrackRect()

                    if track_rect.contains( event.pos() ):
                        relative_x = event.pos().x() - track_rect.x()
                        new_value = int( ( relative_x / track_rect.width() ) * 100 )
                        self.setValue( new_value )
                
                self.clicked.emit( self )
                self.updateAllProperties()

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )
            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos

            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()

            super().move( new_x, new_y )
            self.updatePropertiesPosition()
        
        event.accept()

class ProgressBarWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width, height, parent = None ):
        super().__init__( parent )
        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        
        self.bar_color = QColor( 0, 0, 255 ) 
        self.progress_color = QColor( 255, 255, 255 )
        self.border_color = QColor( 0, 0, 0 ) 
        self.white_border_color = QColor( 236, 238, 241 )
        
        self.progress_value = 50
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.custom_name = ""
        self.stack_order = 1
        self.active = True
        self.visible = True
        self.static = False
        self._3d = True
        self.value = 50
        self.min_value = 0
        self.max_value = 100
        
        self.resizing = False
        self.dragging = False
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        w = self._width
        h = self._height

        pen = QPen( self.bar_color )
        pen.setWidth( 3 )
        painter.setPen( pen )
        painter.setBrush( self.bar_color )
        
        radius = h // 2
        
        painter.drawPie( 0, 0, 2 * radius, 2 * radius, 90 * 16, 180 * 16 )
        painter.drawRect( radius, 0, w - 2 * radius, h )
        painter.drawPie(w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, - 180 * 16 )
        
        pen = QPen( self.progress_color )
        pen.setWidth( 3 )
        painter.setPen( pen )
        painter.setBrush( self.progress_color )
        
        progress_width = int( ( w - 2 * radius ) * ( self.progress_value / 100.0 ) )
        
        inner_offset = 6 
        inner_radius = radius - inner_offset // 2
        
        painter.drawPie( inner_offset // 2, inner_offset // 2, 2 * inner_radius, 2 * inner_radius, 90 * 16, 180 * 16 )
        painter.drawRect( radius - 3 + inner_offset // 2, inner_offset // 2, progress_width, 2 * inner_radius )
        painter.drawPie( inner_offset // 2 + progress_width, inner_offset // 2, 2 * inner_radius, 2 * inner_radius, 90 * 16, - 180 * 16 )

        if self._3d:
            pen = QPen( self.border_color )
            pen.setWidth( 2 )
            painter.setPen( pen )

            painter.drawLine( radius, 0, w - radius, 0 )
            painter.drawArc( w - 2 * radius, 0, 2 * radius, 2 * radius, 90 * 16, - 45 * 16 )
            painter.drawArc( 0, 0, 2 * radius, 2 * radius, 90 * 16, 135 * 16 )

            pen = QPen( self.white_border_color )
            pen.setWidth( 1 )
            painter.setPen( pen )

            painter.drawLine( radius, h, w - radius, h )
            painter.drawArc( w - 2 * radius, 0, 2 * radius, 2 * radius, 45 * 16, - 135 * 16 )
            painter.drawArc( 0, 0, 2 * radius, 2 * radius, 225 * 16, 45 * 16 )

        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint(4, 4), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def move(self, x, y):
        super().move(x, y)
        
        main_window = self.findMainWindow()
        if main_window and main_window.current_shape == self:
            try:
                if hasattr( main_window, 'progress_pos_x_spin' ):
                    main_window.progress_pos_x_spin.blockSignals( True )
                    main_window.progress_pos_x_spin.setValue( x )
                    main_window.progress_pos_x_spin.blockSignals( False )

            except RuntimeError:
                pass
            
            try:
                if hasattr( main_window, 'progress_pos_y_spin' ):
                    main_window.progress_pos_y_spin.blockSignals( True )
                    main_window.progress_pos_y_spin.setValue( y )
                    main_window.progress_pos_y_spin.blockSignals( False )

            except RuntimeError:
                pass

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos
        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 5, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 50, self.resize_start_size.width() + delta.x() )
            new_height = max( 5, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 5, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 50, self.resize_start_size.width() - delta.x() )
            new_height = max( 5, self.resize_start_size.height() - delta.y() )

        self.setSize( new_width, new_height )

    def get_progress( self ):
        return self.progress_value

    def getWidth( self ):
        return self._width

    def getHeight( self ):
        return self._height

    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setSize( self, width, height ):
        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        
        main_window = self.findMainWindow()

        if main_window and main_window.current_shape == self:
            try:
                if hasattr( main_window, 'progress_width_spin' ):
                    main_window.progress_width_spin.blockSignals( True )
                    main_window.progress_width_spin.setValue( width )
                    main_window.progress_width_spin.blockSignals( False )

            except RuntimeError:
                pass
            
            try:
                if hasattr( main_window, 'progress_height_spin' ):
                    main_window.progress_height_spin.blockSignals( True )
                    main_window.progress_height_spin.setValue( height )
                    main_window.progress_height_spin.blockSignals( False )

            except RuntimeError:
                pass
        
        self.update()

    def setBarColor( self, color ):
        self.bar_color = color
        self.update()

    def setProgressColor( self, color ):
        self.progress_color = color
        self.update()

    def setBorderColor( self, color ):
        self.border_color = color
        self.update()

    def setWhiteBorderColor( self, color ):
        self.white_border_color = color
        self.update()

    def setProgress( self, value ):
        self.progress_value = max( 0, min( 100, value ) )
        self.update()

    def setActive( self, active ):
        self.active = active
        self.update()

    def setVisibleProgressBar( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def setStatic( self, static ):
        self.static = static
        self.update()

    def set3d( self, _3d ):
        self._3d = _3d
        self.update()

    def setValue( self, value ):
        self.value = max( self.min_value, min( self.max_value, value ) )
        progress_range = self.max_value - self.min_value

        if progress_range > 0:
            self.progress_value = int( ( ( self.value - self.min_value) / progress_range ) * 100 )

        self.update()

    def setRange( self, min_value, max_value ):
        self.min_value = min_value
        self.max_value = max_value
        self.value = max( min_value, min( max_value, self.value ) )
        progress_range = self.max_value - self.min_value

        if progress_range > 0:
            self.progress_value = int( ( ( self.value - self.min_value ) / progress_range ) * 100 )

        self.update()

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                
                self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

        event.accept()

    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        corner = self.getCornerAt(mouse_pos)

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize(event.globalPosition().toPoint())

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()

            self.move(new_x, new_y)
        
        event.accept()

class ImageWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width = 100, height = 100, parent = None ):
        super().__init__( parent )
        self._width = width
        self._height = height
        
        self.active = True
        self.visible = True
        self.static = False
        self.custom_name = None
        self.stack_order = 1
        
        self._x = 0
        self._y = 0
        
        self.frame_enabled = False
        self.frame_color = QColor( 0, 0, 0 )
        self.frame_width = 5
        
        self.background_color = QColor( 240, 240, 240 )
        
        self.image_path = ""
        self.original_pixmap = QPixmap()
        self.pixmap = QPixmap()
        
        self.selected = False
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        self.resize_start_pos = QPoint()
        self.resize_start_size = QSize()
        
        self.setFixedSize( self._width, self._height )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        painter.setBrush( self.background_color )
        painter.setPen( Qt.PenStyle.NoPen )
        painter.drawRect( 0, 0, self._width, self._height )
        
        if not self.pixmap.isNull():
            if self.frame_enabled:
                margin = self.frame_width  

            else:
                margin = 0
        
            x = margin
            y = margin
            
            painter.drawPixmap(x, y, self.pixmap)
        
        if self.frame_enabled and self.frame_width > 0:
            painter.setPen( QPen( self.frame_color, self.frame_width ) )
            painter.setBrush( Qt.BrushStyle.NoBrush )
            painter.drawRect( 0, 0, self._width, self._height )
        
        if self.selected:
            self.drawSelectionBorder( painter )
            self.drawSelectionHandles( painter )

    def drawSelectionHandles( self, painter ):
        if not self.selected:
            return
            
        handle_size = 8
        half_size = handle_size // 2

        painter.setBrush( QColor( 0, 255, 0 ) )
        painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )

        corners = [ QPoint( 4, 4 ), QPoint( self.width() - 4, 4 ), QPoint( 4, self.height() - 4 ), QPoint( self.width() - 4, self.height() - 4 ) ]

        for corner in corners:
            painter.drawEllipse( corner.x() - half_size, corner.y() - half_size, handle_size, handle_size )
            painter.setBrush( QColor( 255, 255, 255 ) )
            painter.setPen( Qt.PenStyle.NoPen )
            painter.drawEllipse( corner.x() - 1, corner.y() - 1, 2, 2 )
            painter.setBrush( QColor( 0, 255, 0 ) )
            painter.setPen( QPen( QColor( 0, 80, 200 ), 1 ) )
    
    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def handleResize( self, global_pos ):
        if not self.resize_corner:
            return

        delta = global_pos - self.resize_start_pos

        new_width = self.resize_start_size.width()
        new_height = self.resize_start_size.height()

        if self.resize_corner == "bottom_right":
            new_width = max( 20, self.resize_start_size.width() + delta.x() )
            new_height = max( 20, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_right":
            new_width = max( 20, self.resize_start_size.width() + delta.x() )
            new_height = max( 20, self.resize_start_size.height() - delta.y() )

        elif self.resize_corner == "bottom_left":
            new_width = max( 20, self.resize_start_size.width() - delta.x() )
            new_height = max( 20, self.resize_start_size.height() + delta.y() )

        elif self.resize_corner == "top_left":
            new_width = max( 20, self.resize_start_size.width() - delta.x() )
            new_height = max( 20, self.resize_start_size.height() - delta.y() )

        self._width = new_width
        self._height = new_height
        
        self.setFixedSize( new_width, new_height )
        
        if not self.original_pixmap.isNull():
            self.resizePixmap()
        
        self.updatePropertiesSize()

    def resizePixmap( self ):
        if self.original_pixmap.isNull():
            return
        
        if self.frame_enabled:
            margin = self.frame_width  

        else:
            margin = 0

        content_width = max( 1, self._width - 2 * margin )
        content_height = max( 1, self._height - 2 * margin )
        
        self.pixmap = self.original_pixmap.scaled( content_width, content_height, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation )

    def getImagePath( self ):
        return self.image_path

    def getCornerAt( self, pos ):
        handle_size = 12
        half_size = handle_size // 2
        
        corners = {
            "top_left": QPoint( 0, 0 ),
            "top_right": QPoint( self.width(), 0 ),
            "bottom_left": QPoint( 0, self.height() ),
            "bottom_right": QPoint( self.width(), self.height() )
        }
        
        for corner_name, corner_pos in corners.items():
            corner_rect = QRect( corner_pos.x() - half_size, corner_pos.y() - half_size, handle_size, handle_size )
            
            if corner_rect.contains( pos ):
                return corner_name
        
        return None

    def getScaleToFit( self ):
        return self.scale_to_fit

    def getWidth( self ):
        return self._width
    
    def getHeight( self ):
        return self._height

    def setSize( self, width, height ):
        self._width = max( 20, width )
        self._height = max( 20, height )
        self.setFixedSize( self._width, self._height )
        
        if not self.original_pixmap.isNull():
            self.resizePixmap()
        
        self.update()
    
    def setFrameEnabled( self, enabled ):
        self.frame_enabled = enabled
        self.resizePixmap()
        self.update()
    
    def setFrameColor( self, color ):
        self.frame_color = color
        self.update()
    
    def setFrameWidth( self, width ):
        self.frame_width = max( 0, min( 20, width ) )
        self.resizePixmap()
        self.update()
    
    def setBackgroundColor( self, color ):
        self.background_color = color
        self.update()
    
    def setImagePath( self, path ):
        supported_formats = ['.bmp', '.png', '.jpg', '.jpeg', '.jpe']
        
        if path:
            file_extension = path.lower()
            has_supported_extension = any( file_extension.endswith( ext ) for ext in supported_formats )
            
            if has_supported_extension:
                self.image_path = path
                self.original_pixmap = QPixmap( path )
                
                if self.original_pixmap.isNull():
                    self.original_pixmap = QPixmap()
                    self.pixmap = QPixmap()
                    return False
            
                self.resizePixmap()

                if not self.custom_name:
                    filename = os.path.basename( path )
                    self.custom_name = f"Image_{ os.path.splitext( filename )[ 0 ] }"
                
                self.update()
                return True

            else:
                return False
        
        return False
    
    def setScaleToFit( self, scale ):
        self.scale_to_fit = scale
        self.update()
    
    def setSelected( self, selected ):
        self.selected = selected
        self.update()
    
    def setVisibleImage( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def updatePropertiesSize( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if (hasattr( main_window, 'current_shape') and main_window.current_shape == self ):
            
            if hasattr( main_window, 'width_spin' ):
                main_window.width_spin.blockSignals( True )
                main_window.width_spin.setValue( self._width )
                main_window.width_spin.blockSignals( False )
                
            if hasattr(main_window, 'height_spin'):
                main_window.height_spin.blockSignals( True )
                main_window.height_spin.setValue( self._height )
                main_window.height_spin.blockSignals( False )
    
    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            if hasattr( main_window, 'pos_x_spin' ):
                main_window.pos_x_spin.blockSignals( True )
                main_window.pos_x_spin.setValue( self.x() )
                main_window.pos_x_spin.blockSignals( False )
                
            if hasattr( main_window, 'pos_y_spin' ):
                main_window.pos_y_spin.blockSignals( True )
                main_window.pos_y_spin.setValue( self.y() )
                main_window.pos_y_spin.blockSignals( False )
    
    def updateProperties( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
    
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            if hasattr( main_window, 'active_checkbox' ):
                main_window.active_checkbox.blockSignals( True )
                main_window.active_checkbox.setChecked( self.active )
                main_window.active_checkbox.blockSignals( False )
                
            if hasattr( main_window, 'visible_checkbox' ):
                main_window.visible_checkbox.blockSignals( True )
                main_window.visible_checkbox.setChecked( self.visible )
                main_window.visible_checkbox.blockSignals( False )
                
            if hasattr( main_window, 'static_checkbox' ):
                main_window.static_checkbox.blockSignals( True )
                main_window.static_checkbox.setChecked( self.static )
                main_window.static_checkbox.blockSignals( False )
            
            if hasattr( main_window, 'name_edit' ):
                main_window.name_edit.blockSignals( True )
                main_window.name_edit.setText( self.custom_name )
                main_window.name_edit.blockSignals( False )
            
            if hasattr( main_window, 'stack_order_spin' ):
                main_window.stack_order_spin.blockSignals( True )
                main_window.stack_order_spin.setValue( self.stack_order )
                main_window.stack_order_spin.blockSignals( False )
            
            if hasattr( main_window, 'frame_checkbox' ):
                main_window.frame_checkbox.blockSignals( True )
                main_window.frame_checkbox.setChecked( self.frame_enabled )
                main_window.frame_checkbox.blockSignals( False )
            
            if hasattr( main_window, 'frame_width_spin' ):
                main_window.frame_width_spin.blockSignals( True )
                main_window.frame_width_spin.setValue( self.frame_width )
                main_window.frame_width_spin.blockSignals( False ) 
            
            if hasattr(main_window, 'frame_color_rect'):
                main_window.frame_color_rect.setStyleSheet( f"background-color: { self.frame_color.name() }; border: 1px solid #ccc;" )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None
    
    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            self.resize_corner = self.getCornerAt( mouse_pos )

            if self.resize_corner:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.size()

            else:
                self.dragging = True
                self.drag_start_pos = mouse_pos
                self.clicked.emit(self)
                self.updateProperties()

        event.accept()
    
    def mouseMoveEvent( self, event ):
        mouse_pos = event.pos()
        corner = self.getCornerAt( mouse_pos )

        if corner:
            if corner in [ "top_left", "bottom_right" ]:
                self.setCursor( Qt.CursorShape.SizeFDiagCursor )

            elif corner in [ "top_right", "bottom_left" ]:
                self.setCursor( Qt.CursorShape.SizeBDiagCursor )

        else:
            self.setCursor( Qt.CursorShape.ArrowCursor )
        
        if self.resizing and event.buttons() & Qt.MouseButton.LeftButton:
            self.handleResize( event.globalPosition().toPoint() )
            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        elif self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            delta = mouse_pos - self.drag_start_pos

            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()

            super().move( new_x, new_y )
            
            self.updatePropertiesPosition()
        
        event.accept()
    
    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing = False
            self.dragging = False
            self.resize_corner = None

            self.updatePropertiesSize()
            self.updatePropertiesPosition()

        event.accept()

class LabelWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width, height, parent = None ):
        super().__init__( parent )

        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        
        self.text_color = QColor( 0, 0, 0 )            
        self.text = "Text"                    
        
        self.active = True
        self.visible = True
        self.static = False
        
        self.text_size = 20
        self.text_font = "Arial"
        self.text_alignment = "Left"
        
        self.selected = False
        self.selection_color = QColor( 255, 0, 0 )
        
        self.dragging = False
        self.drag_start_pos = QPoint()
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )
        
        self.custom_name = None
        self.stack_order = 1

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        painter.setPen( self.text_color )
        font = QFont( self.text_font, self.text_size )
        painter.setFont( font )
        text_rect = QRect( 0, 0, self._width, self._height )
        alignment_flags = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        
        if self.text_alignment == "Left":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

        elif self.text_alignment == "Center":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter 

        elif self.text_alignment == "Right":
            alignment_flags = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop

        elif self.text_alignment == "Top":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

        elif self.text_alignment == "Bottom":
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
            
        else:
            alignment_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

        painter.drawText( text_rect, alignment_flags, self.text )
        
        if self.selected:
            self.drawSelectionBorder( painter )

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def move( self, x, y ):
        super().move( x, y )
        
        main_window = self.findMainWindow()

        if main_window and hasattr( main_window, 'current_shape' ) and main_window.current_shape == self:
            try:
                if hasattr( main_window, 'pos_x_spin_label' ):
                    main_window.pos_x_spin_label.blockSignals( True )
                    main_window.pos_x_spin_label.setValue( x )
                    main_window.pos_x_spin_label.blockSignals( False )

            except RuntimeError:
                pass
            
            try:
                if hasattr( main_window, 'pos_y_spin_label' ):
                    main_window.pos_y_spin_label.blockSignals( True )
                    main_window.pos_y_spin_label.setValue( y )
                    main_window.pos_y_spin_label.blockSignals( False )

            except RuntimeError:
                pass

    def getWidth( self ):
        return self._width

    def getHeight( self ):
        return self._height

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setSizeBasedOnText( self ):
        painter = QPainter( self )
        font = QFont( self.text_font, self.text_size )
        font_metrics = QFontMetrics( font )
        
        text_width = font_metrics.horizontalAdvance( self.text ) + 20
        text_height = font_metrics.height() + 10
        
        self._width = max( 50, text_width )
        self._height = max( 30, text_height )
        self.setFixedSize( self._width, self._height )
        
        painter.end()
        self.update()

    def setTextColor( self, color ):
        self.text_color = color
        self.update()

    def setTextFont( self, text ):
        self.text = text
        self.setSizeBasedOnText()
        self.update()

    def setTextSize( self, size ):
        self.text_size = size
        self.setSizeBasedOnText()
        self.update()

    def setTextFont( self, font ):
        self.text_font = font
        self.setSizeBasedOnText()
        self.update()

    def setTextAlignment( self, alignment ):
        self.text_alignment = alignment
        self.update()

    def setActive( self, active ):
        self.active = active
        self.setEnabled( active )
        self.update()

    def setVisibleLabel( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def setStatic( self, static ):
        self.static = static
        self.update()

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent
            
            parent = parent.parent()

        return None
    
    def mouseMoveEvent( self, event ):
        if self.dragging and ( event.buttons() & Qt.MouseButton.LeftButton ):
            delta = event.pos() - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            
            self.move( new_x, new_y )
        
        event.accept()

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.pos()
            self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

        event.accept()

class NumericWidget( QWidget ):
    clicked = pyqtSignal( object )
    
    def __init__( self, width, height, parent = None ):
        super().__init__( parent)

        self._width = width
        self._height = height
        self.setFixedSize( width, height )
        
        self.active = True
        self.visible = True
        self.static = False
        
        self.number = 123
        self.number_color = QColor( 0, 0, 0 )
        self.number_size = 20
        self.number_alignment = "Left" 
        self.number_font = "Arial"
        
        self.selected = False
        
        self.dragging = False
        self.drag_start_pos = QPoint()
        
        self.custom_name = None
        self.stack_order = 1
        
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.FocusPolicy.StrongFocus )

        self.updateDisplayText()
        self.updateDisplaySize()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setRenderHint( QPainter.RenderHint.Antialiasing )
        
        painter.setPen( self.number_color )
        font = QFont( self.number_font, self.number_size )
        painter.setFont( font )
        
        text_rect = QRect( 0, 0, self._width, self._height )
        
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

        painter.drawText( text_rect, alignment_flags, self.display_text )
        
        if self.selected:
            self.drawSelectionBorder(painter)

    def drawSelectionBorder( self, painter ):
        if not self.selected:
            return
            
        margin = 2
        border_rect = QRect( margin, margin, self.width() - 2 * margin, self.height() - 2 * margin )

        selection_pen = QPen( QColor( 255, 0, 0 ) )
        selection_pen.setWidth( 3 )
        selection_pen.setStyle( Qt.PenStyle.DashLine )
        selection_pen.setDashPattern( [ 4, 2 ] )

        painter.setPen( selection_pen )
        painter.setBrush( Qt.BrushStyle.NoBrush )
        painter.drawRect( border_rect )

    def setSelected( self, selected ):
        self.selected = selected
        self.update()

    def setNumber( self, number ):
        self.number = number
        self.updateDisplayText()
        self.updateDisplaySize()
        self.update()

    def setNumberColor( self, color ):
        self.number_color = color
        self.update()

    def setNumberSize( self, size ):
        self.number_size = size
        self.updateDisplaySize()
        self.update()

    def setNumberAlignment( self, alignment ):
        self.number_alignment = alignment
        self.update()

    def setActive( self, active ):
        self.active = active
        self.setEnabled( active )
        self.update()

    def setVisibleNumeric( self, visible ):
        self.visible = visible
        self.setVisible( visible )
        self.update()

    def setStatic( self, static ):
        self.static = static
        self.update()

    def getWidth( self ):
        return self._width

    def getHeight( self ):
        return self._height

    def updateDisplayText( self ):
        self.display_text = str(self.number)

    def updateDisplaySize( self ):
        painter = QPainter(self)
        font = QFont(self.number_font, self.number_size)
        font_metrics = QFontMetrics( font )
        
        text_width = font_metrics.horizontalAdvance( self.display_text ) + 20 
        text_height = font_metrics.height() + 10
        
        self._width = max( 50, text_width )
        self._height = max( 30, text_height )
        self.setFixedSize( self._width, self._height )
        
        painter.end()

    def updatePropertiesPosition( self ):
        main_window = self.findMainWindow()

        if not main_window:
            return
        
        if ( hasattr( main_window, 'current_shape' ) and main_window.current_shape == self ):
            if hasattr( main_window, 'pos_x_spin_numeric' ):
                main_window.pos_x_spin_numeric.blockSignals( True )
                main_window.pos_x_spin_numeric.setValue( self.x() )
                main_window.pos_x_spin_numeric.blockSignals( False )

            elif hasattr( main_window, 'pos_x_spin' ):
                main_window.pos_x_spin.blockSignals( True )
                main_window.pos_x_spin.setValue( self.x() )
                main_window.pos_x_spin.blockSignals( False )
                
            if hasattr( main_window, 'pos_y_spin_numeric' ):
                main_window.pos_y_spin_numeric.blockSignals( True )
                main_window.pos_y_spin_numeric.setValue( self.y() )
                main_window.pos_y_spin_numeric.blockSignals( False )

            elif hasattr( main_window, 'pos_y_spin' ):
                main_window.pos_y_spin.blockSignals( True )
                main_window.pos_y_spin.setValue( self.y() )
                main_window.pos_y_spin.blockSignals( False )

    def findMainWindow( self ):
        parent = self.parent()

        while parent:
            if isinstance( parent, QMainWindow ):
                return parent

            parent = parent.parent()

        return None

    def mousePressEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.pos()
            self.clicked.emit( self )

        event.accept()

    def mouseReleaseEvent( self, event ):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.updatePropertiesPosition()

        event.accept()

    def mouseMoveEvent( self, event ):
        if self.dragging and ( event.buttons() & Qt.MouseButton.LeftButton ):
            delta = event.pos() - self.drag_start_pos
            
            new_x = self.x() + delta.x()
            new_y = self.y() + delta.y()
            super().move( new_x, new_y )
            
            self.updatePropertiesPosition()
        
        event.accept()