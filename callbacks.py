from PyQt6.QtWidgets import ( QLabel, QHBoxLayout, QColorDialog, QCheckBox, QFileDialog, QPushButton, QDialog, QVBoxLayout )
from PyQt6.QtGui import ( QLinearGradient, QColor )
from PyQt6.QtCore import Qt
from widgets import*  

show_ellipse_warning = True

#------------------------------------------------------------CANVAS--------------------------------------------------------------

def changeCanvasColor( main_window, canvas, color_rect ):
    color = QColorDialog.getColor( QColor( canvas.canvas_color ) )

    if color.isValid():
        canvas.setBackgroundColor( color.name() )
        color_rect.color = color.name()
        color_rect.update()
        updateCanvasDict( main_window, canvas )

def toggleGrid( main_window, canvas, state ):
    canvas.setGridEnabled( state == Qt.CheckState.Checked.value )
    updateCanvasDict( main_window, canvas )

def changeGridColor( main_window, canvas, color_rect ):
    color = QColorDialog.getColor( QColor( canvas.grid_color ) )

    if color.isValid():
        canvas.setGridColor( color.name() )
        color_rect.color = color.name()
        color_rect.update()
        updateCanvasDict( main_window, canvas )

def changeGridType( main_window, canvas, text ):
    if text == "Lines":
        grid_type = "lines"  

    else: 
       grid_type = "dots"

    canvas.setGridType( grid_type )
    updateCanvasDict( main_window, canvas )

def changeGridSize( main_window, canvas, value ):
    canvas.setGridSize( value )
    updateCanvasDict( main_window, canvas )

def changeCanvasActive( main_window, canvas, state ):
    canvas.setActive( state == Qt.CheckState.Checked.value )
    updateCanvasDict( main_window, canvas )

def changeCanvasVisible( main_window, canvas, state ):
    canvas.setVisibleCanvas( state == Qt.CheckState.Checked.value )
    updateCanvasDict( main_window, canvas )

def changeCanvasStatic( main_window, canvas, state ):
    canvas.setStatic( state == Qt.CheckState.Checked.value )
    updateCanvasDict( main_window, canvas )

def changeCanvasName( main_window, canvas, text ):
    canvas.setName( text )
    updateCanvasDict( main_window, canvas )

def updateCanvasDict( main_window, canvas ):
    if hasattr( main_window, 'all_canvas_dicts' ):
        canvas_id = canvas.canvas_id
        canvas_props = canvas.getCanvasProperties()
        
        if hasattr( main_window, 'canvas_widgets' ):
            widgets = main_window.canvas_widgets.get( canvas_id, [] )
            canvas_props[ 'widgets' ] = [ widget.getPropertiesDict() for widget in widgets if hasattr( widget, 'getPropertiesDict' ) ]
        
        main_window.all_canvas_dicts[ canvas_id ] = canvas_props

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
        
        main_window.sortWidgetsByStackOrder()

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
        
        main_window.sortWidgetsByStackOrder()

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

def updateRectangleEdgesWidth( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, RectangleWidget ):
        main_window.current_shape.setBorderWidth( value )

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
        
        main_window.sortWidgetsByStackOrder()

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
        
        main_window.sortWidgetsByStackOrder()

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
        
        main_window.sortWidgetsByStackOrder()

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

def updateButtonSize( main_window ):
    if hasattr( main_window, 'width_spin' ) and hasattr( main_window, 'height_spin' ):
        main_window.current_shape.setFixedSize( main_window.width_spin.value(), main_window.height_spin.value() )
        updateButtonGradient( main_window )
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = main_window.current_shape.getPropertiesDict()

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
        
        main_window.sortWidgetsByStackOrder()

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
        
        main_window.sortWidgetsByStackOrder()

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
        
        main_window.sortWidgetsByStackOrder()

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

def updateDialTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDialActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setActive( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDialVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setVisibleDial( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDialStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setStatic( state == Qt.CheckState.Checked.value )

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDialName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setCustomName( text )

        if hasattr( main_window, 'all_dial_dicts' ):
            old_name = None

            for name, props in list( main_window.all_dial_dicts.items() ):
                if props.get( 'diameter' ) == main_window.current_shape.diameter:
                    old_name = name

                    break
            
            if old_name and old_name != text:
                main_window.all_dial_dicts[ text ] = main_window.all_dial_dicts.pop( old_name )

            else:
                main_window.all_dial_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateDialStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def updateDialPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        if hasattr( main_window, 'pos_x_spin_dial' ) and hasattr( main_window, 'pos_y_spin_dial' ):
            main_window.current_shape.move( main_window.pos_x_spin_dial.value(), main_window.pos_y_spin_dial.value() )

            if hasattr( main_window, 'all_dial_dicts' ):
                main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDialDiameter( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setDiameter( value )

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDial3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( use_3d )

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateDialValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setValue( value )

        if hasattr( main_window, 'all_dial_dicts' ):
            main_window.all_dial_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------TOGGLE--------------------------------------------------------------

def updateToggleTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateTogglePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        if hasattr (main_window, 'pos_x_spin_toggle' ) and hasattr( main_window, 'pos_y_spin_toggle' ):
            main_window.current_shape.move( main_window.pos_x_spin_toggle.value(), main_window.pos_y_spin_toggle.value() )
            main_window.current_shape.updatePropertiesDict()

def updateToggleActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setActive( active )

        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateToggleVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleToggle( visible )

        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateToggleStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setStatic( static )

        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateToggleName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        if text and text != main_window.current_shape.custom_name:
            if hasattr( main_window, 'all_toggle_dicts' ) and main_window.current_shape.custom_name in main_window.all_toggle_dicts:
                old_dict = main_window.all_toggle_dicts.pop( main_window.current_shape.custom_name )
                old_dict[ 'name' ] = text
                main_window.all_toggle_dicts[ text ] = old_dict
            
            main_window.current_shape.custom_name = text

            if hasattr( main_window, 'all_toggle_dicts' ):
                main_window.all_toggle_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateToggleStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def changeToggleKnobColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        color = QColorDialog.getColor( main_window.current_shape.thumb_color )
        if color.isValid():
            main_window.current_shape.setThumbColor( color )

            if hasattr( main_window, 'knob_color_rect_toggle' ):
                main_window.knob_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_toggle_dicts' ):
                main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeToggleBackgroundColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        color = QColorDialog.getColor( main_window.current_shape.background_color )

        if color.isValid():
            main_window.current_shape.setBackgroundColor( color )
            if hasattr( main_window, 'bg_color_rect_toggle' ):
                main_window.bg_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_toggle_dicts' ):
                main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateToggle3D( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        _3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( _3d )

        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateToggleState( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        is_on = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setState( is_on )

        if hasattr( main_window, 'all_toggle_dicts' ):
            main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def toggle3dEffect( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.update()
        main_window.current_shape.updatePropertiesDict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateTogglePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        if hasattr( main_window, 'pos_x_spin_toggle' ) and hasattr( main_window, 'pos_y_spin_toggle' ):
            main_window.current_shape.move( main_window.pos_x_spin_toggle.value(), main_window.pos_y_spin_toggle.value() )
            if hasattr( main_window, 'all_toggle_dicts' ):
                main_window.all_toggle_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateToggleSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        main_window.current_shape.setSize( value, 30 )

#------------------------------------------------------------SCROLL BAR--------------------------------------------------------------

def updateScrollbarTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_scrollbar_dicts' ):
            main_window.all_scrollbar_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateScrollbarActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = active
        main_window.current_shape.update()

def updateScrollbarVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleScrollBar( visible )

def updateScrollbarStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = static

def updateScrollbarName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.custom_name = text

def updateScrollbarStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def updateScrollbarPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        if hasattr( main_window, 'pos_x_spin_scrollbar' ) and hasattr( main_window, 'pos_y_spin_scrollbar' ):
            main_window.current_shape.move( main_window.pos_x_spin_scrollbar.value(), main_window.pos_y_spin_scrollbar.value() )

def updateScrollbarSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        if hasattr( main_window, 'width_spin_scrollbar' ) and hasattr( main_window, 'height_spin_scrollbar' ):
            main_window.current_shape.setSize( main_window.width_spin_scrollbar.value(), main_window.height_spin_scrollbar.value() )

def changeScrollbarThumbColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        color = QColorDialog.getColor( main_window.current_shape.thumb_color )

        if color.isValid():
            main_window.current_shape.setThumbColor( color )
            main_window.thumb_color_rect_scrollbar.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def changeScrollbarTrackColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        color = QColorDialog.getColor( main_window.current_shape.track_color )

        if color.isValid():
            main_window.current_shape.setTrackColor( color )
            main_window.track_color_rect_scrollbar.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateScrollbar3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( use_3d )

def updateScrollbarRange( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.setRange( value )

        if hasattr( main_window, 'current_value_spin_scrollbar' ):
            main_window.current_value_spin_scrollbar.setRange( 0, value )

def updateScrollbarCurrentValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.setCurrentValue( value )

def updateScrollbarKnobSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.setKnobSize( value )

#------------------------------------------------------------SLIDER--------------------------------------------------------------

def updateSliderTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.tag = value

        if hasattr( main_window, 'all_slider_dicts' ):
            main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeSliderBackgroundLeftColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        color = QColorDialog.getColor( main_window.current_shape.thumb_color )

        if color.isValid():
            main_window.current_shape.setThumbColor( color )
            main_window.bg_left_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_slider_dicts' ):
                main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeSliderBackgroundRightColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        color = QColorDialog.getColor( main_window.current_shape.track_color )

        if color.isValid():
            main_window.current_shape.setTrackColor( color )
            main_window.bg_right_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_slider_dicts' ):
                main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSliderActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = active

        if hasattr( main_window, 'all_slider_dicts' ):
            main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSliderVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleSlider( visible )

        if hasattr( main_window, 'all_slider_dicts' ):
            main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSliderStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = static

        if hasattr( main_window, 'all_slider_dicts' ):
            main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSliderName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.custom_name = text

        if hasattr( main_window, 'all_slider_dicts' ):
            old_name = None

            for name, props in list( main_window.all_slider_dicts.items() ):
                if props.get( 'x' ) == main_window.current_shape.x() and props.get('y') == main_window.current_shape.y():
                    old_name = name

                    break
            
            if old_name and old_name != text:
                main_window.all_slider_dicts[ text ] = main_window.all_slider_dicts.pop( old_name )

            else:
                main_window.all_slider_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateSliderStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def updateSliderPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        if hasattr( main_window, 'pos_x_spin_slider' ) and hasattr( main_window, 'pos_y_spin_slider' ):
            main_window.current_shape.move( main_window.pos_x_spin_slider.value(), main_window.pos_y_spin_slider.value() )

            if hasattr( main_window, 'all_slider_dicts' ):
                main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSliderSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        if hasattr( main_window, 'width_spin_slider' ) and hasattr( main_window, 'height_spin_slider' ):
            main_window.current_shape.setSize( main_window.width_spin_slider.value(), main_window.height_spin_slider.value() )

            if hasattr( main_window, 'all_slider_dicts' ):
                main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeSliderKnobColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        color = QColorDialog.getColor( main_window.current_shape.progress_color )

        if color.isValid():
            main_window.current_shape.setProgressColor( color )
            main_window.knob_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_slider_dicts' ):
                main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSlider3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( use_3d )

        if hasattr( main_window, 'all_slider_dicts' ):
            main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateSliderValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.setValue( value )

        if hasattr( main_window, 'all_slider_dicts' ):
            main_window.all_slider_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------PROGRESS BAR--------------------------------------------------------------

def updateProgressBarActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setActive( active )
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleProgressBar( visible )
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setStatic( static )
        main_window.current_shape.updatePropertiesDict()

def updateProgressBar3D( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        _3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( _3d )
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarName( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        main_window.current_shape.custom_name = main_window.progress_name_edit.text()
        main_window.current_shape.updatePropertiesDict()

def updateProgressBarStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def updateProgressBarPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        if hasattr( main_window, 'progress_pos_x_spin' ) and hasattr( main_window, 'progress_pos_y_spin' ):
            x = main_window.progress_pos_x_spin.value()
            y = main_window.progress_pos_y_spin.value()
            main_window.current_shape.move( x, y )
            main_window.current_shape.updatePropertiesDict()

def updateProgressBarSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        if hasattr( main_window, 'progress_width_spin' ) and hasattr( main_window, 'progress_height_spin' ):
            width = main_window.progress_width_spin.value()
            height = main_window.progress_height_spin.value()
            main_window.current_shape.setSize(width, height)

def changeProgressBarProgressColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        color = QColorDialog.getColor( main_window.current_shape.progress_color )

        if color.isValid():
            main_window.current_shape.setProgressColor( color )
            main_window.progress_progress_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
            main_window.current_shape.updatePropertiesDict()

def changeProgressBarBackgroundColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        color = QColorDialog.getColor( main_window.current_shape.bar_color )

        if color.isValid():
            main_window.current_shape.setBarColor( color )
            main_window.progress_background_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
            main_window.current_shape.updatePropertiesDict()

def updateProgressBarRange( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        min_val = main_window.progress_min_spin.value()
        max_val = main_window.progress_max_spin.value()

        if min_val < max_val:
            main_window.current_shape.setRange( min_val, max_val )
            main_window.progress_value_spin.setRange( min_val, max_val )
            main_window.current_shape.updatePropertiesDict()

def updateProgressBarValue( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        main_window.current_shape.setValue( main_window.progress_value_spin.value() )
        main_window.current_shape.updatePropertiesDict()

#------------------------------------------------------------IMAGE--------------------------------------------------------------

def updateImageActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = is_active

        if hasattr( main_window, 'all_image_dicts' ):
            main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateImageVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleImage( is_visible )

        if hasattr( main_window, 'all_image_dicts' ):
            main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateImageStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = is_static

        if hasattr( main_window, 'all_image_dicts' ):
            main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateImageName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        old_name = main_window.current_shape.custom_name
        main_window.current_shape.custom_name = text
        
        if hasattr( main_window, 'all_image_dicts' ):
            if old_name in main_window.all_image_dicts:
                main_window.all_image_dicts.pop( old_name )
            
            main_window.all_image_dicts[ text ] = main_window.current_shape.getPropertiesDict()

def updateImageStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_image_dicts' ):
            main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def selectImageFile( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName( main_window, "Select Image File", "", "Image Files (*.bmp *.png *.jpg *.jpeg *.jpe);;" "BMP Files (*.bmp);;" "PNG Files (*.png);;" "JPEG Files (*.jpg *.jpeg *.jpe);;" "All Files (*.*)" )

        if file_path:
            success = main_window.current_shape.setImagePath( file_path )

            if success and hasattr( main_window, 'all_image_dicts' ):
                main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateImageFrameEnabled( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_enabled = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setFrameEnabled( is_enabled )
        
        if hasattr( main_window, 'all_image_dicts' ):
            main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateImageFrameWidth( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        main_window.current_shape.setFrameWidth( value )
        
        if hasattr( main_window, 'all_image_dicts' ):
            main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeImageFrameColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        color = QColorDialog.getColor( main_window.current_shape.frame_color )

        if color.isValid():
            main_window.current_shape.setFrameColor( color )
            main_window.frame_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
            
            if hasattr( main_window, 'all_image_dicts' ):
                main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateImageSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        width = main_window.width_spin_image.value()
        height = main_window.height_spin_image.value()
        main_window.current_shape.setSize( width, height )

        if hasattr( main_window.current_shape, 'updatePropertiesDict' ):
            main_window.current_shape.updatePropertiesDict()

def updateImagePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        if hasattr( main_window, 'pos_x_spin_image' ) and hasattr( main_window, 'pos_y_spin_image' ):
            main_window.current_shape.move( main_window.pos_x_spin_image.value(), main_window.pos_y_spin_image.value() )
            
            if hasattr( main_window, 'all_image_dicts' ):
                main_window.all_image_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------LABEL--------------------------------------------------------------

def updateLabelActive( self, state ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        is_active = ( state == Qt.CheckState.Checked.value )
        self.current_shape.setActive( is_active )
        if hasattr( self, 'all_label_dicts' ):
            self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelVisible( self, state ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        self.current_shape.setVisibleLabel( is_visible )

        if hasattr( self, 'all_label_dicts' ):
            self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelStatic( self, state ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        self.current_shape.setStatic( is_static )

        if hasattr( self, 'all_label_dicts' ):
            self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelName( self, text ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.custom_name = text

        if hasattr( self, 'all_label_dicts' ):
            old_name = self.current_shape.custom_name
            self.all_label_dicts[ old_name ] = self.current_shape.getPropertiesDict()

def updateLabelStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, LabelWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def changeLabelTextColor( self ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        color = QColorDialog.getColor( self.current_shape.text_color )

        if color.isValid():
            self.current_shape.setTextColor( color )
            self.text_color_rect_label.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( self, 'all_label_dicts' ):
                self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelText( self, text ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.setTextFont( text )

        if hasattr( self, 'width_spin_label' ):
            self.width_spin_label.setValue( self.current_shape.getWidth() )

        if hasattr (self, 'height_spin_label' ):
            self.height_spin_label.setValue( self.current_shape.getHeight() )

        if hasattr( self, 'all_label_dicts' ):
            self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelTextSize( self, value ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.setTextSize( value )

        if hasattr( self, 'width_spin_label' ):
            self.width_spin_label.setValue( self.current_shape.getWidth() )

        if hasattr( self, 'height_spin_label' ):
            self.height_spin_label.setValue( self.current_shape.getHeight() )

        if hasattr( self, 'all_label_dicts' ):
            self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelAlignment( self, text ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.setTextAlignment( text )

        if hasattr( self, 'all_label_dicts' ):
            self.all_label_dicts[ self.current_shape.custom_name ] = self.current_shape.getPropertiesDict()

def updateLabelSize( self ):
    if self.current_shape:
        updatePositionSpins( self )
        self.current_shape.updatePropertiesDict()

def updateLabelPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, LabelWidget ):
        if hasattr( main_window, 'pos_x_spin_label' ) and hasattr( main_window, 'pos_y_spin_label' ):
            x = main_window.pos_x_spin_label.value()
            y = main_window.pos_y_spin_label.value()
            main_window.current_shape.move(x, y)

def updatePositionSpins( main_window ):
    if main_window.current_shape and hasattr( main_window, 'pos_x_spin' ) and hasattr( main_window, 'pos_y_spin' ):
        main_window.pos_x_spin.blockSignals( True )
        main_window.pos_y_spin.blockSignals( True )
        main_window.pos_x_spin.setValue( main_window.current_shape.x() )
        main_window.pos_y_spin.setValue( main_window.current_shape.y() )
        main_window.pos_x_spin.blockSignals( False )
        main_window.pos_y_spin.blockSignals( False )

        if hasattr( main_window, 'all_line_dicts' ):
            main_window.all_line_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------NUMERIC--------------------------------------------------------------

def updateNumericActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        is_active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setActive( is_active )

        if hasattr( main_window, 'all_numeric_dicts' ):
            main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateNumericVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleNumeric( is_visible )

        if hasattr( main_window, 'all_numeric_dicts' ):
            main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateNumericStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setStatic( is_static )

        if hasattr( main_window, 'all_numeric_dicts' ):
            main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateNumericName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.custom_name = text

        if hasattr( main_window, 'all_numeric_dicts' ):
            old_name = main_window.current_shape.custom_name
            props = main_window.all_numeric_dicts.get( old_name, {} )

            if old_name in main_window.all_numeric_dicts:
                del main_window.all_numeric_dicts[ old_name ]

            main_window.all_numeric_dicts[ text ] = props

def updateNumericStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.stack_order = value
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()
        
        main_window.sortWidgetsByStackOrder()

def updateNumericPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        if hasattr( main_window, 'pos_x_spin_numeric' ) and hasattr( main_window, 'pos_y_spin_numeric' ):
            main_window.current_shape.move( main_window.pos_x_spin_numeric.value(), main_window.pos_y_spin_numeric.value() )

            if hasattr( main_window, 'all_numeric_dicts' ):
                main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def changeNumericNumberColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        color = QColorDialog.getColor( main_window.current_shape.number_color )

        if color.isValid():
            main_window.current_shape.setNumberColor( color )
            main_window.number_color_rect_numeric.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

            if hasattr( main_window, 'all_numeric_dicts' ):
                main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateNumericNumber( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.setNumber( value )

        if hasattr( main_window, 'all_numeric_dicts' ):
            main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateNumericNumberSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.setNumberSize( value )

        if hasattr( main_window, 'all_numeric_dicts' ):
            main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

def updateNumericNumberAlignment( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.setNumberAlignment( text )

        if hasattr( main_window, 'all_numeric_dicts' ):
            main_window.all_numeric_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.getPropertiesDict()

#------------------------------------------------------------GENERIC--------------------------------------------------------------

def generateAutoTag( main_window, current_shape ):
    if hasattr( main_window, 'canvas_widgets' ):
        all_tags = []

        for canvas_id, widgets in main_window.canvas_widgets.items():
            for widget in widgets:
                if hasattr( widget, 'tag' ) and widget != current_shape:
                    all_tags.append( widget.tag )

    else:
        all_tags = []

        for shape in main_window.all_shapes:
            if hasattr( shape, 'tag' ) and shape != current_shape:
                all_tags.append( shape.tag )
    
    for i in range( 256 ):
        if i not in all_tags:
            return i
    
    return 0

def generateWidgetName( main_window, widget_type ):
    if hasattr( main_window, 'canvas_widgets' ):
        current_canvas = main_window.getCurrentCanvas()

        if current_canvas:
            current_widgets = main_window.canvas_widgets.get( current_canvas.canvas_id, [] )

        else:
            current_widgets = []
        
        same_type_count = 0

        for widget in current_widgets:
            if type( widget ).__name__.replace( "Widget", "" ) == widget_type.replace( " ", "" ):
                same_type_count += 1
        
        base_name = widget_type.replace( " ", "_" )
        name = f"{ base_name }_{ same_type_count + 1 }"
        
        existing_names = []

        for widget in current_widgets:
            if hasattr( widget, 'custom_name' ):
                existing_names.append( widget.custom_name )
        
        counter = same_type_count + 1

        while name in existing_names:
            name = f"{ base_name }_{ counter }"
            counter += 1
        
        return name
    
    else:
        if not hasattr( main_window, 'all_shapes' ):
            main_window.all_shapes = []
        
        same_type_count = 0

        for shape in main_window.all_shapes:
            if type( shape ).__name__.replace( "Widget", "" ) == widget_type.replace( " ", "" ):
                same_type_count += 1
        
        base_name = widget_type.replace( " ", "_" )
        name = f"{ base_name }_{ same_type_count + 1 }"
        existing_names = []

        for shape in main_window.all_shapes:
            if hasattr( shape, 'custom_name' ):
                existing_names.append( shape.custom_name )
        
        counter = same_type_count + 1

        while name in existing_names:
            name = f"{ base_name }_{ counter }"
            counter += 1
        
        return name
