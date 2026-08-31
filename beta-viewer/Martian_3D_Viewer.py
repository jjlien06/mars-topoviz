import torch
import numpy as np
from vispy import scene, app
import math

def MartianView(tensor):
 
    #Visualizes a 3D topography tensor using GPU-accelerated volume rendering via Vispy.

    # Move to CPU and convert to NumPy if needed
    if tensor.is_cuda:
        tensor = tensor.cpu()
    volume_data = tensor.numpy()

    # Flip the data along the horizontal axis (axis 1) so that features are oriented correctly
    volume_data = np.flip(volume_data, axis=1)
    
    # Create a Vispy canvas for 3D visualization
    canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
    view = canvas.central_widget.add_view()
    
    # Use an ArcballCamera for a more intuitive "grab-and-rotate" feel
    center = (volume_data.shape[0] / 2,
              volume_data.shape[1] / 2,
              volume_data.shape[2] / 2)
    
    diag = math.sqrt(volume_data.shape[0]**2 +
                     volume_data.shape[1]**2 +
                     volume_data.shape[2]**2)
    
    view.camera = scene.cameras.ArcballCamera(
        fov=60,
        center=center,
        distance=1.5 * diag
    )
    
    # Create a volume visual from the data; threshold determines which values are rendered
    volume = scene.visuals.Volume(
        volume_data, 
        parent=view.scene, 
        threshold=0.5, 
        cmap='viridis'
    )
    
    # Unfreeze the volume to update its properties
    volume.unfreeze()
    
    # Set the rendering method to 'iso' to extract isosurfaces for clearer edges
    volume.method = 'iso'
    volume.iso_threshold = 0.5  # Defines the value at which the surface is extracted
    
    # Optionally, enable shading for better depth cues (if supported)
    try:
        volume.shading = True
    except Exception:
        # Some versions of Vispy might not support shading on Volume visuals.
        pass
    
    # Start the Vispy event loop for interactivity
    app.run()

if __name__ == '__main__':
    # Example: create a dummy tensor representing a 3D sphere
    x_dim, y_dim, z_dim = 100, 100, 50
    xv, yv, zv = np.indices((x_dim, y_dim, z_dim))
    center = np.array([x_dim/2, y_dim/2, z_dim/2])
    radius = min(x_dim, y_dim, z_dim) / 3
    
    # Binary sphere: 1 inside the sphere, 0 outside
    sphere = ((xv - center[0])**2 + (yv - center[1])**2 + (zv - center[2])**2) < radius**2
    tensor_data = torch.from_numpy(sphere.astype(np.float32))
    
    # Visualize the sphere (or replace with your actual tensor)
    MartianView(tensor_data)
