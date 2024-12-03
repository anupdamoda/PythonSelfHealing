import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import ast

# Load existing CSV
csv_file = "C:\\Users\\aceau\\IdeaProjects\\SeleniumSelfHealingTest\\webpage_elements.csv"
data = pd.read_csv(csv_file)

# Set up Selenium WebDriver
driver = webdriver.Chrome()
url = "C:\\Users\\aceau\\OneDrive\\Documents\\Belong-sample\\BelongSample.html"  # Replace with the target URL
driver.get(url)

# Function to fetch current attributes of elements
def get_element_attributes(element):
    script = """
    var items = {}; 
    for (var i = 0; i < arguments[0].attributes.length; i++) { 
        items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value; 
    } 
    return items;
    """
    return driver.execute_script(script, element)

# Check and update elements
updated_data = []
predictions = []

for _, row in data.iterrows():
    tag_name = row["Tag Name"]
    text = row["Text"]


    try:
        attributes = ast.literal_eval(row["Attributes"]) if isinstance(row["Attributes"], str) else {}
    except (ValueError, SyntaxError):
        attributes = {}

    # attributes = eval(row["Attributes"]) if isinstance(row["Attributes"], str) else {}

    try:
        # Locate element by text or other attributes
        xpath = f"//{tag_name}[contains(text(),'{text}')]"
        element = driver.find_element(By.XPATH, xpath)
        current_attributes = get_element_attributes(element)

        # Compare attributes and make predictions
        if attributes != current_attributes:
            attributes = current_attributes  # Update attributes
            prediction = "Valid"  # Example logic: Mark as valid if updated
        else:
            prediction = "Unchanged"

        predictions.append(prediction)
        updated_data.append({"Tag Name": tag_name, "Text Content": text, "Attributes": str(attributes)})

    except Exception as e:
        predictions.append("Not Found")
        updated_data.append({"Tag Name": tag_name, "Text Content": text, "Attributes": str(attributes)})

# Add predictions to DataFrame
updated_df = pd.DataFrame(updated_data)
updated_df["Prediction"] = predictions

# Save updated data to CSV
updated_df.to_csv(csv_file, index=False)
print(f"CSV updated with predictions: {csv_file}")

driver.quit()
