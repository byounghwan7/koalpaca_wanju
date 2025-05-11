import random
import re
import hashlib

def get_soil_image_url(address_or_query):
    """
    Get a soil image URL based on the hash of the address/query.
    This function deterministically returns an image URL for a given address
    to ensure consistent image associations.
    
    Args:
        address_or_query (str): Address or query string
        
    Returns:
        str: URL to a soil image
    """
    # List of available soil sample images
    soil_sample_urls = [
        "https://pixabay.com/get/gceac3a9ce515b90e239f181006e66ad4c0d6953cd04742a4fd986d5fc83ca36cad5f6bd380211bd3c749899079602437c6169d22a35bc76a732a4bc528c37c73_1280.jpg",
        "https://pixabay.com/get/gd8c78dee3bbb5a01621e67faca20fc2b809dfe883bbf2a1a73eeb04242f0db5505b46dc551fe4e109a98feb81139e2b2ee545413e1f601d5fa027139821a00aa_1280.jpg",
        "https://pixabay.com/get/g6415bfc34079daa3789ee51ec9a60fe4f8a48ae3c607688c7341f4e15c972123699df3ee9e8653e1b99d5edcf74018b05c681c823a5c99ca26370bb9a1b4a29d_1280.jpg", 
        "https://pixabay.com/get/gc757a96c9da9d909e26f1ed7a2600cc5ecde01195d92307b8cd13a736648a2ed7c10d7e8c116f2cf7d5b56991d582dd8e835813bfe0fdebccdc38b185296a5ad_1280.jpg"
    ]
    
    # Get a consistent index based on the hash of the address/query
    hash_value = int(hashlib.md5(address_or_query.encode()).hexdigest(), 16)
    index = hash_value % len(soil_sample_urls)
    
    return soil_sample_urls[index]

def extract_soil_type_from_text(text):
    """
    Extract soil type from text.
    
    Args:
        text (str): Text to extract soil type from
        
    Returns:
        str or None: Extracted soil type or None if not found
    """
    # Common soil types
    soil_types = [
        "clay", "sandy", "loamy", "silty", "peaty", "chalky", "clay loam", 
        "sandy loam", "silt loam", "sandy clay", "silty clay", "peat", 
        "alluvial", "rocky"
    ]
    
    # Check if any soil type is mentioned in the text
    for soil_type in soil_types:
        if re.search(r'\b' + soil_type + r'\b', text.lower()):
            return soil_type
    
    return None

def format_soil_data(soil_data):
    """
    Format soil data for display.
    
    Args:
        soil_data (dict): Dictionary containing soil data
        
    Returns:
        str: Formatted soil data text
    """
    if not soil_data:
        return "No soil data available."
    
    formatted_text = "Soil Information:\n"
    
    # Add soil types
    if "soil_types" in soil_data and soil_data["soil_types"]:
        formatted_text += "Soil Types: " + ", ".join(soil_data["soil_types"]) + "\n"
    
    # Add locations
    if "locations" in soil_data and soil_data["locations"]:
        formatted_text += "Locations: " + ", ".join(soil_data["locations"]) + "\n"
    
    # Add characteristics
    if "characteristics" in soil_data and soil_data["characteristics"]:
        formatted_text += "Characteristics:\n"
        for char_name, values in soil_data["characteristics"].items():
            formatted_text += f"  {char_name}: {', '.join(values)}\n"
    
    return formatted_text

def generate_sample_questions(soil_types=None):
    """
    Generate sample questions based on available soil types.
    
    Args:
        soil_types (list, optional): List of soil types
        
    Returns:
        list: Sample questions
    """
    base_questions = [
        "What are the characteristics of {} soil?",
        "Is {} soil good for growing vegetables?",
        "How can I improve {} soil?",
        "What is the pH range of {} soil?",
        "What nutrients are typically found in {} soil?",
        "How does {} soil affect drainage?"
    ]
    
    if not soil_types:
        soil_types = ["clay", "sandy", "loamy", "silty", "peaty"]
    
    questions = []
    for soil_type in soil_types:
        # Add 2 random questions for each soil type
        questions.extend([
            random.choice(base_questions).format(soil_type)
            for _ in range(2)
        ])
    
    # Add general questions
    general_questions = [
        "What factors affect soil fertility?",
        "How do I test my soil pH?",
        "What's the difference between topsoil and subsoil?",
        "How does climate affect soil formation?",
        "What crops grow best in alkaline soil?",
        "How often should I sample my soil for testing?"
    ]
    
    questions.extend(random.sample(general_questions, 3))
    
    # Shuffle and return
    random.shuffle(questions)
    return questions[:5]  # Return 5 sample questions
