import pandas as pd
import re

# Define dictionaries
dictionaries = {
    'urgency_marketing': {
        'limited', 'limited time', 'limited run', 'limited edition', 'order now',
        'last chance', 'hurry', 'while supplies last', 'before they\'re gone',
        'selling out', 'selling fast', 'act now', 'don\'t wait', 'today only',
        'expires soon', 'final hours', 'almost gone'
    },
    'exclusive_marketing': {
        'exclusive', 'exclusively', 'exclusive offer', 'exclusive deal',
        'members only', 'vip', 'special access', 'invitation only',
        'premium', 'privileged', 'limited access', 'select customers',
        'insider', 'private sale', 'early access'
    }
}

def detect_tactics(text):
    """Detect marketing tactics in text and return results."""
    if pd.isna(text) or not isinstance(text, str):
        return {'urgency_marketing': 0, 'exclusive_marketing': 0, 'matched_terms': []}
    
    text_lower = text.lower()
    results = {'urgency_marketing': 0, 'exclusive_marketing': 0, 'matched_terms': []}
    
    for tactic, terms in dictionaries.items():
        for term in terms:
            if term in text_lower:
                results[tactic] = 1
                results['matched_terms'].append(term)
    
    return results

def process_data(file_path='sample_data.csv'):
    """Process CSV file and add marketing tactic detection."""
    # Load data with robust parsing - try different separators
    try:
        df = pd.read_csv(file_path)
    except pd.errors.ParserError:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    
    # If we got a single column with semicolons, it's likely semicolon-separated
    if len(df.columns) == 1 and ';' in df.columns[0]:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    
    # Debug: Show what we loaded
    print(f"Loaded data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    if 'Statement' not in df.columns:
        print("Available columns:", df.columns.tolist())
        raise ValueError("'Statement' column not found in the CSV file")
    print(f"First few Statement values:")
    print(df['Statement'].head())
    
    # Apply detection to Statement column
    detections = df['Statement'].apply(detect_tactics)
    
    # Extract results into separate columns
    df['urgency_detected'] = [d['urgency_marketing'] for d in detections]
    df['exclusive_detected'] = [d['exclusive_marketing'] for d in detections]
    df['matched_terms'] = [', '.join(d['matched_terms']) for d in detections]
    
    return df

# Main execution
if __name__ == "__main__":
    # Process the data
    result_df = process_data()
    
    # Display results
    print("Processing Results:")
    print("="*50)
    for idx, row in result_df.iterrows():
        if row['urgency_detected'] or row['exclusive_detected']:
            print(f"Row {idx+1}: {row['Statement']}")
            print(f"  Urgency: {row['urgency_detected']}, Exclusive: {row['exclusive_detected']}")
            print(f"  Matched terms: {row['matched_terms']}")
            print()
    
    # Save results
    result_df.to_csv('processed_data.csv', index=False)
    print("Results saved to 'processed_data.csv'")
    
    # Summary statistics
    print(f"\nSummary:")
    print(f"Total statements: {len(result_df)}")
    print(f"Urgency tactics detected: {result_df['urgency_detected'].sum()}")
    print(f"Exclusive tactics detected: {result_df['exclusive_detected'].sum()}")
