import httpx
import asyncio

async def create_test_user():
    """Create a test user for demonstration"""
    async with httpx.AsyncClient() as client:
        # Register a test user
        register_data = {
            "email": "test@notaria.com",
            "password": "test123"
        }
        
        try:
            response = await client.post(
                "http://localhost:8000/api/v1/auth/register",
                json=register_data
            )
            print(f"Registration response: {response.status_code}")
            if response.status_code == 200:
                print("Test user created successfully!")
            else:
                print(f"Registration failed: {response.text}")
            
            # Login with the test user
            login_data = {
                "email": "test@notaria.com",
                "password": "test123"
            }
            
            response = await client.post(
                "http://localhost:8000/api/v1/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                print(f"Login successful! Token: {token_data['access_token'][:20]}...")
                
                # Test the tutor chat
                chat_data = {
                    "message": "¿Qué documentos necesito para una compraventa de inmueble?"
                }
                
                response = await client.post(
                    "http://localhost:8000/api/v1/tutor/chat",
                    json=chat_data,
                    headers={"Authorization": f"Bearer {token_data['access_token']}"}
                )
                
                if response.status_code == 200:
                    chat_response = response.json()
                    print(f"Tutor response: {chat_response['answer']}")
                else:
                    print(f"Chat failed: {response.text}")
            else:
                print(f"Login failed: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_user())