"""
Example usage of the Math Explanation Backend API.
Demonstrates how to use the endpoints programmatically.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_status():
    """Test the status endpoint."""
    print("Testing status endpoint...")
    response = requests.get(f"{BASE_URL}/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def solve_text_problem(problem, generate_audio=True, generate_video=True):
    """
    Solve a text-based math problem.
    
    Args:
        problem: The math problem as a string
        generate_audio: Whether to generate audio narration
        generate_video: Whether to generate video animation
    """
    print(f"Solving text problem: {problem}")
    print(f"Options: audio={generate_audio}, video={generate_video}")
    
    payload = {
        "problem": problem,
        "generate_audio": generate_audio,
        "generate_video": generate_video
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/solve_text",
            json=payload,
            timeout=120  # 2 minute timeout
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            
            if result.get('success'):
                data = result.get('data', {})
                
                print("\n📊 Results:")
                print(f"- Solution length: {len(data.get('solution', ''))} characters")
                print(f"- Script length: {len(data.get('teaching_script', ''))} characters")
                
                if 'audio' in data:
                    print(f"- Audio: {data['audio'].get('url')}")
                
                if 'video' in data:
                    print(f"- Video: {data['video'].get('url')}")
                
                return result
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ Request failed: {response.text}")
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out (video generation can take a while)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()


def solve_pdf_problem(pdf_path, generate_audio=True, generate_video=True):
    """
    Solve problems from a PDF worksheet.
    
    Args:
        pdf_path: Path to the PDF file
        generate_audio: Whether to generate audio narration
        generate_video: Whether to generate video animation
    """
    print(f"Solving PDF: {pdf_path}")
    print(f"Options: audio={generate_audio}, video={generate_video}")
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            data = {
                'generate_audio': str(generate_audio).lower(),
                'generate_video': str(generate_video).lower()
            }
            
            response = requests.post(
                f"{BASE_URL}/api/solve_pdf",
                files=files,
                data=data,
                timeout=180  # 3 minute timeout
            )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            
            if result.get('success'):
                data = result.get('data', {})
                print(f"\n📊 Found {data.get('problems_count', 0)} problem(s)")
                
                for i, problem in enumerate(data.get('problems', [])):
                    print(f"\nProblem {i + 1}:")
                    print(f"- Solution length: {len(problem.get('solution', ''))} characters")
                    
                    if 'audio' in problem:
                        print(f"- Audio: {problem['audio'].get('url')}")
                    
                    if 'video' in problem:
                        print(f"- Video: {problem['video'].get('url')}")
                
                return result
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ Request failed: {response.text}")
    
    except FileNotFoundError:
        print(f"❌ PDF file not found: {pdf_path}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out (processing PDFs can take a while)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()


def main():
    """Run example usage demonstrations."""
    print("=" * 60)
    print("Math Explanation Backend - Example Usage")
    print("=" * 60)
    print()
    
    # Check if server is running
    try:
        test_health_check()
        test_status()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running:")
        print("   python app.py")
        return
    
    # Example 1: Simple algebra problem (solution only)
    print("\n" + "=" * 60)
    print("Example 1: Solve algebra problem (solution only)")
    print("=" * 60 + "\n")
    
    solve_text_problem(
        problem="Solve for x: 2x + 5 = 13",
        generate_audio=False,
        generate_video=False
    )
    
    # Example 2: Calculus problem with audio
    print("\n" + "=" * 60)
    print("Example 2: Calculus problem with audio")
    print("=" * 60 + "\n")
    
    solve_text_problem(
        problem="Find the derivative of f(x) = x^2 + 3x - 5",
        generate_audio=True,
        generate_video=False
    )
    
    # Example 3: Full pipeline (uncomment to test video generation)
    # print("\n" + "=" * 60)
    # print("Example 3: Full pipeline with audio and video")
    # print("=" * 60 + "\n")
    # 
    # solve_text_problem(
    #     problem="What is the area of a circle with radius 5?",
    #     generate_audio=True,
    #     generate_video=True
    # )
    
    # Example 4: PDF upload (uncomment and provide PDF path)
    # print("\n" + "=" * 60)
    # print("Example 4: Process PDF worksheet")
    # print("=" * 60 + "\n")
    # 
    # solve_pdf_problem(
    #     pdf_path="path/to/your/worksheet.pdf",
    #     generate_audio=True,
    #     generate_video=True
    # )
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

