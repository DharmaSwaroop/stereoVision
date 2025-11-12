import inkex
import copy
from lxml import etree
import os

shift_map = {
    "max": 5,
    "moderate": 2.5,
    "conservative": 1
}

def transform_to_left_view(left_doc,window_layer,depth_mode):
    
    root = left_doc.getroot()
    shift_value = shift_map.get(depth_mode,5)
    layers = root.findall(".//{http://www.w3.org/2000/svg}g")

    window_index = None
    for i, layer in enumerate(layers):
        label = layer.get("{http://www.inkscape.org/namespaces/inkscape}label", "")
        if label == window_layer:
            window_index = i
            break
    
    if window_index is None:
        raise ValueError(f"Window layer '{window_layer}' not found!")
    
    for i, layer in enumerate(layers):
        label = layer.get("{http://www.inkscape.org/namespaces/inkscape}label", "")
        if i < window_index: 
            dx = -(window_index-i)*shift_value
        elif i == window_index:
            dx = 0
        else:
            dx = (i-window_index)*shift_value

        transform = inkex.Transform(layer.get("transform"))
        transform.add_translate(dx, 0)
        layer.set("transform", str(transform))



def transform_to_right_view(right_doc,window_layer,depth_mode):
    
    root = right_doc.getroot()
    shift_value = shift_map.get(depth_mode,5)
    layers = root.findall(".//{http://www.w3.org/2000/svg}g")

    window_index = None
    for i, layer in enumerate(layers):
        label = layer.get("{http://www.inkscape.org/namespaces/inkscape}label", "")
        if label == window_layer:
            window_index = i
            break
    
    if window_index is None:
        raise ValueError(f"Window layer '{window_layer}' not found!")
    
    for i, layer in enumerate(layers):
        label = layer.get("{http://www.inkscape.org/namespaces/inkscape}label", "")
        if i < window_index: 
            dx = (window_index-i)*shift_value
        elif i == window_index:
            dx = 0
        else:
            dx = -(i-window_index)*shift_value

        transform = layer.get("transform", "")
        if transform:
            transform += f" translate({dx},0)"
        else:
            transform = f"translate({dx},0)"
        layer.set("transform", transform)    


def combine_side_by_side(left_doc, right_doc, output_file="stereo_side_by_side_layers.svg"):
    left_root = left_doc.getroot()
    right_root = right_doc.getroot()

    # Parse dimensions (width and height) in pixels
    width_str = left_root.get("width", "1000").replace("mm", "").replace("px", "")
    height_str = left_root.get("height", "1000").replace("mm", "").replace("px", "")
    width = float(width_str)
    height = float(height_str)

    # Create new combined SVG root
    nsmap = left_root.nsmap
    combined_svg = etree.Element("{http://www.w3.org/2000/svg}svg", nsmap=nsmap)
    combined_svg.set("width", f"{2 * width}mm")
    combined_svg.set("height", f"{height}mm")
    combined_svg.set("viewBox", f"0 0 {2 * width} {height}")

    # Extract layers from both SVGs
    left_layers = {layer.get("{http://www.inkscape.org/namespaces/inkscape}label"): layer
                   for layer in left_root.findall(".//{http://www.w3.org/2000/svg}g[@inkscape:groupmode='layer']")}

    right_layers = {layer.get("{http://www.inkscape.org/namespaces/inkscape}label"): layer
                    for layer in right_root.findall(".//{http://www.w3.org/2000/svg}g[@inkscape:groupmode='layer']")}

    # Combine layers
    for label, left_layer in left_layers.items():
        combined_layer = etree.Element("{http://www.w3.org/2000/svg}g")
        combined_layer.set("{http://www.inkscape.org/namespaces/inkscape}groupmode", "layer")
        combined_layer.set("{http://www.inkscape.org/namespaces/inkscape}label", label)
        combined_layer.set("style", "display:inline")

        # --- LEFT SIDE ---
        left_group = etree.Element("{http://www.w3.org/2000/svg}g")
        layer_transform = left_layer.get("transform", "")
        if layer_transform:
            left_group.set("transform", layer_transform)
        for child in left_layer:
            left_group.append(copy.deepcopy(child))
        combined_layer.append(left_group)

        # --- RIGHT SIDE ---
        right_group = etree.Element("{http://www.w3.org/2000/svg}g")
        if label in right_layers:
        # preserve the layer's transform from right_doc
            layer_transform = right_layers[label].get("transform", "")
            if layer_transform:
                right_group.set("transform", f"{layer_transform} translate({width},0)")
            else:
                right_group.set("transform", f"translate({width},0)")

            for child in right_layers[label]:
                right_group.append(copy.deepcopy(child))

        combined_layer.append(right_group)

        # Add combined layer to SVG
        combined_svg.append(combined_layer)

    # Write output file
    tree = etree.ElementTree(combined_svg)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


class StereoscopicExtension(inkex.EffectExtension):

    def add_arguments(self, pars):
        # Read all the parameters
        pars.add_argument("--window_layer", type=str, default="Layer 1")
        pars.add_argument("--depth_mode", default="moderate")
        pars.add_argument("--export_left_right", type=inkex.Boolean, default=False)
        pars.add_argument("--export_side_by_side", type=inkex.Boolean, default=False)
        pars.add_argument("--export_png", type=inkex.Boolean, default=False)
        pars.add_argument("--export_svg", type=inkex.Boolean, default=False)        
        pars.add_argument("--png_resolution", type=float, default=300.0)
        pars.add_argument("--directory", type=str, default="")

    def effect(self):
        
    
        layers = [layer.get('inkscape:label') for layer in self.svg.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)]
        window_layer = self.options.window_layer
        depth_mode = self.options.depth_mode
        output_dir = self.options.directory
        if not os.path.isdir(output_dir):
            raise ValueError(f"{output_dir} is not a valid directory")
 
        if window_layer not in layers:
            inkex.utils.debug(f"Warning: '{window_layer}' not found. Choose one of: {layers}")

        else: 
            left_doc = copy.deepcopy(self.document)
            right_doc = copy.deepcopy(self.document)
            transform_to_left_view(left_doc,window_layer,depth_mode)
            transform_to_right_view(right_doc,window_layer,depth_mode)
            left_svg_path = os.path.join(output_dir, "left_view.svg")
            right_svg_path = os.path.join(output_dir, "right_view.svg")
            combined_svg_path = os.path.join(output_dir, "stereo_side_by_side_layers.svg")

            if self.options.export_left_right:
                left_doc.write(left_svg_path, encoding="utf-8", xml_declaration=True)
                right_doc.write(right_svg_path, encoding="utf-8", xml_declaration=True)

            if self.options.export_side_by_side:
                combine_side_by_side(left_doc, right_doc, output_file=combined_svg_path)

            if self.options.export_png:
                left_png_path = os.path.join(output_dir, "left_view.png")
                right_png_path = os.path.join(output_dir, "right_view.png")
                combined_png_path = os.path.join(output_dir, "stereo_side_by_side_layers.png")
                inkex.command.inkscape(
                    "stereo_side_by_side_layers.svg",
                    "--export-type=png",
                    f"--export-dpi={self.options.png_resolution}",
                    f"--export-filename={combined_png_path}"
                )
                inkex.command.inkscape(
                    os.path.join(output_dir, "left_view.svg"),
                    "--export-type=png",
                    f"--export-dpi={self.options.png_resolution}",
                    f"--export-filename={left_png_path}"
                )
                inkex.command.inkscape(
                    os.path.join(output_dir, "right_view.svg"),
                    "--export-type=png",
                    f"--export-dpi={self.options.png_resolution}",
                    f"--export-filename={right_png_path}"
                )
            
        



if __name__ == "__main__":
    StereoscopicExtension().run()
    

