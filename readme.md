# Microservice Project - Order history by user email
This project is part of the CampusLinker SaaS application, where we manage user information and shopping carts using Django and Django REST Framework. The project provides API endpoints to interact with the `BuyerInfoModel` and `mcart` models.

## Models

### 1. BuyerInfoModel
This model stores information about buyers, such as their contact details, order history, and other relevant information.

### 2. mcart
This model stores information about items added to the cart by users, including product details, quantity, and other cart-related data.

## API Endpoints

### BuyerInfo API

- **Endpoint:** `http://127.0.0.1:8000/buyerinfo_mcart/api/buyerinfo/`
- **ViewSet:** `BuyerInfoViewSet`
- **Description:** This endpoint provides access to the `BuyerInfoModel`. You can perform CRUD operations on the buyer information through this endpoint.

### mcart API

- **Endpoint:** `http://127.0.0.1:8000/buyerinfo_mcart/api/mcart/`
- **ViewSet:** `mcartViewSet`
- **Description:** This endpoint provides access to the `mcart` model, allowing you to interact with the shopping cart data.

## Data Fetching

You can fetch data from the `BuyerInfoModel` using the `buyerinfo` API endpoint to retrieve and display order history. This data can be filtered by the user's email address to show relevant order history for a specific user.

### Example: Fetching Order History by User Email

To fetch order history for a specific user, you can send a GET request to the `buyerinfo` API endpoint with a filter on the user's email.

```bash
GET http://127.0.0.1:8000/buyerinfo_mcart/api/buyerinfo/?email=user@example.com
```

## Installation
To set up and run the project locally:
1. Clone the repository:
```bash
    git clone https://github.com/sagorluc/Microservice_campus.git
    cd Microservice_campus 
```
1. Install dependencies:
```bash
    pip install -r requirements.txt
```
1. Run migrations:
```bash
    python manage.py migrate
```
1. Run the development server:
```bash
    python manage.py runserver
```

## Access the API:

You can now access the API endpoints at http://127.0.0.1:8000/.


## Usage
* Interact with BuyerInfoModel: Use the /buyerinfo_mcart/api/buyerinfo/ endpoint.

* Interact with mcart: Use the /buyerinfo_mcart/api/mcart/ endpoint.

* Fetch data: Use the endpoints to retrieve and filter data based on user email or other criteria.


