import numpy as np
from typing import Tuple, Dict, Optional
import math


class AngleCalculator:
    """Utility class for calculating various angles in golf swing analysis."""
    
    @staticmethod
    def calculate_angle(point1: Tuple[float, float], 
                       point2: Tuple[float, float], 
                       point3: Tuple[float, float]) -> float:
        """
        Calculate angle between three points (point2 is the vertex).
        
        Args:
            point1: First point (x, y)
            point2: Vertex point (x, y)
            point3: Third point (x, y)
            
        Returns:
            Angle in degrees
        """
        # Convert to numpy arrays for easier calculation
        p1 = np.array(point1)
        p2 = np.array(point2)
        p3 = np.array(point3)
        
        # Calculate vectors
        v1 = p1 - p2
        v2 = p3 - p2
        
        # Calculate angle using dot product
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        
        # Clamp to avoid numerical errors
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        # Convert to degrees
        angle = np.arccos(cos_angle) * 180 / np.pi
        
        return angle
    
    @staticmethod
    def calculate_spine_angle(landmarks: Dict[str, Tuple[float, float]]) -> Optional[float]:
        """
        Calculate spine angle (trunk lean).
        
        Args:
            landmarks: Dictionary of landmark coordinates
            
        Returns:
            Spine angle in degrees (relative to vertical), or None if landmarks missing
        """
        if not all(key in landmarks for key in ['nose', 'left_hip', 'right_hip']):
            return None
        
        # Use midpoint between hips as base
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        hip_midpoint = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)
        
        nose = landmarks['nose']
        
        # Calculate angle from vertical (assuming y-axis is vertical)
        spine_vector = (nose[0] - hip_midpoint[0], nose[1] - hip_midpoint[1])
        vertical_vector = (0, -1)  # Pointing up
        
        # Calculate angle
        dot_product = spine_vector[0] * vertical_vector[0] + spine_vector[1] * vertical_vector[1]
        spine_magnitude = math.sqrt(spine_vector[0]**2 + spine_vector[1]**2)
        
        if spine_magnitude == 0:
            return None
        
        cos_angle = dot_product / spine_magnitude
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
        
        angle = math.acos(cos_angle) * 180 / math.pi
        
        return angle
    
    @staticmethod
    def calculate_knee_flex(landmarks: Dict[str, Tuple[float, float]], side: str = 'left') -> Optional[float]:
        """
        Calculate knee flexion angle.
        
        Args:
            landmarks: Dictionary of landmark coordinates
            side: 'left' or 'right'
            
        Returns:
            Knee flexion angle in degrees, or None if landmarks missing
        """
        hip_key = f'{side}_hip'
        knee_key = f'{side}_knee'
        ankle_key = f'{side}_ankle'
        
        if not all(key in landmarks for key in [hip_key, knee_key, ankle_key]):
            return None
        
        hip = landmarks[hip_key]
        knee = landmarks[knee_key]
        ankle = landmarks[ankle_key]
        
        return AngleCalculator.calculate_angle(hip, knee, ankle)
    
    @staticmethod
    def calculate_arm_angle(landmarks: Dict[str, Tuple[float, float]], side: str = 'left') -> Optional[float]:
        """
        Calculate arm angle at elbow.
        
        Args:
            landmarks: Dictionary of landmark coordinates
            side: 'left' or 'right'
            
        Returns:
            Elbow angle in degrees, or None if landmarks missing
        """
        shoulder_key = f'{side}_shoulder'
        elbow_key = f'{side}_elbow'
        wrist_key = f'{side}_wrist'
        
        if not all(key in landmarks for key in [shoulder_key, elbow_key, wrist_key]):
            return None
        
        shoulder = landmarks[shoulder_key]
        elbow = landmarks[elbow_key]
        wrist = landmarks[wrist_key]
        
        return AngleCalculator.calculate_angle(shoulder, elbow, wrist)
    
    @staticmethod
    def calculate_shoulder_alignment(landmarks: Dict[str, Tuple[float, float]]) -> Optional[float]:
        """
        Calculate shoulder alignment angle (relative to horizontal).
        
        Args:
            landmarks: Dictionary of landmark coordinates
            
        Returns:
            Shoulder alignment angle in degrees, or None if landmarks missing
        """
        if not all(key in landmarks for key in ['left_shoulder', 'right_shoulder']):
            return None
        
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        
        # Calculate angle from horizontal
        shoulder_vector = (right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1])
        horizontal_vector = (1, 0)  # Pointing right
        
        # Calculate angle
        dot_product = shoulder_vector[0] * horizontal_vector[0] + shoulder_vector[1] * horizontal_vector[1]
        shoulder_magnitude = math.sqrt(shoulder_vector[0]**2 + shoulder_vector[1]**2)
        
        if shoulder_magnitude == 0:
            return None
        
        cos_angle = dot_product / shoulder_magnitude
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
        
        angle = math.acos(cos_angle) * 180 / math.pi
        
        return angle
    
    @staticmethod
    def calculate_all_golf_angles(landmarks: Dict[str, Tuple[float, float]]) -> Dict[str, Optional[float]]:
        """
        Calculate all relevant golf swing angles.
        
        Args:
            landmarks: Dictionary of landmark coordinates
            
        Returns:
            Dictionary of calculated angles
        """
        angles = {
            'spine_angle': AngleCalculator.calculate_spine_angle(landmarks),
            'left_knee_flex': AngleCalculator.calculate_knee_flex(landmarks, 'left'),
            'right_knee_flex': AngleCalculator.calculate_knee_flex(landmarks, 'right'),
            'left_arm_angle': AngleCalculator.calculate_arm_angle(landmarks, 'left'),
            'right_arm_angle': AngleCalculator.calculate_arm_angle(landmarks, 'right'),
            'shoulder_alignment': AngleCalculator.calculate_shoulder_alignment(landmarks)
        }
        
        return angles