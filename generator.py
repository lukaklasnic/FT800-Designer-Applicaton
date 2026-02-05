from PyQt6.QtWidgets import ( QFileDialog, QMessageBox )
from widgets import ImageWidget
from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt
from conversion import *

def generateScreenStructure( canvas_name, canvas ):
    content = ""
    
    content += f"    { canvas_name }.visible = { convertBool( canvas.get( 'visible', True ) ) };\n"
    content += f"    { canvas_name }.background_color = { convertColorToHex( canvas.get( 'background_color', '0xFFFFFF' ) ) };\n"
    content += f"    { canvas_name }.grid_enable = { convertBool( canvas.get( 'grid_enable', False ) ) };\n"
    content += f"    { canvas_name }.grid_color = { convertColorToHex( canvas.get( 'grid_color', '0x000000' ) ) };\n"
    content += f"    { canvas_name }.type = { convertGridType( canvas.get( 'grid_type', 'lines' ) ) };\n"
    content += f"    { canvas_name }.grid_size = { canvas.get( 'grid_size', 20 ) };\n"
    content += "\n"

    return content

def generateWidgetStructure( widget_type, name, widget_data ):
    content = ""
    
    if widget_type == 'Line':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x1_coord = { widget_data.get( 'start_x', 50 ) };\n"
        content += f"    { name }.y1_coord = { widget_data.get( 'start_y', 50 ) };\n"
        content += f"    { name }.x2_coord = { widget_data.get( 'end_x', 100 ) };\n"
        content += f"    { name }.y2_coord = { widget_data.get( 'end_y', 100 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'line_color', '0x000000' ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'line_width', 1 ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Rectangle':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'rectangle_width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'rectangle_height', 100 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'edges_color', '0x000000' ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'edges_width', 1 ) };\n"
        content += f"    { name }.gradient.filled = { convertBool(widget_data.get( 'filled', False ) ) };\n"
        content += f"    { name }.gradient.gradient_type = { convertGradientType( widget_data.get( 'gradient_direction', 'Left-Right' ) ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'gradient_start_color', '0x000000' ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'gradient_end_color', '0x000000' ) ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Circle':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 100 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'edges_color', '0x000000' ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'edges_width', 1 ) };\n"
        content += f"    { name }.gradient.filled = { convertBool( widget_data.get( 'filled', False ) ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'fill_color', '0x000000' ) ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Ellipse':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'ellipse_width', 120 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'ellipse_height', 80 ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'edges_color', '0x000000' ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'edges_width', 1 ) };\n"
        content += f"    { name }.gradient.filled = { convertBool( widget_data.get( 'filled', False ) ) };\n"
        content += f"    { name }.gradient.gradient_type = { convertGradientType( widget_data.get( 'gradient_direction', 'Top-Bottom' ) ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'gradient_start_color', '0x000000' ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'gradient_end_color', '0x000000' ) ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Button':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 100 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 100 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'button_width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'button_height', 50 ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'gradient_start_color', '0x000000' ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'gradient_end_color', '0x000000' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.text.text_caption = \"{ widget_data.get( 'text', 'Press' ) }\";\n"
        content += f"    { name }.text.text_size = { widget_data.get( 'text_size', 28 ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'text_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Keys':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'keys_width', 300 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'keys_height', 60 ) };\n"
        content += f"    { name }.gradient.start_color = { convertColorToHex( widget_data.get( 'gradient_start_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }.gradient.end_color = { convertColorToHex( widget_data.get( 'gradient_end_color', '0x000000' ) ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'font_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.type = { convertKeyboardType( widget_data.get( 'keys_type', 'QUERTZ' ) ) };\n"
        content += f"    { name }.text.text_size = { widget_data.get( 'font_size', 28 ) };\n"
        content += "\n"
    
    elif widget_type == 'Clock':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 100 ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', '0x000000' ) ) };\n"
        content += f"    { name }.face_color = { convertColorToHex( widget_data.get( 'face_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.hours = { widget_data.get( 'hours', 0 ) };\n"
        content += f"    { name }.minutes = { widget_data.get( 'minutes', 0 ) };\n"
        content += f"    { name }.seconds = { widget_data.get( 'seconds', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Gauge':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 100 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 100 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 100 ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', '0x000000' ) ) };\n"
        content += f"    { name }.face_color = { convertColorToHex( widget_data.get( 'face_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.major = { widget_data.get( 'major_subdivision', 6 ) };\n"
        content += f"    { name }.minor = { widget_data.get( 'minor_subdivision', 3 ) };\n"
        content += f"    { name }.range = { widget_data.get( 'range', 100 ) };\n"
        content += f"    { name }.val = { widget_data.get( 'value', 50 ) };\n"
        content += "\n"
    
    elif widget_type == 'Dial':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.cx_coord = { widget_data.get( 'center_x', 80 ) };\n"
        content += f"    { name }.cy_coord = { widget_data.get( 'center_y', 80 ) };\n"
        content += f"    { name }.diameter = { widget_data.get( 'diameter', 80 ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', '0x000000' ) ) };\n"
        content += f"    { name }.pointer_color = { convertColorToHex( widget_data.get( 'pointer_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.val = 0x{ int( widget_data.get( 'value', 50 ) * 65535 / 100 ):04X};\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Toggle':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 50 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 50 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'toggle_width', 40 ) };\n"
        content += f"    { name }.thumb_color = { convertColorToHex( widget_data.get( 'thumb_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', '0x000000' ) ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'text_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.state = { convertToggleState( widget_data.get( 'state', False ) ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'ScrollBar':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'scroll_bar_width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'scroll_bar_height', 10 ) };\n"
        content += f"    { name }.thumb_color = { convertColorToHex( widget_data.get( 'thumb_color', '0x000000' ) ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'track_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.val = { widget_data.get( 'current_value', 32767 ) };\n"
        content += f"    { name }.size = { widget_data.get( 'thumb_size', 1000 ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'Slider':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'slider_width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'slider_height', 10 ) };\n"
        content += f"    { name }.thumb_color = { convertColorToHex( widget_data.get( 'thumb_color', '0x000000' ) ) };\n"
        content += f"    { name }.background_color_left = { convertColorToHex( widget_data.get( 'left_background_color', '0x000000' ) ) };\n"
        content += f"    { name }.background_color_right = { convertColorToHex( widget_data.get( 'right_background_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.val = { widget_data.get( 'current_value', 32767 ) };\n"
        content += f"    { name }.tag = { widget_data.get( 'tag', 0 ) };\n"
        content += "\n"
    
    elif widget_type == 'ProgressBar':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'progress_bar_width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'progress_bar_height', 10 ) };\n"
        content += f"    { name }.progress_color = { convertColorToHex( widget_data.get( 'progress_color', '0x000000' ) ) };\n"
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', '0xFFFFFF' ) ) };\n"
        content += f"    { name }._3d = { convert3dEnabled( widget_data.get( 'effect_3d', True ) ) };\n"
        content += f"    { name }.range = { widget_data.get( 'range', 100 ) };\n"
        content += f"    { name }.val = { widget_data.get( 'current_value', 50 ) };\n"
        content += "\n"
    
    elif widget_type == 'Image':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.width = { widget_data.get( 'image_width', 100 ) };\n"
        content += f"    { name }.height = { widget_data.get( 'image_height', 100 ) };\n"
        content += f"    { name }.image_data = &{ widget_data.get( 'name', 'Image_0' ).replace( ' ', '_' ) }_hex;\n"
        content += f"    { name }.frame = { convertBool( widget_data.get( 'frame', False ) ) };\n"
        content += f"    { name }.pen.color = { convertColorToHex( widget_data.get( 'frame_color', '0x000000' ) ) };\n"
        content += f"    { name }.pen.width = { widget_data.get( 'frame_width', 1 ) };\n"
        content += "\n"
    
    elif widget_type == 'Label':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.text.text_color = { convertColorToHex( widget_data.get( 'text_color', '0x000000' ) ) };\n"
        content += f"    { name }.text.text_caption = \"{ widget_data.get( 'text', 'Label' ) }\";\n"
        content += f"    { name }.text.text_size = { widget_data.get( 'text_size', 28 ) };\n"
        content += f"    { name }.alignment = { convertAlignment( widget_data.get( 'text_alignment', 'Left' ) ) };\n"
        content += "\n"
    
    elif widget_type == 'Numeric':
        content += f"    { name }.visible = { convertBool( widget_data.get( 'visible', True ) ) };\n"
        content += f"    { name }.x_coord = { widget_data.get( 'position_x', 0 ) };\n"
        content += f"    { name }.y_coord = { widget_data.get( 'position_y', 0 ) };\n"
        content += f"    { name }.num_color = { convertColorToHex( widget_data.get( 'number_color', '0x000000' ) ) };\n"
        content += f"    { name }.num = { widget_data.get( 'number', 123 ) };\n"
        content += f"    { name }.num_size = { widget_data.get( 'number_size', 28 ) };\n"
        content += f"    { name }.alignment = { convertAlignment( widget_data.get( 'number_alignment', 'Left' ) ) };\n"
        content += "\n"
    
    return content

def generateComponentsH( canvas_data ):
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
    
    for i, canvas in enumerate( canvas_data ):
        if 'widgets' in canvas and canvas.get( 'active', True ):
            for widget in canvas[ 'widgets' ]:
                if widget.get( 'active', True ):
                    widget_type = widget.get( 'type' )

                    if widget_type not in widget_types:
                        widget_types[ widget_type ] = []

                    widget_types[ widget_type ].append( widget )
    
    type_mapping = widgetStructureMapping()
    
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

def generateComponentsC( canvas_data ):
    content = ""
    
    content += f"#include \"components.h\"\n"
    content += "\n"
    content += f"ft800_t ctx;\n"
    content += f"ft800_cfg_t cfg;\n"
    content += f"tp_drv_t drv;\n"
    content += "\n"
    
    for i, canvas in enumerate( canvas_data ):
        if canvas.get( 'active', True ):
            name = canvas.get( 'name', f'Screen_{ i }' )

            if canvas.get( 'static', False ):
                static_prefix = 'static '

            else:
                static_prefix = ''

            content += f"{ static_prefix }ft800_designer_screen { name };\n"
    
    content += "\n"
    
    widget_types = {}
    
    for i, canvas in enumerate( canvas_data ):
        if 'widgets' in canvas and canvas.get( 'active', True ):
            for widget in canvas[ 'widgets' ]:
                if widget.get( 'active', True ):
                    widget_type = widget.get('type')

                    if widget_type not in widget_types:
                        widget_types[ widget_type ] = []

                    widget_types[ widget_type ].append( widget )
    
    type_mapping = widgetStructureMapping()
    
    for widget_type, widgets in widget_types.items():
        if widget_type in type_mapping:
            for widget in widgets:
                name = widget.get('name', f'{widget_type}_{widgets.index(widget)}')
                if widget.get('static', False):
                    static_prefix = 'static '
                else:
                    static_prefix = ''
                content += f"{static_prefix}{type_mapping[widget_type]} {name};\n"
    
    content += "\n"
    
    content += f"void ft800_display_configuration()\n"
    content += "{\n"
    content += f"    ft800_initialization( &ctx, &cfg, &drv );\n"
    content += "\n"
    
    sorted_canvases = sorted( canvas_data, key = lambda x: x.get( 'stack_order', 0 ) )
    
    for i, canvas in enumerate( sorted_canvases ):
        if canvas.get( 'active', True ):
            canvas_name = canvas.get('name', f'Screen_{ i }')
            content += generateScreenStructure( canvas_name, canvas )
            
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
        
        content += generateWidgetStructure( widget_type, name, widget )
    
    content += "}\n\n"
    
    for i, canvas in enumerate( sorted_canvases ):
        if canvas.get( 'active', True ):
            name = canvas.get( 'name', f'Screen_{ i }' )
            
            content += f"void ft800_display_task_{ i }()\n"
            content += "{\n"
            content += f"    if( { name }.visible )\n"
            content +=  "    {\n"
            content += f"        ft800_start_display_list( &ctx );\n"
            content += f"        ft800_designer_screen_settings( &ctx, &{ name } );\n"
            
            if 'widgets' in canvas:
                sorted_widgets = sorted( canvas[ 'widgets' ], key = lambda x: x.get( 'stack_order', 0 ) )
                
                for widget in sorted_widgets:
                    if widget.get( 'active', True ):
                        widget_type = widget.get( 'type' )
                        widget_name = widget.get( 'name', f'{ widget_type }_0' )
                        
                        draw_functions = widgetFunctionMapping()
                        
                        if widget_type in draw_functions:
                            content += f"        { draw_functions[ widget_type ] }( &ctx, &{ widget_name } );\n"
            
            content += f"        ft800_end_display_list( &ctx );\n"
            content += "    }\n"
            content += "}\n\n"
    
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
            width = img_widget.image_width
            height = img_widget.image_height
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

            c_content += f"const code uint8_t { var_name }[ { size } ] = {{\n"

            for i in range( 0, size, 16 ):
                line = ", ".join( f"0x{b:02X}" for b in rgb565[ i:i+16 ] )
                c_content += f"    { line },\n"

            c_content += "};\n\n"
            generated_count += 1

        except Exception as e:
            continue
        
    return c_content

def generateResources( main_window, out_dir = None ):
    all_images = []
    canvas_data_dict = main_window.getAllCanvasData()
    
    for canvas_id, canvas_info in canvas_data_dict.items():
        if 'widgets' in canvas_info:
            for widget in canvas_info[ 'widgets' ]:
                if widget.get( 'type' ) == 'Image' and widget.get( 'active', True ):
                    if canvas_id in main_window.canvas_widgets:
                        for widget_obj in main_window.canvas_widgets[ canvas_id ]:
                            if isinstance( widget_obj, ImageWidget ):
                                all_images.append( widget_obj )
    
    if not all_images:
        return
    
    if out_dir is None:
        out_dir = QFileDialog.getExistingDirectory( main_window, "Select output directory for resource files" )
        if not out_dir:
            return
    
    try:
        h_content = generateResourcesH( main_window, all_images )
        c_content = generateResourcesC( main_window, all_images )
        
        if h_content:
            with open( f"{ out_dir }/resource.h", "w", encoding = 'utf-8' ) as h_file:
                h_file.write( h_content )
        
        if c_content:
            with open( f"{ out_dir }/resource.c", "w", encoding = 'utf-8' ) as c_file:
                c_file.write( c_content )
        
        
    except Exception as e:
        QMessageBox.critical( main_window, "Error", f"Failed to generate resource files:\n{ str( e ) }" )

def generateComponents( main_window, out_dir = None ):
    canvas_data_dict = main_window.getAllCanvasData()
    
    if not canvas_data_dict:
        QMessageBox.warning( main_window, "Warning", "No canvas data found!" )
        return
    
    canvas_data = []

    for canvas_id, canvas_info in canvas_data_dict.items():
        canvas_data.append( canvas_info )
    
    if not canvas_data:
        return
    
    if not out_dir:
        return
    
    try:
        h_content = generateComponentsH( canvas_data )
        c_content = generateComponentsC( canvas_data )
        
        with open( f"{ out_dir }/components.h", "w", encoding = 'utf-8' ) as h_file:
            h_file.write( h_content )
        
        with open( f"{ out_dir }/components.c", "w", encoding = 'utf-8' ) as c_file:
            c_file.write( c_content )
        
    except Exception as e:
        QMessageBox.critical( main_window, "Error", f"Failed to generate component files:\n{str( e ) }" )

def printAllCanvasAndWidgetData(self):
    print("\n" + "="*80)
    print("DEBUG: SVE VREDNOSTI IZ REČNIKA ZA CANVASE I WIDGETE")
    print("="*80)

    all_data = self.getAllCanvasData()
    print(f"\nBroj canvasa: {len(all_data)}")

    for canvas_id, canvas_data in all_data.items():
        print(f"\n{'='*60}")
        print(f"CANVAS {canvas_id}:")
        print(f"{'='*60}")


        print(f"  Naziv: {canvas_data.get('name', 'N/A')}")
        print(f"  Aktivan: {canvas_data.get('active', 'N/A')}")
        print(f"  Vidljiv: {canvas_data.get('visible', 'N/A')}")
        print(f"  Static: {canvas_data.get('static', 'N/A')}")
        print(f"  Background color: {canvas_data.get('background_color', 'N/A')}")
        print(f"  Grid enable: {canvas_data.get('grid_enable', 'N/A')}")
        print(f"  Grid color: {canvas_data.get('grid_color', 'N/A')}")
        print(f"  Grid type: {canvas_data.get('grid_type', 'N/A')}")
        print(f"  Grid size: {canvas_data.get('grid_size', 'N/A')}")


        widgets_list = canvas_data.get('widgets', [])
        print(f"\n  Broj widgeta: {len(widgets_list)}")


        for i, widget_data in enumerate(widgets_list):
            print(f"\n  --- WIDGET {i+1} ---")

            widget_type = widget_data.get('type', '')

            if widget_type == 'Circle':
                print(f"    Centar X: {widget_data.get('center_x', 'N/A')}")
                print(f"    Centar Y: {widget_data.get('center_y', 'N/A')}")
                print(f"    Prečnik: {widget_data.get('diameter', 'N/A')}")
                print(f"    Boja ivice: {widget_data.get('edges_color', 'N/A')}")
                print(f"    Debljina ivice: {widget_data.get('edges_width', 'N/A')}")
                print(f"    Popuna: {widget_data.get('filled', 'N/A')}")
                print(f"    Boja popune: {widget_data.get('fill_color', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")

            elif widget_type == 'Ellipse':
                print(f"    Širina elipse: {widget_data.get('ellipse_width', 'N/A')}")
                print(f"    Visina elipse: {widget_data.get('ellipse_height', 'N/A')}")
                print(f"    Centar X: {widget_data.get('center_x', 'N/A')}")
                print(f"    Centar Y: {widget_data.get('center_y', 'N/A')}")
                print(f"    Boja ivica: {widget_data.get('edges_color', 'N/A')}")
                print(f"    Debljina ivica: {widget_data.get('edges_width', 'N/A')}")
                print(f"    Popuna: {widget_data.get('filled', 'N/A')}")
                print(f"    Smer gradijenta: {widget_data.get('gradient_direction', 'N/A')}")
                print(f"    Početna boja gradijenta: {widget_data.get('gradient_start_color', 'N/A')}")
                print(f"    Krajnja boja gradijenta: {widget_data.get('gradient_end_color', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")

            elif widget_type == 'Rectangle':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Width: {widget_data.get('rectangle_width', 'N/A')}")
                print(f"    Height: {widget_data.get('rectangle_height', 'N/A')}")
                print(f"    Edges color: {widget_data.get('edges_color', 'N/A')}")
                print(f"    Edges width: {widget_data.get('edges_width', 'N/A')}")
                print(f"    Filled: {widget_data.get('filled', 'N/A')}")
                print(f"    Gradient type: {widget_data.get('gradient_direction', 'N/A')}")
                print(f"    Start color: {widget_data.get('gradient_start_color', 'N/A')}")
                print(f"    End color: {widget_data.get('gradient_end_color', 'N/A')}")

            elif widget_type == 'Line':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")
                print(f"    Start X: {widget_data.get('start_x', 'N/A')}")
                print(f"    Start Y: {widget_data.get('start_y', 'N/A')}")
                print(f"    End X: {widget_data.get('end_x', 'N/A')}")
                print(f"    End Y: {widget_data.get('end_y', 'N/A')}")
                print(f"    Line color: {widget_data.get('line_color', 'N/A')}")
                print(f"    Line width: {widget_data.get('line_width', 'N/A')}")

            elif widget_type == 'Button':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Button width: {widget_data.get('button_width', 'N/A')}")
                print(f"    Button height: {widget_data.get('button_height', 'N/A')}")
                print(f"    Gradient start color: {widget_data.get('gradient_start_color', 'N/A')}")
                print(f"    Gradient end color: {widget_data.get('gradient_end_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Text: {widget_data.get('text', 'N/A')}")
                print(f"    Text size: {widget_data.get('text_size', 'N/A')}")
                print(f"    Text color: {widget_data.get('text_color', 'N/A')}")

            elif widget_type == 'Keys':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Keys width: {widget_data.get('keys_width', 'N/A')}")
                print(f"    Keys height: {widget_data.get('keys_height', 'N/A')}")
                print(f"    Gradient start color: {widget_data.get('gradient_start_color', 'N/A')}")
                print(f"    Gradient end color: {widget_data.get('gradient_end_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Keys type: {widget_data.get('keys_type', 'N/A')}")
                print(f"    Text size: {widget_data.get('font_size', 'N/A')}")
                print(f"    Text color: {widget_data.get('font_color', 'N/A')}")

            elif widget_type == 'Clock':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Center X: {widget_data.get('center_x', 'N/A')}")
                print(f"    Center Y: {widget_data.get('center_y', 'N/A')}")
                print(f"    Diameter: {widget_data.get('diameter', 'N/A')}")
                print(f"    Background color: {widget_data.get('background_color', 'N/A')}")
                print(f"    Face color: {widget_data.get('face_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Hours: {widget_data.get('hours', 'N/A')}")
                print(f"    Minutes: {widget_data.get('minutes', 'N/A')}")
                print(f"    Seconds: {widget_data.get('seconds', 'N/A')}")

            elif widget_type == 'Gauge':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Center X: {widget_data.get('center_x', 'N/A')}")
                print(f"    Center Y: {widget_data.get('center_y', 'N/A')}")
                print(f"    Diameter: {widget_data.get('diameter', 'N/A')}")
                print(f"    Background color: {widget_data.get('background_color', 'N/A')}")
                print(f"    Face color: {widget_data.get('face_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Major subdivision: {widget_data.get('major_subdivision', 'N/A')}")
                print(f"    Minor subdivision: {widget_data.get('minor_subdivision', 'N/A')}")
                print(f"    Range: {widget_data.get('range', 'N/A')}")
                print(f"    Value: {widget_data.get('value', 'N/A')}")

            elif widget_type == 'Dial':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Center X: {widget_data.get('center_x', 'N/A')}")
                print(f"    Center Y: {widget_data.get('center_y', 'N/A')}")
                print(f"    Diameter: {widget_data.get('diameter', 'N/A')}")
                print(f"    Background color: {widget_data.get('background_color', 'N/A')}")
                print(f"    Pointer color: {widget_data.get('pointer_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Value: {widget_data.get('value', 'N/A')}")

            elif widget_type == 'Toggle':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Toggle width: {widget_data.get('toggle_width', 'N/A')}")
                print(f"    Thumb color: {widget_data.get('thumb_color', 'N/A')}")
                print(f"    Background color: {widget_data.get('background_color', 'N/A')}")
                print(f"    Text color: {widget_data.get('text_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    State: {widget_data.get('state', 'N/A')}")

            elif widget_type == 'Scroll_bar':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Scroll bar width: {widget_data.get('scroll_bar_width', 'N/A')}")
                print(f"    Scroll bar height: {widget_data.get('scroll_bar_height', 'N/A')}")
                print(f"    Thumb color: {widget_data.get('thumb_color', 'N/A')}")
                print(f"    Background color: {widget_data.get('background_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Value: {widget_data.get('current_value', 'N/A')}")
                print(f"    Thumb size: {widget_data.get('thumb_size', 'N/A')}")

            elif widget_type == 'Slider':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Tag: {widget_data.get('tag', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Slider width: {widget_data.get('slider_width', 'N/A')}")
                print(f"    Slider height: {widget_data.get('slider_height', 'N/A')}")
                print(f"    Thumb color: {widget_data.get('thumb_color', 'N/A')}")
                print(f"    Left color: {widget_data.get('left_background_color', 'N/A')}")
                print(f"    Right color: {widget_data.get('right_background_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Value: {widget_data.get('current_value', 'N/A')}")

            elif widget_type == 'Progress_bar':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Progress bar width: {widget_data.get('progress_bar_width', 'N/A')}")
                print(f"    Progress bar height: {widget_data.get('progress_bar_height', 'N/A')}")
                print(f"    Progress color: {widget_data.get('progress_color', 'N/A')}")
                print(f"    Background color: {widget_data.get('background_color', 'N/A')}")
                print(f"    3D: {widget_data.get('effect_3d', 'N/A')}")
                print(f"    Range: {widget_data.get('range', 'N/A')}")
                print(f"    Value: {widget_data.get('current_value', 'N/A')}")

            elif widget_type == 'Image':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Image width: {widget_data.get('image_width', 'N/A')}")
                print(f"    Image height: {widget_data.get('image_height', 'N/A')}")
                print(f"    Frame: {widget_data.get('frame', 'N/A')}")
                print(f"    Frame color: {widget_data.get('frame_color', 'N/A')}")
                print(f"    Frame width: {widget_data.get('frame_width', 'N/A')}")

            elif widget_type == 'Label':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Text color: {widget_data.get('text_color', 'N/A')}")
                print(f"    Text: {widget_data.get('text', 'N/A')}")
                print(f"    Text size: {widget_data.get('text_size', 'N/A')}")
                print(f"    Text alignment: {widget_data.get('text_alignment', 'N/A')}")

            elif widget_type == 'Numeric':
                print(f"    Active: {widget_data.get('active', 'N/A')}")
                print(f"    Visible: {widget_data.get('visible', 'N/A')}")
                print(f"    Static: {widget_data.get('static', 'N/A')}")
                print(f"    Name: {widget_data.get('name', 'N/A')}")
                print(f"    Stack order: {widget_data.get('stack_order', 'N/A')}")
                print(f"    Position X: {widget_data.get('position_x', 'N/A')}")
                print(f"    Position Y: {widget_data.get('position_y', 'N/A')}")
                print(f"    Number color: {widget_data.get('text_color', 'N/A')}")
                print(f"    Number: {widget_data.get('number', 'N/A')}")
                print(f"    Number size: {widget_data.get('number_size', 'N/A')}")
                print(f"    Number alignment: {widget_data.get('number_alignment', 'N/A')}")

            

    print(f"\n{'='*80}")

    