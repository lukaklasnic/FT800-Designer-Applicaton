from PyQt6.QtWidgets import ( QLabel, QHBoxLayout, QColorDialog, QCheckBox, QFileDialog, QPushButton, QDialog, QVBoxLayout )
from PyQt6.QtGui import ( QLinearGradient, QColor )
from PyQt6.QtCore import Qt
from widgets import*  

show_ellipse_warning = True

#------------------------------------------------------------LINE--------------------------------------------------------------

def updateLineTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        main_window.current_shape.tag = value

        if hasattr (main_window, 'all_line_dicts' ):
            main_window.all_line_dicts [main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateLineActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        active =  (state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = active

        if hasattr( main_window, 'all_line_dicts' ):
            main_window.all_line_dicts [main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateLineVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleLine( visible )

        if hasattr( main_window, 'all_line_dicts' ):
            main_window.all_line_dicts [main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateLineStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = static

        if hasattr( main_window, 'all_line_dicts' ):
            main_window.all_line_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateLineName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        main_window.current_shape.custom_name = text

        if hasattr( main_window, 'all_line_dicts' ):
            old_name = None

            for name, props in list(main_window.all_line_dicts.items()):
                if ( props.get( 'start_x' ) == main_window.current_shape.getLinePoints()[ 0 ] and props.get( 'start_y' ) == main_window.current_shape.getLinePoints()[ 1 ] ):
                    old_name = name

                    break
            
            if old_name and old_name != text:
                main_window.all_line_dicts[ text ] = main_window.all_line_dicts.pop( old_name )

            else:
                main_window.all_line_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateLineStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_line_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateLinePoints (main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        if ( hasattr( main_window, 'start_x_spin_line' ) and hasattr( main_window, 'start_y_spin_line' ) and hasattr( main_window, 'end_x_spin_line' ) and hasattr( main_window, 'end_y_spin_line' ) ):
            start_x = main_window.start_x_spin_line.value()
            start_y = main_window.start_y_spin_line.value()
            end_x = main_window.end_x_spin_line.value()
            end_y = main_window.end_y_spin_line.value()
            main_window.current_shape.setLinePoints( start_x, start_y, end_x, end_y )
            
            if hasattr( main_window, 'all_line_dicts' ):
                main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()


def changeLineColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        color = QColorDialog.getColor( main_window.current_shape.line_color )

        if color.isValid():
            main_window.current_shape.setLineColor( color )
            main_window.color_rect_line.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr(main_window, 'all_line_dicts'):
                main_window.all_line_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateLineEdgesWidth( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, LineWidget ):
        main_window.current_shape.setLineWidth( value )
        if hasattr( main_window, 'all_line_dicts' ):
            main_window.all_line_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------RECTANGLE--------------------------------------------------------------

def updateRectangleTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.setActive( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleVisible(main_window, state):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.setVisibleRectangle( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.setStatic(state == Qt.CheckState.Checked.value)

        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.setCustomName( text )
        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateRectanglePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        if hasattr( main_window, 'pos_x_spin_rect' ) and hasattr( main_window, 'pos_y_spin_rect' ):
            main_window.current_shape.move( main_window.pos_x_spin_rect.value(), main_window.pos_y_spin_rect.value() )

            if hasattr( main_window, 'all_rectangle_dicts' ):
                main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        if hasattr( main_window, 'width_spin_rect' ) and hasattr( main_window, 'height_spin_rect' ):
            main_window.current_shape.setFixedSize( main_window.width_spin_rect.value(), main_window.height_spin_rect.value() )

            if hasattr( main_window, 'all_rectangle_dicts' ):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def changeRectangleEdgesColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        current_color = main_window.current_shape.color
        color = QColorDialog.getColor( current_color )

        if color.isValid():
            main_window.current_shape.setColor( color )
            main_window.edges_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_rectangle_dicts' ):
                main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleEdgesWidth(main_window, value):
    """Ažurira debljinu ivice rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.setBorderWidth(value)
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateRectangleGradientAppearance( main_window ):
    if not hasattr( main_window, 'current_shape' ) or not main_window.current_shape:
        return
    
    if hasattr( main_window, 'start_color_rect_rect' ):
        main_window.start_color_rect_rect.setStyleSheet( f"background-color: { main_window.current_shape.gradient_color1.name() }; "f"border: 2px solid #666;" )
    
    if hasattr( main_window, 'end_color_rect_rect' ):
        main_window.end_color_rect_rect.setStyleSheet( f"background-color: { main_window.current_shape.gradient_color2.name() }; "f"border: 2px solid #666;" )

def updateRectangleProperties( main_window ):
    if not main_window.current_shape:
        return
    
    if hasattr( main_window, 'active_checkbox_rect' ):
        main_window.active_checkbox_rect.blockSignals( True )
        main_window.active_checkbox_rect.setChecked( main_window.current_shape.active )
        main_window.active_checkbox_rect.blockSignals( False )
    
    if hasattr( main_window, 'visible_checkbox_rect' ):
        main_window.visible_checkbox_rect.blockSignals( True )
        main_window.visible_checkbox_rect.setChecked( main_window.current_shape.visible )
        main_window.visible_checkbox_rect.blockSignals( False )
    
    if hasattr( main_window, 'static_checkbox_rect' ):
        main_window.static_checkbox_rect.blockSignals( True )
        main_window.static_checkbox_rect.setChecked( main_window.current_shape.static )
        main_window.static_checkbox_rect.blockSignals( False )
    
    if hasattr( main_window, 'name_edit_rect' ):
        main_window.name_edit_rect.blockSignals( True )
        main_window.name_edit_rect.setText( main_window.current_shape.custom_name )
        main_window.name_edit_rect.blockSignals( False )
    
    if hasattr( main_window, 'stack_order_spin_rect' ):
        main_window.stack_order_spin_rect.blockSignals( True )
        main_window.stack_order_spin_rect.setValue( main_window.current_shape.stack_order )
        main_window.stack_order_spin_rect.blockSignals( False )
    
    if hasattr( main_window, 'pos_x_spin_rect' ):
        main_window.pos_x_spin_rect.blockSignals( True )
        main_window.pos_x_spin_rect.setValue( main_window.current_shape.x() )
        main_window.pos_x_spin_rect.blockSignals( False )
    
    if hasattr( main_window, 'pos_y_spin_rect' ):
        main_window.pos_y_spin_rect.blockSignals( True )
        main_window.pos_y_spin_rect.setValue( main_window.current_shape.y() )
        main_window.pos_y_spin_rect.blockSignals( False )
    
    if hasattr( main_window, 'width_spin_rect' ):
        main_window.width_spin_rect.blockSignals( True )
        main_window.width_spin_rect.setValue( main_window.current_shape.width() )
        main_window.width_spin_rect.blockSignals( False )
    
    if hasattr( main_window, 'height_spin_rect' ):
        main_window.height_spin_rect.blockSignals( True )
        main_window.height_spin_rect.setValue( main_window.current_shape.height() )
        main_window.height_spin_rect.blockSignals( False )
    
    if hasattr( main_window, 'edges_color_rect_rect' ):
        main_window.edges_color_rect_rect.setStyleSheet( f"background-color: { main_window.current_shape.color.name() }; border: 1px solid #ccc;" )
    
    if hasattr( main_window, 'thickness_spin_rect' ):
        main_window.thickness_spin_rect.blockSignals( True )
        main_window.thickness_spin_rect.setValue( main_window.current_shape.border_width )
        main_window.thickness_spin_rect.blockSignals( False )
    
    if hasattr( main_window, 'filled_checkbox_rect' ):
        main_window.filled_checkbox_rect.blockSignals( True )
        main_window.filled_checkbox_rect.setChecked( main_window.current_shape.filled )
        main_window.filled_checkbox_rect.blockSignals( False )
    
    if hasattr( main_window, 'gradient_combo_rect' ):
        main_window.gradient_combo_rect.blockSignals( True )

        direction_mapping = {
            "top_to_bottom": "Top to Bottom",
            "bottom_to_top": "Bottom to Top",
            "left_to_right": "Left to Right",
            "right_to_left": "Right to Left"
        }

        current_direction = direction_mapping.get( main_window.current_shape.gradient_direction, "Top to Bottom" )
        main_window.gradient_combo_rect.setCurrentText( current_direction )
        main_window.gradient_combo_rect.blockSignals( False )
    
    if hasattr( main_window, 'start_color_rect_rect' ):
        main_window.start_color_rect_rect.setStyleSheet( f"background-color: { main_window.current_shape.gradient_color1.name() }; border: 1px solid #ccc;" )
    
    if hasattr( main_window, 'end_color_rect_rect' ):
        main_window.end_color_rect_rect.setStyleSheet( f"background-color: { main_window.current_shape.gradient_color2.name() }; border: 1px solid #ccc;" )

def updateRectangleGradientDirection( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        text_to_direction = {
            "Top to Bottom": "top_to_bottom",
            "Bottom to Top": "bottom_to_top",
            "Left to Right": "left_to_right",
            "Right to Left": "right_to_left"
        }
        
        direction = text_to_direction.get( text, "top_to_bottom" )
        main_window.current_shape.gradient_direction = direction
        main_window.current_shape.update()

        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeRectangleGradientStartColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        color = QColorDialog.getColor( main_window.current_shape.gradient_color1 )
        if color.isValid():
            main_window.current_shape.gradient_color1 = color
            main_window.current_shape.update()
            
            if hasattr( main_window, 'start_color_rect_rect' ):
                main_window.start_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; "f"border: 2px solid #666;" )
            
            if hasattr( main_window, 'all_rectangle_dicts' ):
                main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeRectangleGradientEndColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        color = QColorDialog.getColor( main_window.current_shape.gradient_color2 )

        if color.isValid():
            main_window.current_shape.gradient_color2 = color
            main_window.current_shape.update()
            
            if hasattr(main_window, 'end_color_rect_rect'):
                main_window.end_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; "f"border: 2px solid #666;" )
            
            if hasattr( main_window, 'all_rectangle_dicts' ):
                main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateRectangleFilled( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        filled = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.filled = filled
        main_window.current_shape.update()
        
        if hasattr( main_window, 'all_rectangle_dicts' ):
            main_window.all_rectangle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------CIRCLE--------------------------------------------------------------

def updateCircleTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.tag = value
        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.setActive( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.setVisibleCircle( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.setStatic( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.setCustomName( text )

        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateCirclePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        if hasattr( main_window, 'pos_x_spin_circle' ) and hasattr( main_window, 'pos_y_spin_circle' ):
            center_x = main_window.pos_x_spin_circle.value()
            center_y = main_window.pos_y_spin_circle.value()
            
            x = center_x - main_window.current_shape.diameter // 2
            y = center_y - main_window.current_shape.diameter // 2
            
            main_window.current_shape.move( x, y )
            main_window.current_shape.updateCenterPosition()
            
            if hasattr( main_window, 'all_circle_dicts' ):
                main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        if hasattr( main_window, 'diameter_spin_circle' ):
            diameter = main_window.diameter_spin_circle.value()
            main_window.current_shape.setDiameter( diameter )
            
            if hasattr( main_window, 'pos_x_spin_circle' ) and hasattr( main_window, 'pos_y_spin_circle' ):
                main_window.pos_x_spin_circle.blockSignals( True )
                main_window.pos_y_spin_circle.blockSignals( True )
                main_window.pos_x_spin_circle.setValue( main_window.current_shape.center_x )
                main_window.pos_y_spin_circle.setValue( main_window.current_shape.center_y )
                main_window.pos_x_spin_circle.blockSignals( False )
                main_window.pos_y_spin_circle.blockSignals( False )
            
            if hasattr( main_window, 'all_circle_dicts' ):
                main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeCircleLineColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        current_color = main_window.current_shape.line_color
        color = QColorDialog.getColor( current_color )

        if color.isValid():
            main_window.current_shape.setColor( color )
            main_window.edges_color_rect_circle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_circle_dicts' ):
                main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleEdgeWidth( main_window, value ):

    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        main_window.current_shape.setLineEdgeWidth( value )

        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleFilled( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, CircleWidget ):
        filled = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setFilled( filled )
        
        if hasattr( main_window, 'all_circle_dicts' ):
            main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateCircleFillColorAppearance( main_window ):
    if not hasattr( main_window, 'current_shape' ) or not main_window.current_shape:
        return
    
    if hasattr( main_window, 'fill_color_rect_circle' ):
        main_window.fill_color_rect_circle.setStyleSheet( f"background-color: { main_window.current_shape.fill_color.name() }; "f"border: 1px solid #ccc;" )
        main_window.fill_color_rect_circle.setCursor(Qt.CursorShape.PointingHandCursor)

def changeCircleFillColor( main_window ):
    current_color = main_window.current_shape.fill_color
    color = QColorDialog.getColor( current_color )

    if not main_window.current_shape:
        return
    
    if hasattr (main_window, 'filled_checkbox_circle' ):
        if not main_window.filled_checkbox_circle.isChecked():
            return
    
    if isinstance( main_window.current_shape, CircleWidget ):
        if color.isValid():
            main_window.current_shape.setFillColor( color )
            
            if hasattr(main_window, 'fill_color_rect_circle'):
                main_window.fill_color_rect_circle.setStyleSheet( f"background-color: { color.name() }; "f"border: 1px solid #ccc;" )
            
            if hasattr( main_window, 'all_circle_dicts' ):
                main_window.all_circle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------ELLIPSE--------------------------------------------------------------

def updateEllipseTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_ellipse_dicts' ):
            main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def showFilledWarning( main_window, state ):
    global show_ellipse_warning
    is_filled = ( state == Qt.CheckState.Checked.value )
    
    if is_filled and show_ellipse_warning:
        warning_dialog = QDialog( main_window )
        warning_dialog.setWindowTitle( "Information" )
        warning_dialog.setFixedSize( 400, 200 )
        layout = QVBoxLayout( warning_dialog )
        info_label = QLabel( "This option is resource intensive and may cause unpredictable display behavior." )
        info_label.setWordWrap( True )
        info_label.setStyleSheet( "color: white; font-size: 12px; padding: 10px;" )
        layout.addWidget( info_label )
        
        dont_show_layout = QHBoxLayout()
        dont_show_checkbox = QCheckBox( "Do not show again" )
        dont_show_checkbox.setStyleSheet( "color: white;" )
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
            show_ellipse_warning = False

    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        main_window.current_shape.setFillEnabled( is_filled )
    
    if hasattr( main_window, 'gradient_combo_ellipse' ):
        main_window.gradient_combo_ellipse.setEnabled( is_filled )
    
    if hasattr( main_window, 'start_color_rect_ellipse' ):
        main_window.start_color_rect_ellipse.setEnabled( is_filled )
    
    if hasattr( main_window, 'end_color_rect_ellipse' ):
        main_window.end_color_rect_ellipse.setEnabled( is_filled )

    if hasattr( main_window, 'all_ellipse_dicts' ):
        main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

    main_window.current_shape.update()

def updateEllipseActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        is_active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = is_active

        if hasattr( main_window, 'all_ellipse_dicts' ):
            main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateEllipseVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleEllipse( is_visible )

        if hasattr( main_window, 'all_ellipse_dicts' ):
            main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateEllipseStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = is_static

        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateEllipseName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        main_window.current_shape.custom_name = text

        if hasattr( main_window, 'all_ellipse_dicts' ):
            old_name = main_window.current_shape.custom_name
            main_window.all_ellipse_dicts[ old_name ] = main_window.current_shape.getPropertiesDict()

def updateEllipseStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateEllipsePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        if hasattr( main_window, 'pos_x_spin_ellipse' ) and hasattr( main_window, 'pos_y_spin_ellipse' ):
            main_window.current_shape.move( main_window.pos_x_spin_ellipse.value(), main_window.pos_y_spin_ellipse.value() )

            if hasattr( main_window, 'all_ellipse_dicts' ):
                main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateEllipseSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):

        if hasattr( main_window, 'width_spin_ellipse' ) and hasattr( main_window, 'height_spin_ellipse' ):
            width = main_window.width_spin_ellipse.value()
            height = main_window.height_spin_ellipse.value()
            main_window.current_shape.setSize( width, height )
            
            if hasattr( main_window, 'all_ellipse_dicts' ):
                main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeEllipseEdgesColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        color = QColorDialog.getColor( main_window.current_shape.border_color )

        if color.isValid():
            main_window.current_shape.setBorderColor( color )
            main_window.edges_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_ellipse_dicts' ):
                main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateEllipseEdgeWidth( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        main_window.current_shape.setBorderWidth( value )

        if hasattr( main_window, 'all_ellipse_dicts' ):
            main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()


def updateEllipseGradientType( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        main_window.current_shape.setGradientType( text )

        if hasattr( main_window, 'all_ellipse_dicts' ):
            main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeEllipseStartColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )

        if color.isValid():
            main_window.current_shape.setGradientColors( color, main_window.current_shape.gradient_end_color )
            main_window.start_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_ellipse_dicts' ):
                main_window.all_ellipse_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeEllipseEndColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, EllipseWidget ):
        color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

        if color.isValid():
            main_window.current_shape.setGradientColors( main_window.current_shape.gradient_start_color, color )
            main_window.end_color_rect_ellipse.setStyleSheet( f"background-color: {color.name()}; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_ellipse_dicts' ):
                main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------BUTTON--------------------------------------------------------------

def updateButtonTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateButtonStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateButtonPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        if hasattr( main_window, 'pos_x_spin' ) and hasattr( main_window, 'pos_y_spin' ):
            main_window.current_shape.move( main_window.pos_x_spin.value(), main_window.pos_y_spin.value() )
            main_window.current_shape.updatePropertiesDict()
            
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()


def updateButtonGradient( main_window ):
    if hasattr( main_window.current_shape, 'start_color' ) and hasattr( main_window.current_shape, 'end_color' ):
        gradient = QLinearGradient( 0, 0, 0, main_window.current_shape.height() )
        gradient.setColorAt( 0, main_window.current_shape.start_color )
        gradient.setColorAt( 1, main_window.current_shape.end_color )
        main_window.current_shape.setBackgroundGradient( gradient )
        main_window.current_shape.update()
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeStartColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        if hasattr( main_window.current_shape, 'start_color' ):
            current_color = main_window.current_shape.start_color 
            color = QColorDialog.getColor( current_color )
        
        else:
            color = QColor( "#0000FF" )

        if color.isValid():
            main_window.current_shape.start_color = color
            main_window.start_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
            updateButtonGradient( main_window )
            main_window.current_shape.updatePropertiesDict()
        
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeEndColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        if hasattr( main_window.current_shape, 'end_color'):
            current_color = main_window.current_shape.end_color  
            color = QColorDialog.getColor( current_color )

        else: 
            color = QColor( "#000088" )

        if color.isValid():
            main_window.current_shape.end_color = color
            main_window.end_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
            updateButtonGradient( main_window )
            main_window.current_shape.updatePropertiesDict()
        
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateButtonName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.custom_name = text
        if hasattr( main_window, 'all_button_dicts' ):
            for shape in main_window.all_shapes:
                if shape == main_window.current_shape and hasattr( shape, 'custom_name' ):
                    shape.updatePropertiesDict()
                    main_window.all_button_dicts[ text ] = shape.getPropertiesDict()

def updateStackOrder( main_window, value ):
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
    

def updateButtonText( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.setButtonText( text )
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateButtonTextSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.setTextSize( value )
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeButtonTextColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        color = QColorDialog.getColor( main_window.current_shape.text_color )

        if color.isValid():
            main_window.current_shape.setTextColor( color )
            main_window.text_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
            main_window.current_shape.updatePropertiesDict()
        
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------KEYS--------------------------------------------------------------

def updateKeysFontSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.setFontSize( value )

        if hasattr( main_window, 'all_keys_dicts' ):
            main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeKeysStartColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        color = QColorDialog.getColor( main_window.current_shape.key_color_top )

        if color.isValid():
            main_window.current_shape.setKeyColors( color, main_window.current_shape.key_color_bottom )
            main_window.start_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_keys_dicts' ):
                main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def changeKeysEndColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        color = QColorDialog.getColor( main_window.current_shape.key_color_bottom )

        if color.isValid():
            main_window.current_shape.setKeyColors( main_window.current_shape.key_color_top, color )
            main_window.end_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_keys_dicts' ):
                main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeKeysFontColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        color = QColorDialog.getColor( main_window.current_shape.text_color )

        if color.isValid():
            main_window.current_shape.setTextColor( color )
            main_window.font_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_keys_dicts' ):
                main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeys3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        is_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( is_3d )

        if hasattr( main_window, 'all_keys_dicts' ):
            main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeysActive( main_window, state ):
    """Ažurira active status za keys"""
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = active

        if hasattr( main_window, 'all_keys_dicts' ):
            main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeysVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleKeys( visible )

        if hasattr( main_window, 'all_keys_dicts' ):
            main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeysStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = static

        if hasattr( main_window, 'all_keys_dicts' ):
            main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeysName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.custom_name = text

        if hasattr( main_window, 'all_keys_dicts' ):
            old_name = None

            for name, props in list( main_window.all_keys_dicts.items() ):
                if props.get('position') == ( main_window.current_shape.x(), main_window.current_shape.y() ):
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_keys_dicts[ text ] = main_window.all_keys_dicts.pop( old_name )

            else:
                main_window.all_keys_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateKeysStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.stack_order = value

        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts [main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateKeysPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        if hasattr( main_window, 'pos_x_spin_keys' ) and hasattr( main_window, 'pos_y_spin_keys' ):
            main_window.current_shape.move( main_window.pos_x_spin_keys.value(), main_window.pos_y_spin_keys.value() )

            if hasattr( main_window, 'all_keys_dicts' ):
                main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeysSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        if hasattr( main_window, 'width_spin_keys' ) and hasattr( main_window, 'height_spin_keys' ):
            width = main_window.width_spin_keys.value()
            height = main_window.height_spin_keys.value()
            main_window.current_shape.setSize(width, height)
            
            if hasattr( main_window, 'all_keys_dicts' ):
                main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateKeysType( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.set_key_type( text )

        if hasattr( main_window, 'all_keys_dicts' ):
            main_window.all_keys_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------CLOCK--------------------------------------------------------------

def updateClockPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        if hasattr( main_window, 'pos_x_spin_clock' ) and hasattr( main_window, 'pos_y_spin_clock' ):
            main_window.current_shape.move( main_window.pos_x_spin_clock.value(), main_window.pos_y_spin_clock.value() )

def updateClockActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setActive( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setVisibleClock( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setStatic( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setCustomName( text )

        if hasattr( main_window, 'all_clock_dicts' ):
            old_name = None

            for name, props in list( main_window.all_clock_dicts.items() ):
                if props.get('x') == main_window.current_shape.x() and props.get('y') == main_window.current_shape.y():
                    old_name = name

                    break
            
            if old_name and old_name != text:
                main_window.all_clock_dicts[ text ] = main_window.all_clock_dicts.pop( old_name )
            else:

                main_window.all_clock_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateClockStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateClockPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        if hasattr( main_window, 'pos_x_spin_clock' ) and hasattr( main_window, 'pos_y_spin_clock' ):
            main_window.current_shape.move( main_window.pos_x_spin_clock.value(), main_window.pos_y_spin_clock.value() )

            if hasattr( main_window, 'all_clock_dicts' ):
                main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockDiameter( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setDiameter( value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeClockBackgroundColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        current_color = main_window.current_shape.background_color
        color = QColorDialog.getColor( current_color )

        if color.isValid():
            main_window.current_shape.setBackgroundColor( color )
            main_window.bg_color_rect_clock.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_clock_dicts' ):
                main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClock3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( use_3d )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockHours( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setHours( value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockMinutes( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setMinutes( value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockSeconds( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        main_window.current_shape.setSeconds( value )

        if hasattr( main_window, 'all_clock_dicts' ):
            main_window.all_clock_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateClockSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ClockWidget ):
        if hasattr( main_window, 'diameter_spin_clock' ):
            main_window.current_shape.setDiameter( main_window.diameter_spin_clock.value() )

#------------------------------------------------------------GAUGE--------------------------------------------------------------

def updateGaugeActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setActive( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setVisibleGauge( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setStatic( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setCustomName( text )

        if hasattr( main_window, 'all_gauge_dicts' ):
            old_name = None

            for name, props in list( main_window.all_gauge_dicts.items() ):
                if props.get( 'x' ) == main_window.current_shape.x() and props.get( 'y' ) == main_window.current_shape.y():
                    old_name = name

                    break
            
            if old_name and old_name != text:
                main_window.all_gauge_dicts[ text ] = main_window.all_gauge_dicts.pop( old_name )
            else:
                main_window.all_gauge_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateGaugeStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sort_widgets_by_stack_order()

def updateGaugePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        if hasattr( main_window, 'pos_x_spin_gauge' ) and hasattr( main_window, 'pos_y_spin_gauge '):
            main_window.current_shape.move( main_window.pos_x_spin_gauge.value(), main_window.pos_y_spin_gauge.value() )

            if hasattr( main_window, 'all_gauge_dicts' ):
                main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeDiameter( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setDiameter( value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeGaugeBackgroundColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        current_color = main_window.current_shape.background_color
        color = QColorDialog.getColor( current_color )

        if color.isValid():
            main_window.current_shape.setBackgroundColor( color )
            main_window.bg_color_rect_gauge.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_gauge_dicts' ):
                main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGauge3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( use_3d )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeMajorSubdivision( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setMajorSubdivision( value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeMinorSubdivision( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setMinorSubdivision( value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeRangeValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setRangeValue( value )

        if hasattr( main_window, 'value_spin_gauge' ):
            main_window.value_spin_gauge.setRange( 0, value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        main_window.current_shape.setValue( value )

        if hasattr( main_window, 'all_gauge_dicts' ):
            main_window.all_gauge_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateGaugeSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, GaugeWidget ):
        if hasattr( main_window, 'diameter_spin_gauge' ):
            main_window.current_shape.setDiameter( main_window.diameter_spin_gauge.value() )

#------------------------------------------------------------DIAL--------------------------------------------------------------

def update_dial_tag(main_window, value):
    """Ažurira tag vrednost za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_active(main_window, state):
    """Ažurira active status za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.setActive(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_visible(main_window, state):
    """Ažurira visible status za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.setVisibleDial(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_static(main_window, state):
    """Ažurira static status za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.setStatic(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_name(main_window, text):
    """Ažurira ime dial-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.setCustomName(text)
        if hasattr(main_window, 'all_dial_dicts'):
            # Ažuriraj ključ u rečniku ako se promenilo ime
            old_name = None
            for name, props in list(main_window.all_dial_dicts.items()):
                if props.get('diameter') == main_window.current_shape.diameter:
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_dial_dicts[text] = main_window.all_dial_dicts.pop(old_name)
            else:
                main_window.all_dial_dicts[text] = main_window.current_shape.getPropertiesDict()

def update_dial_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def update_dial_position(main_window):
    """Ažurira poziciju dial-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        if hasattr(main_window, 'pos_x_spin_dial') and hasattr(main_window, 'pos_y_spin_dial'):
            main_window.current_shape.move(main_window.pos_x_spin_dial.value(), main_window.pos_y_spin_dial.value())
            if hasattr(main_window, 'all_dial_dicts'):
                main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_diameter(main_window, value):
    """Ažurira dijametar dial-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.setDiameter(value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_3d(main_window, state):
    """Ažurira 3D efekat za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set3d(use_3d)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_dial_value(main_window, value):
    """Ažurira trenutnu vrednost za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.setValue(value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateDialSize(self):
    """Ažurira veličinu DialWidget-a (zastarelo, za kompatibilnost)"""
    if self.current_shape and isinstance(self.current_shape, DialWidget):
        if hasattr(self, 'width_spin'):
            diameter = self.width_spin.value()
            self.current_shape.setDiameter(diameter)
            self.current_shape.updatePropertiesDict()

#------------------------------------------------------------TOGGLE--------------------------------------------------------------

def update_toggle_tag(main_window, value):
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateTogglePosition(main_window):
    """Ažurira poziciju toggle-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        if hasattr(main_window, 'pos_x_spin_toggle') and hasattr(main_window, 'pos_y_spin_toggle'):
            main_window.current_shape.move(
                main_window.pos_x_spin_toggle.value(), 
                main_window.pos_y_spin_toggle.value()
            )
            # Ažuriraj rečnik
            main_window.current_shape.updatePropertiesDict()

# Ostatak callback funkcija za toggle ostaje isti...

def updateToggleActive(main_window, state):
    """Ažurira active status za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setActive(active)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateToggleVisible(main_window, state):
    """Ažurira visible status za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setVisibleToggle(visible)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateToggleStatic(main_window, state):
    """Ažurira static status za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setStatic(static)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateToggleName(main_window, text):
    """Ažurira ime toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        if text and text != main_window.current_shape.custom_name:
            # Ažuriraj rečnike ako postoji staro ime
            if hasattr(main_window, 'all_toggle_dicts') and main_window.current_shape.custom_name in main_window.all_toggle_dicts:
                old_dict = main_window.all_toggle_dicts.pop(main_window.current_shape.custom_name)
                old_dict['name'] = text
                main_window.all_toggle_dicts[text] = old_dict
            
            main_window.current_shape.custom_name = text
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[text] = main_window.current_shape.getPropertiesDict()

def update_toggle_stack_order(main_window, value):
    """Ažurira stack order za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def changeToggleKnobColor(main_window):
    """Menja boju knob-a toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        color = QColorDialog.getColor(main_window.current_shape.thumb_color)
        if color.isValid():
            main_window.current_shape.setThumbColor(color)
            if hasattr(main_window, 'knob_color_rect_toggle'):
                main_window.knob_color_rect_toggle.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def changeToggleBackgroundColor(main_window):
    """Menja boju pozadine toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        color = QColorDialog.getColor(main_window.current_shape.background_color)
        if color.isValid():
            main_window.current_shape.setBackgroundColor(color)
            if hasattr(main_window, 'bg_color_rect_toggle'):
                main_window.bg_color_rect_toggle.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateToggle3D(main_window, state):
    """Ažurira 3D svojstvo toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        _3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set3d(_3d)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateToggleState(main_window, state):
    """Ažurira stanje toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        is_on = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setState(is_on)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def toggle3dEffect( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.update()
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateTogglePosition(main_window):
    """Ažurira poziciju toggle-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        if hasattr(main_window, 'pos_x_spin_toggle') and hasattr(main_window, 'pos_y_spin_toggle'):
            main_window.current_shape.move(
                main_window.pos_x_spin_toggle.value(), 
                main_window.pos_y_spin_toggle.value()
            )
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateToggleSize(main_window, value):
    """Ažurira veličinu toggle-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        # ToggleWidget ima fiksnu visinu od 30
        main_window.current_shape.setSize(value, 30)

#------------------------------------------------------------SCROLL BAR--------------------------------------------------------------

def update_scrollbar_tag(main_window, value):
    """Ažurira tag vrednost za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_scrollbar_dicts'):
            main_window.all_scrollbar_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_scrollbar_active(main_window, state):
    """Ažurira active status za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = active
        main_window.current_shape.update()

def update_scrollbar_visible(main_window, state):
    """Ažurira visible status za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setVisibleScrollBar(visible)

def update_scrollbar_static(main_window, state):
    """Ažurira static status za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = static

def update_scrollbar_name(main_window, text):
    """Ažurira ime scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.custom_name = text

def update_scroll_bar_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def update_scrollbar_position(main_window):
    """Ažurira poziciju scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        if hasattr(main_window, 'pos_x_spin_scrollbar') and hasattr(main_window, 'pos_y_spin_scrollbar'):
            main_window.current_shape.move(
                main_window.pos_x_spin_scrollbar.value(), 
                main_window.pos_y_spin_scrollbar.value()
            )

def update_scrollbar_size(main_window):
    """Ažurira veličinu scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        if hasattr(main_window, 'width_spin_scrollbar') and hasattr(main_window, 'height_spin_scrollbar'):
            main_window.current_shape.setSize(
                main_window.width_spin_scrollbar.value(), 
                main_window.height_spin_scrollbar.value()
            )

def change_scrollbar_thumb_color(main_window):
    """Menja boju thumb-a scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.thumb_color)
        if color.isValid():
            main_window.current_shape.setThumbColor(color)
            main_window.thumb_color_rect_scrollbar.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")

def change_scrollbar_track_color(main_window):
    """Menja boju track-a scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.track_color)
        if color.isValid():
            main_window.current_shape.setTrackColor(color)
            main_window.track_color_rect_scrollbar.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")

def update_scrollbar_3d(main_window, state):
    """Ažurira 3D efekat za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set3d(use_3d)

def update_scrollbar_range(main_window, value):
    """Ažurira range za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.setRange(value)
        # Ažuriraj max vrednost za current_value spin
        if hasattr(main_window, 'current_value_spin_scrollbar'):
            main_window.current_value_spin_scrollbar.setRange(0, value)

def update_scrollbar_current_value(main_window, value):
    """Ažurira trenutnu vrednost za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.setCurrentValue(value)

def update_scrollbar_knob_size(main_window, value):
    """Ažurira veličinu thumb-a za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.setKnobSize(value)

#------------------------------------------------------------SLIDER--------------------------------------------------------------

def update_slider_tag(main_window, value):
    """Ažurira tag vrednost za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def change_slider_background_left_color(main_window):
    """Menja boju pozadine sa leve strane (progress deo) slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        color = QColorDialog.getColor(main_window.current_shape.thumb_color)
        if color.isValid():
            main_window.current_shape.setThumbColor(color)
            main_window.bg_left_color_rect_slider.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def change_slider_background_right_color(main_window):
    """Menja boju pozadine sa desne strane (track) slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        color = QColorDialog.getColor(main_window.current_shape.track_color)
        if color.isValid():
            main_window.current_shape.setTrackColor(color)
            main_window.bg_right_color_rect_slider.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_slider_active(main_window, state):
    """Ažurira active status za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = active
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_slider_visible(main_window, state):
    """Ažurira visible status za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setVisibleSlider(visible)
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_slider_static(main_window, state):
    """Ažurira static status za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = static
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_slider_name(main_window, text):
    """Ažurira ime slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.custom_name = text
        if hasattr(main_window, 'all_slider_dicts'):
            # Ažuriraj ključ u rečniku ako se promenilo ime
            old_name = None
            for name, props in list(main_window.all_slider_dicts.items()):
                if props.get('x') == main_window.current_shape.x() and props.get('y') == main_window.current_shape.y():
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_slider_dicts[text] = main_window.all_slider_dicts.pop(old_name)
            else:
                main_window.all_slider_dicts[text] = main_window.current_shape.getPropertiesDict()

def update_slider_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def update_slider_position(main_window):
    """Ažurira poziciju slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        if hasattr(main_window, 'pos_x_spin_slider') and hasattr(main_window, 'pos_y_spin_slider'):
            main_window.current_shape.move(main_window.pos_x_spin_slider.value(), main_window.pos_y_spin_slider.value())
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_slider_size(main_window, value):
    """Ažurira veličinu slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        if hasattr(main_window, 'width_spin_slider') and hasattr(main_window, 'height_spin_slider'):
            main_window.current_shape.setSize(main_window.width_spin_slider.value(), main_window.height_spin_slider.value())
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def change_slider_knob_color(main_window):
    """Menja boju knob-a (plavi krug) slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        color = QColorDialog.getColor(main_window.current_shape.progress_color)
        if color.isValid():
            main_window.current_shape.setProgressColor(color)
            main_window.knob_color_rect_slider.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()


def update_slider_3d(main_window, state):
    """Ažurira 3D efekat za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set3d(use_3d)  # Koristi setter metodu
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_slider_value(main_window, value):
    """Ažurira trenutnu vrednost za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.setValue(value)
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------PROGRESS BAR--------------------------------------------------------------

def updateProgressBarActive(main_window, state):
    """Ažurira active status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setActive(active)
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarVisible(main_window, state):
    """Ažurira visible status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setVisibleProgressBar(visible)
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarStatic(main_window, state):
    """Ažurira static status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setStatic(static)
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarThreeD(main_window, state):
    """Ažurira 3D status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        _3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set3d(_3d)
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarName(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        main_window.current_shape.custom_name = main_window.progress_name_edit.text()
        main_window.current_shape.updatePropertiesDict()

def update_progress_bar_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def updateProgressBarPosition(main_window):
    """Ažurira poziciju progress bar-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        if hasattr(main_window, 'progress_pos_x_spin') and hasattr(main_window, 'progress_pos_y_spin'):
            x = main_window.progress_pos_x_spin.value()
            y = main_window.progress_pos_y_spin.value()
            # OVO ĆE POZVATI OVERRIDE MOVE METODU KOJA ĆE AŽURIRATI SPIN BOX-OVE
            main_window.current_shape.move(x, y)
            main_window.current_shape.updatePropertiesDict()

def updateProgressBarSize(main_window):
    """Ažurira veličinu progress bar-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        if hasattr(main_window, 'progress_width_spin') and hasattr(main_window, 'progress_height_spin'):
            width = main_window.progress_width_spin.value()
            height = main_window.progress_height_spin.value()
            # OVO ĆE POZVATI SET_SIZE METODU KOJA ĆE AŽURIRATI SPIN BOX-OVE
            main_window.current_shape.setSize(width, height)

def changeProgressBarProgressColor(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.progress_color)
        if color.isValid():
            main_window.current_shape.setProgressColor(color)
            main_window.progress_progress_color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            main_window.current_shape.updatePropertiesDict()

def changeProgressBarBackgroundColor(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.bar_color)
        if color.isValid():
            main_window.current_shape.setBarColor(color)
            main_window.progress_background_color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            main_window.current_shape.updatePropertiesDict()

def updateProgressBarRange(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        min_val = main_window.progress_min_spin.value()
        max_val = main_window.progress_max_spin.value()
        if min_val < max_val:
            main_window.current_shape.setRange(min_val, max_val)
            # Ažuriraj value spin da bude u opsegu
            main_window.progress_value_spin.setRange(min_val, max_val)
            main_window.current_shape.updatePropertiesDict()

def updateProgressBarValue(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        main_window.current_shape.setValue(main_window.progress_value_spin.value())
        main_window.current_shape.updatePropertiesDict()

#------------------------------------------------------------IMAGE--------------------------------------------------------------

def update_image_active(main_window, state):
    """Ažurira active status za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = is_active
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_image_visible(main_window, state):
    """Ažurira visible status za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setVisibleImage(is_visible)
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_image_static(main_window, state):
    """Ažurira static status za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = is_static
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_image_name(main_window, text):
    """Ažurira ime image widget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        # Sačuvaj staro ime pre promene
        old_name = main_window.current_shape.custom_name
        
        # Postavi novo ime
        main_window.current_shape.custom_name = text
        
        if hasattr(main_window, 'all_image_dicts'):
            # Ako je staro ime bilo u rečniku, izbriši ga
            if old_name in main_window.all_image_dicts:
                main_window.all_image_dicts.pop(old_name)
            
            # Dodaj pod novim imenom
            main_window.all_image_dicts[text] = main_window.current_shape.getPropertiesDict()

def update_image_stack_order(main_window, value):
    """Ažurira stack order za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik - ISPRAVLJENO: all_image_dicts umesto all_button_dicts
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def select_image_file(main_window):
    """Otvara dijalog za odabir slike"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            main_window,
            "Select Image File",
            "",
            "Image Files (*.bmp *.png *.jpg *.jpeg *.jpe);;"
            "BMP Files (*.bmp);;"
            "PNG Files (*.png);;"
            "JPEG Files (*.jpg *.jpeg *.jpe);;"
            "All Files (*.*)"
        )

        if file_path:
            success = main_window.current_shape.setImagePath(file_path)
            if success and hasattr(main_window, 'all_image_dicts'):
                main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_image_frame_enabled(main_window, state):
    """Ažurira enable status za frame i resizuje sliku"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_enabled = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setFrameEnabled(is_enabled)
        
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def update_image_frame_width(main_window, value):
    """Ažurira debljinu frame-a i resizuje sliku"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        main_window.current_shape.setFrameWidth(value)
        
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def change_image_frame_color(main_window):
    """Menja boju frame-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        color = QColorDialog.getColor(main_window.current_shape.frame_color)
        if color.isValid():
            main_window.current_shape.setFrameColor(color)
            main_window.frame_color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            
            if hasattr(main_window, 'all_image_dicts'):
                main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateImageSize(main_window):
    """Ažurira veličinu image widget-a i automatski resizuje sliku"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        width = main_window.width_spin_image.value()
        height = main_window.height_spin_image.value()
        
        # Postavi veličinu (ovo će automatski resizovati sliku)
        main_window.current_shape.setSize(width, height)
        
        # Ažuriraj rečnik
        if hasattr(main_window.current_shape, 'updatePropertiesDict'):
            main_window.current_shape.updatePropertiesDict()

def updateImagePosition(main_window):
    """Ažurira poziciju image-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        if hasattr(main_window, 'pos_x_spin_image') and hasattr(main_window, 'pos_y_spin_image'):
            main_window.current_shape.move(main_window.pos_x_spin_image.value(), main_window.pos_y_spin_image.value())
            
            # Ažuriraj rečnik - ISPRAVLJENO: all_image_dicts umesto all_keys_dicts
            if hasattr(main_window, 'all_image_dicts'):
                main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------LABEL--------------------------------------------------------------

def updateLabelActive(self, state):
    """Ažurira active status za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        self.current_shape.setActive(is_active)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()

def updateLabelVisible(self, state):
    """Ažurira visible status za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        self.current_shape.setVisibleLabel(is_visible)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()

def updateLabelStatic(self, state):
    """Ažurira static status za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        self.current_shape.setStatic(is_static)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()

def updateLabelName(self, text):
    """Ažurira ime label widget-a"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.custom_name = text
        if hasattr(self, 'all_label_dicts'):
            old_name = self.current_shape.custom_name
            self.all_label_dicts[old_name] = self.current_shape.getPropertiesDict()

def update_label_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, LabelWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def changeLabelTextColor(self):
    """Menja boju teksta label-a"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        color = QColorDialog.getColor(self.current_shape.text_color)
        if color.isValid():
            self.current_shape.setTextColor(color)
            self.text_color_rect_label.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(self, 'all_label_dicts'):
                self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()

def updateLabelText(self, text):
    """Ažurira tekst label-a"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.setTextFont(text)
        # Ažuriraj width i height spinbox-ove kada se promeni tekst
        if hasattr(self, 'width_spin_label'):
            self.width_spin_label.setValue(self.current_shape.getWidth())
        if hasattr(self, 'height_spin_label'):
            self.height_spin_label.setValue(self.current_shape.getHeight())
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()


def updateLabelTextSize(self, value):
    """Ažurira veličinu fonta za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.setTextSize(value)
        # Ažuriraj width i height spinbox-ove kada se promeni veličina fonta
        if hasattr(self, 'width_spin_label'):
            self.width_spin_label.setValue(self.current_shape.getWidth())
        if hasattr(self, 'height_spin_label'):
            self.height_spin_label.setValue(self.current_shape.getHeight())
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()

def updateLabelAlignment(self, text):
    """Ažurira poravnanje teksta za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.setTextAlignment(text)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.getPropertiesDict()

def updateLabelSize(self):
    """Ažurira veličinu label-a (veličina se automatski podešava prema tekstu)"""
    if self.current_shape:
        # Veličina se automatski podešava, samo ažuriraj poziciju
        updatePositionSpins(self)
        self.current_shape.updatePropertiesDict()

def updateLabelPosition(main_window):
    """Ažurira poziciju label-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, LabelWidget):
        if hasattr(main_window, 'pos_x_spin_label') and hasattr(main_window, 'pos_y_spin_label'):
            x = main_window.pos_x_spin_label.value()
            y = main_window.pos_y_spin_label.value()
            
            # OVO ĆE POZVATI OVERRIDE MOVE METODU KOJA ĆE AŽURIRATI SPIN BOX-OVE
            main_window.current_shape.move(x, y)
            
            # Rečnik će se ažurirati unutar move metode

def updatePositionSpins(main_window):
    """Ažurira spinbox-ove za poziciju"""
    if main_window.current_shape and hasattr(main_window, 'pos_x_spin') and hasattr(main_window, 'pos_y_spin'):
        main_window.pos_x_spin.blockSignals(True)
        main_window.pos_y_spin.blockSignals(True)
        main_window.pos_x_spin.setValue(main_window.current_shape.x())
        main_window.pos_y_spin.setValue(main_window.current_shape.y())
        main_window.pos_x_spin.blockSignals(False)
        main_window.pos_y_spin.blockSignals(False)
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------NUMERIC--------------------------------------------------------------

def updateNumericActive(main_window, state):
    """Ažurira active status za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setActive(is_active)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateNumericVisible(main_window, state):
    """Ažurira visible status za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setVisibleNumeric(is_visible)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateNumericStatic(main_window, state):
    """Ažurira static status za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.setStatic(is_static)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateNumericName(main_window, text):
    """Ažurira ime numeric widget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.custom_name = text
        if hasattr(main_window, 'all_numeric_dicts'):
            # Ažuriraj ključ u rečniku
            old_name = main_window.current_shape.custom_name
            props = main_window.all_numeric_dicts.get(old_name, {})
            if old_name in main_window.all_numeric_dicts:
                del main_window.all_numeric_dicts[old_name]
            main_window.all_numeric_dicts[text] = props

def update_numeric_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.getPropertiesDict()
        
        # Sortiraj widget-e
        main_window.sort_widgets_by_stack_order()

def updateNumericPosition(main_window):
    """Ažurira poziciju numeric widget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        if hasattr(main_window, 'pos_x_spin_numeric') and hasattr(main_window, 'pos_y_spin_numeric'):
            main_window.current_shape.move(
                main_window.pos_x_spin_numeric.value(),
                main_window.pos_y_spin_numeric.value()
            )
            if hasattr(main_window, 'all_numeric_dicts'):
                main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def changeNumericNumberColor(main_window):
    """Menja boju brojeva za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        color = QColorDialog.getColor(main_window.current_shape.number_color)
        if color.isValid():
            main_window.current_shape.setNumberColor(color)
            main_window.number_color_rect_numeric.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_numeric_dicts'):
                main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateNumericNumber(main_window, value):
    """Ažurira broj koji se prikazuje"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.setNumber(value)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateNumericNumberSize(main_window, value):
    """Ažurira veličinu broja"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.setNumberSize(value)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

def updateNumericNumberAlignment(main_window, text):
    """Ažurira poravnanje broja"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.setNumberAlignment(text)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------CANVAS--------------------------------------------------------------

def change_canvas_color(main_window, canvas, color_rect):
    """Menja boju canvasa"""
    color = QColorDialog.getColor(QColor(canvas.canvas_color))
    if color.isValid():
        canvas.setBackgroundColor(color.name())
        color_rect.color = color.name()
        color_rect.update()
        update_canvas_dict(main_window, canvas)

def toggle_grid(main_window, canvas, state):
    """Uključuje/isključuje grid"""
    canvas.setGridEnabled(state == Qt.CheckState.Checked.value)
    update_canvas_dict(main_window, canvas)

def change_grid_color(main_window, canvas, color_rect):
    """Menja boju grid-a"""
    color = QColorDialog.getColor(QColor(canvas.grid_color))
    if color.isValid():
        canvas.setGridColor(color.name())
        color_rect.color = color.name()
        color_rect.update()
        update_canvas_dict(main_window, canvas)

def change_grid_type(main_window, canvas, text):
    """Menja tip grid-a"""
    grid_type = "lines" if text == "Lines" else "dots"
    canvas.setGridType(grid_type)
    update_canvas_dict(main_window, canvas)

def change_grid_size(main_window, canvas, value):
    """Menja veličinu grid-a"""
    canvas.setGridSize(value)
    update_canvas_dict(main_window, canvas)

def change_canvas_active(main_window, canvas, state):
    """Menja active status canvasa"""
    canvas.setActive(state == Qt.CheckState.Checked.value)
    update_canvas_dict(main_window, canvas)

def change_canvas_visible(main_window, canvas, state):
    """Menja visible status canvasa"""
    canvas.setVisibleCanvas(state == Qt.CheckState.Checked.value)
    update_canvas_dict(main_window, canvas)

def change_canvas_static(main_window, canvas, state):
    """Menja static status canvasa"""
    canvas.setStatic(state == Qt.CheckState.Checked.value)
    update_canvas_dict(main_window, canvas)

def change_canvas_name(main_window, canvas, text):
    """Menja ime canvasa"""
    canvas.setName(text)
    update_canvas_dict(main_window, canvas)

def update_canvas_dict(main_window, canvas):
    """Ažurira rečnik za canvas"""
    if hasattr(main_window, 'all_canvas_dicts'):
        canvas_id = canvas.canvas_id
        canvas_props = canvas.getCanvasProperties()
        
        # Dodaj widget liste ako postoje
        if hasattr(main_window, 'canvas_widgets'):
            widgets = main_window.canvas_widgets.get(canvas_id, [])
            canvas_props['widgets'] = [
                widget.getPropertiesDict() 
                for widget in widgets
                if hasattr(widget, 'getPropertiesDict')
            ]
        
        main_window.all_canvas_dicts[canvas_id] = canvas_props

#------------------------------------------------------------GENERIC--------------------------------------------------------------

def generate_auto_tag(main_window, current_shape):
    """Generiše automatski tag za novi widget"""
    # Proveri da li main_window ima canvas_widgets atribut
    if hasattr(main_window, 'canvas_widgets'):
        all_tags = []
        # Prođi kroz sve widget-e na svim canvas-ima
        for canvas_id, widgets in main_window.canvas_widgets.items():
            for widget in widgets:
                if hasattr(widget, 'tag') and widget != current_shape:
                    all_tags.append(widget.tag)
    else:
        # Stari način
        all_tags = []
        for shape in main_window.all_shapes:
            if hasattr(shape, 'tag') and shape != current_shape:
                all_tags.append(shape.tag)
    
    # Pronađi prvi slobodan tag od 0 do 255
    for i in range(256):
        if i not in all_tags:
            return i
    
    return 0  # Ako su svi zauzeti, vrati 0

def sort_widgets_by_stack_order(main_window):
    """Sortira widget-e po stack_order i ažurira njihov z-order"""
    if not hasattr(main_window, 'all_shapes') or not main_window.all_shapes:
        return
    
    # Sortiraj widget-e po stack_order (manji broj = niže)
    sorted_widgets = sorted(main_window.all_shapes, key=lambda x: x.stack_order)
    
    # Debug ispis
    print(f"\n[callback.py] Sortiranje widget-a po stack_order:")
    for i, widget in enumerate(sorted_widgets):
        print(f"  {i+1}. {widget.custom_name if hasattr(widget, 'custom_name') else 'Unknown'}: stack_order={widget.stack_order}")
    
    # Prvo sve spustimo na dno
    for widget in main_window.all_shapes:
        widget.lower()
    
    # Sada podignemo svaki widget redom (veći stack_order = više)
    for widget in sorted_widgets:
        widget.raise_()
    
    # Ako postoji trenutno selektovani widget, podigni ga na vrh
    if hasattr(main_window, 'current_shape') and main_window.current_shape:
        main_window.current_shape.raise_()


def renumberAllWidgets(main_window):
    """Renumeriše sve widget-e u aplikaciji"""
    # Proveri da li main_window ima canvas_widgets atribut (nova struktura)
    if hasattr(main_window, 'canvas_widgets'):
        # Renumeriši widget-e za svaki canvas
        for canvas_id, widgets in main_window.canvas_widgets.items():
            # Sortiraj widget-e po trenutnom stack_order
            sorted_widgets = sorted(widgets, key=lambda x: x.stack_order)
            
            # Renumeriši
            for i, widget in enumerate(sorted_widgets, 1):
                widget.stack_order = i
            
            # Ažuriraj Z-order
            for widget in widgets:
                widget.lower()
            for widget in sorted_widgets:
                widget.raise_()
    else:
        # Stari način - za kompatibilnost
        if not hasattr(main_window, 'all_shapes'):
            return
        
        # Renumeriši sve widget-e
        for i, shape in enumerate(main_window.all_shapes, 1):
            shape.stack_order = i
        
        # Sortiraj widget-e po stack_order
        sorted_widgets = sorted(main_window.all_shapes, key=lambda x: x.stack_order)
        for widget in main_window.all_shapes:
            widget.lower()
        for widget in sorted_widgets:
            widget.raise_()

def generateWidgetName(main_window, widget_type):
    """Generiše jedinstveno ime za widget na osnovu tipa"""
    # Proveri da li main_window ima canvas_widgets atribut (nova struktura)
    if hasattr(main_window, 'canvas_widgets'):
        # Uzmi sve widget-e iz trenutnog canvasa
        current_canvas = main_window.get_current_canvas()
        if current_canvas:
            current_widgets = main_window.canvas_widgets.get(current_canvas.canvas_id, [])
        else:
            current_widgets = []
        
        # Proveri da li imamo widget-e tog tipa
        same_type_count = 0
        for widget in current_widgets:
            if type(widget).__name__.replace("Widget", "") == widget_type.replace(" ", ""):
                same_type_count += 1
        
        base_name = widget_type.replace(" ", "_")
        name = f"{base_name}_{same_type_count + 1}"
        
        # Proveri da li je ime već zauzeto
        existing_names = []
        for widget in current_widgets:
            if hasattr(widget, 'custom_name'):
                existing_names.append(widget.custom_name)
        
        counter = same_type_count + 1
        while name in existing_names:
            name = f"{base_name}_{counter}"
            counter += 1
        
        return name
    else:
        # Stari način - za kompatibilnost
        if not hasattr(main_window, 'all_shapes'):
            main_window.all_shapes = []
        
        same_type_count = 0
        for shape in main_window.all_shapes:
            if type(shape).__name__.replace("Widget", "") == widget_type.replace(" ", ""):
                same_type_count += 1
        
        base_name = widget_type.replace(" ", "_")
        name = f"{base_name}_{same_type_count + 1}"
        
        existing_names = []
        for shape in main_window.all_shapes:
            if hasattr(shape, 'custom_name'):
                existing_names.append(shape.custom_name)
        
        counter = same_type_count + 1
        while name in existing_names:
            name = f"{base_name}_{counter}"
            counter += 1
        
        return name
