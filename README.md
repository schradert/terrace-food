# Access .docx via Google Drive
Google Client Library installation
```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```

Ask for `credentials.json` and `.env`! (Email [schrader.tristan@gmail.com])

Run `drive_access.ipynb` for file download

# Sneak peek at JSON from `organize_data.py`

```
[
    ...,
    {
        "weekday": "Wednesday",
        "date": "2019-09-11",
        "dishes": [
            {
                "type": "soup",
                "tags": [
                    "Dairy"
                ],
                "name": "Shrimp Shumai Dumpling Soup"
            },
            {
                "type": "entree",
                "tags": [
                    "Dairy"
                ],
                "name": "Chicken Egg Foo Young"
            },
            {
                "type": "entree",
                "tags": [
                    "Gluten-Free"
                ],
                "name": "Chinese Ginger Sesame Salmon Fillet"
            },
            {
                "type": "entree",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Baked 5 Spice Seasoned Tofu"
            },
            {
                "type": "side",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Vegetable Fried Rice"
            },
            {
                "type": "side",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Garlic Oil Snow Peas and Onions"
            },
            {
                "type": "side",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Vegetable Chow Fun"
            },
            {
                "type": "dessert",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Rice Pudding and Sugar Cookies"
            }
        ],
        "theme": "Chinese Day"
    },
    {
        "weekday": "Thursday",
        "date": "2019-09-12",
        "dishes": [
            {
                "type": "soup",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Lentil Vegetable Soup"
            },
            {
                "type": "entree",
                "tags": [],
                "name": "Fresh Catch of the Day*"
            },
            {
                "type": "entree",
                "tags": [
                    "Gluten-Free"
                ],
                "name": "Sriracha Tomato Beef Pot Roast"
            },
            {
                "type": "entree",
                "tags": [
                    "Vegan"
                ],
                "name": "Balsamic Glazed Edamame Chia Burger"
            },
            {
                "type": "side",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Whipped Garlic Potatoes"
            },
            {
                "type": "side",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Chopped Steamed Collard Greens"
            },
            {
                "type": "side",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Pasta w. Artichokes and Roasted Peppers"
            },
            {
                "type": "dessert",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Funnel Cake with Powdered Sugar"
            }
        ]
    },
    {
        "weekday": "Friday",
        "date": "2019-09-13",
        "dishes": [
            {
                "type": "soup",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Smoky Chipotle Mushroom Chili"
            },
            {
                "type": "entree",
                "tags": [
                    "Dairy"
                ],
                "name": "Chicken and Cheddar Burrito"
            },
            {
                "type": "entree",
                "tags": [
                    "Gluten-Free"
                ],
                "name": "Beef and Chili Tamale in Corn Husk"
            },
            {
                "type": "entree",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Pan Seared Tofu with Roasted Pablanos"
            },
            {
                "type": "side",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Mexican Rice and Black Beans"
            },
            {
                "type": "side",
                "tags": [
                    "Vegan",
                    "Gluten-Free"
                ],
                "name": "Roasted Butternut Squash"
            },
            {
                "type": "side",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Vegetarian Layered Tortilla Lasagna"
            },
            {
                "type": "dessert",
                "tags": [
                    "Vegetarian",
                    "Dairy"
                ],
                "name": "Toasted Almond Cream Cake"
            }
        ],
        "theme": "MEXICAN"
    },
    ...,
]
```

## Data to be hosted soon!