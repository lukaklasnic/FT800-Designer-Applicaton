from PyQt6.QtWidgets import ( QColorDialog, QFileDialog )
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from widgets import*  

#------------------------------------------------------------CANVAS--------------------------------------------------------------

def updateCanvasActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.active = state 
    main_window.current_canvas.update()

def updateCanvasVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.visible = state
    main_window.current_canvas.setVisible( main_window.current_canvas.visible )
    main_window.current_canvas.update()

def updateCanvasStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.static = state
    main_window.current_canvas.update()

def updateCanvasName(main_window, text):
    main_window.current_canvas.custom_name = text
    main_window.current_canvas.update()

def updateCanvasColor( main_window ):
    color = QColorDialog.getColor( main_window.current_canvas.canvas_color )
    
    if color.isValid():
        main_window.current_canvas.canvas_color = color
        main_window.canvas_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_canvas.update()

def updateToggleGrid( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.canvas_grid_enable = state
    main_window.current_canvas.update()

def updateGridColor(main_window):
    color = QColorDialog.getColor( main_window.current_canvas.grid_color )
    
    if color.isValid():
        main_window.current_canvas.grid_color = color
        main_window.grid_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_canvas.update()

def changeGridType ( main_window, text ):
    main_window.current_canvas.grid_type = text
    main_window.current_canvas.update()

def changeGridSize( main_window, value ):
    main_window.current_canvas.grid_size = value
    main_window.current_canvas.update()

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
        main_window.current_shape.gradient_start_color = main_window.current_shape.gradient_start_color 
        main_window.start_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def changeEllipseEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = main_window.current_shape.gradient_end_color
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
    main_window.current_shape.move( main_window.pos_x_spin_button.value(), main_window.pos_y_spin_button.value() )
    main_window.current_shape.update()

def updateButtonSize( main_window ):
    main_window.current_shape.setFixedSize( main_window.width_spin_button.value(), main_window.height_spin_button.value() )
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

def updateDialActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateDialVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateDialStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateDialName( main_window, text ):
    main_window.current_shape.custom_name = text 
    main_window.current_shape.update()

def updateDialStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateDialTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateDialPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_dial.value() - main_window.current_shape.diameter // 2, main_window.pos_y_spin_dial.value() - main_window.current_shape.diameter // 2 )

def updateDialSize( main_window, value ):
    main_window.current_shape.diameter = value 
    main_window.current_shape.setFixedSize( value, value )
    main_window.current_shape.update()

def updateDialBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.bg_color_rect_dial.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateDialPointerColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.pointer_color )

    if color.isValid():
        main_window.current_shape.pointer_color = color
        main_window.face_color_rect_dial.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateDial3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateDialValue( main_window, value ):
    main_window.current_shape.value = value 
    main_window.current_shape.update()

#------------------------------------------------------------TOGGLE--------------------------------------------------------------

def updateToggleActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateToggleVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateToggleStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateToggleName( main_window, text ):
    main_window.current_shape.custom_name = text 
    main_window.current_shape.update()

def updateToggleStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateToggleTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateTogglePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_toggle.value(), main_window.pos_y_spin_toggle.value() )
    main_window.current_shape.update()

def updateToggleSize( main_window, value ):
    main_window.current_shape.setFixedSize( main_window.width_spin_toggle.value(), 30 )
    main_window.current_shape.toggle_width = value
    main_window.current_shape.update()

def updateToggleThumbColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.thumb_color )

    if color.isValid():
        main_window.current_shape.thumb_color = color 
        main_window.thumb_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateToggleBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.bg_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateToggleTextColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.text_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateToggle3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateToggleState( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.state = state 
    main_window.current_shape.update()

#------------------------------------------------------------SCROLL BAR--------------------------------------------------------------

def updateScrollbarActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateScrollbarVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateScrollbarStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateScrollbarName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateScrollbarStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateScrollbarTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateScrollbarPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_scrollbar.value(), main_window.pos_y_spin_scrollbar.value() )
    main_window.current_shape.update()

def updateScrollbarSize( main_window ):
    main_window.current_shape.scroll_bar_width = main_window.width_spin_scrollbar.value()
    main_window.current_shape.scroll_bar_height = main_window.height_spin_scrollbar.value()
    main_window.current_shape.setFixedSize( main_window.current_shape.scroll_bar_width, main_window.current_shape.scroll_bar_height  )
    main_window.current_shape.update()

def updateScrollbarThumbColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.thumb_color )

    if color.isValid():
        main_window.current_shape.thumb_color = color 
        main_window.thumb_color_rect_scrollbar.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateScrollbarBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.thumb_color_rect_scrollbar.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateScrollbar3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateScrollbarCurrentValue( main_window, value ):
    main_window.current_shape.current_value = value 
    main_window.current_shape.update()

def updateScrollbarThumbSize( main_window, value ):
    main_window.current_shape.thumb_size = value 
    main_window.current_shape.update()

#------------------------------------------------------------SLIDER--------------------------------------------------------------

def updateSliderActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateSliderVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateSliderStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateSliderName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateSliderStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateSliderTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()

def updateSliderPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_slider.value(), main_window.pos_y_spin_slider.value() )
    main_window.current_shape.update()

def updateSliderSize( main_window, value ):
    main_window.current_shape.slider_width = main_window.width_spin_slider.value()
    main_window.current_shape.slider_height = main_window.height_spin_slider.value() 
    main_window.current_shape.setFixedSize( main_window.current_shape.slider_width, main_window.current_shape.slider_height )
    main_window.current_shape.update()

def changeSliderThumbColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color_left )

    if color.isValid():
        main_window.current_shape.thumb_color = color
        main_window.thumb_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def changeSliderBackgroundLeftColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.thumb_color )

    if color.isValid():
        main_window.current_shape.background_color_left = color 
        main_window.bg_left_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def changeSliderBackgroundRightColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color_right )

    if color.isValid():
        main_window.current_shape.background_color_right = color 
        main_window.bg_right_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateSlider3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateSliderValue( main_window, value ):
    main_window.current_shape.value = value 
    main_window.current_shape.update()

#------------------------------------------------------------PROGRESS BAR--------------------------------------------------------------

def updateProgressBarActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateProgressBarVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateProgressBarStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateProgressBarName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateProgressBarStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateProgressBarPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_progress_bar.value(), main_window.pos_y_spin_progress_bar.value() )
    main_window.current_shape.update()

def updateProgressBarSize( main_window ):
    main_window.current_shape.progress_bar_width = main_window.width_spin_progress_bar.value()
    main_window.current_shape.progress_bar_height = main_window.height_spin_progress_bar.value() 
    main_window.current_shape.setFixedSize( main_window.current_shape.progress_bar_width, main_window.current_shape.progress_bar_height )
    main_window.current_shape.update()

def updateProgressBarProgressColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.progress_color )

    if color.isValid():
        main_window.current_shape.progress_color = color 
        main_window.progress_progress_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateProgressBarBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.progress_background_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateProgressBar3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()

def updateProgressBarRange( main_window ):
    main_window.current_shape.range = main_window.progress_bar_range_spin.value()
    main_window.current_shape.update()

def updateProgressBarValue( main_window ):
    main_window.current_shape.value = main_window.progress_bar_value_spin.value()
    main_window.current_shape.update()

#------------------------------------------------------------IMAGE--------------------------------------------------------------

def updateImageActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateImageVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateImageStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateImageName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateImageStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateImagePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_image.value(), main_window.pos_y_spin_image.value() )
    main_window.current_shape.update()

def updateImageSize( main_window ):
    main_window.current_shape.image_width = main_window.width_spin_image.value()
    main_window.current_shape.image_height = main_window.height_spin_image.value()
    main_window.current_shape.setFixedSize( main_window.current_shape.image_width, main_window.current_shape.image_height )
    main_window.current_shape.resizePixmap()
    main_window.current_shape.update()

def selectImageFile( main_window ):
    file_path, _ = QFileDialog.getOpenFileName( main_window, "Select Image File", "", "Image Files (*.bmp *.png *.jpg *.jpeg *.jpe);;" "BMP Files (*.bmp);;" "PNG Files (*.png);;" "JPEG Files (*.jpg *.jpeg *.jpe);;" "All Files (*.*)" )

    if file_path:
        main_window.current_shape.setImagePath( file_path )

def updateImageFrameEnabled( main_window, state ):
        state == Qt.CheckState.Checked.value 
        main_window.current_shape.frame_enabled = state
        main_window.current_shape.update()

def changeImageFrameColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.frame_color )

    if color.isValid():
        main_window.current_shape.frame_color = color 
        main_window.frame_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )

def updateImageFrameWidth( main_window, value ):
    main_window.current_shape.frame_width = value 
    main_window.current_shape.update()

#------------------------------------------------------------LABEL--------------------------------------------------------------

def updateLabelActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()

def updateLabelVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()

def updateLabelStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()

def updateLabelName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()

def updateLabelStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()

def updateLabelPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_label.value(), main_window.pos_y_spin_label.value() )
    main_window.current_shape.update()

def updateLabelTextColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.text_color_rect_label.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()

def updateLabelText( main_window, text ):
    main_window.current_shape.text = text 
    main_window.current_shape.setSizeBasedOnText()
    main_window.current_shape.update()

def updateLabelTextSize( main_window, value ):
    main_window.current_shape.text_size = value 
    main_window.current_shape.setSizeBasedOnText()
    main_window.current_shape.update()

def updateLabelAlignment( main_window, text ):
    main_window.current_shape.text_alignment = text 
    main_window.current_shape.update()

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
