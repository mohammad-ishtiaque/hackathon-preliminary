# Mofa's Kitchen Buddy - challenge 02


## Technologies Used

*   **Backend:**
    *   FastAPI: For building the API endpoints.
    *   Python: Programming language for backend logic.
    *   sqlite-utils: For managing the SQLite database.
    *   google-generativeai: To leverage Gemini Pro for chatbot.
    *   python-dotenv: For managing environment variables (like API keys).
    *   fastapi-middleware: Library to implement CORS middleware on the back-end.

*   **Frontend:**
    *   HTML: For creating the user interface structure.
    *   CSS: For styling the front-end.
    *   JavaScript: For handling front-end logic and communicating with the backend API.

## Setup Instructions

### Prerequisites


1.  **pip (Python package installer)**
2.  **Google Cloud API Key**: Ensure you have obtained an API Key from Google Cloud for Gemini Pro.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [Your Repository URL]
    cd directory
    ```
2.  **Set up a virtual environment (Optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Linux or macOS
    venv\Scripts\activate # On Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create `.env` file:**
    *   In the root directory, create a file named `.env`.
    *   Add your Google API key:
        ```
        GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
        ```
        *Replace `AIzaSyDf7NCUVVAXleSqbQgc_T5vgKJBH7gBo7s` with your actual key.*
5.  **Run the FastAPI backend:**
    *   Start the server:
        ```bash
        uvicorn main:app --reload
        ```
        *This launches the server at `http://127.0.0.1:8000` by default. Ensure the front-end `index.html` file has the same URL for API calls.*
6.  **Access the Frontend:**  
8.  ```bash
        http-server -p 8000
        ```
  *Open the `[frontend/index.html](http://localhost:9000/)` file in your browser.

## Usage

1.  **Add Ingredients:** Use the input fields to add new ingredients, their quantity, and unit. The updated ingredient list will be displayed below.
2.  **Explore Recipes:**  Browse available recipes in the 'Available Recipes' section.
3.  **Chatbot Interaction:**
    *   Use the chatbot text area to enter your questions or requests.
    *   Click the "Send" button to send your query to the chatbot.
    *   The response will appear in the chatbot response area.
4.  **Add Recipe:**
    * You can add a recipe by providing the necessary information, like Name, Cuisine Type, Taste, Reviews, Preparation Time and Ingredients

## API Endpoints

The following API endpoints are provided by the backend:

*   **Ingredients:**
    *   `GET /ingredients`: Retrieves a list of all available ingredients.
    *   `POST /ingredients`: Adds a new ingredient.
    *   `PUT /ingredients`: Update a existing ingredient.
    *   `DELETE /ingredients`: Delete a  ingredient.
*   **Recipes:**
    *   `GET /recipes`: Retrieves a list of all available recipes.
    *   `POST /recipes`: Adds a new recipe.
*   **Chatbot:**
    *   `POST /chatbot`: Sends a query to the chatbot and receives a response.

## Project Structure
