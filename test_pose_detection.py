#!/usr/bin/env python3
"""
Test script for MediaPipe pose detection setup.
This script creates a simple test image and verifies that the pose detection system works.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.core.pose_detector import PoseDetector
from src.utils.angle_calculator import AngleCalculator
from src.utils.image_utils import ImageUtils


def create_test_image():
    """Create a simple test image with a stick figure."""
    # Create a white background
    img = np.ones((400, 300, 3), dtype=np.uint8) * 255
    
    # Draw a simple stick figure (just for testing)
    # Head
    cv2.circle(img, (150, 50), 20, (0, 0, 0), 2)
    
    # Body
    cv2.line(img, (150, 70), (150, 200), (0, 0, 0), 2)
    
    # Arms
    cv2.line(img, (150, 120), (100, 150), (0, 0, 0), 2)  # Left arm
    cv2.line(img, (150, 120), (200, 150), (0, 0, 0), 2)  # Right arm
    
    # Legs
    cv2.line(img, (150, 200), (120, 300), (0, 0, 0), 2)  # Left leg
    cv2.line(img, (150, 200), (180, 300), (0, 0, 0), 2)  # Right leg
    
    return img


def test_pose_detection_setup():
    """Test if the pose detection system is working properly."""
    print("Testing Golf Swing Analyzer - Pose Detection Setup")
    print("=" * 50)
    
    # Test 1: Create pose detector
    print("1. Testing PoseDetector initialization...")
    try:
        detector = PoseDetector()
        print("   ✓ PoseDetector created successfully")
    except Exception as e:
        print(f"   ✗ Error creating PoseDetector: {e}")
        return False
    
    # Test 2: Create test image
    print("2. Creating test image...")
    try:
        test_img = create_test_image()
        print("   ✓ Test image created successfully")
        
        # Save test image
        ImageUtils.save_image(test_img, "data/sample_images/test_stick_figure.jpg")
        print("   ✓ Test image saved to data/sample_images/test_stick_figure.jpg")
    except Exception as e:
        print(f"   ✗ Error creating test image: {e}")
        return False
    
    # Test 3: Test pose detection
    print("3. Testing pose detection...")
    try:
        pose_results = detector.detect_pose(test_img)
        if pose_results:
            print("   ✓ Pose detection working (pose found in test image)")
        else:
            print("   ⚠ Pose detection working but no pose found in simple test image (this is expected)")
        
        # Test landmark extraction even if no pose found
        landmarks = detector.extract_landmarks_coordinates(pose_results)
        print(f"   ✓ Landmark extraction working (found {len(landmarks)} landmarks)")
    except Exception as e:
        print(f"   ✗ Error in pose detection: {e}")
        return False
    
    # Test 4: Test angle calculation
    print("4. Testing angle calculation...")
    try:
        # Test with dummy landmarks
        dummy_landmarks = {
            'left_shoulder': (0.3, 0.3),
            'left_elbow': (0.2, 0.5),
            'left_wrist': (0.1, 0.7),
            'nose': (0.5, 0.2),
            'left_hip': (0.4, 0.6),
            'right_hip': (0.6, 0.6)
        }
        
        angles = AngleCalculator.calculate_all_golf_angles(dummy_landmarks)
        print(f"   ✓ Angle calculation working (calculated {len([a for a in angles.values() if a is not None])} angles)")
    except Exception as e:
        print(f"   ✗ Error in angle calculation: {e}")
        return False
    
    # Test 5: Test image utilities
    print("5. Testing image utilities...")
    try:
        # Test image loading
        loaded_img = ImageUtils.load_image("data/sample_images/test_stick_figure.jpg")
        if loaded_img is not None:
            print("   ✓ Image loading working")
        
        # Test image resizing
        resized_img = ImageUtils.resize_image(test_img, target_width=200)
        print("   ✓ Image resizing working")
        
        # Test text overlay
        text_img = ImageUtils.add_text_to_image(test_img, "Test Golf Swing Analysis")
        print("   ✓ Text overlay working")
        
        # Save result
        ImageUtils.save_image(text_img, "data/sample_images/test_with_text.jpg")
        print("   ✓ Test result saved to data/sample_images/test_with_text.jpg")
    except Exception as e:
        print(f"   ✗ Error in image utilities: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! The pose detection system is ready.")
    print("\nNext steps:")
    print("- Add real golf swing images to data/sample_images/")
    print("- Test with actual golf swing photos")
    print("- Begin Week 2 development (basic pose detection)")
    
    return True


if __name__ == "__main__":
    success = test_pose_detection_setup()
    if not success:
        print("\n❌ Setup test failed. Please check the error messages above.")
        exit(1)
    else:
        print("\n🎉 Setup test completed successfully!")