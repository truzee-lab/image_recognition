#!/usr/bin/env python3
"""
Enhanced Garment Classifier
Improved classification with confidence thresholding and better prompts
"""

import os
import json
import torch
import clip
from PIL import Image
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedGarmentClassifier:
    def __init__(self, reference_dir="reference_images_pinterest", confidence_threshold=0.15):
        """
        Initialize the enhanced garment classifier
        
        Args:
            reference_dir: Directory containing reference images
            confidence_threshold: Minimum confidence to classify as garment (vs Others)
        """
        self.reference_dir = reference_dir
        self.confidence_threshold = confidence_threshold
        
        # Load CLIP model
        logger.info("Loading CLIP model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        # Load reference images and create prompts
        self.categories, self.reference_features = self._load_reference_images()
        
        logger.info(f"Loaded {len(self.categories)} categories with reference images")
    
    def _load_reference_images(self):
        """Load reference images and extract features"""
        categories = []
        reference_features = []
        
        if not os.path.exists(self.reference_dir):
            logger.error(f"Reference directory {self.reference_dir} not found!")
            return categories, reference_features
        
        for category_folder in os.listdir(self.reference_dir):
            category_path = os.path.join(self.reference_dir, category_folder)
            if not os.path.isdir(category_path):
                continue
            
            # Load images for this category
            category_images = []
            for file in os.listdir(category_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        image_path = os.path.join(category_path, file)
                        image = Image.open(image_path).convert('RGB')
                        image = self.preprocess(image).unsqueeze(0).to(self.device)
                        category_images.append(image)
                    except Exception as e:
                        logger.warning(f"Failed to load {file}: {e}")
                        continue
            
            if category_images:
                # Stack images and extract features
                try:
                    images_tensor = torch.cat(category_images, dim=0)
                    with torch.no_grad():
                        features = self.model.encode_image(images_tensor)
                        features = features / features.norm(dim=-1, keepdim=True)
                    
                    categories.append(category_folder)
                    reference_features.append(features)
                    
                    logger.info(f"Loaded {len(category_images)} images for {category_folder}")
                    
                except Exception as e:
                    logger.error(f"Failed to process category {category_folder}: {e}")
                    continue
        
        return categories, reference_features
    
    def _create_enhanced_prompts(self, category):
        """Create enhanced text prompts for better classification"""
        base_prompts = [
            f"a {category}",
            f"an {category}",
            f"{category} garment",
            f"{category} clothing",
            f"{category} outfit",
            f"{category} dress",
            f"{category} fashion",
            f"{category} style"
        ]
        
        # Add specific prompts for different garment types
        if "saree" in category.lower():
            base_prompts.extend([
                f"traditional {category}",
                f"indian {category}",
                f"{category} drape",
                f"{category} pallu"
            ])
        elif "lehenga" in category.lower():
            base_prompts.extend([
                f"traditional {category}",
                f"indian {category}",
                f"{category} choli",
                f"{category} skirt"
            ])
        elif "kurti" in category.lower():
            base_prompts.extend([
                f"indian {category}",
                f"{category} top",
                f"{category} tunic",
                f"casual {category}"
            ])
        elif "suit" in category.lower():
            base_prompts.extend([
                f"indian {category}",
                f"{category} set",
                f"traditional {category}",
                f"{category} ensemble"
            ])
        elif "gown" in category.lower():
            base_prompts.extend([
                f"indian {category}",
                f"ethnic {category}",
                f"{category} dress",
                f"formal {category}"
            ])
        
        return base_prompts
    
    def classify_image(self, image_path, top_k=3):
        """
        Classify a single image
        
        Args:
            image_path: Path to the image
            top_k: Number of top predictions to return
            
        Returns:
            dict with classification results
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            
            # Extract image features
            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Calculate similarities with all reference categories
            similarities = []
            for i, category in enumerate(self.categories):
                category_features = self.reference_features[i]
                
                # Calculate similarity with all reference images in this category
                category_similarities = torch.cosine_similarity(
                    image_features, category_features, dim=-1
                )
                
                # Take the maximum similarity for this category
                max_similarity = category_similarities.max().item()
                similarities.append((category, max_similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top predictions
            top_predictions = []
            for category, confidence in similarities[:top_k]:
                top_predictions.append({
                    'category': category,
                    'confidence': confidence,
                    'is_garment': confidence >= self.confidence_threshold
                })
            
            # Determine final classification
            best_match = top_predictions[0]
            final_category = best_match['category'] if best_match['is_garment'] else 'Others'
            final_confidence = best_match['confidence']
            
            return {
                'image_path': image_path,
                'final_classification': final_category,
                'confidence': final_confidence,
                'is_garment': best_match['is_garment'],
                'top_predictions': top_predictions,
                'all_similarities': similarities
            }
            
        except Exception as e:
            logger.error(f"Error classifying {image_path}: {e}")
            return {
                'image_path': image_path,
                'final_classification': 'Error',
                'confidence': 0.0,
                'is_garment': False,
                'error': str(e)
            }
    
    def classify_batch(self, image_paths, top_k=3):
        """
        Classify multiple images
        
        Args:
            image_paths: List of image paths
            top_k: Number of top predictions to return
            
        Returns:
            List of classification results
        """
        results = []
        
        for i, image_path in enumerate(image_paths):
            logger.info(f"Classifying {i+1}/{len(image_paths)}: {os.path.basename(image_path)}")
            result = self.classify_image(image_path, top_k)
            results.append(result)
        
        return results
    
    def evaluate_accuracy(self, test_data):
        """
        Evaluate classification accuracy on test data
        
        Args:
            test_data: List of dicts with 'image_path' and 'true_category'
            
        Returns:
            dict with accuracy metrics
        """
        correct = 0
        total = len(test_data)
        category_accuracy = {}
        
        for item in test_data:
            result = self.classify_image(item['image_path'])
            predicted = result['final_classification']
            true_category = item['true_category']
            
            if predicted == true_category:
                correct += 1
            
            # Track per-category accuracy
            if true_category not in category_accuracy:
                category_accuracy[true_category] = {'correct': 0, 'total': 0}
            
            category_accuracy[true_category]['total'] += 1
            if predicted == true_category:
                category_accuracy[true_category]['correct'] += 1
        
        # Calculate overall accuracy
        overall_accuracy = correct / total if total > 0 else 0
        
        # Calculate per-category accuracy
        for category in category_accuracy:
            cat_total = category_accuracy[category]['total']
            cat_correct = category_accuracy[category]['correct']
            category_accuracy[category]['accuracy'] = cat_correct / cat_total if cat_total > 0 else 0
        
        return {
            'overall_accuracy': overall_accuracy,
            'correct_predictions': correct,
            'total_predictions': total,
            'category_accuracy': category_accuracy
        }

def main():
    """Main function for testing the enhanced classifier"""
    
    print("🚀 Enhanced Garment Classifier")
    print("=" * 40)
    
    # Initialize classifier
    classifier = EnhancedGarmentClassifier(confidence_threshold=0.15)
    
    # Test with a few images
    test_images = [
        "test_images/test1.jpg",
        "test_images/test2.jpg",
        "test_images/test3.jpg"
    ]
    
    # Filter to existing images
    existing_test_images = [img for img in test_images if os.path.exists(img)]
    
    if existing_test_images:
        print(f"Testing with {len(existing_test_images)} images...")
        results = classifier.classify_batch(existing_test_images)
        
        for result in results:
            print(f"\n📸 {os.path.basename(result['image_path'])}")
            print(f"   Classification: {result['final_classification']}")
            print(f"   Confidence: {result['confidence']:.3f}")
            print(f"   Is Garment: {result['is_garment']}")
            
            if 'top_predictions' in result:
                print("   Top 3 predictions:")
                for i, pred in enumerate(result['top_predictions'][:3]):
                    print(f"     {i+1}. {pred['category']}: {pred['confidence']:.3f}")
    else:
        print("No test images found. Run with existing images to test.")

if __name__ == "__main__":
    main() 