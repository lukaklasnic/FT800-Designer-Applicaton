#--------------------------------------------------GENERATING FILES---------------------------------------------------------------------

# components_generator.py
# Kompletan fajl za generisanje components.c i components.h fajlova

def get_widget_mapping():
    """Mapiranje widget tipova na odgovarajuće strukturne tipove"""
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

def convert_color_to_hex(color_value):
    """Konvertuje boju u heksadecimalni format"""
    if isinstance(color_value, str):
        # Ukloni # ako postoji
        if color_value.startswith('#'):
            color_value = color_value[1:]
        # Proveri dužinu
        if len(color_value) == 6:
            return f"0x{color_value.upper()}"
        elif len(color_value) == 8:
            # Pretpostavljamo da je ARGB format
            return f"0x{color_value[2:].upper()}"
    elif isinstance(color_value, int):
        return f"0x{color_value:06X}"
    return "0x000000"

def convert_bool(value):
    """Konvertuje Python bool u C bool"""
    return 'true' if value else 'false'

def convert_grid_type(grid_type):
    """Konvertuje tip grida"""
    if grid_type == 'dots':
        return 'FT800_GRID_DOTS'
    return 'FT800_GRID_LINE'

def convert_3d_enabled(value):
    """Konvertuje 3D podešavanje"""
    return 'FT800_3D' if value else 'FT800_FLAT'

def convert_alignment(alignment):
    """Konvertuje alignment vrednost"""
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
    return mapping.get(alignment, 'FT800_ALIGN_CENTER')

def convert_gradient_type(gradient_type):
    """Konvertuje tip gradijenta"""
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
    return mapping.get(gradient_type, 'FT800_LEFT_RIGHT_GRADIENT')

def convert_keyboard_type(key_type):
    """Konvertuje tip tastature"""
    mapping = {
        'NUM': 'FT800_KEYBOARD_NUM',
        'QUERTZ': 'FT800_KEYBOARD_QUERTZ',
        'qwertz': 'FT800_KEYBOARD_QUERTZ',
        'num': 'FT800_KEYBOARD_NUM'
    }
    return mapping.get(key_type, 'FT800_KEYBOARD_NUM')

def convert_toggle_state(state):
    """Konvertuje stanje toggle-a"""
    if isinstance(state, str):
        return 'FT800_ON' if state.lower() == 'on' else 'FT800_OFF'
    return 'FT800_ON' if state else 'FT800_OFF'

def generate_widget_structure(widget_type, name, widget_data):
    """Generiše kod za popunjavanje strukture za dati widget"""
    content = ""
    
    if widget_type == 'Line':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x1_coord = {widget_data.get('x1', 0)};\n"
        content += f"    {name}.y1_coord = {widget_data.get('y1', 0)};\n"
        content += f"    {name}.x2_coord = {widget_data.get('x2', 100)};\n"
        content += f"    {name}.y2_coord = {widget_data.get('y2', 0)};\n"
        content += f"    {name}.pen.color = {convert_color_to_hex(widget_data.get('color', 0xFF0000))};\n"
        content += f"    {name}.pen.width = {widget_data.get('width', 1)};\n"
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Rectangle':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 0)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 0)};\n"
        content += f"    {name}.width = {widget_data.get('width', 100)};\n"
        content += f"    {name}.height = {widget_data.get('height', 100)};\n"
        content += f"    {name}.pen.color = {convert_color_to_hex(widget_data.get('edges_color', 0xFF0000))};\n"
        content += f"    {name}.pen.width = {widget_data.get('thickness', 1)};\n"
        
        filled = widget_data.get('filled', True)
        content += f"    {name}.gradient.filled = {convert_bool(filled)};\n"
        
        if filled:
            if widget_data.get('gradient_enable', False):
                gradient_type = widget_data.get('gradient_type', 'left_right')
                content += f"    {name}.gradient.gradient_type = {convert_gradient_type(gradient_type)};\n"
                
                start_color = widget_data.get('gradient_start_color', widget_data.get('fill_color', 0xFF0000))
                content += f"    {name}.gradient.start_color = {convert_color_to_hex(start_color)};\n"
                
                end_color = widget_data.get('gradient_end_color', widget_data.get('fill_color', 0x0000FF))
                content += f"    {name}.gradient.end_color = {convert_color_to_hex(end_color)};\n"
            else:
                fill_color = widget_data.get('fill_color', 0x0000FF)
                content += f"    {name}.gradient.start_color = {convert_color_to_hex(fill_color)};\n"
                content += f"    {name}.gradient.end_color = {convert_color_to_hex(fill_color)};\n"
        
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Circle':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.cx_coord = {widget_data.get('center_x', 100)};\n"
        content += f"    {name}.cy_coord = {widget_data.get('center_y', 100)};\n"
        content += f"    {name}.diameter = {widget_data.get('diameter', 100)};\n"
        content += f"    {name}.pen.color = {convert_color_to_hex(widget_data.get('line_color', 0xFF0000))};\n"
        content += f"    {name}.pen.width = {widget_data.get('line_thickness', 1)};\n"
        
        filled = widget_data.get('filled', True)
        content += f"    {name}.gradient.filled = {convert_bool(filled)};\n"
        
        if filled:
            fill_color = widget_data.get('fill_color', 0x0000FF)
            content += f"    {name}.gradient.start_color = {convert_color_to_hex(fill_color)};\n"
        
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Ellipse':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.cx_coord = {widget_data.get('center_x', 100)};\n"
        content += f"    {name}.cy_coord = {widget_data.get('center_y', 100)};\n"
        content += f"    {name}.width = {widget_data.get('width', 150)};\n"
        content += f"    {name}.height = {widget_data.get('height', 75)};\n"
        content += f"    {name}.pen.color = {convert_color_to_hex(widget_data.get('border_color', 0xCA75FE))};\n"
        content += f"    {name}.pen.width = {widget_data.get('border_width', 1)};\n"
        
        filled = widget_data.get('filled', True)
        content += f"    {name}.gradient.filled = {convert_bool(filled)};\n"
        
        if filled:
            if widget_data.get('gradient_enable', False):
                gradient_type = widget_data.get('gradient_type', 'top_bottom')
                content += f"    {name}.gradient.gradient_type = {convert_gradient_type(gradient_type)};\n"
                
                start_color = widget_data.get('gradient_start_color', widget_data.get('fill_color', 0xFF0000))
                content += f"    {name}.gradient.start_color = {convert_color_to_hex(start_color)};\n"
                
                end_color = widget_data.get('gradient_end_color', widget_data.get('fill_color', 0x0000FF))
                content += f"    {name}.gradient.end_color = {convert_color_to_hex(end_color)};\n"
            else:
                fill_color = widget_data.get('fill_color', 0x0000FF)
                content += f"    {name}.gradient.start_color = {convert_color_to_hex(fill_color)};\n"
                content += f"    {name}.gradient.end_color = {convert_color_to_hex(fill_color)};\n"
        
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Button':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 100)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 100)};\n"
        content += f"    {name}.width = {widget_data.get('width', 100)};\n"
        content += f"    {name}.height = {widget_data.get('height', 100)};\n"
        content += f"    {name}.gradient.start_color = {convert_color_to_hex(widget_data.get('start_color', 0xFF0000))};\n"
        content += f"    {name}.gradient.end_color = {convert_color_to_hex(widget_data.get('end_color', 0x00FF00))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.text.text_caption = \"{widget_data.get('text', 'Press')}\";\n"
        content += f"    {name}.text.text_size = {widget_data.get('text_size', 28)};\n"
        content += f"    {name}.text.text_color = {convert_color_to_hex(widget_data.get('text_color', 0xFF0000))};\n"
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Keys':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 10)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 10)};\n"
        content += f"    {name}.width = {widget_data.get('width', 300)};\n"
        content += f"    {name}.height = {widget_data.get('height', 60)};\n"
        content += f"    {name}.gradient.start_color = {convert_color_to_hex(widget_data.get('key_color_top', 0xFFFF00))};\n"
        content += f"    {name}.gradient.end_color = {convert_color_to_hex(widget_data.get('key_color_bottom', 0xFFFF00))};\n"
        content += f"    {name}.text.text_color = {convert_color_to_hex(widget_data.get('text_color', 0x00FF00))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.type = {convert_keyboard_type(widget_data.get('key_type', 'NUM'))};\n"
        content += f"    {name}.text.text_size = {widget_data.get('text_size', 27)};\n"
    
    elif widget_type == 'Clock':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.cx_coord = {widget_data.get('center_x', 240)};\n"
        content += f"    {name}.cy_coord = {widget_data.get('center_y', 136)};\n"
        content += f"    {name}.diameter = {widget_data.get('diameter', 100)};\n"
        content += f"    {name}.background_color = {convert_color_to_hex(widget_data.get('background_color', 0x0000FF))};\n"    
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.hours = {widget_data.get('hours', 9)};\n"
        content += f"    {name}.minutes = {widget_data.get('minutes', 53)};\n"
        content += f"    {name}.seconds = {widget_data.get('seconds', 0)};\n"
    
    elif widget_type == 'Gauge':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.cx_coord = {widget_data.get('center_x', 100)};\n"
        content += f"    {name}.cy_coord = {widget_data.get('center_y', 100)};\n"
        content += f"    {name}.diameter = {widget_data.get('diameter', 100)};\n"
        content += f"    {name}.background_color = {convert_color_to_hex(widget_data.get('background_color', 0xFF0000))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.major = {widget_data.get('major_subdivision', 6)};\n"
        content += f"    {name}.minor = {widget_data.get('minor_subdivision', 3)};\n"
        content += f"    {name}.range = {widget_data.get('range_value', 100)};\n"
        content += f"    {name}.val = {widget_data.get('value', 50)};\n"
    
    elif widget_type == 'Dial':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.cx_coord = {widget_data.get('center_x', 240)};\n"
        content += f"    {name}.cy_coord = {widget_data.get('center_y', 130)};\n"
        content += f"    {name}.diameter = {widget_data.get('diameter', 50)};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.val = 0x{int(widget_data.get('value', 0.5) * 65535):04X};\n"
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Toggle':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 50)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 50)};\n"
        content += f"    {name}.width = {widget_data.get('width', 40)};\n"
        content += f"    {name}.knob_color = {convert_color_to_hex(widget_data.get('thumb_color', 0xFF00FF))};\n"
        content += f"    {name}.background_color = {convert_color_to_hex(widget_data.get('background_color', 0x0000FF))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.state = {convert_toggle_state(widget_data.get('is_on', False))};\n"
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'ScrollBar':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 100)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 100)};\n"
        content += f"    {name}.width = {widget_data.get('width', 100)};\n"
        content += f"    {name}.height = {widget_data.get('height', 10)};\n"
        content += f"    {name}.knob_color = {convert_color_to_hex(widget_data.get('thumb_color', 0x0000FF))};\n"
        content += f"    {name}.background_color = {convert_color_to_hex(widget_data.get('track_color', 0xFFFF00))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.range = {widget_data.get('range_value', 65535)};\n"
        content += f"    {name}.val = {widget_data.get('current_val', 32767)};\n"
        content += f"    {name}.size = {widget_data.get('knob_size', 1000)};\n"
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'Slider':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 100)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 100)};\n"
        content += f"    {name}.width = {widget_data.get('width', 100)};\n"
        content += f"    {name}.height = {widget_data.get('height', 10)};\n"
        content += f"    {name}.knob_color = {convert_color_to_hex(widget_data.get('knob_color', 0x00FF00))};\n"
        content += f"    {name}.background_color_left = {convert_color_to_hex(widget_data.get('background_left_color', 0xFF0000))};\n"
        content += f"    {name}.background_color_right = {convert_color_to_hex(widget_data.get('background_right_color', 0x0000FF))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.range = {widget_data.get('range_value', 65535)};\n"
        content += f"    {name}.val = {widget_data.get('value', 32767)};\n"
        if 'tag' in widget_data:
            content += f"    {name}.tag = {widget_data['tag']};\n"
    
    elif widget_type == 'ProgressBar':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 100)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 100)};\n"
        content += f"    {name}.width = {widget_data.get('width', 100)};\n"
        content += f"    {name}.height = {widget_data.get('height', 10)};\n"
        content += f"    {name}.progress_color = {convert_color_to_hex(widget_data.get('progress_color', 0xFFFFFF))};\n"
        content += f"    {name}.background_color = {convert_color_to_hex(widget_data.get('background_color', 0xFF0000))};\n"
        content += f"    {name}._3d = {convert_3d_enabled(widget_data.get('3d_enable', True))};\n"
        content += f"    {name}.range = {widget_data.get('max_value', 100)};\n"
        content += f"    {name}.val = {widget_data.get('value', 50)};\n"
    
    elif widget_type == 'Image':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 50)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 50)};\n"
        content += f"    {name}.width = {widget_data.get('width', 200)};\n"
        content += f"    {name}.height = {widget_data.get('height', 100)};\n"
        content += f"    {name}.image_data = &{widget_data.get('name', 'Image_0').replace(' ', '_')}_hex;  \n"
        content += f"    {name}.frame = {convert_bool(widget_data.get('frame_enable', False))};\n"
        if widget_data.get('frame_enable', False):
            content += f"    {name}.pen.color = {convert_color_to_hex(widget_data.get('frame_color', 0xFF0000))};\n"
            content += f"    {name}.pen.width = {widget_data.get('frame_width', 2)};\n"
    
    elif widget_type == 'Label':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 100)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 100)};\n"
        content += f"    {name}.text.text_color = {convert_color_to_hex(widget_data.get('text_color', 0x0000FF))};\n"
        content += f"    {name}.text.text_caption = \"{widget_data.get('text', 'Labela')}\";\n"
        content += f"    {name}.text.text_size = {widget_data.get('text_size', 30)};\n"
        content += f"    {name}.alignment = {convert_alignment(widget_data.get('alignment', 'right'))};\n"
    
    elif widget_type == 'Numeric':
        content += f"    {name}.visible = {convert_bool(widget_data.get('visible', True))};\n"
        content += f"    {name}.x_coord = {widget_data.get('x', 100)};\n"
        content += f"    {name}.y_coord = {widget_data.get('y', 100)};\n"
        content += f"    {name}.num_color = {convert_color_to_hex(widget_data.get('number_color', 0xFF00EF))};\n"
        content += f"    {name}.num = {widget_data.get('number', 3110)};\n"
        content += f"    {name}.num_size = {widget_data.get('number_size', 30)};\n"
        content += f"    {name}.alignment = {convert_alignment(widget_data.get('alignment', 'right'))};\n"
    
    return content

def generate_components_h(canvas_data, widgets_data):
    """
    Generiše components.h fajl sa deklaracijama struktura i funkcija
    """
    
    content = """#ifndef COMPONENTS_H
#define COMPONENTS_H

#include "MikroSDK.Ft800"
"""
    
    # Proveri da li postoje Image widget-i i dodaj resource.h ako ima
    has_images = False
    for canvas in canvas_data:
        if 'widgets' in canvas:
            for widget in canvas['widgets']:
                if widget.get('type') == 'Image' and widget.get('active', True):
                    has_images = True
                    break
        if has_images:
            break
    
    if has_images:
        content += """#include "resource.h"
"""
    
    content += """
extern ft800_t ctx;
extern ft800_cfg_t cfg;
extern tp_drv_t drv;

"""
    
    # Dodaj deklaracije za canvas strukture
    for i, canvas in enumerate(canvas_data):
        if canvas.get('active', True):
            name = canvas.get('name', f'Screen_{i}')
            static_prefix = 'static ' if canvas.get('static', False) else 'extern '
            content += f"{static_prefix}ft800_designer_screen {name};\n"
    
    content += "\n"
    
    # Grupiši widget-e po tipu
    widget_types = {}
    
    for i, canvas in enumerate(canvas_data):
        if 'widgets' in canvas and canvas.get('active', True):
            for widget in canvas['widgets']:
                if widget.get('active', True):
                    widget_type = widget.get('type')
                    if widget_type not in widget_types:
                        widget_types[widget_type] = []
                    widget_types[widget_type].append(widget)
    
    # Mapiranje widget tipova na strukture
    type_mapping = get_widget_mapping()
    
    # Dodaj deklaracije za widget strukture
    for widget_type, widgets in widget_types.items():
        if widget_type in type_mapping:
            for widget in widgets:
                name = widget.get('name', f'{widget_type}_{widgets.index(widget)}')
                static_prefix = 'static ' if widget.get('static', False) else 'extern '
                content += f"{static_prefix}{type_mapping[widget_type]} {name};\n"
    
    content += "\n"
    
    # Deklaracija glavne konfiguracione funkcije
    content += "void ft800_display_configuration();\n"
    
    # Deklaracije funkcija za svaki canvas
    for i, canvas in enumerate(canvas_data):
        if canvas.get('active', True):
            content += f"void ft800_display_task_{i}();\n"
    
    content += "\n#endif\n"
    
    return content

def generate_components_c(canvas_data, widgets_data):
    """
    Generiše components.c fajl sa definicijama struktura i funkcija
    """
    
    content = """#include "components.h"

ft800_t ctx;
ft800_cfg_t cfg;
tp_drv_t drv;

"""
    
    # Dodaj definicije canvas struktura
    for i, canvas in enumerate(canvas_data):
        if canvas.get('active', True):
            name = canvas.get('name', f'Screen_{i}')
            static_prefix = 'static ' if canvas.get('static', False) else ''
            content += f"{static_prefix}ft800_designer_screen {name};\n"
    
    content += "\n"
    
    # Grupiši widget-e po tipu
    widget_types = {}
    
    for i, canvas in enumerate(canvas_data):
        if 'widgets' in canvas and canvas.get('active', True):
            for widget in canvas['widgets']:
                if widget.get('active', True):
                    widget_type = widget.get('type')
                    if widget_type not in widget_types:
                        widget_types[widget_type] = []
                    widget_types[widget_type].append(widget)
    
    # Mapiranje widget tipova na strukture
    type_mapping = get_widget_mapping()
    
    # Dodaj definicije za widget strukture
    for widget_type, widgets in widget_types.items():
        if widget_type in type_mapping:
            for widget in widgets:
                name = widget.get('name', f'{widget_type}_{widgets.index(widget)}')
                static_prefix = 'static ' if widget.get('static', False) else ''
                content += f"{static_prefix}{type_mapping[widget_type]} {name};\n"
    
    content += "\n"
    
    # Dodaj glavnu konfiguracionu funkciju
    content += """
void ft800_display_configuration()
{
    ft800_initialization( &ctx,&cfg, &drv );
"""
    
    # Sortiraj canvas-e po stack order-u (najniži prvi)
    sorted_canvases = sorted(canvas_data, key=lambda x: x.get('stack_order', 0))
    
# U components_generator.py, unutar generate_components_c funkcije
# Ažurirajte deo koji popunjava strukture za canvas-e:

    # Popuni strukture za canvas-e
    for i, canvas in enumerate(sorted_canvases):
        if canvas.get('active', True):
            name = canvas.get('name', f'Screen_{i}')

            # Obavezna polja koja uvek treba da postoje
            # 1. background_color - boja pozadine canvasa
            if '//Popunjavanje strukture za canvas Screen_0' in canvas:
                hex_color = convert_color_to_hex(canvas['background_color'])
                content += f"    {name}.background_color = {hex_color};\n"
            else:
                # Default vrednost ako nije postavljeno
                content += f"    {name}.background_color = 0x000000;\n"

            # 2. grid_enable - da li je grid omogućen
            grid_enable = canvas.get('grid_enable', False)
            content += f"    {name}.grid_enable = {convert_bool(grid_enable)};" 

            # 3. grid_color - boja grida (samo ako je grid omogućen)
            if grid_enable:
                if 'grid_color' in canvas:
                    grid_color = convert_color_to_hex(canvas['grid_color'])
                    content += f"    {name}.grid_color = {grid_color};\n"
                else:
                    # Default boja grida
                    content += f"    {name}.grid_color = 0xFF0000;\n"

            # 4. type - tip grida (samo ako je grid omogućen)
            if grid_enable:
                grid_type = canvas.get('grid_type', 'line')
                content += f"    {name}.type = {convert_grid_type(grid_type)};\n"
            else:
                # Ako grid nije omogućen, postavi default vrednost
                content += f"    {name}.type = FT800_GRID_LINE;\n"

            # 5. grid_size - veličina grida (samo ako je grid omogućen)
            if grid_enable:
                grid_size = canvas.get('grid_size', 20)
                content += f"    {name}.grid_size = {grid_size};\n"
            else:
                # Default vrednost za grid size
                content += f"    {name}.grid_size = 20;\n"

            # Dodajte ovde ostala polja ako postoje u vašoj ft800_designer_screen strukturi
            # Na primer:
            # 6. width - širina canvasa
            if 'width' in canvas:
                content += f"    {name}.width = {canvas['width']};\n"
            else:
                content += f"    {name}.width = 480;\n"

            # 7. height - visina canvasa
            if 'height' in canvas:
                content += f"    {name}.height = {canvas['height']};\n"
            else:
                content += f"    {name}.height = 272;\n"

            # 8. opacity - providnost canvasa (ako postoji u strukturi)
            if 'opacity' in canvas:
                opacity = canvas['opacity']
                # Konvertuj iz 0-100 u 0-255 ako je potrebno
                if opacity > 1:  # Ako je u procentima
                    opacity = int(opacity * 255 / 100)
                content += f"    {name}.opacity = {opacity};\n"

            # 9. rotation - rotacija canvasa (ako postoji u strukturi)
            if 'rotation' in canvas:
                content += f"    {name}.rotation = {canvas['rotation']};\n"

            # 10. scroll_enable - da li je scroll omogućen
            scroll_enable = canvas.get('scroll_enable', False)
            content += f"    {name}.scroll_enable = {convert_bool(scroll_enable)};\n"

            # 11. scroll_x i scroll_y - scroll pozicije
            if scroll_enable:
                scroll_x = canvas.get('scroll_x', 0)
                scroll_y = canvas.get('scroll_y', 0)
                content += f"    {name}.scroll_x = {scroll_x};\n"
                content += f"    {name}.scroll_y = {scroll_y};\n"

            # 12. touch_enable - da li je touch omogućen
            touch_enable = canvas.get('touch_enable', True)
            content += f"    {name}.touch_enable = {convert_bool(touch_enable)};\n"

            # 13. visible - da li je canvas vidljiv
            visible = canvas.get('visible', True)
            content += f"    {name}.visible = {convert_bool(visible)};\n"

            # 14. z_index - Z-order canvasa
            z_index = canvas.get('z_index', i)
            content += f"    {name}.z_index = {z_index};\n"

            # 15. alpha - alpha blending vrednost
            alpha = canvas.get('alpha', 255)
            content += f"    {name}.alpha = {alpha};\n"

            # 16. blend_mode - način mešanja boja
            blend_mode = canvas.get('blend_mode', 'FT800_BLEND_SRC_OVER')
            content += f"    {name}.blend_mode = {blend_mode};\n"

            # 17. antialias - da li je antialiasing omogućen
            antialias = canvas.get('antialias', True)
            content += f"    {name}.antialias = {convert_bool(antialias)};\n"

            # 18. clip_enable - da li je clipping omogućen
            clip_enable = canvas.get('clip_enable', False)
            content += f"    {name}.clip_enable = {convert_bool(clip_enable)};\n"

            # 19. clip_x, clip_y, clip_width, clip_height - clipping region
            if clip_enable:
                clip_x = canvas.get('clip_x', 0)
                clip_y = canvas.get('clip_y', 0)
                clip_width = canvas.get('clip_width', canvas.get('width', 480))
                clip_height = canvas.get('clip_height', canvas.get('height', 272))
                content += f"    {name}.clip_x = {clip_x};\n"
                content += f"    {name}.clip_y = {clip_y};\n"
                content += f"    {name}.clip_width = {clip_width};\n"
                content += f"    {name}.clip_height = {clip_height};\n"

        # Prikupi sve widget-e sortirane po stack order-u unutar svakog canvasa
    all_widgets = []
    for canvas in sorted_canvases:
        if canvas.get('active', True) and 'widgets' in canvas:
            canvas_widgets = sorted(canvas['widgets'], key=lambda x: x.get('stack_order', 0))
            for widget in canvas_widgets:
                if widget.get('active', True):
                    all_widgets.append((canvas, widget))
    
    # Popuni strukture za widget-e
    for canvas, widget in all_widgets:
        widget_type = widget.get('type')
        name = widget.get('name', f'{widget_type}_0')
        
        content += f"\n"
        
        # Generiši kod za widget strukturu
        content += generate_widget_structure(widget_type, name, widget)
    
    content += "}\n\n"
    
    # Generiši display task funkcije za svaki canvas
    for i, canvas in enumerate(sorted_canvases):
        if canvas.get('active', True):
            name = canvas.get('name', f'Screen_{i}')
            
            content += f"""
void ft800_display_task_{i}()
{{
    ft800_start_display_list( &ctx );
    ft800_designer_screen_settings( &ctx, &{name} );
"""
            
            # Dodaj pozive za widget-e u ovom canvas-u, sortirane po stack order-u
            if 'widgets' in canvas:
                sorted_widgets = sorted(canvas['widgets'], key=lambda x: x.get('stack_order', 0))
                
                for widget in sorted_widgets:
                    if widget.get('active', True):
                        widget_type = widget.get('type')
                        widget_name = widget.get('name', f'{widget_type}_0')
                        
                        # Mapiranje funkcija za crtanje
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
                        
                        if widget_type in draw_functions:
                            # Dodaj komentar ako je komentarisano
                            if widget.get('commented', False):
                                content += f"\n"
                            else:
                                content += f"    {draw_functions[widget_type]}(&ctx, &{widget_name});\n"
            
            content += f"""    ft800_end_display_list( &ctx );
}}
"""
    
    return content