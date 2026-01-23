from PyQt6.QtWidgets import ( QColorDialog, QFileDialog )
from PyQt6.QtGui import ( QLinearGradient, QColor )
from PyQt6.QtCore import Qt
from widgets import*  

#------------------------------------------------------------CANVAS--------------------------------------------------------------

def changeCanvasColor( main_window, canvas, color_rect ):
    color = QColorDialog.getColor( QColor( canvas.canvas_color ) )

    if color.isValid():
        canvas.setBackgroundColor( color.name() )
        color_rect.color = color.name()
        color_rect.update()

def toggleGrid( main_window, canvas, state ):
    canvas.setGridEnabled( state == Qt.CheckState.Checked.value )

def changeGridColor( main_window, canvas, color_rect ):
    color = QColorDialog.getColor( QColor( canvas.grid_color ) )

    if color.isValid():
        canvas.setGridColor( color.name() )
        color_rect.color = color.name()
        color_rect.update()

def changeGridType( main_window, canvas, text ):
    if text == "Lines":
        grid_type = "lines"  

    else: 
       grid_type = "dots"

    canvas.setGridType( grid_type )

def changeGridSize( main_window, canvas, value ):
    canvas.setGridSize( value )

def changeCanvasActive( main_window, canvas, state ):
    canvas.setActive( state == Qt.CheckState.Checked.value )

def changeCanvasVisible( main_window, canvas, state ):
    canvas.setVisibleCanvas( state == Qt.CheckState.Checked.value )

def changeCanvasStatic( main_window, canvas, state ):
    canvas.setStatic( state == Qt.CheckState.Checked.value )

def changeCanvasName( main_window, canvas, text ):
    canvas.setName( text )

#------------------------------------------------------------LINE--------------------------------------------------------------

def updateLineActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateLineVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.setVisible( state )
    main_window.current_shape.visible = state 
    main_window.current_shape.update()

def updateLineStatic( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateLineName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateLineStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateLineTag( main_window, value ):
     main_window.current_shape.tag = value
     main_window.current_shape.update()

def updateLinePosition (main_window ):
    start_x = main_window.start_x_spin_line.value()
    start_y = main_window.start_y_spin_line.value()
    end_x = main_window.end_x_spin_line.value()
    end_y = main_window.end_y_spin_line.value()
    main_window.current_shape.setLinePosition( start_x, start_y, end_x, end_y )

def updateLineColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.line_color )

    if color.isValid():
        main_window.current_shape.line_color = color 
        main_window.color_rect_line.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateLineEdgesWidth( main_window, value ):
    main_window.current_shape.line_width = value
    main_window.current_shape.update()

#------------------------------------------------------------RECTANGLE--------------------------------------------------------------

def updateRectangleActive( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.active = state

def updateRectangleVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateRectangleStatic( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.static = state

def updateRectangleName( main_window, text ):
    main_window.current_shape.custom_name = text

def updateRectangleStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()

def updateRectangleTag( main_window, value ):
    main_window.current_shape.tag = value

def updateRectanglePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_rect.value(), main_window.pos_y_spin_rect.value() )

def updateRectangleSize( main_window ):
    main_window.current_shape.setFixedSize( main_window.width_spin_rect.value(), main_window.height_spin_rect.value() )

def updateRectangleEdgesColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.edges_color )

    if color.isValid():
        main_window.current_shape.edges_color =  color
        main_window.edges_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateRectangleEdgesWidth( main_window, value ):
    main_window.current_shape.edges_width = value
    main_window.current_shape.update()

def updateRectangleFilled( main_window, state ):
        state == Qt.CheckState.Checked.value
        main_window.current_shape.filled = state
        main_window.current_shape.update()

def updateRectangleGradientDirection( main_window, text ):
    main_window.current_shape.gradient_direction = text
    main_window.current_shape.update()

def updateRectangleGradientStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.start_color )

    if color.isValid():
        main_window.current_shape.start_color = color
        main_window.start_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; "f"border: 2px solid #666;" )
        main_window.current_shape.update()
            
def updateRectangleGradientEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.end_color )

    if color.isValid():
        main_window.current_shape.end_color = color
        main_window.end_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; "f"border: 2px solid #666;" )
        main_window.current_shape.update()
        
#------------------------------------------------------------CIRCLE--------------------------------------------------------------

def updateCircleActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateCircleVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateCircleStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateCircleName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update() 

def updateCircleStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateCircleTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateCirclePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_circle.value() - main_window.current_shape.diameter // 2, main_window.pos_y_spin_circle.value() - main_window.current_shape.diameter // 2 )
    main_window.current_shape.update()

def updateCircleSize( main_window, value ):
    main_window.current_shape.setFixedSize( value, value )
    main_window.current_shape.update()

def updateCircleLineColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.edges_color )

    if color.isValid():
        main_window.current_shape.edges_color = color
        main_window.current_shape.update() 
        main_window.edges_color_rect_circle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateCircleEdgeWidth( main_window, value ):
    main_window.current_shape.edges_width = value 
    main_window.current_shape.update() 

def updateCircleFilled( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.filled = state
    main_window.current_shape.update()

def updateCircleFillColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.fill_color )

    if color.isValid():
        main_window.current_shape.fill_color = color
        main_window.fill_color_rect_circle.setStyleSheet( f"background-color: { color.name() }; "f"border: 1px solid #ccc;" )
        main_window.current_shape.update()

#------------------------------------------------------------ELLIPSE--------------------------------------------------------------

def updateEllipseActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateEllipseVisible( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateEllipseStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateEllipseName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateEllipseStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateEllipseTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateEllipsePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_ellipse.value() - main_window.current_shape.ellipse_width // 2, main_window.pos_y_spin_ellipse.value() - main_window.current_shape.ellipse_height // 2 )
    main_window.current_shape.update()

def updateEllipseSize( main_window ):
    main_window.current_shape.ellipse_width =  main_window.width_spin_ellipse.value() 
    main_window.current_shape.ellipse_height =  main_window.height_spin_ellipse.value() 
    main_window.current_shape.update()

def changeEllipseEdgesColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.edges_color )

    if color.isValid():
        main_window.current_shape.edges_color = color 
        main_window.edges_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateEllipseEdgeWidth( main_window, value ):
    main_window.current_shape.edges_width = value 
    main_window.current_shape.update()

def updateEllipseFilled( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.filled = state
    main_window.current_shape.showFilledWarning( state )
    main_window.current_shape.update()

def updateEllipseGradientDirection( main_window, text ):
    main_window.current_shape.gradient_direction = text 
    main_window.current_shape.update()

def changeEllipseStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )

    if color.isValid():
        main_window.current_shape.gradient_start_color = main_window.current_shape.gradient_end_color 
        main_window.start_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def changeEllipseEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = main_window.current_shape.gradient_start_color
        main_window.end_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

#------------------------------------------------------------BUTTON--------------------------------------------------------------

def updateButtonActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateButtonVisible( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateButtonStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateButtonName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateButtonStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateButtonTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateButtonPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin.value(), main_window.pos_y_spin.value() )
    main_window.current_shape.update()

def updateButtonSize( main_window ):
    main_window.current_shape.setFixedSize( main_window.width_spin.value(), main_window.height_spin.value() )
    main_window.current_shape.update()

def updateButtonStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )
        
    if color.isValid():
        main_window.current_shape.gradient_start_color = color
        main_window.gradient_start_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
    
def updateButtonEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = color
        main_window.current_shape.color_press = color
        main_window.gradient_end_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def update3DButton( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()

def updateButtonText( main_window, text ):
    main_window.current_shape.button_text = text
    main_window.current_shape.update() 
        
def updateButtonTextSize( main_window, value ):
    main_window.current_shape.text_size = value 
    main_window.current_shape.update()

def updateButtonTextColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.text_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
 
#------------------------------------------------------------KEYS--------------------------------------------------------------

def updateKeysActive( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateKeysVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state 
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateKeysStatic( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateKeysName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateKeysStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateKeysPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_keys.value(), main_window.pos_y_spin_keys.value() )
    main_window.current_shape.update()

def updateKeysSize( main_window):
    main_window.current_shape.setFixedSize( main_window.width_spin_keys.value(), main_window.height_spin_keys.value() )
    main_window.current_shape.update()

def updateKeysStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )

    if color.isValid():
        main_window.current_shape.gradient_start_color = color
        main_window.start_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateKeysEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = color 
        main_window.end_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def update3DKeys( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()

def updateKeysType( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.key_type = text
        main_window.current_shape.update()

def updateKeysFontSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.font_size = value 
        main_window.current_shape.update()

def updateKeysFontColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.font_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

#------------------------------------------------------------CLOCK--------------------------------------------------------------

def updateClockActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateClockVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateClockStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateClockName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateClockStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateClockPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_clock.value() - main_window.current_shape.diameter // 2, main_window.pos_y_spin_clock.value() - main_window.current_shape.diameter // 2 )
    main_window.current_shape.update()

def updateClockSize( main_window, value ):
    main_window.current_shape.diameter = value 
    main_window.current_shape.setFixedSize( value, value )
    main_window.current_shape.update()

def updateClockBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.bg_color_rect_clock.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateClockFaceColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.face_color )

    if color.isValid():
        main_window.current_shape.face_color = color
        main_window.face_color_rect_clock.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def update3DClock( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateClockHours( main_window, value ):
    main_window.current_shape.hours = value % 60
    main_window.current_shape.update()

def updateClockMinutes( main_window, value ):
    main_window.current_shape.minutes = value % 60
    main_window.current_shape.update()

def updateClockSeconds( main_window, value ):
    main_window.current_shape.seconds = value % 60
    main_window.current_shape.update()

#------------------------------------------------------------GAUGE--------------------------------------------------------------

def updateGaugeActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateGaugeVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateGaugeStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateGaugeName( main_window, text ):
    main_window.current_shape.custom_name = text 
    main_window.current_shape.update()

def updateGaugeStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateGaugePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_gauge.value() - main_window.current_shape.diameter // 2, main_window.pos_y_spin_gauge.value() - main_window.current_shape.diameter // 2 )
    main_window.current_shape.update()

def updateGaugeSize( main_window, value ):
    main_window.current_shape.diameter = value 
    main_window.current_shape.setFixedSize( value, value )
    main_window.current_shape.update()

def updateGaugeBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.bg_color_rect_gauge.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateGaugeFaceColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.face_color )

    if color.isValid():
        main_window.current_shape.face_color = color
        main_window.face_color_rect_gauge.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def update3DGauge( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateGaugeMajorSubdivision( main_window, value ):
    main_window.current_shape.major_subdivision = value 
    main_window.current_shape.update()

def updateGaugeMinorSubdivision( main_window, value ):
    main_window.current_shape.minor_subdivision = value 
    main_window.current_shape.update()

def updateGaugeRangeValue( main_window, value ):
    main_window.current_shape.range_value = value
    main_window.current_shape.update() 

def updateGaugeValue( main_window, value ):
     main_window.current_shape.value = value 
     main_window.current_shape.update()

#------------------------------------------------------------DIAL--------------------------------------------------------------

def updateDialTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.tag = value

def updateDialActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setActive( state == Qt.CheckState.Checked.value )

def updateDialVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setVisibleDial( state == Qt.CheckState.Checked.value )

def updateDialStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setStatic( state == Qt.CheckState.Checked.value )

def updateDialName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setCustomName( text )

def updateDialStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.stack_order = value
        
        main_window.sortWidgetsByStackOrder()

def updateDialPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        if hasattr( main_window, 'pos_x_spin_dial' ) and hasattr( main_window, 'pos_y_spin_dial' ):
            main_window.current_shape.move( main_window.pos_x_spin_dial.value(), main_window.pos_y_spin_dial.value() )

def updateDialDiameter( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setDiameter( value )

def updateDial3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        effect_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( effect_3d )

def updateDialValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, DialWidget ):
        main_window.current_shape.setValue( value )

#------------------------------------------------------------TOGGLE--------------------------------------------------------------

def updateToggleTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        main_window.current_shape.tag = value

def updateTogglePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        if hasattr (main_window, 'pos_x_spin_toggle' ) and hasattr( main_window, 'pos_y_spin_toggle' ):
            main_window.current_shape.move( main_window.pos_x_spin_toggle.value(), main_window.pos_y_spin_toggle.value() )

def updateToggleActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setActive( active )

def updateToggleVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleToggle( visible )

def updateToggleStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setStatic( static )

def updateToggleStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        main_window.current_shape.stack_order = value
        main_window.sortWidgetsByStackOrder()

def changeToggleThumbColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        color = QColorDialog.getColor( main_window.current_shape.thumb_color )
        if color.isValid():
            main_window.current_shape.setThumbColor( color )

            if hasattr( main_window, 'thumb_color_rect_toggle' ):
                main_window.thumb_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def changeToggleBackgroundColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        color = QColorDialog.getColor( main_window.current_shape.background_color )

        if color.isValid():
            main_window.current_shape.setBackgroundColor( color )
            if hasattr( main_window, 'bg_color_rect_toggle' ):
                main_window.bg_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateToggle3D( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        _3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( _3d )

def updateToggleState( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        is_on = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setState( is_on )

def toggle3dEffect( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.effect_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.update()

def updateTogglePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        if hasattr( main_window, 'pos_x_spin_toggle' ) and hasattr( main_window, 'pos_y_spin_toggle' ):
            main_window.current_shape.move( main_window.pos_x_spin_toggle.value(), main_window.pos_y_spin_toggle.value() )

def updateToggleSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ToggleWidget ):
        main_window.current_shape.setSize( value, 30 )

def updateToggleName( main_window, text ):
    pass

#------------------------------------------------------------SCROLL BAR--------------------------------------------------------------

def updateScrollbarTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.tag = value

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
        effect_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( effect_3d )

def updateScrollbarRange( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.setRange( value )

        if hasattr( main_window, 'current_value_spin_scrollbar' ):
            main_window.current_value_spin_scrollbar.setRange( 0, value )

def updateScrollbarCurrentValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.setCurrentValue( value )

def updateScrollbarThumbSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ScrollBarWidget ):
        main_window.current_shape.setThumbSize( value )

#------------------------------------------------------------SLIDER--------------------------------------------------------------

def updateSliderTag( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.tag = value

def changeSliderBackgroundLeftColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        color = QColorDialog.getColor( main_window.current_shape.thumb_color )

        if color.isValid():
            main_window.current_shape.setThumbColor( color )
            main_window.bg_left_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def changeSliderBackgroundRightColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        color = QColorDialog.getColor( main_window.current_shape.track_color )

        if color.isValid():
            main_window.current_shape.setTrackColor( color )
            main_window.bg_right_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateSliderActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = active

def updateSliderVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleSlider( visible )

def updateSliderStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = static

def updateSliderName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.custom_name = text

def updateSliderStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.stack_order = value
        main_window.sortWidgetsByStackOrder()

def updateSliderPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        if hasattr( main_window, 'pos_x_spin_slider' ) and hasattr( main_window, 'pos_y_spin_slider' ):
            main_window.current_shape.move( main_window.pos_x_spin_slider.value(), main_window.pos_y_spin_slider.value() )

def updateSliderSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        if hasattr( main_window, 'width_spin_slider' ) and hasattr( main_window, 'height_spin_slider' ):
            main_window.current_shape.setSize( main_window.width_spin_slider.value(), main_window.height_spin_slider.value() )

def changeSliderThumbColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        color = QColorDialog.getColor( main_window.current_shape.progress_color )

        if color.isValid():
            main_window.current_shape.setProgressColor( color )
            main_window.thumb_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateSlider3d( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        effect_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( effect_3d )

def updateSliderValue( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, SliderWidget ):
        main_window.current_shape.setValue( value )

#------------------------------------------------------------PROGRESS BAR--------------------------------------------------------------

def updateProgressBarActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setActive( active )

def updateProgressBarVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleProgressBar( visible )

def updateProgressBarStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setStatic( static )

def updateProgressBar3D( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        _3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.set3d( _3d )

def updateProgressBarName( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        main_window.current_shape.custom_name = main_window.progress_name_edit.text()

def updateProgressBarStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        main_window.current_shape.stack_order = value
        main_window.sortWidgetsByStackOrder()

def updateProgressBarPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        if hasattr( main_window, 'progress_pos_x_spin' ) and hasattr( main_window, 'progress_pos_y_spin' ):
            x = main_window.progress_pos_x_spin.value()
            y = main_window.progress_pos_y_spin.value()
            main_window.current_shape.move( x, y )

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

def changeProgressBarBackgroundColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        color = QColorDialog.getColor( main_window.current_shape.bar_color )

        if color.isValid():
            main_window.current_shape.setBarColor( color )
            main_window.progress_background_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateProgressBarRange( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        max_val = main_window.progress_max_spin.value()

        if 0 < max_val:
            main_window.current_shape.setRange( 0, max_val )
            main_window.progress_value_spin.setRange( 0, max_val )

def updateProgressBarValue( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ProgressBarWidget ):
        main_window.current_shape.setValue( main_window.progress_value_spin.value() )

#------------------------------------------------------------IMAGE--------------------------------------------------------------

def updateImageActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.active = is_active

def updateImageVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleImage( is_visible )

def updateImageStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.static = is_static

def updateImageName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        main_window.current_shape.custom_name = text

def updateImageStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        main_window.current_shape.stack_order = value
        main_window.sortWidgetsByStackOrder()

def selectImageFile( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName( main_window, "Select Image File", "", "Image Files (*.bmp *.png *.jpg *.jpeg *.jpe);;" "BMP Files (*.bmp);;" "PNG Files (*.png);;" "JPEG Files (*.jpg *.jpeg *.jpe);;" "All Files (*.*)" )

        if file_path:
            success = main_window.current_shape.setImagePath( file_path )

def updateImageFrameEnabled( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        is_enabled = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setFrameEnabled( is_enabled )

def updateImageFrameWidth( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        main_window.current_shape.setFrameWidth( value )

def changeImageFrameColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        color = QColorDialog.getColor( main_window.current_shape.frame_color )

        if color.isValid():
            main_window.current_shape.setFrameColor( color )
            main_window.frame_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateImageSize( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        width = main_window.width_spin_image.value()
        height = main_window.height_spin_image.value()
        main_window.current_shape.setSize( width, height )

def updateImagePosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ImageWidget ):
        if hasattr( main_window, 'pos_x_spin_image' ) and hasattr( main_window, 'pos_y_spin_image' ):
            main_window.current_shape.move( main_window.pos_x_spin_image.value(), main_window.pos_y_spin_image.value() )


#------------------------------------------------------------LABEL--------------------------------------------------------------

def updateLabelActive( self, state ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        is_active = ( state == Qt.CheckState.Checked.value )
        self.current_shape.setActive( is_active )

def updateLabelVisible( self, state ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        self.current_shape.setVisibleLabel( is_visible )

def updateLabelStatic( self, state ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        self.current_shape.setStatic( is_static )

def updateLabelName( self, text ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.custom_name = text

def updateLabelStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, LabelWidget ):
        main_window.current_shape.stack_order = value
        main_window.sortWidgetsByStackOrder()

def changeLabelTextColor( self ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        color = QColorDialog.getColor( self.current_shape.text_color )

        if color.isValid():
            self.current_shape.setTextColor( color )
            self.text_color_rect_label.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateLabelText( self, text ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.setTextFont( text )

        if hasattr( self, 'width_spin_label' ):
            self.width_spin_label.setValue( self.current_shape.keys_width )

        if hasattr (self, 'height_spin_label' ):
            self.height_spin_label.setValue( self.current_shape.keys_height )

def updateLabelTextSize( self, value ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.setTextSize( value )

        if hasattr( self, 'width_spin_label' ):
            self.width_spin_label.setValue( self.current_shape.keys_width )

        if hasattr( self, 'height_spin_label' ):
            self.height_spin_label.setValue( self.current_shape.keys_height )

def updateLabelAlignment( self, text ):
    if self.current_shape and isinstance( self.current_shape, LabelWidget ):
        self.current_shape.setTextAlignment( text )

def updateLabelSize( self ):
    if self.current_shape:
        updatePositionSpins( self )

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

#------------------------------------------------------------NUMERIC--------------------------------------------------------------

def updateNumericActive( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        is_active = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setActive( is_active )

def updateNumericVisible( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        is_visible = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setVisibleNumeric( is_visible )

def updateNumericStatic( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        is_static = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.setStatic( is_static )

def updateNumericName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.custom_name = text

def updateNumericStackOrder( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.stack_order = value
        main_window.sortWidgetsByStackOrder()

def updateNumericPosition( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        if hasattr( main_window, 'pos_x_spin_numeric' ) and hasattr( main_window, 'pos_y_spin_numeric' ):
            main_window.current_shape.move( main_window.pos_x_spin_numeric.value(), main_window.pos_y_spin_numeric.value() )

def changeNumericNumberColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        color = QColorDialog.getColor( main_window.current_shape.number_color )

        if color.isValid():
            main_window.current_shape.setNumberColor( color )
            main_window.number_color_rect_numeric.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateNumericNumber( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.setNumber( value )

def updateNumericNumberSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.setNumberSize( value )

def updateNumericNumberAlignment( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, NumericWidget ):
        main_window.current_shape.setNumberAlignment( text )


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
