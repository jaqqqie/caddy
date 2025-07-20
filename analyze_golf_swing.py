#!/usr/bin/env python3
"""
Golf Swing Analysis Script
Analyzes a golf swing image and provides pose detection and angle measurements.
"""

import sys
import os
from src.core.pose_detector import PoseDetector
from src.utils.angle_calculator import AngleCalculator
from src.utils.image_utils import ImageUtils


def analyze_golf_swing_image(image_path: str, output_dir: str = "data/analysis_results"):
    """
    Analyze a golf swing image and save results.
    
    Args:
        image_path: Path to the golf swing image
        output_dir: Directory to save analysis results
    """
    print(f"Analyzing golf swing image: {image_path}")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load image
    print("1. Loading image...")
    image = ImageUtils.load_image(image_path)
    if image is None:
        print("❌ Failed to load image")
        return False
    print(f"   ✓ Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
    
    # Initialize pose detector
    print("2. Initializing pose detector...")
    detector = PoseDetector()
    print("   ✓ PoseDetector initialized")
    
    # Detect pose
    print("3. Detecting pose landmarks...")
    pose_results = detector.detect_pose(image)
    
    if pose_results is None:
        print("   ❌ No pose detected in image")
        print("\nTips for better pose detection:")
        print("   - Ensure the golfer is clearly visible")
        print("   - Use good lighting conditions")
        print("   - Avoid cluttered backgrounds")
        print("   - Make sure the full body is in frame")
        return False
    
    print("   ✓ Pose detected successfully")
    
    # Extract landmarks
    print("4. Extracting landmark coordinates...")
    all_landmarks = detector.extract_landmarks_coordinates(pose_results)
    golf_landmarks = detector.get_golf_specific_landmarks(all_landmarks)
    print(f"   ✓ Extracted {len(golf_landmarks)} golf-specific landmarks")
    
    # Calculate angles
    print("5. Calculating golf swing angles...")
    angles = AngleCalculator.calculate_all_golf_angles(golf_landmarks)
    
    # Display results
    print("\n" + "🏌️ GOLF SWING ANALYSIS RESULTS" + "\n" + "=" * 50)
    
    for angle_name, angle_value in angles.items():
        if angle_value is not None:
            print(f"{angle_name.replace('_', ' ').title():.<30} {angle_value:.1f}°")
        else:
            print(f"{angle_name.replace('_', ' ').title():.<30} Not detected")
    
    # Create annotated image
    print("\n6. Creating analysis visualization...")
    annotated_image = detector.draw_pose_on_image(image, pose_results)
    
    # Add angle information to image
    y_offset = 30
    for angle_name, angle_value in angles.items():
        if angle_value is not None:
            text = f"{angle_name.replace('_', ' ').title()}: {angle_value:.1f}°"
            annotated_image = ImageUtils.add_text_to_image(
                annotated_image, text, (10, y_offset), 
                font_scale=0.6, color=(0, 255, 0)
            )
            y_offset += 25
    
    # Save results
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_analysis.jpg")
    
    if ImageUtils.save_image(annotated_image, output_path):
        print(f"   ✓ Analysis saved to: {output_path}")
    else:
        print("   ❌ Failed to save analysis image")
    
    # Create side-by-side comparison
    comparison_path = os.path.join(output_dir, f"{base_name}_comparison.jpg")
    comparison_image = ImageUtils.create_side_by_side_comparison(
        image, annotated_image, "Original", "Analysis"
    )
    
    if ImageUtils.save_image(comparison_image, comparison_path):
        print(f"   ✓ Comparison saved to: {comparison_path}")
    
    print("\n✅ Analysis complete!")
    return True


def main():
    """Main function to run golf swing analysis."""
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_golf_swing.py <image_path>")
        print("\nExample:")
        print("  python3 analyze_golf_swing.py data/sample_images/golf_swing.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    success = analyze_golf_swing_image(image_path)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()