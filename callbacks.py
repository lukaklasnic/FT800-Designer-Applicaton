from PyQt6.QtWidgets import ( QColorDialog, QFileDialog )
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from widgets import*  

#------------------------------------------------------------CANVAS--------------------------------------------------------------

def updateCanvasActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.active = state 
    main_window.current_canvas.update()
    main_window.current_canvas.updateDataDict()

def updateCanvasVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.visible = state
    main_window.current_canvas.setVisible( main_window.current_canvas.visible )
    main_window.current_canvas.update()
    main_window.current_canvas.updateDataDict()

def updateCanvasStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_canvas.static = state
    main_window.current_canvas.update()
    main_window.current_canvas.updateDataDict()

def updateCanvasName(main_window, text):
    main_window.current_canvas.custom_name = text
    main_window.current_canvas.update()
    main_window.current_canvas.updateDataDict()

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
        main_window.current_canvas.updateDataDict()

def changeGridType ( main_window, text ):
    main_window.current_canvas.grid_type = text
    main_window.current_canvas.update()
    main_window.current_canvas.updateDataDict()

def changeGridSize( main_window, value ):
    main_window.current_canvas.grid_size = value
    main_window.current_canvas.update()
    main_window.current_canvas.updateDataDict()

#------------------------------------------------------------LINE--------------------------------------------------------------

def updateLineActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLineVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.setVisible( state )
    main_window.current_shape.visible = state 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLineStatic( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLineName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLineStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLineTag( main_window, value ):
     main_window.current_shape.tag = value
     main_window.current_shape.update()
     main_window.current_shape.updateDataDict()

def updateLinePosition (main_window ):
    start_x = main_window.start_x_spin_line.value()
    start_y = main_window.start_y_spin_line.value()
    end_x = main_window.end_x_spin_line.value()
    end_y = main_window.end_y_spin_line.value()
    main_window.current_shape.setLinePosition( start_x, start_y, end_x, end_y )
    main_window.current_shape.updateDataDict()

def updateLineColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.line_color )

    if color.isValid():
        main_window.current_shape.line_color = color 
        main_window.color_rect_line.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateLineEdgesWidth( main_window, value ):
    main_window.current_shape.line_width = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------RECTANGLE--------------------------------------------------------------

def updateRectangleActive( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleStatic( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectanglePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_rect.value(), main_window.pos_y_spin_rect.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleSize( main_window ):
    main_window.current_shape.setFixedSize( main_window.width_spin_rect.value(), main_window.height_spin_rect.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleEdgesColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.edges_color )

    if color.isValid():
        main_window.current_shape.edges_color =  color
        main_window.edges_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateRectangleEdgesWidth( main_window, value ):
    main_window.current_shape.edges_width = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleFilled( main_window, state ):
        state == Qt.CheckState.Checked.value
        main_window.current_shape.filled = state
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateRectangleGradientDirection( main_window, text ):
    main_window.current_shape.gradient_direction = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateRectangleGradientStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.start_color )

    if color.isValid():
        main_window.current_shape.start_color = color
        main_window.start_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; "f"border: 2px solid #666;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()
            
def updateRectangleGradientEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.end_color )

    if color.isValid():
        main_window.current_shape.end_color = color
        main_window.end_color_rect_rect.setStyleSheet( f"background-color: { color.name() }; "f"border: 2px solid #666;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()
        
#------------------------------------------------------------CIRCLE--------------------------------------------------------------

def updateCircleActive(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleVisible(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible(state)
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleStatic(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleName(main_window, text):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update() 
    main_window.current_shape.updateDataDict()

def updateCircleStackOrder(main_window, value):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleTag(main_window, value):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCirclePosition(main_window):
    """Ažuriraj poziciju kruga na osnovu centra"""
    # Izračunaj gornji levi ugao na osnovu centra
    x = main_window.pos_x_spin_circle.value() - main_window.current_shape.diameter // 2
    y = main_window.pos_y_spin_circle.value() - main_window.current_shape.diameter // 2
    
    main_window.current_shape.move(x, y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleSize(main_window):
    """Ažuriraj veličinu kruga"""
    new_diameter = main_window.diameter_spin_circle.value()
    
    # Sačuvaj trenutni centar
    current_center_x = main_window.current_shape.center_x
    current_center_y = main_window.current_shape.center_y
    
    # Izračunaj novu poziciju gornjeg levog ugla da centar ostane isti
    new_x = current_center_x - new_diameter // 2
    new_y = current_center_y - new_diameter // 2
    
    main_window.current_shape.diameter = new_diameter
    main_window.current_shape.setFixedSize(new_diameter, new_diameter)
    main_window.current_shape.move(new_x, new_y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleLineColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.edges_color)

    if color.isValid():
        main_window.current_shape.edges_color = color
        main_window.edges_color_rect_circle.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update() 
        main_window.current_shape.updateDataDict()

def updateCircleEdgeWidth(main_window, value):
    main_window.current_shape.edges_width = value 
    main_window.current_shape.update() 
    main_window.current_shape.updateDataDict()

def updateCircleFilled(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.filled = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateCircleFillColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.fill_color)

    if color.isValid():
        main_window.current_shape.fill_color = color
        main_window.fill_color_rect_circle.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()
#------------------------------------------------------------ELLIPSE--------------------------------------------------------------

def updateEllipseActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseVisible( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipsePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_ellipse.value() - main_window.current_shape.ellipse_width // 2, main_window.pos_y_spin_ellipse.value() - main_window.current_shape.ellipse_height // 2 )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseSize( main_window ):
    main_window.current_shape.ellipse_width =  main_window.width_spin_ellipse.value() 
    main_window.current_shape.ellipse_height =  main_window.height_spin_ellipse.value() 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def changeEllipseEdgesColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.edges_color )

    if color.isValid():
        main_window.current_shape.edges_color = color 
        main_window.edges_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateEllipseEdgeWidth( main_window, value ):
    main_window.current_shape.edges_width = value 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseFilled( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.filled = state
    main_window.current_shape.showFilledWarning( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateEllipseGradientDirection( main_window, text ):
    main_window.current_shape.gradient_direction = text 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def changeEllipseStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )

    if color.isValid():
        main_window.current_shape.gradient_start_color = main_window.current_shape.gradient_start_color 
        main_window.start_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def changeEllipseEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = main_window.current_shape.gradient_end_color
        main_window.end_color_rect_ellipse.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

#------------------------------------------------------------BUTTON--------------------------------------------------------------

def updateButtonActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonVisible( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_button.value(), main_window.pos_y_spin_button.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonSize( main_window ):
    main_window.current_shape.setFixedSize( main_window.width_spin_button.value(), main_window.height_spin_button.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )
        
    if color.isValid():
        main_window.current_shape.gradient_start_color = color
        main_window.gradient_start_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()
    
def updateButtonEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = color
        main_window.current_shape.color_press = color
        main_window.gradient_end_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def update3DButton( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonText( main_window, text ):
    main_window.current_shape.button_text = text
    main_window.current_shape.update() 
    main_window.current_shape.updateDataDict()
        
def updateButtonTextSize( main_window, value ):
    main_window.current_shape.text_size = value 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateButtonTextColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.text_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()
 
#------------------------------------------------------------KEYS--------------------------------------------------------------

def updateKeysActive( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state 
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysStatic( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_keys.value(), main_window.pos_y_spin_keys.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysSize( main_window):
    main_window.current_shape.setFixedSize( main_window.width_spin_keys.value(), main_window.height_spin_keys.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysStartColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_start_color )

    if color.isValid():
        main_window.current_shape.gradient_start_color = color
        main_window.start_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateKeysEndColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.gradient_end_color )

    if color.isValid():
        main_window.current_shape.gradient_end_color = color 
        main_window.end_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def update3DKeys( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateKeysType( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.key_type = text
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateKeysFontSize( main_window, value ):
    if main_window.current_shape and isinstance( main_window.current_shape, KeysWidget ):
        main_window.current_shape.font_size = value 
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateKeysFontColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.font_color_rect_keys.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

#------------------------------------------------------------CLOCK--------------------------------------------------------------

def updateClockActive(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockVisible(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible(state)
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockStatic(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockName(main_window, text):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockStackOrder(main_window, value):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockTag(main_window, value):
    """Nova funkcija za ažuriranje tag-a (ako je potrebno)"""
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockPosition(main_window):
    """Ažuriraj poziciju sata na osnovu centra"""
    # Izračunaj gornji levi ugao na osnovu centra
    x = main_window.pos_x_spin_clock.value() - main_window.current_shape.diameter // 2
    y = main_window.pos_y_spin_clock.value() - main_window.current_shape.diameter // 2
    
    main_window.current_shape.move(x, y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockSize(main_window, value):
    """Ažuriraj veličinu sata"""
    new_diameter = main_window.diameter_spin_clock.value()
    
    # Sačuvaj trenutni centar
    current_center_x = main_window.current_shape.center_x
    current_center_y = main_window.current_shape.center_y
    
    # Izračunaj novu poziciju gornjeg levog ugla da centar ostane isti
    new_x = current_center_x - new_diameter // 2
    new_y = current_center_y - new_diameter // 2
    
    main_window.current_shape.diameter = new_diameter
    main_window.current_shape.setFixedSize(new_diameter, new_diameter)
    main_window.current_shape.move(new_x, new_y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockBackgroundColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.background_color)

    if color.isValid():
        main_window.current_shape.background_color = color
        main_window.bg_color_rect_clock.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateClockFaceColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.face_color)

    if color.isValid():
        main_window.current_shape.face_color = color
        main_window.face_color_rect_clock.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def update3DClock(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockHours(main_window, value):
    main_window.current_shape.hours = value % 24  # Korigovano na 24 sata
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockMinutes(main_window, value):
    main_window.current_shape.minutes = value % 60
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateClockSeconds(main_window, value):
    main_window.current_shape.seconds = value % 60
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------GAUGE--------------------------------------------------------------

def updateGaugeActive(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeVisible(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible(state)
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeStatic(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeName(main_window, text):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeStackOrder(main_window, value):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeTag(main_window, value):
    """Nova funkcija za ažuriranje tag-a (ako je potrebno)"""
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugePosition(main_window):
    """Ažuriraj poziciju merača na osnovu centra"""
    # Izračunaj gornji levi ugao na osnovu centra
    x = main_window.pos_x_spin_gauge.value() - main_window.current_shape.diameter // 2
    y = main_window.pos_y_spin_gauge.value() - main_window.current_shape.diameter // 2
    
    main_window.current_shape.move(x, y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeSize(main_window, value):
    """Ažuriraj veličinu merača"""
    new_diameter = main_window.diameter_spin_gauge.value()
    
    # Sačuvaj trenutni centar
    current_center_x = main_window.current_shape.center_x
    current_center_y = main_window.current_shape.center_y
    
    # Izračunaj novu poziciju gornjeg levog ugla da centar ostane isti
    new_x = current_center_x - new_diameter // 2
    new_y = current_center_y - new_diameter // 2
    
    main_window.current_shape.diameter = new_diameter
    main_window.current_shape.setFixedSize(new_diameter, new_diameter)
    main_window.current_shape.move(new_x, new_y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeBackgroundColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.background_color)

    if color.isValid():
        main_window.current_shape.background_color = color
        main_window.bg_color_rect_gauge.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateGaugeFaceColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.face_color)

    if color.isValid():
        main_window.current_shape.face_color = color
        main_window.face_color_rect_gauge.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def update3DGauge(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeMajorSubdivision(main_window, value):
    main_window.current_shape.major_subdivision = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeMinorSubdivision(main_window, value):
    main_window.current_shape.minor_subdivision = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeRangeValue(main_window, value):
    main_window.current_shape.range_value = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateGaugeValue(main_window, value):
    main_window.current_shape.value = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------DIAL--------------------------------------------------------------

def updateDialActive(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialVisible(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible(state)
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialStatic(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialName(main_window, text):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialStackOrder(main_window, value):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialTag(main_window, value):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialPosition(main_window):
    """Ažuriraj poziciju dajala na osnovu centra"""
    # Izračunaj gornji levi ugao na osnovu centra
    x = main_window.pos_x_spin_dial.value() - main_window.current_shape.diameter // 2
    y = main_window.pos_y_spin_dial.value() - main_window.current_shape.diameter // 2
    
    main_window.current_shape.move(x, y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialSize(main_window, value):
    """Ažuriraj veličinu dajala"""
    new_diameter = main_window.diameter_spin_dial.value()
    
    # Sačuvaj trenutni centar
    current_center_x = main_window.current_shape.center_x
    current_center_y = main_window.current_shape.center_y
    
    # Izračunaj novu poziciju gornjeg levog ugla da centar ostane isti
    new_x = current_center_x - new_diameter // 2
    new_y = current_center_y - new_diameter // 2
    
    main_window.current_shape.diameter = new_diameter
    main_window.current_shape.setFixedSize(new_diameter, new_diameter)
    main_window.current_shape.move(new_x, new_y)
    main_window.current_shape.updateCenterPosition()  # Ažuriraj centar
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialBackgroundColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.background_color)

    if color.isValid():
        main_window.current_shape.background_color = color
        main_window.bg_color_rect_dial.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateDialPointerColor(main_window):
    color = QColorDialog.getColor(main_window.current_shape.pointer_color)

    if color.isValid():
        main_window.current_shape.pointer_color = color
        main_window.face_color_rect_dial.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc;"
        )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateDial3D(main_window, state):
    state = state == Qt.CheckState.Checked.value
    main_window.current_shape.effect_3d = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateDialValue(main_window, value):
    main_window.current_shape.value = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()
#------------------------------------------------------------TOGGLE--------------------------------------------------------------

def updateToggleActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleName( main_window, text ):
    main_window.current_shape.custom_name = text 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateTogglePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_toggle.value(), main_window.pos_y_spin_toggle.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleSize( main_window, value ):
    main_window.current_shape.setFixedSize( main_window.width_spin_toggle.value(), 30 )
    main_window.current_shape.toggle_width = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleThumbColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.thumb_color )

    if color.isValid():
        main_window.current_shape.thumb_color = color 
        main_window.thumb_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateToggleBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.bg_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateToggleTextColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.text_color_rect_toggle.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateToggle3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateToggleState( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.state = state 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------SCROLL BAR--------------------------------------------------------------

def updateScrollbarActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_scrollbar.value(), main_window.pos_y_spin_scrollbar.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarSize( main_window ):
    main_window.current_shape.scroll_bar_width = main_window.width_spin_scrollbar.value()
    main_window.current_shape.scroll_bar_height = main_window.height_spin_scrollbar.value()
    main_window.current_shape.setFixedSize( main_window.current_shape.scroll_bar_width, main_window.current_shape.scroll_bar_height  )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarThumbColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.thumb_color )

    if color.isValid():
        main_window.current_shape.thumb_color = color 
        main_window.thumb_color_rect_scrollbar.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateScrollbarBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.thumb_color_rect_scrollbar.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateScrollbar3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarCurrentValue( main_window, value ):
    main_window.current_shape.current_value = value 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateScrollbarThumbSize( main_window, value ):
    main_window.current_shape.thumb_size = value 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------SLIDER--------------------------------------------------------------

def updateSliderActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderTag( main_window, value ):
    main_window.current_shape.tag = value
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_slider.value(), main_window.pos_y_spin_slider.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderSize( main_window, value ):
    main_window.current_shape.slider_width = main_window.width_spin_slider.value()
    main_window.current_shape.slider_height = main_window.height_spin_slider.value() 
    main_window.current_shape.setFixedSize( main_window.current_shape.slider_width, main_window.current_shape.slider_height )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def changeSliderThumbColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color_left )

    if color.isValid():
        main_window.current_shape.thumb_color = color
        main_window.thumb_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def changeSliderBackgroundLeftColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.thumb_color )

    if color.isValid():
        main_window.current_shape.background_color_left = color 
        main_window.bg_left_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def changeSliderBackgroundRightColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color_right )

    if color.isValid():
        main_window.current_shape.background_color_right = color 
        main_window.bg_right_color_rect_slider.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateSlider3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateSliderValue( main_window, value ):
    main_window.current_shape.value = value 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------PROGRESS BAR--------------------------------------------------------------

def updateProgressBarActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_progress_bar.value(), main_window.pos_y_spin_progress_bar.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarSize( main_window ):
    main_window.current_shape.progress_bar_width = main_window.width_spin_progress_bar.value()
    main_window.current_shape.progress_bar_height = main_window.height_spin_progress_bar.value() 
    main_window.current_shape.setFixedSize( main_window.current_shape.progress_bar_width, main_window.current_shape.progress_bar_height )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarProgressColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.progress_color )

    if color.isValid():
        main_window.current_shape.progress_color = color 
        main_window.progress_progress_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateProgressBarBackgroundColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.background_color )

    if color.isValid():
        main_window.current_shape.background_color = color 
        main_window.progress_background_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateProgressBar3D( main_window, state ):
    state == Qt.CheckState.Checked.value 
    main_window.current_shape.effect_3d = state 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarRange( main_window ):
    main_window.current_shape.range = main_window.progress_bar_range_spin.value()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateProgressBarValue( main_window ):
    main_window.current_shape.value = main_window.progress_bar_value_spin.value()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------IMAGE--------------------------------------------------------------

def updateImageActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateImageVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateImageStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateImageName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateImageStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateImagePosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_image.value(), main_window.pos_y_spin_image.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateImageSize( main_window ):
    main_window.current_shape.image_width = main_window.width_spin_image.value()
    main_window.current_shape.image_height = main_window.height_spin_image.value()
    main_window.current_shape.setFixedSize( main_window.current_shape.image_width, main_window.current_shape.image_height )
    main_window.current_shape.resizePixmap()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def selectImageFile( main_window ):
    file_path, _ = QFileDialog.getOpenFileName( main_window, "Select Image File", "", "Image Files (*.bmp *.png *.jpg *.jpeg *.jpe);;" "BMP Files (*.bmp);;" "PNG Files (*.png);;" "JPEG Files (*.jpg *.jpeg *.jpe);;" "All Files (*.*)" )

    if file_path:
        main_window.current_shape.setImagePath( file_path )
        main_window.current_shape.updateDataDict()

def updateImageFrameEnabled( main_window, state ):
        state == Qt.CheckState.Checked.value 
        main_window.current_shape.frame_enabled = state
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def changeImageFrameColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.frame_color )

    if color.isValid():
        main_window.current_shape.frame_color = color 
        main_window.frame_color_rect.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateImageFrameWidth( main_window, value ):
    main_window.current_shape.frame_width = value 
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------LABEL--------------------------------------------------------------

def updateLabelActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_label.value(), main_window.pos_y_spin_label.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelTextColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.text_color )

    if color.isValid():
        main_window.current_shape.text_color = color 
        main_window.text_color_rect_label.setStyleSheet( f"background-color: { color.name() }; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateLabelText( main_window, text ):
    main_window.current_shape.text = text 
    main_window.current_shape.setSizeBasedOnText()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelTextSize( main_window, value ):
    main_window.current_shape.text_size = value 
    main_window.current_shape.setSizeBasedOnText()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateLabelAlignment( main_window, text ):
    main_window.current_shape.text_alignment = text 
    main_window.current_shape.setSizeBasedOnText()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

#------------------------------------------------------------NUMERIC--------------------------------------------------------------

def updateNumericActive( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.active = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericVisible( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.visible = state
    main_window.current_shape.setVisible( state )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericStatic( main_window, state ):
    state == Qt.CheckState.Checked.value
    main_window.current_shape.static = state
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericName( main_window, text ):
    main_window.current_shape.custom_name = text
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericStackOrder( main_window, value ):
    main_window.current_shape.stack_order = value
    main_window.sortWidgetsByStackOrder()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericPosition( main_window ):
    main_window.current_shape.move( main_window.pos_x_spin_numeric.value(), main_window.pos_y_spin_numeric.value() )
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericNumberColor( main_window ):
    color = QColorDialog.getColor( main_window.current_shape.number_color )

    if color.isValid():
        main_window.current_shape.number_color = color 
        main_window.number_color_rect_numeric.setStyleSheet( f"background-color: {color.name()}; border: 1px solid #ccc;" )
        main_window.current_shape.update()
        main_window.current_shape.updateDataDict()

def updateNumericNumber( main_window, value ):
    main_window.current_shape.number = value 
    main_window.current_shape.setSizeBasedOnNumber()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericNumberSize( main_window, value ):
    main_window.current_shape.number_size = value 
    main_window.current_shape.setSizeBasedOnNumber()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

def updateNumericNumberAlignment( main_window, text ):
    main_window.current_shape.number_alignment = text 
    main_window.current_shape.setSizeBasedOnNumber()
    main_window.current_shape.update()
    main_window.current_shape.updateDataDict()

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
