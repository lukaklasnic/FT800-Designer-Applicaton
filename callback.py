# callback.py
from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QWidget, QSpinBox, QLineEdit, QColorDialog, QCheckBox, QComboBox, QFileDialog, QPushButton, QDialog, QVBoxLayout )
from PyQt6.QtGui import QCursor, QLinearGradient, QBrush, QColor
from PyQt6.QtCore import Qt
from widgets import  ( ColorRectangle, RectangleWidget, LineWidget, CircleWidget, KeysWidget, ButtonWidget, GaugeWidget, ClockWidget, ProgressBarWidget, ScrollBarWidget, DialWidget, SliderWidget, ToggleWidget, LabelWidget, ImageWidget, EllipseWidget, NumericWidget )

button_counter = 0  # Globalni brojač za button-e
_show_ellipse_warning = True

#----------------------------------------------------------------Button----------------------------------------------------------------

def updateButtonSize( main_window ):
    """Ažurira veličinu za ButtonWidget"""
    if hasattr( main_window, 'width_spin' ) and hasattr( main_window, 'height_spin' ):
        main_window.current_shape.setFixedSize( main_window.width_spin.value(), main_window.height_spin.value() )
        # Ažuriraj gradient kada se promeni veličina
        updateButtonGradient( main_window )
        main_window.current_shape.update_properties_dict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def showButtonProperties( main_window, current_index ):
    """Prikazuje properties za ButtonWidget"""
    
    # Ako button nema ime, generiši ga
    if not hasattr( main_window.current_shape, 'custom_name' ) or not main_window.current_shape.custom_name:
        # Pozovi metodu za generisanje imena ako postoji
        if hasattr( main_window, 'generate_button_name' ):
            main_window.current_shape.custom_name = main_window.generate_button_name()
        else:
            # Fallback: broji buttone
            button_count = 0
            for shape in main_window.all_shapes:
                if isinstance( shape, ButtonWidget ):
                    button_count += 1
            main_window.current_shape.custom_name = f"Button_{button_count}"
    
    # Status section
    status_label = QLabel( "Status" )
    status_label.setStyleSheet( "color: white; font-size: 12px; font-weight: bold; margin-top: 10px;" )
    main_window.properties_layout.insertWidget( current_index, status_label )
    current_index += 1
    
    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins( 20, 5, 10, 5 )
    active_label = QLabel( "Active:" )
    active_label.setStyleSheet( "color: white; font-size: 14px;" )
    active_layout.addWidget( active_label )
    active_layout.addStretch(1)
    main_window.active_checkbox = QCheckBox()
    main_window.active_checkbox.setChecked( True )
    main_window.active_checkbox.setStyleSheet( "QCheckBox::indicator { width: 15px; height: 15px; }" )
    active_layout.addWidget(main_window.active_checkbox)
    active_widget = QWidget()
    active_widget.setLayout( active_layout )
    main_window.properties_layout.insertWidget( current_index, active_widget )
    current_index += 1
    
    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins( 20, 5, 10, 5 )
    visible_label = QLabel( "Visible:" )
    visible_label.setStyleSheet( "color: white; font-size: 14px;" )
    visible_layout.addWidget( visible_label )
    visible_layout.addStretch( 1 )
    main_window.visible_checkbox = QCheckBox()
    main_window.visible_checkbox.setChecked( True )
    main_window.visible_checkbox.setStyleSheet( "QCheckBox::indicator { width: 15px; height: 15px; }" )
    visible_layout.addWidget( main_window.visible_checkbox )
    visible_widget = QWidget()
    visible_widget.setLayout( visible_layout )
    main_window.properties_layout.insertWidget( current_index, visible_widget )
    current_index += 1
    
    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins( 20, 5, 10, 5 )
    static_label = QLabel( "Static:" )
    static_label.setStyleSheet( "color: white; font-size: 14px;" )
    static_layout.addWidget( static_label )
    static_layout.addStretch( 1 )
    main_window.static_checkbox = QCheckBox()
    main_window.static_checkbox.setChecked( False )
    main_window.static_checkbox.setStyleSheet( "QCheckBox::indicator { width: 15px; height: 15px; }" )
    static_layout.addWidget( main_window.static_checkbox )
    static_widget = QWidget()
    static_widget.setLayout( static_layout )
    main_window.properties_layout.insertWidget( current_index, static_widget )
    current_index += 1
    
    # 2. BUTTON NAME SECTION
    name_label = QLabel( "Button name" )
    name_label.setStyleSheet( "color: white; font-size: 12px; font-weight: bold; margin-top: 10px;" )
    main_window.properties_layout.insertWidget( current_index, name_label )
    current_index += 1
    
    # Name input - PRIKAŽI VEĆ GENERISANO IME
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins( 20, 5, 10, 5 )
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet( "color: white; font-size: 14px;" )
    name_input_layout.addWidget( name_input_label )
    name_input_layout.addStretch( 1 )
    main_window.name_edit = QLineEdit()
    
    # OVO JE KLJUČNO: Postavi automatski generisano ime u QLineEdit
    main_window.name_edit.setText( main_window.current_shape.custom_name )
    
    main_window.name_edit.textChanged.connect( lambda text: updateButtonName( main_window, text ) )
    main_window.name_edit.setStyleSheet( "color: black; background-color: white;" )
    main_window.name_edit.setFixedWidth( 100 )
    name_input_layout.addWidget( main_window.name_edit )
    name_input_widget = QWidget()
    name_input_widget.setLayout( name_input_layout )
    main_window.properties_layout.insertWidget( current_index, name_input_widget )
    current_index += 1
    
    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin_button = QSpinBox()  # ← button specifično
    main_window.stack_order_spin_button.setRange(1, 100)
    main_window.stack_order_spin_button.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin_button.valueChanged.connect(
        lambda value: update_button_stack_order(main_window, value))
    main_window.stack_order_spin_button.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin_button.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin_button)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1


    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_button = QSpinBox()
    main_window.tag_spin_button.setRange(0, 255)
    main_window.tag_spin_button.setValue(main_window.current_shape.tag)
    main_window.tag_spin_button.valueChanged.connect(lambda value: update_button_tag(main_window, value))
    main_window.tag_spin_button.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_button.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_button)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1
    
    # 3. GEOMETRY SECTION
    geometry_label = QLabel( "Geometry" )
    geometry_label.setStyleSheet( "color: white; font-size: 12px; font-weight: bold; margin-top: 10px;" )
    main_window.properties_layout.insertWidget( current_index, geometry_label )
    current_index += 1
    
    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins( 20, 5, 10, 5 )
    pos_x_label = QLabel( "Position X:" )
    pos_x_label.setStyleSheet( "color: white; font-size: 14px;" )
    pos_x_layout.addWidget( pos_x_label )
    pos_x_layout.addStretch( 1 )
    main_window.pos_x_spin = QSpinBox()
    main_window.pos_x_spin.setRange( 0, 480 )
    main_window.pos_x_spin.setValue( main_window.current_shape.x() )
    main_window.pos_x_spin.valueChanged.connect( lambda value: updateButtonPosition( main_window ) )
    main_window.pos_x_spin.setStyleSheet( "color: black; background-color: white;" )
    main_window.pos_x_spin.setFixedWidth( 60 )
    pos_x_layout.addWidget( main_window.pos_x_spin )
    pos_x_widget = QWidget()
    pos_x_widget.setLayout( pos_x_layout )
    main_window.properties_layout.insertWidget( current_index, pos_x_widget )
    current_index += 1
    
    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins( 20, 5, 10, 5 )
    pos_y_label = QLabel( "Position Y:" )
    pos_y_label.setStyleSheet( "color: white; font-size: 14px;" )
    pos_y_layout.addWidget( pos_y_label )
    pos_y_layout.addStretch( 1 )
    main_window.pos_y_spin = QSpinBox()
    main_window.pos_y_spin.setRange( 0, 272 )
    main_window.pos_y_spin.setValue( main_window.current_shape.y() )
    main_window.pos_y_spin.valueChanged.connect( lambda value: updateButtonPosition( main_window ) )
    main_window.pos_y_spin.setStyleSheet( "color: black; background-color: white;" )
    main_window.pos_y_spin.setFixedWidth( 60 )
    pos_y_layout.addWidget( main_window.pos_y_spin )
    pos_y_widget = QWidget()
    pos_y_widget.setLayout( pos_y_layout )
    main_window.properties_layout.insertWidget( current_index, pos_y_widget )
    current_index += 1
    
    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins( 20, 5, 10, 5 )
    width_label = QLabel( "Width:" )
    width_label.setStyleSheet( "color: white; font-size: 14px;" )
    width_layout.addWidget( width_label )
    width_layout.addStretch( 1 )
    main_window.width_spin = QSpinBox()
    main_window.width_spin.setRange( 10, 480 )
    main_window.width_spin.setValue( main_window.current_shape.width() )
    main_window.width_spin.valueChanged.connect( lambda value: updateButtonSize( main_window ) )
    main_window.width_spin.setStyleSheet( "color: black; background-color: white;" )
    main_window.width_spin.setFixedWidth( 60 )
    width_layout.addWidget( main_window.width_spin )
    width_widget = QWidget()
    width_widget.setLayout( width_layout )
    main_window.properties_layout.insertWidget( current_index, width_widget )
    current_index += 1
    
    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins( 20, 5, 10, 5 )
    height_label = QLabel( "Height:" )
    height_label.setStyleSheet( "color: white; font-size: 14px;" )
    height_layout.addWidget( height_label )
    height_layout.addStretch( 1 )
    main_window.height_spin = QSpinBox()
    main_window.height_spin.setRange( 10, 272 )
    main_window.height_spin.setValue( main_window.current_shape.height() )
    main_window.height_spin.valueChanged.connect( lambda value: updateButtonSize( main_window ) )
    main_window.height_spin.setStyleSheet( "color: black; background-color: white;" )
    main_window.height_spin.setFixedWidth( 60 )
    height_layout.addWidget( main_window.height_spin )
    height_widget = QWidget()
    height_widget.setLayout( height_layout )
    main_window.properties_layout.insertWidget( current_index, height_widget )
    current_index += 1
    
    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel( "Color Adjust" )
    color_adjust_label.setStyleSheet( "color: white; font-size: 12px; font-weight: bold; margin-top: 10px;" )
    main_window.properties_layout.insertWidget( current_index, color_adjust_label )
    current_index += 1
    
    # Start Color
    start_color_layout = QHBoxLayout()
    start_color_layout.setContentsMargins( 20, 5, 10, 5 )
    start_color_label = QLabel( "Start color:" )
    start_color_label.setStyleSheet( "color: white; font-size: 14px;" )
    start_color_layout.addWidget( start_color_label )
    start_color_layout.addStretch( 1 )
    main_window.start_color_rect = ColorRectangle( "#0000FF" )
    
    # OVO JE KLJUČNO: Postavi boju iz dugmeta, ne fiksnu plavu!
    if hasattr( main_window.current_shape, 'start_color' ):
        button_start_color = main_window.current_shape.start_color
        main_window.start_color_rect.setStyleSheet( f"background-color: {button_start_color.name()}; border: 1px solid #ccc;" )
    
    main_window.start_color_rect.mousePressEvent = lambda e: changeStartColor( main_window )
    main_window.start_color_rect.setCursor( Qt.CursorShape.PointingHandCursor )
    start_color_layout.addWidget( main_window.start_color_rect )
    start_color_widget = QWidget()
    start_color_widget.setLayout( start_color_layout )
    main_window.properties_layout.insertWidget( current_index, start_color_widget )
    current_index += 1
    
    # End Color
    end_color_layout = QHBoxLayout()
    end_color_layout.setContentsMargins( 20, 5, 10, 5 )
    end_color_label = QLabel( "End color:" )
    end_color_label.setStyleSheet( "color: white; font-size: 14px;" )
    end_color_layout.addWidget( end_color_label )
    end_color_layout.addStretch( 1 )
    main_window.end_color_rect = ColorRectangle( "#000088" )
    
    # OVO JE KLJUČNO: Postavi boju iz dugmeta, ne fiksnu plavu!
    if hasattr(main_window.current_shape, 'end_color'):
        button_end_color = main_window.current_shape.end_color
        main_window.end_color_rect.setStyleSheet( f"background-color: {button_end_color.name()}; border: 1px solid #ccc;" )
    
    main_window.end_color_rect.mousePressEvent = lambda e: changeEndColor( main_window )
    main_window.end_color_rect.setCursor( Qt.CursorShape.PointingHandCursor )
    end_color_layout.addWidget( main_window.end_color_rect )
    end_color_widget = QWidget()
    end_color_widget.setLayout( end_color_layout )
    main_window.properties_layout.insertWidget( current_index, end_color_widget )
    current_index += 1
    
    # 3D checkbox
    threed_layout = QHBoxLayout()
    threed_layout.setContentsMargins(20, 5, 10, 5)
    threed_label = QLabel("3D:")
    threed_label.setStyleSheet("color: white; font-size: 14px;")
    threed_layout.addWidget(threed_label)
    threed_layout.addStretch(1)
    main_window.threed_checkbox = QCheckBox()
    main_window.threed_checkbox.setChecked(main_window.current_shape.use_3d)  # OVO JE KLJUČNO
    main_window.threed_checkbox.stateChanged.connect(lambda state: toggle3dEffect(main_window, state))
    main_window.threed_checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    threed_layout.addWidget(main_window.threed_checkbox)
    threed_widget = QWidget()
    threed_widget.setLayout(threed_layout)
    main_window.properties_layout.insertWidget(current_index, threed_widget)
    current_index += 1
    
    # 5. TEXT SECTION
    text_label = QLabel( "Text" )
    text_label.setStyleSheet( "color: white; font-size: 12px; font-weight: bold; margin-top: 10px;" )
    main_window.properties_layout.insertWidget( current_index, text_label )
    current_index += 1
    
    # Button Text
    text_layout = QHBoxLayout()
    text_layout.setContentsMargins( 20, 5, 10, 5 )
    text_input_label = QLabel( "Text:" )
    text_input_label.setStyleSheet( "color: white; font-size: 14px;" )
    text_layout.addWidget( text_input_label )
    text_layout.addStretch( 1 )
    main_window.text_edit = QLineEdit()
    main_window.text_edit.setText( main_window.current_shape.button_text )
    main_window.text_edit.textChanged.connect( lambda text: updateButtonText( main_window, text ) )
    main_window.text_edit.setStyleSheet( "color: black; background-color: white;" )
    main_window.text_edit.setFixedWidth( 100 )
    text_layout.addWidget( main_window.text_edit )
    text_widget = QWidget()
    text_widget.setLayout( text_layout )
    main_window.properties_layout.insertWidget( current_index, text_widget )
    current_index += 1
    
    # Text Size
    text_size_layout = QHBoxLayout()
    text_size_layout.setContentsMargins( 20, 5, 10, 5 )
    text_size_label = QLabel( "Text size:" )
    text_size_label.setStyleSheet( "color: white; font-size: 14px;" )
    text_size_layout.addWidget( text_size_label )
    text_size_layout.addStretch( 1 )
    main_window.text_size_spin = QSpinBox()
    main_window.text_size_spin.setRange( 1, 6 )
    main_window.text_size_spin.setValue( main_window.current_shape.text_size )
    main_window.text_size_spin.valueChanged.connect( lambda value: updateButtonTextSize( main_window, value ) )
    main_window.text_size_spin.setStyleSheet( "color: black; background-color: white;" )
    main_window.text_size_spin.setFixedWidth( 60 ) 
    text_size_layout.addWidget( main_window.text_size_spin )
    text_size_widget = QWidget()
    text_size_widget.setLayout( text_size_layout )
    main_window.properties_layout.insertWidget( current_index, text_size_widget )
    current_index += 1
    
    # Text Color
    text_color_layout = QHBoxLayout()
    text_color_layout.setContentsMargins( 20, 5, 10, 5 )
    text_color_label = QLabel( "Text color:" )
    text_color_label.setStyleSheet( "color: white; font-size: 14px;" )
    text_color_layout.addWidget( text_color_label )
    text_color_layout.addStretch( 1 )
    main_window.text_color_rect = ColorRectangle( main_window.current_shape.text_color.name() )
    main_window.text_color_rect.mousePressEvent = lambda e: changeButtonTextColor( main_window )
    main_window.text_color_rect.setCursor( Qt.CursorShape.PointingHandCursor )
    text_color_layout.addWidget( main_window.text_color_rect )
    text_color_widget = QWidget()
    text_color_widget.setLayout( text_color_layout )
    main_window.properties_layout.insertWidget( current_index, text_color_widget )
    current_index += 1
    
    # Postavi početne boje za gradient
    if not hasattr( main_window.current_shape, 'start_color' ):
        main_window.current_shape.start_color = QColor( "#0000FF")
    if not hasattr( main_window.current_shape, 'end_color' ):
        main_window.current_shape.end_color = QColor( "#000088" )
    if not hasattr( main_window.current_shape, 'use_3d' ):
        main_window.current_shape.use_3d = False
    
    # Ažuriraj gradient
    updateButtonGradient( main_window )
    
    return current_index

def update_button_tag(main_window, value):
    """Ažurira tag vrednost za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, ButtonWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_button_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, ButtonWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()


# Dodajte ovu funkciju u callback.py
def updateButtonPosition( main_window ):
    """Ažurira poziciju Button-a"""
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        if hasattr( main_window, 'pos_x_spin' ) and hasattr( main_window, 'pos_y_spin' ):
            main_window.current_shape.move( main_window.pos_x_spin.value(), main_window.pos_y_spin.value() )
            main_window.current_shape.update_properties_dict()
            
            # Ažuriraj globalni rečnik
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()


def updateButtonGradient( main_window ):
    """Ažurira gradient za button"""
    if hasattr( main_window.current_shape, 'start_color' ) and hasattr( main_window.current_shape, 'end_color' ):
        gradient = QLinearGradient( 0, 0, 0, main_window.current_shape.height() )
        gradient.setColorAt( 0, main_window.current_shape.start_color )
        gradient.setColorAt( 1, main_window.current_shape.end_color )
        main_window.current_shape.set_bg_gradient( gradient )
        main_window.current_shape.update()
        main_window.current_shape.update_properties_dict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

def changeStartColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        current_color = main_window.current_shape.start_color if hasattr( main_window.current_shape, 'start_color' ) else QColor( "#0000FF" )
        color = QColorDialog.getColor( current_color )
        if color.isValid():
            main_window.current_shape.start_color = color
            main_window.start_color_rect.setStyleSheet( f"background-color: {color.name()}; border: 1px solid #ccc;" )
            updateButtonGradient( main_window )
            main_window.current_shape.update_properties_dict()
        
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

def changeEndColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        current_color = main_window.current_shape.end_color if hasattr( main_window.current_shape, 'end_color') else QColor( "#000088" )
        color = QColorDialog.getColor( current_color )
        if color.isValid():
            main_window.current_shape.end_color = color
            main_window.end_color_rect.setStyleSheet( f"background-color: {color.name()}; border: 1px solid #ccc;" )
            updateButtonGradient( main_window )
            main_window.current_shape.update_properties_dict()
        
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

def toggle3dEffect( main_window, state ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.use_3d = ( state == Qt.CheckState.Checked.value )
        main_window.current_shape.update()
        main_window.current_shape.update_properties_dict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

def updateButtonName( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.custom_name = text
        if hasattr( main_window, 'all_button_dicts' ):
            # Proveri da li postoji stari ključ
            for shape in main_window.all_shapes:
                if shape == main_window.current_shape and hasattr( shape, 'custom_name' ):
                    # Ažuriraj rečnik
                    shape.update_properties_dict()
                    main_window.all_button_dicts[ text ] = shape.get_properties_dict()

def updateStackOrder( main_window, value ):
        main_window.current_shape.update_properties_dict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()
    

def updateButtonText( main_window, text ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.set_button_text( text )
        main_window.current_shape.update_properties_dict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

def updateButtonTextSize(main_window, value):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        main_window.current_shape.set_text_size( value )
        main_window.current_shape.update_properties_dict()
        
        if hasattr( main_window, 'all_button_dicts' ):
            main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

def changeButtonTextColor( main_window ):
    if main_window.current_shape and isinstance( main_window.current_shape, ButtonWidget ):
        color = QColorDialog.getColor( main_window.current_shape.text_color )
        if color.isValid():
            main_window.current_shape.set_text_color( color )
            main_window.text_color_rect.setStyleSheet( f"background-color: {color.name()}; border: 1px solid #ccc;" )
            main_window.current_shape.update_properties_dict()
        
            if hasattr( main_window, 'all_button_dicts' ):
                main_window.all_button_dicts[ main_window.current_shape.custom_name ] = main_window.current_shape.get_properties_dict()

#----------------------------------------------------------------LINE----------------------------------------------------------------

def showLineProperties(main_window, current_index):
    """Prikazuje properties za LineWidget - SAMO TAČKE LINIJE"""
    # Ako line nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Line")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_line = QCheckBox()
    main_window.active_checkbox_line.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_line.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_line.stateChanged.connect(lambda state: update_line_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_line)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_line = QCheckBox()
    main_window.visible_checkbox_line.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_line.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_line.stateChanged.connect(lambda state: update_line_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_line)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_line = QCheckBox()
    main_window.static_checkbox_line.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_line.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_line.stateChanged.connect(lambda state: update_line_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_line)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. LINE NAME SECTION
    name_label = QLabel("Line Name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_line = QLineEdit()
    main_window.name_edit_line.setText(main_window.current_shape.custom_name)
    main_window.name_edit_line.textChanged.connect(lambda text: update_line_name(main_window, text))
    main_window.name_edit_line.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_line.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_line)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin_line = QSpinBox()  # ← button specifično
    main_window.stack_order_spin_line.setRange(1, 100)
    main_window.stack_order_spin_line.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin_line.valueChanged.connect(
        lambda value: update_line_stack_order(main_window, value))
    main_window.stack_order_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin_line.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin_line)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1


    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_line = QSpinBox()
    main_window.tag_spin_line.setRange(0, 255)
    main_window.tag_spin_line.setValue(main_window.current_shape.tag)
    main_window.tag_spin_line.valueChanged.connect(lambda value: update_line_tag(main_window, value))
    main_window.tag_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_line.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_line)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1
    

    # 3. GEOMETRY SECTION (samo tačke)
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Start Position X
    start_x_layout = QHBoxLayout()
    start_x_layout.setContentsMargins(20, 5, 10, 5)
    start_x_label = QLabel("Start position X:")
    start_x_label.setStyleSheet("color: white; font-size: 14px;")
    start_x_layout.addWidget(start_x_label)
    start_x_layout.addStretch(1)
    main_window.start_x_spin_line = QSpinBox()
    main_window.start_x_spin_line.setRange(0, 480)
    start_x, start_y, end_x, end_y = main_window.current_shape.get_line_points()
    main_window.start_x_spin_line.setValue(start_x)
    main_window.start_x_spin_line.valueChanged.connect(lambda value: update_line_points(main_window))
    main_window.start_x_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.start_x_spin_line.setFixedWidth(60)
    start_x_layout.addWidget(main_window.start_x_spin_line)
    start_x_widget = QWidget()
    start_x_widget.setLayout(start_x_layout)
    main_window.properties_layout.insertWidget(current_index, start_x_widget)
    current_index += 1

    # Start Position Y
    start_y_layout = QHBoxLayout()
    start_y_layout.setContentsMargins(20, 5, 10, 5)
    start_y_label = QLabel("Start position Y:")
    start_y_label.setStyleSheet("color: white; font-size: 14px;")
    start_y_layout.addWidget(start_y_label)
    start_y_layout.addStretch(1)
    main_window.start_y_spin_line = QSpinBox()
    main_window.start_y_spin_line.setRange(0, 272)
    main_window.start_y_spin_line.setValue(start_y)
    main_window.start_y_spin_line.valueChanged.connect(lambda value: update_line_points(main_window))
    main_window.start_y_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.start_y_spin_line.setFixedWidth(60)
    start_y_layout.addWidget(main_window.start_y_spin_line)
    start_y_widget = QWidget()
    start_y_widget.setLayout(start_y_layout)
    main_window.properties_layout.insertWidget(current_index, start_y_widget)
    current_index += 1

    # End Position X
    end_x_layout = QHBoxLayout()
    end_x_layout.setContentsMargins(20, 5, 10, 5)
    end_x_label = QLabel("End position X:")
    end_x_label.setStyleSheet("color: white; font-size: 14px;")
    end_x_layout.addWidget(end_x_label)
    end_x_layout.addStretch(1)
    main_window.end_x_spin_line = QSpinBox()
    main_window.end_x_spin_line.setRange(0, 480)
    main_window.end_x_spin_line.setValue(end_x)
    main_window.end_x_spin_line.valueChanged.connect(lambda value: update_line_points(main_window))
    main_window.end_x_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.end_x_spin_line.setFixedWidth(60)
    end_x_layout.addWidget(main_window.end_x_spin_line)
    end_x_widget = QWidget()
    end_x_widget.setLayout(end_x_layout)
    main_window.properties_layout.insertWidget(current_index, end_x_widget)
    current_index += 1

    # End Position Y
    end_y_layout = QHBoxLayout()
    end_y_layout.setContentsMargins(20, 5, 10, 5)
    end_y_label = QLabel("End position Y:")
    end_y_label.setStyleSheet("color: white; font-size: 14px;")
    end_y_layout.addWidget(end_y_label)
    end_y_layout.addStretch(1)
    main_window.end_y_spin_line = QSpinBox()
    main_window.end_y_spin_line.setRange(0, 272)
    main_window.end_y_spin_line.setValue(end_y)
    main_window.end_y_spin_line.valueChanged.connect(lambda value: update_line_points(main_window))
    main_window.end_y_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.end_y_spin_line.setFixedWidth(60)
    end_y_layout.addWidget(main_window.end_y_spin_line)
    end_y_widget = QWidget()
    end_y_widget.setLayout(end_y_layout)
    main_window.properties_layout.insertWidget(current_index, end_y_widget)
    current_index += 1

    # 4. COLOR SECTION
    color_label = QLabel("Color")
    color_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_label)
    current_index += 1

    # Color picker
    color_layout = QHBoxLayout()
    color_layout.setContentsMargins(20, 5, 10, 5)
    color_picker_label = QLabel("Color:")
    color_picker_label.setStyleSheet("color: white; font-size: 14px;")
    color_layout.addWidget(color_picker_label)
    color_layout.addStretch(1)
    main_window.color_rect_line = ColorRectangle(main_window.current_shape.line_color.name())
    main_window.color_rect_line.mousePressEvent = lambda e: change_line_color(main_window)
    color_layout.addWidget(main_window.color_rect_line)
    color_widget = QWidget()
    color_widget.setLayout(color_layout)
    main_window.properties_layout.insertWidget(current_index, color_widget)
    current_index += 1

    # Line Width (debljina linije)
    line_width_layout = QHBoxLayout()
    line_width_layout.setContentsMargins(20, 5, 10, 5)
    line_width_label = QLabel("Line Width:")
    line_width_label.setStyleSheet("color: white; font-size: 14px;")
    line_width_layout.addWidget(line_width_label)
    line_width_layout.addStretch(1)
    main_window.line_width_spin_line = QSpinBox()
    main_window.line_width_spin_line.setRange(1, 50)
    main_window.line_width_spin_line.setValue(main_window.current_shape.line_width)
    main_window.line_width_spin_line.valueChanged.connect(lambda value: update_line_thickness(main_window, value))
    main_window.line_width_spin_line.setStyleSheet("color: black; background-color: white;")
    main_window.line_width_spin_line.setFixedWidth(60)
    line_width_layout.addWidget(main_window.line_width_spin_line)
    line_width_widget = QWidget()
    line_width_widget.setLayout(line_width_layout)
    main_window.properties_layout.insertWidget(current_index, line_width_widget)
    current_index += 1

    return current_index
# CALLBACK METODE ZA LINE (konzistentne sa drugim widget-ima):


def update_line_tag(main_window, value):
    """Ažurira tag vrednost za line"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_line_active(main_window, state):
    """Ažurira active status za line"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = active
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_line_visible(main_window, state):
    """Ažurira visible status za line"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(visible)
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_line_static(main_window, state):
    """Ažurira static status za line"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = static
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_line_name(main_window, text):
    """Ažurira ime line-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        main_window.current_shape.custom_name = text
        if hasattr(main_window, 'all_line_dicts'):
            old_name = None
            for name, props in list(main_window.all_line_dicts.items()):
                if (props.get('start_x') == main_window.current_shape.get_line_points()[0] and 
                    props.get('start_y') == main_window.current_shape.get_line_points()[1]):
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_line_dicts[text] = main_window.all_line_dicts.pop(old_name)
            else:
                main_window.all_line_dicts[text] = main_window.current_shape.get_properties_dict()

def update_line_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_line_points(main_window):
    """Ažurira pozicije tačaka linije"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        if (hasattr(main_window, 'start_x_spin_line') and 
            hasattr(main_window, 'start_y_spin_line') and 
            hasattr(main_window, 'end_x_spin_line') and 
            hasattr(main_window, 'end_y_spin_line')):
            
            start_x = main_window.start_x_spin_line.value()
            start_y = main_window.start_y_spin_line.value()
            end_x = main_window.end_x_spin_line.value()
            end_y = main_window.end_y_spin_line.value()
            
            main_window.current_shape.set_line_points(start_x, start_y, end_x, end_y)
            
            if hasattr(main_window, 'all_line_dicts'):
                main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()


def change_line_color(main_window):
    """Menja boju linije"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        color = QColorDialog.getColor(main_window.current_shape.line_color)
        if color.isValid():
            main_window.current_shape.set_line_color(color)
            main_window.color_rect_line.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_line_dicts'):
                main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_line_thickness(main_window, value):
    """Ažurira debljinu linije"""
    if main_window.current_shape and isinstance(main_window.current_shape, LineWidget):
        main_window.current_shape.set_line_width(value)
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_position_spins(main_window):
    """Ažurira spinbox-ove za poziciju"""
    if main_window.current_shape and hasattr(main_window, 'pos_x_spin') and hasattr(main_window, 'pos_y_spin'):
        main_window.pos_x_spin.blockSignals(True)
        main_window.pos_y_spin.blockSignals(True)
        main_window.pos_x_spin.setValue(main_window.current_shape.x())
        main_window.pos_y_spin.setValue(main_window.current_shape.y())
        main_window.pos_x_spin.blockSignals(False)
        main_window.pos_y_spin.blockSignals(False)
        if hasattr(main_window, 'all_line_dicts'):
            main_window.all_line_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

#----------------------------------------------------------------CIRCLE----------------------------------------------------------------

def showCircleProperties(main_window, current_index):
    """Prikazuje properties za CircleWidget - konzistentno sa Button i Line"""
    # Ako circle nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Circle")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_circle = QCheckBox()
    main_window.active_checkbox_circle.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_circle.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_circle.stateChanged.connect(lambda state: update_circle_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_circle)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_circle = QCheckBox()
    main_window.visible_checkbox_circle.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_circle.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_circle.stateChanged.connect(lambda state: update_circle_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_circle)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_circle = QCheckBox()
    main_window.static_checkbox_circle.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_circle.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_circle.stateChanged.connect(lambda state: update_circle_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_circle)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. CIRCLE NAME SECTION
    name_label = QLabel("Circle name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_circle = QLineEdit()
    main_window.name_edit_circle.setText(main_window.current_shape.custom_name)
    main_window.name_edit_circle.textChanged.connect(lambda text: update_circle_name(main_window, text))
    main_window.name_edit_circle.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_circle.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_circle)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    main_window.stack_order_spin_circle = QSpinBox()
    main_window.stack_order_spin_circle.setRange(1, 100)
    main_window.stack_order_spin_circle.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin_circle.valueChanged.connect(lambda value: update_circle_stack_order(main_window, value))
    main_window.stack_order_spin_circle.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin_circle.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin_circle)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_circle = QSpinBox()
    main_window.tag_spin_circle.setRange(0, 255)
    main_window.tag_spin_circle.setValue(main_window.current_shape.tag)
    main_window.tag_spin_circle.valueChanged.connect(lambda value: update_circle_tag(main_window, value))
    main_window.tag_spin_circle.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_circle.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_circle)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1


    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X (centar)
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_circle = QSpinBox()
    main_window.pos_x_spin_circle.setRange(0, 480)
    main_window.pos_x_spin_circle.setValue(main_window.current_shape.center_x)
    main_window.pos_x_spin_circle.valueChanged.connect(lambda value: update_circle_position(main_window))
    main_window.pos_x_spin_circle.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_circle.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_circle)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y (centar)
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_circle  = QSpinBox()
    main_window.pos_y_spin_circle.setRange(0, 272)
    main_window.pos_y_spin_circle.setValue(main_window.current_shape.center_y)
    main_window.pos_y_spin_circle.valueChanged.connect(lambda value: update_circle_position(main_window))
    main_window.pos_y_spin_circle.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_circle.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_circle)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Diameter
    diameter_layout = QHBoxLayout()
    diameter_layout.setContentsMargins(20, 5, 10, 5)
    diameter_label = QLabel("Diameter:")
    diameter_label.setStyleSheet("color: white; font-size: 14px;")
    diameter_layout.addWidget(diameter_label)
    diameter_layout.addStretch(1)
    main_window.diameter_spin_circle = QSpinBox()
    main_window.diameter_spin_circle.setRange(10, 480)
    main_window.diameter_spin_circle.setValue(main_window.current_shape.diameter)
    main_window.diameter_spin_circle.valueChanged.connect(lambda value: updateCircleSize(main_window))
    main_window.diameter_spin_circle.setStyleSheet("color: black; background-color: white;")
    main_window.diameter_spin_circle.setFixedWidth(60)
    diameter_layout.addWidget(main_window.diameter_spin_circle)
    diameter_widget = QWidget()
    diameter_widget.setLayout(diameter_layout)
    main_window.properties_layout.insertWidget(current_index, diameter_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Edges color
    edges_color_layout = QHBoxLayout()
    edges_color_layout.setContentsMargins(20, 5, 10, 5)
    edges_color_label = QLabel("Edges color:")
    edges_color_label.setStyleSheet("color: white; font-size: 14px;")
    edges_color_layout.addWidget(edges_color_label)
    edges_color_layout.addStretch(1)

    # Koristi boju iz circle-a
    if hasattr(main_window.current_shape, 'line_color'):
        line_color_hex = main_window.current_shape.line_color.name()
    else:
        line_color_hex = "#FF0000"

    main_window.edges_color_rect_circle = ColorRectangle(line_color_hex)
    main_window.edges_color_rect_circle.mousePressEvent = lambda e: change_circle_line_color(main_window)
    main_window.edges_color_rect_circle.setCursor(Qt.CursorShape.PointingHandCursor)
    edges_color_layout.addWidget(main_window.edges_color_rect_circle)

    edges_color_widget = QWidget()
    edges_color_widget.setLayout(edges_color_layout)
    main_window.properties_layout.insertWidget(current_index, edges_color_widget)
    current_index += 1

    # Thickness
    thickness_layout = QHBoxLayout()
    thickness_layout.setContentsMargins(20, 5, 10, 5)
    thickness_label = QLabel("Thickness:")
    thickness_label.setStyleSheet("color: white; font-size: 14px;")
    thickness_layout.addWidget(thickness_label)
    thickness_layout.addStretch(1)
    main_window.thickness_spin_circle = QSpinBox()
    main_window.thickness_spin_circle.setRange(1, 50)
    main_window.thickness_spin_circle.setValue(main_window.current_shape.line_thickness)
    main_window.thickness_spin_circle.valueChanged.connect(lambda value: update_circle_thickness(main_window, value))
    main_window.thickness_spin_circle.setStyleSheet("color: black; background-color: white;")
    main_window.thickness_spin_circle.setFixedWidth(60)
    thickness_layout.addWidget(main_window.thickness_spin_circle)
    thickness_widget = QWidget()
    thickness_widget.setLayout(thickness_layout)
    main_window.properties_layout.insertWidget(current_index, thickness_widget)
    current_index += 1

    # Filled checkbox
    filled_layout = QHBoxLayout()
    filled_layout.setContentsMargins(20, 5, 10, 5)
    filled_label = QLabel("Filled:")
    filled_label.setStyleSheet("color: white; font-size: 14px;")
    filled_layout.addWidget(filled_label)
    filled_layout.addStretch(1)

    main_window.filled_checkbox_circle = QCheckBox()

    # IZMENJENO: Proverava self.filled umesto fill_color.alpha() > 0
    if hasattr(main_window.current_shape, 'filled'):
        is_filled = main_window.current_shape.filled  # BOOLEAN atribut
    else:
        is_filled = False  # Podrazumevano nije checkiran

    main_window.filled_checkbox_circle.setChecked(is_filled)
    main_window.filled_checkbox_circle.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.filled_checkbox_circle.stateChanged.connect(lambda state: update_circle_filled(main_window, state))
    filled_layout.addWidget(main_window.filled_checkbox_circle)
    filled_widget = QWidget()
    filled_widget.setLayout(filled_layout)
    main_window.properties_layout.insertWidget(current_index, filled_widget)
    current_index += 1

    # Fill Color - UVIJEK PRIKAZAN
    fill_color_layout = QHBoxLayout()
    fill_color_layout.setContentsMargins(20, 5, 10, 5)
    fill_color_label = QLabel("Fill color:")
    fill_color_label.setStyleSheet("color: white; font-size: 14px;")
    fill_color_layout.addWidget(fill_color_label)
    fill_color_layout.addStretch(1)
    
    # UVIJEK koristite ColorRectangle
    if hasattr(main_window.current_shape, 'fill_color'):
        fill_color_hex = main_window.current_shape.fill_color.name()
    else:
        fill_color_hex = "#FFFFFF"
    
    main_window.fill_color_rect_circle = ColorRectangle(fill_color_hex)
    main_window.fill_color_rect_circle.mousePressEvent = lambda e: change_circle_fill_color(main_window)
    
    # Postavite kursor
    main_window.fill_color_rect_circle.setCursor(Qt.CursorShape.PointingHandCursor)
    
    fill_color_layout.addWidget(main_window.fill_color_rect_circle)
    fill_color_widget = QWidget()
    fill_color_widget.setLayout(fill_color_layout)
    main_window.properties_layout.insertWidget(current_index, fill_color_widget)
    current_index += 1

    # Postavite inicijalno stanje boje
    update_circle_fill_color_appearance(main_window)

    return current_index

# CALLBACK METODE ZA CIRCLE:

def update_circle_tag(main_window, value):
    """Ažurira tag vrednost za circle"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_active(main_window, state):
    """Ažurira active status za circle"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.set_active(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_visible(main_window, state):
    """Ažurira visible status za circle"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.set_visible(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_static(main_window, state):
    """Ažurira static status za circle"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.set_static(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_name(main_window, text):
    """Ažurira ime circle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.set_custom_name(text)
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_stack_order(main_window, value):
    """Ažurira stack order za circle i sortira widget-e"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_circle_position(main_window):
    """Ažurira poziciju centra circle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        if hasattr(main_window, 'pos_x_spin_circle') and hasattr(main_window, 'pos_y_spin_circle'):
            center_x = main_window.pos_x_spin_circle.value()
            center_y = main_window.pos_y_spin_circle.value()
            
            # Izračunaj gornji levi ugao na osnovu centra i dijametra
            x = center_x - main_window.current_shape.diameter // 2
            y = center_y - main_window.current_shape.diameter // 2
            
            main_window.current_shape.move(x, y)
            main_window.current_shape.update_center_position()
            
            if hasattr(main_window, 'all_circle_dicts'):
                main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateCircleSize(main_window):
    """Ažurira veličinu circle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        if hasattr(main_window, 'diameter_spin_circle'):
            diameter = main_window.diameter_spin_circle.value()
            main_window.current_shape.set_diameter(diameter)
            
            # Ažuriraj poziciju centra
            if hasattr(main_window, 'pos_x_spin_circle') and hasattr(main_window, 'pos_y_spin_circle'):
                main_window.pos_x_spin_circle.blockSignals(True)
                main_window.pos_y_spin_circle.blockSignals(True)
                main_window.pos_x_spin_circle.setValue(main_window.current_shape.center_x)
                main_window.pos_y_spin_circle.setValue(main_window.current_shape.center_y)
                main_window.pos_x_spin_circle.blockSignals(False)
                main_window.pos_y_spin_circle.blockSignals(False)
            
            if hasattr(main_window, 'all_circle_dicts'):
                main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_circle_line_color(main_window):
    """Menja boju ivice circle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        current_color = main_window.current_shape.line_color
        color = QColorDialog.getColor(current_color)
        if color.isValid():
            main_window.current_shape.set_color(color)
            main_window.edges_color_rect_circle.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_circle_dicts'):
                main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_thickness(main_window, value):
    """Ažurira debljinu ivice circle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.set_line_thickness(value)
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_filled(main_window, state):
    """Ažurira filled property za CircleWidget - samo boolean"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        filled = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_filled(filled)  # SAMO SETUJE BOOLEAN
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()
def update_circle_fill_color_appearance(main_window):
    """Ažurira izgled Fill Color rectangle-a na osnovu stanja"""
    if not hasattr(main_window, 'current_shape') or not main_window.current_shape:
        return
    
    if hasattr(main_window, 'fill_color_rect_circle'):
#        if hasattr(main_window, 'filled_checkbox_circle'):
#            filled = main_window.filled_checkbox_circle.isChecked()
#        else:
#            filled = getattr(main_window.current_shape, 'filled', False)
        
        #if filled:
            # Kada je filled, prikaži punu boju i omogući promenu
        main_window.fill_color_rect_circle.setStyleSheet(
            f"background-color: {main_window.current_shape.fill_color.name()}; "
            f"border: 1px solid #ccc;"
        )
        main_window.fill_color_rect_circle.setCursor(Qt.CursorShape.PointingHandCursor)
            #main_window.fill_color_rect_circle.setToolTip("Click to change fill color")
        #else:
            # Kada nije filled, prikaži sivu boju i onemogući
            #main_window.fill_color_rect_circle.setStyleSheet(
            #    "background-color: #cccccc; "
            #    "border: 1px solid #999999;"
            #)
            #main_window.fill_color_rect_circle.setCursor(Qt.CursorShape.ForbiddenCursor)
            #main_window.fill_color_rect_circle.setToolTip("Check 'Filled' to enable fill color")

def change_circle_fill_color(main_window):
    """Menja boju popune circle-a - samo ako je Filled checkiran"""
    current_color = main_window.current_shape.fill_color
        
    color = QColorDialog.getColor(current_color)
    if not main_window.current_shape:
        return
    
    # Proveri da li je Filled checkiran
    if hasattr(main_window, 'filled_checkbox_circle'):
        if not main_window.filled_checkbox_circle.isChecked():
            # Ako nije checkiran, ne dozvoli promenu boje
            return
    
    if isinstance(main_window.current_shape, CircleWidget):

        if color.isValid():
            # BEZ ALPHA KANALA - samo RGB
            main_window.current_shape.set_fill_color(color)
            
            # Ažuriraj izgled ColorRectangle-a
            if hasattr(main_window, 'fill_color_rect_circle'):
                main_window.fill_color_rect_circle.setStyleSheet(
                    f"background-color: {color.name()}; "
                    f"border: 1px solid #ccc;"
                )
            
            # Ažuriraj rečnik
            if hasattr(main_window, 'all_circle_dicts'):
                main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_circle_stack_order(main_window, value):
    """Ažurira stack order za circle i sortira widget-e"""
    if main_window.current_shape and isinstance(main_window.current_shape, CircleWidget):
        main_window.current_shape.stack_order = value
        
        # Sortiraj sve widget-e - koristi metodu iz MainWindow
        main_window.sortWidgetsByStackOrder()
        
        if hasattr(main_window, 'all_circle_dicts'):
            main_window.all_circle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

    # RECTANGLE METHODS
#----------------------------------------------------------------RECTANGLE----------------------------------------------------------------

def showRectangleProperties(main_window, current_index):
    """Prikazuje properties za RectangleWidget - konzistentno sa drugim widget-ima"""
    # Ako rectangle nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Rectangle")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_rect = QCheckBox()
    main_window.active_checkbox_rect.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_rect.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_rect.stateChanged.connect(lambda state: update_rectangle_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_rect)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_rect = QCheckBox()
    main_window.visible_checkbox_rect.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_rect.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_rect.stateChanged.connect(lambda state: update_rectangle_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_rect)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_rect = QCheckBox()
    main_window.static_checkbox_rect.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_rect.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_rect.stateChanged.connect(lambda state: update_rectangle_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_rect)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. RECTANGLE NAME SECTION
    name_label = QLabel("Rectangle name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_rect = QLineEdit()
    main_window.name_edit_rect.setText(main_window.current_shape.custom_name)
    main_window.name_edit_rect.textChanged.connect(lambda text: update_rectangle_name(main_window, text))
    main_window.name_edit_rect.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_rect.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_rect)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    main_window.stack_order_spin_rect = QSpinBox()
    main_window.stack_order_spin_rect.setRange(1, 100)
    main_window.stack_order_spin_rect.setValue(main_window.current_shape.stack_order)  # ← OVDE
    
    main_window.stack_order_spin_rect.valueChanged.connect(lambda value: update_rectangle_stack_order(main_window, value))
    main_window.stack_order_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin_rect.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin_rect)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_rect = QSpinBox()
    main_window.tag_spin_rect.setRange(0, 255)
    main_window.tag_spin_rect.setValue(main_window.current_shape.tag)
    main_window.tag_spin_rect.valueChanged.connect(lambda value: update_rectangle_tag(main_window, value))
    main_window.tag_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_rect.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_rect)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1

    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_rect = QSpinBox()
    main_window.pos_x_spin_rect.setRange(0, 480)
    main_window.pos_x_spin_rect.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_rect.valueChanged.connect(lambda value: update_rectangle_position(main_window))
    main_window.pos_x_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_rect.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_rect)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_rect = QSpinBox()
    main_window.pos_y_spin_rect.setRange(0, 272)
    main_window.pos_y_spin_rect.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_rect.valueChanged.connect(lambda value: update_rectangle_position(main_window))
    main_window.pos_y_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_rect.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_rect)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_rect = QSpinBox()
    main_window.width_spin_rect.setRange(10, 480)
    main_window.width_spin_rect.setValue(main_window.current_shape.width())
    main_window.width_spin_rect.valueChanged.connect(lambda value: update_rectangle_size(main_window))
    main_window.width_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_rect.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_rect)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.height_spin_rect = QSpinBox()
    main_window.height_spin_rect.setRange(10, 272)
    main_window.height_spin_rect.setValue(main_window.current_shape.height())
    main_window.height_spin_rect.valueChanged.connect(lambda value: update_rectangle_size(main_window))
    main_window.height_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.height_spin_rect.setFixedWidth(60)
    height_layout.addWidget(main_window.height_spin_rect)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Edges color
    edges_color_layout = QHBoxLayout()
    edges_color_layout.setContentsMargins(20, 5, 10, 5)
    edges_color_label = QLabel("Edges color:")
    edges_color_label.setStyleSheet("color: white; font-size: 14px;")
    edges_color_layout.addWidget(edges_color_label)
    edges_color_layout.addStretch(1)

    # Koristi boju iz rectangle-a
    if hasattr(main_window.current_shape, 'color'):
        edge_color_hex = main_window.current_shape.color.name()
    else:
        edge_color_hex = "#FF0000"

    main_window.edges_color_rect_rect = ColorRectangle(edge_color_hex)
    main_window.edges_color_rect_rect.mousePressEvent = lambda e: change_rectangle_edge_color(main_window)
    main_window.edges_color_rect_rect.setCursor(Qt.CursorShape.PointingHandCursor)
    edges_color_layout.addWidget(main_window.edges_color_rect_rect)

    edges_color_widget = QWidget()
    edges_color_widget.setLayout(edges_color_layout)
    main_window.properties_layout.insertWidget(current_index, edges_color_widget)
    current_index += 1

    # Thickness
    thickness_layout = QHBoxLayout()
    thickness_layout.setContentsMargins(20, 5, 10, 5)
    thickness_label = QLabel("Thickness:")
    thickness_label.setStyleSheet("color: white; font-size: 14px;")
    thickness_layout.addWidget(thickness_label)
    thickness_layout.addStretch(1)
    main_window.thickness_spin_rect = QSpinBox()
    main_window.thickness_spin_rect.setRange(1, 50)
    main_window.thickness_spin_rect.setValue(main_window.current_shape.border_width)
    main_window.thickness_spin_rect.valueChanged.connect(lambda value: update_rectangle_thickness(main_window, value))
    main_window.thickness_spin_rect.setStyleSheet("color: black; background-color: white;")
    main_window.thickness_spin_rect.setFixedWidth(60)
    thickness_layout.addWidget(main_window.thickness_spin_rect)
    thickness_widget = QWidget()
    thickness_widget.setLayout(thickness_layout)
    main_window.properties_layout.insertWidget(current_index, thickness_widget)
    current_index += 1

    # Filled checkbox - OVO TREBA DA AKTIVIRA/DEAKTIVIRA GRADIJENT
    filled_layout = QHBoxLayout()
    filled_layout.setContentsMargins(20, 5, 10, 5)
    filled_label = QLabel("Filled:")
    filled_label.setStyleSheet("color: white; font-size: 14px;")
    filled_layout.addWidget(filled_label)
    filled_layout.addStretch(1)
    main_window.filled_checkbox_rect = QCheckBox()
    main_window.filled_checkbox_rect.setChecked(getattr(main_window.current_shape, 'filled', True))
    main_window.filled_checkbox_rect.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.filled_checkbox_rect.stateChanged.connect(lambda state: update_rectangle_filled(main_window, state))
    filled_layout.addWidget(main_window.filled_checkbox_rect)
    filled_widget = QWidget()
    filled_widget.setLayout(filled_layout)
    main_window.properties_layout.insertWidget(current_index, filled_widget)
    current_index += 1

    # Gradient type dropdown - UVIJEK PRIKAZAN
    gradient_type_layout = QHBoxLayout()
    gradient_type_layout.setContentsMargins(20, 5, 10, 5)
    gradient_type_label = QLabel("Gradient type:")
    gradient_type_label.setStyleSheet("color: white; font-size: 14px;")
    gradient_type_layout.addWidget(gradient_type_label)
    gradient_type_layout.addStretch(1)
    
    main_window.gradient_combo_rect = QComboBox()
    main_window.gradient_combo_rect.addItems([
        "Top to Bottom",
        "Bottom to Top",
        "Left to Right",
        "Right to Left"
    ])
    
    # Mapiranje direction-a na tekst
    direction_mapping = {
        "top_to_bottom": "Top to Bottom",
        "bottom_to_top": "Bottom to Top",
        "left_to_right": "Left to Right",
        "right_to_left": "Right to Left"
    }
    
    current_direction = getattr(main_window.current_shape, 'gradient_direction', "top_to_bottom")
    current_text = direction_mapping.get(current_direction, "Top to Bottom")
    main_window.gradient_combo_rect.setCurrentText(current_text)
    main_window.gradient_combo_rect.currentTextChanged.connect(lambda text: update_rectangle_gradient_direction(main_window, text))
    main_window.gradient_combo_rect.setStyleSheet("color: black; background-color: white;")
    main_window.gradient_combo_rect.setFixedWidth(120)
    gradient_type_layout.addWidget(main_window.gradient_combo_rect)
    
    gradient_type_widget = QWidget()
    gradient_type_widget.setLayout(gradient_type_layout)
    main_window.properties_layout.insertWidget(current_index, gradient_type_widget)
    current_index += 1

    # Start Color - UVIJEK PRIKAZAN
    start_color_layout = QHBoxLayout()
    start_color_layout.setContentsMargins(20, 5, 10, 5)
    start_color_label = QLabel("Start color:")
    start_color_label.setStyleSheet("color: white; font-size: 14px;")
    start_color_layout.addWidget(start_color_label)
    start_color_layout.addStretch(1)
    
    if hasattr(main_window.current_shape, 'gradient_color1'):
        start_color_hex = main_window.current_shape.gradient_color1.name()
    else:
        start_color_hex = "#FF0000"
    
    main_window.start_color_rect_rect = ColorRectangle(start_color_hex)
    main_window.start_color_rect_rect.mousePressEvent = lambda e: change_rectangle_gradient_start_color(main_window)
    main_window.start_color_rect_rect.setCursor(Qt.CursorShape.PointingHandCursor)
    start_color_layout.addWidget(main_window.start_color_rect_rect)
    
    start_color_widget = QWidget()
    start_color_widget.setLayout(start_color_layout)
    main_window.properties_layout.insertWidget(current_index, start_color_widget)
    current_index += 1

    # End Color - UVIJEK PRIKAZAN
    end_color_layout = QHBoxLayout()
    end_color_layout.setContentsMargins(20, 5, 10, 5)
    end_color_label = QLabel("End color:")
    end_color_label.setStyleSheet("color: white; font-size: 14px;")
    end_color_layout.addWidget(end_color_label)
    end_color_layout.addStretch(1)
    
    if hasattr(main_window.current_shape, 'gradient_color2'):
        end_color_hex = main_window.current_shape.gradient_color2.name()
    else:
        end_color_hex = "#0000FF"
    
    main_window.end_color_rect_rect = ColorRectangle(end_color_hex)
    main_window.end_color_rect_rect.mousePressEvent = lambda e: change_rectangle_gradient_end_color(main_window)
    main_window.end_color_rect_rect.setCursor(Qt.CursorShape.PointingHandCursor)
    end_color_layout.addWidget(main_window.end_color_rect_rect)
    
    end_color_widget = QWidget()
    end_color_widget.setLayout(end_color_layout)
    main_window.properties_layout.insertWidget(current_index, end_color_widget)
    current_index += 1

    # Postavi inicijalno stanje gradient boja
    update_rectangle_gradient_appearance(main_window)

    return current_index

# CALLBACK METODE ZA RECTANGLE:


def update_rectangle_tag(main_window, value):
    """Ažurira tag vrednost za rectangle"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_active(main_window, state):
    """Ažurira active status za rectangle"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.set_active(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_visible(main_window, state):
    """Ažurira visible status za rectangle"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.set_visible(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_static(main_window, state):
    """Ažurira static status za rectangle"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.set_static(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_name(main_window, text):
    """Ažurira ime rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.set_custom_name(text)
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_stack_order(main_window, value):
    """Ažurira stack order za rectangle i sortira widget-e"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        # Postavi novi stack_order
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_rectangle_position(main_window):
    """Ažurira poziciju rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        if hasattr(main_window, 'pos_x_spin_rect') and hasattr(main_window, 'pos_y_spin_rect'):
            main_window.current_shape.move(main_window.pos_x_spin_rect.value(), main_window.pos_y_spin_rect.value())
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_size(main_window):
    """Ažurira veličinu rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        if hasattr(main_window, 'width_spin_rect') and hasattr(main_window, 'height_spin_rect'):
            main_window.current_shape.setFixedSize(main_window.width_spin_rect.value(), main_window.height_spin_rect.value())
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_rectangle_edge_color(main_window):
    """Menja boju ivice rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        current_color = main_window.current_shape.color
        color = QColorDialog.getColor(current_color)
        if color.isValid():
            main_window.current_shape.set_color(color)
            main_window.edges_color_rect_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_thickness(main_window, value):
    """Ažurira debljinu ivice rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        main_window.current_shape.set_border_width(value)
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_filled(main_window, state):
    """Ažurira filled property za RectangleWidget"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        filled = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_filled(filled)
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_gradient_direction(main_window, text):
    """Ažurira smer gradijenta za rectangle"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        # Mapiranje teksta na direction
        text_to_direction = {
            "Top to Bottom": "top_to_bottom",
            "Bottom to Top": "bottom_to_top",
            "Left to Right": "left_to_right",
            "Right to Left": "right_to_left"
        }
        
        direction = text_to_direction.get(text, "top_to_bottom")
        main_window.current_shape.set_gradient_direction(direction)
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_gradient_appearance(main_window):
    """Ažurira izgled gradient boja na osnovu stanja"""
    if not hasattr(main_window, 'current_shape') or not main_window.current_shape:
        return
    
    # Boje su uvek vidljive, samo ažuriraj stil
    if hasattr(main_window, 'start_color_rect_rect'):
        main_window.start_color_rect_rect.setStyleSheet(
            f"background-color: {main_window.current_shape.gradient_color1.name()}; "
            f"border: 2px solid #666;"
        )
    
    if hasattr(main_window, 'end_color_rect_rect'):
        main_window.end_color_rect_rect.setStyleSheet(
            f"background-color: {main_window.current_shape.gradient_color2.name()}; "
            f"border: 2px solid #666;"
        )

def change_rectangle_gradient_start_color(main_window):
    """Menja početnu boju gradijenta rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        color = QColorDialog.getColor(main_window.current_shape.gradient_color1)
        if color.isValid():
            main_window.current_shape.set_gradient_color1(color)
            
            # Ažuriraj izgled
            update_rectangle_gradient_appearance(main_window)
            
            # Ažuriraj rečnik
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_rectangle_gradient_end_color(main_window):
    """Menja krajnju boju gradijenta rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        color = QColorDialog.getColor(main_window.current_shape.gradient_color2)
        if color.isValid():
            main_window.current_shape.set_gradient_color2(color)
            
            # Ažuriraj izgled
            update_rectangle_gradient_appearance(main_window)
            
            # Ažuriraj rečnik
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateRectangleProperties(main_window):
    """Ažurira properties prikaz za RectangleWidget"""
    if not main_window.current_shape:
        return
    
    # Blokiraj signale
    if hasattr(main_window, 'active_checkbox_rect'):
        main_window.active_checkbox_rect.blockSignals(True)
        main_window.active_checkbox_rect.setChecked(main_window.current_shape.active)
        main_window.active_checkbox_rect.blockSignals(False)
    
    if hasattr(main_window, 'visible_checkbox_rect'):
        main_window.visible_checkbox_rect.blockSignals(True)
        main_window.visible_checkbox_rect.setChecked(main_window.current_shape.visible)
        main_window.visible_checkbox_rect.blockSignals(False)
    
    if hasattr(main_window, 'static_checkbox_rect'):
        main_window.static_checkbox_rect.blockSignals(True)
        main_window.static_checkbox_rect.setChecked(main_window.current_shape.static)
        main_window.static_checkbox_rect.blockSignals(False)
    
    if hasattr(main_window, 'name_edit_rect'):
        main_window.name_edit_rect.blockSignals(True)
        main_window.name_edit_rect.setText(main_window.current_shape.custom_name)
        main_window.name_edit_rect.blockSignals(False)
    
    if hasattr(main_window, 'stack_order_spin_rect'):
        main_window.stack_order_spin_rect.blockSignals(True)
        main_window.stack_order_spin_rect.setValue(main_window.current_shape.stack_order)
        main_window.stack_order_spin_rect.blockSignals(False)
    
    if hasattr(main_window, 'pos_x_spin_rect'):
        main_window.pos_x_spin_rect.blockSignals(True)
        main_window.pos_x_spin_rect.setValue(main_window.current_shape.x())
        main_window.pos_x_spin_rect.blockSignals(False)
    
    if hasattr(main_window, 'pos_y_spin_rect'):
        main_window.pos_y_spin_rect.blockSignals(True)
        main_window.pos_y_spin_rect.setValue(main_window.current_shape.y())
        main_window.pos_y_spin_rect.blockSignals(False)
    
    if hasattr(main_window, 'width_spin_rect'):
        main_window.width_spin_rect.blockSignals(True)
        main_window.width_spin_rect.setValue(main_window.current_shape.width())
        main_window.width_spin_rect.blockSignals(False)
    
    if hasattr(main_window, 'height_spin_rect'):
        main_window.height_spin_rect.blockSignals(True)
        main_window.height_spin_rect.setValue(main_window.current_shape.height())
        main_window.height_spin_rect.blockSignals(False)
    
    if hasattr(main_window, 'edges_color_rect_rect'):
        main_window.edges_color_rect_rect.setStyleSheet(
            f"background-color: {main_window.current_shape.color.name()}; border: 1px solid #ccc;"
        )
    
    if hasattr(main_window, 'thickness_spin_rect'):
        main_window.thickness_spin_rect.blockSignals(True)
        main_window.thickness_spin_rect.setValue(main_window.current_shape.border_width)
        main_window.thickness_spin_rect.blockSignals(False)
    
    if hasattr(main_window, 'filled_checkbox_rect'):
        main_window.filled_checkbox_rect.blockSignals(True)
        main_window.filled_checkbox_rect.setChecked(main_window.current_shape.filled)
        main_window.filled_checkbox_rect.blockSignals(False)
    
    if hasattr(main_window, 'gradient_combo_rect'):
        main_window.gradient_combo_rect.blockSignals(True)
        direction_mapping = {
            "top_to_bottom": "Top to Bottom",
            "bottom_to_top": "Bottom to Top",
            "left_to_right": "Left to Right",
            "right_to_left": "Right to Left"
        }
        current_direction = direction_mapping.get(main_window.current_shape.gradient_direction, "Top to Bottom")
        main_window.gradient_combo_rect.setCurrentText(current_direction)
        main_window.gradient_combo_rect.blockSignals(False)
    
    # Ažuriraj gradient boje
    if hasattr(main_window, 'start_color_rect_rect'):
        main_window.start_color_rect_rect.setStyleSheet(
            f"background-color: {main_window.current_shape.gradient_color1.name()}; border: 1px solid #ccc;"
        )
    
    if hasattr(main_window, 'end_color_rect_rect'):
        main_window.end_color_rect_rect.setStyleSheet(
            f"background-color: {main_window.current_shape.gradient_color2.name()}; border: 1px solid #ccc;"
        )

def update_rectangle_gradient_direction(main_window, text):
    """Ažurira smer gradijenta za rectangle"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        # Mapiranje teksta na direction
        text_to_direction = {
            "Top to Bottom": "top_to_bottom",
            "Bottom to Top": "bottom_to_top",
            "Left to Right": "left_to_right",
            "Right to Left": "right_to_left"
        }
        
        direction = text_to_direction.get(text, "top_to_bottom")
        main_window.current_shape.gradient_direction = direction
        main_window.current_shape.update()
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_rectangle_gradient_start_color(main_window):
    """Menja početnu boju gradijenta rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        color = QColorDialog.getColor(main_window.current_shape.gradient_color1)
        if color.isValid():
            main_window.current_shape.gradient_color1 = color
            main_window.current_shape.update()
            
            # Ažuriraj izgled
            if hasattr(main_window, 'start_color_rect_rect'):
                main_window.start_color_rect_rect.setStyleSheet(
                    f"background-color: {color.name()}; "
                    f"border: 2px solid #666;"
                )
            
            # Ažuriraj rečnik
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_rectangle_gradient_end_color(main_window):
    """Menja krajnju boju gradijenta rectangle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        color = QColorDialog.getColor(main_window.current_shape.gradient_color2)
        if color.isValid():
            main_window.current_shape.gradient_color2 = color
            main_window.current_shape.update()
            
            # Ažuriraj izgled
            if hasattr(main_window, 'end_color_rect_rect'):
                main_window.end_color_rect_rect.setStyleSheet(
                    f"background-color: {color.name()}; "
                    f"border: 2px solid #666;"
                )
            
            # Ažuriraj rečnik
            if hasattr(main_window, 'all_rectangle_dicts'):
                main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_filled(main_window, state):
    """Ažurira filled property za RectangleWidget"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        filled = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.filled = filled
        main_window.current_shape.update()
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_rectangle_stack_order(main_window, value):
    """Ažurira stack order za rectangle i sortira widget-e"""
    if main_window.current_shape and isinstance(main_window.current_shape, RectangleWidget):
        # Postavi novi stack_order
        main_window.current_shape.stack_order = value
        
        # Sortiraj sve widget-e po stack_order
        sort_widgets_by_stack_order(main_window)
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_rectangle_dicts'):
            main_window.all_rectangle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()
#----------------------------------------------------------------------------------------------------------------------------------------------------------

def showClockProperties(main_window, current_index):
    """Prikazuje properties za ClockWidget"""
    # Ako clock nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Clock")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_clock = QCheckBox()
    main_window.active_checkbox_clock.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_clock.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_clock.stateChanged.connect(lambda state: update_clock_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_clock)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_clock = QCheckBox()
    main_window.visible_checkbox_clock.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_clock.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_clock.stateChanged.connect(lambda state: update_clock_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_clock)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_clock = QCheckBox()
    main_window.static_checkbox_clock.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_clock.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_clock.stateChanged.connect(lambda state: update_clock_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_clock)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. CLOCK NAME SECTION
    name_label = QLabel("Clock name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_clock = QLineEdit()
    main_window.name_edit_clock.setText(main_window.current_shape.custom_name)
    main_window.name_edit_clock.textChanged.connect(lambda text: update_clock_name(main_window, text))
    main_window.name_edit_clock.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_clock.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_clock)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_clock_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_clock = QSpinBox()
    main_window.pos_x_spin_clock.setRange(0, 480)
    main_window.pos_x_spin_clock.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_clock.valueChanged.connect(lambda value: updateClockPosition(main_window))
    main_window.pos_x_spin_clock.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_clock.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_clock)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_clock = QSpinBox()
    main_window.pos_y_spin_clock.setRange(0, 272)
    main_window.pos_y_spin_clock.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_clock.valueChanged.connect(lambda value: updateClockPosition(main_window))
    main_window.pos_y_spin_clock.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_clock.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_clock)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Diameter
    diameter_layout = QHBoxLayout()
    diameter_layout.setContentsMargins(20, 5, 10, 5)
    diameter_label = QLabel("Diameter:")
    diameter_label.setStyleSheet("color: white; font-size: 14px;")
    diameter_layout.addWidget(diameter_label)
    diameter_layout.addStretch(1)
    main_window.diameter_spin_clock = QSpinBox()
    main_window.diameter_spin_clock.setRange(50, 272)
    main_window.diameter_spin_clock.setValue(main_window.current_shape.diameter)
    main_window.diameter_spin_clock.valueChanged.connect(lambda value: update_clock_diameter(main_window, value))
    main_window.diameter_spin_clock.setStyleSheet("color: black; background-color: white;")
    main_window.diameter_spin_clock.setFixedWidth(60)
    diameter_layout.addWidget(main_window.diameter_spin_clock)
    diameter_widget = QWidget()
    diameter_widget.setLayout(diameter_layout)
    main_window.properties_layout.insertWidget(current_index, diameter_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Background Color
    bg_color_layout = QHBoxLayout()
    bg_color_layout.setContentsMargins(20, 5, 10, 5)
    bg_color_label = QLabel("Background color:")
    bg_color_label.setStyleSheet("color: white; font-size: 14px;")
    bg_color_layout.addWidget(bg_color_label)
    bg_color_layout.addStretch(1)

    bg_color_hex = main_window.current_shape.background_color.name()
    main_window.bg_color_rect_clock = ColorRectangle(bg_color_hex)
    main_window.bg_color_rect_clock.mousePressEvent = lambda e: change_clock_background_color(main_window)
    main_window.bg_color_rect_clock.setCursor(Qt.CursorShape.PointingHandCursor)
    bg_color_layout.addWidget(main_window.bg_color_rect_clock)

    bg_color_widget = QWidget()
    bg_color_widget.setLayout(bg_color_layout)
    main_window.properties_layout.insertWidget(current_index, bg_color_widget)
    current_index += 1

    # 3D Checkbox
    use_3d_layout = QHBoxLayout()
    use_3d_layout.setContentsMargins(20, 5, 10, 5)
    use_3d_label = QLabel("3D:")
    use_3d_label.setStyleSheet("color: white; font-size: 14px;")
    use_3d_layout.addWidget(use_3d_label)
    use_3d_layout.addStretch(1)
    main_window.use_3d_checkbox_clock = QCheckBox()
    main_window.use_3d_checkbox_clock.setChecked(getattr(main_window.current_shape, 'use_3d', False))
    main_window.use_3d_checkbox_clock.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.use_3d_checkbox_clock.stateChanged.connect(lambda state: update_clock_use_3d(main_window, state))
    use_3d_layout.addWidget(main_window.use_3d_checkbox_clock)
    use_3d_widget = QWidget()
    use_3d_widget.setLayout(use_3d_layout)
    main_window.properties_layout.insertWidget(current_index, use_3d_widget)
    current_index += 1

    # 5. TIME SECTION
    time_label = QLabel("Time")
    time_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, time_label)
    current_index += 1

    # Hours
    hours_layout = QHBoxLayout()
    hours_layout.setContentsMargins(20, 5, 10, 5)
    hours_label = QLabel("Hours:")
    hours_label.setStyleSheet("color: white; font-size: 14px;")
    hours_layout.addWidget(hours_label)
    hours_layout.addStretch(1)
    main_window.hours_spin_clock = QSpinBox()
    main_window.hours_spin_clock.setRange(0, 11)
    main_window.hours_spin_clock.setValue(getattr(main_window.current_shape, 'hours', 10))
    main_window.hours_spin_clock.valueChanged.connect(lambda value: update_clock_hours(main_window, value))
    main_window.hours_spin_clock.setStyleSheet("color: black; background-color: white;")
    main_window.hours_spin_clock.setFixedWidth(60)
    hours_layout.addWidget(main_window.hours_spin_clock)
    hours_widget = QWidget()
    hours_widget.setLayout(hours_layout)
    main_window.properties_layout.insertWidget(current_index, hours_widget)
    current_index += 1

    # Minutes
    minutes_layout = QHBoxLayout()
    minutes_layout.setContentsMargins(20, 5, 10, 5)
    minutes_label = QLabel("Minutes:")
    minutes_label.setStyleSheet("color: white; font-size: 14px;")
    minutes_layout.addWidget(minutes_label)
    minutes_layout.addStretch(1)
    main_window.minutes_spin_clock = QSpinBox()
    main_window.minutes_spin_clock.setRange(0, 59)
    main_window.minutes_spin_clock.setValue(getattr(main_window.current_shape, 'minutes', 15))
    main_window.minutes_spin_clock.valueChanged.connect(lambda value: update_clock_minutes(main_window, value))
    main_window.minutes_spin_clock.setStyleSheet("color: black; background-color: white;")
    main_window.minutes_spin_clock.setFixedWidth(60)
    minutes_layout.addWidget(main_window.minutes_spin_clock)
    minutes_widget = QWidget()
    minutes_widget.setLayout(minutes_layout)
    main_window.properties_layout.insertWidget(current_index, minutes_widget)
    current_index += 1

    # Seconds
    seconds_layout = QHBoxLayout()
    seconds_layout.setContentsMargins(20, 5, 10, 5)
    seconds_label = QLabel("Seconds:")
    seconds_label.setStyleSheet("color: white; font-size: 14px;")
    seconds_layout.addWidget(seconds_label)
    seconds_layout.addStretch(1)
    main_window.seconds_spin_clock = QSpinBox()
    main_window.seconds_spin_clock.setRange(0, 59)
    main_window.seconds_spin_clock.setValue(getattr(main_window.current_shape, 'seconds', 45))
    main_window.seconds_spin_clock.valueChanged.connect(lambda value: update_clock_seconds(main_window, value))
    main_window.seconds_spin_clock.setStyleSheet("color: black; background-color: white;")
    main_window.seconds_spin_clock.setFixedWidth(60)
    seconds_layout.addWidget(main_window.seconds_spin_clock)
    seconds_widget = QWidget()
    seconds_widget.setLayout(seconds_layout)
    main_window.properties_layout.insertWidget(current_index, seconds_widget)
    current_index += 1

    return current_index

# CALLBACK METODE ZA CLOCK:

def updateClockPosition(main_window):
    """Ažurira poziciju clock-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        if hasattr(main_window, 'pos_x_spin_clock') and hasattr(main_window, 'pos_y_spin_clock'):
            main_window.current_shape.move(main_window.pos_x_spin_clock.value(), main_window.pos_y_spin_clock.value())

def update_clock_active(main_window, state):
    """Ažurira active status za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_active(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_visible(main_window, state):
    """Ažurira visible status za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_visible(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_static(main_window, state):
    """Ažurira static status za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_static(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_name(main_window, text):
    """Ažurira ime clock-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_custom_name(text)
        if hasattr(main_window, 'all_clock_dicts'):
            # Ažuriraj ključ u rečniku ako se promenilo ime
            old_name = None
            for name, props in list(main_window.all_clock_dicts.items()):
                if props.get('x') == main_window.current_shape.x() and props.get('y') == main_window.current_shape.y():
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_clock_dicts[text] = main_window.all_clock_dicts.pop(old_name)
            else:
                main_window.all_clock_dicts[text] = main_window.current_shape.get_properties_dict()

def update_clock_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_clock_position(main_window):
    """Ažurira poziciju clock-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        if hasattr(main_window, 'pos_x_spin_clock') and hasattr(main_window, 'pos_y_spin_clock'):
            main_window.current_shape.move(main_window.pos_x_spin_clock.value(), main_window.pos_y_spin_clock.value())
            if hasattr(main_window, 'all_clock_dicts'):
                main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_diameter(main_window, value):
    """Ažurira dijametar clock-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_diameter(value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_clock_background_color(main_window):
    """Menja boju pozadine clock-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        current_color = main_window.current_shape.background_color
        color = QColorDialog.getColor(current_color)
        if color.isValid():
            main_window.current_shape.set_background_color(color)
            main_window.bg_color_rect_clock.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_clock_dicts'):
                main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_use_3d(main_window, state):
    """Ažurira 3D efekat za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_use_3d(use_3d)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_hours(main_window, value):
    """Ažurira sate za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_hours(value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_minutes(main_window, value):
    """Ažurira minute za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_minutes(value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_clock_seconds(main_window, value):
    """Ažurira sekunde za clock"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        main_window.current_shape.set_seconds(value)
        if hasattr(main_window, 'all_clock_dicts'):
            main_window.all_clock_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateClockSize(main_window):
    """Ažurira veličinu ClockWidget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ClockWidget):
        if hasattr(main_window, 'diameter_spin_clock'):
            main_window.current_shape.set_diameter(main_window.diameter_spin_clock.value())
#-------------------------------------------------------------------------------------------------------------------------------

# GAUGE METHODS
def showGaugeProperties(main_window, current_index):
    """Prikazuje properties za GaugeWidget"""
    # Ako gauge nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Gauge")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_gauge = QCheckBox()
    main_window.active_checkbox_gauge.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_gauge.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_gauge.stateChanged.connect(lambda state: update_gauge_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_gauge)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_gauge = QCheckBox()
    main_window.visible_checkbox_gauge.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_gauge.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_gauge.stateChanged.connect(lambda state: update_gauge_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_gauge)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_gauge = QCheckBox()
    main_window.static_checkbox_gauge.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_gauge.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_gauge.stateChanged.connect(lambda state: update_gauge_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_gauge)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. GAUGE NAME SECTION
    name_label = QLabel("Gauge name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_gauge = QLineEdit()
    main_window.name_edit_gauge.setText(main_window.current_shape.custom_name)
    main_window.name_edit_gauge.textChanged.connect(lambda text: update_gauge_name(main_window, text))
    main_window.name_edit_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_gauge.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_gauge)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_gauge_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_gauge = QSpinBox()
    main_window.pos_x_spin_gauge.setRange(0, 480)
    main_window.pos_x_spin_gauge.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_gauge.valueChanged.connect(lambda value: update_gauge_position(main_window))
    main_window.pos_x_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_gauge.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_gauge)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_gauge = QSpinBox()
    main_window.pos_y_spin_gauge.setRange(0, 272)
    main_window.pos_y_spin_gauge.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_gauge.valueChanged.connect(lambda value: update_gauge_position(main_window))
    main_window.pos_y_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_gauge.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_gauge)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Diameter
    diameter_layout = QHBoxLayout()
    diameter_layout.setContentsMargins(20, 5, 10, 5)
    diameter_label = QLabel("Diameter:")
    diameter_label.setStyleSheet("color: white; font-size: 14px;")
    diameter_layout.addWidget(diameter_label)
    diameter_layout.addStretch(1)
    main_window.diameter_spin_gauge = QSpinBox()
    main_window.diameter_spin_gauge.setRange(50, 272)
    main_window.diameter_spin_gauge.setValue(main_window.current_shape.diameter)
    main_window.diameter_spin_gauge.valueChanged.connect(lambda value: update_gauge_diameter(main_window, value))
    main_window.diameter_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.diameter_spin_gauge.setFixedWidth(60)
    diameter_layout.addWidget(main_window.diameter_spin_gauge)
    diameter_widget = QWidget()
    diameter_widget.setLayout(diameter_layout)
    main_window.properties_layout.insertWidget(current_index, diameter_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Background Color
    bg_color_layout = QHBoxLayout()
    bg_color_layout.setContentsMargins(20, 5, 10, 5)
    bg_color_label = QLabel("Background color:")
    bg_color_label.setStyleSheet("color: white; font-size: 14px;")
    bg_color_layout.addWidget(bg_color_label)
    bg_color_layout.addStretch(1)

    bg_color_hex = main_window.current_shape.background_color.name()
    main_window.bg_color_rect_gauge = ColorRectangle(bg_color_hex)
    main_window.bg_color_rect_gauge.mousePressEvent = lambda e: change_gauge_background_color(main_window)
    main_window.bg_color_rect_gauge.setCursor(Qt.CursorShape.PointingHandCursor)
    bg_color_layout.addWidget(main_window.bg_color_rect_gauge)

    bg_color_widget = QWidget()
    bg_color_widget.setLayout(bg_color_layout)
    main_window.properties_layout.insertWidget(current_index, bg_color_widget)
    current_index += 1

    # 3D Checkbox
    use_3d_layout = QHBoxLayout()
    use_3d_layout.setContentsMargins(20, 5, 10, 5)
    use_3d_label = QLabel("3D:")
    use_3d_label.setStyleSheet("color: white; font-size: 14px;")
    use_3d_layout.addWidget(use_3d_label)
    use_3d_layout.addStretch(1)
    main_window.use_3d_checkbox_gauge = QCheckBox()
    main_window.use_3d_checkbox_gauge.setChecked(getattr(main_window.current_shape, 'use_3d', False))
    main_window.use_3d_checkbox_gauge.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.use_3d_checkbox_gauge.stateChanged.connect(lambda state: update_gauge_use_3d(main_window, state))
    use_3d_layout.addWidget(main_window.use_3d_checkbox_gauge)
    use_3d_widget = QWidget()
    use_3d_widget.setLayout(use_3d_layout)
    main_window.properties_layout.insertWidget(current_index, use_3d_widget)
    current_index += 1

    # 5. VALUE SECTION
    value_label = QLabel("Value")
    value_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, value_label)
    current_index += 1

    # Major Subdivision
    major_sub_layout = QHBoxLayout()
    major_sub_layout.setContentsMargins(20, 5, 10, 5)
    major_sub_label = QLabel("Major subdivision:")
    major_sub_label.setStyleSheet("color: white; font-size: 14px;")
    major_sub_layout.addWidget(major_sub_label)
    major_sub_layout.addStretch(1)
    main_window.major_sub_spin_gauge = QSpinBox()
    main_window.major_sub_spin_gauge.setRange(1, 20)
    main_window.major_sub_spin_gauge.setValue(getattr(main_window.current_shape, 'major_subdivision', 6))
    main_window.major_sub_spin_gauge.valueChanged.connect(lambda value: update_gauge_major_subdivision(main_window, value))
    main_window.major_sub_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.major_sub_spin_gauge.setFixedWidth(60)
    major_sub_layout.addWidget(main_window.major_sub_spin_gauge)
    major_sub_widget = QWidget()
    major_sub_widget.setLayout(major_sub_layout)
    main_window.properties_layout.insertWidget(current_index, major_sub_widget)
    current_index += 1

    # Minor Subdivision
    minor_sub_layout = QHBoxLayout()
    minor_sub_layout.setContentsMargins(20, 5, 10, 5)
    minor_sub_label = QLabel("Minor subdivision:")
    minor_sub_label.setStyleSheet("color: white; font-size: 14px;")
    minor_sub_layout.addWidget(minor_sub_label)
    minor_sub_layout.addStretch(1)
    main_window.minor_sub_spin_gauge = QSpinBox()
    main_window.minor_sub_spin_gauge.setRange(0, 10)
    main_window.minor_sub_spin_gauge.setValue(getattr(main_window.current_shape, 'minor_subdivision', 4))
    main_window.minor_sub_spin_gauge.valueChanged.connect(lambda value: update_gauge_minor_subdivision(main_window, value))
    main_window.minor_sub_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.minor_sub_spin_gauge.setFixedWidth(60)
    minor_sub_layout.addWidget(main_window.minor_sub_spin_gauge)
    minor_sub_widget = QWidget()
    minor_sub_widget.setLayout(minor_sub_layout)
    main_window.properties_layout.insertWidget(current_index, minor_sub_widget)
    current_index += 1

    # Range
    range_layout = QHBoxLayout()
    range_layout.setContentsMargins(20, 5, 10, 5)
    range_label = QLabel("Range:")
    range_label.setStyleSheet("color: white; font-size: 14px;")
    range_layout.addWidget(range_label)
    range_layout.addStretch(1)
    main_window.range_spin_gauge = QSpinBox()
    main_window.range_spin_gauge.setRange(1, 1000)
    main_window.range_spin_gauge.setValue(getattr(main_window.current_shape, 'range_value', 100))
    main_window.range_spin_gauge.valueChanged.connect(lambda value: update_gauge_range_value(main_window, value))
    main_window.range_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.range_spin_gauge.setFixedWidth(60)
    range_layout.addWidget(main_window.range_spin_gauge)
    range_widget = QWidget()
    range_widget.setLayout(range_layout)
    main_window.properties_layout.insertWidget(current_index, range_widget)
    current_index += 1

    # Value
    value_val_layout = QHBoxLayout()
    value_val_layout.setContentsMargins(20, 5, 10, 5)
    value_val_label = QLabel("Value:")
    value_val_label.setStyleSheet("color: white; font-size: 14px;")
    value_val_layout.addWidget(value_val_label)
    value_val_layout.addStretch(1)
    main_window.value_spin_gauge = QSpinBox()
    main_window.value_spin_gauge.setRange(0, getattr(main_window.current_shape, 'range_value', 100))
    main_window.value_spin_gauge.setValue(getattr(main_window.current_shape, 'value', 50))
    main_window.value_spin_gauge.valueChanged.connect(lambda value: update_gauge_value(main_window, value))
    main_window.value_spin_gauge.setStyleSheet("color: black; background-color: white;")
    main_window.value_spin_gauge.setFixedWidth(60)
    value_val_layout.addWidget(main_window.value_spin_gauge)
    value_val_widget = QWidget()
    value_val_widget.setLayout(value_val_layout)
    main_window.properties_layout.insertWidget(current_index, value_val_widget)
    current_index += 1

    return current_index

# CALLBACK METODE ZA GAUGE:

def update_gauge_active(main_window, state):
    """Ažurira active status za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_active(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_visible(main_window, state):
    """Ažurira visible status za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_visible(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_static(main_window, state):
    """Ažurira static status za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_static(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_name(main_window, text):
    """Ažurira ime gauge-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_custom_name(text)
        if hasattr(main_window, 'all_gauge_dicts'):
            # Ažuriraj ključ u rečniku ako se promenilo ime
            old_name = None
            for name, props in list(main_window.all_gauge_dicts.items()):
                if props.get('x') == main_window.current_shape.x() and props.get('y') == main_window.current_shape.y():
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_gauge_dicts[text] = main_window.all_gauge_dicts.pop(old_name)
            else:
                main_window.all_gauge_dicts[text] = main_window.current_shape.get_properties_dict()

def update_gauge_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_gauge_position(main_window):
    """Ažurira poziciju gauge-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        if hasattr(main_window, 'pos_x_spin_gauge') and hasattr(main_window, 'pos_y_spin_gauge'):
            main_window.current_shape.move(main_window.pos_x_spin_gauge.value(), main_window.pos_y_spin_gauge.value())
            if hasattr(main_window, 'all_gauge_dicts'):
                main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_diameter(main_window, value):
    """Ažurira dijametar gauge-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_diameter(value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_gauge_background_color(main_window):
    """Menja boju pozadine gauge-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        current_color = main_window.current_shape.background_color
        color = QColorDialog.getColor(current_color)
        if color.isValid():
            main_window.current_shape.set_background_color(color)
            main_window.bg_color_rect_gauge.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_gauge_dicts'):
                main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_use_3d(main_window, state):
    """Ažurira 3D efekat za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_use_3d(use_3d)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_major_subdivision(main_window, value):
    """Ažurira broj glavnih podeoka za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_major_subdivision(value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_minor_subdivision(main_window, value):
    """Ažurira broj sporednih podeoka za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_minor_subdivision(value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_range_value(main_window, value):
    """Ažurira maksimalnu vrednost za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_range_value(value)
        # Ažuriraj maksimum za value spin
        if hasattr(main_window, 'value_spin_gauge'):
            main_window.value_spin_gauge.setRange(0, value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_gauge_value(main_window, value):
    """Ažurira trenutnu vrednost za gauge"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        main_window.current_shape.set_value(value)
        if hasattr(main_window, 'all_gauge_dicts'):
            main_window.all_gauge_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateGaugeSize(main_window):
    """Ažurira veličinu GaugeWidget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, GaugeWidget):
        if hasattr(main_window, 'diameter_spin_gauge'):
            main_window.current_shape.set_diameter(main_window.diameter_spin_gauge.value())

#-------------------------------------------------------------------------------------------------------------------------------

# U callback.py, dodaj sledeće funkcije:

# U callback.py, dodaj sledeće funkcije:

def showDialProperties(main_window, current_index):
    """Prikazuje properties za DialWidget - KOMPLETNO ZASEBNO kao Gauge"""
    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_dial = QCheckBox()
    main_window.active_checkbox_dial.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_dial.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_dial.stateChanged.connect(lambda state: update_dial_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_dial)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_dial = QCheckBox()
    main_window.visible_checkbox_dial.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_dial.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_dial.stateChanged.connect(lambda state: update_dial_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_dial)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_dial = QCheckBox()
    main_window.static_checkbox_dial.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_dial.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_dial.stateChanged.connect(lambda state: update_dial_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_dial)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. DIAL NAME SECTION
    name_label = QLabel("Dial Name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_dial = QLineEdit()
    main_window.name_edit_dial.setText(main_window.current_shape.custom_name)
    main_window.name_edit_dial.textChanged.connect(lambda text: update_dial_name(main_window, text))
    main_window.name_edit_dial.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_dial.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_dial)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_dial_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1


    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_dial = QSpinBox()
    main_window.tag_spin_dial.setRange(0, 255)
    main_window.tag_spin_dial.setValue(main_window.current_shape.tag)
    main_window.tag_spin_dial.valueChanged.connect(lambda value: update_dial_tag(main_window, value))
    main_window.tag_spin_dial.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_dial.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_dial)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1

    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_dial = QSpinBox()
    main_window.pos_x_spin_dial.setRange(0, 480)
    main_window.pos_x_spin_dial.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_dial.valueChanged.connect(lambda value: update_dial_position(main_window))
    main_window.pos_x_spin_dial.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_dial.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_dial)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_dial = QSpinBox()
    main_window.pos_y_spin_dial.setRange(0, 272)
    main_window.pos_y_spin_dial.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_dial.valueChanged.connect(lambda value: update_dial_position(main_window))
    main_window.pos_y_spin_dial.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_dial.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_dial)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Diameter
    diameter_layout = QHBoxLayout()
    diameter_layout.setContentsMargins(20, 5, 10, 5)
    diameter_label = QLabel("Diameter:")
    diameter_label.setStyleSheet("color: white; font-size: 14px;")
    diameter_layout.addWidget(diameter_label)
    diameter_layout.addStretch(1)
    main_window.diameter_spin_dial = QSpinBox()
    main_window.diameter_spin_dial.setRange(50, 272)
    main_window.diameter_spin_dial.setValue(main_window.current_shape.diameter)
    main_window.diameter_spin_dial.valueChanged.connect(lambda value: update_dial_diameter(main_window, value))
    main_window.diameter_spin_dial.setStyleSheet("color: black; background-color: white;")
    main_window.diameter_spin_dial.setFixedWidth(60)
    diameter_layout.addWidget(main_window.diameter_spin_dial)
    diameter_widget = QWidget()
    diameter_widget.setLayout(diameter_layout)
    main_window.properties_layout.insertWidget(current_index, diameter_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # 3D Checkbox
    _3d_layout = QHBoxLayout()
    _3d_layout.setContentsMargins(20, 5, 10, 5)
    _3d_label = QLabel("3D:")
    _3d_label.setStyleSheet("color: white; font-size: 14px;")
    _3d_layout.addWidget(_3d_label)
    _3d_layout.addStretch(1)
    main_window._3d_checkbox_dial = QCheckBox()
    main_window._3d_checkbox_dial.setChecked(getattr(main_window.current_shape, '_3d', True))
    main_window._3d_checkbox_dial.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window._3d_checkbox_dial.stateChanged.connect(lambda state: update_dial_3d(main_window, state))
    _3d_layout.addWidget(main_window._3d_checkbox_dial)
    _3d_widget = QWidget()
    _3d_widget.setLayout(_3d_layout)
    main_window.properties_layout.insertWidget(current_index, _3d_widget)
    current_index += 1

    # 5. VALUE SECTION
    value_label = QLabel("Value")
    value_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, value_label)
    current_index += 1

    # Value
    value_val_layout = QHBoxLayout()
    value_val_layout.setContentsMargins(20, 5, 10, 5)
    value_val_label = QLabel("Value:")
    value_val_label.setStyleSheet("color: white; font-size: 14px;")
    value_val_layout.addWidget(value_val_label)
    value_val_layout.addStretch(1)
    main_window.value_spin_dial = QSpinBox()
    main_window.value_spin_dial.setRange(0, 100)
    main_window.value_spin_dial.setValue(getattr(main_window.current_shape, 'value', 0))
    main_window.value_spin_dial.valueChanged.connect(lambda value: update_dial_value(main_window, value))
    main_window.value_spin_dial.setStyleSheet("color: black; background-color: white;")
    main_window.value_spin_dial.setFixedWidth(60)
    value_val_layout.addWidget(main_window.value_spin_dial)
    value_val_widget = QWidget()
    value_val_widget.setLayout(value_val_layout)
    main_window.properties_layout.insertWidget(current_index, value_val_widget)
    current_index += 1

    return current_index

# CALLBACK METODE ZA DIAL:

def update_dial_tag(main_window, value):
    """Ažurira tag vrednost za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_active(main_window, state):
    """Ažurira active status za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.set_active(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_visible(main_window, state):
    """Ažurira visible status za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.set_visible(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_static(main_window, state):
    """Ažurira static status za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.set_static(state == Qt.CheckState.Checked.value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_name(main_window, text):
    """Ažurira ime dial-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.set_custom_name(text)
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
                main_window.all_dial_dicts[text] = main_window.current_shape.get_properties_dict()

def update_dial_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_dial_position(main_window):
    """Ažurira poziciju dial-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        if hasattr(main_window, 'pos_x_spin_dial') and hasattr(main_window, 'pos_y_spin_dial'):
            main_window.current_shape.move(main_window.pos_x_spin_dial.value(), main_window.pos_y_spin_dial.value())
            if hasattr(main_window, 'all_dial_dicts'):
                main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_diameter(main_window, value):
    """Ažurira dijametar dial-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.set_diameter(value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_3d(main_window, state):
    """Ažurira 3D efekat za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(use_3d)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_dial_value(main_window, value):
    """Ažurira trenutnu vrednost za dial"""
    if main_window.current_shape and isinstance(main_window.current_shape, DialWidget):
        main_window.current_shape.set_value(value)
        if hasattr(main_window, 'all_dial_dicts'):
            main_window.all_dial_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateDialSize(self):
    """Ažurira veličinu DialWidget-a (zastarelo, za kompatibilnost)"""
    if self.current_shape and isinstance(self.current_shape, DialWidget):
        if hasattr(self, 'width_spin'):
            diameter = self.width_spin.value()
            self.current_shape.set_diameter(diameter)
            self.current_shape.update_properties_dict()

#-------------------------------------------------------------------------------------------------------------------------------

def showToggleProperties(main_window, current_index):
    """Prikazuje properties za ToggleWidget - KOMPLETNO ZASEBNO kao Gauge"""
    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1
    
    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_toggle = QCheckBox()
    main_window.active_checkbox_toggle.setChecked(main_window.current_shape.active)
    main_window.active_checkbox_toggle.stateChanged.connect(lambda state: updateToggleActive(main_window))
    active_layout.addWidget(main_window.active_checkbox_toggle)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1
    
    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_toggle = QCheckBox()
    main_window.visible_checkbox_toggle.setChecked(main_window.current_shape.visible)
    main_window.visible_checkbox_toggle.stateChanged.connect(lambda state: updateToggleVisible(main_window))
    visible_layout.addWidget(main_window.visible_checkbox_toggle)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1
    
    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_toggle = QCheckBox()
    main_window.static_checkbox_toggle.setChecked(main_window.current_shape.static)
    main_window.static_checkbox_toggle.stateChanged.connect(lambda state: updateToggleStatic(main_window))
    static_layout.addWidget(main_window.static_checkbox_toggle)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1
    
    # 2. TOGGLE NAME SECTION
    name_label = QLabel("Toggle Name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1
    
    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_toggle = QLineEdit()
    main_window.name_edit_toggle.setText(getattr(main_window.current_shape, 'custom_name', 'Toggle_0'))
    main_window.name_edit_toggle.textChanged.connect(lambda text: updateToggleName(main_window, text))
    main_window.name_edit_toggle.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_toggle.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_toggle)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1
    
    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_toggle_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_toggle = QSpinBox()
    main_window.tag_spin_toggle.setRange(0, 255)
    main_window.tag_spin_toggle.setValue(main_window.current_shape.tag)
    main_window.tag_spin_toggle.valueChanged.connect(lambda value: update_button_tag(main_window, value))
    main_window.tag_spin_toggle.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_toggle.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_toggle)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1
    
    
    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_toggle = QSpinBox()
    main_window.pos_x_spin_toggle.setRange(0, 480)
    main_window.pos_x_spin_toggle.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_toggle.valueChanged.connect(lambda value: updateTogglePosition(main_window))
    main_window.pos_x_spin_toggle.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_toggle.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_toggle)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_toggle = QSpinBox()
    main_window.pos_y_spin_toggle.setRange(0, 272)
    main_window.pos_y_spin_toggle.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_toggle.valueChanged.connect(lambda value: updateTogglePosition(main_window))
    main_window.pos_y_spin_toggle.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_toggle.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_toggle)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_toggle = QSpinBox()
    main_window.width_spin_toggle.setRange(80, 480)
    main_window.width_spin_toggle.setValue(main_window.current_shape.get_width())
    main_window.width_spin_toggle.valueChanged.connect(lambda value: updateToggleSize(main_window, value))
    main_window.width_spin_toggle.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_toggle.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_toggle)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_label = QLabel("Color Adjust")
    color_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_label)
    current_index += 1
    
    # Knob Color
    knob_color_layout = QHBoxLayout()
    knob_color_layout.setContentsMargins(20, 5, 10, 5)
    knob_color_label = QLabel("Knob Color:")
    knob_color_label.setStyleSheet("color: white; font-size: 14px;")
    knob_color_layout.addWidget(knob_color_label)
    knob_color_layout.addStretch(1)
    main_window.knob_color_rect_toggle = ColorRectangle(main_window.current_shape.thumb_color.name())
    main_window.knob_color_rect_toggle.mousePressEvent = lambda e: changeToggleKnobColor(main_window)
    knob_color_layout.addWidget(main_window.knob_color_rect_toggle)
    knob_color_widget = QWidget()
    knob_color_widget.setLayout(knob_color_layout)
    main_window.properties_layout.insertWidget(current_index, knob_color_widget)
    current_index += 1
    
    # Background Color
    bg_color_layout = QHBoxLayout()
    bg_color_layout.setContentsMargins(20, 5, 10, 5)
    bg_color_label = QLabel("Background Color:")
    bg_color_label.setStyleSheet("color: white; font-size: 14px;")
    bg_color_layout.addWidget(bg_color_label)
    bg_color_layout.addStretch(1)
    main_window.bg_color_rect_toggle = ColorRectangle(main_window.current_shape.background_color.name())
    main_window.bg_color_rect_toggle.mousePressEvent = lambda e: changeToggleBackgroundColor(main_window)
    bg_color_layout.addWidget(main_window.bg_color_rect_toggle)
    bg_color_widget = QWidget()
    bg_color_widget.setLayout(bg_color_layout)
    main_window.properties_layout.insertWidget(current_index, bg_color_widget)
    current_index += 1
    
    # 3D checkbox
    _3d_layout = QHBoxLayout()
    _3d_layout.setContentsMargins(20, 5, 10, 5)
    _3d_label = QLabel("3D:")
    _3d_label.setStyleSheet("color: white; font-size: 14px;")
    _3d_layout.addWidget(_3d_label)
    _3d_layout.addStretch(1)
    main_window._3d_checkbox_toggle = QCheckBox()
    main_window._3d_checkbox_toggle.setChecked(main_window.current_shape._3d)
    main_window._3d_checkbox_toggle.stateChanged.connect(lambda state: updateToggle3D(main_window, state))
    _3d_layout.addWidget(main_window._3d_checkbox_toggle)
    _3d_widget = QWidget()
    _3d_widget.setLayout(_3d_layout)
    main_window.properties_layout.insertWidget(current_index, _3d_widget)
    current_index += 1
    
    # 5. STATE SECTION
    state_main_label = QLabel("State")
    state_main_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, state_main_label)
    current_index += 1
    
    # State checkbox
    state_layout = QHBoxLayout()
    state_layout.setContentsMargins(20, 5, 10, 5)
    state_field_label = QLabel("State:")
    state_field_label.setStyleSheet("color: white; font-size: 14px;")
    state_layout.addWidget(state_field_label)
    state_layout.addStretch(1)
    main_window.state_checkbox_toggle = QCheckBox("ON")
    main_window.state_checkbox_toggle.setChecked(main_window.current_shape.is_on)
    main_window.state_checkbox_toggle.stateChanged.connect(lambda state: updateToggleState(main_window, state))
    state_layout.addWidget(main_window.state_checkbox_toggle)
    state_widget = QWidget()
    state_widget.setLayout(state_layout)
    main_window.properties_layout.insertWidget(current_index, state_widget)
    current_index += 1
    
    return current_index

# Dodaj ove funkcije u callback.py

def update_toggle_tag(main_window, value):
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateTogglePosition(main_window):
    """Ažurira poziciju toggle-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        if hasattr(main_window, 'pos_x_spin_toggle') and hasattr(main_window, 'pos_y_spin_toggle'):
            main_window.current_shape.move(
                main_window.pos_x_spin_toggle.value(), 
                main_window.pos_y_spin_toggle.value()
            )
            # Ažuriraj rečnik
            main_window.current_shape.update_properties_dict()

# Ostatak callback funkcija za toggle ostaje isti...

def updateToggleActive(main_window, state):
    """Ažurira active status za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_active(active)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateToggleVisible(main_window, state):
    """Ažurira visible status za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(visible)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateToggleStatic(main_window, state):
    """Ažurira static status za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_static(static)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

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
                main_window.all_toggle_dicts[text] = main_window.current_shape.get_properties_dict()

def update_toggle_stack_order(main_window, value):
    """Ažurira stack order za toggle"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def changeToggleKnobColor(main_window):
    """Menja boju knob-a toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        color = QColorDialog.getColor(main_window.current_shape.thumb_color)
        if color.isValid():
            main_window.current_shape.set_thumb_color(color)
            if hasattr(main_window, 'knob_color_rect_toggle'):
                main_window.knob_color_rect_toggle.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def changeToggleBackgroundColor(main_window):
    """Menja boju pozadine toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        color = QColorDialog.getColor(main_window.current_shape.background_color)
        if color.isValid():
            main_window.current_shape.set_background_color(color)
            if hasattr(main_window, 'bg_color_rect_toggle'):
                main_window.bg_color_rect_toggle.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateToggle3D(main_window, state):
    """Ažurira 3D svojstvo toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        _3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(_3d)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateToggleState(main_window, state):
    """Ažurira stanje toggle-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        is_on = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_state(is_on)
        if hasattr(main_window, 'all_toggle_dicts'):
            main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateTogglePosition(main_window):
    """Ažurira poziciju toggle-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        if hasattr(main_window, 'pos_x_spin_toggle') and hasattr(main_window, 'pos_y_spin_toggle'):
            main_window.current_shape.move(
                main_window.pos_x_spin_toggle.value(), 
                main_window.pos_y_spin_toggle.value()
            )
            if hasattr(main_window, 'all_toggle_dicts'):
                main_window.all_toggle_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateToggleSize(main_window, value):
    """Ažurira veličinu toggle-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ToggleWidget):
        # ToggleWidget ima fiksnu visinu od 30
        main_window.current_shape.set_size(value, 30)
#-------------------------------------------------------------------------------------------------------------------------------

    # LABEL METHODS
def showLabelProperties(self, current_index):
    """Prikazuje properties za LabelWidget"""
    
    # STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    self.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    self.active_checkbox_label = QCheckBox()
    self.active_checkbox_label.setChecked(getattr(self.current_shape, 'active', True))
    self.active_checkbox_label.stateChanged.connect(lambda state: updateLabelActive(self, state))
    active_layout.addWidget(self.active_checkbox_label)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    self.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    self.visible_checkbox_label = QCheckBox()
    self.visible_checkbox_label.setChecked(getattr(self.current_shape, 'visible', True))
    self.visible_checkbox_label.stateChanged.connect(lambda state: updateLabelVisible(self, state))
    visible_layout.addWidget(self.visible_checkbox_label)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    self.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    self.static_checkbox_label = QCheckBox()
    self.static_checkbox_label.setChecked(getattr(self.current_shape, 'static', False))
    self.static_checkbox_label.stateChanged.connect(lambda state: updateLabelStatic(self, state))
    static_layout.addWidget(self.static_checkbox_label)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    self.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # LABEL NAME SECTION
    label_name_label = QLabel("Label Name")
    label_name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    self.properties_layout.insertWidget(current_index, label_name_label)
    current_index += 1

    # Name input
    name_layout = QHBoxLayout()
    name_layout.setContentsMargins(20, 5, 10, 5)
    name_label = QLabel("Name:")
    name_label.setStyleSheet("color: white; font-size: 14px;")
    name_layout.addWidget(name_label)
    name_layout.addStretch(1)
    self.label_name_edit = QLineEdit()
    self.label_name_edit.setText(self.current_shape.custom_name)
    self.label_name_edit.textChanged.connect(lambda text: updateLabelName(self, text))
    self.label_name_edit.setStyleSheet("color: black; background-color: white;")
    self.label_name_edit.setFixedWidth(100)
    name_layout.addWidget(self.label_name_edit)
    name_widget = QWidget()
    name_widget.setLayout(name_layout)
    self.properties_layout.insertWidget(current_index, name_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    self.stack_order_spin = QSpinBox()  # ← button specifično
    self.stack_order_spin.setRange(1, 100)
    self.stack_order_spin.setValue(self.current_shape.stack_order)
    self.stack_order_spin.valueChanged.connect(
        lambda value: update_label_stack_order(self, value))
    self.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    self.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(self.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    self.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    self.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    self.pos_x_spin_label = QSpinBox()
    self.pos_x_spin_label.setRange(0, 480)
    self.pos_x_spin_label.setValue(self.current_shape.x())
    self.pos_x_spin_label.valueChanged.connect(lambda: updateLabelPosition(self))
    self.pos_x_spin_label.setStyleSheet("color: black; background-color: white;")
    self.pos_x_spin_label.setFixedWidth(60)
    pos_x_layout.addWidget(self.pos_x_spin_label)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    self.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    self.pos_y_spin_label = QSpinBox()
    self.pos_y_spin_label.setRange(0, 272)
    self.pos_y_spin_label.setValue(self.current_shape.y())
    self.pos_y_spin_label.valueChanged.connect(lambda: updateLabelPosition(self))
    self.pos_y_spin_label.setStyleSheet("color: black; background-color: white;")
    self.pos_y_spin_label.setFixedWidth(60)
    pos_y_layout.addWidget(self.pos_y_spin_label)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    self.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1



    # COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    self.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Text Color
    text_color_layout = QHBoxLayout()
    text_color_layout.setContentsMargins(20, 5, 10, 5)
    text_color_label = QLabel("Text Color:")
    text_color_label.setStyleSheet("color: white; font-size: 14px;")
    text_color_layout.addWidget(text_color_label)
    text_color_layout.addStretch(1)
    self.text_color_rect_label = ColorRectangle(self.current_shape.text_color.name())
    self.text_color_rect_label.mousePressEvent = lambda e: changeLabelTextColor(self)
    text_color_layout.addWidget(self.text_color_rect_label)
    text_color_widget = QWidget()
    text_color_widget.setLayout(text_color_layout)
    self.properties_layout.insertWidget(current_index, text_color_widget)
    current_index += 1

    # TEXT SECTION
    text_main_label = QLabel("Text")
    text_main_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    self.properties_layout.insertWidget(current_index, text_main_label)
    current_index += 1

    # Text input
    text_layout = QHBoxLayout()
    text_layout.setContentsMargins(20, 5, 10, 5)
    text_field_label = QLabel("Text:")
    text_field_label.setStyleSheet("color: white; font-size: 14px;")
    text_layout.addWidget(text_field_label)
    text_layout.addStretch(1)
    self.text_edit_label = QLineEdit()
    self.text_edit_label.setText(self.current_shape.text)
    self.text_edit_label.textChanged.connect(lambda text: updateLabelText(self, text))
    self.text_edit_label.setStyleSheet("color: black; background-color: white;")
    self.text_edit_label.setFixedWidth(150)
    text_layout.addWidget(self.text_edit_label)
    text_widget = QWidget()
    text_widget.setLayout(text_layout)
    self.properties_layout.insertWidget(current_index, text_widget)
    current_index += 1

    # Text Size
    text_size_layout = QHBoxLayout()
    text_size_layout.setContentsMargins(20, 5, 10, 5)
    text_size_label = QLabel("Text Size:")
    text_size_label.setStyleSheet("color: white; font-size: 14px;")
    text_size_layout.addWidget(text_size_label)
    text_size_layout.addStretch(1)
    self.text_size_spin_label = QSpinBox()
    self.text_size_spin_label.setRange(6, 72)
    self.text_size_spin_label.setValue(self.current_shape.text_size)
    self.text_size_spin_label.valueChanged.connect(lambda value: updateLabelTextSize(self, value))
    self.text_size_spin_label.setStyleSheet("color: black; background-color: white;")
    self.text_size_spin_label.setFixedWidth(60)
    text_size_layout.addWidget(self.text_size_spin_label)
    text_size_widget = QWidget()
    text_size_widget.setLayout(text_size_layout)
    self.properties_layout.insertWidget(current_index, text_size_widget)
    current_index += 1

    # Text Font (ako želite da dodate)
    # font_layout = QHBoxLayout()
    # font_layout.setContentsMargins(20, 5, 10, 5)
    # font_label = QLabel("Font:")
    # font_label.setStyleSheet("color: white; font-size: 14px;")
    # font_layout.addWidget(font_label)
    # font_layout.addStretch(1)
    # self.font_combo_label = QComboBox()
    # self.font_combo_label.addItems(["Arial", "Times New Roman", "Courier New", "Verdana"])
    # self.font_combo_label.setCurrentText(self.current_shape.text_font)
    # self.font_combo_label.currentTextChanged.connect(lambda text: updateLabelFont(self, text))
    # self.font_combo_label.setStyleSheet("color: black; background-color: white;")
    # self.font_combo_label.setFixedWidth(100)
    # font_layout.addWidget(self.font_combo_label)
    # font_widget = QWidget()
    # font_widget.setLayout(font_layout)
    # self.properties_layout.insertWidget(current_index, font_widget)
    # current_index += 1

    # Text Alignment
    alignment_layout = QHBoxLayout()
    alignment_layout.setContentsMargins(20, 5, 10, 5)
    alignment_label = QLabel("Text Alignment:")
    alignment_label.setStyleSheet("color: white; font-size: 14px;")
    alignment_layout.addWidget(alignment_label)
    alignment_layout.addStretch(1)
    self.alignment_combo = QComboBox()
    self.alignment_combo.addItems(["Left", "Center", "Right", "Top", "Bottom"])
    self.alignment_combo.setCurrentText(self.current_shape.text_alignment)
    self.alignment_combo.currentTextChanged.connect(lambda text: updateLabelAlignment(self, text))
    self.alignment_combo.setStyleSheet("color: black; background-color: white;")
    self.alignment_combo.setFixedWidth(100)
    alignment_layout.addWidget(self.alignment_combo)
    alignment_widget = QWidget()
    alignment_widget.setLayout(alignment_layout)
    self.properties_layout.insertWidget(current_index, alignment_widget)
    current_index += 1

    return current_index

def updateLabelActive(self, state):
    """Ažurira active status za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        self.current_shape.set_active(is_active)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()

def updateLabelVisible(self, state):
    """Ažurira visible status za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        self.current_shape.set_visible(is_visible)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()

def updateLabelStatic(self, state):
    """Ažurira static status za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        self.current_shape.set_static(is_static)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()

def updateLabelName(self, text):
    """Ažurira ime label widget-a"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.custom_name = text
        if hasattr(self, 'all_label_dicts'):
            old_name = self.current_shape.custom_name
            self.all_label_dicts[old_name] = self.current_shape.get_properties_dict()

def update_label_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, LabelWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def changeLabelTextColor(self):
    """Menja boju teksta label-a"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        color = QColorDialog.getColor(self.current_shape.text_color)
        if color.isValid():
            self.current_shape.set_text_color(color)
            self.text_color_rect_label.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(self, 'all_label_dicts'):
                self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()

def updateLabelText(self, text):
    """Ažurira tekst label-a"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.set_text(text)
        # Ažuriraj width i height spinbox-ove kada se promeni tekst
        if hasattr(self, 'width_spin_label'):
            self.width_spin_label.setValue(self.current_shape.get_width())
        if hasattr(self, 'height_spin_label'):
            self.height_spin_label.setValue(self.current_shape.get_height())
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()


def updateLabelTextSize(self, value):
    """Ažurira veličinu fonta za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.set_text_size(value)
        # Ažuriraj width i height spinbox-ove kada se promeni veličina fonta
        if hasattr(self, 'width_spin_label'):
            self.width_spin_label.setValue(self.current_shape.get_width())
        if hasattr(self, 'height_spin_label'):
            self.height_spin_label.setValue(self.current_shape.get_height())
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()

def updateLabelAlignment(self, text):
    """Ažurira poravnanje teksta za label"""
    if self.current_shape and isinstance(self.current_shape, LabelWidget):
        self.current_shape.set_text_alignment(text)
        if hasattr(self, 'all_label_dicts'):
            self.all_label_dicts[self.current_shape.custom_name] = self.current_shape.get_properties_dict()

def updateLabelSize(self):
    """Ažurira veličinu label-a (veličina se automatski podešava prema tekstu)"""
    if self.current_shape:
        # Veličina se automatski podešava, samo ažuriraj poziciju
        update_position_spins(self)
        self.current_shape.update_properties_dict()

def updateLabelPosition(main_window):
    """Ažurira poziciju label-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, LabelWidget):
        if hasattr(main_window, 'pos_x_spin_label') and hasattr(main_window, 'pos_y_spin_label'):
            x = main_window.pos_x_spin_label.value()
            y = main_window.pos_y_spin_label.value()
            
            # OVO ĆE POZVATI OVERRIDE MOVE METODU KOJA ĆE AŽURIRATI SPIN BOX-OVE
            main_window.current_shape.move(x, y)
            
            # Rečnik će se ažurirati unutar move metode


#-------------------------------------------------------------------------------------------------------------------------------

def showSliderProperties(main_window, current_index):
    """Prikazuje properties za SliderWidget - KOMPLETNO ZASEBNO"""
    # Ako slider nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Slider")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_slider = QCheckBox()
    main_window.active_checkbox_slider.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_slider.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_slider.stateChanged.connect(lambda state: update_slider_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_slider)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_slider = QCheckBox()
    main_window.visible_checkbox_slider.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_slider.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_slider.stateChanged.connect(lambda state: update_slider_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_slider)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_slider = QCheckBox()
    main_window.static_checkbox_slider.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_slider.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_slider.stateChanged.connect(lambda state: update_slider_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_slider)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. SLIDER NAME SECTION
    name_label = QLabel("Slider Name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_slider = QLineEdit()
    main_window.name_edit_slider.setText(main_window.current_shape.custom_name)
    main_window.name_edit_slider.textChanged.connect(lambda text: update_slider_name(main_window, text))
    main_window.name_edit_slider.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_slider.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_slider)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_slider_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_slider = QSpinBox()
    main_window.tag_spin_slider.setRange(0, 255)
    main_window.tag_spin_slider.setValue(main_window.current_shape.tag)
    main_window.tag_spin_slider.valueChanged.connect(lambda value: update_slider_tag(main_window, value))
    main_window.tag_spin_slider.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_slider.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_slider)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1

    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_slider = QSpinBox()
    main_window.pos_x_spin_slider.setRange(0, 480)
    main_window.pos_x_spin_slider.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_slider.valueChanged.connect(lambda value: update_slider_position(main_window))
    main_window.pos_x_spin_slider.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_slider.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_slider)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_slider = QSpinBox()
    main_window.pos_y_spin_slider.setRange(0, 272)
    main_window.pos_y_spin_slider.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_slider.valueChanged.connect(lambda value: update_slider_position(main_window))
    main_window.pos_y_spin_slider.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_slider.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_slider)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_slider = QSpinBox()
    main_window.width_spin_slider.setRange(100, 480)
    main_window.width_spin_slider.setValue(main_window.current_shape.get_width())
    main_window.width_spin_slider.valueChanged.connect(lambda value: update_slider_size(main_window, value))
    main_window.width_spin_slider.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_slider.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_slider)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.height_spin_slider = QSpinBox()
    main_window.height_spin_slider.setRange(50, 272)
    main_window.height_spin_slider.setValue(main_window.current_shape.get_height())
    main_window.height_spin_slider.valueChanged.connect(lambda value: update_slider_size(main_window, value))
    main_window.height_spin_slider.setStyleSheet("color: black; background-color: white;")
    main_window.height_spin_slider.setFixedWidth(60)
    height_layout.addWidget(main_window.height_spin_slider)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Knob Color (Progress color - plavi krug)
    knob_color_layout = QHBoxLayout()
    knob_color_layout.setContentsMargins(20, 5, 10, 5)
    knob_color_label = QLabel("Knob Color:")
    knob_color_label.setStyleSheet("color: white; font-size: 14px;")
    knob_color_layout.addWidget(knob_color_label)
    knob_color_layout.addStretch(1)
    main_window.knob_color_rect_slider = ColorRectangle(main_window.current_shape.progress_color.name())
    main_window.knob_color_rect_slider.mousePressEvent = lambda e: change_slider_knob_color(main_window)
    knob_color_layout.addWidget(main_window.knob_color_rect_slider)
    knob_color_widget = QWidget()
    knob_color_widget.setLayout(knob_color_layout)
    main_window.properties_layout.insertWidget(current_index, knob_color_widget)
    current_index += 1

    # Background Color Left (leva strana - progress)
    bg_left_color_layout = QHBoxLayout()
    bg_left_color_layout.setContentsMargins(20, 5, 10, 5)
    bg_left_color_label = QLabel("Background Color Left:")
    bg_left_color_label.setStyleSheet("color: white; font-size: 14px;")
    bg_left_color_layout.addWidget(bg_left_color_label)
    bg_left_color_layout.addStretch(1)
    main_window.bg_left_color_rect_slider = ColorRectangle(main_window.current_shape.thumb_color.name())
    main_window.bg_left_color_rect_slider.mousePressEvent = lambda e: change_slider_background_left_color(main_window)
    bg_left_color_layout.addWidget(main_window.bg_left_color_rect_slider)
    bg_left_widget = QWidget()
    bg_left_widget.setLayout(bg_left_color_layout)
    main_window.properties_layout.insertWidget(current_index, bg_left_widget)
    current_index += 1

    # Background Color Right (desna strana - track)
    bg_right_color_layout = QHBoxLayout()
    bg_right_color_layout.setContentsMargins(20, 5, 10, 5)
    bg_right_color_label = QLabel("Background Color Right:")
    bg_right_color_label.setStyleSheet("color: white; font-size: 14px;")
    bg_right_color_layout.addWidget(bg_right_color_label)
    bg_right_color_layout.addStretch(1)
    main_window.bg_right_color_rect_slider = ColorRectangle(main_window.current_shape.track_color.name())
    main_window.bg_right_color_rect_slider.mousePressEvent = lambda e: change_slider_background_right_color(main_window)
    bg_right_color_layout.addWidget(main_window.bg_right_color_rect_slider)
    bg_right_widget = QWidget()
    bg_right_widget.setLayout(bg_right_color_layout)
    main_window.properties_layout.insertWidget(current_index, bg_right_widget)
    current_index += 1

    # 3D Checkbox (dodaj ovu funkciju ako želiš 3D efekat)
    _3d_layout = QHBoxLayout()
    _3d_layout.setContentsMargins(20, 5, 10, 5)
    _3d_label = QLabel("3D:")
    _3d_label.setStyleSheet("color: white; font-size: 14px;")
    _3d_layout.addWidget(_3d_label)
    _3d_layout.addStretch(1)
    main_window._3d_checkbox_slider = QCheckBox()
    main_window._3d_checkbox_slider.setChecked(getattr(main_window.current_shape, '_3d', False))
    main_window._3d_checkbox_slider.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window._3d_checkbox_slider.stateChanged.connect(lambda state: update_slider_3d(main_window, state))
    _3d_layout.addWidget(main_window._3d_checkbox_slider)
    _3d_widget = QWidget()
    _3d_widget.setLayout(_3d_layout)
    main_window.properties_layout.insertWidget(current_index, _3d_widget)
    current_index += 1

    # 5. VALUE SECTION
    value_label = QLabel("Value")
    value_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, value_label)
    current_index += 1

    # Range (maksimalna vrednost)
    range_layout = QHBoxLayout()
    range_layout.setContentsMargins(20, 5, 10, 5)
    range_label = QLabel("Range:")
    range_label.setStyleSheet("color: white; font-size: 14px;")
    range_layout.addWidget(range_label)
    range_layout.addStretch(1)
    main_window.range_spin_slider = QSpinBox()
    main_window.range_spin_slider.setRange(1, 1000)
    main_window.range_spin_slider.setValue(100)  # Fiksni range za slider (0-100)
    main_window.range_spin_slider.setEnabled(False)  # Disable jer je slider fiksan 0-100
    main_window.range_spin_slider.setStyleSheet("color: black; background-color: #e0e0e0;")
    main_window.range_spin_slider.setFixedWidth(60)
    range_layout.addWidget(main_window.range_spin_slider)
    range_widget = QWidget()
    range_widget.setLayout(range_layout)
    main_window.properties_layout.insertWidget(current_index, range_widget)
    current_index += 1

    # Value (trenutna vrednost)
    value_val_layout = QHBoxLayout()
    value_val_layout.setContentsMargins(20, 5, 10, 5)
    value_val_label = QLabel("Value:")
    value_val_label.setStyleSheet("color: white; font-size: 14px;")
    value_val_layout.addWidget(value_val_label)
    value_val_layout.addStretch(1)
    main_window.value_spin_slider = QSpinBox()
    main_window.value_spin_slider.setRange(0, 100)
    main_window.value_spin_slider.setValue(main_window.current_shape.get_value())
    main_window.value_spin_slider.valueChanged.connect(lambda value: update_slider_value(main_window, value))
    main_window.value_spin_slider.setStyleSheet("color: black; background-color: white;")
    main_window.value_spin_slider.setFixedWidth(60)
    value_val_layout.addWidget(main_window.value_spin_slider)
    value_val_widget = QWidget()
    value_val_widget.setLayout(value_val_layout)
    main_window.properties_layout.insertWidget(current_index, value_val_widget)
    current_index += 1

    return current_index

# CALLBACK METODE ZA SLIDER:

def update_slider_tag(main_window, value):
    """Ažurira tag vrednost za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_slider_background_left_color(main_window):
    """Menja boju pozadine sa leve strane (progress deo) slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        color = QColorDialog.getColor(main_window.current_shape.thumb_color)
        if color.isValid():
            main_window.current_shape.set_thumb_color(color)
            main_window.bg_left_color_rect_slider.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_slider_background_right_color(main_window):
    """Menja boju pozadine sa desne strane (track) slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        color = QColorDialog.getColor(main_window.current_shape.track_color)
        if color.isValid():
            main_window.current_shape.set_track_color(color)
            main_window.bg_right_color_rect_slider.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_slider_active(main_window, state):
    """Ažurira active status za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = active
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_slider_visible(main_window, state):
    """Ažurira visible status za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(visible)
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_slider_static(main_window, state):
    """Ažurira static status za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = static
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

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
                main_window.all_slider_dicts[text] = main_window.current_shape.get_properties_dict()

def update_slider_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_slider_position(main_window):
    """Ažurira poziciju slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        if hasattr(main_window, 'pos_x_spin_slider') and hasattr(main_window, 'pos_y_spin_slider'):
            main_window.current_shape.move(main_window.pos_x_spin_slider.value(), main_window.pos_y_spin_slider.value())
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_slider_size(main_window, value):
    """Ažurira veličinu slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        if hasattr(main_window, 'width_spin_slider') and hasattr(main_window, 'height_spin_slider'):
            main_window.current_shape.set_size(main_window.width_spin_slider.value(), main_window.height_spin_slider.value())
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_slider_knob_color(main_window):
    """Menja boju knob-a (plavi krug) slider-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        color = QColorDialog.getColor(main_window.current_shape.progress_color)
        if color.isValid():
            main_window.current_shape.set_progress_color(color)
            main_window.knob_color_rect_slider.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_slider_dicts'):
                main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()


def update_slider_3d(main_window, state):
    """Ažurira 3D efekat za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(use_3d)  # Koristi setter metodu
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_slider_value(main_window, value):
    """Ažurira trenutnu vrednost za slider"""
    if main_window.current_shape and isinstance(main_window.current_shape, SliderWidget):
        main_window.current_shape.set_value(value)
        if hasattr(main_window, 'all_slider_dicts'):
            main_window.all_slider_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

#-------------------------------------------------------------------------------------------------------------------------------
# SCROLLBAR METHODS - ISPRAVLJENE
def showScrollBarProperties(main_window, current_index):
    """Prikazuje properties za ScrollBarWidget"""
    # Ako scrollbar nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "ScrollBar")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_scrollbar = QCheckBox()
    main_window.active_checkbox_scrollbar.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_scrollbar.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_scrollbar.stateChanged.connect(lambda state: update_scrollbar_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_scrollbar)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_scrollbar = QCheckBox()
    main_window.visible_checkbox_scrollbar.setChecked(main_window.current_shape.visible)
    main_window.visible_checkbox_scrollbar.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_scrollbar.stateChanged.connect(lambda state: update_scrollbar_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_scrollbar)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_scrollbar = QCheckBox()
    main_window.static_checkbox_scrollbar.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_scrollbar.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_scrollbar.stateChanged.connect(lambda state: update_scrollbar_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_scrollbar)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. SCROLLBAR NAME SECTION
    name_label = QLabel("ScrollBar Name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_scrollbar = QLineEdit()
    main_window.name_edit_scrollbar.setText(main_window.current_shape.custom_name)
    main_window.name_edit_scrollbar.textChanged.connect(lambda text: update_scrollbar_name(main_window, text))
    main_window.name_edit_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_scrollbar.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_scrollbar)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_scroll_bar_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_scrollbar = QSpinBox()
    main_window.tag_spin_scrollbar.setRange(0, 255)
    main_window.tag_spin_scrollbar.setValue(main_window.current_shape.tag)
    main_window.tag_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_tag(main_window, value))
    main_window.tag_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_scrollbar.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_scrollbar)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1

    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_scrollbar = QSpinBox()
    main_window.pos_x_spin_scrollbar.setRange(0, 480)
    main_window.pos_x_spin_scrollbar.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_position(main_window))
    main_window.pos_x_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_scrollbar.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_scrollbar)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_scrollbar = QSpinBox()
    main_window.pos_y_spin_scrollbar.setRange(0, 272)
    main_window.pos_y_spin_scrollbar.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_position(main_window))
    main_window.pos_y_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_scrollbar.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_scrollbar)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_scrollbar = QSpinBox()
    main_window.width_spin_scrollbar.setRange(100, 480)
    main_window.width_spin_scrollbar.setValue(main_window.current_shape.get_width())
    main_window.width_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_size(main_window))
    main_window.width_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_scrollbar.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_scrollbar)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.height_spin_scrollbar = QSpinBox()
    main_window.height_spin_scrollbar.setRange(10, 272)  # Promenjeno min na 10
    main_window.height_spin_scrollbar.setValue(main_window.current_shape.get_height())
    main_window.height_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_size(main_window))
    main_window.height_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.height_spin_scrollbar.setFixedWidth(60)
    height_layout.addWidget(main_window.height_spin_scrollbar)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Thumb Color
    thumb_color_layout = QHBoxLayout()
    thumb_color_layout.setContentsMargins(20, 5, 10, 5)
    thumb_color_label = QLabel("Thumb Color:")
    thumb_color_label.setStyleSheet("color: white; font-size: 14px;")
    thumb_color_layout.addWidget(thumb_color_label)
    thumb_color_layout.addStretch(1)
    main_window.thumb_color_rect_scrollbar = ColorRectangle(main_window.current_shape.thumb_color.name())
    main_window.thumb_color_rect_scrollbar.mousePressEvent = lambda e: change_scrollbar_thumb_color(main_window)
    thumb_color_layout.addWidget(main_window.thumb_color_rect_scrollbar)
    thumb_color_widget = QWidget()
    thumb_color_widget.setLayout(thumb_color_layout)
    main_window.properties_layout.insertWidget(current_index, thumb_color_widget)
    current_index += 1

    # Track Color
    track_color_layout = QHBoxLayout()
    track_color_layout.setContentsMargins(20, 5, 10, 5)
    track_color_label = QLabel("Track Color:")
    track_color_label.setStyleSheet("color: white; font-size: 14px;")
    track_color_layout.addWidget(track_color_label)
    track_color_layout.addStretch(1)
    main_window.track_color_rect_scrollbar = ColorRectangle(main_window.current_shape.track_color.name())
    main_window.track_color_rect_scrollbar.mousePressEvent = lambda e: change_scrollbar_track_color(main_window)
    track_color_layout.addWidget(main_window.track_color_rect_scrollbar)
    track_color_widget = QWidget()
    track_color_widget.setLayout(track_color_layout)
    main_window.properties_layout.insertWidget(current_index, track_color_widget)
    current_index += 1

    # 3D Checkbox
    _3d_layout = QHBoxLayout()
    _3d_layout.setContentsMargins(20, 5, 10, 5)
    _3d_label = QLabel("3D:")
    _3d_label.setStyleSheet("color: white; font-size: 14px;")
    _3d_layout.addWidget(_3d_label)
    _3d_layout.addStretch(1)
    main_window._3d_checkbox_scrollbar = QCheckBox()
    main_window._3d_checkbox_scrollbar.setChecked(getattr(main_window.current_shape, '_3d', True))
    main_window._3d_checkbox_scrollbar.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window._3d_checkbox_scrollbar.stateChanged.connect(lambda state: update_scrollbar_3d(main_window, state))
    _3d_layout.addWidget(main_window._3d_checkbox_scrollbar)
    _3d_widget = QWidget()
    _3d_widget.setLayout(_3d_layout)
    main_window.properties_layout.insertWidget(current_index, _3d_widget)
    current_index += 1

    # 5. VALUE SECTION
    value_label = QLabel("Value")
    value_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, value_label)
    current_index += 1

    # Range (opseg vrednosti)
    range_layout = QHBoxLayout()
    range_layout.setContentsMargins(20, 5, 10, 5)
    range_label = QLabel("Range:")
    range_label.setStyleSheet("color: white; font-size: 14px;")
    range_layout.addWidget(range_label)
    range_layout.addStretch(1)
    main_window.range_spin_scrollbar = QSpinBox()
    main_window.range_spin_scrollbar.setRange(1, 1000)
    main_window.range_spin_scrollbar.setValue(main_window.current_shape.range_value)
    main_window.range_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_range(main_window, value))
    main_window.range_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.range_spin_scrollbar.setFixedWidth(60)
    range_layout.addWidget(main_window.range_spin_scrollbar)
    range_widget = QWidget()
    range_widget.setLayout(range_layout)
    main_window.properties_layout.insertWidget(current_index, range_widget)
    current_index += 1

    # Current Value (trenutna pozicija scroll bar-a)
    current_value_layout = QHBoxLayout()
    current_value_layout.setContentsMargins(20, 5, 10, 5)
    current_value_label = QLabel("Current Value:")
    current_value_label.setStyleSheet("color: white; font-size: 14px;")
    current_value_layout.addWidget(current_value_label)
    current_value_layout.addStretch(1)
    main_window.current_value_spin_scrollbar = QSpinBox()
    main_window.current_value_spin_scrollbar.setRange(0, main_window.current_shape.range_value)
    main_window.current_value_spin_scrollbar.setValue(main_window.current_shape.current_value)
    main_window.current_value_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_current_value(main_window, value))
    main_window.current_value_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.current_value_spin_scrollbar.setFixedWidth(60)
    current_value_layout.addWidget(main_window.current_value_spin_scrollbar)
    current_value_widget = QWidget()
    current_value_widget.setLayout(current_value_layout)
    main_window.properties_layout.insertWidget(current_index, current_value_widget)
    current_index += 1

    # Knob Size (veličina thumb-a u procentima)
    knob_size_layout = QHBoxLayout()
    knob_size_layout.setContentsMargins(20, 5, 10, 5)
    knob_size_label = QLabel("Knob Size (%):")
    knob_size_label.setStyleSheet("color: white; font-size: 14px;")
    knob_size_layout.addWidget(knob_size_label)
    knob_size_layout.addStretch(1)
    main_window.knob_size_spin_scrollbar = QSpinBox()
    main_window.knob_size_spin_scrollbar.setRange(10, 100)  # 10-100%
    main_window.knob_size_spin_scrollbar.setValue(main_window.current_shape.knob_size)
    main_window.knob_size_spin_scrollbar.valueChanged.connect(lambda value: update_scrollbar_knob_size(main_window, value))
    main_window.knob_size_spin_scrollbar.setStyleSheet("color: black; background-color: white;")
    main_window.knob_size_spin_scrollbar.setFixedWidth(60)
    knob_size_layout.addWidget(main_window.knob_size_spin_scrollbar)
    knob_size_widget = QWidget()
    knob_size_widget.setLayout(knob_size_layout)
    main_window.properties_layout.insertWidget(current_index, knob_size_widget)
    current_index += 1

    return current_index

# ISPRAVLJENE CALLBACK METODE ZA SCROLLBAR:

def update_scrollbar_tag(main_window, value):
    """Ažurira tag vrednost za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_scrollbar_dicts'):
            main_window.all_scrollbar_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

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
        main_window.current_shape.set_visible(visible)

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
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

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
            main_window.current_shape.set_size(
                main_window.width_spin_scrollbar.value(), 
                main_window.height_spin_scrollbar.value()
            )

def change_scrollbar_thumb_color(main_window):
    """Menja boju thumb-a scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.thumb_color)
        if color.isValid():
            main_window.current_shape.set_thumb_color(color)
            main_window.thumb_color_rect_scrollbar.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")

def change_scrollbar_track_color(main_window):
    """Menja boju track-a scrollbar-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.track_color)
        if color.isValid():
            main_window.current_shape.set_track_color(color)
            main_window.track_color_rect_scrollbar.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")

def update_scrollbar_3d(main_window, state):
    """Ažurira 3D efekat za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        use_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(use_3d)

def update_scrollbar_range(main_window, value):
    """Ažurira range za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.set_range(value)
        # Ažuriraj max vrednost za current_value spin
        if hasattr(main_window, 'current_value_spin_scrollbar'):
            main_window.current_value_spin_scrollbar.setRange(0, value)

def update_scrollbar_current_value(main_window, value):
    """Ažurira trenutnu vrednost za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.set_current_value(value)

def update_scrollbar_knob_size(main_window, value):
    """Ažurira veličinu thumb-a za scrollbar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ScrollBarWidget):
        main_window.current_shape.set_knob_size(value)

#-------------------------------------------------------------------------------------------------------------------------------

# PROGRESS BAR FUNCTIONS - konzistentno sa ostalim widget-ima
def showProgressBarProperties(main_window, current_index):
    """Prikazuje properties za ProgressBarWidget"""
    # Status
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.progress_active_checkbox = QCheckBox()
    main_window.progress_active_checkbox.setChecked(main_window.current_shape.active)
    main_window.progress_active_checkbox.stateChanged.connect(lambda state: updateProgressBarActive(main_window, state))
    main_window.progress_active_checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    active_layout.addWidget(main_window.progress_active_checkbox)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.progress_visible_checkbox = QCheckBox()
    main_window.progress_visible_checkbox.setChecked(main_window.current_shape.visible)
    main_window.progress_visible_checkbox.stateChanged.connect(lambda state: updateProgressBarVisible(main_window, state))
    main_window.progress_visible_checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    visible_layout.addWidget(main_window.progress_visible_checkbox)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.progress_static_checkbox = QCheckBox()
    main_window.progress_static_checkbox.setChecked(main_window.current_shape.static)
    main_window.progress_static_checkbox.stateChanged.connect(lambda state: updateProgressBarStatic(main_window, state))
    main_window.progress_static_checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    static_layout.addWidget(main_window.progress_static_checkbox)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # Progress bar name
    name_label = QLabel("Progress bar name")
    name_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name
    name_layout = QHBoxLayout()
    name_layout.setContentsMargins(20, 5, 10, 5)
    name_text_label = QLabel("Name:")
    name_text_label.setStyleSheet("color: white; font-size: 14px;")
    name_layout.addWidget(name_text_label)
    main_window.progress_name_edit = QLineEdit(main_window.current_shape.custom_name)
    main_window.progress_name_edit.setStyleSheet("color: black; background-color: white;")
    main_window.progress_name_edit.textChanged.connect(lambda text: updateProgressBarName(main_window))
    name_layout.addWidget(main_window.progress_name_edit)
    name_widget = QWidget()
    name_widget.setLayout(name_layout)
    main_window.properties_layout.insertWidget(current_index, name_widget)
    current_index += 1

    # Stack order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_progress_bar_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Geometry
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.progress_pos_x_spin = QSpinBox()
    main_window.progress_pos_x_spin.setRange(0, 480)
    main_window.progress_pos_x_spin.setValue(main_window.current_shape.x())
    main_window.progress_pos_x_spin.valueChanged.connect(lambda value: updateProgressBarPosition(main_window))
    main_window.progress_pos_x_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_pos_x_spin.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.progress_pos_x_spin)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.progress_pos_y_spin = QSpinBox()
    main_window.progress_pos_y_spin.setRange(0, 272)
    main_window.progress_pos_y_spin.setValue(main_window.current_shape.y())
    main_window.progress_pos_y_spin.valueChanged.connect(lambda value: updateProgressBarPosition(main_window))
    main_window.progress_pos_y_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_pos_y_spin.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.progress_pos_y_spin)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.progress_width_spin = QSpinBox()
    main_window.progress_width_spin.setRange(50, 480)
    main_window.progress_width_spin.setValue(main_window.current_shape.get_width())
    main_window.progress_width_spin.valueChanged.connect(lambda value: updateProgressBarSize(main_window))
    main_window.progress_width_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_width_spin.setFixedWidth(60)
    width_layout.addWidget(main_window.progress_width_spin)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.progress_height_spin = QSpinBox()
    main_window.progress_height_spin.setRange(1, 272)
    main_window.progress_height_spin.setValue(main_window.current_shape.get_height())
    main_window.progress_height_spin.valueChanged.connect(lambda value: updateProgressBarSize(main_window))
    main_window.progress_height_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_height_spin.setFixedWidth(60)
    height_layout.addWidget(main_window.progress_height_spin)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1

    # Color Adjust
    color_label = QLabel("Color Adjust")
    color_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_label)
    current_index += 1

    # Progress color
    progress_color_layout = QHBoxLayout()
    progress_color_layout.setContentsMargins(20, 5, 10, 5)
    progress_color_label = QLabel("Progress color:")
    progress_color_label.setStyleSheet("color: white; font-size: 14px;")
    progress_color_layout.addWidget(progress_color_label)
    progress_color_layout.addStretch(1)
    main_window.progress_progress_color_rect = ColorRectangle(main_window.current_shape.progress_color.name())
    main_window.progress_progress_color_rect.mousePressEvent = lambda e: changeProgressBarProgressColor(main_window)
    main_window.progress_progress_color_rect.setCursor(Qt.CursorShape.PointingHandCursor)
    progress_color_layout.addWidget(main_window.progress_progress_color_rect)
    progress_color_widget = QWidget()
    progress_color_widget.setLayout(progress_color_layout)
    main_window.properties_layout.insertWidget(current_index, progress_color_widget)
    current_index += 1

    # Background color
    background_color_layout = QHBoxLayout()
    background_color_layout.setContentsMargins(20, 5, 10, 5)
    background_color_label = QLabel("Background color:")
    background_color_label.setStyleSheet("color: white; font-size: 14px;")
    background_color_layout.addWidget(background_color_label)
    background_color_layout.addStretch(1)
    main_window.progress_background_color_rect = ColorRectangle(main_window.current_shape.bar_color.name())
    main_window.progress_background_color_rect.mousePressEvent = lambda e: changeProgressBarBackgroundColor(main_window)
    main_window.progress_background_color_rect.setCursor(Qt.CursorShape.PointingHandCursor)
    background_color_layout.addWidget(main_window.progress_background_color_rect)
    background_color_widget = QWidget()
    background_color_widget.setLayout(background_color_layout)
    main_window.properties_layout.insertWidget(current_index, background_color_widget)
    current_index += 1

    # 3D
    _3d_layout = QHBoxLayout()
    _3d_layout.setContentsMargins(20, 5, 10, 5)
    _3d_label = QLabel("3D:")
    _3d_label.setStyleSheet("color: white; font-size: 14px;")
    _3d_layout.addWidget(_3d_label)
    _3d_layout.addStretch(1)
    main_window.progress_3d_checkbox = QCheckBox()
    main_window.progress_3d_checkbox.setChecked(main_window.current_shape._3d)
    main_window.progress_3d_checkbox.stateChanged.connect(lambda state: updateProgressBarThreeD(main_window, state))
    main_window.progress_3d_checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    _3d_layout.addWidget(main_window.progress_3d_checkbox)
    _3d_widget = QWidget()
    _3d_widget.setLayout(_3d_layout)
    main_window.properties_layout.insertWidget(current_index, _3d_widget)
    current_index += 1

    # Value
    value_label = QLabel("Value")
    value_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, value_label)
    current_index += 1

    # Range
    range_layout = QHBoxLayout()
    range_layout.setContentsMargins(20, 5, 10, 5)
    range_label = QLabel("Range:")
    range_label.setStyleSheet("color: white; font-size: 14px;")
    range_layout.addWidget(range_label)
    main_window.progress_min_spin = QSpinBox()
    main_window.progress_min_spin.setRange(-1000, 1000)
    main_window.progress_min_spin.setValue(main_window.current_shape.min_value)
    main_window.progress_min_spin.valueChanged.connect(lambda value: updateProgressBarRange(main_window))
    main_window.progress_min_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_min_spin.setFixedWidth(60)
    range_layout.addWidget(main_window.progress_min_spin)
    
    range_to_label = QLabel("to")
    range_to_label.setStyleSheet("color: white; font-size: 14px;")
    range_layout.addWidget(range_to_label)
    
    main_window.progress_max_spin = QSpinBox()
    main_window.progress_max_spin.setRange(-1000, 1000)
    main_window.progress_max_spin.setValue(main_window.current_shape.max_value)
    main_window.progress_max_spin.valueChanged.connect(lambda value: updateProgressBarRange(main_window))
    main_window.progress_max_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_max_spin.setFixedWidth(60)
    range_layout.addWidget(main_window.progress_max_spin)
    
    range_widget = QWidget()
    range_widget.setLayout(range_layout)
    main_window.properties_layout.insertWidget(current_index, range_widget)
    current_index += 1

    # Value
    value_spin_layout = QHBoxLayout()
    value_spin_layout.setContentsMargins(20, 5, 10, 5)
    value_spin_label = QLabel("Value:")
    value_spin_label.setStyleSheet("color: white; font-size: 14px;")
    value_spin_layout.addWidget(value_spin_label)
    value_spin_layout.addStretch(1)
    main_window.progress_value_spin = QSpinBox()
    main_window.progress_value_spin.setRange(-1000, 1000)
    main_window.progress_value_spin.setValue(main_window.current_shape.value)
    main_window.progress_value_spin.valueChanged.connect(lambda value: updateProgressBarValue(main_window))
    main_window.progress_value_spin.setStyleSheet("color: black; background-color: white;")
    main_window.progress_value_spin.setFixedWidth(60)
    value_spin_layout.addWidget(main_window.progress_value_spin)
    value_spin_widget = QWidget()
    value_spin_widget.setLayout(value_spin_layout)
    main_window.properties_layout.insertWidget(current_index, value_spin_widget)
    current_index += 1

    return current_index

def updateProgressBarActive(main_window, state):
    """Ažurira active status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_active(active)
        main_window.current_shape.update_properties_dict()

def updateProgressBarVisible(main_window, state):
    """Ažurira visible status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(visible)
        main_window.current_shape.update_properties_dict()

def updateProgressBarStatic(main_window, state):
    """Ažurira static status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_static(static)
        main_window.current_shape.update_properties_dict()

def updateProgressBarThreeD(main_window, state):
    """Ažurira 3D status za progress bar"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        _3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(_3d)
        main_window.current_shape.update_properties_dict()

def updateProgressBarName(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        main_window.current_shape.custom_name = main_window.progress_name_edit.text()
        main_window.current_shape.update_properties_dict()

def update_progress_bar_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def updateProgressBarPosition(main_window):
    """Ažurira poziciju progress bar-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        if hasattr(main_window, 'progress_pos_x_spin') and hasattr(main_window, 'progress_pos_y_spin'):
            x = main_window.progress_pos_x_spin.value()
            y = main_window.progress_pos_y_spin.value()
            # OVO ĆE POZVATI OVERRIDE MOVE METODU KOJA ĆE AŽURIRATI SPIN BOX-OVE
            main_window.current_shape.move(x, y)
            main_window.current_shape.update_properties_dict()

def updateProgressBarSize(main_window):
    """Ažurira veličinu progress bar-a kada se promeni u properties baru"""
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        if hasattr(main_window, 'progress_width_spin') and hasattr(main_window, 'progress_height_spin'):
            width = main_window.progress_width_spin.value()
            height = main_window.progress_height_spin.value()
            # OVO ĆE POZVATI SET_SIZE METODU KOJA ĆE AŽURIRATI SPIN BOX-OVE
            main_window.current_shape.set_size(width, height)
            # Rečnik će se ažurirati unutar set_size

def changeProgressBarProgressColor(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.progress_color)
        if color.isValid():
            main_window.current_shape.set_progress_color(color)
            main_window.progress_progress_color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            main_window.current_shape.update_properties_dict()

def changeProgressBarBackgroundColor(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        color = QColorDialog.getColor(main_window.current_shape.bar_color)
        if color.isValid():
            main_window.current_shape.set_bar_color(color)
            main_window.progress_background_color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            main_window.current_shape.update_properties_dict()

def updateProgressBarRange(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        min_val = main_window.progress_min_spin.value()
        max_val = main_window.progress_max_spin.value()
        if min_val < max_val:
            main_window.current_shape.set_range(min_val, max_val)
            # Ažuriraj value spin da bude u opsegu
            main_window.progress_value_spin.setRange(min_val, max_val)
            main_window.current_shape.update_properties_dict()

def updateProgressBarValue(main_window):
    if main_window.current_shape and isinstance(main_window.current_shape, ProgressBarWidget):
        main_window.current_shape.set_value(main_window.progress_value_spin.value())
        main_window.current_shape.update_properties_dict()

#-------------------------------------------------------------------------------------------------------------------------------

def showKeysProperties(main_window, current_index):
    """Prikazuje properties za KeysWidget sa novim sekcijama"""
    # Ako keys nema ime, generiši ga
    if not hasattr(main_window.current_shape, 'custom_name') or not main_window.current_shape.custom_name:
        main_window.current_shape.custom_name = generateWidgetName(main_window, "Keys")

    # 1. STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_keys = QCheckBox()
    main_window.active_checkbox_keys.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_keys.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.active_checkbox_keys.stateChanged.connect(lambda state: update_keys_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_keys)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_keys = QCheckBox()
    main_window.visible_checkbox_keys.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_keys.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.visible_checkbox_keys.stateChanged.connect(lambda state: update_keys_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_keys)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_keys = QCheckBox()
    main_window.static_checkbox_keys.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_keys.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window.static_checkbox_keys.stateChanged.connect(lambda state: update_keys_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_keys)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # 2. KEYS NAME SECTION
    name_label = QLabel("Keys Name")
    name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, name_label)
    current_index += 1

    # Name input
    name_input_layout = QHBoxLayout()
    name_input_layout.setContentsMargins(20, 5, 10, 5)
    name_input_label = QLabel("Name:")
    name_input_label.setStyleSheet("color: white; font-size: 14px;")
    name_input_layout.addWidget(name_input_label)
    name_input_layout.addStretch(1)
    main_window.name_edit_keys = QLineEdit()
    main_window.name_edit_keys.setText(main_window.current_shape.custom_name)
    main_window.name_edit_keys.textChanged.connect(lambda text: update_keys_name(main_window, text))
    main_window.name_edit_keys.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_keys.setFixedWidth(100)
    name_input_layout.addWidget(main_window.name_edit_keys)
    name_input_widget = QWidget()
    name_input_widget.setLayout(name_input_layout)
    main_window.properties_layout.insertWidget(current_index, name_input_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_keys_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1
    # 3. GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_keys = QSpinBox()
    main_window.pos_x_spin_keys.setRange(0, 480)
    main_window.pos_x_spin_keys.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_keys.valueChanged.connect(lambda value: update_keys_position(main_window))
    main_window.pos_x_spin_keys.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_keys.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_keys)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_keys = QSpinBox()
    main_window.pos_y_spin_keys.setRange(0, 272)
    main_window.pos_y_spin_keys.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_keys.valueChanged.connect(lambda value: update_keys_position(main_window))
    main_window.pos_y_spin_keys.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_keys.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_keys)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_keys = QSpinBox()
    main_window.width_spin_keys.setRange(100, 480)
    main_window.width_spin_keys.setValue(main_window.current_shape.get_width())
    main_window.width_spin_keys.valueChanged.connect(lambda value: update_keys_size(main_window, value))
    main_window.width_spin_keys.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_keys.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_keys)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.height_spin_keys = QSpinBox()
    main_window.height_spin_keys.setRange(80, 272)
    main_window.height_spin_keys.setValue(main_window.current_shape.get_height())
    main_window.height_spin_keys.valueChanged.connect(lambda value: update_keys_size(main_window, value))
    main_window.height_spin_keys.setStyleSheet("color: black; background-color: white;")
    main_window.height_spin_keys.setFixedWidth(60)
    height_layout.addWidget(main_window.height_spin_keys)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1

    # 4. COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Start Color (gornja boja gradijenta)
    start_color_layout = QHBoxLayout()
    start_color_layout.setContentsMargins(20, 5, 10, 5)
    start_color_label = QLabel("Start Color:")
    start_color_label.setStyleSheet("color: white; font-size: 14px;")
    start_color_layout.addWidget(start_color_label)
    start_color_layout.addStretch(1)
    main_window.start_color_rect_keys = ColorRectangle(main_window.current_shape.key_color_top.name())
    main_window.start_color_rect_keys.mousePressEvent = lambda e: change_keys_start_color(main_window)
    start_color_layout.addWidget(main_window.start_color_rect_keys)
    start_color_widget = QWidget()
    start_color_widget.setLayout(start_color_layout)
    main_window.properties_layout.insertWidget(current_index, start_color_widget)
    current_index += 1

    # End Color (donja boja gradijenta)
    end_color_layout = QHBoxLayout()
    end_color_layout.setContentsMargins(20, 5, 10, 5)
    end_color_label = QLabel("End Color:")
    end_color_label.setStyleSheet("color: white; font-size: 14px;")
    end_color_layout.addWidget(end_color_label)
    end_color_layout.addStretch(1)
    main_window.end_color_rect_keys = ColorRectangle(main_window.current_shape.key_color_bottom.name())
    main_window.end_color_rect_keys.mousePressEvent = lambda e: change_keys_end_color(main_window)
    end_color_layout.addWidget(main_window.end_color_rect_keys)
    end_color_widget = QWidget()
    end_color_widget.setLayout(end_color_layout)
    main_window.properties_layout.insertWidget(current_index, end_color_widget)
    current_index += 1

    # Font Color (boja teksta)
    font_color_layout = QHBoxLayout()
    font_color_layout.setContentsMargins(20, 5, 10, 5)
    font_color_label = QLabel("Font Color:")
    font_color_label.setStyleSheet("color: white; font-size: 14px;")
    font_color_layout.addWidget(font_color_label)
    font_color_layout.addStretch(1)
    main_window.font_color_rect_keys = ColorRectangle(main_window.current_shape.text_color.name())
    main_window.font_color_rect_keys.mousePressEvent = lambda e: change_keys_font_color(main_window)
    font_color_layout.addWidget(main_window.font_color_rect_keys)
    font_color_widget = QWidget()
    font_color_widget.setLayout(font_color_layout)
    main_window.properties_layout.insertWidget(current_index, font_color_widget)
    current_index += 1

    # 3D Checkbox
    _3d_layout = QHBoxLayout()
    _3d_layout.setContentsMargins(20, 5, 10, 5)
    _3d_label = QLabel("3D:")
    _3d_label.setStyleSheet("color: white; font-size: 14px;")
    _3d_layout.addWidget(_3d_label)
    _3d_layout.addStretch(1)
    main_window._3d_checkbox_keys = QCheckBox()
    main_window._3d_checkbox_keys.setChecked(main_window.current_shape.is_3d)
    main_window._3d_checkbox_keys.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
    main_window._3d_checkbox_keys.stateChanged.connect(lambda state: update_keys_3d(main_window, state))
    _3d_layout.addWidget(main_window._3d_checkbox_keys)
    _3d_widget = QWidget()
    _3d_widget.setLayout(_3d_layout)
    main_window.properties_layout.insertWidget(current_index, _3d_widget)
    current_index += 1

    # 5. KEYBOARD TYPE SECTION
    keyboard_type_label = QLabel("Keyboard Type")
    keyboard_type_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, keyboard_type_label)
    current_index += 1

    # Type selection
    type_layout = QHBoxLayout()
    type_layout.setContentsMargins(20, 5, 10, 5)
    type_selection_label = QLabel("Type:")
    type_selection_label.setStyleSheet("color: white; font-size: 14px;")
    type_layout.addWidget(type_selection_label)
    type_layout.addStretch(1)
    main_window.type_combo_keys = QComboBox()
    main_window.type_combo_keys.addItems(["QUERTZ", "NUM"])
    main_window.type_combo_keys.setCurrentText(main_window.current_shape.key_type)
    main_window.type_combo_keys.currentTextChanged.connect(lambda text: update_keys_type(main_window, text))
    main_window.type_combo_keys.setStyleSheet("color: black; background-color: white;")
    main_window.type_combo_keys.setFixedWidth(100)
    type_layout.addWidget(main_window.type_combo_keys)
    type_widget = QWidget()
    type_widget.setLayout(type_layout)
    main_window.properties_layout.insertWidget(current_index, type_widget)
    current_index += 1

    # Font Size
    font_size_layout = QHBoxLayout()
    font_size_layout.setContentsMargins(20, 5, 10, 5)
    font_size_label = QLabel("Font Size:")
    font_size_label.setStyleSheet("color: white; font-size: 14px;")
    font_size_layout.addWidget(font_size_label)
    font_size_layout.addStretch(1)
    main_window.font_size_spin_keys = QSpinBox()
    main_window.font_size_spin_keys.setRange(6, 30)
    main_window.font_size_spin_keys.setValue(getattr(main_window.current_shape, 'font_size', 12))
    main_window.font_size_spin_keys.valueChanged.connect(lambda value: update_keys_font_size(main_window, value))
    main_window.font_size_spin_keys.setStyleSheet("color: black; background-color: white;")
    main_window.font_size_spin_keys.setFixedWidth(60)
    font_size_layout.addWidget(main_window.font_size_spin_keys)
    font_size_widget = QWidget()
    font_size_widget.setLayout(font_size_layout)
    main_window.properties_layout.insertWidget(current_index, font_size_widget)
    current_index += 1

    return current_index

# Dodaj nove callback funkcije i izmeni postojeće:

def update_keys_font_size(main_window, value):
    """Ažurira veličinu fonta za keys"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        main_window.current_shape.set_font_size(value)
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_keys_start_color(main_window):
    """Menja start boju gradijenta tastera"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        color = QColorDialog.getColor(main_window.current_shape.key_color_top)
        if color.isValid():
            main_window.current_shape.set_key_colors(color, main_window.current_shape.key_color_bottom)
            main_window.start_color_rect_keys.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_keys_dicts'):
                main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_keys_end_color(main_window):
    """Menja end boju gradijenta tastera"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        color = QColorDialog.getColor(main_window.current_shape.key_color_bottom)
        if color.isValid():
            main_window.current_shape.set_key_colors(main_window.current_shape.key_color_top, color)
            main_window.end_color_rect_keys.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_keys_dicts'):
                main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_keys_font_color(main_window):
    """Menja boju fonta za tastere"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        color = QColorDialog.getColor(main_window.current_shape.text_color)
        if color.isValid():
            main_window.current_shape.set_text_color(color)
            main_window.font_color_rect_keys.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_keys_dicts'):
                main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

# Izmeni postojeće funkcije da rade sa novim imenima:

def update_keys_3d(main_window, state):
    """Ažurira 3D efekat za keys"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        is_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(is_3d)
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

# Ukloni stare funkcije za boje koje više ne koristimo
# (change_keys_color_top i change_keys_color_bottom)

# Dodaj novi atribut u get_properties_dict u KeysWidget klasi:
# 'font_size': self.font_size

# CALLBACK METODE ZA KEYS:

def update_keys_active(main_window, state):
    """Ažurira active status za keys"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = active
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_keys_visible(main_window, state):
    """Ažurira visible status za keys"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(visible)
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_keys_static(main_window, state):
    """Ažurira static status za keys"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = static
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_keys_name(main_window, text):
    """Ažurira ime keys-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        main_window.current_shape.custom_name = text
        if hasattr(main_window, 'all_keys_dicts'):
            old_name = None
            for name, props in list(main_window.all_keys_dicts.items()):
                if props.get('position') == (main_window.current_shape.x(), main_window.current_shape.y()):
                    old_name = name
                    break
            
            if old_name and old_name != text:
                main_window.all_keys_dicts[text] = main_window.all_keys_dicts.pop(old_name)
            else:
                main_window.all_keys_dicts[text] = main_window.current_shape.get_properties_dict()

def update_keys_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def update_keys_position(main_window):
    """Ažurira poziciju keys-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        if hasattr(main_window, 'pos_x_spin_keys') and hasattr(main_window, 'pos_y_spin_keys'):
            main_window.current_shape.move(main_window.pos_x_spin_keys.value(), main_window.pos_y_spin_keys.value())
            if hasattr(main_window, 'all_keys_dicts'):
                main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_keys_size(main_window, value):
    """Ažurira veličinu keys-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        if hasattr(main_window, 'width_spin_keys') and hasattr(main_window, 'height_spin_keys'):
            width = main_window.width_spin_keys.value()
            height = main_window.height_spin_keys.value()
            main_window.current_shape.set_size(width, height)
            
            if hasattr(main_window, 'all_keys_dicts'):
                main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_keys_type(main_window, text):
    """Ažurira tip tastature"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        main_window.current_shape.set_key_type(text)
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_keys_3d(main_window, state):
    """Ažurira 3D efekat za keys"""
    if main_window.current_shape and isinstance(main_window.current_shape, KeysWidget):
        is_3d = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_3d(is_3d)
        if hasattr(main_window, 'all_keys_dicts'):
            main_window.all_keys_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()


#-------------------------------------------------------------------------------------------------------------------------------

def showImageProperties(main_window, current_index):
    """Prikazuje properties za ImageWidget konzistentno sa drugim widget-ima"""
    
    # STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox = QCheckBox()
    main_window.active_checkbox.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox.stateChanged.connect(lambda state: update_image_active(main_window, state))
    active_layout.addWidget(main_window.active_checkbox)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox = QCheckBox()
    main_window.visible_checkbox.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox.stateChanged.connect(lambda state: update_image_visible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox = QCheckBox()
    main_window.static_checkbox.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox.stateChanged.connect(lambda state: update_image_static(main_window, state))
    static_layout.addWidget(main_window.static_checkbox)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # IMAGE NAME SECTION
    image_name_label = QLabel("Image Name")
    image_name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, image_name_label)
    current_index += 1

    # Name input
    name_layout = QHBoxLayout()
    name_layout.setContentsMargins(20, 5, 10, 5)
    name_label = QLabel("Name:")
    name_label.setStyleSheet("color: white; font-size: 14px;")
    name_layout.addWidget(name_label)
    name_layout.addStretch(1)
    main_window.name_edit = QLineEdit()
    main_window.name_edit.setText(main_window.current_shape.custom_name)
    main_window.name_edit.textChanged.connect(lambda text: update_image_name(main_window, text))
    main_window.name_edit.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit.setFixedWidth(100)
    name_layout.addWidget(main_window.name_edit)
    name_widget = QWidget()
    name_widget.setLayout(name_layout)
    main_window.properties_layout.insertWidget(current_index, name_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin_image = QSpinBox()  # ← button specifično
    main_window.stack_order_spin_image.setRange(1, 100)
    main_window.stack_order_spin_image.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin_image.valueChanged.connect(lambda value: update_image_stack_order(main_window, value))
    main_window.stack_order_spin_image.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin_image.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin_image)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_image = QSpinBox()
    main_window.pos_x_spin_image.setRange(0, 480)
    main_window.pos_x_spin_image.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_image.valueChanged.connect(lambda value: updateImagePosition(main_window))
    main_window.pos_x_spin_image.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_image.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_image)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_image = QSpinBox()
    main_window.pos_y_spin_image.setRange(0, 272)
    main_window.pos_y_spin_image.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_image.valueChanged.connect(lambda value: updateImagePosition(main_window))
    main_window.pos_y_spin_image.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_image.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_image)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_image = QSpinBox()
    main_window.width_spin_image.setRange(100, 480)
    main_window.width_spin_image.setValue(main_window.current_shape.get_width())
    main_window.width_spin_image.valueChanged.connect(lambda: updateImageSize(main_window))
    main_window.width_spin_image.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_image.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_image)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.height_spin_image = QSpinBox()
    main_window.height_spin_image.setRange(80, 272)
    main_window.height_spin_image.setValue(main_window.current_shape.get_height())
    main_window.height_spin_image.valueChanged.connect(lambda: updateImageSize(main_window))
    main_window.height_spin_image.setStyleSheet("color: black; background-color: white;")
    main_window.height_spin_image.setFixedWidth(60)
    height_layout.addWidget(main_window.height_spin_image)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1
    
    # IMAGE SECTION
    image_label = QLabel("Image")
    image_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, image_label)
    current_index += 1

    # Select Image button
    select_image_layout = QHBoxLayout()
    select_image_layout.setContentsMargins(20, 5, 10, 5)
    select_image_label = QLabel("Select image:")
    select_image_label.setStyleSheet("color: white; font-size: 14px;")
    select_image_layout.addWidget(select_image_label)
    select_image_layout.addStretch(1)
    main_window.select_image_button = QPushButton("Browse...")
    main_window.select_image_button.clicked.connect(lambda: select_image_file(main_window))
    main_window.select_image_button.setStyleSheet("color: black; background-color: white;")
    main_window.select_image_button.setFixedWidth(80)
    select_image_layout.addWidget(main_window.select_image_button)
    select_image_widget = QWidget()
    select_image_widget.setLayout(select_image_layout)
    main_window.properties_layout.insertWidget(current_index, select_image_widget)
    current_index += 1

    # FRAME SECTION
    frame_label = QLabel("Frame")
    frame_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, frame_label)
    current_index += 1

    # Frame Enable checkbox
    frame_enable_layout = QHBoxLayout()
    frame_enable_layout.setContentsMargins(20, 5, 10, 5)
    frame_enable_label = QLabel("Enable:")
    frame_enable_label.setStyleSheet("color: white; font-size: 14px;")
    frame_enable_layout.addWidget(frame_enable_label)
    frame_enable_layout.addStretch(1)
    main_window.frame_checkbox = QCheckBox()
    main_window.frame_checkbox.setChecked(main_window.current_shape.frame_enabled)
    main_window.frame_checkbox.stateChanged.connect(lambda state: update_image_frame_enabled(main_window, state))
    frame_enable_layout.addWidget(main_window.frame_checkbox)
    frame_enable_widget = QWidget()
    frame_enable_widget.setLayout(frame_enable_layout)
    main_window.properties_layout.insertWidget(current_index, frame_enable_widget)
    current_index += 1

    # Frame Color
    frame_color_layout = QHBoxLayout()
    frame_color_layout.setContentsMargins(20, 5, 10, 5)
    frame_color_label = QLabel("Frame Color:")
    frame_color_label.setStyleSheet("color: white; font-size: 14px;")
    frame_color_layout.addWidget(frame_color_label)
    frame_color_layout.addStretch(1)
    main_window.frame_color_rect = ColorRectangle(main_window.current_shape.frame_color.name())
    main_window.frame_color_rect.mousePressEvent = lambda e: change_image_frame_color(main_window)
    frame_color_layout.addWidget(main_window.frame_color_rect)
    frame_color_widget = QWidget()
    frame_color_widget.setLayout(frame_color_layout)
    main_window.properties_layout.insertWidget(current_index, frame_color_widget)
    current_index += 1

    # Frame Width
    frame_width_layout = QHBoxLayout()
    frame_width_layout.setContentsMargins(20, 5, 10, 5)
    frame_width_label = QLabel("Width:")
    frame_width_label.setStyleSheet("color: white; font-size: 14px;")
    frame_width_layout.addWidget(frame_width_label)
    frame_width_layout.addStretch(1)
    main_window.frame_width_spin = QSpinBox()
    main_window.frame_width_spin.setRange(0, 20)
    main_window.frame_width_spin.setValue(main_window.current_shape.frame_width)
    main_window.frame_width_spin.valueChanged.connect(lambda value: update_image_frame_width(main_window, value))
    main_window.frame_width_spin.setStyleSheet("color: black; background-color: white;")
    main_window.frame_width_spin.setFixedWidth(60)
    frame_width_layout.addWidget(main_window.frame_width_spin)
    frame_width_widget = QWidget()
    frame_width_widget.setLayout(frame_width_layout)
    main_window.properties_layout.insertWidget(current_index, frame_width_widget)
    current_index += 1

    return current_index

# CALLBACK FUNKCIJE ZA IMAGE WIDGET

def update_image_active(main_window, state):
    """Ažurira active status za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = is_active
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_image_visible(main_window, state):
    """Ažurira visible status za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(is_visible)
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_image_static(main_window, state):
    """Ažurira static status za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = is_static
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

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
            main_window.all_image_dicts[text] = main_window.current_shape.get_properties_dict()

def update_image_stack_order(main_window, value):
    """Ažurira stack order za image"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik - ISPRAVLJENO: all_image_dicts umesto all_button_dicts
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

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
            success = main_window.current_shape.set_image_path(file_path)
            if success and hasattr(main_window, 'all_image_dicts'):
                main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_image_frame_enabled(main_window, state):
    """Ažurira enable status za frame"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        is_enabled = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_frame_enabled(is_enabled)
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def update_image_frame_width(main_window, value):
    """Ažurira debljinu frame-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        main_window.current_shape.set_frame_width(value)
        if hasattr(main_window, 'all_image_dicts'):
            main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def change_image_frame_color(main_window):
    """Menja boju frame-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        color = QColorDialog.getColor(main_window.current_shape.frame_color)
        if color.isValid():
            main_window.current_shape.set_frame_color(color)
            main_window.frame_color_rect.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_image_dicts'):
                main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateImageSize(main_window):
    """Ažurira veličinu image widget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        width = main_window.width_spin_image.value()
        height = main_window.height_spin_image.value()
        main_window.current_shape.set_size(width, height)
        
        # Ažuriraj rečnik
        if hasattr(main_window.current_shape, 'update_properties_dict'):
            main_window.current_shape.update_properties_dict()

def updateImagePosition(main_window):
    """Ažurira poziciju image-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, ImageWidget):
        if hasattr(main_window, 'pos_x_spin_image') and hasattr(main_window, 'pos_y_spin_image'):
            main_window.current_shape.move(main_window.pos_x_spin_image.value(), main_window.pos_y_spin_image.value())
            
            # Ažuriraj rečnik - ISPRAVLJENO: all_image_dicts umesto all_keys_dicts
            if hasattr(main_window, 'all_image_dicts'):
                main_window.all_image_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

#-------------------------------------------------------------------------------------------------------------------------------

def showEllipseProperties(main_window, current_index):
    """Prikazuje properties za EllipseWidget"""
    
    # STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_ellipse = QCheckBox()
    main_window.active_checkbox_ellipse.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_ellipse.stateChanged.connect(lambda state: updateEllipseActive(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_ellipse)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_ellipse = QCheckBox()
    main_window.visible_checkbox_ellipse.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_ellipse.stateChanged.connect(lambda state: updateEllipseVisible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_ellipse)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_ellipse = QCheckBox()
    main_window.static_checkbox_ellipse.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_ellipse.stateChanged.connect(lambda state: updateEllipseStatic(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_ellipse)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # ELLIPSE NAME SECTION
    ellipse_name_label = QLabel("Ellipse Name")
    ellipse_name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, ellipse_name_label)
    current_index += 1

    # Name input
    name_layout = QHBoxLayout()
    name_layout.setContentsMargins(20, 5, 10, 5)
    name_label = QLabel("Name:")
    name_label.setStyleSheet("color: white; font-size: 14px;")
    name_layout.addWidget(name_label)
    name_layout.addStretch(1)
    main_window.name_edit_ellipse = QLineEdit()
    main_window.name_edit_ellipse.setText(main_window.current_shape.custom_name)
    main_window.name_edit_ellipse.textChanged.connect(lambda text: updateEllipseName(main_window, text))
    main_window.name_edit_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_ellipse.setFixedWidth(100)
    name_layout.addWidget(main_window.name_edit_ellipse)
    name_widget = QWidget()
    name_widget.setLayout(name_layout)
    main_window.properties_layout.insertWidget(current_index, name_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_ellipse_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # Tag input
    tag_layout = QHBoxLayout()
    tag_layout.setContentsMargins(20, 5, 10, 5)
    tag_input_label = QLabel("Tag value:")
    tag_input_label.setStyleSheet("color: white; font-size: 14px;")
    tag_layout.addWidget(tag_input_label)
    tag_layout.addStretch(1)

    main_window.tag_spin_ellipse = QSpinBox()
    main_window.tag_spin_ellipse.setRange(0, 255)
    main_window.tag_spin_ellipse.setValue(main_window.current_shape.tag)
    main_window.tag_spin_ellipse.valueChanged.connect(lambda value: update_ellipse_tag(main_window, value))
    main_window.tag_spin_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.tag_spin_ellipse.setFixedWidth(60)
    tag_layout.addWidget(main_window.tag_spin_ellipse)

    tag_widget = QWidget()
    tag_widget.setLayout(tag_layout)
    main_window.properties_layout.insertWidget(current_index, tag_widget)
    current_index += 1

    # GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_ellipse = QSpinBox()
    main_window.pos_x_spin_ellipse.setRange(0, 480)
    main_window.pos_x_spin_ellipse.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_ellipse.valueChanged.connect(lambda: updateEllipsePosition(main_window))
    main_window.pos_x_spin_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_ellipse.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_ellipse)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_ellipse = QSpinBox()
    main_window.pos_y_spin_ellipse.setRange(0, 272)
    main_window.pos_y_spin_ellipse.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_ellipse.valueChanged.connect(lambda: updateEllipsePosition(main_window))
    main_window.pos_y_spin_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_ellipse.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_ellipse)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # Width
    width_layout = QHBoxLayout()
    width_layout.setContentsMargins(20, 5, 10, 5)
    width_label = QLabel("Width:")
    width_label.setStyleSheet("color: white; font-size: 14px;")
    width_layout.addWidget(width_label)
    width_layout.addStretch(1)
    main_window.width_spin_ellipse = QSpinBox()
    main_window.width_spin_ellipse.setRange(20, 480)
    main_window.width_spin_ellipse.setValue(main_window.current_shape.get_width())
    main_window.width_spin_ellipse.valueChanged.connect(lambda: updateEllipseSize(main_window))
    main_window.width_spin_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.width_spin_ellipse.setFixedWidth(60)
    width_layout.addWidget(main_window.width_spin_ellipse)
    width_widget = QWidget()
    width_widget.setLayout(width_layout)
    main_window.properties_layout.insertWidget(current_index, width_widget)
    current_index += 1

    # Height
    height_layout = QHBoxLayout()
    height_layout.setContentsMargins(20, 5, 10, 5)
    height_label = QLabel("Height:")
    height_label.setStyleSheet("color: white; font-size: 14px;")
    height_layout.addWidget(height_label)
    height_layout.addStretch(1)
    main_window.height_spin_ellipse = QSpinBox()
    main_window.height_spin_ellipse.setRange(20, 272)
    main_window.height_spin_ellipse.setValue(main_window.current_shape.get_height())
    main_window.height_spin_ellipse.valueChanged.connect(lambda: updateEllipseSize(main_window))
    main_window.height_spin_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.height_spin_ellipse.setFixedWidth(60)
    height_layout.addWidget(main_window.height_spin_ellipse)
    height_widget = QWidget()
    height_widget.setLayout(height_layout)
    main_window.properties_layout.insertWidget(current_index, height_widget)
    current_index += 1

# COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Edges Color
    edges_color_layout = QHBoxLayout()
    edges_color_layout.setContentsMargins(20, 5, 10, 5)
    edges_color_label = QLabel("Edges color:")
    edges_color_label.setStyleSheet("color: white; font-size: 14px;")
    edges_color_layout.addWidget(edges_color_label)
    edges_color_layout.addStretch(1)
    main_window.edges_color_rect_ellipse = ColorRectangle(main_window.current_shape.border_color.name())
    main_window.edges_color_rect_ellipse.mousePressEvent = lambda e: changeEllipseEdgesColor(main_window)
    edges_color_layout.addWidget(main_window.edges_color_rect_ellipse)
    edges_color_widget = QWidget()
    edges_color_widget.setLayout(edges_color_layout)
    main_window.properties_layout.insertWidget(current_index, edges_color_widget)
    current_index += 1

    # Thickness
    thickness_layout = QHBoxLayout()
    thickness_layout.setContentsMargins(20, 5, 10, 5)
    thickness_label = QLabel("Thickness:")
    thickness_label.setStyleSheet("color: white; font-size: 14px;")
    thickness_layout.addWidget(thickness_label)
    thickness_layout.addStretch(1)
    main_window.thickness_spin_ellipse = QSpinBox()
    main_window.thickness_spin_ellipse.setRange(1, 20)
    main_window.thickness_spin_ellipse.setValue(main_window.current_shape.border_width)
    main_window.thickness_spin_ellipse.valueChanged.connect(lambda value: updateEllipseThickness(main_window, value))
    main_window.thickness_spin_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.thickness_spin_ellipse.setFixedWidth(60)
    thickness_layout.addWidget(main_window.thickness_spin_ellipse)
    thickness_widget = QWidget()
    thickness_widget.setLayout(thickness_layout)
    main_window.properties_layout.insertWidget(current_index, thickness_widget)
    current_index += 1

    # Filled checkbox (sa upozorenjem)
    filled_layout = QHBoxLayout()
    filled_layout.setContentsMargins(20, 5, 10, 5)
    filled_label = QLabel("Filled:")
    filled_label.setStyleSheet("color: white; font-size: 14px;")
    filled_layout.addWidget(filled_label)
    filled_layout.addStretch(1)
    main_window.filled_checkbox_ellipse = QCheckBox()
    main_window.filled_checkbox_ellipse.setChecked(main_window.current_shape.fill_enabled)
    main_window.filled_checkbox_ellipse.stateChanged.connect(lambda state: showFilledWarning(main_window, state))
    filled_layout.addWidget(main_window.filled_checkbox_ellipse)
    filled_widget = QWidget()
    filled_widget.setLayout(filled_layout)
    main_window.properties_layout.insertWidget(current_index, filled_widget)
    current_index += 1

    # Gradient Type (samo ako je Filled enabled)
    gradient_type_layout = QHBoxLayout()
    gradient_type_layout.setContentsMargins(20, 5, 10, 5)
    gradient_type_label = QLabel("Gradient type:")
    gradient_type_label.setStyleSheet("color: white; font-size: 14px;")
    gradient_type_layout.addWidget(gradient_type_label)
    gradient_type_layout.addStretch(1)
    main_window.gradient_combo_ellipse = QComboBox()
    main_window.gradient_combo_ellipse.addItems(["Top-Bottom", "Bottom-Top", "Left-Right", "Right-Left"])
    main_window.gradient_combo_ellipse.setCurrentText(main_window.current_shape.gradient_type)
    main_window.gradient_combo_ellipse.currentTextChanged.connect(lambda text: updateEllipseGradientType(main_window, text))
    main_window.gradient_combo_ellipse.setEnabled(main_window.current_shape.fill_enabled)
    main_window.gradient_combo_ellipse.setStyleSheet("color: black; background-color: white;")
    main_window.gradient_combo_ellipse.setFixedWidth(120)
    gradient_type_layout.addWidget(main_window.gradient_combo_ellipse)
    gradient_type_widget = QWidget()
    gradient_type_widget.setLayout(gradient_type_layout)
    main_window.properties_layout.insertWidget(current_index, gradient_type_widget)
    current_index += 1

    # Start Color (samo ako je Filled enabled)
    start_color_layout = QHBoxLayout()
    start_color_layout.setContentsMargins(20, 5, 10, 5)
    start_color_label = QLabel("Start color:")
    start_color_label.setStyleSheet("color: white; font-size: 14px;")
    start_color_layout.addWidget(start_color_label)
    start_color_layout.addStretch(1)
    main_window.start_color_rect_ellipse = ColorRectangle(main_window.current_shape.gradient_start_color.name())
    main_window.start_color_rect_ellipse.mousePressEvent = lambda e: changeEllipseStartColor(main_window)
    main_window.start_color_rect_ellipse.setEnabled(main_window.current_shape.fill_enabled)
    start_color_layout.addWidget(main_window.start_color_rect_ellipse)
    start_color_widget = QWidget()
    start_color_widget.setLayout(start_color_layout)
    main_window.properties_layout.insertWidget(current_index, start_color_widget)
    current_index += 1

    # End Color (samo ako je Filled enabled)
    end_color_layout = QHBoxLayout()
    end_color_layout.setContentsMargins(20, 5, 10, 5)
    end_color_label = QLabel("End color:")
    end_color_label.setStyleSheet("color: white; font-size: 14px;")
    end_color_layout.addWidget(end_color_label)
    end_color_layout.addStretch(1)
    main_window.end_color_rect_ellipse = ColorRectangle(main_window.current_shape.gradient_end_color.name())
    main_window.end_color_rect_ellipse.mousePressEvent = lambda e: changeEllipseEndColor(main_window)
    main_window.end_color_rect_ellipse.setEnabled(main_window.current_shape.fill_enabled)
    end_color_layout.addWidget(main_window.end_color_rect_ellipse)
    end_color_widget = QWidget()
    end_color_widget.setLayout(end_color_layout)
    main_window.properties_layout.insertWidget(current_index, end_color_widget)
    current_index += 1

    return current_index


def update_ellipse_tag(main_window, value):
    """Ažurira tag vrednost za ellipse"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        main_window.current_shape.tag = value
        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def showFilledWarning(main_window, state):
    """Prikazuje upozorenje kada se enabluje Filled opcija"""
    global _show_ellipse_warning
    
    is_filled = (state == Qt.CheckState.Checked.value)
    
    if is_filled and _show_ellipse_warning:
        warning_dialog = QDialog(main_window)
        warning_dialog.setWindowTitle("Information")
        warning_dialog.setFixedSize(400, 200)
        
        layout = QVBoxLayout(warning_dialog)
        
        # Informacioni tekst
        info_label = QLabel("This option is resource intensive and may cause unpredictable display behavior.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: white; font-size: 12px; padding: 10px;")
        layout.addWidget(info_label)
        
        # "Do not show again" checkbox
        dont_show_layout = QHBoxLayout()
        dont_show_checkbox = QCheckBox("Do not show again")
        dont_show_checkbox.setStyleSheet("color: white;")
        dont_show_layout.addWidget(dont_show_checkbox)
        dont_show_layout.addStretch(1)
        layout.addLayout(dont_show_layout)
        
        # OK button
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(warning_dialog.accept)
        ok_button.setFixedWidth(80)
        button_layout.addStretch(1)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)
        
        warning_dialog.exec()
        
        # Sačuvaj preferenciju samo za ovu sesiju
        if dont_show_checkbox.isChecked():
            _show_ellipse_warning = False

    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        main_window.current_shape.set_fill_enabled(is_filled)
    
    # Ažuriraj enable status drugih kontrola
    if hasattr(main_window, 'gradient_combo_ellipse'):
        main_window.gradient_combo_ellipse.setEnabled(is_filled)
    
    if hasattr(main_window, 'start_color_rect_ellipse'):
        main_window.start_color_rect_ellipse.setEnabled(is_filled)
    
    if hasattr(main_window, 'end_color_rect_ellipse'):
        main_window.end_color_rect_ellipse.setEnabled(is_filled)
    
    # Ažuriraj rečnik
    if hasattr(main_window, 'all_ellipse_dicts'):
        main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()
    
    # OBAVEZNO pozovi update() da bi se nacrtao ponovo
    main_window.current_shape.update()

# CALLBACK FUNKCIJE ZA ELLIPSE WIDGET
def updateEllipseActive(main_window, state):
    """Ažurira active status za ellipse"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.active = is_active
        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateEllipseVisible(main_window, state):
    """Ažurira visible status za ellipse"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(is_visible)
        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateEllipseStatic(main_window, state):
    """Ažurira static status za ellipse"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.static = is_static
        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateEllipseName(main_window, text):
    """Ažurira ime ellipse widget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        main_window.current_shape.custom_name = text
        if hasattr(main_window, 'all_ellipse_dicts'):
            old_name = main_window.current_shape.custom_name
            main_window.all_ellipse_dicts[old_name] = main_window.current_shape.get_properties_dict()

def update_ellipse_stack_order(main_window, value):
    """Ažurira stack order za button"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        main_window.current_shape.stack_order = value
        
        # Ažuriraj rečnik
        if hasattr(main_window, 'all_button_dicts'):
            main_window.all_button_dicts[main_window.current_shape.custom_name] = \
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def updateEllipsePosition(main_window):
    """Ažurira poziciju ellipse-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        if hasattr(main_window, 'pos_x_spin_ellipse') and hasattr(main_window, 'pos_y_spin_ellipse'):
            main_window.current_shape.move(
                main_window.pos_x_spin_ellipse.value(),
                main_window.pos_y_spin_ellipse.value()
            )
            if hasattr(main_window, 'all_ellipse_dicts'):
                main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateEllipseSize(main_window):
    """Ažurira veličinu ellipse-a - ovo se poziva direktno iz properties"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        if hasattr(main_window, 'width_spin_ellipse') and hasattr(main_window, 'height_spin_ellipse'):
            width = main_window.width_spin_ellipse.value()
            height = main_window.height_spin_ellipse.value()
            main_window.current_shape.set_size(width, height)
            
            if hasattr(main_window, 'all_ellipse_dicts'):
                main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def changeEllipseEdgesColor(main_window):
    """Menja boju ivica ellipse-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        color = QColorDialog.getColor(main_window.current_shape.border_color)
        if color.isValid():
            main_window.current_shape.set_border_color(color)
            main_window.edges_color_rect_ellipse.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_ellipse_dicts'):
                main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateEllipseThickness(main_window, value):
    """Ažurira debljinu ivica ellipse-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        main_window.current_shape.set_border_width(value)
        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()



def updateEllipseGradientType(main_window, text):
    """Ažurira tip gradijenta za ellipse"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        main_window.current_shape.set_gradient_type(text)
        if hasattr(main_window, 'all_ellipse_dicts'):
            main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def changeEllipseStartColor(main_window):
    """Menja start boju gradijenta ellipse-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        color = QColorDialog.getColor(main_window.current_shape.gradient_start_color)
        if color.isValid():
            main_window.current_shape.set_gradient_colors(color, main_window.current_shape.gradient_end_color)
            main_window.start_color_rect_ellipse.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_ellipse_dicts'):
                main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def changeEllipseEndColor(main_window):
    """Menja end boju gradijenta ellipse-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, EllipseWidget):
        color = QColorDialog.getColor(main_window.current_shape.gradient_end_color)
        if color.isValid():
            main_window.current_shape.set_gradient_colors(main_window.current_shape.gradient_start_color, color)
            main_window.end_color_rect_ellipse.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_ellipse_dicts'):
                main_window.all_ellipse_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

#-------------------------------------------------------------------------------------------------------------------------------

def showNumericProperties(main_window, current_index):
    """Prikazuje properties za NumericWidget"""
    
    # STATUS SECTION
    status_label = QLabel("Status")
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, status_label)
    current_index += 1

    # Active checkbox
    active_layout = QHBoxLayout()
    active_layout.setContentsMargins(20, 5, 10, 5)
    active_label = QLabel("Active:")
    active_label.setStyleSheet("color: white; font-size: 14px;")
    active_layout.addWidget(active_label)
    active_layout.addStretch(1)
    main_window.active_checkbox_numeric = QCheckBox()
    main_window.active_checkbox_numeric.setChecked(getattr(main_window.current_shape, 'active', True))
    main_window.active_checkbox_numeric.stateChanged.connect(lambda state: updateNumericActive(main_window, state))
    active_layout.addWidget(main_window.active_checkbox_numeric)
    active_widget = QWidget()
    active_widget.setLayout(active_layout)
    main_window.properties_layout.insertWidget(current_index, active_widget)
    current_index += 1

    # Visible checkbox
    visible_layout = QHBoxLayout()
    visible_layout.setContentsMargins(20, 5, 10, 5)
    visible_label = QLabel("Visible:")
    visible_label.setStyleSheet("color: white; font-size: 14px;")
    visible_layout.addWidget(visible_label)
    visible_layout.addStretch(1)
    main_window.visible_checkbox_numeric = QCheckBox()
    main_window.visible_checkbox_numeric.setChecked(getattr(main_window.current_shape, 'visible', True))
    main_window.visible_checkbox_numeric.stateChanged.connect(lambda state: updateNumericVisible(main_window, state))
    visible_layout.addWidget(main_window.visible_checkbox_numeric)
    visible_widget = QWidget()
    visible_widget.setLayout(visible_layout)
    main_window.properties_layout.insertWidget(current_index, visible_widget)
    current_index += 1

    # Static checkbox
    static_layout = QHBoxLayout()
    static_layout.setContentsMargins(20, 5, 10, 5)
    static_label = QLabel("Static:")
    static_label.setStyleSheet("color: white; font-size: 14px;")
    static_layout.addWidget(static_label)
    static_layout.addStretch(1)
    main_window.static_checkbox_numeric = QCheckBox()
    main_window.static_checkbox_numeric.setChecked(getattr(main_window.current_shape, 'static', False))
    main_window.static_checkbox_numeric.stateChanged.connect(lambda state: updateNumericStatic(main_window, state))
    static_layout.addWidget(main_window.static_checkbox_numeric)
    static_widget = QWidget()
    static_widget.setLayout(static_layout)
    main_window.properties_layout.insertWidget(current_index, static_widget)
    current_index += 1

    # NUMERIC NAME SECTION
    numeric_name_label = QLabel("Numeric Name")
    numeric_name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, numeric_name_label)
    current_index += 1

    # Name input
    name_layout = QHBoxLayout()
    name_layout.setContentsMargins(20, 5, 10, 5)
    name_label = QLabel("Name:")
    name_label.setStyleSheet("color: white; font-size: 14px;")
    name_layout.addWidget(name_label)
    name_layout.addStretch(1)
    main_window.name_edit_numeric = QLineEdit()
    main_window.name_edit_numeric.setText(main_window.current_shape.custom_name)
    main_window.name_edit_numeric.textChanged.connect(lambda text: updateNumericName(main_window, text))
    main_window.name_edit_numeric.setStyleSheet("color: black; background-color: white;")
    main_window.name_edit_numeric.setFixedWidth(100)
    name_layout.addWidget(main_window.name_edit_numeric)
    name_widget = QWidget()
    name_widget.setLayout(name_layout)
    main_window.properties_layout.insertWidget(current_index, name_widget)
    current_index += 1

    # Stack Order
    stack_order_layout = QHBoxLayout()
    stack_order_layout.setContentsMargins(20, 5, 10, 5)
    stack_order_label = QLabel("Stack order:")
    stack_order_label.setStyleSheet("color: white; font-size: 14px;")
    stack_order_layout.addWidget(stack_order_label)
    stack_order_layout.addStretch(1)
    
    main_window.stack_order_spin = QSpinBox()  # ← button specifično
    main_window.stack_order_spin.setRange(1, 100)
    main_window.stack_order_spin.setValue(main_window.current_shape.stack_order)
    main_window.stack_order_spin.valueChanged.connect(
        lambda value: update_numeric_stack_order(main_window, value))
    main_window.stack_order_spin.setStyleSheet("color: black; background-color: white;")
    main_window.stack_order_spin.setFixedWidth(60)
    stack_order_layout.addWidget(main_window.stack_order_spin)
    
    stack_order_widget = QWidget()
    stack_order_widget.setLayout(stack_order_layout)
    main_window.properties_layout.insertWidget(current_index, stack_order_widget)
    current_index += 1

    # GEOMETRY SECTION
    geometry_label = QLabel("Geometry")
    geometry_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, geometry_label)
    current_index += 1

    # Position X
    pos_x_layout = QHBoxLayout()
    pos_x_layout.setContentsMargins(20, 5, 10, 5)
    pos_x_label = QLabel("Position X:")
    pos_x_label.setStyleSheet("color: white; font-size: 14px;")
    pos_x_layout.addWidget(pos_x_label)
    pos_x_layout.addStretch(1)
    main_window.pos_x_spin_numeric = QSpinBox()
    main_window.pos_x_spin_numeric.setRange(0, 480)
    main_window.pos_x_spin_numeric.setValue(main_window.current_shape.x())
    main_window.pos_x_spin_numeric.valueChanged.connect(lambda: updateNumericPosition(main_window))
    main_window.pos_x_spin_numeric.setStyleSheet("color: black; background-color: white;")
    main_window.pos_x_spin_numeric.setFixedWidth(60)
    pos_x_layout.addWidget(main_window.pos_x_spin_numeric)
    pos_x_widget = QWidget()
    pos_x_widget.setLayout(pos_x_layout)
    main_window.properties_layout.insertWidget(current_index, pos_x_widget)
    current_index += 1

    # Position Y
    pos_y_layout = QHBoxLayout()
    pos_y_layout.setContentsMargins(20, 5, 10, 5)
    pos_y_label = QLabel("Position Y:")
    pos_y_label.setStyleSheet("color: white; font-size: 14px;")
    pos_y_layout.addWidget(pos_y_label)
    pos_y_layout.addStretch(1)
    main_window.pos_y_spin_numeric = QSpinBox()
    main_window.pos_y_spin_numeric.setRange(0, 272)
    main_window.pos_y_spin_numeric.setValue(main_window.current_shape.y())
    main_window.pos_y_spin_numeric.valueChanged.connect(lambda: updateNumericPosition(main_window))
    main_window.pos_y_spin_numeric.setStyleSheet("color: black; background-color: white;")
    main_window.pos_y_spin_numeric.setFixedWidth(60)
    pos_y_layout.addWidget(main_window.pos_y_spin_numeric)
    pos_y_widget = QWidget()
    pos_y_widget.setLayout(pos_y_layout)
    main_window.properties_layout.insertWidget(current_index, pos_y_widget)
    current_index += 1

    # COLOR ADJUST SECTION
    color_adjust_label = QLabel("Color Adjust")
    color_adjust_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, color_adjust_label)
    current_index += 1

    # Number Color
    number_color_layout = QHBoxLayout()
    number_color_layout.setContentsMargins(20, 5, 10, 5)
    number_color_label = QLabel("Number color:")
    number_color_label.setStyleSheet("color: white; font-size: 14px;")
    number_color_layout.addWidget(number_color_label)
    number_color_layout.addStretch(1)
    main_window.number_color_rect_numeric = ColorRectangle(main_window.current_shape.number_color.name())
    main_window.number_color_rect_numeric.mousePressEvent = lambda e: changeNumericNumberColor(main_window)
    number_color_layout.addWidget(main_window.number_color_rect_numeric)
    number_color_widget = QWidget()
    number_color_widget.setLayout(number_color_layout)
    main_window.properties_layout.insertWidget(current_index, number_color_widget)
    current_index += 1

    # NUMBERS SECTION
    numbers_label = QLabel("Numbers")
    numbers_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; margin-top: 10px;")
    main_window.properties_layout.insertWidget(current_index, numbers_label)
    current_index += 1

    # Number value
    number_layout = QHBoxLayout()
    number_layout.setContentsMargins(20, 5, 10, 5)
    number_label = QLabel("Number:")
    number_label.setStyleSheet("color: white; font-size: 14px;")
    number_layout.addWidget(number_label)
    number_layout.addStretch(1)
    main_window.number_spin_numeric = QSpinBox()
    main_window.number_spin_numeric.setRange(-99999, 99999)
    main_window.number_spin_numeric.setValue(main_window.current_shape.number)
    main_window.number_spin_numeric.valueChanged.connect(lambda value: updateNumericNumber(main_window, value))
    main_window.number_spin_numeric.setStyleSheet("color: black; background-color: white;")
    main_window.number_spin_numeric.setFixedWidth(80)
    number_layout.addWidget(main_window.number_spin_numeric)
    number_widget = QWidget()
    number_widget.setLayout(number_layout)
    main_window.properties_layout.insertWidget(current_index, number_widget)
    current_index += 1

    # Number Size
    number_size_layout = QHBoxLayout()
    number_size_layout.setContentsMargins(20, 5, 10, 5)
    number_size_label = QLabel("Number size:")
    number_size_label.setStyleSheet("color: white; font-size: 14px;")
    number_size_layout.addWidget(number_size_label)
    number_size_layout.addStretch(1)
    main_window.number_size_spin_numeric = QSpinBox()
    main_window.number_size_spin_numeric.setRange(8, 72)
    main_window.number_size_spin_numeric.setValue(main_window.current_shape.number_size)
    main_window.number_size_spin_numeric.valueChanged.connect(lambda value: updateNumericNumberSize(main_window, value))
    main_window.number_size_spin_numeric.setStyleSheet("color: black; background-color: white;")
    main_window.number_size_spin_numeric.setFixedWidth(60)
    number_size_layout.addWidget(main_window.number_size_spin_numeric)
    number_size_widget = QWidget()
    number_size_widget.setLayout(number_size_layout)
    main_window.properties_layout.insertWidget(current_index, number_size_widget)
    current_index += 1

    # Number Alignment
    number_alignment_layout = QHBoxLayout()
    number_alignment_layout.setContentsMargins(20, 5, 10, 5)
    number_alignment_label = QLabel("Alignment:")
    number_alignment_label.setStyleSheet("color: white; font-size: 14px;")
    number_alignment_layout.addWidget(number_alignment_label)
    number_alignment_layout.addStretch(1)
    main_window.number_alignment_combo_numeric = QComboBox()
    main_window.number_alignment_combo_numeric.addItems(["Left", "Center", "Right", "Top", "Bottom"])
    main_window.number_alignment_combo_numeric.setCurrentText(main_window.current_shape.number_alignment)
    main_window.number_alignment_combo_numeric.currentTextChanged.connect(lambda text: updateNumericNumberAlignment(main_window, text))
    main_window.number_alignment_combo_numeric.setStyleSheet("color: black; background-color: white;")
    main_window.number_alignment_combo_numeric.setFixedWidth(80)
    number_alignment_layout.addWidget(main_window.number_alignment_combo_numeric)
    number_alignment_widget = QWidget()
    number_alignment_widget.setLayout(number_alignment_layout)
    main_window.properties_layout.insertWidget(current_index, number_alignment_widget)
    current_index += 1

    return current_index

# CALLBACK FUNKCIJE ZA NUMERIC WIDGET
def updateNumericActive(main_window, state):
    """Ažurira active status za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        is_active = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_active(is_active)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateNumericVisible(main_window, state):
    """Ažurira visible status za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        is_visible = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_visible(is_visible)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateNumericStatic(main_window, state):
    """Ažurira static status za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        is_static = (state == Qt.CheckState.Checked.value)
        main_window.current_shape.set_static(is_static)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

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
                main_window.current_shape.get_properties_dict()
        
        # Sortiraj widget-e
        main_window.sortWidgetsByStackOrder()

def updateNumericPosition(main_window):
    """Ažurira poziciju numeric widget-a"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        if hasattr(main_window, 'pos_x_spin_numeric') and hasattr(main_window, 'pos_y_spin_numeric'):
            main_window.current_shape.move(
                main_window.pos_x_spin_numeric.value(),
                main_window.pos_y_spin_numeric.value()
            )
            if hasattr(main_window, 'all_numeric_dicts'):
                main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def changeNumericNumberColor(main_window):
    """Menja boju brojeva za numeric widget"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        color = QColorDialog.getColor(main_window.current_shape.number_color)
        if color.isValid():
            main_window.current_shape.set_number_color(color)
            main_window.number_color_rect_numeric.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            if hasattr(main_window, 'all_numeric_dicts'):
                main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateNumericNumber(main_window, value):
    """Ažurira broj koji se prikazuje"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.set_number(value)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateNumericNumberSize(main_window, value):
    """Ažurira veličinu broja"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.set_number_size(value)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

def updateNumericNumberAlignment(main_window, text):
    """Ažurira poravnanje broja"""
    if main_window.current_shape and isinstance(main_window.current_shape, NumericWidget):
        main_window.current_shape.set_number_alignment(text)
        if hasattr(main_window, 'all_numeric_dicts'):
            main_window.all_numeric_dicts[main_window.current_shape.custom_name] = main_window.current_shape.get_properties_dict()

#----------------------------------------------------------------------------------------------------------------------------------------------------------

def generate_auto_tag(main_window, current_shape):
    """Generiše automatski tag za novi widget"""
    all_tags = []
    for shape in main_window.all_shapes:
        if hasattr(shape, 'tag') and shape != current_shape:  # Isključi trenutni shape
            all_tags.append(shape.tag)
    
    # Pronađi prvi slobodan tag od 0 do 255
    for i in range(256):
        if i not in all_tags:
            return i
    
    return 0  # Ako su svi zauzeti, vrati 0

#-------------------------------------------------------------------------------------------------------------------------------

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
    """Renumera sve widget-e na canvas-u po tipu (zamenjuje obe metode)"""
    from widgets import ButtonWidget, LineWidget, RectangleWidget, CircleWidget, GaugeWidget, ClockWidget, ProgressBarWidget, ScrollBarWidget, DialWidget, SliderWidget, ToggleWidget, LabelWidget, ImageWidget, KeysWidget
    
    # Grupiši widget-e po tipu
    widgets_by_type = {
        'Button': [],
        'Line': [],
        'Rectangle': [],
        'Circle': [],
        'Gauge': [],
        'Clock': [],
        'ProgressBar': [],
        'ScrollBar': [],
        'Dial': [],
        'Slider': [],
        'Toggle': [],
        'Label': [],
        'Image': [],
        'Keys': []
    }
    
    # Grupiši widget-e
    for shape in main_window.all_shapes:
        if isinstance(shape, ButtonWidget):
            widgets_by_type['Button'].append(shape)
        elif isinstance(shape, LineWidget):
            widgets_by_type['Line'].append(shape)
        elif isinstance(shape, RectangleWidget):
            widgets_by_type['Rectangle'].append(shape)
        elif isinstance(shape, CircleWidget):
            widgets_by_type['Circle'].append(shape)
        elif isinstance(shape, GaugeWidget):
            widgets_by_type['Gauge'].append(shape)
        elif isinstance(shape, ClockWidget):
            widgets_by_type['Clock'].append(shape)
        elif isinstance(shape, ProgressBarWidget):
            widgets_by_type['ProgressBar'].append(shape)
        elif isinstance(shape, ScrollBarWidget):
            widgets_by_type['ScrollBar'].append(shape)
        elif isinstance(shape, DialWidget):
            widgets_by_type['Dial'].append(shape)
        elif isinstance(shape, SliderWidget):
            widgets_by_type['Slider'].append(shape)
        elif isinstance(shape, ToggleWidget):
            widgets_by_type['Toggle'].append(shape)
        elif isinstance(shape, LabelWidget):
            widgets_by_type['Label'].append(shape)
        elif isinstance(shape, ImageWidget):
            widgets_by_type['Image'].append(shape)
        elif isinstance(shape, KeysWidget):
            widgets_by_type['Keys'].append(shape)
    
    # Renumeriši svaki tip posebno
    for widget_type, widgets in widgets_by_type.items():
        if widgets:  # Ako ima widget-a ovog tipa
            # Sortiraj po poziciji (Y pa X)
            widgets.sort(key=lambda w: (w.y(), w.x()))
            
            # Dodeli nove brojeve
            for i, widget in enumerate(widgets, 1):
                if hasattr(widget, 'custom_name'):
                    widget.custom_name = f"{widget_type}_{i}"
                elif hasattr(widget, 'set_custom_name'):
                    widget.set_custom_name(f"{widget_type}_{i}")
    
    # Ažuriraj properties ako je nešto selektovano
    if main_window.current_shape:
        main_window.showShapeProperties()

def generateWidgetName(main_window, widget_type):
    """Generiše automatsko ime za bilo koji tip widget-a"""
    type_count = 0
    existing_names = []
    
    # Proveri koje klase pripadaju ovom tipu
    type_classes = {
        'Button': [ButtonWidget],
        'Line': [LineWidget],
        'Rectangle': [RectangleWidget],
        'Circle': [CircleWidget],
        'Gauge': [GaugeWidget],
        'Clock': [ClockWidget],
        'ProgressBar': [ProgressBarWidget],
        'ScrollBar': [ScrollBarWidget],
        'Dial': [DialWidget],
        'Slider': [SliderWidget],
        'Toggle': [ToggleWidget],
        'Label': [LabelWidget],
        'Image': [ImageWidget],
        'Keys': [KeysWidget],
        'Numeric': [NumericWidget],
        'Ellipse': [EllipseWidget]
    }
    
    # Prikupi postojeća imena za ovaj tip
    if widget_type in type_classes:
        for shape in main_window.all_shapes:
            for widget_class in type_classes[widget_type]:
                if isinstance(shape, widget_class) and hasattr(shape, 'custom_name'):
                    existing_names.append(shape.custom_name)
    
    # Pronađi sledeći slobodan broj
    while True:
        candidate_name = f"{widget_type}_{type_count}"
        if candidate_name not in existing_names:
            return candidate_name
        type_count += 1

# Onda možete ukloniti generateButtonName i generateLineName
# i koristiti ovu jednu metodu za sve



# DODAJTE OVAJ IMPORT NA KRAJ callback.py DA BISTE IZVEZLI NOVE METODE:
__all__ = [
    'showButtonProperties', 'updateButtonSize',
    'showLineProperties', 'updateLineSize',
    'showCircleProperties', 'updateCircleSize',
    'generateWidgetName', 'renumberAllWidgets',
    'update_line_active', 'update_line_visible', 'update_line_static',
    'update_line_name', 'update_line_stack_order', 'update_line_position',
    'update_line_size', 'change_line_color', 'update_line_thickness',
    'update_circle_active', 'update_circle_visible', 'update_circle_static',
    'update_circle_name', 'update_circle_stack_order', 'update_circle_position',
    'change_circle_line_color', 'update_circle_thickness',
    'update_circle_filled', 'change_circle_fill_color',
    'updateLineAngle', 'updateLineLength', 'update_position_spins',
    'showRectangleProperties', 'updateRectangleProperties',
    'update_rectangle_active', 'update_rectangle_visible', 'update_rectangle_static',
    'update_rectangle_name', 'update_rectangle_stack_order', 'update_rectangle_position',
    'update_rectangle_size', 'change_rectangle_edge_color', 'update_rectangle_thickness',
    'update_rectangle_filled', 'update_rectangle_gradient_direction',
    'change_rectangle_gradient_start_color', 'change_rectangle_gradient_end_color',
    'showRectangleProperties', 'updateRectangleProperties',
    'update_rectangle_active', 'update_rectangle_visible', 'update_rectangle_static',
    'update_rectangle_name', 'update_rectangle_stack_order', 'update_rectangle_position',
    'update_rectangle_size', 'change_rectangle_edge_color', 'update_rectangle_thickness',
    'update_rectangle_filled', 'update_rectangle_gradient_direction',
    'change_rectangle_gradient_start_color', 'change_rectangle_gradient_end_color'
]