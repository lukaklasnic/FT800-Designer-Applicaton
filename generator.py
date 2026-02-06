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
        content += f"    { name }.background_color = { convertColorToHex( widget_data.get( 'background_color', '0xFFFFFF' ) ) };\n"
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

def generateResourcesH(self, all_images):
    if not all_images:
        return None
    
    h_content = ""
    h_content += f"#ifndef NECTO_DESIGNER_RESOURCE_H\n"
    h_content += f"#define NECTO_DESIGNER_RESOURCE_H\n"
    h_content += f"#include \"stdint.h\"\n"
    h_content += "\n"
    
    # Koristimo dictionary da pratimo već generisane slike
    # Ključ je hash ili naziv, vrijednost je var_name
    generated = {}
    
    for idx, img_widget in enumerate(all_images):
        try:
            if not hasattr(img_widget, 'pixmap') or img_widget.pixmap.isNull():
                continue
            
            # Generiši jedinstveni naziv za sliku
            if hasattr(img_widget, 'custom_name') and img_widget.custom_name:
                clean_name = img_widget.custom_name.replace(' ', '_').replace('-', '_')
                var_name = f"{clean_name}_hex"
            else:
                # Koristimo ID widgeta ako postoji, inače indeks
                widget_id = getattr(img_widget, 'widget_id', f"image_{idx}")
                var_name = f"{widget_id}_hex"
            
            # Provjeri da li smo već generisali ovu sliku
            # Napravi ključ od originalne slike
            image_hash = None
            if hasattr(img_widget, 'pixmap'):
                # Pokušaj da dobiješ hash od slike
                try:
                    # Kreiraj jedinstveni identifikator od dimenzija i custom_name
                    width = getattr(img_widget, 'image_width', 0)
                    height = getattr(img_widget, 'image_height', 0)
                    custom_name = getattr(img_widget, 'custom_name', '')
                    image_hash = f"{custom_name}_{width}x{height}"
                except:
                    image_hash = str(id(img_widget))
            
            if image_hash and image_hash in generated:
                # Ova slika je već generisana, preskoči
                continue
            
            h_content += f"extern const code uint8_t {var_name}[];\n"
            if image_hash:
                generated[image_hash] = var_name
            
        except Exception as e:
            continue
        
    h_content += "\n"
    h_content += "#endif\n"
    
    return h_content

def generateResourcesC(self, all_images):
    if not all_images:
        return None

    c_content = ""
    c_content += f"#include \"stdint.h\"\n"
    c_content += f"#include \"resource.h\"\n"
    c_content += "\n"

    # Dictionary za praćenje već generisanih slika
    # Ključ: image_hash, Vrijednost: (var_name, rgb565_data)
    generated_images = {}
    
    for idx, img_widget in enumerate(all_images):
        try:
            if not hasattr(img_widget, 'pixmap') or img_widget.pixmap.isNull():
                continue
            
            # Dobij dimenzije
            width = getattr(img_widget, 'image_width', 100)
            height = getattr(img_widget, 'image_height', 100)
            
            # Provjeri dimenzije
            if width <= 0 or height <= 0:
                continue
            
            # Generiši jedinstveni naziv za sliku
            if hasattr(img_widget, 'custom_name') and img_widget.custom_name:
                clean_name = img_widget.custom_name.replace(' ', '_').replace('-', '_')
                var_name = f"{clean_name}_hex"
            else:
                # Koristimo ID widgeta ako postoji, inače indeks
                widget_id = getattr(img_widget, 'widget_id', f"image_{idx}")
                var_name = f"{widget_id}_hex"
            
            # Kreiraj jedinstveni hash za ovu sliku
            custom_name = getattr(img_widget, 'custom_name', '')
            image_hash = f"{custom_name}_{width}x{height}_{id(img_widget.pixmap) if hasattr(img_widget, 'pixmap') else id(img_widget)}"
            
            # Provjeri da li smo već generisali ovu sliku
            if image_hash in generated_images:
                continue
            
            # Procesuiraj sliku
            image = img_widget.pixmap.toImage()
            
            # Provjeri da li je slika validna
            if image.isNull():
                continue
            
            # Skaliraj sliku na željene dimenzije
            scaled_image = image.scaled(width, height, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            # Konvertuj u RGB888 format
            rgb888_image = scaled_image.convertToFormat(QImage.Format.Format_RGB888)
            
            # Provjeri da li je konverzija uspjela
            if rgb888_image.isNull():
                continue
            
            rgb565 = bytearray()
            
            # Procesuiraj svaki piksel
            for y in range(height):
                for x in range(width):
                    # Dobij boju piksela
                    color = rgb888_image.pixelColor(x, y)
                    if not color.isValid():
                        # Ako boja nije validna, koristi crnu
                        r, g, b = 0, 0, 0
                    else:
                        r = color.red()
                        g = color.green()
                        b = color.blue()
                    
                    # Konvertuj u RGB565
                    r = max(0, min(255, r)) >> 3
                    g = max(0, min(255, g)) >> 2
                    b = max(0, min(255, b)) >> 3
                    
                    value = (r << 11) | (g << 5) | b
                    rgb565.append(value & 0xFF)
                    rgb565.append((value >> 8) & 0xFF)
            
            size = len(rgb565)
            
            # Dodaj u dictionary
            generated_images[image_hash] = (var_name, rgb565, size)
            
        except Exception as e:
            print(f"Error processing image {idx}: {e}")
            continue
    
    # Generiši C kod za sve jedinstvene slike
    for var_name, rgb565, size in generated_images.values():
        c_content += f"const code uint8_t {var_name}[{size}] = {{\n"
        
        for i in range(0, size, 16):
            line = ", ".join(f"0x{b:02X}" for b in rgb565[i:i+16])
            c_content += f"    {line},\n"
        
        c_content += "};\n\n"
        
    return c_content

def generateResources(main_window, out_dir=None):
    all_images = []
    canvas_data_dict = main_window.getAllCanvasData()
    
    # Prikupi sve Image widgete
    for canvas_id, canvas_info in canvas_data_dict.items():
        if 'widgets' in canvas_info:
            for widget in canvas_info['widgets']:
                if widget.get('type') == 'Image' and widget.get('active', True):
                    if canvas_id in main_window.canvas_widgets:
                        for widget_obj in main_window.canvas_widgets[canvas_id]:
                            if isinstance(widget_obj, ImageWidget):
                                # Provjeri da li widget ima jedinstveni ID
                                if not hasattr(widget_obj, 'widget_id'):
                                    # Dodaj jedinstveni ID ako ne postoji
                                    widget_obj.widget_id = f"image_{len(all_images)}"
                                
                                # Dodaj widget samo ako već nije dodan
                                if widget_obj not in all_images:
                                    all_images.append(widget_obj)
    
    if not all_images:
        return
    
    if out_dir is None:
        out_dir = QFileDialog.getExistingDirectory(main_window, "Select output directory for resource files")
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
        QMessageBox.critical(main_window, "Error", f"Failed to generate resource files:\n{str(e)}")

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
