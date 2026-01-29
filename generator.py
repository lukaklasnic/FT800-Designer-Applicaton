from PyQt6.QtWidgets import ( QFileDialog, QMessageBox )
from widgets import ImageWidget
from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt

def getWidgetMapping():
    return {
        'Line': 'ft800_designer_line',
        'Rectangle': 'ft800_designer_rectangle',
        'Circle': 'ft800_designer_circle',
        'Ellipse': 'ft800_designer_ellipse',
        'Button': 'ft800_designer_button',
        'Keys': 'ft800_designer_keys',
        'Clock': 'ft800_designer_clock',
        'Gauge': 'ft800_designer_gauge',
        'Dial': 'ft800_designer_dial',
        'Toggle': 'ft800_designer_toggle',
        'ScrollBar': 'ft800_designer_scroll_bar',
        'Slider': 'ft800_designer_slider',
        'ProgressBar': 'ft800_designer_progress_bar',
        'Image': 'ft800_designer_image',
        'Label': 'ft800_designer_label',
        'Numeric': 'ft800_designer_numeric'
    }

def convertColorToHex( color_value ):
    if isinstance( color_value, str ):
        if color_value.startswith( '#' ):
            color_value = color_value[ 1: ]

        if len( color_value ) == 6:
            return f"0x{ color_value.upper() }"
        
        elif len( color_value ) == 8:
            return f"0x{ color_value[ 2: ].upper() }"
        
    elif isinstance( color_value, int ):
        return f"0x{color_value:06X}"
    
    return "0x000000"

def convertBool( value ):
    if value:
        return 'true'  
    
    else: 
        return 'false'

def convertGridType( grid_type ) :
    if grid_type == 'dots':
        return 'FT800_GRID_DOTS'
    
    elif grid_type == 'lines':
        return 'FT800_GRID_LINE'

def convert3dEnabled( value ):
    if value:
        return 'FT800_3D'
      
    else: 
        return 'FT800_FLAT'

def convertAlignment( alignment ):
    mapping = {
        'left': 'FT800_ALIGN_LEFT',
        'right': 'FT800_ALIGN_RIGHT',
        'top': 'FT800_ALIGN_TOP',
        'bottom': 'FT800_ALIGN_BOTTOM',
        'center': 'FT800_ALIGN_CENTER',
        'FT800_ALIGN_LEFT': 'FT800_ALIGN_LEFT',
        'FT800_ALIGN_RIGHT': 'FT800_ALIGN_RIGHT',
        'FT800_ALIGN_TOP': 'FT800_ALIGN_TOP',
        'FT800_ALIGN_BOTTOM': 'FT800_ALIGN_BOTTOM',
        'FT800_ALIGN_CENTER': 'FT800_ALIGN_CENTER'
    }

    return mapping.get( alignment, 'FT800_ALIGN_CENTER' )

def convertGradientType( gradient_type ):
    mapping = {
        'top_bottom': 'FT800_TOP_BOTTOM_GRADIENT',
        'bottom_top': 'FT800_BOTTOM_TOP_GRADIENT',
        'left_right': 'FT800_LEFT_RIGHT_GRADIENT',
        'right_left': 'FT800_RIGHT_LEFT_GRADIENT',
        'FT800_TOP_BOTTOM_GRADIENT': 'FT800_TOP_BOTTOM_GRADIENT',
        'FT800_BOTTOM_TOP_GRADIENT': 'FT800_BOTTOM_TOP_GRADIENT',
        'FT800_LEFT_RIGHT_GRADIENT': 'FT800_LEFT_RIGHT_GRADIENT',
        'FT800_RIGHT_LEFT_GRADIENT': 'FT800_RIGHT_LEFT_GRADIENT'
    }

    return mapping.get( gradient_type, 'FT800_LEFT_RIGHT_GRADIENT' )

def convertKeyboardType( key_type ):
    mapping = {
        'NUM': 'FT800_KEYBOARD_NUM',
        'QUERTZ': 'FT800_KEYBOARD_QUERTZ',
        'qwertz': 'FT800_KEYBOARD_QUERTZ',
        'num': 'FT800_KEYBOARD_NUM'
    }

    return mapping.get( key_type, 'FT800_KEYBOARD_NUM' )

def convertToggleState( state ):
    if isinstance( state, str ):
        if state.lower() == 'on':
            return 'FT800_ON'  
        
        else: 
            return 'FT800_OFF'
        
    if state:    
        return 'FT800_ON'  
    
    else: 
        return 'FT800_OFF'

def generateWidgetStructure( widget_type, name, widget_data ):
    content = ""
    
    if widget_type == 'Line':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x1_coord = { widget_data.get( 'x1', 0 ) };\n"
        content += f"    { name }.y1_coord = { widget_data.get( 'y1', 0 ) };\n"
        content += f"    { name }.x2_coord = { widget_data.get( 'x2', 100 ) };\n"
        content += f"    { name }.y2_coord = { widget_data.get( 'y2', 0 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'color', 0xFF0000 ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'width', 1 ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Rectangle':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 100 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'edges_color', 0xFF0000 ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'thickness', 1 ) };\n"
        content += f"    { name }.gradient.filled = { convertBool( widget_data.get( 'filled', True ) ) };\n"
        content += f"    { name }.gradient.gradient_type = { convertGradientType( widget_data.get( 'gradient_type', 'left_right' ) ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'gradient_start_color', widget_data.get( 'fill_color', 0xFF0000 ) ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'gradient_end_color', widget_data.get( 'fill_color', 0x0000FF ) ) ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Circle':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 100 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'edges_color', 0xFF0000 ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'line_edges_width', 1 ) };\n"
        content += f"    { name }.gradient.filled = { convertBool( widget_data.get( 'filled', True ) ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'fill_color', 0x0000FF ) ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Ellipse':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 150 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 75 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'border_color', 0xCA75FE ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'edges_width', 1 ) };\n"
        content += f"    { name }.gradient.filled = { convertBool( widget_data.get( 'filled', True ) ) };\n"
        content += f"    { name }.gradient.gradient_type = { convertGradientType( widget_data.get( 'gradient_type', 'top_bottom' ) ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'gradient_start_color', widget_data.get( 'fill_color', 0xFF0000 ) ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'gradient_end_color', widget_data.get( 'fill_color', 0x0000FF ) ) ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Button':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 100 ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'start_color', 0xFF0000 ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'end_color', 0x00FF00 ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.text.text_caption = \"{widget_data.get( 'text', 'Press' ) }\";\n"
        content += f"    { name }.text.text_size = { widget_data.get( 'text_size', 28 ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'text_color', 0xFF0000 ) )};\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Keys':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 10 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 10 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 300 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 60 ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'key_color_top', 0xFFFF00 ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex(widget_data.get( 'key_color_bottom', 0xFFFF00 ) ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'text_color', 0x00FF00 ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.type = { convertKeyboardType( widget_data.get( 'key_type', 'NUM' ) ) };\n"
        content += f"    { name }.text.text_size = { widget_data.get( 'text_size', 27 ) };\n"
        content += "\n"
    
    elif widget_type == 'Clock':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 240 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 136 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 100 ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', 0x0000FF ) ) };\n"    
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.hours = { widget_data.get( 'hours', 9 ) };\n"
        content += f"    { name }.minutes = { widget_data.get( 'minutes', 53 ) };\n"
        content += f"    { name }.seconds = { widget_data.get( 'seconds', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Gauge':
        content += f"    { name }.visible = { convertBool(widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 100 ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', 0xFF0000 ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.major = { widget_data.get( 'major_subdivision', 6 ) };\n"
        content += f"    { name }.minor = { widget_data.get( 'minor_subdivision', 3 ) };\n"
        content += f"    { name }.range = { widget_data.get( 'range_value', 100 ) };\n"
        content += f"    { name }.val = { widget_data.get( 'value', 50 ) };\n"
        content += "\n"
    
    elif widget_type == 'Dial':
        content += f"    { name }.visible = { convertBool(widget_data.get( 'v1isible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 2140 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 1130 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 50 ) };\n"
        content += f"    { name }._3d = {convert3dEnabled(widget_data.get('3d_enable', True) ) };\n"
        content += f"    { name }.val = 0x{int(widget_data.get( 'value', 0.5 ) * 65535 ):04X};\n"
        content += f"    { name }.tag = {widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Toggle':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 50 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 50 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 40 ) };\n"
        content += f"    { name }.thumb_color = { convertColorToHex( widget_data.get( 'thumb_color', 0xFF00FF ) ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', 0x0000FF ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.state = { convertToggleState( widget_data.get( 'is_on', False ) ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'ScrollBar':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 10 ) };\n"
        content += f"    { name }.thumb_color = { convertColorToHex( widget_data.get( 'thumb_color', 0x0000FF ) ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'track_color', 0xFFFF00 ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.range = { widget_data.get(' range_value', 65535 ) };\n"
        content += f"    { name }.val = { widget_data.get( 'current_val', 32767 ) };\n"
        content += f"    { name }.size = { widget_data.get( 'thumb_size', 1000 ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'Slider':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 10 ) };\n"
        content += f"    { name }.thumb_color = { convertColorToHex( widget_data.get( 'thumb_color', 0x00FF00 ) ) };\n"
        content += f"    { name }.background_color_left = { convertColorToHex( widget_data.get( 'background_left_color', 0xFF0000 ) ) };\n"
        content += f"    { name }.background_color_right = { convertColorToHex( widget_data.get( 'background_right_color', 0x0000FF ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.range = { widget_data.get( 'range_value', 65535 ) };\n"
        content += f"    { name }.val = { widget_data.get( 'value', 32767 ) };\n"
        content += f"    { name }.tag = { widget_data[ 'tag' ] };\n"
        content += "\n"
    
    elif widget_type == 'ProgressBar':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 10 ) };\n"
        content += f"    { name }.progress_color = { convertColorToHex( widget_data.get( 'progress_color', 0xFFFFFF ) ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', 0xFF0000 ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( '3d_enable', True ) ) };\n"
        content += f"    { name }.range = {widget_data.get( 'max_value', 100 ) };\n"
        content += f"    { name }.val = { widget_data.get( 'value', 50 ) };\n"
        content += "\n"
    
    elif widget_type == 'Image':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 50 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 50 ) };\n"
        content += f"    { name }.width = { widget_data.get ('width', 200 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'height', 100 ) };\n"
        content += f"    { name }.image_data = &{ widget_data.get( 'name', 'Image_0' ).replace( ' ' , '_' ) }_hex;  \n"
        content += f"    { name }.frame = { convertBool( widget_data.get( 'frame_enable', False ) ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'frame_color', 0xFF0000 ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'frame_width', 2 ) };\n"
        content += "\n"
    
    elif widget_type == 'Label':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'y', 100 ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'text_color', 0x0000FF ) ) };\n"
        content += f"    { name }.text.text_caption = \"{ widget_data.get('text', 'Labela' ) }\";\n"
        content += f"    { name }.text.text_size = { widget_data.get( 'text_size', 30 ) };\n"
        content += f"    { name }.alignment = { convertAlignment( widget_data.get( 'alignment', 'right' ) ) };\n"
        content += "\n"
    
    elif widget_type == 'Numeric':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get('x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get('y', 100 ) };\n"
        content += f"    { name }.num_color = { convertColorToHex( widget_data.get( 'number_color', 0xFF00EF ) ) };\n"
        content += f"    { name }.num = { widget_data.get( 'number', 3110 ) };\n"
        content += f"    { name }.num_size = { widget_data.get( 'number_size', 30)};\n"
        content += f"    { name }.alignment = { convertAlignment( widget_data.get( 'alignment', 'right' ) ) };\n"
        content += "\n"
    
    return content

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
       defaults = { 'center_x': 100, 'center_y': 100, 'diameter': 100, 'edges_color': 0xFF0000, 'line_edges_width': 1, 'filled': True, 'fill_color': 0x0000FF, 'tag': 3 }

    elif widget_type == 'Ellipse':
       defaults = { 'center_x': 100, 'center_y': 100, 'width': 150, 'height': 75, 'border_color': 0xCA75FE, 'edges_width': 1, 'filled': True, 'fill_color': 0x0000FF, 'tag': 4, 'gradient_enable': False, 'gradient_type': 'top_bottom', 'gradient_start_color': 0xFF0000, 'gradient_end_color': 0x0000FF }

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
       defaults = { 'x': 100, 'y': 100, 'width': 100, 'height': 10, 'thumb_color': 0x0000FF, 'track_color': 0xFFFF00, '3d_enable': True, 'range_value': 65535, 'current_val': 32767, 'thumb_size': 1000, 'tag': 8 }

    elif widget_type == 'Slider':
       defaults = { 'x': 100, 'y': 100, 'width': 100, 'height': 10, 'thumb_color': 0x00FF00, 'background_left_color': 0xFF0000, 'background_right_color': 0x0000FF, '3d_enable': True, 'range_value': 65535, 'value': 32767, 'tag': 9 }

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


def generateComponentsH(canvas_data, widgets_data):
    content = ""

    content += f"#ifndef COMPONENTS_H\n"
    content += f"#define COMPONENTS_H\n"
    content += f"#include \"MikroSDK.Ft800\"\n"
    
    has_images = False

    for canvas in canvas_data:
        if 'widgets' in canvas:
            for widget in canvas[ 'widgets' ]:
                if widget.get( 'type' ) == 'Image' and widget.get( 'active', True ):
                    has_images = True

                    break

        if has_images:
            break
    
    if has_images:
        content += f"#include \"resource.h\"\n"

    content += "\n"
    content += f"extern ft800_t ctx;\n"
    content += f"extern ft800_cfg_t cfg;\n"
    content += f"extern tp_drv_t drv;\n"
    content += "\n"

    for i, canvas in enumerate( canvas_data ):
        if canvas.get( 'active', True ):
            name = canvas.get( 'name', f'Screen_{ i }' )
            if canvas.get( 'static', False ):
                static_prefix = 'static '  

            else: 
                static_prefix = 'extern '
            content += f"{ static_prefix }ft800_designer_screen { name };\n"
    
    content += "\n"
    
    widget_types = {}
    
    for i, canvas in enumerate(canvas_data):
        if 'widgets' in canvas and canvas.get('active', True):
            for widget in canvas['widgets']:
                if widget.get('active', True):
                    widget_type = widget.get('type')
                    if widget_type not in widget_types:
                        widget_types[widget_type] = []
                    widget_types[widget_type].append(widget)
    
    type_mapping = getWidgetMapping()
    
    for widget_type, widgets in widget_types.items():
        if widget_type in type_mapping:
            for widget in widgets:
                name = widget.get( 'name', f'{ widget_type }_{ widgets.index( widget ) }' )

                if widget.get( 'static', False ):
                    static_prefix = 'static '  

                else:
                    static_prefix = 'extern '

                content += f"{ static_prefix }{type_mapping[ widget_type ] } { name };\n"
    
    content += "\n"

    content += "void ft800_display_configuration();\n"
    
    for i, canvas in enumerate( canvas_data ):
        if canvas.get( 'active', True ):
            content += f"void ft800_display_task_{ i }();\n"
    
    content += "\n#endif"
    
    return content

def generateComponentsC(canvas_data, widgets_data):
    content = ""

    content += f"#include \"components.h\"\n"
    content += "\n"
    content += f"ft800_t ctx;\n"
    content += f"ft800_cfg_t cfg;\n"
    content += f"tp_drv_t drv;\n"
    
    content += "\n"

    for i, canvas in enumerate( canvas_data ):
        if canvas.get( 'active', True ):
            name = canvas.get( 'name', f'Screen_{ i }') 

            if canvas.get('static', False):
                static_prefix = 'static '  

            else: 
                static_prefix = ''

            content += f"{ static_prefix }ft800_designer_screen { name };\n"
    
    
    
    widget_types = {}
    
    for i, canvas in enumerate( canvas_data ):
        if 'widgets' in canvas and canvas.get( 'active', True ):
            for widget in canvas[ 'widgets' ]:
                if widget.get( 'active', True ):
                    widget_type = widget.get( 'type' )

                    if widget_type not in widget_types:
                        widget_types[ widget_type ] = []

                    widget_types[ widget_type ].append( widget )
    
    type_mapping = getWidgetMapping()
    
    for widget_type, widgets in widget_types.items():
        if widget_type in type_mapping:
            for widget in widgets:
                name = widget.get( 'name', f'{ widget_type }_{ widgets.index( widget ) }' )
                if widget.get( 'static', False ):
                    static_prefix = 'static '  

                else: 
                    static_prefix = ''

                content += f"{ static_prefix }{ type_mapping[ widget_type ] } { name };\n"
    
    content += "\n"
    
    content += f"void ft800_display_configuration()\n"
    content += "{\n"
    content += f"    ft800_initialization( &ctx, &cfg, &drv );\n"
    content += "\n"

    sorted_canvases = sorted( canvas_data, key = lambda x: x.get( 'stack_order', 0 ) )
    
    for i, canvas in enumerate( sorted_canvases ):
        if canvas.get( 'active', True ):
            content += f"    { canvas.get( 'name', f'Screen_{ i }' )}.background_color = { convertColorToHex( canvas[ 'background_color' ] ) };\n"
            content += f"    { canvas.get( 'name', f'Screen_{ i }' )}.grid_enable = { convertBool( canvas.get( 'grid_enable', False ) ) };\n" 
            content += f"    { canvas.get( 'name', f'Screen_{ i }' )}.grid_color = { convertColorToHex( canvas[ 'grid_color' ] ) };\n"
            content += f"    { canvas.get( 'name', f'Screen_{ i }' )}.type = { convertGridType( canvas.get( 'grid_type', 'line' ) ) };\n"
            content += f"    { canvas.get( 'name', f'Screen_{ i }' )}.grid_size = { canvas.get( 'grid_size', 20 ) };\n"
            content += f"    { canvas.get( 'name', f'Screen_{ i }' )}.visible = { convertBool( canvas.get( 'visible', True ) ) };\n"
            content += "\n"
    
    all_widgets = []

    for canvas in sorted_canvases:
        if canvas.get( 'active', True ) and 'widgets' in canvas:
            canvas_widgets = sorted( canvas[ 'widgets' ], key = lambda x: x.get( 'stack_order', 0 ) )
            for widget in canvas_widgets:
                if widget.get( 'active', True ):
                    all_widgets.append( ( canvas, widget ) )
    
    for canvas, widget in all_widgets:
        widget_type = widget.get( 'type' )
        name = widget.get( 'name', f'{ widget_type }_0' )
        
        content += generateWidgetStructure(widget_type, name, widget)
    
    content += "}\n\n"
    
    for i, canvas in enumerate(sorted_canvases):
        if canvas.get('active', True):
            name = canvas.get('name', f'Screen_{i}')
            
            content += f"void ft800_display_task_{i}()\n"
            content += "{\n"
            content += f"    ft800_start_display_list( &ctx );\n"
            content += f"    ft800_designer_screen_settings( &ctx, &{name} );\n"

            if 'widgets' in canvas:
                sorted_widgets = sorted( canvas[ 'widgets'] , key = lambda x: x.get( 'stack_order', 0 ) )
                
                for widget in sorted_widgets:
                    if widget.get( 'active', True ):
                        widget_type = widget.get( 'type' )
                        widget_name = widget.get( 'name', f'{ widget_type }_0' )
                        
                        draw_functions = {
                            'Line': 'ft800_line_designer',
                            'Rectangle': 'ft800_rectangle_designer',
                            'Circle': 'ft800_circle_designer',
                            'Ellipse': 'ft800_ellipse_designer',
                            'Button': 'ft800_button_designer',
                            'Keys': 'ft800_keys_designer',
                            'Clock': 'ft800_clock_designer',
                            'Gauge': 'ft800_gauge_designer',
                            'Dial': 'ft800_dial_designer',
                            'Toggle': 'ft800_toggle_designer',
                            'ScrollBar': 'ft800_scroll_bar_designer',
                            'Slider': 'ft800_slider_designer',
                            'ProgressBar': 'ft800_progress_bar_designer',
                            'Image': 'ft800_image_designer',
                            'Label': 'ft800_label_designer',
                            'Numeric': 'ft800_numeric_designer'
                        }
                        
 
                        content += f"    { draw_functions[ widget_type ] }( &ctx, &{ widget_name } );\n"
            
            content += f"    ft800_end_display_list( &ctx );\n"
            content += "}\n"
    
    return content

def generateResourcesH( self, all_images ):
    if not all_images:
        return None
    
    h_content = ""
    h_content += f"#ifndef NECTO_DESIGNER_RESOURCE_H\n"
    h_content += f"#define NECTO_DESIGNER_RESOURCE_H\n"
    h_content += f"#include \"stdint.h\"\n"
    h_content += "\n"
    
    generated_count = 0
    
    for img_widget in all_images:
        try:
            if not hasattr( img_widget, 'pixmap' ) or img_widget.pixmap.isNull():
                continue
            
            if hasattr( img_widget, 'custom_name' ) and img_widget.custom_name:
                clean_name = img_widget.custom_name.replace( ' ', '_' ).replace( '-', '_' )
                var_name = f"{ clean_name }_hex"

            else:
                var_name = f"image_{ generated_count }_hex"
            
            h_content += f"extern const code uint8_t { var_name }[];\n"
            generated_count += 1
            
        except Exception as e:
            continue
        
    h_content += "\n"
    h_content += "#endif\n"
    
    return h_content

def generateResourcesC( self, all_images ):
    if not all_images:
        return None

    c_content = ""
    c_content += f"#include \"stdint.h\"\n"
    c_content += f"#include \"resource.h\"\n"
    c_content += "\n"

    generated_count = 0

    for img_widget in all_images:
        try:
            if not hasattr( img_widget, 'pixmap' ) or img_widget.pixmap.isNull():
                continue
            
            image = img_widget.pixmap.toImage()
            width = img_widget.getWidth()
            height = img_widget.getHeight()
            scaled_image = image.scaled( width, height, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation )
            rgb888_image = scaled_image.convertToFormat( QImage.Format.Format_RGB888 )
            rgb565 = bytearray()

            for y in range( height ):
                for x in range( width ):
                    c = rgb888_image.pixelColor( x, y )

                    r = min( max( c.red(), 0 ), 255 ) >> 3
                    g = min( max( c.green(), 0 ), 255 ) >> 2
                    b = min( max( c.blue(), 0 ), 255 ) >> 3

                    value = ( r << 11 ) | ( g << 5 ) | b
                    rgb565.append( value & 0xFF )
                    rgb565.append( ( value >> 8 ) & 0xFF )

            size = len( rgb565 )

            if hasattr( img_widget, 'custom_name' ) and img_widget.custom_name:
                clean_name = img_widget.custom_name.replace( ' ', '_' ).replace( '-', '_' )
                var_name = f" {clean_name }_hex"

            else:
                var_name = f"image_{ generated_count }_hex"

            c_content += f"const code uint8_t { var_name }[] = {{\n"

            for i in range( 0, size, 16 ):
                line = ", ".join( f"0x{b:02X}" for b in rgb565[ i:i+16 ] )
                c_content += f"    { line },\n"

            c_content += "};\n\n"
            generated_count += 1

        except Exception as e:
            continue
        
    return c_content

def generateResources( main_window, out_dir=None ):
    all_images = []
        
    for canvas_id in range( len( main_window.canvases ) ):
        canvas_widgets = main_window.canvases[ canvas_id ].widget_container.children()
            
        for widget in canvas_widgets:
            if isinstance( widget, ImageWidget ):
                all_images.append( widget )
        
    if not all_images:
        return
    
    if out_dir is None:
        out_dir = QFileDialog.getExistingDirectory( main_window, "Select output directory for resource files" )
        
        if not out_dir:
            return
    
    try:
        h_content = generateResourcesH(main_window, all_images)
        c_content = generateResourcesC(main_window, all_images)
            
        if h_content:
            with open(f"{out_dir}/resource.h", "w", encoding='utf-8') as h_file:
                h_file.write(h_content)
            
        if c_content:
            with open(f"{out_dir}/resource.c", "w", encoding='utf-8') as c_file:
                c_file.write(c_content)
                    
    except Exception as e:
        QMessageBox.critical( main_window, "Error",  f"Failed to generate resource files:\n{ str( e ) }" )

def generateComponents( main_window, out_dir=None ):
    canvas_data = []

    for canvas_id, canvas_props in main_window.all_canvas_dicts.items():
        canvas_info = canvas_props.copy()
        canvas_widgets = []
        widgets = main_window.canvas_widgets.get( canvas_id, [] )

        for widget in widgets:
            if hasattr( widget, 'getPropertiesDict' ):
                widget_dict = widget.getPropertiesDict()
                widget_type = type( widget ).__name__.replace( 'Widget', '' )

                if widget_type == 'ScrollBar':
                    widget_type = 'ScrollBar'

                elif widget_type == 'ProgressBar':
                    widget_type = 'ProgressBar'

                widget_dict[ 'type' ] = widget_type

                canvas_widgets.append( widget_dict )

        canvas_info[ 'widgets' ] = canvas_widgets
        canvas_data.append( canvas_info )

    if not canvas_data:
        return

    if not out_dir:
        return

    try:
        h_content = generateComponentsH( canvas_data, {} )
        c_content = generateComponentsC( canvas_data, {} )

        with open( f"{ out_dir }/components.h", "w", encoding='utf-8' ) as h_file:
            h_file.write( h_content )

        with open( f"{ out_dir }/components.c", "w", encoding='utf-8' ) as c_file:
            c_file.write( c_content )

    except Exception as e:
        QMessageBox.critical( main_window, "Error",  f"Failed to generate component files:\n{ str( e ) }" )