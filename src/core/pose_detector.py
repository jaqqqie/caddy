import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, List, Tuple


class PoseDetector:
    def __init__(self, 
                 static_image_mode: bool = True,
                 model_complexity: int = 2,
                 enable_segmentation: bool = False,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize MediaPipe Pose detector for golf swing analysis.
        
        Args:
            static_image_mode: Whether to detect poses in static images
            model_complexity: Complexity of pose model (0, 1, or 2)
            enable_segmentation: Whether to generate segmentation mask
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def detect_pose(self, image: np.ndarray) -> Optional[Dict]:
        """
        Detect pose landmarks in an image.
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            Dictionary containing pose landmarks and metadata, or None if no pose detected
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.pose.process(rgb_image)
        
        if results.pose_landmarks:
            return {
                'landmarks': results.pose_landmarks,
                'world_landmarks': results.pose_world_landmarks,
                'segmentation_mask': results.segmentation_mask
            }
        
        return None
    
    def extract_landmarks_coordinates(self, pose_results: Dict) -> Dict[str, Tuple[float, float]]:
        """
        Extract landmark coordinates as a dictionary.
        
        Args:
            pose_results: Results from detect_pose method
            
        Returns:
            Dictionary mapping landmark names to (x, y) coordinates
        """
        if not pose_results or 'landmarks' not in pose_results:
            return {}
        
        landmarks = pose_results['landmarks']
        landmark_coords = {}
        
        # Map MediaPipe landmark indices to meaningful names
        landmark_names = {
            0: 'nose', 1: 'left_eye_inner', 2: 'left_eye', 3: 'left_eye_outer',
            4: 'right_eye_inner', 5: 'right_eye', 6: 'right_eye_outer',
            7: 'left_ear', 8: 'right_ear', 9: 'mouth_left', 10: 'mouth_right',
            11: 'left_shoulder', 12: 'right_shoulder', 13: 'left_elbow', 14: 'right_elbow',
            15: 'left_wrist', 16: 'right_wrist', 17: 'left_pinky', 18: 'right_pinky',
            19: 'left_index', 20: 'right_index', 21: 'left_thumb', 22: 'right_thumb',
            23: 'left_hip', 24: 'right_hip', 25: 'left_knee', 26: 'right_knee',
            27: 'left_ankle', 28: 'right_ankle', 29: 'left_heel', 30: 'right_heel',
            31: 'left_foot_index', 32: 'right_foot_index'
        }
        
        for idx, landmark in enumerate(landmarks.landmark):
            if idx in landmark_names:
                landmark_coords[landmark_names[idx]] = (landmark.x, landmark.y)
        
        return landmark_coords
    
    def draw_pose_on_image(self, image: np.ndarray, pose_results: Dict) -> np.ndarray:
        """
        Draw pose landmarks and connections on image.
        
        Args:
            image: Original image
            pose_results: Results from detect_pose method
            
        Returns:
            Image with pose landmarks drawn
        """
        if not pose_results or 'landmarks' not in pose_results:
            return image
        
        annotated_image = image.copy()
        
        # Draw pose landmarks
        self.mp_drawing.draw_landmarks(
            annotated_image,
            pose_results['landmarks'],
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )
        
        return annotated_image
    
    def get_golf_specific_landmarks(self, landmark_coords: Dict[str, Tuple[float, float]]) -> Dict[str, Tuple[float, float]]:
        """
        Extract golf-specific key points for swing analysis.
        
        Args:
            landmark_coords: Dictionary of all landmark coordinates
            
        Returns:
            Dictionary of golf-relevant landmarks
        """
        golf_landmarks = {}
        
        # Key points for golf swing analysis
        key_points = [
            'nose', 'left_shoulder', 'right_shoulder',
            'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist',
            'left_hip', 'right_hip', 'left_knee', 'right_knee',
            'left_ankle', 'right_ankle'
        ]
        
        for point in key_points:
            if point in landmark_coords:
                golf_landmarks[point] = landmark_coords[point]
        
        return golf_landmarks
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'pose'):
            self.pose.close()