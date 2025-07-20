import cv2
import numpy as np
from typing import Tuple, Optional
import os


class ImageUtils:
    """Utility functions for image processing and manipulation."""
    
    @staticmethod
    def load_image(image_path: str) -> Optional[np.ndarray]:
        """
        Load an image from file path.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Image as numpy array or None if loading failed
        """
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return None
        
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not load image from {image_path}")
                return None
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> bool:
        """
        Save an image to file.
        
        Args:
            image: Image as numpy array
            output_path: Path where to save the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            success = cv2.imwrite(output_path, image)
            if not success:
                print(f"Error: Could not save image to {output_path}")
                return False
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    @staticmethod
    def resize_image(image: np.ndarray, 
                    target_width: int = None, 
                    target_height: int = None,
                    maintain_aspect_ratio: bool = True) -> np.ndarray:
        """
        Resize an image.
        
        Args:
            image: Input image
            target_width: Target width (optional)
            target_height: Target height (optional)
            maintain_aspect_ratio: Whether to maintain aspect ratio
            
        Returns:
            Resized image
        """
        if target_width is None and target_height is None:
            return image
        
        height, width = image.shape[:2]
        
        if maintain_aspect_ratio:
            if target_width is not None and target_height is not None:
                # Calculate which dimension to use to maintain aspect ratio
                width_ratio = target_width / width
                height_ratio = target_height / height
                ratio = min(width_ratio, height_ratio)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
            elif target_width is not None:
                ratio = target_width / width
                new_width = target_width
                new_height = int(height * ratio)
            else:  # target_height is not None
                ratio = target_height / height
                new_height = target_height
                new_width = int(width * ratio)
        else:
            new_width = target_width or width
            new_height = target_height or height
        
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized
    
    @staticmethod
    def add_text_to_image(image: np.ndarray, 
                         text: str, 
                         position: Tuple[int, int] = (10, 30),
                         font_scale: float = 0.7,
                         color: Tuple[int, int, int] = (0, 255, 0),
                         thickness: int = 2) -> np.ndarray:
        """
        Add text overlay to an image.
        
        Args:
            image: Input image
            text: Text to add
            position: (x, y) position for text
            font_scale: Size of the font
            color: Color in BGR format
            thickness: Thickness of the text
            
        Returns:
            Image with text overlay
        """
        result_image = image.copy()
        
        # Add black background for better text visibility
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        cv2.rectangle(result_image, 
                     (position[0] - 5, position[1] - text_size[1] - 5),
                     (position[0] + text_size[0] + 5, position[1] + 5),
                     (0, 0, 0), -1)
        
        # Add text
        cv2.putText(result_image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)
        
        return result_image
    
    @staticmethod
    def create_side_by_side_comparison(image1: np.ndarray, 
                                     image2: np.ndarray,
                                     title1: str = "Original",
                                     title2: str = "Analysis") -> np.ndarray:
        """
        Create a side-by-side comparison of two images.
        
        Args:
            image1: First image
            image2: Second image
            title1: Title for first image
            title2: Title for second image
            
        Returns:
            Combined side-by-side image
        """
        # Resize images to same height
        height = min(image1.shape[0], image2.shape[0])
        img1_resized = ImageUtils.resize_image(image1, target_height=height)
        img2_resized = ImageUtils.resize_image(image2, target_height=height)
        
        # Create combined image
        combined_width = img1_resized.shape[1] + img2_resized.shape[1]
        combined_image = np.zeros((height, combined_width, 3), dtype=np.uint8)
        
        # Place images side by side
        combined_image[:, :img1_resized.shape[1]] = img1_resized
        combined_image[:, img1_resized.shape[1]:] = img2_resized
        
        # Add titles
        combined_image = ImageUtils.add_text_to_image(combined_image, title1, (10, 30))
        combined_image = ImageUtils.add_text_to_image(combined_image, title2, 
                                                    (img1_resized.shape[1] + 10, 30))
        
        return combined_image
    
    @staticmethod
    def convert_coordinates_to_pixels(normalized_coords: Tuple[float, float], 
                                    image_shape: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert normalized coordinates (0-1) to pixel coordinates.
        
        Args:
            normalized_coords: (x, y) coordinates in range [0, 1]
            image_shape: (height, width) of the image
            
        Returns:
            (x, y) pixel coordinates
        """
        height, width = image_shape[:2]
        x_pixel = int(normalized_coords[0] * width)
        y_pixel = int(normalized_coords[1] * height)
        return (x_pixel, y_pixel)